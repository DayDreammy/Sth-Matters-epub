#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Workflow helpers for deep/quick search orchestration.

This module centralizes the handoff between the AI agent (produces JSON)
and the Python document generators (consume JSON), making it easier to
test with injected runners and fixtures.
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Callable, Dict, List, Optional

RunnerResult = subprocess.CompletedProcess
CommandRunner = Callable[[List[str], Optional[str]], RunnerResult]
ClaudeInvoker = Callable[[str, str], RunnerResult]


def build_deep_search_prompt(topic: str) -> str:
    """Construct the deep-search prompt aligning with refactor.md."""
    return (
        "@config/ai_prompt.md and perform the Deep Search for topic: "
        f"'{topic}'. Focus on Phase 1 (Exploration) and Phase 2 (Synthesis). "
        "Save the knowledge index JSON to output/[topic]_index.json as STRICT valid JSON (escape all quotes inside strings). "
        "On the very last line, print the absolute path to that JSON wrapped in triple brackets. "
        "Do not run Python generators."
    )


def extract_index_path(stdout: str) -> str:
    """Extract [[[ /abs/path ]]] marker from Claude stdout."""
    match = re.search(r"\[\[\[\s*(.*?)\s*\]\]\]\s*$", stdout.strip(), re.MULTILINE)
    if not match:
        raise ValueError("未找到索引文件路径标记 ([[[ ... ]]]).")
    return match.group(1).strip()


def default_runner(cmd: List[str], cwd: Optional[str] = None) -> RunnerResult:
    """Run a command with capture; raises on non-zero exit."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )


def find_generated_documents(output_dir: str, topic: str) -> Dict[str, str]:
    """Locate generated documents for the topic."""
    patterns = {
        "md": f"{topic}_source_based_文档.md",
        "html": f"{topic}_html_文档.html",
        "epub": f"{topic}_*.epub",
    }
    found: Dict[str, str] = {}
    base_path = Path(output_dir)
    if not base_path.exists():
        return found

    for file_type, pattern in patterns.items():
        matches = sorted(base_path.glob(pattern), key=os.path.getmtime, reverse=True)
        if matches:
            found[file_type] = str(matches[0])
    return found


def run_document_generators(
    index_path: str,
    kb_dir: str,
    output_dir: Optional[str] = None,
    runner: CommandRunner = default_runner,
    base_dir: Optional[str] = None,
) -> Dict[str, str]:
    """Run Markdown/HTML and EPUB generators for a given index."""
    index_path = os.path.abspath(index_path)
    kb_dir = os.path.abspath(kb_dir)
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(index_path), "..", "output")
    output_dir = os.path.abspath(output_dir)
    base_dir = base_dir or os.getcwd()

    md_cmd = [
        "python",
        "src/document_generator/md_generator.py",
        "-i",
        index_path,
        "-o",
        output_dir,
        "-k",
        kb_dir,
        "-l",
        "all",
    ]
    epub_cmd = [
        "python",
        "src/document_generator/epub_cli.py",
        "-i",
        index_path,
        "-o",
        output_dir,
        "-k",
        kb_dir,
    ]

    runner(md_cmd, cwd=base_dir)
    runner(epub_cmd, cwd=base_dir)

    # Topic name drives file naming
    with open(index_path, "r", encoding="utf-8") as f:
        topic = json.load(f).get("metadata", {}).get("topic", "topic")

    return find_generated_documents(output_dir, topic)


def call_claude(
    prompt: str,
    base_dir: str,
    claude_path: str,
    runner: CommandRunner = default_runner,
) -> RunnerResult:
    """Invoke Claude CLI with the provided prompt."""
    command = [
        claude_path,
        "-p",
        prompt,
        "--allowedTools",
        "Bash,Read,Write,Edit,Grep,Glob",
    ]
    return runner(command, cwd=base_dir)


def run_deep_search_workflow(
    topic: str,
    base_dir: str,
    kb_dir: str,
    output_dir: Optional[str] = None,
    claude_invoker: Optional[ClaudeInvoker] = None,
    generator_runner: CommandRunner = default_runner,
    claude_path: Optional[str] = None,
) -> Dict[str, object]:
    """Full deep-search workflow: invoke AI, parse path, run generators."""
    output_dir = output_dir or os.path.join(base_dir, "output")
    prompt = build_deep_search_prompt(topic)

    if claude_invoker is None:
        if not claude_path:
            raise FileNotFoundError("未找到 Claude CLI 路径。")
        claude_invoker = lambda pr, cwd: call_claude(
            pr, cwd, claude_path, runner=generator_runner
        )

    claude_result = claude_invoker(prompt, base_dir)
    if getattr(claude_result, "returncode", 1) != 0:
        return {
            "success": False,
            "error": "Claude CLI 执行失败",
            "stdout": getattr(claude_result, "stdout", ""),
            "stderr": getattr(claude_result, "stderr", ""),
        }

    try:
        index_path = extract_index_path(getattr(claude_result, "stdout", ""))
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": getattr(claude_result, "stdout", ""),
        }

    if not os.path.isabs(index_path):
        index_path = os.path.abspath(os.path.join(base_dir, index_path))

    if not os.path.exists(index_path):
        return {
            "success": False,
            "error": f"索引文件不存在: {index_path}",
            "stdout": getattr(claude_result, "stdout", ""),
        }

    files = run_document_generators(
        index_path=index_path,
        kb_dir=kb_dir,
        output_dir=output_dir,
        runner=generator_runner,
        base_dir=base_dir,
    )

    return {
        "success": len(files) > 0,
        "index_path": index_path,
        "files": files,
        "stdout": getattr(claude_result, "stdout", ""),
    }

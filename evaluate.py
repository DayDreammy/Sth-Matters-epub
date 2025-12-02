#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""End-to-end evaluator for quick and deep search flows.

Usage:
  python evaluate.py --mode quick
  python evaluate.py --mode deep --deep-topic 社会化
  python evaluate.py --mode both
"""

import argparse
import glob
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, Optional

# Make src importable
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from quick_search import perform_quick_search  # noqa: E402
from workflow import run_document_generators  # noqa: E402
from rpa import DeepSearchRPA  # noqa: E402


@dataclass
class CheckResult:
    name: str
    success: bool
    detail: str = ""


def _print_header(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def _verify_outputs(output_dir: str, topic: str) -> Dict[str, str]:
    """Return found files (md/html/epub) for a topic."""
    patterns = {
        "md": f"*{topic}*source_based_文档.md",
        "html": f"*{topic}*_html_文档.html",
        "epub": f"*{topic}*.epub",
    }
    found = {}
    for kind, pattern in patterns.items():
        matches = glob.glob(os.path.join(output_dir, pattern))
        matches.sort(key=os.path.getmtime, reverse=True)
        if matches:
            found[kind] = matches[0]
    return found


def run_quick(topic: str, base_dir: str) -> CheckResult:
    _print_header(f"[Quick] Searching '{topic}'")
    result = perform_quick_search(topic, base_dir)
    if not result["success"]:
        return CheckResult("quick", False, result.get("error", "搜索失败"))

    index_path = result.get("index_file_path")
    if not index_path or not os.path.exists(index_path):
        return CheckResult("quick", False, "未找到快速搜索索引文件")

    kb_dir = os.path.join(base_dir, "knowledge_base", "sth-matters")
    output_dir = os.path.join(base_dir, "output")
    run_document_generators(
        index_path=index_path,
        kb_dir=kb_dir,
        output_dir=output_dir,
        base_dir=base_dir,
    )

    files = _verify_outputs(output_dir, topic)
    if len(files) < 3:
        return CheckResult("quick", False, f"生成文件缺失: {files}")

    with open(files["md"], "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("#"):
        return CheckResult("quick", False, "Markdown 文件缺少标题")

    print("Quick search OK:", files)
    return CheckResult("quick", True, json.dumps(files, ensure_ascii=False))


def run_deep(topic: str, base_dir: str) -> CheckResult:
    _print_header(f"[Deep] Searching '{topic}'")
    rpa = DeepSearchRPA(base_dir=base_dir)
    result = rpa.run_complete_search(topic)

    if not result.get("success"):
        return CheckResult("deep", False, result.get("error", "搜索失败"))

    files = result.get("files", {})
    if len(files) < 3:
        return CheckResult("deep", False, f"生成文件缺失: {files}")

    print("Deep search OK:", files)
    return CheckResult("deep", True, json.dumps(files, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Run end-to-end checks.")
    parser.add_argument(
        "--mode",
        choices=["quick", "deep", "both"],
        default="both",
        help="选择测试模式",
    )
    parser.add_argument("--quick-topic", default="AI", help="快速搜索主题")
    parser.add_argument("--deep-topic", default="社会化", help="深度搜索主题")
    args = parser.parse_args()

    base_dir = ROOT_DIR

    results = []
    start = time.time()

    if args.mode in ("quick", "both"):
        results.append(run_quick(args.quick_topic, base_dir))
    if args.mode in ("deep", "both"):
        results.append(run_deep(args.deep_topic, base_dir))

    _print_header("Summary")
    exit_code = 0
    for res in results:
        status = "✅" if res.success else "❌"
        print(f"{status} {res.name}: {res.detail}")
        if not res.success:
            exit_code = 1

    elapsed = time.time() - start
    print(f"\nTotal time: {elapsed:.1f}s")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

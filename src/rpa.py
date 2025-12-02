#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度搜索和文档生成RPA脚本
自动执行Claude CLI命令，监控文档生成过程
"""

import subprocess
import json
import os
import time
import glob
from pathlib import Path
from typing import Optional, Dict, Any
from logger import get_logger
from workflow import (
    build_deep_search_prompt,
    extract_index_path,
    run_document_generators,
    call_claude,
)


class DeepSearchRPA:
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # 项目根目录是src目录的上两级
            self.base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), ".."))
        else:
            self.base_dir = base_dir

        self.output_dir = os.path.join(self.base_dir, "output")
        self.config_dir = os.path.join(self.base_dir, "config")
        self.kb_dir = os.path.join(self.base_dir, "knowledge_base")

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

        # 初始化日志记录器
        self.logger = get_logger("DeepSearchRPA")
        self.logger.info("DeepSearchRPA 初始化完成")

    def _find_claude_cli(self) -> Optional[str]:
        """
        自动检测Claude CLI的路径，支持Linux和Windows

        Returns:
            str or None: Claude CLI的路径，如果未找到则返回None
        """
        import platform
        import shutil

        system = platform.system().lower()

        # 1. 首先尝试从PATH中查找
        claude_path = shutil.which("claude")
        if claude_path:
            print(f"在PATH中找到Claude CLI: {claude_path}")
            return claude_path

        # 2. 如果PATH中没有，尝试常见安装位置
        if system == "windows":
            # Windows常见路径
            possible_paths = [
                os.path.expanduser(r"~/AppData/Local/npm/claude.cmd"),
                os.path.expanduser(r"~/AppData/Roaming/npm/claude.cmd"),
                r"C:\Program Files\nodejs\claude.cmd",
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\bin\claude.cmd"
            ]
        else:
            # Linux/macOS常见路径
            possible_paths = [
                "/usr/bin/claude",
                "/usr/local/bin/claude",
                os.path.expanduser("~/.local/bin/claude"),
                os.path.expanduser("~/bin/claude"),
                "/opt/claude/bin/claude"
            ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"在常见位置找到Claude CLI: {path}")
                return path

        # 3. 如果都找不到，返回None
        print("未找到Claude CLI，请确保已正确安装")
        return None

    def run_claude_search(self, topic: str) -> Dict[str, Any]:
        """
        执行Claude CLI命令进行深度搜索

        Args:
            topic: 搜索主题

        Returns:
            Dict: 执行结果状态
        """
        print(f"开始为主题 '{topic}' 执行深度搜索...")

        prompt = build_deep_search_prompt(topic)

        claude_path = self._find_claude_cli()
        if claude_path is None:
            return {
                "success": False,
                "error": "未找到Claude CLI，请确保已正确安装",
                "returncode": -3
            }

        try:
            result = call_claude(prompt, self.base_dir, claude_path)

            print(f"Claude CLI 执行完成，返回码: {result.returncode}")

            if result.stdout:
                print(
                    "标准输出:", result.stdout[:1000] + "..." if len(result.stdout) > 1000 else result.stdout)

            if result.stderr:
                print(
                    "错误输出:", result.stderr[:1000] + "..." if len(result.stderr) > 1000 else result.stderr)

            # 等待文件生成
            time.sleep(1)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        except subprocess.TimeoutExpired:
            print("Claude CLI 执行超时")
            return {
                "success": False,
                "error": "命令执行超时（30分钟）",
                "returncode": -1
            }
        except Exception as e:
            print(f"执行Claude CLI时出错: {str(e)}")
            return {
            "success": False,
            "error": str(e),
            "returncode": -2
        }

    def run_complete_search(self, topic: str) -> Dict[str, Any]:
        """
        执行完整的深度搜索和文档生成流程

        Args:
            topic: 搜索主题

        Returns:
            Dict: 完整的执行结果
        """
        print(f"开始执行完整搜索流程: {topic}")

        claude_result = self.run_claude_search(topic)

        if not claude_result["success"]:
            return {
                "success": False,
                "error": f"Claude CLI 执行失败: {claude_result.get('error', '未知错误')}",
                "claude_result": claude_result,
                "files": {}
            }

        try:
            index_path = extract_index_path(claude_result.get("stdout", ""))
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "claude_result": claude_result,
                "files": {}
            }

        if not os.path.isabs(index_path):
            index_path = os.path.abspath(os.path.join(self.base_dir, index_path))

        if not os.path.exists(index_path):
            return {
                "success": False,
                "error": f"索引文件不存在: {index_path}",
                "claude_result": claude_result,
                "files": {}
            }

        try:
            kb_dir = os.path.join(self.kb_dir, "sth-matters")
            generated_files = run_document_generators(
                index_path=index_path,
                kb_dir=kb_dir,
                output_dir=self.output_dir,
                base_dir=self.base_dir,
            )
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"文档生成失败: {e}",
                "claude_result": claude_result,
                "files": {}
            }

        return {
            "success": len(generated_files) > 0,
            "topic": topic,
            "claude_result": claude_result,
            "files": generated_files,
            "output_dir": self.output_dir,
            "index_file": index_path,
        }


if __name__ == "__main__":
    # 测试代码
    rpa = DeepSearchRPA()

    test_topic = "社会化"
    result = rpa.run_complete_search(test_topic)

    print("=== 执行结果 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))

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

class DeepSearchRPA:
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            self.base_dir = os.getcwd()
        else:
            self.base_dir = base_dir

        self.generated_docs_dir = os.path.join(self.base_dir, "_对话检索汇编", "generated_docs")
        self.index_dir = os.path.join(self.base_dir, "_对话检索汇编")

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

        # 构造Claude CLI命令（自动检测路径）
        prompt = f"请根据CLAUDE.md中定义的流程，对{topic}进行一次完整的深度搜索和文档生成。"

        # 自动检测Claude CLI路径
        claude_path = self._find_claude_cli()
        if claude_path is None:
            return {
                "success": False,
                "error": "未找到Claude CLI，请确保已正确安装",
                "returncode": -3
            }

        command = [
            claude_path,
            "-p", prompt,
            "--output-format", "json",
            "--allowedTools", "Bash,Read,Write,Edit,Grep,Glob",
            "--verbose"
        ]

        try:
            # 执行命令
            result = subprocess.run(
                command,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=1800  # 30分钟超时
            )

            print(f"Claude CLI 执行完成，返回码: {result.returncode}")

            if result.stdout:
                print("标准输出:", result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)

            if result.stderr:
                print("错误输出:", result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)

            # 等待文件生成
            time.sleep(5)

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

    def find_generated_files(self, topic: str, wait_time: int = 180) -> Dict[str, str]:
        """
        查找生成的文档文件

        Args:
            topic: 搜索主题
            wait_time: 等待文件生成的最大时间（秒）

        Returns:
            Dict: 文件路径映射
        """
        print(f"等待文档生成，最多等待 {wait_time/60:.0f} 分钟...")

        # 可能的文件模式
        file_patterns = [
            f"*{topic}*.epub",
            f"*{topic}*.md",
            f"*{topic}*.html",
            "*_epub_*.epub",
            "*_thematic_*.md",
            "*_concepts_*.md",
            "*_summary_*.md",
            "*_html_*.html"
        ]

        found_files = {}
        start_time = time.time()

        while time.time() - start_time < wait_time:
            # 检查生成的文档目录
            if os.path.exists(self.generated_docs_dir):
                for pattern in file_patterns:
                    files = glob.glob(os.path.join(self.generated_docs_dir, pattern))
                    if files:
                        # 按修改时间排序，取最新的
                        files.sort(key=os.path.getmtime, reverse=True)
                        latest_file = files[0]

                        file_type = os.path.splitext(latest_file)[1][1:]  # 去掉点
                        if file_type not in found_files:
                            found_files[file_type] = latest_file
                            print(f"找到 {file_type} 文件: {latest_file}")

            # 如果找到了主要文件类型，提前返回
            if 'epub' in found_files or 'md' in found_files:
                break

            time.sleep(2)

        print(f"总共找到 {len(found_files)} 个文件")
        return found_files

    def run_complete_search(self, topic: str) -> Dict[str, Any]:
        """
        执行完整的深度搜索和文档生成流程

        Args:
            topic: 搜索主题

        Returns:
            Dict: 完整的执行结果
        """
        print(f"开始执行完整搜索流程: {topic}")

        # 第一步：执行Claude CLI
        claude_result = self.run_claude_search(topic)

        if not claude_result["success"]:
            return {
                "success": False,
                "error": f"Claude CLI 执行失败: {claude_result.get('error', '未知错误')}",
                "claude_result": claude_result,
                "files": {}
            }

        # 第二步：查找生成的文件
        generated_files = self.find_generated_files(topic)

        return {
            "success": len(generated_files) > 0,
            "topic": topic,
            "claude_result": claude_result,
            "files": generated_files,
            "generated_docs_dir": self.generated_docs_dir
        }

if __name__ == "__main__":
    # 测试代码
    rpa = DeepSearchRPA()

    test_topic = "社会化"
    result = rpa.run_complete_search(test_topic)

    print("=== 执行结果 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
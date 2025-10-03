#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库深度搜索系统 - 生产版本
整合深度搜索和邮件发送功能
"""

import os
import time
import json
import argparse
from datetime import datetime
from deep_search_rpa import DeepSearchRPA
from email_sender import EmailSender

# set env
os.environ["ANTHROPIC_BASE_URL"] = "https://open.bigmodel.cn/api/anthropic"
os.environ["ANTHROPIC_AUTH_TOKEN"] = "3b222275909a41df8eb8553503ab3300.rJZMbCswT0DXgqph"


class KnowledgeSearchSystem:
    def __init__(self):
        self.search_rpa = DeepSearchRPA()
        self.email_sender = EmailSender()

    def process_request(self, topic: str, email: str, verbose: bool = True) -> dict:
        """
        处理搜索请求的完整流程

        Args:
            topic: 搜索主题
            email: 收件邮箱
            verbose: 是否显示详细信息

        Returns:
            dict: 处理结果
        """
        if verbose:
            print(f"开始处理搜索请求...")
            print(f"主题: {topic}")
            print(f"邮箱: {email}")
            print("-" * 50)

        result = {
            "topic": topic,
            "email": email,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "search_result": None,
            "email_result": None,
            "error": None
        }

        try:
            # 第一步：执行深度搜索
            if verbose:
                print("第一步: 执行深度搜索...")

            search_result = self.search_rpa.run_complete_search(topic)
            result["search_result"] = search_result

            if not search_result["success"]:
                result["error"] = f"深度搜索失败: {search_result.get('error', '未知错误')}"
                if verbose:
                    print(f"❌ {result['error']}")
                return result

            if verbose:
                print(f"搜索完成，生成了 {len(search_result['files'])} 个文件")
                for file_type, file_path in search_result["files"].items():
                    file_name = os.path.basename(file_path)
                    print(f"   {file_type.upper()}: {file_name}")

            # 第二步：发送邮件
            if verbose:
                print("\n第二步: 发送邮件...")

            email_result = self.email_sender.send_documents(
                recipient_email=email,
                topic=topic,
                files=search_result["files"]
            )
            result["email_result"] = email_result

            if not email_result["success"]:
                result["error"] = f"邮件发送失败: {email_result.get('error', '未知错误')}"
                if verbose:
                    print(f"❌ {result['error']}")
                return result

            if verbose:
                print(f"邮件发送成功，附件数量: {email_result['total_files']}")
                print(f"   收件人: {email}")
                print(
                    f"   发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # 成功完成
            result["success"] = True
            result["end_time"] = datetime.now().isoformat()

            if verbose:
                print("\n" + "=" * 50)
                print("处理完成！")
                print(f"请查收邮件: {email}")
                print("=" * 50)

        except Exception as e:
            result["error"] = f"系统错误: {str(e)}"
            result["end_time"] = datetime.now().isoformat()
            if verbose:
                print(f"❌ 系统错误: {e}")

        return result

    def save_result(self, result: dict, filename: str = None) -> str:
        """
        保存处理结果到文件

        Args:
            result: 处理结果
            filename: 文件名（可选）

        Returns:
            str: 保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"search_result_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return filename


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='知识库深度搜索系统')
    parser.add_argument('topic', help='搜索主题')
    parser.add_argument('email', help='收件邮箱')
    parser.add_argument('--save', action='store_true', help='保存结果到文件')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    parser.add_argument('--test-email', action='store_true', help='仅测试邮件配置')

    args = parser.parse_args()

    system = KnowledgeSearchSystem()

    # 仅测试邮件配置
    if args.test_email:
        print("测试邮件配置...")
        result = system.email_sender.test_connection()
        if result["success"]:
            print("邮件配置正常")
        else:
            print(f"邮件配置错误: {result['error']}")
        return

    # 处理搜索请求
    result = system.process_request(
        topic=args.topic,
        email=args.email,
        verbose=not args.quiet
    )

    # 保存结果
    if args.save:
        filename = system.save_result(result)
        if not args.quiet:
            print(f"\n结果已保存到: {filename}")

    # 设置退出码
    exit_code = 0 if result["success"] else 1
    exit(exit_code)


if __name__ == "__main__":
    main()

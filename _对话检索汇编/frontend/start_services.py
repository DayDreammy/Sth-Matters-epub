#!/usr/bin/env python3
"""
启动脚本 - 启动搜索服务和文件下载服务
"""

import sys
import os
import subprocess
import threading
import time
from pathlib import Path

def start_search_service():
    """启动搜索服务 (port 5000)"""
    print("启动搜索服务 (端口: 5000)...")
    try:
        subprocess.run([
            sys.executable, 'enhanced_app.py'
        ], check=True)
    except KeyboardInterrupt:
        print("\n搜索服务已停止")
    except Exception as e:
        print(f"搜索服务启动失败: {e}")

def start_file_service():
    """启动文件服务 (port 5001)"""
    print("启动文件下载服务 (端口: 5001)...")
    try:
        subprocess.run([
            sys.executable, 'file_server.py'
        ], check=True)
    except KeyboardInterrupt:
        print("\n文件下载服务已停止")
    except Exception as e:
        print(f"文件下载服务启动失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("知识库搜索系统启动器")
    print("=" * 60)
    print()
    print("请选择启动模式:")
    print("1. 启动完整服务 (搜索 + 文件下载)")
    print("2. 仅启动搜索服务 (端口 5000)")
    print("3. 仅启动文件下载服务 (端口 5001)")
    print("4. 退出")
    print()

    while True:
        try:
            choice = input("请输入选择 (1-4): ").strip()

            if choice == '1':
                print("\n正在启动完整服务...")
                print("搜索服务: http://localhost:5000")
                print("文件下载: http://localhost:5001")
                print("\n按 Ctrl+C 停止服务")
                print()

                # 启动文件下载服务
                file_thread = threading.Thread(target=start_file_service, daemon=True)
                file_thread.start()

                # 等待1秒让文件服务先启动
                time.sleep(1)

                # 启动搜索服务
                start_search_service()
                break

            elif choice == '2':
                print("\n正在启动搜索服务...")
                print("搜索服务: http://localhost:5000")
                print("\n按 Ctrl+C 停止服务")
                print()

                start_search_service()
                break

            elif choice == '3':
                print("\n正在启动文件下载服务...")
                print("文件下载: http://localhost:5001")
                print("\n按 Ctrl+C 停止服务")
                print()

                start_file_service()
                break

            elif choice == '4':
                print("退出")
                sys.exit(0)

            else:
                print("无效选择，请输入 1-4")

        except KeyboardInterrupt:
            print("\n\n退出")
            sys.exit(0)
        except Exception as e:
            print(f"错误: {e}")

if __name__ == '__main__':
    # 检查当前目录
    if not Path('enhanced_app.py').exists():
        print("错误: 找不到 enhanced_app.py 文件")
        print("请确保在正确的目录中运行此脚本")
        sys.exit(1)

    main()
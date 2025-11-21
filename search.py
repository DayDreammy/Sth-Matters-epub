#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能检索系统主入口
提供统一的命令行接口
"""

import argparse
import json
import sys
from pathlib import Path

# 导入API模块
from api.search_api import SearchAPI


def print_banner():
    """打印程序横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                        智能检索系统                          ║
║                   Intelligent Search Engine                 ║
║                                                              ║
║  📁 数据目录: knowledge_base                                            ║
║  🔍 搜索类型: 文件名、内容、标签                                ║
║  📄 输出格式: Markdown、HTML、JSON                            ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="智能检索系统 - 高效的文档搜索和内容分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python search.py "关键词"                    # 基本搜索
  python search.py "关键词" -t content        # 内容搜索
  python search.py "关键词" -f html -s        # 生成HTML并保存
  python search.py --stats                    # 显示统计信息
  python search.py --rebuild                  # 重建索引
        """
    )

    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("-t", "--type", choices=["filename", "content", "tag", "all"],
                        default="all", help="搜索类型 (默认: all)")
    parser.add_argument("-n", "--max-results", type=int, default=50,
                        help="最大结果数 (默认: 50)")
    parser.add_argument("-f", "--format", choices=["summary", "detailed", "thematic", "html", "json"],
                        default="summary", help="输出格式 (默认: summary)")
    parser.add_argument("-s", "--save", action="store_true", help="保存结果到文件")
    parser.add_argument("-d", "--knowledge-base-dir",
                        default="knowledge_base", help="知识库根目录路径 (默认: knowledge_base)")
    parser.add_argument("-p", "--search-paths", nargs="+",
                        help="搜索路径列表（相对于知识库根目录）")
    parser.add_argument("-c", "--config", default="config/config.json",
                        help="配置文件路径 (默认: config/config.json)")
    parser.add_argument("-o", "--output-dir",
                        default="output", help="输出目录路径 (默认: output)")
    parser.add_argument("--stats", action="store_true", help="显示系统统计信息")
    parser.add_argument("--rebuild", action="store_true", help="重建搜索索引")
    parser.add_argument("--profiles", action="store_true", help="显示搜索配置文件")
    parser.add_argument("--profile", help="使用指定的搜索配置文件")
    parser.add_argument("--list-paths", action="store_true", help="显示当前搜索路径")
    parser.add_argument("--web", action="store_true", help="启动Web API服务")
    parser.add_argument("--quiet", action="store_true", help="静默模式，减少输出")

    args = parser.parse_args()

    # 静默模式不显示横幅
    if not args.quiet:
        print_banner()

    # 初始化API
    try:
        api = SearchAPI(args.knowledge_base_dir,
                        args.search_paths, args.config, args.output_dir)
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)

    # 显示搜索配置文件
    if args.profiles:
        try:
            profiles = api.get_search_profiles()
            if not args.quiet:
                print("\n📋 搜索配置文件")
                print("=" * 40)
                for profile_id, profile_info in profiles.items():
                    print(
                        f"• {profile_id}: {profile_info.get('name', profile_id)}")
                    print(f"  路径: {', '.join(profile_info.get('paths', []))}")
                    print(f"  描述: {profile_info.get('description', '无描述')}")
                    print()
            else:
                print(json.dumps(profiles, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ 获取配置文件失败: {e}")
        return

    # 使用搜索配置文件
    if args.profile:
        try:
            result = api.use_search_profile(args.profile)
            if result["success"]:
                print(f"✅ 已切换到搜索配置: {args.profile}")
            else:
                print(f"❌ 切换配置失败: {result['error']}")
        except Exception as e:
            print(f"❌ 切换配置失败: {e}")
        return

    # 显示当前搜索路径
    if args.list_paths:
        try:
            if not args.quiet:
                print(f"\n📂 当前搜索路径: {api.engine.search_paths}")
                print(f"📁 知识库根目录: {api.engine.knowledge_base_dir}")
            else:
                print(json.dumps({
                    "search_paths": api.engine.search_paths,
                    "knowledge_base_dir": str(api.engine.knowledge_base_dir)
                }, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ 获取搜索路径失败: {e}")
        return

    # 处理Web API模式
    if args.web:
        try:
            from api.web_api import app
            print("🚀 启动Web API服务...")
            print(f"📡 服务地址: http://localhost:5000")
            api.engine.build_index()  # 预先构建索引
            app.run(host='0.0.0.0', port=5000, debug=False)
        except ImportError:
            print("❌ Web API需要安装Flask: pip install flask flask-cors")
        except Exception as e:
            print(f"❌ 启动Web服务失败: {e}")
        return

    # 处理统计信息
    if args.stats:
        try:
            stats = api.get_stats()
            if not args.quiet:
                print("\n📊 系统统计信息")
                print("=" * 50)
                print(f"📁 总文件数: {stats['total_files']:,}")
                print(f"📝 总字数: {stats['total_words']:,}")
                print(f"🕒 最后索引时间: {stats['last_index_time']}")

                if stats['file_types']:
                    print("\n📄 文件类型分布:")
                    for ext, count in sorted(stats['file_types'].items()):
                        print(f"  {ext or '无扩展名'}: {count}")

                if stats['categories']:
                    print("\n📂 目录分布:")
                    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)[:10]:
                        print(f"  {category}: {count}")
                    if len(stats['categories']) > 10:
                        print(f"  ... 还有 {len(stats['categories']) - 10} 个目录")
            else:
                print(json.dumps(stats, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ 获取统计信息失败: {e}")
        return

    # 处理索引重建
    if args.rebuild:
        try:
            api.rebuild_index()
        except Exception as e:
            print(f"❌ 重建索引失败: {e}")
        return

    # 检查搜索关键词
    if not args.query:
        print("❌ 请提供搜索关键词")
        print("💡 使用 --help 查看帮助信息")
        sys.exit(1)

    # 执行搜索
    try:
        result = api.search(
            query=args.query,
            search_type=args.type,
            max_results=args.max_results,
            format_type=args.format,
            save_file=args.save
        )

        if result["success"]:
            if not args.quiet and args.format != "json":
                print(f"\n✅ 搜索完成: {result['total_results']} 个结果")
                if result["saved_file"]:
                    print(f"💾 已保存到: {result['saved_file']}")
                print("-" * 50)

            # 显示结果
            if args.format == "json":
                print(json.dumps(result["content"],
                      ensure_ascii=False, indent=2))
            else:
                print(result["content"])
        else:
            print(f"❌ 搜索失败: {result.get('message', '未知错误')}")

    except KeyboardInterrupt:
        print("\n⏹️ 搜索已取消")
    except Exception as e:
        print(f"❌ 搜索出错: {e}")


if __name__ == "__main__":
    main()

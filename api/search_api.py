#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能检索系统API接口
提供RESTful API和命令行接口
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# 添加父目录到路径以便导入core模块
sys.path.append(str(Path(__file__).parent.parent))

from core.search_engine import IntelligentSearchEngine
from core.document_generator import DocumentGenerator


class SearchAPI:
    """搜索API接口"""

    def __init__(self, knowledge_base_dir: str = "knowledge_base",
                 search_paths: List[str] = None,
                 config_path: str = "config/config.json",
                 output_dir: str = "output"):
        """
        初始化API

        Args:
            knowledge_base_dir: 知识库根目录
            search_paths: 搜索路径列表
            config_path: 配置文件路径
            output_dir: 输出目录
        """
        self.engine = IntelligentSearchEngine(knowledge_base_dir, search_paths, config_path)
        self.generator = DocumentGenerator(output_dir)

    def search(self, query: str, search_type: str = "all",
               max_results: int = 50, format_type: str = "summary",
               save_file: bool = False, include_full_content: bool = False) -> Dict[str, Any]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            search_type: 搜索类型 ('filename', 'content', 'tag', 'all')
            max_results: 最大结果数
            format_type: 输出格式 ('summary', 'detailed', 'thematic', 'full_content', 'html', 'json')
            save_file: 是否保存到文件
            include_full_content: 是否包含完整原文内容

        Returns:
            Dict: 搜索结果
        """
        print(f"🔍 搜索关键词: '{query}'")
        print(f"📁 知识库目录: {self.engine.knowledge_base_dir}")
        print(f"📂 搜索路径: {self.engine.search_paths}")
        print(f"🔎 搜索类型: {search_type}")
        if include_full_content:
            print(f"📄 包含完整原文内容")
        print("-" * 50)

        # 执行搜索
        results = self.engine.search(query, search_type, max_results, include_full_content)

        print(f"✅ 找到 {len(results)} 个结果")

        if not results:
            return {
                "success": True,
                "query": query,
                "search_type": search_type,
                "total_results": 0,
                "results": [],
                "content": "未找到相关结果",
                "saved_file": None
            }

        # 生成输出
        if format_type == "html":
            content = self.generator.generate_html(results, query, include_full_content)
            output_format = "html"
        elif format_type == "json":
            content = self.generator.generate_json(results, query, include_full_content=include_full_content)
            output_format = "json"
        else:
            content = self.generator.generate_markdown(results, query, format_type, include_full_content)
            output_format = "markdown"

        # 保存文件
        saved_file = None
        if save_file:
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"search_{safe_query}_{format_type}"
            saved_file = self.generator.save_document(content, filename, output_format)
            print(f"💾 已保存到: {saved_file}")

        return {
            "success": True,
            "query": query,
            "search_type": search_type,
            "total_results": len(results),
            "results": results,
            "content": content,
            "saved_file": saved_file
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        return self.engine.get_stats()

    def rebuild_index(self) -> Dict[str, Any]:
        """重建索引"""
        print("🔄 重建索引中...")
        index = self.engine.build_index()
        print("✅ 索引重建完成")
        return {"success": True, "index": index}

    def get_search_profiles(self) -> Dict[str, Any]:
        """获取搜索配置文件列表"""
        return self.engine.get_search_profiles()

    def use_search_profile(self, profile_name: str) -> Dict[str, Any]:
        """使用指定的搜索配置文件"""
        try:
            self.engine.use_search_profile(profile_name)
            return {"success": True, "profile": profile_name}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_search_paths(self, paths: List[str]) -> Dict[str, Any]:
        """设置自定义搜索路径"""
        try:
            self.engine.set_search_paths(paths)
            return {"success": True, "paths": paths}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="智能检索系统")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("-t", "--type", choices=["filename", "content", "tag", "all"],
                       default="all", help="搜索类型")
    parser.add_argument("-n", "--max-results", type=int, default=50,
                       help="最大结果数")
    parser.add_argument("-f", "--format", choices=["summary", "detailed", "thematic", "full_content", "html", "json"],
                       default="summary", help="输出格式")
    parser.add_argument("-s", "--save", action="store_true", help="保存到文件")
    parser.add_argument("--full-content", action="store_true", help="包含完整原文内容")
    parser.add_argument("-d", "--knowledge-base-dir", default="knowledge_base", help="知识库根目录路径")
    parser.add_argument("-p", "--search-paths", nargs="+", help="搜索路径列表（相对于知识库根目录）")
    parser.add_argument("-c", "--config", default="config/config.json", help="配置文件路径")
    parser.add_argument("-o", "--output-dir", default="output", help="输出目录路径")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--rebuild", action="store_true", help="重建索引")
    parser.add_argument("--profiles", action="store_true", help="显示搜索配置文件")
    parser.add_argument("--profile", help="使用指定的搜索配置文件")
    parser.add_argument("--list-paths", action="store_true", help="显示当前搜索路径")

    args = parser.parse_args()

    # 初始化API
    api = SearchAPI(args.knowledge_base_dir, args.search_paths, args.config, args.output_dir)

    # 处理特殊命令
    # 显示搜索配置文件
    if args.profiles:
        profiles = api.get_search_profiles()
        print("\n📋 搜索配置文件")
        print("=" * 40)
        for profile_id, profile_info in profiles.items():
            print(f"• {profile_id}: {profile_info.get('name', profile_id)}")
            print(f"  路径: {', '.join(profile_info.get('paths', []))}")
            print(f"  描述: {profile_info.get('description', '无描述')}")
            print()
        return

    # 使用搜索配置文件
    if args.profile:
        result = api.use_search_profile(args.profile)
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ 切换配置失败: {result['error']}")
        return

    # 显示当前搜索路径
    if args.list_paths:
        print(f"\n📂 当前搜索路径: {api.engine.search_paths}")
        print(f"📁 知识库根目录: {api.engine.knowledge_base_dir}")
        return

    if args.stats:
        stats = api.get_stats()
        print("\n📊 系统统计信息")
        print("=" * 50)
        print(f"📁 知识库根目录: {api.engine.knowledge_base_dir}")
        print(f"📂 搜索路径: {', '.join(api.engine.search_paths)}")
        print(f"📄 总文件数: {stats['total_files']:,}")
        print(f"📝 总字数: {stats['total_words']:,}")
        print(f"🕒 最后索引时间: {stats['last_index_time']}")
        print("\n文件类型分布:")
        for ext, count in stats['file_types'].items():
            print(f"  {ext or '无扩展名'}: {count}")
        print("\n目录分布:")
        for category, count in sorted(stats['categories'].items()):
            print(f"  {category}: {count}")
        return

    if args.rebuild:
        api.rebuild_index()
        return

    # 检查是否提供了搜索关键词
    if not args.query:
        parser.print_help()
        print("\n❌ 请提供搜索关键词")
        return

    # 执行搜索
    result = api.search(
        query=args.query,
        search_type=args.type,
        max_results=args.max_results,
        format_type=args.format,
        save_file=args.save,
        include_full_content=args.full_content
    )

    # 显示结果
    if result["success"]:
        if args.format == "json":
            print(json.dumps(result["content"], ensure_ascii=False, indent=2))
        else:
            print("\n" + result["content"])
    else:
        print(f"❌ 搜索失败: {result.get('message', '未知错误')}")


if __name__ == "__main__":
    main()
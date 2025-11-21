#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能检索系统核心引擎
提供高效的文档检索、内容分析和搜索功能
"""

import os
import re
import json
import glob
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    """搜索结果数据类"""
    file_path: str
    title: str
    content_preview: str
    relevance_score: float
    match_type: str  # 'filename', 'content', 'tag'
    line_numbers: List[int]
    word_count: int


class IntelligentSearchEngine:
    """智能检索引擎"""

    def __init__(self, knowledge_base_dir: str = "knowledge_base",
                 search_paths: List[str] = None, config_path: str = "config/config.json"):
        """
        初始化搜索引擎

        Args:
            knowledge_base_dir: 知识库根目录路径
            search_paths: 搜索路径列表，相对于知识库根目录
            config_path: 配置文件路径
        """
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.data_dir = self.knowledge_base_dir  # 添加data_dir属性以兼容现有代码
        self.config_path = Path(config_path)

        # 加载配置
        self.config = self._load_config()

        # 设置搜索路径
        if search_paths is None:
            search_paths = self.config.get("search_engine", {}).get("default_search_paths", ["9a"])
        self.search_paths = search_paths

        # 设置支持的文件扩展名
        self.supported_extensions = set(
            self.config.get("search_engine", {}).get("supported_extensions",
                                                    [".md", ".txt", ".json", ".html", ".htm"])
        )

        self.cache = {}  # 简单的内存缓存
        self.last_index_time = None

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {self.config_path}: {e}")

        # 返回默认配置
        return {
            "search_engine": {
                "supported_extensions": [".md", ".txt", ".json", ".html", ".htm"],
                "default_search_paths": ["9a"],
                "search_scope": {
                    "include_subdirectories": True,
                    "exclude_patterns": [".git", "__pycache__", "node_modules", ".DS_Store"],
                    "max_file_size": 104857600
                }
            }
        }

    def _get_full_search_paths(self) -> List[Path]:
        """获取完整的搜索路径"""
        full_paths = []
        search_scope = self.config.get("search_engine", {}).get("search_scope", {})

        for search_path in self.search_paths:
            if search_path == "*":
                # 搜索整个知识库
                full_paths.extend(self.knowledge_base_dir.iterdir())
            else:
                path = self.knowledge_base_dir / search_path
                if path.exists():
                    if path.is_file():
                        full_paths.append(path)
                    else:
                        # 如果是目录且启用子目录搜索
                        if search_scope.get("include_subdirectories", True):
                            full_paths.extend(path.rglob("*"))
                        else:
                            full_paths.extend(path.iterdir())

        return full_paths

    def _should_exclude_file(self, file_path: Path) -> bool:
        """检查文件是否应该被排除"""
        search_scope = self.config.get("search_engine", {}).get("search_scope", {})
        exclude_patterns = search_scope.get("exclude_patterns", [])

        # 检查排除模式
        for pattern in exclude_patterns:
            if pattern in str(file_path):
                return True

        # 检查文件大小
        max_file_size = search_scope.get("max_file_size", 104857600)  # 默认100MB
        try:
            if file_path.stat().st_size > max_file_size:
                return True
        except OSError:
            return True

        return False

    def set_search_paths(self, paths: List[str]):
        """设置搜索路径"""
        self.search_paths = paths
        self.clear_cache()  # 清除缓存以强制重新索引

    def get_search_profiles(self) -> Dict[str, Dict[str, Any]]:
        """获取搜索配置文件"""
        return self.config.get("search_profiles", {})

    def use_search_profile(self, profile_name: str):
        """使用指定的搜索配置文件"""
        profiles = self.get_search_profiles()
        if profile_name in profiles:
            profile = profiles[profile_name]
            self.set_search_paths(profile.get("paths", ["9a"]))
            print(f"已切换到搜索配置: {profile.get('name', profile_name)}")
        else:
            print(f"搜索配置 '{profile_name}' 不存在")

    def clear_cache(self):
        """清除缓存"""
        self.cache = {}
        self.last_index_time = None

    def build_index(self) -> Dict[str, Any]:
        """构建文档索引"""
        print("正在构建文档索引...")

        index = {
            "metadata": {
                "build_time": datetime.now().isoformat(),
                "total_files": 0,
                "total_size": 0
            },
            "files": {},
            "tags": {},
            "categories": {}
        }

        total_size = 0
        file_count = 0

        # 遍历所有文件
        for file_path in self._get_all_files():
            try:
                file_info = self._analyze_file(file_path)
                if file_info:
                    # 使用相对于知识库根目录的路径
                    try:
                        relative_path = str(file_path.relative_to(self.knowledge_base_dir))
                    except ValueError:
                        relative_path = str(file_path)
                    index["files"][relative_path] = file_info
                    total_size += file_info["size"]
                    file_count += 1

                    # 提取标签
                    for tag in file_info.get("tags", []):
                        if tag not in index["tags"]:
                            index["tags"][tag] = []
                        index["tags"][tag].append(str(file_path.relative_to(self.data_dir)))

            except Exception as e:
                print(f"处理文件时出错 {file_path}: {e}")

        index["metadata"]["total_files"] = file_count
        index["metadata"]["total_size"] = total_size
        self.last_index_time = datetime.now()

        print(f"索引构建完成: {file_count} 个文件, 总大小 {total_size/1024:.1f} KB")
        return index

    def search(self, query: str, search_type: str = "all", max_results: int = 50) -> List[SearchResult]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            search_type: 搜索类型 ('filename', 'content', 'tag', 'all')
            max_results: 最大结果数

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if not self.cache or not self.last_index_time:
            self.cache = self.build_index()

        results = []
        query_lower = query.lower()

        for file_relative_path, file_info in self.cache["files"].items():
            file_path = self.knowledge_base_dir / file_relative_path

            # 文件名匹配
            if search_type in ['filename', 'all']:
                if query_lower in file_path.name.lower():
                    result = self._create_search_result(
                        file_path, file_info, query, 'filename', []
                    )
                    results.append(result)

            # 标签匹配
            if search_type in ['tag', 'all']:
                for tag in file_info.get("tags", []):
                    if query_lower in tag.lower():
                        result = self._create_search_result(
                            file_path, file_info, query, 'tag', []
                        )
                        results.append(result)
                        break

            # 内容匹配
            if search_type in ['content', 'all']:
                content_matches = self._search_content(file_path, query)
                if content_matches:
                    result = self._create_search_result(
                        file_path, file_info, query, 'content', content_matches
                    )
                    results.append(result)

        # 按相关性排序并限制结果数量
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]

    def _get_all_files(self) -> List[Path]:
        """获取所有支持的文件"""
        files = []
        all_paths = self._get_full_search_paths()

        for path in all_paths:
            # 跳过目录
            if path.is_dir():
                continue

            # 检查文件扩展名
            if path.suffix in self.supported_extensions:
                # 检查是否应该排除
                if not self._should_exclude_file(path):
                    files.append(path)

        return files

    def _analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """分析单个文件"""
        try:
            stat = file_path.stat()
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # 提取标题（Markdown文件的第一行#开头的内容）
            title = file_path.stem
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            # 提取标签（#tag格式）
            tags = re.findall(r'#(\w+[\u4e00-\u9fff]?\w*)', content)

            # 提取分类（基于目录结构）
            try:
                category = str(file_path.parent.relative_to(self.knowledge_base_dir))
            except ValueError:
                # 如果文件不在知识库目录下，使用完整路径
                category = str(file_path.parent)

            return {
                "title": title,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "tags": tags,
                "category": category,
                "word_count": len(content),
                "line_count": len(lines),
                "preview": content[:200] + "..." if len(content) > 200 else content
            }

        except Exception as e:
            print(f"分析文件失败 {file_path}: {e}")
            return None

    def _search_content(self, file_path: Path, query: str) -> List[int]:
        """在文件内容中搜索"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            matches = []

            query_lower = query.lower()
            for i, line in enumerate(lines, 1):
                if query_lower in line.lower():
                    matches.append(i)

            return matches
        except Exception:
            return []

    def _create_search_result(self, file_path: Path, file_info: Dict[str, Any],
                            query: str, match_type: str, line_numbers: List[int]) -> SearchResult:
        """创建搜索结果对象"""
        # 计算相关性得分
        score = 0.0
        if match_type == 'filename':
            score = 0.9
        elif match_type == 'tag':
            score = 0.8
        elif match_type == 'content':
            score = 0.6 + min(len(line_numbers) * 0.1, 0.3)

        # 获取内容预览
        preview = file_info.get("preview", "")
        if match_type == 'content' and line_numbers:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                preview_lines = []
                for line_num in line_numbers[:3]:  # 显示前3个匹配行
                    if 0 <= line_num - 1 < len(lines):
                        line = lines[line_num - 1].strip()
                        if line:
                            preview_lines.append(f"第{line_num}行: {line}")
                preview = "\n".join(preview_lines)
            except Exception:
                pass

        return SearchResult(
            file_path=str(file_path),
            title=file_info.get("title", file_path.stem),
            content_preview=preview,
            relevance_score=score,
            match_type=match_type,
            line_numbers=line_numbers,
            word_count=file_info.get("word_count", 0)
        )

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.cache:
            self.cache = self.build_index()

        metadata = self.cache["metadata"]
        files = self.cache["files"]

        # 统计文件类型分布
        extensions = {}
        categories = {}
        total_words = 0

        for file_info in files.values():
            ext = Path(file_info["title"]).suffix or "no_extension"
            extensions[ext] = extensions.get(ext, 0) + 1

            category = file_info.get("category", "root")
            categories[category] = categories.get(category, 0) + 1

            total_words += file_info.get("word_count", 0)

        return {
            "index_metadata": metadata,
            "total_files": len(files),
            "total_words": total_words,
            "file_types": extensions,
            "categories": categories,
            "last_index_time": self.last_index_time.isoformat() if self.last_index_time else None
        }
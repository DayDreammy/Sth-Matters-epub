#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档生成器 - 将搜索结果转换为多种格式的文档
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
from .search_engine import SearchResult


class DocumentGenerator:
    """文档生成器"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化文档生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_markdown(self, results: List[SearchResult], query: str,
                         layout: str = "summary", include_full_content: bool = False) -> str:
        """
        生成Markdown文档

        Args:
            results: 搜索结果列表
            query: 搜索关键词
            layout: 布局类型 ('summary', 'detailed', 'thematic', 'full_content')
            include_full_content: 是否包含完整原文内容

        Returns:
            str: 生成的Markdown内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if layout == "summary":
            return self._generate_summary_markdown(results, query, timestamp)
        elif layout == "detailed":
            return self._generate_detailed_markdown(results, query, timestamp, include_full_content)
        elif layout == "thematic":
            return self._generate_thematic_markdown(results, query, timestamp, include_full_content)
        elif layout == "full_content":
            return self._generate_full_content_markdown(results, query, timestamp)
        else:
            return self._generate_summary_markdown(results, query, timestamp)

    def _generate_summary_markdown(self, results: List[SearchResult],
                                 query: str, timestamp: str) -> str:
        """生成概要式Markdown文档"""
        md_content = f"""# 搜索结果概要

**搜索关键词**: `{query}`
**生成时间**: {timestamp}
**结果数量**: {len(results)}

---

## 快速摘要

"""

        if not results:
            md_content += "未找到相关结果。\n"
            return md_content

        # 按相关性排序
        results.sort(key=lambda x: x.relevance_score, reverse=True)

        # 生成简要列表
        for i, result in enumerate(results[:20], 1):  # 限制前20个结果
            md_content += f"{i}. **{result.title}**\n"
            md_content += f"   - 路径: `{result.file_path}`\n"
            md_content += f"   - 匹配类型: {result.match_type}\n"
            md_content += f"   - 相关性: {result.relevance_score:.2f}\n"
            if result.line_numbers:
                md_content += f"   - 匹配行: {result.line_numbers[:5]}{'...' if len(result.line_numbers) > 5 else ''}\n"
            md_content += "\n"

        return md_content

    def _generate_detailed_markdown(self, results: List[SearchResult],
                                  query: str, timestamp: str, include_full_content: bool = False) -> str:
        """生成详细式Markdown文档"""
        md_content = f"""# 详细搜索结果

**搜索关键词**: `{query}`
**生成时间**: {timestamp}
**结果数量**: {len(results)}

---

"""

        if not results:
            md_content += "未找到相关结果。\n"
            return md_content

        results.sort(key=lambda x: x.relevance_score, reverse=True)

        for i, result in enumerate(results, 1):
            md_content += f"""## {i}. {result.title}

**文件路径**: `{result.file_path}`
**匹配类型**: {result.match_type}
**相关性得分**: {result.relevance_score:.2f}
**字数**: {result.word_count:,} 字

**内容预览**:
```markdown
{result.content_preview}
```
"""

            # 如果需要完整内容且有完整内容
            if include_full_content and result.full_content:
                md_content += f"""
**完整原文**:
```markdown
{result.full_content}
```

---
"""
            else:
                md_content += "\n---\n"

        return md_content

    def _generate_thematic_markdown(self, results: List[SearchResult],
                                  query: str, timestamp: str, include_full_content: bool = False) -> str:
        """生成主题式Markdown文档"""
        # 按匹配类型分组
        grouped_results = {}
        for result in results:
            if result.match_type not in grouped_results:
                grouped_results[result.match_type] = []
            grouped_results[result.match_type].append(result)

        md_content = f"""# 主题式搜索结果

**搜索关键词**: `{query}`
**生成时间**: {timestamp}
**结果数量**: {len(results)}

---

"""

        if not results:
            md_content += "未找到相关结果。\n"
            return md_content

        # 按主题展示
        for match_type, type_results in grouped_results.items():
            type_names = {
                'filename': '文件名匹配',
                'content': '内容匹配',
                'tag': '标签匹配'
            }

            md_content += f"## {type_names.get(match_type, match_type)} ({len(type_results)} 个结果)\n\n"

            type_results.sort(key=lambda x: x.relevance_score, reverse=True)

            for result in type_results:
                md_content += f"### {result.title}\n\n"
                md_content += f"**路径**: `{result.file_path}`  \n"
                md_content += f"**相关性**: {result.relevance_score:.2f}  \n"
                if result.line_numbers:
                    md_content += f"**匹配行**: {result.line_numbers[:3]}{'...' if len(result.line_numbers) > 3 else ''}  \n"
                md_content += f"**预览**: {result.content_preview[:150]}{'...' if len(result.content_preview) > 150 else ''}\n\n"

                # 如果需要完整内容且有完整内容
                if include_full_content and result.full_content:
                    md_content += f"**完整原文**:\n\n```markdown\n{result.full_content}\n```\n\n"

                md_content += "---\n\n"

        return md_content

    def _generate_full_content_markdown(self, results: List[SearchResult],
                                      query: str, timestamp: str) -> str:
        """生成完整内容式Markdown文档"""
        md_content = f"""# 完整原文搜索结果

**搜索关键词**: `{query}`
**生成时间**: {timestamp}
**结果数量**: {len(results)}

---

"""

        if not results:
            md_content += "未找到相关结果。\n"
            return md_content

        results.sort(key=lambda x: x.relevance_score, reverse=True)

        for i, result in enumerate(results, 1):
            md_content += f"""## {i}. {result.title}

**文件路径**: `{result.file_path}`
**匹配类型**: {result.match_type}
**相关性得分**: {result.relevance_score:.2f}
**字数**: {result.word_count:,} 字

"""

            # 显示完整内容
            if result.full_content:
                md_content += f"""```markdown
{result.full_content}
```

"""
            else:
                md_content += "**完整内容不可用**\n\n"

            md_content += "---\n\n"

        return md_content

    def generate_html(self, results: List[SearchResult], query: str,
                     include_full_content: bool = False) -> str:
        """生成HTML文档"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>搜索结果 - {query}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 40px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }}
        .search-info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; }}
        .result {{ border: 1px solid #ddd; margin-bottom: 20px; border-radius: 5px; overflow: hidden; }}
        .result-header {{ background: #f8f9fa; padding: 15px; border-bottom: 1px solid #ddd; }}
        .result-title {{ font-size: 18px; font-weight: bold; color: #007acc; margin: 0; }}
        .result-meta {{ font-size: 12px; color: #666; margin-top: 5px; }}
        .result-content {{ padding: 15px; }}
        .match-filename {{ border-left: 4px solid #28a745; }}
        .match-content {{ border-left: 4px solid #ffc107; }}
        .match-tag {{ border-left: 4px solid #17a2b8; }}
        .relevance {{ background: #007acc; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; }}
        .preview {{ background: #f8f9fa; padding: 10px; border-radius: 3px; font-family: monospace; font-size: 13px; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>搜索结果</h1>
        <div class="search-info">
            <strong>搜索关键词:</strong> {query}<br>
            <strong>生成时间:</strong> {timestamp}<br>
            <strong>结果数量:</strong> {len(results)}
        </div>
"""

        if not results:
            html_content += "<p>未找到相关结果。</p>"
        else:
            results.sort(key=lambda x: x.relevance_score, reverse=True)

            for result in results:
                match_class = f"match-{result.match_type}"
                content_display = result.content_preview

                # 如果需要完整内容且有完整内容
                if include_full_content and result.full_content:
                    content_display = result.full_content

                html_content += f"""
        <div class="result {match_class}">
            <div class="result-header">
                <div class="result-title">{result.title}</div>
                <div class="result-meta">
                    <span class="relevance">{result.relevance_score:.2f}</span>
                    匹配类型: {result.match_type} |
                    路径: <code>{result.file_path}</code> |
                    字数: {result.word_count:,}
                    {' | 包含完整内容' if include_full_content and result.full_content else ''}
                </div>
            </div>
            <div class="result-content">
                <div class="preview">{content_display}</div>
            </div>
        </div>
"""

        html_content += """
    </div>
</body>
</html>"""

        return html_content

    def generate_json(self, results: List[SearchResult], query: str,
                     metadata: Dict[str, Any] = None, include_full_content: bool = False) -> Dict[str, Any]:
        """生成JSON格式结果"""
        timestamp = datetime.now().isoformat()

        json_data = {
            "metadata": {
                "query": query,
                "timestamp": timestamp,
                "total_results": len(results),
                "generator": "IntelligentSearchEngine"
            },
            "results": []
        }

        if metadata:
            json_data["metadata"].update(metadata)

        for result in results:
            result_data = {
                "title": result.title,
                "file_path": result.file_path,
                "content_preview": result.content_preview,
                "relevance_score": result.relevance_score,
                "match_type": result.match_type,
                "line_numbers": result.line_numbers,
                "word_count": result.word_count
            }

            # 如果需要完整内容且有完整内容
            if include_full_content and result.full_content is not None:
                result_data["full_content"] = result.full_content

            json_data["results"].append(result_data)

        return json_data

    def save_document(self, content: str, filename: str, format_type: str = "markdown"):
        """保存文档到文件"""
        if format_type == "html":
            filename = f"{filename}.html"
        elif format_type == "json":
            filename = f"{filename}.json"
        else:
            filename = f"{filename}.md"

        file_path = self.output_dir / filename

        if format_type == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return str(file_path)

    def generate_all_formats(self, results: List[SearchResult], query: str,
                           base_filename: str = None, include_full_content: bool = False) -> Dict[str, str]:
        """生成所有格式的文档"""
        if not base_filename:
            # 从查询中生成安全的文件名
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            base_filename = f"search_{safe_query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        saved_files = {}

        # 生成各种格式的文档
        formats = [
            ("summary_markdown", "summary", self.generate_markdown(results, query, "summary", include_full_content)),
            ("detailed_markdown", "detailed", self.generate_markdown(results, query, "detailed", include_full_content)),
            ("thematic_markdown", "thematic", self.generate_markdown(results, query, "thematic", include_full_content)),
            ("html", "html", self.generate_html(results, query, include_full_content)),
            ("json", "json", self.generate_json(results, query, include_full_content=include_full_content))
        ]

        # 如果需要完整内容，再生成一个专门的完整内容文档
        if include_full_content:
            formats.append(
                ("full_content_markdown", "full_content", self.generate_markdown(results, query, "full_content"))
            )

        for format_name, format_type, content in formats:
            try:
                filename = f"{base_filename}_{format_name}"
                file_path = self.save_document(content, filename, format_type)
                saved_files[format_name] = file_path
                print(f"✓ 已生成 {format_name}: {file_path}")
            except Exception as e:
                print(f"✗ 生成 {format_name} 时出错: {e}")

        return saved_files
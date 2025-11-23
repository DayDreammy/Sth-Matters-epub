#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阅读文档生成器
根据JSON索引文件生成不同格式的阅读文档
"""

import json
import os
import re
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional


class MDDocumentGenerator:
    def __init__(self, index_file_path: str, kb_dir: str):
        """初始化文档生成器"""
        self.index_file_path = index_file_path
        self.kb_dir = kb_dir
        self.index_data = self._load_index()
        self.include_source_content = True  # 默认包含原始内容

    def _load_index(self) -> Dict[str, Any]:
        """加载JSON索引文件"""
        try:
            with open(self.index_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"索引文件未找到: {self.index_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析错误: {e}")

    def _read_source_file(self, file_path: str) -> str:
        """读取源文件内容"""
        if not self.include_source_content:
            return "（已跳过原始文件内容）"

        # AI可能生成相对于知识库根目录的路径，我们直接拼接
        full_path = os.path.join(self.kb_dir, file_path)
        
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return f"读取文件时出错: {full_path}, 错误: {e}"
        
        return f"无法找到文件: {full_path}"

    def _markdown_to_html(self, markdown_text: str) -> str:
        """将markdown文本转换为HTML格式"""
        if not markdown_text:
            return ""

        html = markdown_text

        # 处理标题 (# ## ### #### ##### ######)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^##### (.+)$', r'<h5>\1</h5>',
                      html, flags=re.MULTILINE)
        html = re.sub(r'^###### (.+)$', r'<h6>\1</h6>',
                      html, flags=re.MULTILINE)

        # 处理粗体 (**text** 和 __text__)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)

        # 处理斜体 (*text* 和 _text_)
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
        html = re.sub(r'_([^_]+)_', r'<em>\1</em>', html)

        # 处理链接 [text](url)
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                      r'<a href="\2" target="_blank">\1</a>', html)

        # 处理无序列表 (- item 和 * item)
        def process_list_items(text):
            lines = text.split('\n')
            in_list = False
            result = []

            for line in lines:
                if re.match(r'^[\s]*[-*] ', line):
                    if not in_list:
                        result.append('<ul>')
                        in_list = True
                    # 处理列表项，可能包含内部格式
                    item_content = re.sub(r'^[\s]*[-*] ', '', line)
                    result.append(f'<li>{item_content}</li>')
                else:
                    if in_list:
                        result.append('</ul>')
                        in_list = False
                    result.append(line)

            if in_list:
                result.append('</ul>')

            return '\n'.join(result)

        html = process_list_items(html)

        # 处理有序列表 (1. item)
        def process_ordered_list_items(text):
            lines = text.split('\n')
            in_list = False
            result = []

            for line in lines:
                if re.match(r'^[\s]*\d+\. ', line):
                    if not in_list:
                        result.append('<ol>')
                        in_list = True
                    # 处理列表项
                    item_content = re.sub(r'^[\s]*\d+\. ', '', line)
                    result.append(f'<li>{item_content}</li>')
                else:
                    if in_list:
                        result.append('</ol>')
                        in_list = False
                    result.append(line)

            if in_list:
                result.append('</ol>')

            return '\n'.join(result)

        html = process_ordered_list_items(html)

        # 处理引用 (> text)
        html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>',
                      html, flags=re.MULTILINE)

        # 处理代码块 (```text```)
        html = re.sub(r'```([^`]+)```', r'<pre><code>\1</code></pre>', html)

        # 处理行内代码 (`text`)
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # 处理分割线 (--- 或 ***)
        html = re.sub(r'^[-*]{3,}$', r'<hr>', html, flags=re.MULTILINE)

        # 处理段落（将连续的非空行包装在<p>标签中）
        def process_paragraphs(text):
            lines = text.split('\n')
            result = []
            in_paragraph = False
            current_paragraph = []

            for line in lines:
                stripped_line = line.strip()

                # 跳过已经是HTML标签的行
                if stripped_line.startswith('<') and stripped_line.endswith('>'):
                    if in_paragraph:
                        result.append(
                            '<p>' + ' '.join(current_paragraph) + '</p>')
                        current_paragraph = []
                        in_paragraph = False
                    result.append(line)
                    continue

                # 跳过空行
                if not stripped_line:
                    if in_paragraph:
                        result.append(
                            '<p>' + ' '.join(current_paragraph) + '</p>')
                        current_paragraph = []
                        in_paragraph = False
                    continue

                # 添加到当前段落
                current_paragraph.append(stripped_line)
                in_paragraph = True

            # 处理最后一个段落
            if in_paragraph:
                result.append('<p>' + ' '.join(current_paragraph) + '</p>')

            return '\n'.join(result)

        html = process_paragraphs(html)

        return html

    def _format_source_header(self, source: Dict[str, Any]) -> str:
        """格式化来源标题头部"""
        # 从文件路径中提取原标题（去除扩展名）
        original_title = os.path.splitext(
            os.path.basename(source['file_path']))[0]

        header = f"### {original_title}\n\n"

        return header

    def generate_thematic_document(self) -> str:
        """生成按主题分类的文档"""
        output = []

        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 主题分类阅读文档\n")
        output.append(
            f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**主题**: {metadata['topic']}\n")
        output.append(f"**来源数量**: {metadata['total_sources']}\n")
        output.append("---\n\n")

        # 按分类分组
        category_groups = {}
        for source in self.index_data['sources']:
            category = source['category']
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(source)

        # 生成各分类内容
        category_names = {
            'core_theory': '核心理论',
            'critical_analysis': '批判分析',
            'family_education': '家庭教育',
            'social_paradox': '社会悖论',
            'consequences': '后果分析',
            'child_development': '儿童发展',
            'personality_development': '人格发展',
            'human_attributes': '人类属性',
            'practical_skills': '实践技能'
        }

        for category, sources in category_groups.items():
            category_name = category_names.get(category, category)
            output.append(f"## {category_name}\n\n")

            for source in sources:
                output.append(self._format_source_header(source))

                # 读取原文内容
                content = self._read_source_file(source['file_path'])

                # 提取主要引用（这里简化处理，实际可以根据需要更精确地提取）
                output.append(f"> {source['content_preview']}\n\n")

                # 如果内容较长，可以添加更多原文
                if len(content) > 500:
                    output.append(
                        content[:1000] + "..." if len(content) > 1000 else content)
                    output.append("\n\n")
                else:
                    output.append(content)
                    output.append("\n\n")

                output.append("---\n\n")

        return ''.join(output)

    def generate_source_based_document(self) -> str:
        """生成按来源分组的文档"""
        output = []

        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 来源分组阅读文档\n")
        output.append(
            f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**主题**: {metadata['topic']}\n")
        output.append(f"**来源数量**: {metadata['total_sources']}\n")
        output.append("---\n\n")

        # 按文件路径分组
        file_groups = {}
        for source in self.index_data['sources']:
            file_path = source['file_path']
            if file_path not in file_groups:
                file_groups[file_path] = []
            file_groups[file_path].append(source)

        # 生成各文件内容
        for file_path, sources in file_groups.items():
            output.append(f"## 文件: {os.path.basename(file_path)}\n\n")

            for source in sources:
                output.append(self._format_source_header(source))

                # 读取原文内容
                content = self._read_source_file(file_path)
                output.append(content)
                output.append("\n\n")

            output.append("---\n\n")

        return ''.join(output)

    def generate_concepts_document(self) -> str:
        """生成按关键概念组织的文档"""
        output = []

        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 关键概念文档\n")
        output.append(
            f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**主题**: {metadata['topic']}\n")
        output.append(f"**来源数量**: {metadata['total_sources']}\n")
        output.append("---\n\n")

        # 提取所有关键概念
        all_concepts = {}
        for source in self.index_data['sources']:
            for concept in source['key_concepts']:
                if concept not in all_concepts:
                    all_concepts[concept] = []
                all_concepts[concept].append(source)

        # 按概念组织
        for concept, sources in all_concepts.items():
            output.append(f"## {concept}\n\n")

            for source in sources:
                original_title = os.path.splitext(
                    os.path.basename(source['file_path']))[0]
                output.append(f"### {original_title}\n\n")
                output.append(
                    f"**来源**: `{os.path.basename(source['file_path'])}`\n")
                output.append(f"**字数**: {source['word_count']}\n")
                if source.get('zhihu_link'):
                    output.append(
                        f"**知乎链接**: [{source['title']}]({source['zhihu_link']})\n")
                output.append("\n")
                output.append(f"> {source['content_preview']}\n\n")

            output.append("---\n\n")

        return ''.join(output)

    def generate_html_document(self) -> str:
        """生成HTML格式文档"""
        output = []

        # HTML头部
        metadata = self.index_data['metadata']
        output.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""+metadata['topic']+""" - 知识文档</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .metadata {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .toc {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .toc h2 {
            margin-top: 0;
            color: #333;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin: 5px 0;
        }
        .toc a {
            color: #667eea;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .toc a:hover {
            background-color: #f0f0f0;
        }
        .source {
            background: white;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .source-header {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }
        .source-title {
            color: #333;
            margin: 0 0 10px 0;
            font-size: 1.3em;
        }
        .source-meta {
            color: #666;
            font-size: 0.9em;
        }
        .source-meta .meta-item {
            display: inline-block;
            margin-right: 15px;
            margin-bottom: 5px;
        }
        .source-content {
            padding: 20px;
        }
        .content-preview {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            font-style: italic;
        }
        .original-content {
            background: #fafafa;
            padding: 20px;
            border-radius: 6px;
            font-family: inherit;
            line-height: 1.8;
        }
        .original-content h1, .original-content h2, .original-content h3, 
        .original-content h4, .original-content h5, .original-content h6 {
            color: #333;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        .original-content h1 {
            font-size: 2em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .original-content h2 {
            font-size: 1.5em;
            border-bottom: 1px solid #ddd;
            padding-bottom: 8px;
        }
        .original-content h3 {
            font-size: 1.25em;
        }
        .original-content p {
            margin-bottom: 16px;
            text-align: justify;
        }
        .original-content ul, .original-content ol {
            margin: 16px 0;
            padding-left: 20px;
        }
        .original-content li {
            margin-bottom: 8px;
        }
        .original-content blockquote {
            border-left: 4px solid #667eea;
            margin: 16px 0;
            padding: 8px 16px;
            background: #f8f9fa;
            font-style: italic;
        }
        .original-content pre {
            background: #2d3748;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 16px 0;
        }
        .original-content code {
            background: #e2e8f0;
            color: #2d3748;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }
        .original-content pre code {
            background: none;
            color: inherit;
            padding: 0;
        }
        .original-content a {
            color: #667eea;
            text-decoration: none;
        }
        .original-content a:hover {
            text-decoration: underline;
        }
        .original-content hr {
            border: none;
            height: 1px;
            background: #ddd;
            margin: 24px 0;
        }
        .original-content strong {
            font-weight: 600;
            color: #2d3748;
        }
        .original-content em {
            font-style: italic;
            color: #4a5568;
        }
        .category {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
        }
        .tag {
            display: inline-block;
            background: #e9ecef;
            color: #495057;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 0.8em;
            margin-right: 5px;
        }
        .zhihu-link {
            color: #0066ff;
            text-decoration: none;
            font-weight: bold;
        }
        .zhihu-link:hover {
            text-decoration: underline;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            .header {
                padding: 20px;
            }
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>"""+metadata['topic']+"""</h1>
        <p>知识文档 - 便于阅读的HTML格式</p>
    </div>
    
    <div class="metadata">
        <h2>文档信息</h2>
        <div class="source-meta">
            <span class="meta-item"><strong>生成日期:</strong> """+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"""</span>
            <span class="meta-item"><strong>主题:</strong> """+ metadata['topic']+"""</span>
            <span class="meta-item"><strong>来源数量:</strong> """+ str(metadata['total_sources'])+"""</span>
        </div>
    </div>""")

        # 统计信息
        total_words = sum(s['word_count'] for s in self.index_data['sources'])
        output.append("""
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">"""+str(metadata['total_sources'])+"""</div>
            <div class="stat-label">来源数量</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">"""+str(total_words)+"""</div>
            <div class="stat-label">总字数</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">"""+str(len(set(s['category'] for s in self.index_data['sources'])))+"""</div>
            <div class="stat-label">分类数量</div>
        </div>
    </div>""")

        # 目录
        output.append("""
    <div class="toc">
        <h2>📚 目录</h2>
        <ul>""")

        # 按分类生成目录
        category_groups = {}
        for source in self.index_data['sources']:
            category = source['category']
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(source)

        category_names = {
            'core_theory': '核心理论',
            'critical_analysis': '批判分析',
            'family_education': '家庭教育',
            'education_priority': '教育优先级',
            'social_paradox': '社会悖论',
            'consequences': '后果分析',
            'social_negation': '社会性否定',
            'child_development': '儿童发展',
            'excessive_socialization': '过度社会化',
            'personality_development': '人格发展',
            'core_importance': '核心重要性',
            'practice_guidance': '实践指导',
            'human_attributes': '人类属性',
            'self_awareness': '自我认知',
            'gender_differences': '性别差异',
            'practical_skills': '实践技能',
            'survival_competitiveness': '生存竞争力',
            'legal_awareness': '法律意识'
        }

        for category, sources in category_groups.items():
            category_name = category_names.get(category, category)
            output.append(
                f"""            <li><a href="#{category}">{category_name} ({len(sources)}篇)</a></li>""")

        output.append("""
        </ul>
    </div>""")

        # 生成各分类内容
        for category, sources in category_groups.items():
            category_name = category_names.get(category, category)
            output.append(f"""    <div class="source" id="{category}">
        <div class="source-header">
            <h2 class="source-title">{category_name}</h2>
            <div class="source-meta">
                <span class="category">{category_name}</span>
                <span class="meta-item">共 {len(sources)} 篇文章</span>
            </div>
        </div>
        <div class="source-content">""")

            for source in sources:
                output.append(f"""            <div class="source">
                <div class="source-header">
                    <h3 class="source-title">{source['title']}</h3>
                    <div class="source-meta">""")

                if source.get('zhihu_link'):
                    output.append(f"""                        <span class="meta-item">
                            <a href="{source['zhihu_link']}" class="zhihu-link" target="_blank">🔗 知乎链接</a>
                        </span>""")

                output.append(f"""                        <span class="meta-item"><strong>文件:</strong> {source['file_path']}</span>
                        <span class="meta-item"><strong>字数:</strong> {source['word_count']}</span>
                        <span class="meta-item"><strong>分类:</strong> <span class="category">{category_name}</span></span>
                    </div>
                    <div class="source-meta">
                        <span class="meta-item"><strong>标签:</strong>""")

                for tag in source['tags']:
                    output.append(f""" <span class="tag">{tag}</span>""")

                output.append("""                        </span>
                    </div>
                    <div class="source-meta">
                        <span class="meta-item"><strong>关键概念:</strong>""")

                for concept in source['key_concepts']:
                    output.append(f""" <span class="tag">{concept}</span>""")

                output.append("""                        </span>
                    </div>
                </div>
                <div class="source-content">
                    <div class="content-preview">""")

                output.append(f"""{source['content_preview']}""")

                output.append("""</div>""")

                # 读取原文内容
                content = self._read_source_file(source['file_path'])
                if content.startswith("无法读取文件"):
                    output.append(f"""                    <div class="original-content" style="color: #666; font-style: italic;">
                        {content}
                    </div>""")
                else:
                    # 将markdown转换为HTML
                    html_content = self._markdown_to_html(content)
                    output.append(f"""                    <div class="original-content">
                        {html_content}
                    </div>""")

                output.append("""
                </div>
            </div>""")

            output.append("""
        </div>
    </div>""")

        # HTML尾部
        output.append("""
    <footer style="text-align: center; margin-top: 40px; padding: 20px; color: #666; font-size: 0.9em;">
        <p>文档由 Claude Code 自动生成 | 基于 JSON 索引数据</p>
    </footer>
</body>
</html>""")

        return ''.join(output)

    def generate_summary_document(self) -> str:
        """生成概要文档"""
        output = []

        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 内容概要\n")
        output.append(
            f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**主题**: {metadata['topic']}\n")
        output.append(f"**来源数量**: {metadata['total_sources']}\n")
        output.append("---\n\n")

        # 统计信息
        output.append("## 统计信息\n\n")
        output.append(f"- **总来源数**: {metadata['total_sources']}\n")
        output.append(
            f"- **分类数量**: {len(set(s['category'] for s in self.index_data['sources']))}\n")
        output.append(
            f"- **总字数**: {sum(s['word_count'] for s in self.index_data['sources'])}\n\n")

        # 分类统计
        category_stats = {}
        for source in self.index_data['sources']:
            category = source['category']
            if category not in category_stats:
                category_stats[category] = {'count': 0, 'words': 0}
            category_stats[category]['count'] += 1
            category_stats[category]['words'] += source['word_count']

        output.append("## 分类统计\n\n")
        for category, stats in category_stats.items():
            output.append(
                f"- **{category}**: {stats['count']} 个来源, {stats['words']} 字\n")
        output.append("\n")

        # 关键概念
        output.append("## 关键概念\n\n")
        all_concepts = set()
        for source in self.index_data['sources']:
            all_concepts.update(source['key_concepts'])

        for concept in sorted(all_concepts):
            output.append(f"- {concept}\n")
        output.append("\n")

        # 关系网络
        relationships = self.index_data['relationships']
        output.append("## 概念关系\n\n")
        output.append("### 核心概念\n")
        for concept in relationships['core_concepts']:
            output.append(f"- {concept}\n")
        output.append("\n")

        output.append("### 相关主题\n")
        for topic in relationships['related_topics']:
            output.append(f"- {topic}\n")
        output.append("\n")

        output.append("### 实践应用\n")
        for app in relationships['practical_applications']:
            output.append(f"- {app}\n")
        output.append("\n")

        output.append("### 批判观点\n")
        for viewpoint in relationships['critical_viewpoints']:
            output.append(f"- {viewpoint}\n")
        output.append("\n")

        return ''.join(output)

    def generate_document(self, layout_type: str = 'thematic') -> str:
        """生成指定格式的文档"""
        if layout_type == 'thematic':
            return self.generate_thematic_document()
        elif layout_type == 'source_based':
            return self.generate_source_based_document()
        elif layout_type == 'concepts':
            return self.generate_concepts_document()
        elif layout_type == 'summary':
            return self.generate_summary_document()
        elif layout_type == 'html':
            return self.generate_html_document()
        else:
            raise ValueError(f"不支持的布局类型: {layout_type}")

    def save_document(self, content: str, output_path: str) -> None:
        """保存文档到文件"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"文档已保存到: {output_path}")
        except Exception as e:
            print(f"保存文档时发生错误: {e}")


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='根据JSON索引文件生成不同格式的阅读文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python gen_reading_md.py -i 索引文件.json -o 输出目录
  python gen_reading_md.py -i 索引文件.json -o 输出目录 -l thematic
  python gen_reading_md.py -i 索引文件.json -o 输出目录 -l html -t 主题名称
        '''
    )

    parser.add_argument(
        '-i', '--index',
        required=True,
        help='JSON索引文件路径'
    )

    parser.add_argument(
        '-k', '--kb-dir',
        required=True,
        help='知识库根目录路径'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='输出目录路径'
    )

    parser.add_argument(
        '-l', '--layout',
        choices=['thematic', 'source_based',
                 'concepts', 'summary', 'html', 'all'],
        default='all',
        help='文档布局类型 (默认: all)'
    )

    parser.add_argument(
        '-t', '--topic',
        help='自定义主题名称 (默认使用JSON中的主题)'
    )

    parser.add_argument(
        '--no-source-content',
        action='store_true',
        help='不包含原始文件内容，仅生成索引信息'
    )

    return parser.parse_args()


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()

    index_file = args.index
    output_dir = args.output
    kb_dir = args.kb_dir
    layout_type = args.layout
    custom_topic = args.topic
    no_source_content = args.no_source_content

    try:
        # 创建生成器
        generator = MDDocumentGenerator(index_file, kb_dir)

        # 如果有自定义主题名称，更新索引数据
        if custom_topic:
            generator.index_data['metadata']['topic'] = custom_topic

        # 设置是否包含原始内容
        generator.include_source_content = not no_source_content

        # 确定要生成的布局类型
        if layout_type == 'all':
            layouts = ['thematic', 'source_based',
                       'concepts', 'summary', 'html']
        else:
            layouts = [layout_type]

        # 生成文档
        for layout in layouts:
            print(f"正在生成 {layout} 格式的文档...")

            # 生成文档内容
            content = generator.generate_document(layout)

            # 确定输出文件名
            topic_name = generator.index_data['metadata']['topic']
            if layout == 'html':
                output_file = os.path.join(
                    output_dir, f"{topic_name}_{layout}_文档.html")
            else:
                output_file = os.path.join(
                    output_dir, f"{topic_name}_{layout}_文档.md")

            # 保存文档
            generator.save_document(content, output_file)

            print(f"{layout} 格式文档生成完成!")

        print("\n所有文档生成完成!")
        print(f"输出目录: {output_dir}")

    except Exception as e:
        print(f"生成文档时发生错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()

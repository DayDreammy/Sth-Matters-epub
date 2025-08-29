#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社会化主题EPUB电子书生成器
根据JSON索引文件生成EPUB格式的电子书
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from ebooklib import epub
from bs4 import BeautifulSoup
import html

class SocializationEPUBGenerator:
    def __init__(self, index_file_path: str):
        """初始化EPUB生成器"""
        self.index_file_path = index_file_path
        self.index_data = self._load_index()
        
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
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"无法读取文件: {file_path}"
        except Exception as e:
            return f"读取文件时发生错误: {e}"
    
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
        html = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
        
        # 处理粗体 (**text** 和 __text__)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
        
        # 处理斜体 (*text* 和 _text_)
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
        html = re.sub(r'_([^_]+)_', r'<em>\1</em>', html)
        
        # 处理链接 [text](url)
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        
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
        html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
        
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
                        result.append('<p>' + ' '.join(current_paragraph) + '</p>')
                        current_paragraph = []
                        in_paragraph = False
                    result.append(line)
                    continue
                
                # 跳过空行
                if not stripped_line:
                    if in_paragraph:
                        result.append('<p>' + ' '.join(current_paragraph) + '</p>')
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
    
    def _create_chapter_content(self, source: Dict[str, Any]) -> str:
        """创建章节内容"""
        content = self._read_source_file(source['file_path'])
        html_content = self._markdown_to_html(content)
        
        # 创建章节HTML
        chapter_html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{html.escape(source['title'])}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
                    line-height: 1.8;
                    margin: 2em;
                    text-align: justify;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #333;
                    margin-top: 1.5em;
                    margin-bottom: 0.8em;
                    font-weight: 600;
                }}
                h1 {{
                    font-size: 2em;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 0.5em;
                }}
                h2 {{
                    font-size: 1.5em;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 0.3em;
                }}
                h3 {{
                    font-size: 1.25em;
                }}
                p {{
                    margin-bottom: 1em;
                }}
                ul, ol {{
                    margin: 1em 0;
                    padding-left: 2em;
                }}
                li {{
                    margin-bottom: 0.5em;
                }}
                blockquote {{
                    border-left: 4px solid #667eea;
                    margin: 1em 0;
                    padding: 0.5em 1em;
                    background: #f8f9fa;
                    font-style: italic;
                }}
                pre {{
                    background: #2d3748;
                    color: #e2e8f0;
                    padding: 1em;
                    border-radius: 0.3em;
                    overflow-x: auto;
                    margin: 1em 0;
                }}
                code {{
                    background: #e2e8f0;
                    color: #2d3748;
                    padding: 0.2em 0.4em;
                    border-radius: 0.2em;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 0.9em;
                }}
                pre code {{
                    background: none;
                    color: inherit;
                    padding: 0;
                }}
                a {{
                    color: #667eea;
                    text-decoration: none;
                }}
                hr {{
                    border: none;
                    height: 1px;
                    background: #ddd;
                    margin: 2em 0;
                }}
                strong {{
                    font-weight: 600;
                    color: #2d3748;
                }}
                em {{
                    font-style: italic;
                    color: #4a5568;
                }}
                .source-info {{
                    background: #f8f9fa;
                    padding: 1em;
                    border-radius: 0.3em;
                    margin-bottom: 2em;
                    font-size: 0.9em;
                    color: #666;
                }}
                .tags {{
                    margin-top: 0.5em;
                }}
                .tag {{
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 0.2em 0.5em;
                    border-radius: 0.2em;
                    font-size: 0.8em;
                    margin-right: 0.3em;
                }}
            </style>
        </head>
        <body>
            <div class="source-info">
                <h2>{html.escape(os.path.splitext(os.path.basename(source['file_path']))[0])}</h2>
            </div>
            <div class="content">
                {html_content}
            </div>
        </body>
        </html>
        """
        
        return chapter_html
    
    def generate_epub(self, output_path: str) -> None:
        """生成EPUB文件"""
        # 创建EPUB书籍
        book = epub.EpubBook()
        
        # 设置元数据
        metadata = self.index_data['metadata']
        total_words = sum(s["word_count"] for s in self.index_data["sources"])
        
        book.set_identifier(f'socialization-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
        book.set_title(f'{metadata["topic"]} - 知识文档合集')
        book.set_language('zh-CN')
        book.add_author('Claude Code')
        book.add_metadata('DC', 'description', f'{metadata["topic"]}主题的深度知识合集，包含{metadata["total_sources"]}篇精选文章，总字数约{total_words}字。涵盖核心理论、批判分析、家庭教育、人格发展等多个维度，是理解社会化概念的完整知识体系。')
        book.add_metadata('DC', 'publisher', 'Claude Code')
        book.add_metadata('DC', 'date', datetime.now().strftime('%Y-%m-%d'))
        book.add_metadata('DC', 'subject', '社会化,家庭教育,人格发展,伦理学,社会学')
        book.add_metadata('DC', 'rights', 'Generated by Claude Code for personal use')
        
        # 添加微信读书优化的元数据
        book.add_metadata('DC', 'type', 'Knowledge Collection')
        book.add_metadata('DC', 'format', 'EPUB')
        book.add_metadata('DC', 'coverage', 'Social Sciences, Education, Psychology')
        
        # 创建封面页面
        total_words = sum(s["word_count"] for s in self.index_data["sources"])
        cover_html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>封面</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
                    text-align: center;
                    padding: 2em;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    margin: 0;
                }}
                h1 {{
                    font-size: 2.5em;
                    margin-bottom: 0.3em;
                    font-weight: 700;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .subtitle {{
                    font-size: 1.3em;
                    margin-bottom: 2em;
                    opacity: 0.9;
                    font-weight: 300;
                }}
                .info {{
                    background: rgba(255, 255, 255, 0.15);
                    padding: 2em;
                    border-radius: 1em;
                    margin: 1em auto;
                    max-width: 400px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                .stat {{
                    margin: 0.8em 0;
                    font-size: 1.1em;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }}
                .stat-icon {{
                    margin-right: 0.5em;
                }}
                .generated {{
                    position: absolute;
                    bottom: 2em;
                    left: 0;
                    right: 0;
                    font-size: 0.9em;
                    opacity: 0.7;
                }}
                .description {{
                    max-width: 500px;
                    margin: 0 auto 2em;
                    font-size: 1.1em;
                    line-height: 1.6;
                    opacity: 0.9;
                }}
            </style>
        </head>
        <body>
            <h1>{metadata["topic"]}</h1>
            <div class="subtitle">深度知识文档合集</div>
            <div class="description">
                涵盖核心理论、批判分析、家庭教育、人格发展等多个维度的完整知识体系
            </div>
            <div class="info">
                <div class="stat">
                    <span><span class="stat-icon">📚</span> 来源数量</span>
                    <span>{metadata["total_sources"]} 篇</span>
                </div>
                <div class="stat">
                    <span><span class="stat-icon">📝</span> 总字数</span>
                    <span>{total_words:,} 字</span>
                </div>
                <div class="stat">
                    <span><span class="stat-icon">📂</span> 分类数量</span>
                    <span>{len(set(s["category"] for s in self.index_data["sources"]))} 个</span>
                </div>
                <div class="stat">
                    <span><span class="stat-icon">📅</span> 生成日期</span>
                    <span>{datetime.now().strftime("%Y-%m-%d")}</span>
                </div>
            </div>
            <div class="generated">
                由 Claude Code 自动生成 | 适用于微信读书
            </div>
        </body>
        </html>
        """
        
        # 创建封面章节
        cover_chapter = epub.EpubHtml(
            title='封面',
            file_name='cover.xhtml',
            content=cover_html,
            lang='zh-CN'
        )
        book.add_item(cover_chapter)
        
        # 创建目录页面
        toc_html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>目录</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
                    line-height: 1.8;
                    margin: 2em;
                }
                h1 {
                    color: #333;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 0.5em;
                }
                .toc-entry {
                    margin: 1em 0;
                }
                .toc-entry a {
                    color: #667eea;
                    text-decoration: none;
                    font-size: 1.1em;
                }
                .toc-entry a:hover {
                    text-decoration: underline;
                }
                .category {
                    background: #667eea;
                    color: white;
                    padding: 0.2em 0.5em;
                    border-radius: 0.2em;
                    font-size: 0.8em;
                    margin-left: 0.5em;
                }
            </style>
        </head>
        <body>
            <h1>📚 目录</h1>
        """
        
        # 按分类分组
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
        
        chapter_id = 1
        chapters = []
        
        for category, sources in category_groups.items():
            category_name = category_names.get(category, category)
            toc_html += f'<h2>{category_name} <span class="category">{len(sources)}篇</span></h2>'
            
            for source in sources:
                chapter_filename = f'chapter_{chapter_id:03d}.xhtml'
                toc_html += f'<div class="toc-entry"><a href="{chapter_filename}">{source["title"]}</a></div>'
                
                # 创建章节内容
                chapter_content = self._create_chapter_content(source)
                chapter = epub.EpubHtml(
                    title=source['title'],
                    file_name=chapter_filename,
                    content=chapter_content,
                    lang='zh-CN'
                )
                book.add_item(chapter)
                chapters.append(chapter)
                chapter_id += 1
        
        toc_html += """
        </body>
        </html>
        """
        
        # 创建目录章节
        toc_chapter = epub.EpubHtml(
            title='目录',
            file_name='toc.xhtml',
            content=toc_html,
            lang='zh-CN'
        )
        book.add_item(toc_chapter)
        
        # 设置目录
        book.toc = (toc_chapter, cover_chapter, *chapters)
        
        # 添加导航文件
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # 设置spine
        book.spine = ['cover', 'nav', 'toc'] + [chapter for chapter in chapters]
        
        # 写入EPUB文件
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            epub.write_epub(output_path, book, {})
            print(f"EPUB文件已生成: {output_path}")
        except Exception as e:
            print(f"生成EPUB文件时发生错误: {e}")
            raise


def main():
    """主函数 - 示例用法"""
    # 设置文件路径
    index_file = r"D:\yy\Sth-Matters\_对话检索汇编\社会化_索引.json"
    output_dir = r"D:\yy\Sth-Matters\_对话检索汇编\generated_docs"
    
    try:
        # 创建生成器
        generator = SocializationEPUBGenerator(index_file)
        
        # 生成EPUB文件
        output_file = os.path.join(output_dir, f"社会化_{datetime.now().strftime('%Y%m%d_%H%M%S')}.epub")
        
        print("正在生成EPUB文件...")
        generator.generate_epub(output_file)
        
        print("EPUB文件生成完成!")
        print(f"输出文件: {output_file}")
        print("现在可以将此文件导入到微信读书中阅读了！")
        
    except Exception as e:
        print(f"生成EPUB文件时发生错误: {e}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社会化主题阅读文档生成器
根据JSON索引文件生成不同格式的阅读文档
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class SocializationDocumentGenerator:
    def __init__(self, index_file_path: str):
        """初始化文档生成器"""
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
    
    def _format_source_header(self, source: Dict[str, Any]) -> str:
        """格式化来源标题头部"""
        header = f"### {source['title']}\n\n"
        
        if source.get('zhihu_link'):
            header += f"**知乎链接**: [{source['title']}]({source['zhihu_link']})  \n"
        
        header += f"**文件来源**: `{source['file_path']}`\n"
        header += f"**分类**: {source['category']}\n"
        header += f"**标签**: {', '.join(source['tags'])}\n"
        header += f"**字数**: {source['word_count']}\n"
        header += f"**关键概念**: {', '.join(source['key_concepts'])}\n\n"
        
        return header
    
    def generate_thematic_document(self) -> str:
        """生成按主题分类的文档"""
        output = []
        
        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 主题分类阅读文档\n")
        output.append(f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
                    output.append("```\n")
                    output.append(content[:1000] + "..." if len(content) > 1000 else content)
                    output.append("\n```\n\n")
                else:
                    output.append("```\n")
                    output.append(content)
                    output.append("\n```\n\n")
                
                output.append("---\n\n")
        
        return ''.join(output)
    
    def generate_source_based_document(self) -> str:
        """生成按来源分组的文档"""
        output = []
        
        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 来源分组阅读文档\n")
        output.append(f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
                output.append("```\n")
                output.append(content)
                output.append("\n```\n\n")
            
            output.append("---\n\n")
        
        return ''.join(output)
    
    def generate_concepts_document(self) -> str:
        """生成按关键概念组织的文档"""
        output = []
        
        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 关键概念文档\n")
        output.append(f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
                output.append(f"### {source['title']}\n\n")
                output.append(f"**文件来源**: `{source['file_path']}`\n\n")
                output.append(f"> {source['content_preview']}\n\n")
            
            output.append("---\n\n")
        
        return ''.join(output)
    
    def generate_summary_document(self) -> str:
        """生成概要文档"""
        output = []
        
        # 文档头部
        metadata = self.index_data['metadata']
        output.append(f"# {metadata['topic']} - 内容概要\n")
        output.append(f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.append(f"**主题**: {metadata['topic']}\n")
        output.append(f"**来源数量**: {metadata['total_sources']}\n")
        output.append("---\n\n")
        
        # 统计信息
        output.append("## 统计信息\n\n")
        output.append(f"- **总来源数**: {metadata['total_sources']}\n")
        output.append(f"- **分类数量**: {len(set(s['category'] for s in self.index_data['sources']))}\n")
        output.append(f"- **总字数**: {sum(s['word_count'] for s in self.index_data['sources'])}\n\n")
        
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
            output.append(f"- **{category}**: {stats['count']} 个来源, {stats['words']} 字\n")
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


def main():
    """主函数 - 示例用法"""
    # 设置文件路径
    index_file = r"D:\yy\Sth-Matters\_对话检索汇编\社会化_索引.json"
    output_dir = r"D:\yy\Sth-Matters\_对话检索汇编\generated_docs"
    
    try:
        # 创建生成器
        generator = SocializationDocumentGenerator(index_file)
        
        # 生成不同格式的文档
        layouts = ['thematic', 'source_based', 'concepts', 'summary']
        
        for layout in layouts:
            print(f"正在生成 {layout} 格式的文档...")
            
            # 生成文档内容
            content = generator.generate_document(layout)
            
            # 保存文档
            output_file = os.path.join(output_dir, f"社会化_{layout}_文档.md")
            generator.save_document(content, output_file)
            
            print(f"{layout} 格式文档生成完成!")
        
        print("\n所有文档生成完成!")
        print(f"输出目录: {output_dir}")
        
    except Exception as e:
        print(f"生成文档时发生错误: {e}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社会化主题文档批量生成器
一键生成所有格式的文档：Markdown、HTML、EPUB
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from generate_reading_doc import SocializationDocumentGenerator
from generate_epub import SocializationEPUBGenerator

def main():
    """主函数 - 批量生成所有格式文档"""
    # 设置文件路径
    index_file = r"D:\yy\Sth-Matters\_对话检索汇编\社会化_索引.json"
    output_dir = r"D:\yy\Sth-Matters\_对话检索汇编\generated_docs"
    
    try:
        print("=" * 60)
        print("🚀 开始批量生成社会化主题文档")
        print("=" * 60)
        
        # 1. 生成Markdown格式文档
        print("\n📝 生成Markdown格式文档...")
        md_generator = SocializationDocumentGenerator(index_file)
        md_layouts = ['thematic', 'source_based', 'concepts', 'summary']
        
        for layout in md_layouts:
            print(f"   正在生成 {layout} 格式...")
            content = md_generator.generate_document(layout)
            output_file = os.path.join(output_dir, f"社会化_{layout}_文档.md")
            md_generator.save_document(content, output_file)
            print(f"   ✅ {layout} 格式完成")
        
        # 2. 生成HTML格式文档
        print("\n🌐 生成HTML格式文档...")
        html_content = md_generator.generate_document('html')
        html_file = os.path.join(output_dir, f"社会化_html_文档.html")
        md_generator.save_document(html_content, html_file)
        print("   ✅ HTML格式完成")
        
        # 3. 生成EPUB格式文档
        print("\n📚 生成EPUB格式文档...")
        epub_generator = SocializationEPUBGenerator(index_file)
        epub_file = os.path.join(output_dir, f"社会化_{datetime.now().strftime('%Y%m%d_%H%M%S')}.epub")
        epub_generator.generate_epub(epub_file)
        print("   ✅ EPUB格式完成")
        
        # 4. 生成汇总报告
        print("\n📊 生成汇总报告...")
        report_content = generate_summary_report(index_file, output_dir)
        report_file = os.path.join(output_dir, f"生成报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print("   ✅ 汇总报告完成")
        
        print("\n" + "=" * 60)
        print("🎉 所有文档生成完成！")
        print("=" * 60)
        print(f"\n📁 输出目录: {output_dir}")
        print("\n📄 生成的文件:")
        
        # 列出生成的文件
        for filename in os.listdir(output_dir):
            if filename.startswith('社会化_') or filename.endswith('.epub'):
                filepath = os.path.join(output_dir, filename)
                file_size = os.path.getsize(filepath)
                size_mb = file_size / (1024 * 1024)
                print(f"   • {filename} ({size_mb:.2f} MB)")
        
        print(f"\n📋 汇总报告: {os.path.basename(report_file)}")
        print("\n💡 使用建议:")
        print("   • Markdown文件: 适合编辑和进一步处理")
        print("   • HTML文件: 适合浏览器阅读，支持交互")
        print("   • EPUB文件: 适合导入微信读书等电子书阅读器")
        print("   • 汇总报告: 记录生成过程和文件信息")
        
    except Exception as e:
        print(f"\n❌ 生成过程中发生错误: {e}")
        raise

def generate_summary_report(index_file: str, output_dir: str) -> str:
    """生成汇总报告"""
    # 加载索引数据
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    metadata = index_data['metadata']
    total_words = sum(s["word_count"] for s in index_data["sources"])
    
    # 统计生成的文件
    generated_files = []
    for filename in os.listdir(output_dir):
        if filename.startswith('社会化_') or filename.endswith('.epub'):
            filepath = os.path.join(output_dir, filename)
            file_size = os.path.getsize(filepath)
            size_mb = file_size / (1024 * 1024)
            generated_files.append({
                'filename': filename,
                'size_mb': size_mb,
                'format': filename.split('.')[-1] if '.' in filename else 'unknown'
            })
    
    report = f"""# 社会化主题文档生成报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**主题**: {metadata['topic']}
**生成工具**: Claude Code 知识管理系统

## 📊 数据统计

- **来源数量**: {metadata['total_sources']} 篇
- **总字数**: {total_words:,} 字
- **分类数量**: {len(set(s['category'] for s in index_data['sources']))} 个
- **关键概念**: {len(set(concept for s in index_data['sources'] for concept in s['key_concepts']))} 个

## 📄 生成的文件

| 文件名 | 格式 | 大小 (MB) | 用途 |
|--------|------|----------|------|
"""
    
    for file_info in generated_files:
        format_descriptions = {
            'md': 'Markdown文档，适合编辑',
            'html': 'HTML文档，适合浏览器阅读',
            'epub': 'EPUB电子书，适合微信读书',
            'unknown': '未知格式'
        }
        
        description = format_descriptions.get(file_info['format'], '其他格式')
        report += f"| {file_info['filename']} | {file_info['format'].upper()} | {file_info['size_mb']:.2f} | {description} |\n"
    
    report += f"""
## 📚 内容分类

"""
    
    # 按分类统计
    category_stats = {}
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
    
    for source in index_data['sources']:
        category = source['category']
        if category not in category_stats:
            category_stats[category] = {'count': 0, 'words': 0}
        category_stats[category]['count'] += 1
        category_stats[category]['words'] += source['word_count']
    
    report += "| 分类 | 篇数 | 字数 | 占比 |\n"
    report += "|------|------|------|------|\n"
    
    for category, stats in category_stats.items():
        category_name = category_names.get(category, category)
        percentage = (stats['words'] / total_words) * 100
        report += f"| {category_name} | {stats['count']} | {stats['words']:,} | {percentage:.1f}% |\n"
    
    report += f"""
## 🔧 技术特性

### Markdown文档
- 支持多种布局方式（主题分类、来源分组、概念组织、概要统计）
- 移除了代码块包装，保持原始markdown格式
- 包含完整的元数据和引用信息

### HTML文档  
- 响应式设计，支持移动设备
- 完整的markdown到HTML转换
- 交互式目录导航
- 现代化UI设计
- 优化的阅读体验

### EPUB文档
- 标准EPUB格式，兼容主流电子书阅读器
- 特别优化了微信读书体验
- 完整的书籍元数据
- 精美的封面设计
- 结构化的章节组织

## 💡 使用指南

### 微信读书使用方法
1. 将生成的EPUB文件传输到手机
2. 打开微信读书应用
3. 点击"+"号或"导入"按钮
4. 选择EPUB文件导入
5. 享受高质量的阅读体验

### 其他阅读器
- 支持Apple Books、Google Play Books等主流阅读器
- 支持Kindle（可能需要格式转换）
- 支持任意支持EPUB标准的电子书阅读器

## 📝 备注

- 所有文档均基于原始JSON索引数据生成
- 保留了完整的引用链接和来源信息
- 支持中文字符和复杂格式
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*由 Claude Code 知识管理系统自动生成*
"""
    
    return report

if __name__ == "__main__":
    main()
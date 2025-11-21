#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复扩展搜索结果格式问题
确保JSON文件格式正确，可以用于文档生成
"""

import json
import os

def fix_expanded_results():
    base_dir = os.getcwd()
    output_dir = os.path.join(base_dir, '_对话检索汇编')
    input_file = os.path.join(output_dir, '社会化_扩展搜索结果.json')
    output_file = os.path.join(output_dir, '社会化_扩展搜索结果_修复版.json')

    # 读取原始文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 修复relationships部分，确保所有字段都存在
    if 'relationships' not in data:
        data['relationships'] = {}

    relationships = data['relationships']

    # 确保所有必需的关系字段都存在
    default_relationships = {
        "core_concepts": [],
        "related_topics": [],
        "practical_applications": [],
        "critical_viewpoints": [],
        "theoretical_frameworks": [],
        "developmental_stages": [],
        "cross_disciplinary": []
    }

    for key, default_value in default_relationships.items():
        if key not in relationships:
            relationships[key] = default_value

    # 确保sources中所有文件都有必需的字段
    required_fields = [
        'id', 'title', 'file_path', 'zhihu_link', 'category',
        'tags', 'content_preview', 'word_count', 'key_concepts'
    ]

    for i, source in enumerate(data['sources']):
        # 确保有必需的字段
        for field in required_fields:
            if field not in source:
                if field == 'tags' or field == 'key_concepts':
                    source[field] = []
                elif field == 'word_count':
                    source[field] = 0
                elif field == 'category':
                    source[field] = 'general'
                elif field == 'content_preview':
                    source[field] = 'No preview available'
                else:
                    source[field] = ''

        # 确保id是唯一的
        source['id'] = i + 1

    # 重新计算关系映射
    print("重新计算概念关系...")

    # 提取所有概念
    all_concepts = []
    all_tags = []
    all_categories = set()

    for source in data['sources']:
        if 'key_concepts' in source and isinstance(source['key_concepts'], list):
            all_concepts.extend(source['key_concepts'])
        if 'tags' in source and isinstance(source['tags'], list):
            all_tags.extend(source['tags'])
        if 'category' in source:
            all_categories.add(source['category'])

    # 统计概念频率
    from collections import Counter
    concept_counter = Counter(all_concepts)
    tag_counter = Counter(all_tags)

    # 更新关系映射
    relationships['core_concepts'] = [concept for concept, count in concept_counter.most_common(30)]
    relationships['related_topics'] = [tag for tag, count in tag_counter.most_common(20)]
    relationships['practical_applications'] = [concept for concept in concept_counter.most_common(15) if any(keyword in concept for keyword in ['方法', '技巧', '应用', '实践', '教育', '沟通'])]
    relationships['critical_viewpoints'] = [concept for concept in concept_counter.most_common(15) if any(keyword in concept for keyword in ['批判', '问题', '挑战', '困难', '矛盾', '冲突'])]

    # 添加元数据
    data['metadata']['processing_note'] = '修复版 - 确保格式兼容性'
    data['metadata']['total_concepts'] = len(all_concepts)
    data['metadata']['total_categories'] = len(all_categories)

    # 保存修复后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"修复后的文件已保存到: {output_file}")
    print(f"总文件数: {len(data['sources'])}")
    print(f"总概念数: {len(all_concepts)}")
    print(f"总分类数: {len(all_categories)}")

    return output_file

if __name__ == "__main__":
    fix_expanded_results()
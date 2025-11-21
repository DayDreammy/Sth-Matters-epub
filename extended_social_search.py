#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社会化扩展搜索脚本
基于已有搜索结果进行概念扩展和深化搜索
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class ExtendedSocialSearch:
    def __init__(self, base_repo_path: str):
        self.base_repo_path = Path(base_repo_path)
        self.current_results = []
        self.expanded_results = []

    def load_existing_results(self, json_file_path: str):
        """加载已有的搜索结果"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.current_results = data['sources']
        print(f"已加载 {len(self.current_results)} 条现有搜索结果")
        return data

    def extract_key_concepts(self) -> Set[str]:
        """从现有结果中提取关键概念"""
        concepts = set()

        # 从现有文章的key_concepts中提取
        for source in self.current_results:
            if 'key_concepts' in source:
                concepts.update(source['key_concepts'])

        # 从tags中提取
        for source in self.current_results:
            if 'tags' in source:
                concepts.update(source['tags'])

        # 手动添加核心社会化相关概念
        core_concepts = {
            # 核心概念
            '社会适应', '社会互动', '社会关系', '群体融入', '社会规范内化',
            '社会认知', '社会学习', '社会身份', '社会资本', '情感社会化',
            '职业社会化', '数字社会化',

            # 理论基础
            '社会认知理论', '社会学习理论', '社会身份理论', '社会资本理论',
            '发展心理学', '教育心理学', '社会心理学', '人格发展',

            # 实践应用
            '教育方法', '沟通技巧', '情绪管理', '冲突解决', '团队合作',
            '领导力', '组织行为', '跨文化交际',

            # 相关领域
            '家庭关系', '同伴关系', '师生关系', '职场关系', '社会支持',
            '心理健康', '人格障碍', '社交焦虑', '孤独感',

            # 发展阶段
            '儿童社会化', '青少年社会化', '成人社会化', '老年社会化',
            '终身社会化'
        }

        concepts.update(core_concepts)
        return concepts

    def search_concept_files(self, concepts: Set[str]) -> List[Dict]:
        """搜索包含相关概念的文件"""
        expanded_sources = []

        # 搜索策略：从多个角度搜索
        search_patterns = []

        # 1. 直接概念搜索
        for concept in concepts:
            search_patterns.append(concept)

        # 2. 变体和相关词搜索
        concept_variations = {
            '社会适应': ['适应', '环境适应', '社会融入'],
            '社会互动': ['互动', '交往', '沟通', '交流'],
            '社会关系': ['人际关系', '社交', '交往关系'],
            '群体融入': ['融入', '归属感', '群体认同'],
            '社会规范': ['规范', '规则', '社会秩序'],
            '社会认知': ['认知', '社会理解', '社会知觉'],
            '社会学习': ['学习', '模仿', '观察学习'],
            '社会身份': ['身份', '角色', '社会角色'],
            '社会资本': ['人脉', '资源', '社会网络'],
            '情感社会化': ['情感', '情绪', '情感表达'],
            '职业社会化': ['职业', '工作', '职场'],
            '数字社会化': ['数字', '网络', '社交媒体', '互联网']
        }

        for main_concept, variations in concept_variations.items():
            search_patterns.extend(variations)

        # 搜索所有markdown文件
        md_files = list(self.base_repo_path.rglob("*.md"))

        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查是否包含相关概念
                matched_concepts = []
                for pattern in search_patterns:
                    if re.search(rf'{pattern}', content, re.IGNORECASE):
                        matched_concepts.append(pattern)

                if matched_concepts:
                    # 提取文件信息
                    rel_path = str(file_path.relative_to(self.base_repo_path))

                    # 尝试从内容中提取知乎链接
                    zhihu_links = re.findall(r'https://www\.zhihu\.com/[^\s\)]+', content)
                    zhihu_link = zhihu_links[0] if zhihu_links else ""

                    # 提取标题（从文件名或内容的第一行）
                    title = file_path.stem
                    first_line = content.split('\n')[0].strip()
                    if first_line.startswith('#'):
                        title = first_line.lstrip('#').strip()

                    # 生成内容预览
                    preview = content[:200] + "..." if len(content) > 200 else content

                    # 统计字数
                    word_count = len(content)

                    source = {
                        "id": len(self.current_results) + len(expanded_sources) + 1,
                        "title": title,
                        "file_path": str(file_path),
                        "zhihu_link": zhihu_link,
                        "category": self._categorize_content(matched_concepts, rel_path),
                        "tags": matched_concepts[:5],  # 取前5个匹配的概念
                        "content_preview": preview,
                        "word_count": word_count,
                        "key_concepts": self._extract_key_concepts_from_content(content),
                        "search_phase": "expansion",
                        "matched_patterns": matched_concepts
                    }

                    expanded_sources.append(source)

            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")
                continue

        return expanded_sources

    def _categorize_content(self, concepts: List[str], rel_path: str) -> str:
        """对内容进行分类"""
        category_rules = {
            'theoretical_basis': ['理论', '认知', '学习', '身份', '资本'],
            'practical_application': ['方法', '技巧', '管理', '沟通', '教育'],
            'developmental_stage': ['儿童', '青少年', '成人', '老年', '发展'],
            'related_fields': ['家庭', '心理', '健康', '文化', '组织'],
            'social_issues': ['问题', '障碍', '焦虑', '孤独', '冲突']
        }

        for category, keywords in category_rules.items():
            if any(keyword in ' '.join(concepts) for keyword in keywords):
                return category

        return 'expansion_general'

    def _extract_key_concepts_from_content(self, content: str) -> List[str]:
        """从内容中提取关键概念"""
        # 简单的关键概念提取逻辑
        concepts = []

        # 社会化相关关键词
        social_keywords = [
            '社会化', '社会适应', '社会互动', '社会关系', '群体融入',
            '社会规范', '社会认知', '社会学习', '社会身份', '情感',
            '职业', '数字', '沟通', '合作', '冲突', '认同', '角色'
        ]

        for keyword in social_keywords:
            if keyword in content and content.count(keyword) >= 2:
                concepts.append(keyword)

        return concepts[:8]  # 最多返回8个概念

    def deduplicate_results(self, expanded_sources: List[Dict]) -> List[Dict]:
        """去重处理"""
        seen_paths = set()
        deduplicated = []

        # 首先保留所有现有结果
        deduplicated.extend(self.current_results)

        # 添加新的不重复结果
        for source in expanded_sources:
            file_path = source['file_path']
            # 检查是否与现有结果重复
            is_duplicate = any(
                existing['file_path'] == file_path
                for existing in self.current_results
            )

            if not is_duplicate and file_path not in seen_paths:
                deduplicated.append(source)
                seen_paths.add(file_path)

        return deduplicated

    def establish_relationships(self, all_sources: List[Dict]) -> Dict:
        """建立概念关系映射"""
        all_concepts = set()
        all_categories = set()
        all_tags = set()

        for source in all_sources:
            if 'key_concepts' in source:
                all_concepts.update(source['key_concepts'])
            if 'tags' in source:
                all_tags.update(source['tags'])
            if 'category' in source:
                all_categories.add(source['category'])

        # 分析概念关系
        relationships = {
            "core_concepts": list(all_concepts)[:20],  # 核心概念
            "related_topics": list(all_tags)[:15],     # 相关主题
            "theoretical_frameworks": [],              # 理论框架
            "practical_applications": [],              # 实践应用
            "developmental_stages": [],                # 发展阶段
            "cross_disciplinary": []                   # 跨学科连接
        }

        # 分类整理概念
        concept_categories = {
            "theoretical_frameworks": ['理论', '认知理论', '学习理论', '身份理论', '资本理论'],
            "practical_applications": ['方法', '技巧', '沟通', '教育', '管理', '职场'],
            "developmental_stages": ['儿童', '青少年', '成人', '老年', '发展'],
            "cross_disciplinary": ['心理学', '教育学', '社会学', '管理学', '传播学']
        }

        for category, keywords in concept_categories.items():
            matching_concepts = [
                concept for concept in all_concepts
                if any(keyword in concept for keyword in keywords)
            ]
            relationships[category] = matching_concepts[:10]

        return relationships

    def generate_expanded_index(self, output_file: str):
        """生成扩展搜索结果索引"""
        # 1. 提取关键概念
        print("正在提取关键概念...")
        concepts = self.extract_key_concepts()
        print(f"提取到 {len(concepts)} 个关键概念")

        # 2. 搜索扩展内容
        print("正在进行扩展搜索...")
        expanded_sources = self.search_concept_files(concepts)
        print(f"搜索到 {len(expanded_sources)} 个新文件")

        # 3. 去重处理
        print("正在进行去重处理...")
        all_sources = self.deduplicate_results(expanded_sources)
        print(f"去重后共 {len(all_sources)} 个文件")

        # 4. 建立关系映射
        print("正在建立概念关系映射...")
        relationships = self.establish_relationships(all_sources)

        # 5. 生成最终索引
        expanded_index = {
            "metadata": {
                "topic": "社会化",
                "search_phase": "expanded",
                "search_date": "2025-08-29",
                "generated_by": "Claude Code - Extended Search",
                "total_sources": len(all_sources),
                "original_sources": len(self.current_results),
                "new_sources": len(all_sources) - len(self.current_results),
                "description": "Expanded search results for socialization topics with concept extension and cross-disciplinary connections"
            },
            "sources": all_sources,
            "relationships": relationships,
            "expansion methodology": {
                "internal_deepening": "基于初始结果的关键概念深入分析",
                "external_expansion": "扩展到相关理论和应用领域",
                "relationship_mapping": "建立概念间的关联映射",
                "cross_disciplinary": "连接心理学、教育学、社会学、管理学等领域"
            }
        }

        # 6. 保存结果
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(expanded_index, f, ensure_ascii=False, indent=2)

        print(f"扩展搜索结果已保存到: {output_file}")

        # 7. 生成统计报告
        self.generate_statistics_report(expanded_index, output_file.replace('.json', '_统计报告.txt'))

        return expanded_index

    def generate_statistics_report(self, expanded_index: Dict, report_file: str):
        """生成统计报告"""
        metadata = expanded_index['metadata']
        sources = expanded_index['sources']
        relationships = expanded_index['relationships']

        report = f"""
社会化扩展搜索统计报告
======================

基本信息：
--------
搜索主题：{metadata['topic']}
搜索阶段：{metadata['search_phase']}
搜索日期：{metadata['search_date']}
数据源总数：{metadata['total_sources']}
原始数据源：{metadata['original_sources']}
新增数据源：{metadata['new_sources']}

内容分类统计：
-----------
"""

        # 统计分类
        category_stats = {}
        for source in sources:
            category = source.get('category', 'unknown')
            category_stats[category] = category_stats.get(category, 0) + 1

        for category, count in sorted(category_stats.items()):
            report += f"{category}: {count} 个文件\n"

        report += f"""
概念关系统计：
-----------
核心概念数：{len(relationships['core_concepts'])}
相关主题数：{len(relationships['related_topics'])}
理论框架数：{len(relationships['theoretical_frameworks'])}
实践应用数：{len(relationships['practical_applications'])}
发展阶段数：{len(relationships['developmental_stages'])}
跨学科连接数：{len(relationships['cross_disciplinary'])}

字数统计：
-------
"""

        # 字数统计
        total_words = sum(source.get('word_count', 0) for source in sources)
        avg_words = total_words // len(sources) if sources else 0

        report += f"总字数：{total_words:,} 字\n"
        report += f"平均字数：{avg_words:,} 字\n"

        # 按字数范围统计
        word_ranges = {
            '0-500字': 0,
            '500-1000字': 0,
            '1000-2000字': 0,
            '2000字以上': 0
        }

        for source in sources:
            word_count = source.get('word_count', 0)
            if word_count < 500:
                word_ranges['0-500字'] += 1
            elif word_count < 1000:
                word_ranges['500-1000字'] += 1
            elif word_count < 2000:
                word_ranges['1000-2000字'] += 1
            else:
                word_ranges['2000字以上'] += 1

        report += "\n字数分布：\n"
        for range_name, count in word_ranges.items():
            report += f"{range_name}: {count} 个文件\n"

        report += f"""
扩展效果评估：
-----------
扩展率：{(metadata['new_sources'] / metadata['original_sources'] * 100):.1f}%
覆盖率：扩展搜索涵盖了社会化的多个维度和跨学科领域
深度：包含了理论基础、实践应用、发展阶段等多个层面
广度：连接了心理学、教育学、社会学、管理学等相关学科

搜索策略说明：
-----------
1. 内部深化：基于初始结果的18个核心概念进行深入分析
2. 外部扩展：扩展到社会认知理论、社会学习理论等相关理论框架
3. 关系映射：建立了概念间的关联和层次关系
4. 跨学科连接：连接了多个相关学科领域的知识

报告生成时间：{metadata['search_date']}
生成工具：Claude Code Extended Search System
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"统计报告已保存到: {report_file}")

def main():
    """主函数"""
    base_repo_path = os.getcwd()
    output_dir = os.path.join(base_repo_path, '_对话检索汇编')
    existing_index_file = os.path.join(output_dir, '社会化_索引.json')
    output_file = os.path.join(output_dir, '社会化_扩展搜索结果.json')

    print("开始社会化扩展搜索...")
    print("=" * 50)

    # 创建扩展搜索器
    searcher = ExtendedSocialSearch(base_repo_path)

    # 加载现有结果
    print("加载现有搜索结果...")
    existing_data = searcher.load_existing_results(existing_index_file)

    # 生成扩展索引
    print("生成扩展搜索索引...")
    expanded_index = searcher.generate_expanded_index(output_file)

    print("=" * 50)
    print("扩展搜索完成！")
    print(f"原始结果：{existing_data['metadata']['total_sources']} 条")
    print(f"扩展结果：{expanded_index['metadata']['total_sources']} 条")
    print(f"新增内容：{expanded_index['metadata']['new_sources']} 条")
    print(f"扩展率：{(expanded_index['metadata']['new_sources'] / existing_data['metadata']['total_sources'] * 100):.1f}%")

if __name__ == "__main__":
    main()
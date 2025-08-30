# 深度搜索系统 (Deep Search System)

这是一个综合性的中文知识管理仓库的深度搜索系统，能够对任何给定主题进行全面搜索并生成多格式阅读文档。

## 系统工作流程

### 第一阶段：初始深度搜索
**目标**: 进行多角度搜索创建基础索引

**搜索策略**:
- **多维度方法**: 从各种角度和方面进行搜索
- **文件级搜索**: 使用中图法分类系统扫描文件名和目录结构
- **内容级搜索**: 在所有Markdown文件中进行全文搜索
- **标签搜索**: 利用综合标签系统
- **语义搜索**: 理解超越简单关键词匹配的概念

**输出**: 包含以下内容的JSON索引：
- 原始文章内容和元数据
- 知乎链接和来源引用
- 内容分类和标签
- 字数统计和相关性评分
- 关键概念提取

### 第二阶段：概念扩展
**目标**: 基于初始结果深化理解并扩展搜索范围

**过程**:
- **内部深化**: 分析第一阶段结果中的关键概念
- **外部扩展**: 识别相关概念和更广泛的主题
- **关系映射**: 建立概念之间的联系
- **情境丰富化**: 寻找支持和对比的观点

**搜索增强**:
- 从初始结果中提取关键概念
- 搜索相关术语和更广泛的主题
- 识别跨学科联系
- 寻找实际应用和理论框架

### 第三阶段：结果整合
**目标**: 将两个搜索阶段合并为综合索引

**整合过程**:
- 合并初始搜索结果和扩展概念
- 删除重复项并解决冲突
- 建立概念之间的层次关系
- 创建统一的分类系统
- 生成综合元数据

**最终索引结构**:
```json
{
  "metadata": {
    "topic": "搜索主题",
    "search_date": "2025-08-30",
    "total_sources": 25,
    "description": "Comprehensive topic analysis"
  },
  "sources": [
    {
      "id": 1,
      "title": "文章标题",
      "file_path": "完整文件路径",
      "zhihu_link": "知乎原文链接",
      "category": "分类标签",
      "tags": ["相关标签"],
      "content_preview": "内容预览",
      "word_count": 1500,
      "key_concepts": ["关键概念"]
    }
  ],
  "relationships": {
    "core_concepts": [],
    "related_topics": [],
    "practical_applications": [],
    "critical_viewpoints": []
  }
}
```

### 第四阶段：文档生成
**目标**: 从集成索引生成多种格式文档

**JSON索引文件存储**:
- 将第三阶段的集成JSON索引保存到: `_对话检索汇编/[主题]_索引.json`
- 示例文件路径: `_对话检索汇编/社会化_索引.json`

**文档生成工具**:
系统使用灵活的Python脚本 (`gen_reading_md.py`) 处理JSON索引文件并生成各种格式的文档。

**脚本位置**: `_对话检索汇编/scripts/gen_reading_md.py`

**命令行接口**:
```bash
# 进入脚本目录
cd _对话检索汇编/scripts

# 生成文档
python gen_reading_md.py -i ../[主题]_索引.json -o ../generated_docs [OPTIONS]
```

**可用选项**:
- `-i/--index`: JSON索引文件路径 (必需)
- `-o/--output`: 输出目录路径 (必需)
- `-l/--layout`: 文档布局类型 (thematic/source_based/concepts/summary/html/all, 默认all)
- `-t/--topic`: 自定义主题名称
- `--no-source-content`: 不包含原始文件内容

**使用示例**:
```bash
# 生成所有格式文档
python gen_reading_md.py -i ../社会化_索引.json -o ../generated_docs

# 生成特定格式文档
python gen_reading_md.py -i ../社会化_索引.json -o ../generated_docs -l thematic

# 生成HTML文档并自定义主题
python gen_reading_md.py -i ../社会化_索引.json -o ../generated_docs -l html -t "我的主题"

# 不包含原始内容（仅索引信息）
python gen_reading_md.py -i ../社会化_索引.json -o ../generated_docs --no-source-content
```

**输出目录结构**:
```
_对话检索汇编/
├── generated_docs/
│   ├── [主题]_thematic_文档.md
│   ├── [主题]_source_based_文档.md
│   ├── [主题]_concepts_文档.md
│   ├── [主题]_summary_文档.md
│   └── [主题]_html_文档.html
├── scripts/
│   └── gen_reading_md.py
└── [主题]_索引.json
```

**输出格式**:
1. **EPUB电子书**: 优化移动阅读，特别是微信读书
2. **Markdown文档**: 多种布局（主题、来源、概念、概要）
3. **HTML文档**: 网络友好格式，具有交互式导航
4. **阅读汇编**: 按主题和相关性组织

**布局类型**:
- **thematic**: 按主题分类的文档
- **source_based**: 按来源分组的文档
- **concepts**: 按关键概念组织的文档
- **summary**: 内容概要文档
- **html**: 交互式HTML文档

## 使用说明

### 执行深度搜索
1. **第一阶段**: 执行初始深度搜索，创建基础JSON索引
2. **第二阶段**: 基于初始结果进行概念扩展
3. **第三阶段**: 整合所有结果，创建最终JSON索引文件
4. **第四阶段**: 使用文档生成工具创建多格式阅读文档

### 文档生成
1. 将最终JSON索引保存到 `_对话检索汇编/[主题]_索引.json`
2. 进入脚本目录: `cd _对话检索汇编/scripts`
3. 运行生成命令: `python gen_reading_md.py -i ../[主题]_索引.json -o ../generated_docs`
4. 运行生成epub命令: `python generate_epub_cli.py -i ../[主题]_索引.json -o ../generated_docs`
5. 在 `generated_docs` 目录中查看生成的文档

### 自定义选项
- 使用 `-l` 参数选择特定布局类型
- 使用 `-t` 参数自定义主题名称

## 系统特点

- **多维度搜索**: 从文件名、内容、标签、语义等多个角度进行搜索
- **概念扩展**: 自动识别相关概念和跨学科联系
- **智能整合**: 建立概念层次关系，消除重复
- **多格式输出**: 支持Markdown、HTML、EPUB等多种格式
- **灵活配置**: 支持自定义主题、布局类型和内容包含选项

这个系统专为中文知识管理设计，能够高效处理大规模知识库，为用户提供深度、全面的主题研究和阅读材料。
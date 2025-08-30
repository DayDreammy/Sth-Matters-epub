# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive Chinese knowledge management repository containing organized learning notes and articles from a Chinese author. The repository includes a sophisticated document retrieval and generation system that performs deep search on specific topics and generates multi-format reading documents.

## Primary Task: Deep Search System

The core functionality of this repository is to perform deep search on any given topic within the knowledge base. The system follows a structured four-phase workflow:

### Phase 1: Initial Deep Search
**Objective**: Conduct comprehensive multi-angle search to create a foundational index

**Search Strategy**:
- **Multi-dimensional approach**: Search from various perspectives and aspects
- **File-level search**: Scan filenames and directory structures using the Chinese Library Classification system
- **Content-level search**: Full-text search within all Markdown files
- **Tag-based search**: Leverage the comprehensive tagging system
- **Semantic search**: Understand concepts beyond simple keyword matching

**Output**: JSON index containing:
- Original article content and metadata
- Zhihu links and source references
- Content categorization and tagging
- Word counts and relevance scoring
- Key concept extraction

### Phase 2: Concept Expansion
**Objective**: Deepen understanding and extend search scope based on initial results

**Process**:
- **Internal deepening**: Analyze key concepts from Phase 1 results
- **External expansion**: Identify related concepts and broader themes
- **Relationship mapping**: Establish connections between concepts
- **Contextual enrichment**: Find supporting and contrasting viewpoints

**Search Enhancement**:
- Extract key concepts from initial results
- Search for related terminology and broader themes
- Identify cross-disciplinary connections
- Find practical applications and theoretical frameworks

### Phase 3: Result Integration
**Objective**: Combine both search phases into a comprehensive index

**Integration Process**:
- Merge initial search results with expanded concepts
- Remove duplicates and resolve conflicts
- Establish hierarchical relationships between concepts
- Create unified categorization system
- Generate comprehensive metadata

**Final Index Structure**:
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

### Phase 4: Document Generation
**Objective**: Generate multiple format documents from the integrated index

**JSON Index File Storage**:
- Save the integrated JSON index from Phase 3 to: `_对话检索汇编/[主题]_索引.json`
- Example file path: `_对话检索汇编/社会化_索引.json`

**Document Generator Tool**: 
The system uses a flexible Python script (`gen_reading_md.py`) that processes JSON index files and generates various document formats.

**Script Location**: `_对话检索汇编/scripts/gen_reading_md.py`

**Command Line Interface**:
```bash
# 进入脚本目录
cd _对话检索汇编/scripts

# 生成文档
python gen_reading_md.py -i ../[主题]_索引.json -o ../generated_docs [OPTIONS]
```

**Available Options**:
- `-i/--index`: JSON索引文件路径 (必需)
- `-o/--output`: 输出目录路径 (必需)
- `-l/--layout`: 文档布局类型 (thematic/source_based/concepts/summary/html/all, 默认all)
- `-t/--topic`: 自定义主题名称
- `--no-source-content`: 不包含原始文件内容

**Usage Examples**:
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

**Output Directory Structure**:
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

**Output Formats**:
1. **EPUB Electronic Books**: Optimized for mobile reading, especially WeChat Reading
2. **Markdown Documents**: Multiple layouts (thematic, source-based, concepts, summary)
3. **HTML Documents**: Web-friendly format with interactive navigation
4. **Reading Compilations**: Organized by theme and relevance

**Layout Types**:
- **thematic**: 按主题分类的文档
- **source_based**: 按来源分组的文档
- **concepts**: 按关键概念组织的文档
- **summary**: 内容概要文档
- **html**: 交互式HTML文档

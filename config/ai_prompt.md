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
**Objective**: Generate multiple format documents from the integrated index.

**JSON Index File Storage**:
- Save the integrated JSON index from Phase 3 to: `output/[主题]_索引.json`
- Example file path: `output/社会化_索引.json`

**Document Generator Tools**: 
The system uses two Python scripts to process the JSON index file and generate various document formats.

**Script Locations**: 
- `src/document_generator/md_generator.py`
- `src/document_generator/epub_cli.py`

**Command Line Interface**:

1.  **Generate MD and HTML documents**:
    ```bash
    python src/document_generator/md_generator.py -i output/[主题]_索引.json -o output -k knowledge_base -l all
    ```

2.  **Generate EPUB document**:
    ```bash
    python src/document_generator/epub_cli.py -i output/[主题]_索引.json -o output -k knowledge_base
    ```

**Combined Command**: You should execute both commands sequentially to generate all required formats.
```bash
python src/document_generator/md_generator.py -i output/[主题]_索引.json -o output -k knowledge_base -l all && python src/document_generator/epub_cli.py -i output/[主题]_索引.json -o output -k knowledge_base
```

**Available Options for `md_generator.py`**:
- `-i/--index`: Path to the JSON index file (required).
- `-o/--output`: Output directory path (required).
- `-k/--kb-dir`: Path to the knowledge base root directory (required).
- `-l/--layout`: Document layout type (thematic/source_based/concepts/summary/html/all, default: all).
- `-t/--topic`: Custom topic name.

**Available Options for `epub_cli.py`**:
- `-i/--index`: Path to the JSON index file (required).
- `-o/--output`: Output directory path (required).
- `-k/--kb-dir`: Path to the knowledge base root directory (required).
- `-t/--title`: Custom book title.

**Final Output Directory Structure**:
```
/
├── output/
│   ├── [主题]_索引.json
│   ├── [主题]_thematic_文档.md
│   ├── [主题]_source_based_文档.md
│   ├── [主题]_concepts_文档.md
│   ├── [主题]_summary_文档.md
│   ├── [主题]_html_文档.html
│   └── [主题]_[timestamp].epub
├── src/
│   └── document_generator/
│       ├── md_generator.py
│       └── epub_cli.py
└── knowledge_base/
```

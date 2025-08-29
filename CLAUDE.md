# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a knowledge repository containing organized learning notes and articles from a Chinese author. The repository is structured as a personal knowledge management system using Markdown files, organized by topic using a modified Chinese Library Classification system.

## Repository Structure

The repository contains several main sections:

- **【文章目录】**: Main article directory organized by subject classification
  - Philosophy, Natural Sciences, Applied Sciences, Social Sciences, etc.
  - Each category contains subcategories with detailed topic organization
- **【本周更新】**: Weekly updated content
- **待归档**: Articles pending archival
- **摘抄本**: Quote collections and excerpts
- **沙海拾金**: Comment discussions and general discussions
- **_附件**: Supporting images and attachments

## Content Organization

The content follows a modified Chinese Library Classification (中图法) system:

1. **Philosophy** (哲学类): General philosophy, Chinese philosophy, Western philosophy, logic, metaphysics, psychology, aesthetics, ethics
2. **Natural Sciences** (自然科学): General science, mathematics, astronomy, physics, chemistry, biology, botany, zoology, anthropology
3. **Applied Sciences** (应用科学): General applied science, medicine, home economics, agriculture, engineering, chemical engineering, manufacturing, commerce
4. **Social Sciences** (社会科学): Statistics, education, customs, sociology, economics, finance, politics, law, military
5. **Chinese History & Geography** (中国史地): General history/geography, Chinese dynastic history, Chinese cultural history
6. **World History & Geography** (世界史地): World history and geography
7. **Language & Literature** (语言文学类): Language and literature works
8. **Arts** (艺术类): Arts and entertainment

## Tag System

The repository uses a comprehensive tagging system with hierarchical relationships:

- **Family** (家族): Personal legacy and foundational articles
- **Handling Affairs** (处事): Methods, practices, SOPs
- **Parent-Child** (亲子): Parent-child relationships and education
- **Internal & External** (内外): Internal construction, external management, values and taste
- **Safety** (安全): Identifying danger signals, personal safety
- **Psychology** (心理): Psychological issues and mental health
- **Business Management** (企管): Enterprise management
- **Career** (职业): Work attitude and life planning
- **Gender Relations** (两性): Love principles and practice
- **Social Sciences** (社科): Social phenomena and case analysis
- **Science** (科学): Scientific concepts and principles
- **Technology** (科技): Past, present, and future technology
- **Military** (军事): Military technology and art
- **Skills** (功夫): Core abilities, cooking, martial arts, survival skills
- **Entertainment** (文娱): Literature, film, entertainment
- **Arts & Culture** (文艺): Culture and arts
- **History** (历史): Historical perspectives and insights
- **Theology** (神学): Love and religious philosophy
- **Current Affairs** (时政): Current political commentary

## File Naming Conventions

- Articles use descriptive Chinese titles
- Files are organized in hierarchical directory structures
- Untitled articles are given descriptive titles in brackets
- Special collections use prefixes like "合集" (collection) or "专题" (special topic)

## Content Processing

When working with this repository:

1. **Article Format**: Articles follow a standard format with metadata including author, last update, links, categories, tags, and comment sections
2. **Content Classification**: Use the established classification system when organizing new content
3. **Tag Relationships**: Maintain the hierarchical tag system and relationships
4. **Cross-references**: Articles often reference each other, maintain these internal links

## Special Topics

The repository contains several special topic collections:
- **Covid-19**: Pandemic-related content
- **Russia-Ukraine War**: Geopolitical analysis
- **Artificial Intelligence**: AI-related discussions
- **Great Filter**: Philosophical discussions on existential risks

## Tools and Usage

- **Obsidian**: Primary tool for viewing and editing the knowledge base
- **Visual Studio Code**: Recommended for bulk text replacements
- **Markdown**: All content is in Markdown format for compatibility

## Query Processing Workflow

When you ask a question, I will help you find relevant or supporting texts from the files and provide you with a document:

### Search Process

1. **Analyze Query**: Understand your question and identify key concepts, topics, and keywords
2. **Search Strategy**: Use multiple search approaches:
   - Search file names and directory structures
   - Search within file contents using Grep tool
   - Use the classification system to narrow down relevant categories
   - Leverage the tag system to find related content
3. **Content Retrieval**: Extract relevant passages with original file paths
4. **Document Generation**: Create a comprehensive document with:
   - Relevant text excerpts
   - Original file paths for each excerpt
   - Context and organization of findings
   - Cross-references between related articles

### Search Strategy Principles

**Primary Focus**: The main task is to find original text materials that are comprehensive, in-depth, and interconnected. The emphasis is on:

1. **Comprehensiveness**: Find all relevant original materials across the repository
2. **Depth**: Locate in-depth discussions and analyses of the topic
3. **Original Text**: Present original passages without excessive organization or editing
4. **Supporting Materials**: Include related discussions, quotes, and contextual materials

**Approach**: Prioritize finding and presenting the original text content over creating structured summaries or analyses. The goal is to provide the raw materials for research and reading, allowing the user to draw their own insights and conclusions.

### Search Capabilities

- **Full-text search**: Search across all Markdown files in the repository
- **Category-based search**: Search within specific subject classifications
- **Tag-based search**: Find articles using the comprehensive tag system
- **Filename search**: Locate articles by title or filename
- **Content analysis**: Understand and match concepts beyond simple keyword matching

### Output Format

The resulting document will include:
- **Summary**: Brief overview of findings
- **Relevant Texts**: Direct quotes with original file paths
- **Context**: Background information for each relevant passage
- **Related Content**: Additional articles that may be of interest
- **Organization**: Structured presentation of findings by topic or category

## Enhanced Two-Step Search Process

A more efficient and flexible two-step process has been implemented for topic searches and content generation:

### Step 1: Search and Index Generation

1. **Comprehensive Search**: Conduct thorough search using multiple strategies to find all relevant original materials
2. **Index Creation**: Generate both a reading compilation document and a structured JSON index file containing:
   - Metadata for each source (title, file path, zhihu link if available)
   - Content excerpts with precise location information
   - Thematic categorization and tags
   - Relationship mapping between related concepts

### Step 2: Flexible Document Generation

1. **Python Script Integration**: Use a Python script to read the JSON index and generate customized reading documents
2. **Flexible Output**: The script can create documents with different organization schemes:
   - Thematic grouping
   - Chronological ordering
   - Source-based organization
   - Custom user-defined arrangements

### File Structure

```
_对话检索汇编/
├── 主题_原文汇编.md          # Complete original text compilation
├── 主题_索引.json             # Structured index data
├── generate_reading_doc.py   # Python script for document generation
└── custom_layouts/            # Custom layout templates (optional)
```

### Benefits

1. **Efficiency**: Search once, generate multiple document formats
2. **Flexibility**: Easy to reorganize content without re-searching
3. **Consistency**: Structured data ensures reliable processing
4. **Extensibility**: Can add new layouts and filters as needed
5. **Integration**: Enables programmatic content analysis and processing

### Previous Process (Legacy)

The original single-step process is maintained for backward compatibility:
- Direct generation of reading compilation files
- Manual organization and formatting
- Single output format per search

## Notes

- This is a knowledge management repository, not a traditional code project
- Content is primarily in Chinese with some English references
- The repository emphasizes knowledge organization and cross-referencing
- Articles are collected from various sources with proper attribution
- The system is designed for personal learning and knowledge construction
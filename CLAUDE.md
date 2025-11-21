# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Chinese intelligent search system that provides efficient document retrieval and content analysis capabilities. The system features a command-line interface and web API for searching through a comprehensive Chinese knowledge base, with support for multiple output formats including Markdown, HTML, and JSON.

**Note**: The repository contains two systems:
1. **Current Active System**: An intelligent search engine (`search.py`, `core/`, `api/`)
2. **Legacy Deep Search System**: Referenced in documentation but directories not currently present (`_对话检索汇编/`)

This CLAUDE.md focuses on the current active intelligent search system.

## Development Commands

### Running the System

**Basic Search Operations:**
```bash
# Basic search (default searches knowledge_base/9a directory)
python search.py "搜索关键词"

# Search specific directories
python search.py "关键词" -p "knowledge_base/Sth-Matters/【文章目录】" "knowledge_base/Sth-Matters/沙海拾金"

# Content-only search
python search.py "关键词" -t content

# Generate HTML format and save
python search.py "关键词" -f html -s

# Use predefined search profiles
python search.py --profile articles    # Search articles only
python search.py --profile highlights   # Search highlights and excerpts

# Display system statistics
python search.py --stats

# List current search paths
python search.py --list-paths

# Show available search profiles
python search.py --profiles
```

**Web API Operations:**
```bash
# Start Web API service
python search.py --web
# Service runs on http://localhost:5000

# Install dependencies for web API
pip install flask flask-cors
```

**System Management:**
```bash
# Rebuild search index
python search.py --rebuild

# View all available options
python search.py --help
```

### Installation and Setup

**Dependencies:**
```bash
# Core functionality (Python standard library only)
# No additional dependencies required

# For Web API functionality
pip install -r requirements.txt

# Development dependencies
pip install pytest black flake8
```

### Testing and Development

**Code Quality:**
```bash
# Format code
black *.py core/ api/

# Lint code
flake8 *.py core/ api/

# Run tests (when available)
pytest
```

## System Architecture

### Core Components

**Search Engine (`core/search_engine.py`)**:
- `IntelligentSearchEngine`: Main search engine class
- `SearchResult`: Data class for search results
- Multi-dimensional search: filename, content, tag, and combined search
- Configurable search paths and file type filtering
- Memory caching for performance optimization

**Document Generator (`core/document_generator.py`)**:
- `DocumentGenerator`: Converts search results to various formats
- Support for summary, detailed, thematic, HTML, and JSON outputs
- Template-based document generation
- File saving and organization capabilities

**API Layer**:
- `api/search_api.py`: `SearchAPI` class providing unified interface
- `api/web_api.py`: Flask-based REST API service
- Command-line interface through `search.py`

### Configuration System

**Main Configuration (`config/config.json`)**:
- Search engine settings (paths, file types, limits)
- Document generator preferences
- Web API configuration (host, port, CORS)
- Search profiles for different scopes
- Feature toggles and logging settings

**Search Profiles**:
- `default`: Standard knowledge base search
- `all`: Entire knowledge base search
- `articles`: Article directory only
- `highlights`: Highlights and excerpts

### Knowledge Base Structure

**Directory Organization**:
```
knowledge_base/
└── Sth-Matters/           # Main knowledge base
    ├── 【文章目录】/         # Primary articles
    ├── 沙海拾金/           # Curated highlights
    ├── 摘抄本/             # Excerpts and quotes
    ├── 待归档/             # Pending organization
    └── 其他资料...         # Additional materials
```

**File Support**: `.md`, `.txt`, `.json`, `.html`, `.htm`

### API Endpoints (Web API)

When running `python search.py --web`, the following endpoints are available:

| Method | Path | Description |
|--------|------|------------|
| POST | `/api/search` | Execute search |
| POST | `/api/generate` | Generate documents |
| GET | `/api/stats` | Get system statistics |
| POST | `/api/rebuild` | Rebuild index |
| GET | `/api/profiles` | List search profiles |
| POST | `/api/profile/<name>` | Use specific profile |
| GET/POST | `/api/paths` | Get/set search paths |
| GET | `/api/health` | Health check |
| GET | `/api/download/<filename>` | Download files |

### Search Types

**Available Search Types**:
- `filename`: File name matching
- `content`: Full-text content search
- `tag`: Tag search (supports #tag format)
- `all`: Combined search (default)

**Output Formats**:
- `summary`: Concise Markdown overview
- `detailed`: Comprehensive Markdown report
- `thematic`: Topic-organized Markdown
- `html`: Interactive HTML document
- `json`: Structured JSON data

### Key Implementation Details

**Search Algorithm**:
- Multi-dimensional matching with relevance scoring
- Support for fuzzy matching and exact matching
- Content preview extraction with highlighting
- Line number tracking for content matches

**Performance Features**:
- In-memory caching of search indices
- Configurable result limits (default: 50, max: 200)
- Incremental index updates
- File size and type filtering

**Extensibility**:
- Plugin-ready architecture for new search types
- Configurable output templates
- Custom search profiles
- Modular component design

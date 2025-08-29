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

## Web Interface System

A comprehensive web interface has been implemented to allow users to submit topic search requests through a user-friendly web form. The system uses Claude Code's headless mode to execute searches and sends results via email.

### System Architecture

```
_对话检索汇编/
├── frontend/                    # Web interface directory
│   ├── index.html              # Frontend interface
│   ├── app.py                  # Flask backend server
│   ├── config.json             # Configuration file
│   ├── requirements.txt        # Python dependencies
│   ├── start.sh                # Linux/Mac startup script
│   ├── start.bat               # Windows startup script
│   └── README.md               # Frontend documentation
├── generate_reading_doc.py    # Main document generator
├── generate_epub.py          # EPUB generator  
├── generated_docs/           # Output directory
└── README.md                 # System documentation
```

### Features

#### 🎯 Core Functionality
- **User-Friendly Interface**: Modern web form with responsive design
- **Multi-Format Support**: Choose from Markdown, HTML, EPUB, thematic, concepts, summary
- **Real-Time Progress**: Live status updates and progress tracking
- **Email Notifications**: Automatic delivery of results to user's inbox
- **Asynchronous Processing**: Background task queue for concurrent requests

#### 🛠️ Technical Implementation
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Flask with RESTful API
- **Task Management**: Thread-based queue system
- **Email Integration**: SMTP with attachment support
- **Error Handling**: Comprehensive logging and error recovery

### Web Interface Workflow

#### Step 1: User Submission
1. **Access Interface**: Navigate to `http://localhost:5000`
2. **Fill Form**: 
   - Enter search topic
   - Provide email address
   - Select output formats
   - Set priority level
   - Add optional notes
3. **Submit**: Click "开始搜索" to start the process

#### Step 2: Backend Processing
1. **Validation**: Server validates input and creates task
2. **Queue System**: Task added to processing queue
3. **Claude Code Execution**: System calls Claude Code in headless mode
4. **Document Generation**: Multiple formats generated simultaneously

#### Step 3: Result Delivery
1. **Email Preparation**: Results packaged with HTML email body
2. **Attachment Handling**: All generated files attached to email
3. **Notification**: Email sent to user with complete results
4. **Status Update**: Task status updated to completed

### API Endpoints

#### POST /api/search
Submit a new search request

**Request:**
```json
{
  "topic": "搜索主题",
  "email": "user@example.com", 
  "priority": "normal|high|urgent",
  "formats": "markdown,html,epub,thematic,concepts,summary",
  "notes": "备注信息"
}
```

#### GET /api/status/<task_id>
Check task status and progress

#### GET /api/health
System health check and statistics

### Configuration

#### Email Setup
Edit `frontend/config.json`:
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "your_email@gmail.com",
    "smtp_password": "your_app_password",
    "from_email": "your_email@gmail.com"
  }
}
```

#### Claude Code Path
Ensure Claude Code CLI is installed and accessible via command line.

### Starting the System

#### Method 1: Using Startup Scripts
- **Windows**: Double-click `frontend/start.bat`
- **Linux/Mac**: Run `./frontend/start.sh`

#### Method 2: Manual Start
```bash
cd frontend
pip install -r requirements.txt
python app.py
```

### Usage Example

1. **Start Server**: Run the startup script
2. **Open Browser**: Navigate to `http://localhost:5000`
3. **Submit Request**: 
   - Topic: "家庭教育"
   - Email: "your@email.com"
   - Formats: Select all options
   - Priority: "normal"
4. **Monitor Progress**: Watch real-time progress updates
5. **Receive Results**: Check email for completed documents

### Benefits Over Direct Command Line

1. **Accessibility**: No need to use command line interface
2. **User-Friendly**: Intuitive web form with clear options
3. **Notifications**: Automatic email delivery eliminates need to check for results
4. **Progress Tracking**: Real-time status updates
5. **Concurrent Processing**: Multiple users can submit requests simultaneously
6. **Error Handling**: Better error reporting and recovery

### When You Request a Topic Search Now

When you ask me to search for a topic, I have two options:

#### Option 1: Direct Processing (Previous Method)
I can still execute the search directly as before:
- Run `python generate_reading_doc.py` with your topic
- Run `python generate_epub.py` with your topic  
- Generate all format variations automatically
- Provide complete results with explanations

#### Option 2: Web Interface (New Method)
I can guide you to use the web interface:
- Start the web server using the startup script
- Access the interface at `http://localhost:5000`
- Submit your request through the web form
- Receive results via email notification

### Enhanced Two-Step Search Process

A comprehensive automated system has been implemented for topic searches and multi-format document generation:

### Step 1: Automated Search and Multi-Format Generation

When you request a topic search, I will:

1. **Execute Search Scripts**: Run the automated Python scripts to perform comprehensive searches
2. **Generate Multiple Formats**: Create various output formats simultaneously:
   - `主题_原文汇编.md`: Complete original text compilation
   - `主题_thematic_文档.md`: Thematic organization
   - `主题_concepts_文档.md`: Concept index
   - `主题_summary_文档.md`: Content summary
   - `主题_html_文档.html`: Web-friendly format
   - `主题_*.epub`: E-book format for e-readers

3. **Search Strategy**: The system uses multiple approaches:
   - File name and directory structure analysis
   - Full-content text search using Grep
   - Classification system navigation
   - Tag-based content discovery
   - Semantic matching and keyword analysis

### Step 2: Results Delivery and Options

1. **Provide Results**: Deliver all generated documents to you
2. **Format Options**: Explain the different available formats and their use cases
3. **Customization**: Offer to adjust formats or organization based on your preferences

### System Architecture

```
_对话检索汇编/
├── generate_reading_doc.py    # Main document generator
├── generate_epub.py          # EPUB generator  
├── generated_docs/           # Output directory
│   ├── 主题_原文汇编.md       # Complete compilation
│   ├── 主题_thematic_文档.md  # Thematic organization
│   ├── 主题_concepts_文档.md  # Concept index
│   ├── 主题_summary_文档.md   # Summary and statistics
│   ├── 主题_html_文档.html    # HTML version
│   └── 主题_*.epub           # EPUB e-book
└── README.md                 # System documentation
```

### Current Process (Active)

The current automated process:
- Executes `generate_reading_doc.py` for comprehensive search and document generation
- Executes `generate_epub.py` for e-book format generation
- Produces multiple output formats in a single run
- Maintains consistent formatting and metadata across all formats
- Supports WeChat Reading optimization for EPUB files

### Benefits

1. **Efficiency**: Complete search and multi-format generation in one operation
2. **Comprehensiveness**: All relevant materials captured and organized
3. **Flexibility**: Multiple output formats for different reading preferences
4. **Consistency**: Uniform formatting and metadata handling
5. **Accessibility**: Formats available for web, print, and e-reader consumption

### When You Request a Topic Search

When you ask me to search for a topic, I will:

1. **Execute the Automated System**: 
   - Run `python generate_reading_doc.py` with your topic
   - Run `python generate_epub.py` with your topic
   - Generate all format variations automatically

2. **Provide Complete Results**:
   - All generated markdown documents
   - HTML version for web browsing
   - EPUB files for e-readers
   - Summary of findings and statistics

3. **Offer Customization**:
   - Adjust formatting preferences
   - Modify organization schemes
   - Add or remove metadata displays
   - Generate additional formats as needed

### Usage Examples

**Your request**: "请帮我搜索关于'家庭教育'的内容"
**My response**: 
- Execute automated search for "家庭教育"
- Generate all document formats
- Provide complete results with explanations
- Offer customization options

**Your request**: "我想要一个关于'心理学'的EPUB文件"
**My response**:
- Execute search for "心理学"
- Generate EPUB and supporting documents
- Provide files and usage instructions

## Notes

- This is a knowledge management repository, not a traditional code project
- Content is primarily in Chinese with some English references
- The repository emphasizes knowledge organization and cross-referencing
- Articles are collected from various sources with proper attribution
- The system is designed for personal learning and knowledge construction
# 智能检索系统 (Intelligent Search Engine)

一个高效、简洁的文档检索和内容分析系统，专注于提供快速、准确的搜索功能和多格式文档生成。

## 🎯 项目特点

- **代码与内容分离**: 清晰的知识库目录结构，便于内容管理和版本控制
- **灵活搜索范围**: 通过配置文件支持多种搜索范围配置，满足不同需求
- **专注搜索**: 核心功能围绕高效检索设计，支持文件名、内容、标签多维度搜索
- **极简架构**: 代码结构清晰，依赖最小化，易于维护和扩展
- **多种输出**: 支持Markdown、HTML、JSON等多种格式的结果输出
- **API优先**: 提供命令行和Web API双重接口，便于集成和自动化

## 🚀 快速开始

### 安装依赖

```bash
# 基础功能无需额外依赖（使用Python标准库）
# 如需Web API功能，请安装：
pip install flask flask-cors
```

### 基本使用

```bash
# 基本搜索（默认搜索knowledge_base/Sth-Matters目录）
python search.py "搜索关键词"

# 指定搜索范围
python search.py "关键词" -p "Sth-Matters/【文章目录】" "Sth-Matters/沙海拾金"

# 内容搜索
python search.py "关键词" -t content

# 生成HTML格式并保存
python search.py "关键词" -f html -s

# 显示系统统计信息
python search.py --stats

# 使用预配置的搜索范围
python search.py --profile articles    # 仅搜索文章
python search.py --profile highlights   # 搜索精华内容

# 查看可用的搜索配置
python search.py --profiles

# 显示当前搜索路径
python search.py --list-paths

# 启动Web API服务
python search.py --web
```

## 📁 项目结构

```
intelligent-search-engine/
├── knowledge_base/          # 📚 知识库根目录
│   └── Sth-Matters/         # 默认检索内容存储
│       ├── 【文章目录】/      # 主要文章内容
│       ├── 沙海拾金/         # 精华内容摘录
│       ├── 摘抄本/           # 句子和段落摘抄
│       ├── 待归档/           # 待整理资料
│       └── 其他资料...       # 其他文档资料
├── core/                    # 🔧 核心引擎
│   ├── __init__.py
│   ├── search_engine.py     # 智能搜索引擎
│   └── document_generator.py # 文档生成器
├── api/                     # 🌐 API接口层
│   ├── __init__.py
│   ├── search_api.py        # 命令行API
│   └── web_api.py           # Web API服务
├── config/                  # ⚙️ 配置文件
│   └── config.json          # 系统配置和搜索范围设置
├── output/                  # 📄 输出目录
├── search.py                # 🚀 主入口脚本
├── requirements.txt         # 依赖列表
├── plan.md                  # 📋 项目计划
├── context.md               # 🧠 项目知识库
├── tasks.md                 # ✅ 任务跟踪
└── README.md                # 📖 项目说明
```

### 🗂 知识库组织

知识库采用**代码与内容分离**的设计原则：

- **`knowledge_base/`** - 所有待检索内容的根目录
- **搜索范围配置** - 通过配置文件灵活指定要搜索的目录和文件
- **多知识库支持** - 可配置多个搜索范围，支持不同类型的知识分离管理

## 🔍 搜索功能

### 搜索类型

- **filename**: 文件名匹配搜索
- **content**: 文件内容全文搜索
- **tag**: 标签搜索（支持#tag格式）
- **all**: 综合搜索（默认）

### 输出格式

- **summary**: 概要式Markdown文档
- **detailed**: 详细式Markdown文档
- **thematic**: 主题式Markdown文档
- **html**: 交互式HTML网页
- **json**: 结构化JSON数据

### 命令行选项

```bash
python search.py [关键词] [选项]

位置参数:
  query                 搜索关键词

搜索配置:
  -d, --knowledge-base-dir  知识库根目录路径 (默认: knowledge_base)
  -p, --search-paths         搜索路径列表（相对于知识库根目录）
  -c, --config              配置文件路径 (默认: config/config.json)
  --profile                 使用指定的搜索配置文件
  --profiles                显示可用的搜索配置文件
  --list-paths             显示当前搜索路径

搜索选项:
  -t, --type          搜索类型 (filename/content/tag/all)
  -n, --max-results   最大结果数 (默认: 50)
  -f, --format        输出格式 (summary/detailed/thematic/html/json)
  -s, --save          保存结果到文件

系统管理:
  -o, --output-dir    输出目录路径 (默认: output)
  --stats             显示系统统计信息
  --rebuild           重建搜索索引
  --web               启动Web API服务
  --quiet             静默模式
```

## 🌐 Web API

启动Web API服务：

```bash
python search.py --web
```

### API接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/search` | 执行搜索 |
| POST | `/api/generate` | 生成文档 |
| GET | `/api/stats` | 获取统计信息 |
| POST | `/api/rebuild` | 重建索引 |
| GET | `/api/profiles` | 获取搜索配置文件列表 |
| POST | `/api/profile/<name>` | 使用指定搜索配置 |
| GET/POST | `/api/paths` | 获取/设置搜索路径 |
| GET | `/api/health` | 健康检查 |
| GET | `/api/download/<filename>` | 下载文件 |

### API使用示例

```bash
# 搜索API
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索关键词", "type": "content"}'

# 生成文档API
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "关键词", "format": "html", "save_file": true}'
```

## ⚙️ 配置说明

系统配置文件位于 `config/config.json`，主要配置项：

- **search_engine**: 搜索引擎配置
  - `knowledge_base_directory`: 知识库根目录
  - `default_search_paths`: 默认搜索路径列表
  - `search_scope`: 搜索范围设置（排除模式、文件大小限制等）
- **search_profiles**: 预定义搜索配置
  - `default`: 默认搜索范围
  - `articles`: 仅搜索文章目录
  - `highlights`: 搜索精华内容和摘抄
  - `all`: 搜索整个知识库
- **document_generator**: 文档生成配置
- **web_api**: Web API配置
- **logging**: 日志配置
- **features**: 功能开关

### 搜索配置文件示例

```json
{
  "search_profiles": {
    "articles": {
      "name": "文章搜索",
      "paths": ["9a/【文章目录】"],
      "description": "仅搜索文章目录"
    },
    "highlights": {
      "name": "精华内容",
      "paths": ["9a/沙海拾金", "9a/摘抄本"],
      "description": "搜索精华内容和摘抄"
    }
  }
}
```

## 📊 系统特性

### 智能索引
- 自动构建文档索引
- 支持多种文件格式（.md, .txt, .json, .html）
- 提取标题、标签、分类等元信息
- 内存缓存提高搜索性能

### 搜索算法
- 多维度匹配算法
- 相关性评分机制
- 支持模糊匹配和精确匹配
- 按相关性排序结果

### 文档生成
- 多种布局模板
- 内容预览和高亮
- 支持大文档分页处理
- 自动文件命名和组织

## 🔧 开发指南

### 核心类说明

- **IntelligentSearchEngine**: 核心搜索引擎
- **DocumentGenerator**: 文档生成器
- **SearchAPI**: 命令行API接口
- **SearchResult**: 搜索结果数据类

### 扩展开发

```python
# 导入核心模块
from core import IntelligentSearchEngine, DocumentGenerator
from api import SearchAPI

# 创建搜索引擎实例
engine = IntelligentSearchEngine("9a")
results = engine.search("关键词", search_type="content")

# 生成文档
generator = DocumentGenerator("output")
content = generator.generate_html(results, "关键词")
```

## 📈 性能优化

- 使用内存缓存减少重复索引构建
- 支持增量索引更新
- 异步搜索处理（Web API）
- 结果分页和限制

## 🛠 故障排除

### 常见问题

1. **搜索结果为空**
   - 检查9a目录是否包含文件
   - 确认搜索关键词拼写
   - 尝试使用不同的搜索类型

2. **索引构建缓慢**
   - 检查文件数量和大小
   - 考虑移除不支持的文件格式
   - 使用`--rebuild`重建索引

3. **Web API无法启动**
   - 确认安装了flask和flask-cors
   - 检查端口5000是否被占用

### 日志查看

系统日志位置：`logs/search_engine.log`

## 🤝 贡献指南

本项目采用Context Engineering Protocol进行开发管理：

1. **plan.md** - 定义项目目标和开发阶段
2. **context.md** - 记录技术决策和架构设计
3. **tasks.md** - 跟踪具体任务和进度

### 开发流程

1. 阅读现有文档了解项目架构
2. 在tasks.md中创建新任务
3. 实现功能并更新相关文档
4. 提交代码并标记任务完成

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🙏 致谢

感谢所有为知识整理和分享做出贡献的朋友们。

---

*最后更新：2025-11-21 | 版本：1.0.0*
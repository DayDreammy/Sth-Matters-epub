# Project Context & Knowledge Base

## 🧠 Core Concepts (核心概念与对齐)
- **应用类型**: 一个基于大语言模型（LLM）的知识库深度分析与报告生成工具。
- **核心工作流**: 用户输入主题 -> `rpa.py` 调用LLM并引用知识库进行分析 -> LLM生成一个`索引.json`文件 -> `document_generator`中的脚本读取该JSON文件 -> 生成`.md`, `.html`, `.epub`三种格式的报告 -> 通过邮件发送给用户。
- **知识库**: 知识库内容是独立的，可替换的。当前任务要求将其替换为 `https://github.com/AaNingNing/Sth-Matters` 的内容。

## 🏗 Architecture Decisions (架构决策)
- **代码结构**: 采用 `src` 目录来存放所有核心Python代码，与配置、数据和输出分离。
- **模块化**: 将文档生成、RPA流程、邮件发送等功能拆分为独立的模块。
- **配置外部化**: 将邮件配置、AI Prompt等从代码中分离到 `config/` 目录。
- **依赖管理**: 使用 `requirements.txt` 明确管理Python第三方库。

## 💡 Lessons Learned (已验证的结论)
- [2025-11-23]: 仅分析 `gradio_interface.py` 是不够的。AI Agent执行的后台脚本 (`gen_reading_md.py`, `generate_epub_cli.py`) 是整个工作流的关键部分，必须一同迁移。
- [2025-11-23]: `generate_epub_cli.py` 依赖于同目录下的 `generate_epub.py`。
- [2025-11-23]: EPUB生成依赖 `ebooklib` 和 `beautifulsoup4` 两个外部库。

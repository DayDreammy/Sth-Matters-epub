# 知识库文档下载和预览功能使用说明

## 功能概述

知识库文档下载和预览功能为现有的深度搜索系统增加了便捷的文件管理和查看能力。用户可以在搜索完成后：

1. **在线预览HTML文档** - 直接在浏览器中查看生成的HTML文档
2. **批量下载文档** - 支持下载所有格式（Markdown、HTML、EPUB）
3. **文件管理** - 按主题分类查看、搜索和筛选文档
4. **统计信息** - 查看文件数量、大小、类型等统计数据

## 系统架构

### 文件结构
```
_对话检索汇编/frontend/
├── enhanced_app.py          # 增强版搜索服务（集成下载功能）
├── file_server.py           # 独立文件下载服务
├── start_services.py        # 服务启动脚本
└── static/
    ├── search.html          # 搜索页面
    ├── files.html           # 文件管理页面
    └── index.html           # 文件下载中心主页
```

### 服务端口
- **搜索服务**: http://localhost:5000
- **文件下载服务**: http://localhost:5001

## 启动方式

### 方式一：使用启动脚本（推荐）
```bash
cd _对话检索汇编/frontend
python3 start_services.py
```

选择启动模式：
- `1` - 启动完整服务（搜索 + 文件下载）
- `2` - 仅启动搜索服务
- `3` - 仅启动文件下载服务

### 方式二：手动启动
```bash
# 启动增强版搜索服务（包含文件下载功能）
cd _对话检索汇编/frontend
python3 enhanced_app.py

# 或启动独立的文件下载服务
python3 file_server.py
```

## 使用方法

### 1. 搜索和生成文档
1. 访问 http://localhost:5000
2. 输入搜索主题和邮箱地址
3. 选择输出格式（支持：markdown, html, epub）
4. 等待搜索完成

### 2. 查看和下载文档
1. 搜索完成后，点击"前往文件下载中心"
2. 或直接访问 http://localhost:5000/files
3. 在文件管理界面可以：
   - 查看所有生成的文档
   - 按主题分类浏览
   - 搜索特定文件
   - 预览HTML文档
   - 下载所需格式

### 3. API接口
系统提供完整的REST API：

#### 文件管理接口
- `GET /api/files` - 获取文件列表
- `GET /api/files/search?q=关键词` - 搜索文件
- `GET /api/files/topics` - 获取主题汇总
- `GET /api/files/download/<filename>` - 下载文件
- `GET /api/files/preview/<filename>` - 预览HTML文件
- `GET /api/stats` - 获取统计信息

#### 搜索接口
- `POST /api/search` - 发起搜索任务
- `GET /api/status/<task_id>` - 查看任务状态
- `GET /api/health` - 健康检查

## 功能特性

### 文件预览
- **支持格式**: HTML文档
- **预览方式**: 模态框内嵌预览，支持全屏查看
- **交互功能**: 保留原文档的所有链接和样式

### 文件下载
- **支持格式**: Markdown (.md), HTML (.html), EPUB (.epub), JSON (.json)
- **下载方式**: 单个文件下载或批量下载
- **文件信息**: 显示文件大小、修改时间、主题等信息

### 文件管理
- **主题分类**: 自动按主题对文件进行分组
- **搜索功能**: 支持按文件名和主题搜索
- **筛选功能**: 按文件类型（HTML、Markdown、EPUB）筛选
- **排序功能**: 按修改时间倒序显示

### 统计信息
- 总文件数量和大小
- 主题数量统计
- 各类型文件统计
- 最新文件信息

## 技术实现

### 后端技术栈
- **Flask**: Web框架
- **Flask-CORS**: 跨域支持
- **Python 3.8+**: 后端语言
- **Pathlib**: 文件路径处理

### 前端技术栈
- **原生JavaScript**: 无框架依赖
- **CSS3**: 响应式设计
- **HTML5**: 现代Web标准
- **Fetch API**: 异步通信

### 关键功能实现
1. **文件扫描**: 使用Python的Pathlib扫描文档目录
2. **文件类型识别**: 根据文件扩展名自动识别类型
3. **主题提取**: 从文件名中智能提取主题信息
4. **HTML预览**: 直接读取HTML文件内容并渲染
5. **文件下载**: 使用Flask的send_file实现安全的文件下载

## 配置说明

### 文件路径配置
在 `file_server.py` 中修改基础目录：
```python
class FileManager:
    def __init__(self, base_dir: str = "../generated_docs"):
        # 修改为实际的文档目录路径
```

### 邮件配置
在 `enhanced_app.py` 中配置邮件服务：
```python
"email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "your_email@gmail.com",
    "smtp_password": "your_password",
    "from_email": "your_email@gmail.com"
}
```

## 故障排除

### 常见问题

1. **文件无法加载**
   - 检查 `generated_docs` 目录路径是否正确
   - 确认文件权限设置正确

2. **中文文件名预览失败**
   - 由于URL编码问题，部分中文文件名可能无法直接预览
   - 建议使用文件管理界面的预览按钮

3. **服务启动失败**
   - 检查端口5000和5001是否被占用
   - 确认Python依赖已安装：`pip install flask flask-cors`

4. **邮件发送失败**
   - 检查邮箱配置是否正确
   - 确认邮箱开启SMTP服务

### 日志查看
- 搜索服务日志: `enhanced_search_server.log`
- 文件服务日志: 控制台输出

## 性能优化

### 大文件处理
- HTML文件可能较大（几十MB），预览时需要耐心加载
- 建议使用现代浏览器的最新版本

### 并发访问
- 文件下载服务支持多用户同时访问
- 搜索任务采用队列处理，避免资源冲突

## 更新日志

### v1.0.0 (2025-11-21)
- ✅ 实现完整的文件下载和预览功能
- ✅ 支持HTML文档在线预览
- ✅ 添加主题分类和搜索功能
- ✅ 提供REST API接口
- ✅ 响应式Web界面
- ✅ 服务启动脚本

## 联系支持

如遇到问题或需要功能增强，请：
1. 检查本文档的故障排除部分
2. 查看服务日志文件
3. 联系系统管理员

---

**注意**: 本功能为知识库搜索系统的扩展模块，需要配合主搜索系统使用。
# 知识库深度搜索系统

一个智能知识库搜索和文档管理系统，支持深度搜索、多格式文档生成、在线预览和文件下载功能。

## 功能特点

- 🔍 **深度搜索**：基于Claude CLI进行多角度知识库分析
- 📚 **文档生成**：自动生成EPUB、Markdown、HTML等多种格式
- 📧 **邮件发送**：将生成结果直接发送到指定邮箱
- 🌐 **现代化Web界面**：响应式设计，支持桌面和移动端
- 📄 **HTML在线预览**：直接在浏览器中预览生成的HTML文档
- 📁 **文件管理中心**：按主题分类、搜索、筛选和批量下载文档
- 📊 **统计信息**：查看文件数量、大小、类型等详细数据

## 文件说明

### 传统Gradio版本
- `gradio_interface.py` - 传统Gradio Web界面程序
- `deep_search_rpa.py` - RPA脚本，执行Claude CLI和文档生成
- `email_sender.py` - 邮件发送脚本
- `email_config.json` - 邮件配置文件

### 新版Flask系统（推荐）
- `_对话检索汇编/frontend/enhanced_app.py` - 增强版搜索服务（集成下载功能）
- `_对话检索汇编/frontend/file_server.py` - 独立文件下载服务
- `_对话检索汇编/frontend/start_services.py` - 服务启动脚本
- `_对话检索汇编/frontend/static/` - 前端界面文件
- `requirements.txt` - Python依赖包

## 安装和配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置邮件
编辑 `email_config.json` 文件：

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your_email@gmail.com",
  "sender_password": "your_app_password",
  "sender_name": "知识库搜索系统"
}
```

**重要提醒**：
- 对于Gmail，需要使用"应用专用密码"而不是普通密码
- 请在Google账户设置中启用两步验证并生成应用密码

### 3. 启动系统

#### 方式一：使用新版Flask系统（推荐）
```bash
cd _对话检索汇编/frontend
python3 start_services.py
```
选择启动模式：
- `1` - 启动完整服务（搜索 + 文件下载）
- `2` - 仅启动搜索服务
- `3` - 仅启动文件下载服务

#### 方式二：使用传统Gradio版本
```bash
python gradio_interface.py
```

### 4. 访问界面
- **新版搜索页面**: http://localhost:5000
- **文件下载中心**: http://localhost:5000/files 或 http://localhost:5001
- **传统Gradio界面**: http://localhost:7860

## 使用方法

### 新版系统使用流程

1. **执行搜索**：
   - 访问 http://localhost:5000
   - 输入搜索主题（如"社会化"、"认知偏差"等）
   - 输入您的邮箱地址
   - 选择输出格式（markdown, html, epub）
   - 点击"开始搜索"按钮

2. **查看结果**：
   - 搜索完成后点击"前往文件下载中心"
   - 在文件管理界面浏览所有生成的文档
   - 按主题分类查看文件
   - 使用搜索功能查找特定文档

3. **预览和下载**：
   - HTML文档支持在线预览
   - 点击下载按钮获取所需格式
   - 支持批量下载所有文件

### 传统版本使用流程

1. 打开Gradio Web界面 (http://localhost:7860)
2. 输入搜索主题和邮箱地址
3. 点击"开始搜索并发送"按钮
4. 等待处理完成，查收邮件即可

## 输出文档格式

系统会自动生成以下格式的文档：

- **HTML文档**：网页格式，支持交互式导航和在线预览
- **EPUB电子书**：适合微信读书等移动端阅读
- **Thematic文档**：按主题分类组织的Markdown文件
- **Source-based文档**：按来源分组的Markdown文件
- **Concepts文档**：按关键概念组织的Markdown文件
- **Summary文档**：内容概要的Markdown文件

## 新版系统特色功能

### 📄 HTML在线预览
- 直接在浏览器中查看生成的HTML文档
- 保留原文档的所有样式和交互功能
- 支持全屏预览和模态框显示

### 📁 智能文件管理
- **主题分类**：自动按搜索主题对文件进行分组
- **实时搜索**：支持按文件名和主题关键词搜索
- **类型筛选**：可按HTML、Markdown、EPUB等格式筛选
- **批量操作**：支持一键下载所有筛选文件

### 📊 统计信息面板
- 显示总文件数量和总大小
- 按文件类型统计分布
- 主题数量和文件分布情况
- 最新文件更新时间

### 🔌 REST API接口
系统提供完整的API接口，支持程序化访问：
```bash
# 获取文件列表
GET /api/files

# 搜索文件
GET /api/files/search?q=关键词

# 获取主题统计
GET /api/files/topics

# 下载文件
GET /api/files/download/<filename>

# 预览HTML文件
GET /api/files/preview/<filename>
```

## 注意事项

- 单次搜索大约需要5-15分钟
- 请确保网络连接稳定
- 大文件可能需要几分钟才能收到邮件
- 首次使用建议先测试邮件配置

## 注意事项

- 单次搜索大约需要5-15分钟
- 请确保网络连接稳定
- 大文件可能需要几分钟才能收到邮件
- 首次使用建议先测试邮件配置
- 新版系统需要Python 3.8+和Flask依赖

## 故障排除

### 新版系统问题

#### 服务启动失败
1. **端口被占用**：
   ```bash
   # 检查端口占用
   lsof -i :5000
   lsof -i :5001

   # 终止占用进程
   kill -9 <PID>
   ```

2. **依赖缺失**：
   ```bash
   pip install flask flask-cors
   ```

3. **文件无法加载**：
   - 检查 `generated_docs` 目录路径是否正确
   - 确认文件权限设置正确

#### HTML预览失败
1. **中文文件名问题**：由于URL编码，部分中文文件名可能无法直接预览
2. **文件过大**：大型HTML文件（>50MB）加载较慢，请耐心等待
3. **浏览器兼容性**：建议使用Chrome、Firefox等现代浏览器

#### 文件下载问题
1. **下载链接失效**：确认文件仍在 `generated_docs` 目录中
2. **权限问题**：检查文件和目录的读权限

### 传统版本问题

#### 邮件发送失败
1. 检查 `email_config.json` 配置是否正确
2. 确认邮箱密码或应用密码有效
3. 检查防火墙是否阻止SMTP连接

#### 搜索失败
1. 确认Claude CLI已正确安装
2. 检查是否有足够的磁盘空间
3. 确认网络连接正常

#### 文件生成问题
1. 检查 `_对话检索汇编/generated_docs` 目录权限
2. 确认Python脚本执行权限
3. 查看控制台错误信息

### 日志查看
- **新版系统日志**：`enhanced_search_server.log`
- **传统版本日志**：控制台输出和Gradio日志
- **邮件发送日志**：检查邮件服务器返回的错误信息

## 技术架构

### 新版Flask系统（推荐）
- **前端**：响应式Web界面（原生JavaScript + CSS3）
- **后端**：Flask Web框架 + 异步任务队列
- **文件管理**：专门的文件服务器和API接口
- **搜索引擎**：Claude CLI集成
- **邮件服务**：SMTP协议 + 多格式附件支持
- **文档处理**：多格式生成器（HTML、Markdown、EPUB）
- **缓存系统**：文件扫描和主题提取缓存

### 传统Gradio版本
- **前端**：Gradio Web界面
- **后端**：Python脚本集成
- **搜索引擎**：Claude CLI
- **邮件服务**：SMTP协议
- **文档处理**：多格式生成器

## 详细文档

- **下载功能详细说明**：查看 `_对话检索汇编/README_下载功能使用说明.md`
- **API接口文档**：参考系统内的API接口说明
- **配置指南**：查看相关配置文件的注释说明

---

## 更新日志

### v2.0.0 (2025-11-21) - 文件下载和预览功能
- ✨ 新增HTML文档在线预览功能
- ✨ 新增智能文件管理中心
- ✨ 新增主题分类和搜索功能
- ✨ 新增批量下载支持
- ✨ 新增统计信息面板
- ✨ 新增完整的REST API接口
- 🔧 系统架构升级为Flask + 异步任务队列
- 🎨 现代化响应式Web界面设计
- 📱 移动端适配支持

### v1.0.0 - 基础搜索系统
- 🔍 基于Claude CLI的深度搜索功能
- 📚 多格式文档生成（EPUB、Markdown、HTML）
- 📧 邮件发送功能
- 🌐 Gradio Web界面
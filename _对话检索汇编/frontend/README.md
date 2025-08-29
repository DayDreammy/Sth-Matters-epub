# 知识库主题搜索系统 - 前端界面

一个基于Web的界面，用于用户提交主题搜索请求，通过Claude Code无头模式执行搜索，并通过邮件发送结果。

## 系统架构

```
frontend/
├── index.html          # 前端界面
├── app.py             # Flask后端服务器
├── config.json        # 配置文件
├── requirements.txt   # Python依赖
└── README.md          # 本文档
```

## 功能特性

### 🎯 核心功能
- **智能搜索界面**: 用户友好的Web表单，支持主题搜索请求提交
- **多格式输出**: 支持Markdown、HTML、EPUB、主题分类、概念索引、内容概要等多种格式
- **实时进度**: 显示搜索进度和状态更新
- **邮件通知**: 完成后自动发送结果到用户邮箱
- **异步处理**: 后台任务队列，支持并发处理

### 🛠️ 技术特点
- **响应式设计**: 基于Bootstrap 5，适配各种设备
- **现代UI**: 渐变背景、卡片式布局、流畅动画
- **RESTful API**: 标准化的后端接口
- **错误处理**: 完善的错误处理和日志记录
- **配置管理**: 灵活的配置文件系统

## 快速开始

### 1. 环境准备

确保您的系统已安装：
- Python 3.8+
- Claude Code CLI工具
- Node.js (可选，用于开发)

### 2. 安装依赖

```bash
cd frontend
pip install -r requirements.txt
```

### 3. 配置设置

编辑 `config.json` 文件：

```json
{
  "claude_code_path": "claude",
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "your_email@gmail.com",
    "smtp_password": "your_app_password",
    "from_email": "your_email@gmail.com"
  }
}
```

**邮件配置说明：**
- **Gmail用户**: 需要使用应用专用密码，不是普通密码
- **其他邮箱**: 根据邮箱提供商设置相应的SMTP服务器和端口

### 4. 启动服务器

```bash
python app.py
```

服务器将在 `http://localhost:5000` 启动

### 5. 使用界面

打开浏览器访问 `http://localhost:5000`，填写搜索表单：
- 输入搜索主题
- 提供邮箱地址
- 选择输出格式
- 点击"开始搜索"

## API 接口

### POST /api/search
提交搜索请求

**请求体：**
```json
{
  "topic": "搜索主题",
  "email": "user@example.com",
  "priority": "normal|high|urgent",
  "formats": "markdown,html,epub",
  "notes": "备注信息"
}
```

**响应：**
```json
{
  "success": true,
  "task_id": "task_20240829_143000_1234",
  "message": "搜索任务已创建，正在处理中..."
}
```

### GET /api/status/<task_id>
获取任务状态

**响应：**
```json
{
  "success": true,
  "task_id": "task_20240829_143000_1234",
  "status": "pending|processing|completed|failed",
  "progress": 50,
  "message": "正在执行智能检索...",
  "created_at": "2024-08-29T14:30:00",
  "result": {...},
  "error": null
}
```

### GET /api/health
健康检查

**响应：**
```json
{
  "success": true,
  "status": "running",
  "timestamp": "2024-08-29T14:30:00",
  "queue_size": 2,
  "completed_tasks": 15
}
```

## 工作流程

### 1. 用户提交请求
- 填写搜索表单
- 选择输出格式
- 提交到后端

### 2. 后端处理
- 验证输入数据
- 创建任务并加入队列
- 返回任务ID

### 3. 任务执行
- 工作线程从队列获取任务
- 调用Claude Code无头模式
- 执行搜索和文档生成

### 4. 结果处理
- 收集生成的文件
- 准备邮件内容
- 发送邮件通知

### 5. 状态更新
- 实时更新任务状态
- 记录处理日志
- 清理临时文件

## 配置选项

### config.json 详细配置

```json
{
  "claude_code_path": "claude",                    // Claude Code CLI路径
  "email": {                                      // 邮件配置
    "smtp_server": "smtp.gmail.com",             // SMTP服务器
    "smtp_port": 587,                            // SMTP端口
    "smtp_username": "your_email@gmail.com",     // 邮箱用户名
    "smtp_password": "your_app_password",        // 邮箱密码/应用密码
    "from_email": "your_email@gmail.com"         // 发件人邮箱
  },
  "output_dir": "generated_docs",                 // 输出目录
  "max_file_size": 52428800,                      // 最大文件大小(字节)
  "server": {                                     // 服务器配置
    "host": "0.0.0.0",                           // 监听地址
    "port": 5000,                                // 监听端口
    "debug": false                               // 调试模式
  },
  "search": {                                     // 搜索配置
    "timeout": 1800,                             // 超时时间(秒)
    "max_concurrent_tasks": 5,                   // 最大并发任务数
    "retry_attempts": 3                          // 重试次数
  },
  "formats": {                                    // 格式配置
    "default": ["markdown", "html", "epub", "thematic", "concepts", "summary"],
    "available": ["markdown", "html", "epub", "thematic", "concepts", "summary"]
  }
}
```

## 部署选项

### 开发环境
```bash
python app.py
```

### 生产环境
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 故障排除

### 常见问题

1. **Claude Code未找到**
   - 确保Claude Code CLI已正确安装
   - 检查`claude_code_path`配置是否正确

2. **邮件发送失败**
   - 检查SMTP配置是否正确
   - Gmail用户需要使用应用专用密码
   - 确认邮箱服务器的安全设置

3. **任务超时**
   - 检查网络连接
   - 增加超时时间配置
   - 确认Claude Code服务正常

4. **权限问题**
   - 确保有写入输出目录的权限
   - 检查Claude Code的访问权限

### 日志查看
```bash
tail -f search_server.log
```

## 扩展功能

### 数据库集成
可以添加数据库支持来持久化任务记录和搜索历史。

### 用户认证
添加用户登录和权限管理功能。

### 文件管理
实现文件的上传、下载和管理功能。

### 批量处理
支持批量主题搜索和定时任务。

## 安全考虑

1. **输入验证**: 所有用户输入都经过验证和清理
2. **文件安全**: 限制文件上传大小和类型
3. **API保护**: 可以添加API密钥认证
4. **日志记录**: 记录所有操作和错误

## 性能优化

1. **异步处理**: 使用异步任务队列提高并发性能
2. **缓存机制**: 缓存常用搜索结果
3. **负载均衡**: 支持多实例部署
4. **资源管理**: 合理管理内存和CPU资源

## 许可证

本项目采用MIT许可证。

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- Email: [your-email@example.com]
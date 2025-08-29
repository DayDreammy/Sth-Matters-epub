# 知识库搜索系统 - 完整版

这是一个完整的**前后端分离**的知识库搜索系统，包含真正的后台服务和Claude Code集成。

## 🏗️ 系统架构

```
web-interface/
├── backend/                 # 后端服务器
│   ├── server.js           # Express服务器主文件
│   ├── claude-code-api.js  # Claude Code API集成
│   ├── package.json        # Node.js依赖配置
│   └── .env.example        # 环境变量示例
├── index-full.html         # 完整版前端页面
├── script-api.js          # API版本JavaScript
├── styles.css             # 样式文件
├── start-server.bat       # Windows启动脚本
└── README.md              # 使用说明
```

## 🚀 功能特点

### 后端功能
- ✅ **Express.js服务器** - 提供RESTful API
- ✅ **文件索引系统** - 自动扫描和索引.md文件
- ✅ **实时文件监控** - 监控文件变化并自动更新索引
- ✅ **Claude Code集成** - 调用Claude Code进行智能搜索
- ✅ **搜索日志记录** - 记录所有搜索操作
- ✅ **文件分类和标签** - 自动提取分类和标签信息
- ✅ **RESTful API** - 提供完整的API接口

### 前端功能
- ✅ **实时搜索** - 支持自动和手动搜索
- ✅ **结果高亮** - 搜索关键词高亮显示
- ✅ **文件查看** - 点击查看完整文件内容
- ✅ **统计信息** - 显示文件总数、分类数等
- ✅ **API状态监控** - 实时显示后端连接状态
- ✅ **响应式设计** - 完美适配手机、平板、桌面
- ✅ **对话日志** - 记录所有操作历史

## 📋 系统要求

- **Node.js** >= 14.0.0
- **npm** >= 6.0.0
- **Claude Code** (可选，用于高级搜索功能)
- **现代浏览器** (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)

## 🛠️ 安装和运行

### 1. 快速启动 (Windows)

```bash
# 双击启动脚本
start-server.bat
```

### 2. 手动启动

```bash
# 进入项目目录
cd D:\yy\Sth-Matters\web-interface

# 进入后端目录
cd backend

# 安装依赖
npm install

# 启动服务器
node server.js
```

### 3. 访问系统

打开浏览器访问：`http://localhost:3000`

## 🔧 配置说明

### 环境变量配置

复制 `backend/.env.example` 为 `backend/.env`：

```env
# 服务器配置
PORT=3000
NODE_ENV=development

# 知识库根目录
KNOWLEDGE_BASE_PATH=../../../

# Claude Code配置
CLAUDE_CODE_PATH=claude-code
CLAUDE_CODE_TIMEOUT=30000

# 搜索配置
MAX_SEARCH_RESULTS=50
DEFAULT_CONTEXT_LINES=2
ENABLE_FILE_WATCHING=true
```

### Claude Code配置

如果需要使用Claude Code的高级搜索功能，确保：

1. Claude Code已安装并在PATH中
2. 在环境变量中配置正确的路径
3. 确保Claude Code可以访问你的知识库目录

## 📡 API接口

### 搜索接口
```http
POST /api/search
Content-Type: application/json

{
    "query": "搜索关键词",
    "options": {
        "limit": 20,
        "offset": 0,
        "category": "分类名称",
        "tags": ["标签1", "标签2"],
        "sortBy": "relevance"
    }
}
```

### 获取文件详情
```http
GET /api/files/:path
```

### 获取分类列表
```http
GET /api/categories
```

### 获取标签列表
```http
GET /api/tags
```

### 获取统计信息
```http
GET /api/stats
```

### 重新索引
```http
POST /api/reindex
```

### 获取搜索日志
```http
GET /api/logs?limit=50
```

## 🔍 搜索功能

### 支持的搜索类型
- **标题搜索** - 在文件标题中搜索
- **内容搜索** - 在文件内容中搜索
- **标签搜索** - 在文件标签中搜索
- **路径搜索** - 在文件路径中搜索

### 搜索选项
- **分类过滤** - 按文件分类筛选
- **标签过滤** - 按标签筛选
- **排序方式** - 按相关性、日期、大小排序
- **分页** - 支持分页显示结果

### 相关性评分
- 标题匹配: 10分
- 标签匹配: 8分
- 内容匹配: 5分
- 路径匹配: 3分

## 📱 前端界面

### 主要组件
1. **搜索区域** - 输入框和搜索按钮
2. **统计信息** - 显示文件总数、分类数等
3. **搜索结果** - 显示搜索结果列表
4. **对话日志** - 记录所有操作历史
5. **文件查看器** - 模态框显示完整文件内容

### 快捷键
- `Ctrl/Cmd + K` - 聚焦搜索框
- `Ctrl/Cmd + L` - 清空日志
- `Ctrl/Cmd + Enter` - 执行搜索

## 🛡️ 安全特性

- **CORS保护** - 配置跨域访问
- **输入验证** - 验证搜索查询
- **路径安全** - 防止路径遍历攻击
- **错误处理** - 完善的错误处理机制

## 📊 监控和日志

### 系统监控
- API连接状态
- 文件索引状态
- 搜索性能统计

### 日志记录
- 搜索历史记录
- 系统错误日志
- 文件变更记录

## 🔧 故障排除

### 常见问题

1. **后端启动失败**
   - 检查Node.js是否正确安装
   - 确保端口3000未被占用
   - 检查依赖包是否正确安装

2. **前端无法连接后端**
   - 确认后端服务器正在运行
   - 检查防火墙设置
   - 确认API地址配置正确

3. **搜索结果为空**
   - 检查知识库路径配置
   - 确认.md文件存在
   - 尝试重新索引

4. **Claude Code功能不可用**
   - 确认Claude Code已安装
   - 检查环境变量配置
   - 确认Claude Code可以访问知识库

### 调试模式

启用调试模式：
```bash
cd backend
DEBUG=knowledge-base-search:* node server.js
```

## 🚀 部署选项

### 开发环境
```bash
npm run dev
```

### 生产环境
```bash
npm start
```

### 使用PM2部署
```bash
npm install -g pm2
pm2 start server.js --name knowledge-base-search
pm2 save
pm2 startup
```

## 📈 性能优化

### 后端优化
- 文件索引缓存
- 搜索结果缓存
- 分页加载
- 异步文件处理

### 前端优化
- 懒加载
- 防抖搜索
- 结果缓存
- 图片懒加载

## 🔮 未来规划

- [ ] 用户认证系统
- [ ] 高级搜索过滤器
- [ ] 搜索结果导出
- [ ] 多语言支持
- [ ] 深色主题
- [ ] 移动端APP
- [ ] 云端部署
- [ ] AI智能推荐
- [ ] 搜索历史分析

## 📄 许可证

本项目基于MIT许可证开源。

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📞 支持

如果遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查浏览器控制台错误信息
3. 查看后端服务器日志
4. 提交Issue描述问题

---

**注意**: 这是一个完整的搜索系统，需要Node.js环境支持。如果你只需要一个简单的静态演示，请使用`index.html`文件。
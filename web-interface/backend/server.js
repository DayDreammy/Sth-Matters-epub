const express = require('express');
const cors = require('cors');
const fs = require('fs-extra');
const path = require('path');
const chokidar = require('chokidar');
const natural = require('natural');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../')));

// 知识库根目录
const KNOWLEDGE_BASE_ROOT = path.join(__dirname, '../../../');

// 缓存知识库内容
let knowledgeCache = new Map();
let fileIndex = [];

// 初始化知识库索引
async function initializeKnowledgeBase() {
    console.log('正在初始化知识库索引...');
    
    // 扫描.md文件
    const scanDir = async (dir) => {
        const files = await fs.readdir(dir);
        
        for (const file of files) {
            const filePath = path.join(dir, file);
            const stat = await fs.stat(filePath);
            
            if (stat.isDirectory()) {
                await scanDir(filePath);
            } else if (file.endsWith('.md')) {
                await indexFile(filePath);
            }
        }
    };
    
    await scanDir(KNOWLEDGE_BASE_ROOT);
    console.log(`知识库索引完成，共索引 ${fileIndex.length} 个文件`);
}

// 索引单个文件
async function indexFile(filePath) {
    try {
        const content = await fs.readFile(filePath, 'utf8');
        const relativePath = path.relative(KNOWLEDGE_BASE_ROOT, filePath);
        
        // 提取文件信息
        const fileInfo = {
            path: relativePath,
            title: extractTitle(content, path.basename(filePath)),
            content: content,
            tags: extractTags(content),
            category: extractCategory(relativePath),
            size: content.length,
            lastModified: (await fs.stat(filePath)).mtime
        };
        
        // 添加到索引
        fileIndex.push(fileInfo);
        knowledgeCache.set(relativePath, fileInfo);
        
        console.log(`已索引: ${relativePath}`);
    } catch (error) {
        console.error(`索引文件失败: ${filePath}`, error.message);
    }
}

// 提取标题
function extractTitle(content, fileName) {
    // 尝试从第一个 # 标题提取
    const titleMatch = content.match(/^#\s+(.+)$/m);
    if (titleMatch) {
        return titleMatch[1].trim();
    }
    
    // 否则使用文件名（去掉.md）
    return fileName.replace(/\.md$/, '');
}

// 提取标签
function extractTags(content) {
    const tags = [];
    
    // 从 Tag 字段提取
    const tagMatch = content.match(/^Tag:\s*(.+)$/m);
    if (tagMatch) {
        const tagString = tagMatch[1];
        // 处理类似 #4-职业发展/5-创业 的标签
        const tagMatches = tagString.match(/#[^#\s]+/g);
        if (tagMatches) {
            tags.push(...tagMatches.map(tag => tag.substring(1)));
        }
    }
    
    // 从 Category 字段提取
    const categoryMatch = content.match(/^Category:\s*(.+)$/m);
    if (categoryMatch) {
        tags.push(categoryMatch[1].trim());
    }
    
    return tags;
}

// 提取分类
function extractCategory(filePath) {
    const parts = filePath.split(path.sep);
    if (parts.length >= 2) {
        return parts[0]; // 第一级目录作为分类
    }
    return '未分类';
}

// 搜索功能
function searchKnowledgeBase(query, options = {}) {
    const {
        limit = 10,
        offset = 0,
        category = null,
        tags = [],
        sortBy = 'relevance'
    } = options;
    
    const results = [];
    const queryLower = query.toLowerCase();
    
    // 对每个文件进行搜索
    fileIndex.forEach(file => {
        let score = 0;
        let matches = [];
        
        // 分类过滤
        if (category && file.category !== category) {
            return;
        }
        
        // 标签过滤
        if (tags.length > 0) {
            const hasMatchingTag = tags.some(tag => 
                file.tags.some(fileTag => 
                    fileTag.toLowerCase().includes(tag.toLowerCase())
                )
            );
            if (!hasMatchingTag) return;
        }
        
        // 标题匹配 (权重: 10)
        if (file.title.toLowerCase().includes(queryLower)) {
            score += 10;
            matches.push({ type: 'title', text: file.title });
        }
        
        // 标签匹配 (权重: 8)
        file.tags.forEach(tag => {
            if (tag.toLowerCase().includes(queryLower)) {
                score += 8;
                matches.push({ type: 'tag', text: tag });
            }
        });
        
        // 内容匹配 (权重: 5)
        if (file.content.toLowerCase().includes(queryLower)) {
            score += 5;
            // 提取相关内容片段
            const contentMatches = extractContentMatches(file.content, query);
            matches.push(...contentMatches);
        }
        
        // 路径匹配 (权重: 3)
        if (file.path.toLowerCase().includes(queryLower)) {
            score += 3;
            matches.push({ type: 'path', text: file.path });
        }
        
        if (score > 0) {
            results.push({
                ...file,
                score,
                matches,
                relevantContent: extractRelevantContent(file.content, query)
            });
        }
    });
    
    // 排序
    results.sort((a, b) => {
        switch (sortBy) {
            case 'relevance':
                return b.score - a.score;
            case 'date':
                return new Date(b.lastModified) - new Date(a.lastModified);
            case 'size':
                return b.size - a.size;
            default:
                return b.score - a.score;
        }
    });
    
    // 分页
    const paginatedResults = results.slice(offset, offset + limit);
    
    return {
        results: paginatedResults,
        total: results.length,
        query,
        options
    };
}

// 提取内容匹配
function extractContentMatches(content, query) {
    const matches = [];
    const queryLower = query.toLowerCase();
    const lines = content.split('\n');
    
    lines.forEach((line, index) => {
        if (line.toLowerCase().includes(queryLower)) {
            matches.push({
                type: 'content',
                text: line.trim(),
                line: index + 1
            });
        }
    });
    
    return matches.slice(0, 3); // 最多返回3个匹配
}

// 提取相关内容
function extractRelevantContent(content, query, maxLength = 300) {
    const queryLower = query.toLowerCase();
    const index = content.toLowerCase().indexOf(queryLower);
    
    if (index === -1) return content.substring(0, maxLength) + '...';
    
    const start = Math.max(0, index - 100);
    const end = Math.min(content.length, index + query.length + 100);
    let extracted = content.substring(start, end);
    
    if (start > 0) extracted = '...' + extracted;
    if (end < content.length) extracted = extracted + '...';
    
    return extracted;
}

// API路由

// 搜索接口
app.post('/api/search', (req, res) => {
    try {
        const { query, options = {} } = req.body;
        
        if (!query || query.trim() === '') {
            return res.status(400).json({
                error: '搜索查询不能为空'
            });
        }
        
        const results = searchKnowledgeBase(query, options);
        
        // 记录搜索日志
        logSearch(query, results);
        
        res.json(results);
    } catch (error) {
        console.error('搜索错误:', error);
        res.status(500).json({
            error: '搜索失败',
            message: error.message
        });
    }
});

// 获取文件详情
app.get('/api/files/:path', (req, res) => {
    try {
        const filePath = decodeURIComponent(req.params.path);
        const fullPath = path.join(KNOWLEDGE_BASE_ROOT, filePath);
        
        if (!knowledgeCache.has(filePath)) {
            return res.status(404).json({
                error: '文件不存在'
            });
        }
        
        const fileInfo = knowledgeCache.get(filePath);
        res.json(fileInfo);
    } catch (error) {
        console.error('获取文件详情错误:', error);
        res.status(500).json({
            error: '获取文件详情失败',
            message: error.message
        });
    }
});

// 获取分类列表
app.get('/api/categories', (req, res) => {
    try {
        const categories = [...new Set(fileIndex.map(file => file.category))];
        res.json(categories);
    } catch (error) {
        console.error('获取分类列表错误:', error);
        res.status(500).json({
            error: '获取分类列表失败',
            message: error.message
        });
    }
});

// 获取标签列表
app.get('/api/tags', (req, res) => {
    try {
        const allTags = fileIndex.flatMap(file => file.tags);
        const uniqueTags = [...new Set(allTags)];
        res.json(uniqueTags);
    } catch (error) {
        console.error('获取标签列表错误:', error);
        res.status(500).json({
            error: '获取标签列表失败',
            message: error.message
        });
    }
});

// 获取统计信息
app.get('/api/stats', (req, res) => {
    try {
        const stats = {
            totalFiles: fileIndex.length,
            totalSize: fileIndex.reduce((sum, file) => sum + file.size, 0),
            categories: [...new Set(fileIndex.map(file => file.category))].length,
            tags: [...new Set(fileIndex.flatMap(file => file.tags))].length,
            lastUpdated: new Date().toISOString()
        };
        
        res.json(stats);
    } catch (error) {
        console.error('获取统计信息错误:', error);
        res.status(500).json({
            error: '获取统计信息失败',
            message: error.message
        });
    }
});

// 重新索引
app.post('/api/reindex', async (req, res) => {
    try {
        console.log('开始重新索引...');
        fileIndex = [];
        knowledgeCache.clear();
        
        await initializeKnowledgeBase();
        
        res.json({
            message: '重新索引完成',
            filesIndexed: fileIndex.length
        });
    } catch (error) {
        console.error('重新索引错误:', error);
        res.status(500).json({
            error: '重新索引失败',
            message: error.message
        });
    }
});

// 搜索日志
const searchLogs = [];

function logSearch(query, results) {
    const log = {
        query,
        timestamp: new Date().toISOString(),
        resultsCount: results.total,
        userIp: req.ip || 'unknown'
    };
    
    searchLogs.push(log);
    
    // 保持最近1000条记录
    if (searchLogs.length > 1000) {
        searchLogs.shift();
    }
    
    console.log(`搜索记录: "${query}" - ${results.total} 个结果`);
}

// 获取搜索日志
app.get('/api/logs', (req, res) => {
    try {
        const limit = parseInt(req.query.limit) || 50;
        const logs = searchLogs.slice(-limit);
        
        res.json({
            logs,
            total: searchLogs.length
        });
    } catch (error) {
        console.error('获取搜索日志错误:', error);
        res.status(500).json({
            error: '获取搜索日志失败',
            message: error.message
        });
    }
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error('服务器错误:', err);
    res.status(500).json({
        error: '服务器内部错误',
        message: err.message
    });
});

// 404处理
app.use((req, res) => {
    res.status(404).json({
        error: '接口不存在',
        path: req.path
    });
});

// 启动服务器
app.listen(PORT, async () => {
    console.log(`知识库搜索服务器启动在端口 ${PORT}`);
    console.log(`访问地址: http://localhost:${PORT}`);
    
    // 初始化知识库
    await initializeKnowledgeBase();
    
    // 监控文件变化
    const watcher = chokidar.watch(path.join(KNOWLEDGE_BASE_ROOT, '**/*.md'), {
        ignored: /node_modules/,
        persistent: true
    });
    
    watcher
        .on('add', async (filePath) => {
            console.log(`文件新增: ${filePath}`);
            await indexFile(filePath);
        })
        .on('change', async (filePath) => {
            console.log(`文件修改: ${filePath}`);
            await indexFile(filePath);
        })
        .on('unlink', (filePath) => {
            console.log(`文件删除: ${filePath}`);
            const relativePath = path.relative(KNOWLEDGE_BASE_ROOT, filePath);
            fileIndex = fileIndex.filter(file => file.path !== relativePath);
            knowledgeCache.delete(relativePath);
        });
    
    console.log('文件监控已启动');
});

// 优雅关闭
process.on('SIGTERM', () => {
    console.log('正在关闭服务器...');
    watcher.close();
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('正在关闭服务器...');
    watcher.close();
    process.exit(0);
});
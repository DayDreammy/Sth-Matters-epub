// 知识库搜索系统 - 与后端API通信版本

class KnowledgeBaseSearch {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.searchResults = document.getElementById('searchResults');
        this.resultCount = document.getElementById('resultCount');
        this.conversationLog = document.getElementById('conversationLog');
        this.autoSearch = document.getElementById('autoSearch');
        this.showLog = document.getElementById('showLog');
        this.clearLogBtn = document.getElementById('clearLog');
        this.logSection = document.getElementById('logSection');
        
        this.searchTimeout = null;
        this.isSearching = false;
        this.apiBaseUrl = 'http://localhost:3000/api';
        
        this.init();
    }
    
    init() {
        console.log('初始化知识库搜索系统...');
        
        // 检查DOM元素
        console.log('搜索输入框:', this.searchInput);
        console.log('搜索按钮:', this.searchBtn);
        console.log('搜索结果区域:', this.searchResults);
        
        // 绑定事件监听器
        this.searchBtn.addEventListener('click', () => {
            console.log('搜索按钮被点击');
            this.performSearch();
        });
        
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                console.log('回车键被按下');
                this.performSearch();
            }
        });
        
        // 自动搜索功能
        this.searchInput.addEventListener('input', () => {
            if (this.autoSearch.checked) {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => {
                    this.performSearch();
                }, 500);
            }
        });
        
        // 显示/隐藏日志
        this.showLog.addEventListener('change', () => {
            this.logSection.classList.toggle('hidden', !this.showLog.checked);
        });
        
        // 清空日志
        this.clearLogBtn.addEventListener('click', () => {
            this.clearLog();
        });
        
        // 初始化日志
        this.addLogEntry('系统初始化完成', 'system');
        
        // 测试API连接
        this.testApiConnection();
        
        console.log('知识库搜索系统初始化完成');
    }
    
    async testApiConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/stats`);
            if (response.ok) {
                const stats = await response.json();
                this.addLogEntry(`API连接成功 - 索引了 ${stats.totalFiles} 个文件`, 'system');
            } else {
                this.addLogEntry('API连接失败 - 服务器返回错误', 'error');
            }
        } catch (error) {
            this.addLogEntry(`API连接失败 - ${error.message}`, 'error');
            console.error('API连接测试失败:', error);
        }
    }
    
    async performSearch() {
        console.log('执行搜索功能...');
        const query = this.searchInput.value.trim();
        console.log('搜索查询:', query);
        
        if (!query) {
            console.log('搜索查询为空，显示空状态');
            this.showEmptyState();
            return;
        }
        
        // 记录用户搜索
        this.addLogEntry(`搜索: ${query}`, 'user');
        
        // 显示搜索状态
        this.setSearchingState(true);
        
        try {
            // 调用后端API
            const response = await fetch(`${this.apiBaseUrl}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    options: {
                        limit: 20,
                        offset: 0,
                        sortBy: 'relevance'
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const results = await response.json();
            console.log('搜索结果:', results);
            
            this.displayResults(results);
            this.setSearchingState(false);
            
            // 记录搜索结果
            this.addLogEntry(`找到 ${results.total} 个相关结果`, 'assistant');
            
        } catch (error) {
            console.error('搜索失败:', error);
            this.setSearchingState(false);
            this.addLogEntry(`搜索失败: ${error.message}`, 'error');
            this.showErrorMessage(`搜索失败: ${error.message}`);
        }
    }
    
    displayResults(results) {
        this.searchResults.innerHTML = '';
        this.resultCount.textContent = `共找到 ${results.total} 个结果`;
        
        if (results.results.length === 0) {
            this.showEmptyState();
            return;
        }
        
        results.results.forEach((result, index) => {
            const resultElement = this.createResultElement(result, results.query);
            this.searchResults.appendChild(resultElement);
        });
    }
    
    createResultElement(result, query) {
        const div = document.createElement('div');
        div.className = 'result-item';
        
        // 高亮查询词
        const highlightedTitle = this.highlightText(result.title, query);
        const highlightedContent = this.highlightText(result.relevantContent, query);
        
        div.innerHTML = `
            <h3 class="result-title">${highlightedTitle}</h3>
            <div class="result-source">${result.path}</div>
            <div class="result-meta">
                <span class="result-category">分类: ${result.category}</span>
                <span class="result-score">相关性: ${result.score}</span>
            </div>
            <div class="result-content">
                <p>${highlightedContent}</p>
            </div>
            <div class="result-tags">
                ${result.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <div class="result-actions">
                <button class="view-file-btn" data-path="${result.path}">查看完整文件</button>
            </div>
        `;
        
        // 添加查看文件按钮事件
        const viewBtn = div.querySelector('.view-file-btn');
        viewBtn.addEventListener('click', () => {
            this.viewFile(result.path);
        });
        
        return div;
    }
    
    async viewFile(filePath) {
        try {
            this.addLogEntry(`查看文件: ${filePath}`, 'user');
            
            const response = await fetch(`${this.apiBaseUrl}/files/${encodeURIComponent(filePath)}`);
            if (!response.ok) {
                throw new Error(`无法获取文件: ${response.statusText}`);
            }
            
            const fileInfo = await response.json();
            this.showFileModal(fileInfo);
            
        } catch (error) {
            console.error('查看文件失败:', error);
            this.addLogEntry(`查看文件失败: ${error.message}`, 'error');
        }
    }
    
    showFileModal(fileInfo) {
        // 创建模态框
        const modal = document.createElement('div');
        modal.className = 'file-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${fileInfo.title}</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="file-info">
                        <p><strong>路径:</strong> ${fileInfo.path}</p>
                        <p><strong>分类:</strong> ${fileInfo.category}</p>
                        <p><strong>标签:</strong> ${fileInfo.tags.join(', ')}</p>
                        <p><strong>大小:</strong> ${this.formatFileSize(fileInfo.size)}</p>
                        <p><strong>最后修改:</strong> ${new Date(fileInfo.lastModified).toLocaleString()}</p>
                    </div>
                    <div class="file-content">
                        <pre>${this.escapeHtml(fileInfo.content)}</pre>
                    </div>
                </div>
            </div>
        `;
        
        // 添加样式
        const style = document.createElement('style');
        style.textContent = `
            .file-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            
            .modal-content {
                background: white;
                border-radius: 12px;
                max-width: 90%;
                max-height: 90%;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
            
            .modal-header {
                padding: 1.5rem;
                border-bottom: 1px solid #e9ecef;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .modal-header h3 {
                margin: 0;
                color: #333;
            }
            
            .close-modal {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: #666;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .close-modal:hover {
                color: #333;
            }
            
            .modal-body {
                padding: 1.5rem;
                overflow-y: auto;
                flex: 1;
            }
            
            .file-info {
                margin-bottom: 1rem;
                padding: 1rem;
                background: #f8f9fa;
                border-radius: 8px;
            }
            
            .file-info p {
                margin: 0.5rem 0;
            }
            
            .file-content {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 1rem;
                max-height: 400px;
                overflow-y: auto;
            }
            
            .file-content pre {
                white-space: pre-wrap;
                word-wrap: break-word;
                margin: 0;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                line-height: 1.6;
            }
        `;
        
        document.head.appendChild(style);
        
        // 关闭模态框事件
        const closeModal = () => {
            document.body.removeChild(modal);
            document.head.removeChild(style);
        };
        
        modal.querySelector('.close-modal').addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
        
        document.body.appendChild(modal);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<span class="highlight">$1</span>');
    }
    
    showEmptyState() {
        this.searchResults.innerHTML = `
            <div class="empty-state">
                <p>请输入搜索关键词开始查找内容</p>
            </div>
        `;
        this.resultCount.textContent = '共找到 0 个结果';
    }
    
    showErrorMessage(message) {
        this.searchResults.innerHTML = `
            <div class="error-state">
                <p>❌ ${message}</p>
                <p>请检查后端服务器是否正常运行</p>
            </div>
        `;
        this.resultCount.textContent = '搜索失败';
    }
    
    setSearchingState(isSearching) {
        this.isSearching = isSearching;
        this.searchBtn.disabled = isSearching;
        this.searchResults.classList.toggle('searching', isSearching);
        
        if (isSearching) {
            this.searchResults.innerHTML = `
                <div class="empty-state">
                    <div class="loading"></div>
                    <p>正在搜索中...</p>
                </div>
            `;
        }
    }
    
    addLogEntry(content, type = 'system') {
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        
        const time = new Date().toLocaleString('zh-CN');
        logEntry.innerHTML = `
            <div class="log-time">${time}</div>
            <div class="log-content">${this.escapeHtml(content)}</div>
        `;
        
        this.conversationLog.appendChild(logEntry);
        this.conversationLog.scrollTop = this.conversationLog.scrollHeight;
    }
    
    clearLog() {
        this.conversationLog.innerHTML = '';
        this.addLogEntry('日志已清空', 'system');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // 其他实用方法
    async getCategories() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/categories`);
            return await response.json();
        } catch (error) {
            console.error('获取分类失败:', error);
            return [];
        }
    }
    
    async getTags() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/tags`);
            return await response.json();
        } catch (error) {
            console.error('获取标签失败:', error);
            return [];
        }
    }
    
    async getStats() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/stats`);
            return await response.json();
        } catch (error) {
            console.error('获取统计信息失败:', error);
            return null;
        }
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    const searchSystem = new KnowledgeBaseSearch();
    
    // 将搜索系统暴露到全局作用域，便于调试
    window.knowledgeBaseSearch = searchSystem;
    
    console.log('知识库搜索系统已初始化');
    console.log('可用命令:');
    console.log('- knowledgeBaseSearch.performSearch() : 执行搜索');
    console.log('- knowledgeBaseSearch.getCategories() : 获取分类');
    console.log('- knowledgeBaseSearch.getTags() : 获取标签');
    console.log('- knowledgeBaseSearch.getStats() : 获取统计信息');
});

// 添加快捷键支持
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K 聚焦搜索框
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchInput').focus();
    }
    
    // Ctrl/Cmd + L 清空日志
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        document.getElementById('clearLog').click();
    }
    
    // Ctrl/Cmd + Enter 执行搜索
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('searchBtn').click();
    }
});
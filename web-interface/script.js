// 知识库搜索系统 - JavaScript代码

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
        
        // 模拟的知识库数据
        this.knowledgeBase = [
            {
                title: "博士伦",
                source: "D:\\yy\\Sth-Matters\\【文章目录】\\【1 - 哲学类】\\190 - 伦理学\\192 - 个人伦理\\立志\\博士伦.md",
                content: "博士应该逃离的不该是科研，而是特定的人生困境。\n\n不要错误的定性。定性错了，整个问题就错了，而错误的问题已经预定了错误的答案，后面都是注定的一条死路。\n\n什么叫特定的人生困境？\n\n我们开一开上帝视角，飞到二三十年后俯视整条时间线，你会发现一件非常可怕的悲剧——\n\n你所选择的第一项事业、你的第一个雄心壮志，大概率是会以你自己心灰意冷甚至愤懑绝望告终的。",
                tags: ["博士", "人生困境", "科研", "心理建设"]
            },
            {
                title: "导师",
                source: "D:\\yy\\Sth-Matters\\待归档\\导师.md",
                content: "你没什么不可表态的，是你的论文题目，你觉得担心，不管是谁导致的这个担心，这个担心都是你的导师有责任要处理的问题。\n\n导师只是提供指导服务，是辅助而已，不是ta要写论文你给代笔，ta的意见不具备决定性。",
                tags: ["导师", "论文", "学术自由", "责任"]
            },
            {
                title: "傻博士",
                source: "D:\\yy\\Sth-Matters\\【文章目录】\\【1 - 哲学类】\\190 - 伦理学\\198 - 职业伦理\\职业分析\\傻博士.md",
                content: "博士的"傻"其实有一种共同的本质：\n\n一般人倾向解决困扰，博士习惯性的倾向解决问题。\n\n解决困扰是痛苦导向的，是基于体感和直觉的。胜在理论上的"立竿见影"和"直奔主题"。\n\n解决问题则涉及到归纳现象、抽象概念、厘清机制、建立方法、检验方法、得出结论这整个流程。",
                tags: ["博士", "解决问题", "研究方法", "理论"]
            },
            {
                title: "前途",
                source: "D:\\yy\\Sth-Matters\\【文章目录】\\【1 - 哲学类】\\190 - 伦理学\\198 - 职业伦理\\选择与规划\\前途.md",
                content: "借这个问题说一下到底人要怎么选择自己的人生前途。\n\n这共有三个流行的策略：\n\nA）根据主流意见来办——即**从众流。**\n\nB）根据自己对未来趋势的判断来办——即**先知流**。\n\nC）按照"无论世界怎样发展，这种选择总不会被淘汰"的法则，做万全的保守选择——即**稳健流。**",
                tags: ["前途", "职业规划", "选择策略", "人生决策"]
            },
            {
                title: "研发资源",
                source: "D:\\yy\\Sth-Matters\\【文章目录】\\【4 - 应用科学】\\400 - 应用科学总论\\研发资源.md",
                content: "这事涉及到的问题，并不是一个简单的青教非升即走制度的问题。\n\n而是中国的研发资源过度集中在高校系统内的问题。\n\n中国因为长期缺少必要的发展压力，而系统性的缺少在编制外的、有足够容量的人才蓄水池。\n\n那就是产业界的研发力量。",
                tags: ["研发", "资源分配", "高校", "产业界"]
            },
            {
                title: "创新问题",
                source: "D:\\yy\\Sth-Matters\\【文章目录】\\【4 - 应用科学】\\400 - 应用科学总论\\创新问题.md",
                content: "要谈创新的能力，首先要定义什么叫创新。\n\n创新有一连串的等级。\n\nLv0 别人做过，你也知道别人做过，你在跟着做过的人的示范和讲解，试图通过重复其做法复现其结果，或掌握复现其结果的能力。\n\nLv1 别人做过，你也知道别人做过，你拿得到别人做出来的成品（或至少对其存在有确认），且部分知道对方的方法概要，你在尝试靠自己补全那些缺失的环节，以求复现其结果，或掌握复现其结果的能力。",
                tags: ["创新", "能力等级", "研究方法", "创造力"]
            }
        ];
        
        this.init();
    }
    
    init() {
        console.log('初始化知识库搜索系统...');
        
        // 检查DOM元素是否存在
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
        console.log('知识库搜索系统初始化完成');
    }
    
    performSearch() {
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
        
        // 模拟搜索延迟
        setTimeout(() => {
            const results = this.searchKnowledgeBase(query);
            console.log('搜索结果:', results);
            this.displayResults(results, query);
            this.setSearchingState(false);
            
            // 记录搜索结果
            this.addLogEntry(`找到 ${results.length} 个相关结果`, 'assistant');
        }, 800);
    }
    
    searchKnowledgeBase(query) {
        const results = [];
        const lowerQuery = query.toLowerCase();
        
        this.knowledgeBase.forEach(item => {
            let score = 0;
            let matchedContent = '';
            
            // 标题匹配 (权重最高)
            if (item.title.toLowerCase().includes(lowerQuery)) {
                score += 10;
            }
            
            // 标签匹配
            item.tags.forEach(tag => {
                if (tag.toLowerCase().includes(lowerQuery)) {
                    score += 8;
                }
            });
            
            // 内容匹配
            if (item.content.toLowerCase().includes(lowerQuery)) {
                score += 5;
                // 提取匹配的内容片段
                matchedContent = this.extractRelevantContent(item.content, query);
            }
            
            // 文件路径匹配
            if (item.source.toLowerCase().includes(lowerQuery)) {
                score += 3;
            }
            
            if (score > 0) {
                results.push({
                    ...item,
                    score,
                    matchedContent: matchedContent || item.content.substring(0, 200) + '...'
                });
            }
        });
        
        // 按相关性排序
        return results.sort((a, b) => b.score - a.score);
    }
    
    extractRelevantContent(content, query, maxLength = 300) {
        const lowerQuery = query.toLowerCase();
        const lowerContent = content.toLowerCase();
        const queryIndex = lowerContent.indexOf(lowerQuery);
        
        if (queryIndex === -1) return content.substring(0, maxLength) + '...';
        
        // 找到查询词周围的文本
        const start = Math.max(0, queryIndex - 100);
        const end = Math.min(content.length, queryIndex + query.length + 100);
        let extracted = content.substring(start, end);
        
        // 添加省略号
        if (start > 0) extracted = '...' + extracted;
        if (end < content.length) extracted = extracted + '...';
        
        return extracted;
    }
    
    displayResults(results, query) {
        this.searchResults.innerHTML = '';
        this.resultCount.textContent = `共找到 ${results.length} 个结果`;
        
        if (results.length === 0) {
            this.showEmptyState();
            return;
        }
        
        results.forEach((result, index) => {
            const resultElement = this.createResultElement(result, query);
            this.searchResults.appendChild(resultElement);
        });
    }
    
    createResultElement(result, query) {
        const div = document.createElement('div');
        div.className = 'result-item';
        
        // 高亮查询词
        const highlightedTitle = this.highlightText(result.title, query);
        const highlightedContent = this.highlightText(result.matchedContent, query);
        
        div.innerHTML = `
            <h3 class="result-title">${highlightedTitle}</h3>
            <div class="result-source">${result.source}</div>
            <div class="result-content">
                <p>${highlightedContent}</p>
            </div>
            <div class="result-tags">
                ${result.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
        `;
        
        return div;
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
    
    // 添加新的知识库条目
    addKnowledgeBaseEntry(entry) {
        this.knowledgeBase.push(entry);
        this.addLogEntry(`新增知识库条目: ${entry.title}`, 'system');
    }
    
    // 导出日志
    exportLog() {
        const logEntries = Array.from(this.conversationLog.children).map(entry => {
            const time = entry.querySelector('.log-time').textContent;
            const content = entry.querySelector('.log-content').textContent;
            return `[${time}] ${content}`;
        });
        
        const logText = logEntries.join('\n');
        const blob = new Blob([logText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `conversation_log_${new Date().toISOString().split('T')[0]}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        
        this.addLogEntry('日志已导出', 'system');
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    const searchSystem = new KnowledgeBaseSearch();
    
    // 将搜索系统暴露到全局作用域，便于调试
    window.knowledgeBaseSearch = searchSystem;
    
    // 添加一些示例数据
    console.log('知识库搜索系统已初始化');
    console.log('可用命令:');
    console.log('- knowledgeBaseSearch.addKnowledgeBaseEntry(entry) : 添加新的知识库条目');
    console.log('- knowledgeBaseSearch.exportLog() : 导出对话日志');
    console.log('- knowledgeBaseSearch.performSearch() : 执行搜索');
});

// 添加一些有用的快捷键
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

// 添加标签样式
const style = document.createElement('style');
style.textContent = `
    .result-tags {
        margin-top: 1rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .tag {
        background: #e9ecef;
        color: #495057;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .tag:hover {
        background: #dee2e6;
    }
`;
document.head.appendChild(style);
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs-extra');

class ClaudeCodeAPI {
    constructor() {
        this.workspacePath = path.join(__dirname, '../../../');
        this.claudeCodePath = this.findClaudeCodePath();
    }

    // 查找Claude Code可执行文件路径
    findClaudeCodePath() {
        // Windows路径
        if (process.platform === 'win32') {
            const possiblePaths = [
                path.join(process.env.LOCALAPPDATA, 'Anthropic', 'Claude Code', 'claude-code.exe'),
                path.join(process.env.PROGRAMFILES, 'Anthropic', 'Claude Code', 'claude-code.exe'),
                'claude-code.exe'
            ];
            
            for (const testPath of possiblePaths) {
                if (fs.existsSync(testPath)) {
                    return testPath;
                }
            }
        }
        
        // macOS/Linux路径
        const possiblePaths = [
            '/usr/local/bin/claude-code',
            '/opt/claude-code/bin/claude-code',
            'claude-code'
        ];
        
        for (const testPath of possiblePaths) {
            if (fs.existsSync(testPath)) {
                return testPath;
            }
        }
        
        // 如果找不到，尝试使用claude-code命令
        return 'claude-code';
    }

    // 执行Claude Code命令
    async executeCommand(args, options = {}) {
        return new Promise((resolve, reject) => {
            const timeout = options.timeout || 30000; // 默认30秒超时
            
            const child = spawn(this.claudeCodePath, args, {
                cwd: this.workspacePath,
                stdio: ['pipe', 'pipe', 'pipe'],
                shell: false
            });

            let stdout = '';
            let stderr = '';

            child.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            child.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            child.on('close', (code) => {
                if (code === 0) {
                    resolve({
                        success: true,
                        stdout: stdout.trim(),
                        stderr: stderr.trim(),
                        code
                    });
                } else {
                    reject(new Error(`Claude Code command failed with code ${code}: ${stderr}`));
                }
            });

            child.on('error', (error) => {
                reject(new Error(`Failed to execute Claude Code: ${error.message}`));
            });

            // 超时处理
            setTimeout(() => {
                child.kill();
                reject(new Error('Claude Code command timeout'));
            }, timeout);
        });
    }

    // 搜索文件内容
    async searchContent(query, options = {}) {
        const {
            filePattern = '**/*.md',
            maxResults = 50,
            contextLines = 2
        } = options;

        try {
            // 构建搜索命令
            const args = ['search', query];
            
            if (filePattern) {
                args.push('--glob', filePattern);
            }
            
            if (maxResults) {
                args.push('--max-results', maxResults.toString());
            }
            
            if (contextLines) {
                args.push('--context', contextLines.toString());
            }

            const result = await this.executeCommand(args);
            
            // 解析搜索结果
            return this.parseSearchResults(result.stdout);
        } catch (error) {
            console.error('Claude Code search error:', error);
            throw error;
        }
    }

    // 读取文件内容
    async readFile(filePath) {
        try {
            const result = await this.executeCommand(['read', filePath]);
            return result.stdout;
        } catch (error) {
            console.error('Claude Code read file error:', error);
            throw error;
        }
    }

    // 获取文件列表
    async listFiles(pattern = '**/*.md') {
        try {
            const result = await this.executeCommand(['ls', '--glob', pattern]);
            return this.parseFileList(result.stdout);
        } catch (error) {
            console.error('Claude Code list files error:', error);
            throw error;
        }
    }

    // 获取项目状态
    async getStatus() {
        try {
            const result = await this.executeCommand(['status']);
            return this.parseStatus(result.stdout);
        } catch (error) {
            console.error('Claude Code status error:', error);
            throw error;
        }
    }

    // 执行任务
    async executeTask(taskDescription, options = {}) {
        const {
            timeout = 60000, // 默认1分钟超时
            background = false
        } = options;

        try {
            const args = ['task', taskDescription];
            
            if (background) {
                args.push('--background');
            }

            const result = await this.executeCommand(args, { timeout });
            return this.parseTaskResult(result.stdout);
        } catch (error) {
            console.error('Claude Code task error:', error);
            throw error;
        }
    }

    // 解析搜索结果
    parseSearchResults(stdout) {
        const results = [];
        const lines = stdout.split('\n');
        
        let currentFile = null;
        let currentMatches = [];
        
        for (const line of lines) {
            if (line.startsWith('File: ')) {
                // 新文件开始
                if (currentFile) {
                    results.push({
                        file: currentFile,
                        matches: currentMatches
                    });
                }
                currentFile = line.substring(6).trim();
                currentMatches = [];
            } else if (line.includes(':') && line.trim()) {
                // 匹配行
                const [lineNumber, ...contentParts] = line.split(':');
                const content = contentParts.join(':').trim();
                
                currentMatches.push({
                    lineNumber: parseInt(lineNumber),
                    content: content
                });
            }
        }
        
        // 添加最后一个文件
        if (currentFile) {
            results.push({
                file: currentFile,
                matches: currentMatches
            });
        }
        
        return results;
    }

    // 解析文件列表
    parseFileList(stdout) {
        const files = [];
        const lines = stdout.split('\n');
        
        for (const line of lines) {
            if (line.trim()) {
                files.push(line.trim());
            }
        }
        
        return files;
    }

    // 解析状态
    parseStatus(stdout) {
        const status = {
            branch: '',
            clean: true,
            changes: []
        };
        
        const lines = stdout.split('\n');
        for (const line of lines) {
            if (line.startsWith('On branch ')) {
                status.branch = line.substring(10).trim();
            } else if (line.startsWith('Changes not staged for commit:')) {
                status.clean = false;
            } else if (line.trim().startsWith('modified:')) {
                status.changes.push({
                    type: 'modified',
                    file: line.substring(9).trim()
                });
            } else if (line.trim().startsWith('new file:')) {
                status.changes.push({
                    type: 'new',
                    file: line.substring(8).trim()
                });
            } else if (line.trim().startsWith('deleted:')) {
                status.changes.push({
                    type: 'deleted',
                    file: line.substring(8).trim()
                });
            }
        }
        
        return status;
    }

    // 解析任务结果
    parseTaskResult(stdout) {
        const lines = stdout.split('\n');
        const result = {
            success: true,
            message: '',
            output: []
        };
        
        for (const line of lines) {
            if (line.startsWith('Task completed:')) {
                result.message = line.substring(15).trim();
            } else if (line.trim()) {
                result.output.push(line.trim());
            }
        }
        
        return result;
    }

    // 检查Claude Code是否可用
    async isAvailable() {
        try {
            await this.executeCommand(['--version']);
            return true;
        } catch (error) {
            console.error('Claude Code not available:', error);
            return false;
        }
    }

    // 获取Claude Code版本
    async getVersion() {
        try {
            const result = await this.executeCommand(['--version']);
            return result.stdout;
        } catch (error) {
            console.error('Failed to get Claude Code version:', error);
            return 'unknown';
        }
    }
}

module.exports = ClaudeCodeAPI;
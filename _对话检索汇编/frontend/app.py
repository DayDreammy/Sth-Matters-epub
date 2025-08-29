#!/usr/bin/env python3
"""
知识库主题搜索后端服务器
处理前端请求，执行Claude Code无头模式搜索，并发送邮件通知
"""

import os
import sys
import json
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, Any, List
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import queue

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('search_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 任务队列
task_queue = queue.Queue()
results = {}

class SearchTask:
    """搜索任务类"""
    def __init__(self, task_id: str, data: Dict[str, Any]):
        self.task_id = task_id
        self.data = data
        self.status = "pending"
        self.progress = 0
        self.message = ""
        self.result = None
        self.error = None
        self.created_at = datetime.now()

class SearchEngine:
    """搜索引擎类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.claude_code_path = self.config.get('claude_code_path', 'claude')
        self.base_dir = Path(__file__).parent
        self.generated_docs_dir = self.base_dir / "generated_docs"
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "claude_code_path": "claude",
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_username": "",
                "smtp_password": "",
                "from_email": ""
            },
            "output_dir": "generated_docs",
            "max_file_size": 50 * 1024 * 1024  # 50MB
        }
    
    def execute_claude_search(self, topic: str, formats: List[str]) -> Dict[str, Any]:
        """执行Claude Code无头模式搜索"""
        try:
            # 构建Claude Code命令
            cmd = [
                self.claude_code_path,
                '-p',
                f'搜索主题：{topic}，生成格式：{", ".join(formats)}',
                '--output-format', 'json',
                '--allowed-tools', 'Bash,Read,Write,Glob,Grep,Task',
                '--cwd', str(self.base_dir.parent),
                '--append-system-prompt', '@CLAUDE.md'
            ]
            
            logger.info(f"执行Claude Code命令: {' '.join(cmd)}")
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800  # 30分钟超时
            )
            
            if result.returncode == 0:
                try:
                    output = json.loads(result.stdout)
                    return {
                        'success': True,
                        'output': output,
                        'files': self.find_generated_files(topic)
                    }
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'output': result.stdout,
                        'files': self.find_generated_files(topic)
                    }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'returncode': result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '搜索超时，请重试'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def find_generated_files(self, topic: str) -> List[str]:
        """查找生成的文件"""
        files = []
        if self.generated_docs_dir.exists():
            for file_path in self.generated_docs_dir.glob(f"*{topic}*"):
                if file_path.is_file():
                    files.append(str(file_path))
        return files

class EmailNotifier:
    """邮件通知类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.smtp_server = config['email']['smtp_server']
        self.smtp_port = config['email']['smtp_port']
        self.smtp_username = config['email']['smtp_username']
        self.smtp_password = config['email']['smtp_password']
        self.from_email = config['email']['from_email']
    
    def send_notification(self, to_email: str, subject: str, body: str, attachments: List[str] = None):
        """发送邮件通知"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # 添加邮件正文
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 添加附件
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"邮件已发送至 {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False

class TaskWorker:
    """任务工作线程"""
    
    def __init__(self, search_engine: SearchEngine, email_notifier: EmailNotifier):
        self.search_engine = search_engine
        self.email_notifier = email_notifier
        self.running = True
    
    def process_task(self, task: SearchTask):
        """处理单个任务"""
        try:
            task.status = "processing"
            task.message = "正在初始化搜索..."
            task.progress = 10
            
            topic = task.data['topic']
            email = task.data['email']
            formats = task.data.get('formats', 'markdown,html,epub').split(',')
            
            logger.info(f"开始处理任务: {task.task_id}, 主题: {topic}")
            
            # 执行搜索
            task.message = "正在执行智能检索..."
            task.progress = 30
            
            search_result = self.search_engine.execute_claude_search(topic, formats)
            
            if search_result['success']:
                task.message = "正在生成文档..."
                task.progress = 60
                
                # 准备邮件内容
                subject = f"知识库搜索完成 - {topic}"
                body = self.create_email_body(topic, search_result, task.data)
                
                # 发送邮件
                task.message = "正在发送邮件..."
                task.progress = 80
                
                attachments = search_result.get('files', [])
                email_sent = self.email_notifier.send_notification(
                    email, subject, body, attachments
                )
                
                if email_sent:
                    task.status = "completed"
                    task.message = "搜索完成，结果已发送至您的邮箱"
                    task.progress = 100
                    task.result = search_result
                else:
                    task.status = "failed"
                    task.message = "搜索完成，但邮件发送失败"
                    task.error = "邮件发送失败"
                    
            else:
                task.status = "failed"
                task.message = "搜索失败"
                task.error = search_result.get('error', '未知错误')
                
        except Exception as e:
            logger.error(f"处理任务 {task.task_id} 时发生错误: {e}")
            task.status = "failed"
            task.message = "处理过程中发生错误"
            task.error = str(e)
    
    def create_email_body(self, topic: str, search_result: Dict[str, Any], task_data: Dict[str, Any]) -> str:
        """创建邮件正文"""
        files = search_result.get('files', [])
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .content {{ padding: 20px; }}
                .file-list {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🔍 知识库搜索完成</h2>
                <p><strong>搜索主题：</strong>{topic}</p>
                <p><strong>完成时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="content">
                <h3>📊 搜索结果</h3>
                <p>已成功为您生成以下格式的文档：</p>
                
                <div class="file-list">
                    <h4>📁 生成的文件：</h4>
                    <ul>
                """
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            html_body += f"<li><strong>{file_name}</strong> ({file_size:.1f} KB)</li>"
        
        html_body += f"""
                    </ul>
                </div>
                
                <h3>📋 搜索配置</h3>
                <ul>
                    <li><strong>优先级：</strong>{task_data.get('priority', '普通')}</li>
                    <li><strong>输出格式：</strong>{task_data.get('formats', 'markdown,html,epub')}</li>
                </ul>
                
                {f'<p><strong>备注：</strong>{task_data.get("notes", "")}</p>' if task_data.get('notes') else ''}
                
                <p>所有文件已作为附件发送，请查收。</p>
            </div>
            
            <div class="footer">
                <p>此邮件由知识库主题搜索系统自动发送</p>
                <p>如有问题，请联系系统管理员</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def run(self):
        """运行工作线程"""
        while self.running:
            try:
                task = task_queue.get(timeout=1)
                self.process_task(task)
                results[task.task_id] = task
                task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"工作线程错误: {e}")

# 全局变量
search_engine = SearchEngine()
email_notifier = EmailNotifier(search_engine.config)
task_worker = TaskWorker(search_engine, email_notifier)

@app.route('/')
def index():
    """首页"""
    return app.send_static_file('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """搜索接口"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['topic', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 创建任务
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(data['topic']) % 10000:04d}"
        task = SearchTask(task_id, data)
        
        # 添加到队列
        task_queue.put(task)
        results[task_id] = task
        
        logger.info(f"创建搜索任务: {task_id}, 主题: {data['topic']}")
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '搜索任务已创建，正在处理中...'
        })
        
    except Exception as e:
        logger.error(f"搜索接口错误: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """获取任务状态"""
    if task_id not in results:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404
    
    task = results[task_id]
    return jsonify({
        'success': True,
        'task_id': task_id,
        'status': task.status,
        'progress': task.progress,
        'message': task.message,
        'created_at': task.created_at.isoformat(),
        'result': task.result,
        'error': task.error
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'queue_size': task_queue.qsize(),
        'completed_tasks': len([t for t in results.values() if t.status == 'completed'])
    })

def main():
    """主函数"""
    try:
        # 检查配置
        if not search_engine.config['email']['smtp_username']:
            logger.warning("邮件配置未完整设置，邮件通知功能将不可用")
        
        # 启动工作线程
        worker_thread = threading.Thread(target=task_worker.run, daemon=True)
        worker_thread.start()
        
        logger.info("知识库搜索服务器启动")
        logger.info(f"服务地址: http://localhost:5000")
        
        # 启动Flask服务器
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        logger.info("正在关闭服务器...")
        task_worker.running = False
        sys.exit(0)
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
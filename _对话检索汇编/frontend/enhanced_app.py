#!/usr/bin/env python3
"""
知识库主题搜索增强版后端服务器
集成搜索、文件下载和预览功能
"""

import os
import sys
import json
import subprocess
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import threading
import queue

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_search_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 任务队列
task_queue = queue.Queue()
results = {}

class FileManager:
    """文件管理类"""

    def __init__(self, base_dir: str = "_对话检索汇编/generated_docs"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_file_list(self, topic: Optional[str] = None, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取文件列表"""
        files = []

        try:
            # 搜索文件
            pattern = f"*{topic}*" if topic else "*"
            if file_type:
                pattern = f"*{topic}*.{file_type}" if topic else f"*.{file_type}"

            for file_path in self.base_dir.glob(pattern):
                if file_path.is_file():
                    # 获取文件信息
                    stat = file_path.stat()
                    file_info = {
                        'name': file_path.name,
                        'path': str(file_path.relative_to(self.base_dir.parent.parent)),
                        'size': stat.st_size,
                        'size_human': self._format_size(stat.st_size),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'type': self._get_file_type(file_path.suffix),
                        'extension': file_path.suffix.lower(),
                        'download_url': f"/api/files/download/{file_path.name}",
                        'preview_url': self._get_preview_url(file_path)
                    }

                    # 提取主题信息
                    file_info['topic'] = self._extract_topic(file_path.name)

                    files.append(file_info)

            # 按修改时间倒序排列
            files.sort(key=lambda x: x['modified'], reverse=True)

        except Exception as e:
            logger.error(f"获取文件列表失败: {e}")

        return files

    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"

    def _get_file_type(self, extension: str) -> str:
        """根据扩展名获取文件类型"""
        extension = extension.lower()
        if extension == '.html':
            return 'html'
        elif extension in ['.md', '.markdown']:
            return 'markdown'
        elif extension == '.epub':
            return 'epub'
        elif extension == '.json':
            return 'json'
        else:
            return 'unknown'

    def _get_preview_url(self, file_path: Path) -> Optional[str]:
        """获取预览URL"""
        if file_path.suffix.lower() == '.html':
            return f"/api/files/preview/{file_path.name}"
        return None

    def _extract_topic(self, filename: str) -> str:
        """从文件名中提取主题"""
        # 移除常见的后缀
        suffixes = [
            '_thematic_文档.md', '_source_based_文档.md', '_concepts_文档.md',
            '_summary_文档.md', '_html_文档.html', '_epub_文档.epub'
        ]

        topic = filename
        for suffix in suffixes:
            if topic.endswith(suffix):
                topic = topic[:-len(suffix)]
                break

        return topic

    def get_file_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """获取单个文件信息"""
        file_path = self.base_dir / filename

        if not file_path.exists() or not file_path.is_file():
            return None

        try:
            stat = file_path.stat()
            return {
                'name': filename,
                'path': str(file_path),
                'size': stat.st_size,
                'size_human': self._format_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': self._get_file_type(file_path.suffix),
                'extension': file_path.suffix.lower(),
                'download_url': f"/api/files/download/{filename}",
                'preview_url': self._get_preview_url(file_path),
                'topic': self._extract_topic(filename)
            }
        except Exception as e:
            logger.error(f"获取文件信息失败 {filename}: {e}")
            return None

    def search_files(self, query: str) -> List[Dict[str, Any]]:
        """搜索文件"""
        all_files = self.get_file_list()

        if not query:
            return all_files

        query = query.lower()
        matched_files = []

        for file_info in all_files:
            # 搜索文件名和主题
            if (query in file_info['name'].lower() or
                query in file_info['topic'].lower()):
                matched_files.append(file_info)

        return matched_files

    def get_topics_summary(self) -> Dict[str, Any]:
        """获取主题汇总信息"""
        files = self.get_file_list()
        topics = {}

        for file_info in files:
            topic = file_info['topic']
            if topic not in topics:
                topics[topic] = {
                    'topic': topic,
                    'files': [],
                    'total_size': 0,
                    'types': set(),
                    'latest_modified': '1970-01-01T00:00:00'
                }

            topics[topic]['files'].append(file_info)
            topics[topic]['total_size'] += file_info['size']
            topics[topic]['types'].add(file_info['type'])

            if file_info['modified'] > topics[topic]['latest_modified']:
                topics[topic]['latest_modified'] = file_info['modified']

        # 转换set为list并排序
        for topic_data in topics.values():
            topic_data['types'] = sorted(list(topic_data['types']))
            topic_data['total_size_human'] = self._format_size(topic_data['total_size'])
            topic_data['file_count'] = len(topic_data['files'])

        return {
            'topics': sorted(topics.values(), key=lambda x: x['latest_modified'], reverse=True),
            'total_topics': len(topics),
            'total_files': len(files),
            'total_size': self._format_size(sum(f['size'] for f in files))
        }


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
            logger.warning(
                f"Configuration file {config_path} not found, using default configuration")
            return self.get_default_config()
        except UnicodeDecodeError:
            logger.warning(
                f"Configuration file {config_path} encoding error, using default configuration")
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
        """Execute Claude Code headless mode search"""
        try:
            # Set environment variables for Claude Code
            env = os.environ.copy()
            env['ANTHROPIC_BASE_URL'] = 'https://open.bigmodel.cn/api/anthropic'
            env['ANTHROPIC_AUTH_TOKEN'] = '3b222275909a41df8eb8553503ab3300.rJZMbCswT0DXgqph'

            # Use forward slashes for cross-platform compatibility
            target_dir = str(self.base_dir.parent).replace('\\', '/')

            # Build Claude Code command with proper quoting
            prompt = f'{topic},output formats:{formats}'
            # 计算对话检索汇编目录相对于项目根目录的相对路径
            conversation_dir = '_对话检索汇编'
            cmd = [
                self.claude_code_path,
                '-p',
                f'"{prompt}"',
                '--output-format', 'json',
                '--allowed-tools', 'Bash,Read,Write,Glob,Grep,Task',
                '--add-dir', conversation_dir  # 使用相对路径
            ]

            logger.info(f"Target directory: {target_dir}")
            logger.info(f"Executing Claude Code command: {' '.join(cmd)}")

            # Execute command with environment variables
            # 首先切换到项目根目录，然后执行claude命令
            project_root = str(self.base_dir.parent.parent)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minutes timeout
                env=env,  # Pass environment variables
                cwd=project_root,  # 设置工作目录为项目根目录
                encoding='utf-8',  # Explicitly set UTF-8 encoding
                errors='replace'  # Handle encoding errors gracefully
            )

            if result.returncode == 0:
                logger.info(f"Claude Code stdout: {result.stdout}")
                logger.info(f"Claude Code stderr: {result.stderr}")

                # Try to parse JSON output
                try:
                    output = json.loads(result.stdout)
                    return {
                        'success': True,
                        'output': output,
                        'files': self.find_generated_files(topic)
                    }
                except json.JSONDecodeError:
                    # If output is not JSON, check if it's a success response
                    if result.stdout and "error" not in result.stdout.lower():
                        return {
                            'success': True,
                            'output': result.stdout,
                            'files': self.find_generated_files(topic)
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"Claude Code execution failed: {result.stdout}",
                            'stderr': result.stderr
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
                'error': 'Search timeout, please retry'
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

            logger.info(f"Email sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
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

            logger.info(
                f"Starting task processing: {task.task_id}, topic: {topic}")

            # 执行搜索
            task.message = "正在执行智能检索..."
            task.progress = 30

            search_result = self.search_engine.execute_claude_search(
                topic, formats)

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
                    task.message = "搜索完成，结果已发送至您的邮箱。您也可以在文件下载中心查看和下载。"
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

                <h3>📥 文件下载</h3>
                <p>您也可以访问 <a href="http://localhost:5001">文件下载中心</a> 在线预览HTML文档或下载所有文件。</p>

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
file_manager = FileManager()
task_worker = TaskWorker(search_engine, email_notifier)


# ========== 搜索相关接口 ==========
@app.route('/')
def index():
    """主页 - 返回搜索界面"""
    return send_from_directory('static', 'search.html')


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

        logger.info(f"Created search task: {task_id}, topic: {data['topic']}")

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Search task created and processing...'
        })

    except Exception as e:
        logger.error(f"Search API error: {e}")
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


# ========== 文件管理相关接口 ==========
@app.route('/files')
def files_page():
    """文件管理页面"""
    return send_from_directory('static', 'files.html')


@app.route('/api/files', methods=['GET'])
def get_files():
    """获取文件列表"""
    try:
        topic = request.args.get('topic')
        file_type = request.args.get('type')

        files = file_manager.get_file_list(topic, file_type)

        return jsonify({
            'success': True,
            'files': files,
            'count': len(files),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"获取文件列表失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/files/search', methods=['GET'])
def search_files():
    """搜索文件"""
    try:
        query = request.args.get('q', '').strip()

        if not query:
            return jsonify({
                'success': False,
                'message': '搜索关键词不能为空'
            }), 400

        files = file_manager.search_files(query)

        return jsonify({
            'success': True,
            'query': query,
            'files': files,
            'count': len(files),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"搜索文件失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/files/topics', methods=['GET'])
def get_topics():
    """获取主题汇总"""
    try:
        topics_summary = file_manager.get_topics_summary()

        return jsonify({
            'success': True,
            **topics_summary,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"获取主题汇总失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/files/download/<filename>', methods=['GET'])
def download_file(filename):
    """下载文件"""
    try:
        file_path = file_manager.base_dir / filename

        if not file_path.exists() or not file_path.is_file():
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404

        # 推测MIME类型
        mimetype, _ = mimetypes.guess_type(str(file_path))
        if mimetype is None:
            mimetype = 'application/octet-stream'

        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )

    except Exception as e:
        logger.error(f"下载文件失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/files/preview/<filename>', methods=['GET'])
def preview_file(filename):
    """预览文件（目前仅支持HTML）"""
    try:
        file_path = file_manager.base_dir / filename

        if not file_path.exists() or not file_path.is_file():
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404

        # 检查文件类型
        if file_path.suffix.lower() != '.html':
            return jsonify({
                'success': False,
                'message': '仅支持HTML文件预览'
            }), 400

        # 读取HTML内容并返回
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}

        except UnicodeDecodeError:
            return jsonify({
                'success': False,
                'message': '文件编码错误'
            }), 500

    except Exception as e:
        logger.error(f"预览文件失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        files = file_manager.get_file_list()
        topics_summary = file_manager.get_topics_summary()

        # 按文件类型统计
        type_stats = {}
        for file_info in files:
            file_type = file_info['type']
            if file_type not in type_stats:
                type_stats[file_type] = {'count': 0, 'size': 0}
            type_stats[file_type]['count'] += 1
            type_stats[file_type]['size'] += file_info['size']

        for stats in type_stats.values():
            stats['size_human'] = file_manager._format_size(stats['size'])

        return jsonify({
            'success': True,
            'stats': {
                'total_files': len(files),
                'total_topics': topics_summary['total_topics'],
                'total_size': topics_summary['total_size'],
                'by_type': type_stats,
                'latest_file': files[0] if files else None
            },
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def main():
    """主函数"""
    try:
        # 创建static目录
        static_dir = Path('static')
        static_dir.mkdir(exist_ok=True)

        # 检查配置
        if not search_engine.config['email']['smtp_username']:
            logger.warning("邮件配置未完整设置，邮件通知功能将不可用")

        # 启动工作线程
        worker_thread = threading.Thread(target=task_worker.run, daemon=True)
        worker_thread.start()

        logger.info("Enhanced Knowledge Base Search Server started")
        logger.info(f"搜索服务地址: http://localhost:5000")
        logger.info(f"文件下载地址: http://localhost:5000/files")

        # 启动Flask服务器
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        task_worker.running = False
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
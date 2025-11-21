#!/usr/bin/env python3
"""
文件下载和预览服务
为搜索完成的文档提供下载和预览功能
"""

import os
import json
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class FileManager:
    """文件管理类"""

    def __init__(self, base_dir: str = "../generated_docs"):
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
                        'download_url': f"/api/download/{file_path.name}",
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
            return f"/api/preview/{file_path.name}"
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
                'download_url': f"/api/download/{filename}",
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

# 全局文件管理器
file_manager = FileManager()

@app.route('/')
def index():
    """主页 - 返回文件管理界面"""
    return send_from_directory('static', 'index.html')

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

@app.route('/api/files/<filename>', methods=['GET'])
def get_file_info(filename):
    """获取单个文件信息"""
    try:
        file_info = file_manager.get_file_info(filename)

        if not file_info:
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404

        return jsonify({
            'success': True,
            'file': file_info,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"获取文件信息失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
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

@app.route('/api/preview/<filename>', methods=['GET'])
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

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'message': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    # 创建static目录
    static_dir = Path('static')
    static_dir.mkdir(exist_ok=True)

    logger.info("文件下载和预览服务启动")
    logger.info(f"服务地址: http://localhost:5001")
    logger.info(f"文件目录: {file_manager.base_dir}")

    app.run(host='0.0.0.0', port=5001, debug=True)
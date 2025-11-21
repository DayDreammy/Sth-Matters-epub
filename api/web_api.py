#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能检索系统Web API
提供简单的Flask REST API接口
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from core.search_engine import IntelligentSearchEngine
from core.document_generator import DocumentGenerator

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化搜索引擎
engine = IntelligentSearchEngine("knowledge_base", config_path="config/config.json")
generator = DocumentGenerator("output")


@app.route('/api/search', methods=['POST'])
def api_search():
    """搜索API"""
    try:
        data = request.get_json()

        query = data.get('query', '').strip()
        if not query:
            return jsonify({"error": "搜索关键词不能为空"}), 400

        search_type = data.get('type', 'all')
        max_results = min(data.get('max_results', 50), 200)  # 限制最大结果数
        include_full_content = data.get('include_full_content', False)

        # 执行搜索
        results = engine.search(query, search_type, max_results, include_full_content)

        results_data = []
        for r in results:
            result_item = {
                "title": r.title,
                "file_path": r.file_path,
                "content_preview": r.content_preview,
                "relevance_score": r.relevance_score,
                "match_type": r.match_type,
                "line_numbers": r.line_numbers,
                "word_count": r.word_count
            }

            # 如果有完整内容，添加到结果中
            if include_full_content and r.full_content is not None:
                result_item["full_content"] = r.full_content

            results_data.append(result_item)

        return jsonify({
            "success": True,
            "query": query,
            "search_type": search_type,
            "total_results": len(results),
            "include_full_content": include_full_content,
            "results": results_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """生成文档API"""
    try:
        data = request.get_json()

        query = data.get('query', '').strip()
        if not query:
            return jsonify({"error": "搜索关键词不能为空"}), 400

        search_type = data.get('type', 'all')
        max_results = min(data.get('max_results', 50), 200)
        format_type = data.get('format', 'summary')
        save_file = data.get('save_file', False)
        include_full_content = data.get('include_full_content', False)

        # 执行搜索
        results = engine.search(query, search_type, max_results, include_full_content)

        if not results:
            return jsonify({"error": "未找到相关结果"}), 404

        # 生成文档
        if format_type == 'html':
            content = generator.generate_html(results, query, include_full_content)
        elif format_type == 'json':
            content = generator.generate_json(results, query, include_full_content=include_full_content)
        else:
            content = generator.generate_markdown(results, query, format_type, include_full_content)

        response_data = {
            "success": True,
            "query": query,
            "format": format_type,
            "total_results": len(results),
            "include_full_content": include_full_content,
            "content": content
        }

        # 如果需要保存文件
        if save_file:
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"search_{safe_query}_{format_type}"
            output_format = "json" if format_type == 'json' else ("html" if format_type == 'html' else "markdown")
            saved_path = generator.save_document(content, filename, output_format)
            response_data["saved_file"] = saved_path

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """获取统计信息API"""
    try:
        stats = engine.get_stats()
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/rebuild', methods=['POST'])
def api_rebuild():
    """重建索引API"""
    try:
        index = engine.build_index()
        return jsonify({
            "success": True,
            "message": "索引重建完成",
            "index": index["metadata"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def api_health():
    """健康检查API"""
    return jsonify({
        "status": "healthy",
        "service": "Intelligent Search Engine",
        "version": "1.0.0"
    })


@app.route('/api/download/<filename>', methods=['GET'])
def api_download(filename):
    """下载生成的文件"""
    try:
        file_path = Path("output") / filename
        if not file_path.exists():
            return jsonify({"error": "文件不存在"}), 404

        return send_file(str(file_path), as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/profiles', methods=['GET'])
def api_profiles():
    """获取搜索配置文件列表"""
    try:
        profiles = engine.get_search_profiles()
        return jsonify({
            "success": True,
            "profiles": profiles
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/profile/<profile_name>', methods=['POST'])
def api_use_profile(profile_name):
    """使用指定的搜索配置文件"""
    try:
        engine.use_search_profile(profile_name)
        return jsonify({
            "success": True,
            "message": f"已切换到搜索配置: {profile_name}",
            "current_profile": profile_name
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/paths', methods=['GET', 'POST'])
def api_search_paths():
    """获取或设置搜索路径"""
    try:
        if request.method == 'GET':
            return jsonify({
                "success": True,
                "search_paths": engine.search_paths,
                "knowledge_base_dir": str(engine.knowledge_base_dir)
            })
        else:
            data = request.get_json()
            paths = data.get('paths', [])
            engine.set_search_paths(paths)
            return jsonify({
                "success": True,
                "message": "搜索路径已更新",
                "search_paths": engine.search_paths
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "接口不存在"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500


if __name__ == '__main__':
    print("🚀 启动智能检索系统Web API")
    print("📡 服务地址: http://localhost:5000")
    print("📚 API文档:")
    print("  POST /api/search - 搜索接口")
    print("  POST /api/generate - 生成文档接口")
    print("  GET /api/stats - 统计信息接口")
    print("  POST /api/rebuild - 重建索引接口")
    print("  GET /api/health - 健康检查接口")
    print("  GET /api/download/<filename> - 下载文件接口")
    print("-" * 50)

    # 启动前构建索引
    print("🔄 初始化搜索引擎...")
    engine.build_index()
    print("✅ 搜索引擎就绪")

    app.run(host='0.0.0.0', port=5000, debug=True)
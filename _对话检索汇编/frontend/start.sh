#!/bin/bash

# 知识库主题搜索系统启动脚本

set -e

echo "🚀 启动知识库主题搜索系统..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
echo "📋 Python版本: $python_version"

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误: 请在frontend目录中运行此脚本"
    exit 1
fi

# 检查依赖
echo "🔍 检查依赖..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: requirements.txt 文件不存在"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "⚠️  警告: config.json 不存在，将使用默认配置"
fi

# 检查Claude Code
echo "🔍 检查Claude Code..."
if ! command -v claude &> /dev/null; then
    echo "❌ 错误: Claude Code 未找到，请确保已安装Claude Code CLI"
    echo "安装指南: https://docs.anthropic.com/claude/docs/claude-code"
    exit 1
fi

# 创建必要的目录
mkdir -p ../generated_docs
mkdir -p logs

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=production

echo "✅ 环境检查完成"
echo "🌐 启动服务器..."
echo "📍 服务地址: http://localhost:5000"
echo "📊 健康检查: http://localhost:5000/api/health"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动服务器
python app.py
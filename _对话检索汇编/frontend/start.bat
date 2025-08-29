@echo off
chcp 65001 >nul
echo 🚀 启动知识库主题搜索系统...

:: 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: Python 未找到，请确保已安装Python
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo 📋 Python版本: %%i

:: 检查是否在正确的目录
if not exist "app.py" (
    echo ❌ 错误: 请在frontend目录中运行此脚本
    pause
    exit /b 1
)

:: 检查依赖文件
if not exist "requirements.txt" (
    echo ❌ 错误: requirements.txt 文件不存在
    pause
    exit /b 1
)

:: 安装依赖
echo 📦 安装Python依赖...
pip install -r requirements.txt

:: 检查配置文件
if not exist "config.json" (
    echo ⚠️  警告: config.json 不存在，将使用默认配置
)

:: 检查Claude Code
echo 🔍 检查Claude Code...
claude --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: Claude Code 未找到，请确保已安装Claude Code CLI
    echo 安装指南: https://docs.anthropic.com/claude/docs/claude-code
    pause
    exit /b 1
)

:: 创建必要的目录
if not exist "..\generated_docs" mkdir "..\generated_docs"
if not exist "logs" mkdir "logs"

echo ✅ 环境检查完成
echo 🌐 启动服务器...
echo 📍 服务地址: http://localhost:5000
echo 📊 健康检查: http://localhost:5000/api/health
echo.
echo 按 Ctrl+C 停止服务器
echo.

:: 启动服务器
python app.py

pause
@echo off
echo ========================================
echo 知识库搜索系统启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo 检查Node.js是否安装...
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Node.js 未安装或不在PATH中
    echo 请访问 https://nodejs.org/ 下载并安装Node.js
    pause
    exit /b 1
)

echo Node.js版本:
node --version
echo.

echo 检查npm是否安装...
npm --version >nul 2>&1
if errorlevel 1 (
    echo 错误: npm 未安装
    pause
    exit /b 1
)

echo npm版本:
npm --version
echo.

echo 进入后端目录...
cd backend

echo 检查package.json是否存在...
if not exist "package.json" (
    echo 错误: package.json 不存在
    cd ..
    pause
    exit /b 1
)

echo 检查node_modules是否存在...
if not exist "node_modules" (
    echo 正在安装依赖包...
    npm install
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        cd ..
        pause
        exit /b 1
    )
    echo 依赖包安装完成
) else (
    echo 依赖包已存在
)

echo.
echo ========================================
echo 启动后端服务器...
echo ========================================
echo 服务器将在 http://localhost:3000 启动
echo 请保持此窗口运行
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

node server.js

pause
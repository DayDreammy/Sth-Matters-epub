@echo off
echo Starting Knowledge Base Search System...

:: Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found, please ensure Python is installed
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo Python Version: %%i

:: Check if in correct directory
if not exist "app.py" (
    echo ERROR: Please run this script in the frontend directory
    pause
    exit /b 1
)

:: Check requirements file
if not exist "requirements.txt" (
    echo ERROR: requirements.txt file not found
    pause
    exit /b 1
)

:: Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

:: Check configuration file
if not exist "config.json" (
    echo WARNING: config.json not found, will use default configuration
)

set ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
set ANTHROPIC_AUTH_TOKEN=3b222275909a41df8eb8553503ab3300.rJZMbCswT0DXgqph

:: Create necessary directories
if not exist "..\generated_docs" mkdir "..\generated_docs"
if not exist "logs" mkdir "logs"

echo Environment check completed
echo Starting server...
echo Service URL: http://localhost:5000
echo Health check: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop server
echo.

:: Start server
python app.py

pause
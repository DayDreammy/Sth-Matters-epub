#!/bin/bash

# Knowledge Base Search System Startup Script

set -e

echo "Starting Knowledge Base Search System..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
echo "Python Version: $python_version"

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "ERROR: Please run this script in the frontend directory"
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt file not found"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check configuration file
if [ ! -f "config.json" ]; then
    echo "WARNING: config.json not found, will use default configuration"
fi

# Check Claude Code
echo "Checking Claude Code..."
if ! command -v claude &> /dev/null; then
    echo "ERROR: Claude Code not found, please ensure Claude Code CLI is installed"
    echo "Installation guide: https://docs.anthropic.com/claude/docs/claude-code"
    exit 1
fi

# Create necessary directories
mkdir -p ../generated_docs
mkdir -p logs

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

echo "Environment check completed"
echo "Starting server..."
echo "Service URL: http://localhost:5000"
echo "Health check: http://localhost:5000/api/health"
echo ""
echo "Press Ctrl+C to stop server"
echo ""

# Start server
python app.py
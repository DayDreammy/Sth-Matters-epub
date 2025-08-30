#!/usr/bin/env python3
"""
Frontend Interface System Test Script
Used to verify that the web interface and backend API are working properly
"""

import json
import requests
import time
import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_server_health():
    """Test server health status"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Server health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Queue size: {data.get('queue_size')}")
            print(f"   Completed tasks: {data.get('completed_tasks')}")
            return True
        else:
            print(f"[ERROR] Server health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Cannot connect to server: {e}")
        return False

def test_search_api():
    """Test search API"""
    try:
        # Test data
        test_data = {
            "topic": "Test Topic",
            "email": "test@example.com",
            "priority": "normal",
            "formats": "markdown,html",
            "notes": "This is a test request"
        }
        
        print("[SEARCH] Testing search API...")
        response = requests.post(
            'http://localhost:5000/api/search',
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                task_id = data.get('task_id')
                print(f"[OK] Search API test passed")
                print(f"   Task ID: {task_id}")
                return task_id
            else:
                print(f"[ERROR] Search API test failed: {data.get('message')}")
                return None
        else:
            print(f"[ERROR] Search API test failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Search API test exception: {e}")
        return None

def test_task_status(task_id):
    """Test task status query"""
    if not task_id:
        return False
        
    try:
        print(f"[STATUS] Testing task status query (ID: {task_id})...")
        response = requests.get(f'http://localhost:5000/api/status/{task_id}', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"[OK] Task status query successful")
                print(f"   Status: {data.get('status')}")
                print(f"   Progress: {data.get('progress')}%")
                print(f"   Message: {data.get('message')}")
                return True
            else:
                print(f"[ERROR] Task status query failed: {data.get('message')}")
                return False
        else:
            print(f"[ERROR] Task status query failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Task status query exception: {e}")
        return False

def test_config_file():
    """Test configuration file"""
    config_path = Path(__file__).parent / 'config.json'
    
    if not config_path.exists():
        print("[WARNING]  Configuration file does not exist, will use default configuration")
        return True
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("[OK] Configuration file format is correct")
        
        # Check required fields
        required_fields = ['claude_code_path', 'email']
        for field in required_fields:
            if field not in config:
                print(f"[WARNING]  Configuration file missing field: {field}")
        
        # Check email configuration
        email_config = config.get('email', {})
        if email_config.get('smtp_username') and email_config.get('smtp_password'):
            print("[OK] Email configuration is set")
        else:
            print("[WARNING]  Email configuration is not complete")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Configuration file format error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Configuration file read error: {e}")
        return False

def test_dependencies():
    """Test Python dependencies"""
    required_packages = ['flask', 'requests']
    
    print("[SEARCH] Checking Python dependencies...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package} is installed")
        except ImportError:
            print(f"[ERROR] {package} is not installed")
            return False
    
    return True

def main():
    """Main test function"""
    print("Starting frontend interface system test...")
    print("=" * 50)
    
    # Test configuration file
    print("\nTesting configuration file...")
    test_config_file()
    
    # Test dependencies
    print("\n[PACKAGE] Testing Python dependencies...")
    if not test_dependencies():
        print("[ERROR] Dependency check failed, please install required packages")
        return
    
    # Test server connection
    print("\n[WEB] Testing server connection...")
    if not test_server_health():
        print("[ERROR] Server connection failed, please ensure server is running")
        print("[INFO] Run 'python app.py' or './start.sh' to start server")
        return
    
    # Test search API
    print("\n[SEARCH] Testing search API...")
    task_id = test_search_api()
    
    # Test task status
    if task_id:
        print("\n[STATUS] Testing task status query...")
        test_task_status(task_id)
    
    print("\n" + "=" * 50)
    print("[OK] Frontend interface system test completed")
    
    # Usage instructions
    print("\n[INFO] Usage Instructions:")
    print("1. Start server: python app.py or ./start.sh")
    print("2. Access interface: http://localhost:5000")
    print("3. Configure email: Edit config.json file")
    print("4. Submit search: Fill form and submit")
    
    print("\n[EMAIL] Email Configuration Reminder:")
    print("- Gmail users need to use app-specific passwords")
    print("- Other email providers please check corresponding SMTP settings")
    print("- Ensure email allows third-party app access")

if __name__ == '__main__':
    main()
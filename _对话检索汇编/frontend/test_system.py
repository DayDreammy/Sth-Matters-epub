#!/usr/bin/env python3
"""
前端界面系统测试脚本
用于验证Web界面和后端API是否正常工作
"""

import json
import requests
import time
import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

def test_server_health():
    """测试服务器健康状态"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ 服务器健康检查通过")
            print(f"   状态: {data.get('status')}")
            print(f"   队列大小: {data.get('queue_size')}")
            print(f"   已完成任务: {data.get('completed_tasks')}")
            return True
        else:
            print(f"❌ 服务器健康检查失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务器: {e}")
        return False

def test_search_api():
    """测试搜索API"""
    try:
        # 测试数据
        test_data = {
            "topic": "测试主题",
            "email": "test@example.com",
            "priority": "normal",
            "formats": "markdown,html",
            "notes": "这是一个测试请求"
        }
        
        print("🔍 测试搜索API...")
        response = requests.post(
            'http://localhost:5000/api/search',
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                task_id = data.get('task_id')
                print(f"✅ 搜索API测试通过")
                print(f"   任务ID: {task_id}")
                return task_id
            else:
                print(f"❌ 搜索API测试失败: {data.get('message')}")
                return None
        else:
            print(f"❌ 搜索API测试失败: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 搜索API测试异常: {e}")
        return None

def test_task_status(task_id):
    """测试任务状态查询"""
    if not task_id:
        return False
        
    try:
        print(f"📊 测试任务状态查询 (ID: {task_id})...")
        response = requests.get(f'http://localhost:5000/api/status/{task_id}', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 任务状态查询成功")
                print(f"   状态: {data.get('status')}")
                print(f"   进度: {data.get('progress')}%")
                print(f"   消息: {data.get('message')}")
                return True
            else:
                print(f"❌ 任务状态查询失败: {data.get('message')}")
                return False
        else:
            print(f"❌ 任务状态查询失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 任务状态查询异常: {e}")
        return False

def test_config_file():
    """测试配置文件"""
    config_path = Path(__file__).parent / 'config.json'
    
    if not config_path.exists():
        print("⚠️  配置文件不存在，将使用默认配置")
        return True
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ 配置文件格式正确")
        
        # 检查必要字段
        required_fields = ['claude_code_path', 'email']
        for field in required_fields:
            if field not in config:
                print(f"⚠️  配置文件缺少字段: {field}")
        
        # 检查邮件配置
        email_config = config.get('email', {})
        if email_config.get('smtp_username') and email_config.get('smtp_password'):
            print("✅ 邮件配置已设置")
        else:
            print("⚠️  邮件配置未完整设置")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置文件读取错误: {e}")
        return False

def test_dependencies():
    """测试Python依赖"""
    required_packages = ['flask', 'requests']
    
    print("🔍 检查Python依赖...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始前端界面系统测试...")
    print("=" * 50)
    
    # 测试配置文件
    print("\n📋 测试配置文件...")
    test_config_file()
    
    # 测试依赖
    print("\n📦 测试Python依赖...")
    if not test_dependencies():
        print("❌ 依赖检查失败，请安装所需包")
        return
    
    # 测试服务器连接
    print("\n🌐 测试服务器连接...")
    if not test_server_health():
        print("❌ 服务器连接失败，请确保服务器正在运行")
        print("💡 运行 'python app.py' 或 './start.sh' 启动服务器")
        return
    
    # 测试搜索API
    print("\n🔍 测试搜索API...")
    task_id = test_search_api()
    
    # 测试任务状态
    if task_id:
        print("\n📊 测试任务状态查询...")
        test_task_status(task_id)
    
    print("\n" + "=" * 50)
    print("✅ 前端界面系统测试完成")
    
    # 使用说明
    print("\n💡 使用说明:")
    print("1. 启动服务器: python app.py 或 ./start.sh")
    print("2. 访问界面: http://localhost:5000")
    print("3. 配置邮件: 编辑 config.json 文件")
    print("4. 提交搜索: 填写表单并提交")
    
    print("\n📧 邮件配置提醒:")
    print("- Gmail用户需要使用应用专用密码")
    print("- 其他邮箱请查看对应的SMTP设置")
    print("- 确保邮箱允许第三方应用访问")

if __name__ == '__main__':
    main()
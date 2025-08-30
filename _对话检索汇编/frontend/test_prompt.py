#!/usr/bin/env python3
"""
测试prompt构建
"""

import os
import sys
sys.path.append('.')

from app import SearchEngine

# 创建搜索引擎实例
search_engine = SearchEngine()

# 测试命令构建
topic = '测试主题'
formats = ['markdown', 'html', 'epub']

# 模拟命令构建
target_dir = str(search_engine.base_dir.parent).replace('\\', '/')
claude_md_path = str(search_engine.base_dir.parent.parent / 'CLAUDE.md').replace('\\', '/')
prompt = f'{topic},output formats:{formats}'

cmd = [
    search_engine.claude_code_path,
    '-p',
    f'"{prompt}"',
    '--output-format', 'json',
    '--allowed-tools', 'Bash,Read,Write,Glob,Grep,Task',
    '--add-dir', '_对话检索汇编'  # 使用相对路径，工作目录将在项目根目录
]

print('构建的命令:')
print(' '.join(cmd))
print(f'\nPrompt内容: {prompt}')
print(f'CLAUDE.md路径: {claude_md_path}')
print(f'目标目录: {target_dir}')
print(f'工作目录: {search_engine.base_dir.parent.parent}')
print(f'相对路径: _对话检索汇编')

# 检查CLAUDE.md文件是否存在
if os.path.exists(claude_md_path):
    print(f'\n[OK] CLAUDE.md文件存在: {claude_md_path}')
    with open(claude_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f'文件内容长度: {len(content)} 字符')
        print('文件前200字符:')
        print(content[:200])
else:
    print(f'\n[ERROR] CLAUDE.md文件不存在: {claude_md_path}')
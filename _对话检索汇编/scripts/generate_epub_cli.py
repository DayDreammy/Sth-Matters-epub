#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB生成器命令行工具
根据JSON索引文件生成EPUB格式的电子书
"""

import sys
import os
import argparse
from datetime import datetime

# 导入EPUB生成器类
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from generate_epub import SocializationEPUBGenerator


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='根据JSON索引文件生成EPUB电子书',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python generate_epub_cli.py -i 索引文件.json -o 输出目录
  python generate_epub_cli.py -i 索引文件.json -o 输出目录 -t 自定义书名
        '''
    )
    
    parser.add_argument(
        '-i', '--index',
        required=True,
        help='JSON索引文件路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='输出目录路径'
    )
    
    parser.add_argument(
        '-t', '--title',
        help='自定义书名（默认使用JSON中的主题）'
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    index_file = args.index
    output_dir = args.output
    custom_title = args.title
    
    try:
        # 创建生成器
        generator = SocializationEPUBGenerator(index_file)
        
        # 如果有自定义书名，更新索引数据
        if custom_title:
            generator.index_data['metadata']['topic'] = custom_title
        
        # 生成EPUB文件名
        topic_name = generator.index_data['metadata']['topic']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f'{topic_name}_{timestamp}.epub')
        
        # 生成EPUB文件
        print(f'正在生成EPUB文件: {topic_name}')
        generator.generate_epub(output_file)
        
        print('EPUB文件生成完成!')
        print(f'输出文件: {output_file}')
        print('现在可以将此文件导入到微信读书、Apple Books等电子书阅读器中阅读了！')
        
    except Exception as e:
        print(f'生成EPUB文件时发生错误: {e}')
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
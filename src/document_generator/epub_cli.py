import sys
import os
import argparse
from datetime import datetime

# 确保可以从父目录导入
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_generator.epub_generator import EPUBDocumentGenerator


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='根据JSON索引文件生成EPUB电子书',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python epub_cli.py -i /path/to/index.json -o /path/to/output -k /path/to/kb
  python epub_cli.py -i /path/to/index.json -o /path/to/output -k /path/to/kb -t "自定义书名"
        '''
    )
    
    parser.add_argument(
        '-i', '--index',
        required=True,
        help='JSON索引文件路径'
    )

    parser.add_argument(
        '-k', '--kb-dir',
        required=True,
        help='知识库根目录路径'
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
    args = parse_arguments()
    
    try:
        # 创建生成器
        generator = EPUBDocumentGenerator(args.index, args.kb_dir)
        
        # 如果有自定义书名，更新索引数据
        if args.title:
            generator.index_data['metadata']['topic'] = args.title
        
        # 生成EPUB文件名
        topic_name = generator.index_data['metadata']['topic']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(args.output, f'{topic_name}_{timestamp}.epub')
        
        # 生成EPUB文件
        print(f'正在生成EPUB文件: {topic_name}')
        generator.generate_epub(output_file)
        
        print('EPUB文件生成完成!')
        print(f'输出文件: {output_file}')
        
    except Exception as e:
        print(f'生成EPUB文件时发生错误: {e}')
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

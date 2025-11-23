import os
import sys
import glob

# 将src目录添加到Python路径中
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import KnowledgeSearchInterface

def run_evaluation():
    """
    执行评估测试，验证重构后的代码是否能正常工作。
    """
    print("="*20)
    print("开始执行重构后代码评估...")
    print("="*20)

    # --- 配置 ---
    test_topic = "社会化"
    test_email = "eval@example.com"
    project_root = os.path.dirname(__file__)
    output_dir = os.path.join(project_root, "output")
    
    # --- 模拟Gradio进度条 ---
    class MockProgress:
        def __call__(self, progress, desc=""):
            print(f"进度: {progress*100:.0f}%, 描述: {desc}")

    # --- 执行核心功能 ---
    try:
        print(f"1. 初始化 KnowledgeSearchInterface...")
        interface = KnowledgeSearchInterface()
        print("   初始化成功。")

        print(f"2. 调用 search_and_send 方法...")
        print(f"   主题: {test_topic}")
        print(f"   邮箱: {test_email}")
        result_message = interface.search_and_send(test_topic, test_email, progress=MockProgress())
        print("\n   search_and_send 方法返回信息:")
        print("-" * 15)
        print(result_message)
        print("-" * 15)

    except Exception as e:
        print(f"\n❌ 在执行过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
        return False

    # --- 验证产出 ---
    print("\n3. 验证输出文件...")
    
    # 清理旧的评估文件（如果存在）
    for f in glob.glob(os.path.join(output_dir, f"*{test_topic}*")):
        # os.remove(f)
        pass # 暂时不删除，方便调试

    # 查找生成的文件
    md_files = glob.glob(os.path.join(output_dir, f"*{test_topic}*.md"))
    html_files = glob.glob(os.path.join(output_dir, f"*{test_topic}*.html"))
    epub_files = glob.glob(os.path.join(output_dir, f"*{test_topic}*.epub"))

    # 检查文件是否存在
    md_ok = len(md_files) > 0
    html_ok = len(html_files) > 0
    epub_ok = len(epub_files) > 0

    print(f"   - 检查 Markdown (.md) 文件: {'✅' if md_ok else '❌'}")
    print(f"   - 检查 HTML (.html) 文件:    {'✅' if html_ok else '❌'}")
    print(f"   - 检查 EPUB (.epub) 文件:     {'✅' if epub_ok else '❌'}")

    if not (md_ok and html_ok and epub_ok):
        print("\n[评估失败]: 未能生成所有必需的文档格式。")
        return False

    # 检查文件是否包含内容（带原文）
    def file_has_content(file_path):
        return os.path.getsize(file_path) > 1024  # 假设文件大于1KB则认为有内容

    md_content_ok = file_has_content(md_files[0])
    html_content_ok = file_has_content(html_files[0])
    epub_content_ok = file_has_content(epub_files[0])

    print("\n4. 验证文件内容...")
    print(f"   - 检查 Markdown 文件内容: {'.md 文件 > 1KB' if md_content_ok else '❌ .md 文件过小或为空'}")
    print(f"   - 检查 HTML 文件内容:    {'.html 文件 > 1KB' if html_content_ok else '❌ .html 文件过小或为空'}")
    print(f"   - 检查 EPUB 文件内容:     {'.epub 文件 > 1KB' if epub_content_ok else '❌ .epub 文件过小或为空'}")

    if not (md_content_ok and html_content_ok and epub_content_ok):
        print("\n[评估失败]: 一个或多个文件内容过小，可能未包含原文。")
        return False

    print("\n" + "="*20)
    print("✅ 评估通过！所有检查项均符合预期。")
    print("="*20)
    return True

if __name__ == "__main__":
    if not run_evaluation():
        sys.exit(1)

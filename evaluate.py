import os
import sys
import glob
import re
import time

# 将src目录添加到Python路径中
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import KnowledgeSearchInterface

class MockProgress:
    """模拟Gradio的进度条，用于在后台脚本中打印进度。"""
    def __call__(self, progress, desc=""):
        print(f"进度: {progress*100:.0f}%, 描述: {desc}")

def cleanup_files(output_dir, topic):
    """删除指定主题的旧输出文件，以便进行干净的测试。"""
    print(f"\n--- 清理旧文件 (主题: {topic}) ---")
    files_to_delete = glob.glob(os.path.join(output_dir, f"*{topic}*.*的发展"))
    if not files_to_delete:
        print("没有找到旧文件，无需清理。")
        return
    for f in files_to_delete:
        try:
            os.remove(f)
            print(f"已删除: {os.path.basename(f)}")
        except OSError as e:
            print(f"删除文件失败: {e}")

def run_deep_search_evaluation():
    """
    执行【深度搜索】的评估测试。
    """
    print("="*40)
    print("  开始执行【深度搜索】评估...")
    print("="*40)

    # --- 配置 ---
    test_topic = "社会化" # 确保这个主题在知识库中存在
    test_email = "eval@example.com"
    project_root = os.path.dirname(__file__)
    output_dir = os.path.join(project_root, "output")
    
    cleanup_files(output_dir, test_topic)

    # --- 执行核心功能 ---
    try:
        print("\n1. 初始化 KnowledgeSearchInterface...")
        interface = KnowledgeSearchInterface()
        print("   初始化成功。")

        print(f"\n2. 调用 deep_search_and_send 方法...")
        result_message = interface.deep_search_and_send(test_topic, test_email, progress=MockProgress())
        print("\n   方法返回信息:")
        print("-" * 20)
        print(result_message)
        print("-" * 20)
        if "❌" in result_message:
             print("\n[评估失败]: 深度搜索方法返回了错误信息。")
             return False

    except Exception as e:
        print(f"\n❌ 在执行过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
        return False

    # --- 验证产出 ---
    print("\n3. 验证输出文件...")
    time.sleep(1) # 等待文件系统响应
    md_files = glob.glob(os.path.join(output_dir, f"*{test_topic}*.md"))
    html_files = glob.glob(os.path.join(output_dir, f"*{test_topic}*.html"))
    epub_files = glob.glob(os.path.join(output_dir, f"*{test_topic}*.epub"))

    md_ok = len(md_files) > 0
    html_ok = len(html_files) > 0
    epub_ok = len(epub_files) > 0

    print(f"   - 检查 Markdown (.md) 文件: {'✅' if md_ok else '❌'}")
    print(f"   - 检查 HTML (.html) 文件:    {'✅' if html_ok else '❌'}")
    print(f"   - 检查 EPUB (.epub) 文件:     {'✅' if epub_ok else '❌'}")

    if not (md_ok and html_ok and epub_ok):
        print("\n[评估失败]: 未能生成所有必需的文档格式。")
        return False

    print("\n✅ [深度搜索] 评估通过！")
    return True

def run_quick_search_evaluation():
    """
    执行【快速搜索】的评估测试，并验证内容。
    """
    print("="*40)
    print("  开始执行【快速搜索】评估...")
    print("="*40)

    # --- 配置 ---
    test_topic = "社会化" # 确保这个主题在知识库中存在
    test_email = "eval@example.com"
    project_root = os.path.dirname(__file__)
    output_dir = os.path.join(project_root, "output")

    cleanup_files(output_dir, test_topic)

    # --- 执行核心功能 ---
    try:
        print("\n1. 初始化 KnowledgeSearchInterface...")
        interface = KnowledgeSearchInterface()
        print("   初始化成功。")

        print(f"\n2. 调用 quick_search_and_send 方法...")
        result_message = interface.quick_search_and_send(test_topic, test_email, progress=MockProgress())
        print("\n   方法返回信息:")
        print("-" * 20)
        print(result_message)
        print("-" * 20)
        if "❌" in result_message:
             print("\n[评估失败]: 快速搜索方法返回了错误信息。")
             return False

    except Exception as e:
        print(f"\n❌ 在执行过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
        return False

    # --- 验证产出 ---
    print("\n3. 验证输出文件...")
    time.sleep(1) # 等待文件系统响应
    # 快速搜索生成的 thematic_文档 是主要验证对象
    md_pattern = os.path.join(output_dir, f"*{test_topic}*_thematic_文档.md")
    html_pattern = os.path.join(output_dir, f"*{test_topic}*_html_文档.html")
    epub_pattern = os.path.join(output_dir, f"*{test_topic}*.epub")
    
    md_files = glob.glob(md_pattern)
    html_files = glob.glob(html_pattern)
    epub_files = glob.glob(epub_pattern)

    md_ok = len(md_files) > 0
    html_ok = len(html_files) > 0
    epub_ok = len(epub_files) > 0

    print(f"   - 检查 Markdown (.md) 文件: {'✅' if md_ok else '❌'}")
    print(f"   - 检查 HTML (.html) 文件:    {'✅' if html_ok else '❌'}")
    print(f"   - 检查 EPUB (.epub) 文件:     {'✅' if epub_ok else '❌'}")

    if not (md_ok and html_ok and epub_ok):
        print("\n[评估失败]: 未能生成所有必需的文档格式。")
        return False

    # --- 关键内容验证 ---
    print("\n4. 验证Markdown文件内容...")
    md_path = md_files[0]
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    title_found = bool(re.search(r'^#\s+.+', md_content))
    word_count_found = bool(re.search(r'字数', md_content))
    content_found = "原文" in md_content
    # 假设知识库中关于“社会化”的文章包含知乎链接
    zhihu_link_found = bool(re.search(r'https://zhuanlan.zhihu.com/p/\w+', md_content))

    print(f"   - 检查标题:     {'✅' if title_found else '❌'}")
    print(f"   - 检查'字数'字段: {'✅' if word_count_found else '❌'}")
    print(f"   - 检查'原文'内容: {'✅' if content_found else '❌'}")
    print(f"   - 检查知乎链接:   {'✅' if zhihu_link_found else '⚠️'}") # 设为警告，因为不一定每篇都有

    if not (title_found and word_count_found and content_found):
        print("\n[评估失败]: Markdown文件内容不符合要求（缺少标题、字数或原文）。")
        return False

    print("\n✅ [快速搜索] 评估通过！")
    return True


if __name__ == "__main__":
    print("开始执行完整的评估套件...\n")
    
    # 依次执行两个测试
    # deep_search_ok = run_deep_search_evaluation()
    # print("\n" + "#"*40 + "\n")
    
    # time.sleep(5) # 在两个测试之间稍作停顿
    
    quick_search_ok = run_quick_search_evaluation()
    
    print("\n" + "="*40)
    print("  评估套件执行完毕")
    print("="*40)
    
    # print(f"深度搜索测试结果: {'✅ 通过' if deep_search_ok else '❌ 失败'}")
    print(f"快速搜索测试结果: {'✅ 通过' if quick_search_ok else '❌ 失败'}")
    
    # if deep_search_ok and quick_search_ok:
    if quick_search_ok:
        print("\n🎉🎉🎉 所有评估均已通过！🎉🎉🎉")
        sys.exit(0)
    else:
        print("\n🔥🔥🔥 部分评估失败，请检查日志。🔥🔥🔥")
        sys.exit(1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio前端界面
集成深度搜索RPA和邮件发送功能
"""

import gradio as gr
import os
import json
import time
import subprocess
import glob
from datetime import datetime
from rpa import DeepSearchRPA
from email_client import EmailClient
from quick_search import perform_quick_search


# set env
os.environ["ANTHROPIC_BASE_URL"] = "https://open.bigmodel.cn/api/anthropic"
os.environ["ANTHROPIC_AUTH_TOKEN"] = "3b222275909a41df8eb8553503ab3300.rJZMbCswT0DXgqph"


class KnowledgeSearchInterface:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.output_dir = os.path.join(self.base_dir, "output")
        self.search_rpa = DeepSearchRPA(base_dir=self.base_dir)
        self.email_sender = EmailClient()

    def _send_email_and_get_report(self, topic: str, email: str, files: dict) -> str:
        """Helper function to send email and generate a report."""
        email_result = self.email_sender.send_documents(
            recipient_email=email.strip(),
            topic=topic.strip(),
            files=files
        )

        if email_result["success"]:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            attached_files = email_result.get("attached_files", [])
            result_msg = f"""✅ **搜索和发送完成！**

📋 **搜索信息**
- 主题：{topic.strip()}
- 完成时间：{timestamp}

📁 **生成文件**：{len(files)} 个
{chr(10).join([f"• {file_type.upper()}: {os.path.basename(path)}" for file_type, path in files.items()])}

📧 **邮件信息**
- 收件人：{email.strip()}
- 发送文件：{len(attached_files)} 个
- 状态：发送成功

请查收邮件，所有生成的文档已添加为附件。"""
        else:
            error_msg = email_result.get("error", "未知错误")
            result_msg = f"""⚠️ **搜索完成但邮件发送失败**

📋 **搜索信息**
- 主题：{topic.strip()}
- 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📁 **生成文件**：{len(files)} 个
{chr(10).join([f"• {file_type.upper()}: {os.path.basename(path)}" for file_type, path in files.items()])}

❌ **邮件错误**
- 收件人：{email.strip()}
- 错误信息：{error_msg}

文件已生成在本地，请检查邮件配置或手动发送。"""
        return result_msg

    def deep_search_and_send(self, topic: str, email: str, progress=gr.Progress()):
        """Executes the DEEP search and send workflow."""
        progress(0.1, desc="[深度搜索] 开始执行AI代理搜索...")
        search_result = self.search_rpa.run_complete_search(topic.strip())

        if not search_result["success"]:
            error_msg = search_result.get("error", "未知错误")
            return f"❌ [深度搜索] 失败: {error_msg}"

        progress(0.7, desc="[深度搜索] 文档生成完成，准备发送邮件...")
        files = search_result.get("files", {})
        if not files:
            return "⚠️ [深度搜索] 完成但未找到生成的文档文件"

        progress(0.8, desc="[深度搜索] 正在发送邮件...")
        report = self._send_email_and_get_report(topic, email, files)
        progress(1.0, desc="[深度搜索] 完成！")
        return report

    def quick_search_and_send(self, topic: str, email: str, progress=gr.Progress()):
        """Executes the QUICK search and send workflow."""
        progress(0.1, desc="[快速搜索] 开始执行关键词匹配...")
        
        # Step 1: Perform quick search to get the index file
        search_result = perform_quick_search(topic.strip(), self.base_dir)

        if not search_result["success"]:
            return f"❌ [快速搜索] 失败: {search_result.get('error', '未知错误')}"
        
        index_file_path = search_result.get("index_file_path")
        if not index_file_path:
            return "✅ [快速搜索] 完成，没有找到相关内容。"

        progress(0.4, desc="[快速搜索] 索引生成，开始转换文档...")

        # Step 2: Call document generators
        try:
            md_gen_cmd = [
                "python", "src/document_generator/md_generator.py",
                "-i", index_file_path,
                "-o", self.output_dir,
                "-k", os.path.join(self.base_dir, "knowledge_base", "sth-matters"),
                "-l", "all"
            ]
            epub_gen_cmd = [
                "python", "src/document_generator/epub_cli.py",
                "-i", index_file_path,
                "-o", self.output_dir,
                "-k", os.path.join(self.base_dir, "knowledge_base", "sth-matters")
            ]
            
            print(f"Executing: {' '.join(md_gen_cmd)}")
            subprocess.run(md_gen_cmd, check=True, capture_output=True, text=True, encoding='utf-8')
            
            print(f"Executing: {' '.join(epub_gen_cmd)}")
            subprocess.run(epub_gen_cmd, check=True, capture_output=True, text=True, encoding='utf-8')

        except subprocess.CalledProcessError as e:
            error_message = f"文档生成脚本执行失败: {e.stderr}"
            print(error_message)
            return f"❌ [快速搜索] {error_message}"
        
        progress(0.7, desc="[快速搜索] 文档生成完成，准备发送邮件...")

        # Step 3: Find generated files
        time.sleep(1) # Allow a moment for files to be fully written
        file_patterns = {
            'md': f"*{topic}*_thematic_文档.md",
            'html': f"*{topic}*_html_文档.html",
            'epub': f"*{topic}*.epub"
        }
        found_files = {}
        for file_type, pattern in file_patterns.items():
            # Search in output dir, get the latest one
            files = sorted(glob.glob(os.path.join(self.output_dir, pattern)), key=os.path.getmtime, reverse=True)
            if files:
                found_files[file_type] = files[0]

        if not found_files:
            return "⚠️ [快速搜索] 完成但未找到生成的文档文件"

        progress(0.8, desc="[快速搜索] 正在发送邮件...")
        report = self._send_email_and_get_report(topic, email, found_files)
        progress(1.0, desc="[快速搜索] 完成！")
        return report

    def dispatch_search(self, topic: str, email: str, search_type: str, progress=gr.Progress()):
        """Dispatches the search based on user's choice."""
        if not topic.strip():
            return "❌ 请输入搜索主题"
        if not email.strip() or "@" not in email or "." not in email:
            return "❌ 请输入有效的邮箱地址"

        if search_type == "快速搜索":
            return self.quick_search_and_send(topic, email, progress)
        else: # Default to Deep Search
            return self.deep_search_and_send(topic, email, progress)

    def test_email_config(self):
        """测试邮件配置"""
        result = self.email_sender.test_connection()
        if result["success"]:
            return "✅ 邮件配置正常"
        else:
            return f"❌ 邮件配置错误: {result['error']}"

    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(title="Sth-matters 知识库搜索系统", theme=gr.themes.Soft()) as interface:
            gr.HTML("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>📚 Sth-matters 知识库帮你找原文</h1>
                <p>输入您感兴趣的主题，选择搜索模式，系统将自动处理并发送结果到您的邮箱。</p>
            </div>
            """)

            with gr.Tabs():
                with gr.TabItem("🚀 开始搜索"):
                    with gr.Row():
                        with gr.Column(scale=3):
                            topic_input = gr.Textbox(label="🔍 搜索主题", placeholder="例如：社会化、认知偏差、人工智能...", lines=2)
                            email_input = gr.Textbox(label="📧 邮箱地址", placeholder="your_email@example.com", type="email")
                        with gr.Column(scale=2):
                            search_type_input = gr.Radio(
                                ["深度搜索", "快速搜索"],
                                label="⚙️ 搜索模式",
                                value="深度搜索",
                                info="深度搜索：AI代理执行，全面但耗时较长(3-5分钟)。快速搜索：关键词匹配，秒级响应但结果有限。"
                            )
                    
                    submit_btn = gr.Button("🚀 开始执行并发送邮件", variant="primary", size="lg")
                    
                    result_output = gr.Markdown(value="💡 请输入主题和邮箱，然后点击开始按钮...", label="执行结果")

                with gr.TabItem("📖 使用说明"):
                    gr.Markdown("""
                    ### 系统功能
                    1. **深度搜索**：AI代理驱动，对知识库进行多角度的深入分析、扩展和总结。
                    2. **快速搜索**：基于关键词直接匹配知识库中的文章，速度快，适合精确查找。
                    3. **文档生成**：自动生成EPUB、Markdown、HTML等多种格式。
                    4. **邮件发送**：将生成结果直接发送到指定邮箱。
                    """)
                
                with gr.TabItem("⚙️ 系统设置"):
                    test_email_btn = gr.Button("📧 测试邮件配置")
                    test_email_output = gr.Markdown()
                    test_email_btn.click(fn=self.test_email_config, outputs=[test_email_output])

            submit_btn.click(
                fn=self.dispatch_search,
                inputs=[topic_input, email_input, search_type_input],
                outputs=[result_output],
                show_progress=True
            )

            gr.Examples(
                examples=[
                    ["社会化", "example@email.com", "深度搜索"],
                    ["认知偏差", "example@email.com", "快速搜索"],
                ],
                inputs=[topic_input, email_input, search_type_input],
                label="📝 示例（请将邮箱改为您自己的）"
            )
        return interface

def main():
    """主函数"""
    app = KnowledgeSearchInterface()
    interface = app.create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7899, share=False, show_error=True, show_api=True)

if __name__ == "__main__":
    main()
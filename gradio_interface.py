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
from datetime import datetime
from deep_search_rpa import DeepSearchRPA
from email_sender import EmailSender


# set env
os.environ["ANTHROPIC_BASE_URL"] = "https://open.bigmodel.cn/api/anthropic"
os.environ["ANTHROPIC_AUTH_TOKEN"] = "3b222275909a41df8eb8553503ab3300.rJZMbCswT0DXgqph"


class KnowledgeSearchInterface:
    def __init__(self):
        self.search_rpa = DeepSearchRPA()
        self.email_sender = EmailSender()

    def search_and_send(self, topic: str, email: str, progress=gr.Progress()):
        """
        执行搜索并发送邮件的完整流程

        Args:
            topic: 搜索主题
            email: 收件邮箱
            progress: Gradio进度条

        Returns:
            str: 执行结果信息
        """
        if not topic.strip():
            return "❌ 请输入搜索主题"

        if not email.strip():
            return "❌ 请输入邮箱地址"

        if "@" not in email or "." not in email:
            return "❌ 请输入有效的邮箱地址"

        progress(0.1, desc="开始执行深度搜索...")

        # 第一步：执行深度搜索
        search_result = self.search_rpa.run_complete_search(topic.strip())

        if not search_result["success"]:
            error_msg = search_result.get("error", "未知错误")
            return f"❌ 深度搜索失败: {error_msg}"

        progress(0.7, desc="文档生成完成，准备发送邮件...")

        # 第二步：发送邮件
        files = search_result["files"]
        if not files:
            return "⚠️ 搜索完成但未找到生成的文档文件"

        progress(0.8, desc="正在发送邮件...")
        email_result = self.email_sender.send_documents(
            recipient_email=email.strip(),
            topic=topic.strip(),
            files=files
        )

        progress(1.0, desc="完成！")

        # 生成结果报告
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

    def test_email_config(self):
        """测试邮件配置"""
        result = self.email_sender.test_connection()
        if result["success"]:
            return "✅ 邮件配置正常"
        else:
            return f"❌ 邮件配置错误: {result['error']}"

    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(
            title="Sth-matters 知识库搜索系统",
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {
                max-width: 800px !important;
                margin: auto !important;
            }
            .main-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .info-box {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
            """
        ) as interface:

            # 标题和说明
            gr.HTML("""
            <div class="main-header">
                <h1>📚 Sth-matters 知识库帮你找原文</h1>
                <p>输入您感兴趣的主题，系统将自动进行深度搜索并生成多种格式的学习文档，然后发送到您的邮箱。</p>
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 15px 0;">
                    <p style="margin: 0; color: #856404;">
                        <strong>⏰ 温馨提示：</strong>深度搜索分析需要较长时间（约3-5分钟），成功后会自动发送到您的邮箱。提交后您可以先去忙其他事情，完成后查收邮件即可！
                    </p>
                </div>
            </div>
            """)

            # 使用说明
            with gr.Accordion("📖 使用说明", open=False):
                gr.Markdown("""
                ### 系统功能
                1. **深度搜索**：基于中文知识库进行多角度深度分析
                2. **文档生成**：自动生成EPUB、Markdown、HTML等多种格式
                3. **邮件发送**：将生成结果直接发送到指定邮箱

                ### 使用步骤
                1. 在下方输入框中输入您感兴趣的主题或问题
                2. 输入您的邮箱地址
                3. 点击"开始搜索并发送"按钮
                4. 等待系统完成处理，查收邮件即可

                ### 输入建议
                - 可以输入具体概念、理论、人物、事件等
                - 支持中英文混合输入
                - 建议使用简洁明确的表述
                """)

            # 主要输入区域
            with gr.Row():
                with gr.Column(scale=3):
                    topic_input = gr.Textbox(
                        label="🔍 搜索主题",
                        placeholder="例如：社会化、认知偏差、人工智能、商业模式等...",
                        lines=2,
                        max_lines=4
                    )

                with gr.Column(scale=2):
                    email_input = gr.Textbox(
                        label="📧 邮箱地址",
                        placeholder="your_email@example.com",
                        type="email"
                    )

            # 操作按钮
            with gr.Row():
                submit_btn = gr.Button(
                    "🚀 开始搜索并发送",
                    variant="primary",
                    size="lg",
                    scale=2
                )
                test_email_btn = gr.Button(
                    "📧 测试邮件配置",
                    variant="secondary",
                    size="lg"
                )

            # 操作提示
            gr.HTML("""
            <div style="text-align: center; margin: 10px 0; color: #666;">
                <p style="margin: 0; font-size: 0.9em;">
                    💡 提交后将开始深度搜索，请耐心等待3-5分钟，完成后会自动发送到您的邮箱
                </p>
            </div>
            """)

            # 结果显示区域
            result_output = gr.Markdown(
                value="💡 请输入主题和邮箱，然后点击开始按钮...",
                label="执行结果"
            )

            # 状态信息
            with gr.Accordion("ℹ️ 系统信息", open=False):
                gr.Markdown("""
                ### 系统状态
                - 深度搜索引擎：✅ 正常
                - 文档生成器：✅ 正常
                - 邮件发送器：待测试

                ### 支持的文档格式
                - **EPUB电子书**：适合微信读书等移动端阅读
                - **Markdown文档**：主题分类、概念分析、来源分组、内容概要
                - **HTML文档**：网页格式，支持交互式导航

                ### 注意事项
                - 单次搜索大约需要5-15分钟
                - 请确保邮箱地址正确
                - 大文件可能需要几分钟才能收到
                """)

            # 事件绑定
            submit_btn.click(
                fn=self.search_and_send,
                inputs=[topic_input, email_input],
                outputs=[result_output],
                show_progress=True
            )

            test_email_btn.click(
                fn=self.test_email_config,
                outputs=[result_output]
            )

            # 示例
            gr.Examples(
                examples=[
                    ["社会化", "example@email.com"],
                    ["认知偏差", "example@email.com"],
                    ["商业模式创新", "example@email.com"],
                    ["人工智能伦理", "example@email.com"],
                    ["系统思维", "example@email.com"]
                ],
                inputs=[topic_input, email_input],
                label="📝 示例（请将邮箱改为您自己的）"
            )

        return interface


def main():
    """主函数"""
    app = KnowledgeSearchInterface()
    interface = app.create_interface()

    interface.launch(
        server_name="0.0.0.0",
        server_port=7899,
        share=False,
        show_error=True,
        show_api=True
    )


if __name__ == "__main__":
    main()

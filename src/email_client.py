#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送脚本
支持SMTP发送生成的文档文件到指定邮箱
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional
import json
from datetime import datetime
from logger import get_logger


class EmailClient:
    def __init__(self, config_file: str = None):
        """
        初始化邮件发送器

        Args:
            config_file: 邮件配置文件路径
        """
        if config_file is None:
            # 默认配置文件路径在项目根目录的config文件夹下
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.config_file = os.path.join(base_dir, "config", "email_config.json")
        else:
            self.config_file = config_file

        # 初始化日志记录器
        self.logger = get_logger("EmailClient")
        self.logger.info(f"EmailClient 初始化完成，配置文件: {self.config_file}")

        self.config = self.load_config()

    def load_config(self) -> Dict:
        """
        加载邮件配置

        Returns:
            Dict: 配置信息
        """
        default_config = {
            "smtp_server": "smtp.163.com",
            "smtp_port": 465,
            "sender_email": "daydreammy@163.com",
            "sender_password": "NUYQEBJEHZRHGLSI",
            "sender_name": "知识库搜索系统"
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置和用户配置
                default_config.update(config)
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {e}")
        else:
            # 创建默认配置文件
            self.save_config(default_config)
            print(f"已创建默认配置文件: {self.config_file}")
            print("请编辑配置文件中的邮件服务器信息")

        return default_config

    def save_config(self, config: Dict):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def send_documents(self, recipient_email: str, topic: str, files: Dict[str, str]) -> Dict[str, any]:
        """
        发送文档到指定邮箱

        Args:
            recipient_email: 收件人邮箱
            topic: 搜索主题
            files: 文件路径字典 {文件类型: 文件路径}

        Returns:
            Dict: 发送结果
        """
        if not files:
            return {
                "success": False,
                "error": "没有找到要发送的文件"
            }

        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"知识库搜索结果 - {topic} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            # 邮件正文
            body = f"""
您好！

您的9a知识库深度搜索已完成，以下是搜索结果详情：

搜索主题：{topic}
完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
生成文件数量：{len(files)}

文件列表：
"""

            for file_type, file_path in files.items():
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path) / 1024  # KB
                    body += f"- {file_name} ({file_type.upper()}, {file_size:.0f}KB)\n"
                else:
                    body += f"- {file_type.upper()} 文件 (文件不存在)\n"

            body += """
这些文件包含了您搜索主题的深度分析结果，包括：
- EPUB电子书（适合移动端阅读）

如有任何问题，请联系 Daydreammy.

祝你健康、平安、喜乐，有信心、有成果、有收获！
Sth-matters 知识库搜索系统
"""

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加附件
            attached_files = []
            for file_type, file_path in files.items():
                if os.path.exists(file_path):
                    try:
                        # 根据文件扩展名设置正确的MIME类型
                        file_ext = os.path.splitext(file_path)[1].lower()
                        file_name = os.path.basename(file_path)

                        if file_ext == '.epub':
                            mime_type = 'application/epub+zip'
                        elif file_ext == '.pdf':
                            mime_type = 'application/pdf'
                        elif file_ext == '.html':
                            mime_type = 'text/html'
                        elif file_ext == '.md':
                            mime_type = 'text/markdown'
                        elif file_ext in ['.txt', '.log']:
                            mime_type = 'text/plain'
                        else:
                            mime_type = 'application/octet-stream'

                        # 添加附件
                        with open(file_path, "rb") as attachment:
                            # 1. 根据主类型和子类型创建 part
                            main_type, sub_type = mime_type.split('/', 1)
                            part = MIMEBase(main_type, sub_type)

                            # 2. 设置附件内容
                            part.set_payload(attachment.read())

                        # 3. 对内容进行 Base64 编码
                        encoders.encode_base64(part)

                        # 4. 设置标准的 Content-Disposition 头（使用关键字参数）
                        part.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=file_name
                        )

                        # 5. 移除多余的 Content-Type 头（已删除）

                        msg.attach(part)
                        attached_files.append(file_name)
                        print(f"已添加附件: {file_name} ({mime_type})")

                    except Exception as e:
                        print(f"添加附件失败 {file_path}: {e}")

            # 发送邮件 (163邮箱使用SSL)
            if self.config['smtp_port'] == 465:
                # SSL连接
                print("正在建立SSL连接...")
                with smtplib.SMTP_SSL(
                    self.config['smtp_server'],
                    self.config['smtp_port'],
                    timeout=60  # 60秒超时
                ) as server:
                    print("正在登录邮件服务器...")
                    server.login(
                        self.config['sender_email'],
                        self.config['sender_password']
                    )
                    print("正在发送邮件...")
                    text = msg.as_string()
                    server.sendmail(
                        self.config['sender_email'],
                        recipient_email,
                        text
                    )
            else:
                # 普通连接 + STARTTLS
                print("正在建立SMTP连接...")
                with smtplib.SMTP(
                    self.config['smtp_server'],
                    self.config['smtp_port'],
                    timeout=60  # 60秒超时
                ) as server:
                    print("启用安全传输...")
                    server.starttls()  # 启用安全传输
                    print("正在登录邮件服务器...")
                    server.login(
                        self.config['sender_email'],
                        self.config['sender_password']
                    )
                    print("正在发送邮件...")
                    text = msg.as_string()
                    server.sendmail(
                        self.config['sender_email'],
                        recipient_email,
                        text
                    )

            return {
                "success": True,
                "recipient": recipient_email,
                "topic": topic,
                "attached_files": attached_files,
                "total_files": len(attached_files)
            }

        except smtplib.SMTPAuthenticationError as e:
            return {
                "success": False,
                "error": f"SMTP认证失败: {str(e)} - 请检查邮箱和授权码"
            }
        except smtplib.SMTPConnectError as e:
            return {
                "success": False,
                "error": f"SMTP连接错误: {str(e)} - 无法连接到邮件服务器"
            }
        except smtplib.SMTPServerDisconnected as e:
            return {
                "success": False,
                "error": f"SMTP服务器断开连接: {str(e)} - 可能是网络问题或附件太大"
            }
        except smtplib.SMTPDataError as e:
            return {
                "success": False,
                "error": f"SMTP数据错误: {str(e)} - 可能是附件格式或大小问题"
            }
        except smtplib.SMTPRecipientsRefused as e:
            return {
                "success": False,
                "error": f"收件人被拒绝: {str(e)} - 请检查收件人邮箱地址"
            }
        except smtplib.SMTPResponseException as e:
            return {
                "success": False,
                "error": f"SMTP响应错误: {str(e)}"
            }
        except TimeoutError as e:
            return {
                "success": False,
                "error": f"邮件发送超时: {str(e)} - 可能是附件太大或网络超时"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"发送邮件时出现未知错误: {str(e)}"
            }

    def test_connection(self) -> Dict[str, any]:
        """
        测试邮件服务器连接

        Returns:
            Dict: 测试结果
        """
        try:
            if self.config['smtp_port'] == 465:
                # SSL连接
                with smtplib.SMTP_SSL(self.config['smtp_server'], self.config['smtp_port']) as server:
                    server.login(
                        self.config['sender_email'], self.config['sender_password'])
            else:
                # 普通连接 + STARTTLS
                with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                    server.starttls()
                    server.login(
                        self.config['sender_email'], self.config['sender_password'])
            return {
                "success": True,
                "message": "邮件服务器连接成功"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"连接失败: {str(e)}"
            }


if __name__ == "__main__":
    # 测试代码
    sender = EmailSender()

    # 测试连接
    print("=== 测试邮件连接 ===")
    test_result = sender.test_connection()
    print(json.dumps(test_result, ensure_ascii=False, indent=2))

    # 示例：发送测试邮件
    if test_result["success"]:
        print("\n=== 发送测试邮件 ===")
        test_files = {
            "epub": r"D:\yy\Sth-Matters\_对话检索汇编\generated_docs\面对重大选择的心态与对象选择_20251004_003825.epub",
            "md": r"D:\yy\Sth-Matters\_对话检索汇编\generated_docs\亲密关系中的责任_concepts_文档.md"
        }

        # 检查文件是否存在
        existing_files = {k: v for k,
                          v in test_files.items() if os.path.exists(v)}

        if existing_files:
            result = sender.send_documents(
                recipient_email="1781051483@qq.com",
                topic="测试主题",
                files=existing_files
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("没有找到测试文件，跳过邮件发送测试")

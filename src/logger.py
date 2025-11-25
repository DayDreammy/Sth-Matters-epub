#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统模块
为Sth-Matters项目提供统一的日志记录功能
"""

import os
import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json


class ColoredFormatter(logging.Formatter):
    """带颜色的控制台日志格式化器"""

    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
    }
    RESET = '\033[0m'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 检查是否支持颜色输出
        self.use_color = self._supports_color()

    def _supports_color(self):
        """检测当前终端是否支持ANSI颜色"""
        # 检查环境变量
        if os.environ.get('NO_COLOR'):
            return False
        if os.environ.get('FORCE_COLOR'):
            return True

        # 检查是否为TTY终端
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False

        # 检查TERM环境变量
        term = os.environ.get('TERM', '')
        if 'color' in term or term in ('xterm', 'xterm-256color', 'screen', 'tmux'):
            return True

        return False

    def format(self, record):
        # 只有在支持颜色的终端才添加颜色
        if self.use_color and hasattr(record, 'levelname') and record.levelname in self.COLORS:
            # 保存原始levelname
            original_levelname = record.levelname
            # 添加颜色
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"

            # 格式化日志
            formatted = super().format(record)

            # 恢复原始levelname，避免影响其他handler
            record.levelname = original_levelname

            return formatted
        else:
            return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON格式的日志格式化器，用于结构化日志"""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # 添加额外的字段
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'topic'):
            log_entry['topic'] = record.topic
        if hasattr(record, 'search_type'):
            log_entry['search_type'] = record.search_type
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration
        if hasattr(record, 'file_count'):
            log_entry['file_count'] = record.file_count
        if hasattr(record, 'email'):
            log_entry['email'] = record.email

        # 添加异常信息
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False, separators=(',', ':'))


class SthMattersLogger:
    """Sth-Matters项目专用日志管理器"""

    def __init__(self,
                 log_dir: str = "logs",
                 log_level: str = "INFO",
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5,
                 enable_json: bool = True):
        """
        初始化日志系统

        Args:
            log_dir: 日志文件存储目录
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_file_size: 单个日志文件最大大小
            backup_count: 保留的日志文件备份数量
            enable_json: 是否启用JSON格式日志
        """
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.enable_json = enable_json

        # 创建日志目录
        self.log_dir.mkdir(exist_ok=True)

        # 日志记录器字典
        self._loggers: Dict[str, logging.Logger] = {}

        # 配置根日志记录器
        self._setup_root_logger()

    def _setup_root_logger(self):
        """配置根日志记录器"""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        # 清除已有的处理器
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_formatter = ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # 主日志文件处理器
        main_log_file = self.log_dir / "sth_matters.log"
        file_handler = logging.handlers.RotatingFileHandler(
            main_log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        # JSON格式日志文件处理器
        if self.enable_json:
            json_log_file = self.log_dir / "sth_matters.json"
            json_handler = logging.handlers.RotatingFileHandler(
                json_log_file,
                maxBytes=self.max_file_size,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            json_handler.setLevel(self.log_level)
            json_formatter = JSONFormatter()
            json_handler.setFormatter(json_formatter)
            root_logger.addHandler(json_handler)

        # 错误日志单独处理器
        error_log_file = self.log_dir / "errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s\n'
            'Exception: %(exc_info)s\n' + '-'*80,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        root_logger.addHandler(error_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """
        获取指定名称的日志记录器

        Args:
            name: 日志记录器名称，通常使用模块名

        Returns:
            日志记录器实例
        """
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
        return self._loggers[name]

    def log_search_start(self, topic: str, search_type: str, email: str, user_id: Optional[str] = None):
        """记录搜索开始事件"""
        logger = self.get_logger("search_events")
        extra = {
            'topic': topic,
            'search_type': search_type,
            'email': email,
            'event_type': 'search_start'
        }
        if user_id:
            extra['user_id'] = user_id

        logger.info(f"开始{search_type}: 主题='{topic}', 邮箱='{email}'", extra=extra)

    def log_search_complete(self, topic: str, search_type: str, duration: float,
                          file_count: int, success: bool, error_msg: Optional[str] = None):
        """记录搜索完成事件"""
        logger = self.get_logger("search_events")
        extra = {
            'topic': topic,
            'search_type': search_type,
            'duration': duration,
            'file_count': file_count,
            'success': success,
            'event_type': 'search_complete'
        }

        if success:
            logger.info(f"{search_type}完成: 主题='{topic}', 耗时={duration:.2f}秒, 生成文件={file_count}个", extra=extra)
        else:
            extra['error'] = error_msg
            logger.error(f"{search_type}失败: 主题='{topic}', 错误='{error_msg}'", extra=extra)

    def log_email_sent(self, topic: str, email: str, file_paths: list, success: bool, error_msg: Optional[str] = None):
        """记录邮件发送事件"""
        logger = self.get_logger("email_events")
        extra = {
            'topic': topic,
            'email': email,
            'file_count': len(file_paths),
            'success': success,
            'event_type': 'email_sent'
        }

        if success:
            logger.info(f"邮件发送成功: 主题='{topic}', 收件人='{email}', 附件={len(file_paths)}个", extra=extra)
        else:
            extra['error'] = error_msg
            logger.error(f"邮件发送失败: 主题='{topic}', 收件人='{email}', 错误='{error_msg}'", extra=extra)

    def log_file_operation(self, operation: str, file_path: str, success: bool, details: Optional[str] = None):
        """记录文件操作事件"""
        logger = self.get_logger("file_operations")
        extra = {
            'operation': operation,
            'file_path': file_path,
            'success': success,
            'event_type': 'file_operation'
        }

        if details:
            extra['details'] = details

        if success:
            logger.debug(f"文件操作成功: {operation} - {file_path}", extra=extra)
        else:
            logger.error(f"文件操作失败: {operation} - {file_path} - {details}", extra=extra)

    def log_performance(self, operation: str, duration: float, details: Optional[Dict[str, Any]] = None):
        """记录性能指标"""
        logger = self.get_logger("performance")
        extra = {
            'operation': operation,
            'duration': duration,
            'event_type': 'performance'
        }

        if details:
            extra.update(details)

        logger.info(f"性能指标: {operation} 耗时 {duration:.2f}秒", extra=extra)

    def get_log_stats(self) -> Dict[str, Any]:
        """获取日志统计信息"""
        stats = {
            'log_dir': str(self.log_dir),
            'log_files': [],
            'total_size': 0
        }

        for log_file in self.log_dir.glob("*.log*"):
            size = log_file.stat().st_size if log_file.exists() else 0
            stats['log_files'].append({
                'name': log_file.name,
                'size': size,
                'modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat() if log_file.exists() else None
            })
            stats['total_size'] += size

        return stats


# 全局日志管理器实例
_logger_manager: Optional[SthMattersLogger] = None


def get_logger(name: str = __name__) -> logging.Logger:
    """
    获取日志记录器的便捷函数

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器实例
    """
    global _logger_manager
    if _logger_manager is None:
        # 默认配置
        _logger_manager = SthMattersLogger()

    return _logger_manager.get_logger(name)


def init_logging(log_dir: str = "logs",
                log_level: str = "INFO",
                enable_json: bool = True,
                **kwargs) -> SthMattersLogger:
    """
    初始化日志系统

    Args:
        log_dir: 日志目录
        log_level: 日志级别
        enable_json: 是否启用JSON格式
        **kwargs: 其他配置参数

    Returns:
        日志管理器实例
    """
    global _logger_manager
    _logger_manager = SthMattersLogger(
        log_dir=log_dir,
        log_level=log_level,
        enable_json=enable_json,
        **kwargs
    )

    # 记录初始化信息
    logger = _logger_manager.get_logger("system")
    logger.info(f"日志系统初始化完成: 日志目录='{log_dir}', 级别='{log_level}', JSON格式={enable_json}")

    return _logger_manager


def get_log_manager() -> Optional[SthMattersLogger]:
    """获取全局日志管理器实例"""
    return _logger_manager


# 便捷的日志记录函数
def log_search_start(topic: str, search_type: str, email: str, user_id: Optional[str] = None):
    """记录搜索开始事件的便捷函数"""
    manager = get_log_manager()
    if manager:
        manager.log_search_start(topic, search_type, email, user_id)


def log_search_complete(topic: str, search_type: str, duration: float,
                       file_count: int, success: bool, error_msg: Optional[str] = None):
    """记录搜索完成事件的便捷函数"""
    manager = get_log_manager()
    if manager:
        manager.log_search_complete(topic, search_type, duration, file_count, success, error_msg)


def log_email_sent(topic: str, email: str, file_paths: list, success: bool, error_msg: Optional[str] = None):
    """记录邮件发送事件的便捷函数"""
    manager = get_log_manager()
    if manager:
        manager.log_email_sent(topic, email, file_paths, success, error_msg)


if __name__ == "__main__":
    # 测试日志系统
    print("=== Sth-Matters 日志系统测试 ===")

    # 初始化日志系统
    logger_manager = init_logging(log_dir="test_logs", log_level="DEBUG")

    # 获取日志记录器
    logger = get_logger("test_module")

    # 测试各种日志级别
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    logger.critical("这是一条严重错误")

    # 测试特殊日志功能
    logger_manager.log_search_start("测试主题", "深度搜索", "test@example.com", "user123")
    logger_manager.log_search_complete("测试主题", "深度搜索", 120.5, 5, True)
    logger_manager.log_email_sent("测试主题", "test@example.com", ["file1.pdf", "file2.epub"], True)
    logger_manager.log_performance("文档生成", 45.2, {"file_count": 3, "format": "epub"})

    # 测试异常日志
    try:
        # 模拟一个不会造成实际问题的异常
        raise ValueError("这是一个测试异常，用于验证异常日志功能")
    except Exception as e:
        logger.exception(f"测试异常日志功能: {e}")

    # 显示日志统计
    stats = logger_manager.get_log_stats()
    print(f"\n日志统计: {json.dumps(stats, indent=2, ensure_ascii=False)}")

    print("\n=== 日志系统测试完成 ===")
    print(f"请查看 'test_logs' 目录中的日志文件")
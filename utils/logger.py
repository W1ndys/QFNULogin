import os
import sys
import datetime
from loguru import logger


def setup_logger():
    """
    配置日志系统 (使用 loguru)
    """
    # 确保logs目录存在
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 移除默认的 handler
    logger.remove()

    # 定义日志格式
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # 添加控制台 handler
    logger.add(sys.stderr, format=log_format, level="INFO", colorize=True)

    # 添加文件 handler
    log_file_path = os.path.join(
        "logs", f'app_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",  # 日志文件大小超过 10MB 时轮转
        retention="1 week",  # 保留一周的日志
        encoding="utf-8",
    )

    return logger

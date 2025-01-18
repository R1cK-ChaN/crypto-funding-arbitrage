import logging
import os
from datetime import datetime

def setup_logger():
    """设置日志记录器"""
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 设置文件处理器
    file_handler = logging.FileHandler(
        f'logs/arbitrage_{datetime.now().strftime("%Y%m%d")}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # 设置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 设置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_logger():
    """获取日志记录器"""
    return logging.getLogger()

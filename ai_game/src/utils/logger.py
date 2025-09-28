"""
日志配置模块
"""
import logging
import os
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    设置日志配置
    
    Args:
        log_level (str): 日志级别
        
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logs_dir = os.path.join(project_root, "logs")
    
    # 创建logs目录
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # 创建日志器
    logger = logging.getLogger("ai_snake_game")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建文件处理器
    log_filename = os.path.join(logs_dir, f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# 创建全局日志器
logger = setup_logging()

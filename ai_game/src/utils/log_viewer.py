"""
日志查看工具
"""
import os
import glob
from datetime import datetime
from src.utils.logger import logger


def list_log_files() -> list:
    """
    列出所有日志文件
    
    Returns:
        list: 日志文件列表
    """
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logs_dir = os.path.join(project_root, "logs")
    log_files = glob.glob(os.path.join(logs_dir, "*.log"))
    return sorted(log_files, key=os.path.getmtime, reverse=True)


def view_latest_log() -> None:
    """
    查看最新的日志文件
    """
    log_files = list_log_files()
    if not log_files:
        print("没有找到日志文件")
        return
    
    latest_log = log_files[0]
    print(f"查看最新日志文件: {latest_log}")
    print("-" * 50)
    
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"读取日志文件失败: {e}")


def view_log_summary() -> None:
    """
    查看日志摘要
    """
    log_files = list_log_files()
    if not log_files:
        print("没有找到日志文件")
        return
    
    print("日志文件摘要:")
    print("-" * 50)
    
    for i, log_file in enumerate(log_files[:5]):  # 只显示最近5个
        try:
            file_size = os.path.getsize(log_file)
            mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
            print(f"{i+1}. {os.path.basename(log_file)}")
            print(f"   大小: {file_size} 字节")
            print(f"   修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        except Exception as e:
            print(f"读取文件信息失败: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "latest":
        view_latest_log()
    else:
        view_log_summary()
        print("使用 'python src/utils/log_viewer.py latest' 查看最新日志内容")

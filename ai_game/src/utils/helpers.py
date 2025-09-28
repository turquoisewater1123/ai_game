"""
辅助函数模块
"""
import random
from typing import List, Tuple
from src.utils.constants import GRID_WIDTH, GRID_HEIGHT


def generate_random_position(exclude_positions: List[Tuple[int, int]] = None) -> Tuple[int, int]:
    """
    生成随机位置
    
    Args:
        exclude_positions (List[Tuple[int, int]], optional): 需要排除的位置列表
        
    Returns:
        Tuple[int, int]: 随机生成的位置坐标
    """
    if exclude_positions is None:
        exclude_positions = []
    
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in exclude_positions:
            return (x, y)


def calculate_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    计算两点间的欧几里得距离
    
    Args:
        pos1 (Tuple[int, int]): 第一个位置
        pos2 (Tuple[int, int]): 第二个位置
        
    Returns:
        float: 两点间的距离
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def is_valid_position(pos: Tuple[int, int]) -> bool:
    """
    检查位置是否在游戏区域内
    
    Args:
        pos (Tuple[int, int]): 要检查的位置
        
    Returns:
        bool: 位置是否有效
    """
    x, y = pos
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT


def get_opposite_direction(direction: Tuple[int, int]) -> Tuple[int, int]:
    """
    获取相反方向
    
    Args:
        direction (Tuple[int, int]): 当前方向
        
    Returns:
        Tuple[int, int]: 相反方向
    """
    return (-direction[0], -direction[1])

"""
蛇类实现
"""
from typing import List, Tuple
from src.utils.constants import Direction, GRID_WIDTH, GRID_HEIGHT
from src.utils.helpers import is_valid_position


class Snake:
    """
    贪吃蛇类，负责蛇的移动、生长和碰撞检测
    """
    
    def __init__(self, start_pos: Tuple[int, int] = None) -> "Snake":
        """
        初始化蛇
        
        Args:
            start_pos (Tuple[int, int], optional): 蛇的起始位置，默认为游戏区域中心
            
        Raises:
            ValueError: 当起始位置无效时抛出
        """
        if start_pos is None:
            start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        
        if not is_valid_position(start_pos):
            raise ValueError("蛇的起始位置无效")
        
        self.body: List[Tuple[int, int]] = [start_pos]
        self.direction: Tuple[int, int] = Direction.RIGHT
        self.grow_pending: bool = False
    
    def move(self) -> None:
        """
        移动蛇到下一个位置
        """
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # 添加新头部
        self.body.insert(0, new_head)
        
        # 如果没有待生长的标记，移除尾部
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
    
    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """
        改变蛇的移动方向
        
        Args:
            new_direction (Tuple[int, int]): 新的移动方向
            
        Raises:
            ValueError: 当方向无效时抛出
        """
        # 防止蛇反向移动
        if new_direction == (-self.direction[0], -self.direction[1]):
            return
        
        self.direction = new_direction
    
    def grow(self) -> None:
        """
        标记蛇需要生长（下次移动时不会移除尾部）
        """
        self.grow_pending = True
    
    def check_collision(self) -> bool:
        """
        检查蛇是否发生碰撞
        
        Returns:
            bool: 是否发生碰撞
        """
        head = self.body[0]
        
        # 检查是否撞墙
        if not is_valid_position(head):
            return True
        
        # 检查是否撞到自己
        if head in self.body[1:]:
            return True
        
        return False
    
    def get_head_position(self) -> Tuple[int, int]:
        """
        获取蛇头位置
        
        Returns:
            Tuple[int, int]: 蛇头坐标
        """
        return self.body[0]
    
    def get_length(self) -> int:
        """
        获取蛇的长度
        
        Returns:
            int: 蛇的长度
        """
        return len(self.body)
    
    def reset(self, start_pos: Tuple[int, int] = None) -> None:
        """
        重置蛇到初始状态
        
        Args:
            start_pos (Tuple[int, int], optional): 新的起始位置
        """
        if start_pos is None:
            start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        
        self.body = [start_pos]
        self.direction = Direction.RIGHT
        self.grow_pending = False

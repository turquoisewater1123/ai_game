"""
食物类实现
"""
from typing import Tuple, List
from src.utils.constants import GRID_WIDTH, GRID_HEIGHT
from src.utils.helpers import generate_random_position, is_valid_position


class Food:
    """
    食物类，负责食物的生成和位置管理
    """
    
    def __init__(self) -> "Food":
        """
        初始化食物
        """
        self.position: Tuple[int, int] = self._generate_position()
        self.value: int = 1  # 食物价值
        self.special_type: str = "normal"  # 特殊食物类型
    
    def _generate_position(self) -> Tuple[int, int]:
        """
        生成随机食物位置
        
        Returns:
            Tuple[int, int]: 食物位置坐标
        """
        return generate_random_position()
    
    def respawn(self, exclude_positions: List[Tuple[int, int]] = None) -> None:
        """
        重新生成食物位置
        
        Args:
            exclude_positions (List[Tuple[int, int]], optional): 需要排除的位置列表
        """
        self.position = generate_random_position(exclude_positions)
        self.value = 1
        self.special_type = "normal"
    
    def get_position(self) -> Tuple[int, int]:
        """
        获取食物位置
        
        Returns:
            Tuple[int, int]: 食物坐标
        """
        return self.position
    
    def is_eaten(self, snake_head: Tuple[int, int]) -> bool:
        """
        检查食物是否被吃掉
        
        Args:
            snake_head (Tuple[int, int]): 蛇头位置
            
        Returns:
            bool: 是否被吃掉
        """
        return snake_head == self.position
    
    def set_special_food(self, food_type: str, value: int = 1) -> None:
        """
        设置特殊食物
        
        Args:
            food_type (str): 食物类型
            value (int): 食物价值
        """
        self.special_type = food_type
        self.value = value


class SpecialFood(Food):
    """
    特殊食物类，继承自普通食物
    """
    
    def __init__(self, food_type: str = "speed_boost", value: int = 2) -> "SpecialFood":
        """
        初始化特殊食物
        
        Args:
            food_type (str): 食物类型
            value (int): 食物价值
        """
        super().__init__()
        self.special_type = food_type
        self.value = value
    
    def get_effect(self) -> str:
        """
        获取食物效果
        
        Returns:
            str: 食物效果描述
        """
        effects = {
            "speed_boost": "加速",
            "slow_down": "减速", 
            "extra_points": "额外分数",
            "invincible": "无敌"
        }
        return effects.get(self.special_type, "未知效果")

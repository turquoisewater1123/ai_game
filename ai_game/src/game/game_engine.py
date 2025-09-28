"""
游戏引擎核心模块
"""
from typing import Tuple, List, Optional
import random
from src.game.snake import Snake
from src.game.food import Food, SpecialFood
from src.utils.constants import GameState, Direction, AIDifficulty
from src.utils.logger import logger


class GameEngine:
    """
    游戏引擎类，负责游戏逻辑控制和状态管理
    """
    
    def __init__(self) -> "GameEngine":
        """
        初始化游戏引擎
        """
        self.snake: Snake = Snake()
        self.food: Food = Food()
        self.score: int = 0
        self.game_state: str = GameState.MENU
        self.ai_enabled: bool = False
        self.ai_difficulty: int = AIDifficulty.MEDIUM
        self.game_speed: int = 15
        self.special_food_spawn_chance: float = 0.1  # 10%概率生成特殊食物
        self.special_food: Optional[SpecialFood] = None
        self.special_food_timer: int = 0
        self.special_food_duration: int = 300  # 特殊食物存在时间（帧数）
    
    def start_game(self, ai_enabled: bool = False, difficulty: int = AIDifficulty.MEDIUM) -> None:
        """
        开始新游戏
        
        Args:
            ai_enabled (bool): 是否启用AI
            difficulty (int): AI难度等级
            
        Raises:
            ValueError: 当难度等级无效时抛出
        """
        try:
            if difficulty not in [AIDifficulty.EASY, AIDifficulty.MEDIUM, AIDifficulty.HARD, AIDifficulty.EXPERT]:
                raise ValueError(f"无效的AI难度等级: {difficulty}")
            
            logger.info(f"开始新游戏 - AI模式: {ai_enabled}, 难度: {difficulty}")
            
            self.reset_game()
            self.ai_enabled = ai_enabled
            self.ai_difficulty = difficulty
            self.game_state = GameState.PLAYING
            self._set_game_speed()
            
            logger.info(f"游戏已开始 - 状态: {self.game_state}, 速度: {self.game_speed}")
            
        except Exception as e:
            logger.error(f"开始游戏失败: {e}")
            raise
    
    def reset_game(self) -> None:
        """
        重置游戏到初始状态
        """
        try:
            logger.info("重置游戏状态")
            self.snake = Snake()
            self.food = Food()
            self.score = 0
            self.special_food = None
            self.special_food_timer = 0
            logger.debug(f"游戏重置完成 - 分数: {self.score}, 蛇长度: {self.snake.get_length()}")
        except Exception as e:
            logger.error(f"重置游戏失败: {e}")
            raise
    
    def pause_game(self) -> None:
        """
        暂停游戏
        """
        if self.game_state == GameState.PLAYING:
            logger.info("游戏暂停")
            self.game_state = GameState.PAUSED
    
    def resume_game(self) -> None:
        """
        恢复游戏
        """
        if self.game_state == GameState.PAUSED:
            logger.info("游戏恢复")
            self.game_state = GameState.PLAYING
    
    def update(self) -> None:
        """
        更新游戏状态
        """
        try:
            if self.game_state != GameState.PLAYING:
                return
            
            # 移动蛇
            self.snake.move()
            logger.debug(f"蛇移动到: {self.snake.get_head_position()}")
            
            # 检查碰撞
            if self.snake.check_collision():
                logger.info(f"游戏结束 - 最终分数: {self.score}, 蛇长度: {self.snake.get_length()}")
                self.game_state = GameState.GAME_OVER
                return
            
            # 检查是否吃到食物
            if self.snake.get_head_position() == self.food.get_position():
                logger.info(f"吃到普通食物 - 位置: {self.food.get_position()}")
                self._eat_food()
            
            # 检查是否吃到特殊食物
            if self.special_food and self.snake.get_head_position() == self.special_food.get_position():
                logger.info(f"吃到特殊食物 - 类型: {self.special_food.special_type}, 位置: {self.special_food.get_position()}")
                self._eat_special_food()
            
            # 更新特殊食物计时器
            self._update_special_food()
            
        except Exception as e:
            logger.error(f"游戏更新失败: {e}")
            self.game_state = GameState.GAME_OVER
    
    def _eat_food(self) -> None:
        """
        处理吃到普通食物的逻辑
        """
        self.snake.grow()
        self.score += self.food.value
        
        # 重新生成食物
        exclude_positions = self.snake.body.copy()
        if self.special_food:
            exclude_positions.append(self.special_food.get_position())
        
        self.food.respawn(exclude_positions)
        
        # 随机生成特殊食物
        if not self.special_food and self._should_spawn_special_food():
            self._spawn_special_food()
    
    def _eat_special_food(self) -> None:
        """
        处理吃到特殊食物的逻辑
        """
        if not self.special_food:
            return
        
        self.score += self.special_food.value
        self._apply_special_food_effect()
        self.special_food = None
        self.special_food_timer = 0
    
    def _should_spawn_special_food(self) -> bool:
        """
        判断是否应该生成特殊食物
        
        Returns:
            bool: 是否生成特殊食物
        """
        import random
        return random.random() < self.special_food_spawn_chance
    
    def _spawn_special_food(self) -> None:
        """
        生成特殊食物
        """
        exclude_positions = self.snake.body.copy()
        exclude_positions.append(self.food.get_position())
        
        self.special_food = SpecialFood()
        self.special_food.respawn(exclude_positions)
        self.special_food_timer = self.special_food_duration
    
    def _update_special_food(self) -> None:
        """
        更新特殊食物状态
        """
        if self.special_food:
            self.special_food_timer -= 1
            if self.special_food_timer <= 0:
                self.special_food = None
    
    def _apply_special_food_effect(self) -> None:
        """
        应用特殊食物效果
        """
        if not self.special_food:
            return
        
        effect = self.special_food.special_type
        if effect == "speed_boost":
            self.game_speed = min(self.game_speed + 2, 30)
        elif effect == "slow_down":
            self.game_speed = max(self.game_speed - 2, 5)
        elif effect == "extra_points":
            self.score += 10
    
    def _set_game_speed(self) -> None:
        """
        根据AI难度设置游戏速度
        """
        speed_map = {
            AIDifficulty.EASY: 10,
            AIDifficulty.MEDIUM: 15,
            AIDifficulty.HARD: 20,
            AIDifficulty.EXPERT: 25
        }
        self.game_speed = speed_map.get(self.ai_difficulty, 15)
    
    def get_game_info(self) -> dict:
        """
        获取游戏信息
        
        Returns:
            dict: 包含游戏状态信息的字典
        """
        return {
            "score": self.score,
            "snake_length": self.snake.get_length(),
            "game_state": self.game_state,
            "ai_enabled": self.ai_enabled,
            "difficulty": self.ai_difficulty,
            "special_food_active": self.special_food is not None
        }
    
    def change_snake_direction(self, direction: Tuple[int, int]) -> None:
        """
        改变蛇的移动方向
        
        Args:
            direction (Tuple[int, int]): 新的移动方向
        """
        if self.game_state == GameState.PLAYING:
            self.snake.change_direction(direction)

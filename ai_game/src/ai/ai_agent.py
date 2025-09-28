"""
AI智能体模块
"""
from typing import List, Tuple, Optional, Set
import random
from src.ai.pathfinding import Pathfinding
from src.utils.constants import Direction, AIDifficulty
from src.utils.helpers import calculate_distance, get_opposite_direction
from src.utils.logger import logger


class AIAgent:
    """
    AI智能体类，负责为贪吃蛇游戏提供智能决策
    """
    
    def __init__(self, difficulty: int = AIDifficulty.MEDIUM) -> "AIAgent":
        """
        初始化AI智能体
        
        Args:
            difficulty (int): AI难度等级
        """
        self.difficulty = difficulty
        self.pathfinder = Pathfinding()
        self.current_path: List[Tuple[int, int]] = []
        self.last_food_position: Optional[Tuple[int, int]] = None
        self.thinking_depth = self._get_thinking_depth()
        self.risk_tolerance = self._get_risk_tolerance()
    
    def _get_thinking_depth(self) -> int:
        """
        根据难度获取AI思考深度
        
        Returns:
            int: 思考深度
        """
        depth_map = {
            AIDifficulty.EASY: 1,
            AIDifficulty.MEDIUM: 2,
            AIDifficulty.HARD: 3,
            AIDifficulty.EXPERT: 4
        }
        return depth_map.get(self.difficulty, 2)
    
    def _get_risk_tolerance(self) -> float:
        """
        根据难度获取AI风险容忍度
        
        Returns:
            float: 风险容忍度 (0-1)
        """
        risk_map = {
            AIDifficulty.EASY: 0.3,
            AIDifficulty.MEDIUM: 0.5,
            AIDifficulty.HARD: 0.7,
            AIDifficulty.EXPERT: 0.9
        }
        return risk_map.get(self.difficulty, 0.5)
    
    def get_next_move(self, snake_body: List[Tuple[int, int]], 
                     food_position: Tuple[int, int],
                     special_food_position: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        """
        获取AI的下一个移动方向
        
        Args:
            snake_body (List[Tuple[int, int]]): 蛇的身体位置列表
            food_position (Tuple[int, int]): 食物位置
            special_food_position (Optional[Tuple[int, int]]): 特殊食物位置
            
        Returns:
            Tuple[int, int]: 下一个移动方向
            
        Raises:
            ValueError: 当输入参数无效时抛出
        """
        try:
            if not snake_body:
                logger.warning("蛇身体为空，返回默认方向")
                return Direction.RIGHT
            
            head = snake_body[0]
            obstacles = set(snake_body[1:])  # 蛇身作为障碍物
            
            logger.debug(f"AI决策 - 蛇头: {head}, 食物: {food_position}, 特殊食物: {special_food_position}")
            
            # 检查是否需要重新规划路径
            if (self._should_replan_path(head, food_position, special_food_position)):
                logger.debug("重新规划路径")
                self._plan_path(head, food_position, special_food_position, obstacles)
            
            # 获取下一个移动方向
            next_direction = self._get_direction_from_path(head)
            
            # 如果路径无效，使用安全移动策略
            if not next_direction or not self._is_safe_move(head, next_direction, obstacles):
                logger.warning("路径无效，使用安全移动策略")
                next_direction = self._get_safe_move(head, obstacles)
            
            # 根据难度添加一些随机性
            if random.random() < (1 - self.risk_tolerance) * 0.1:
                logger.debug("添加随机性")
                next_direction = self._add_randomness(next_direction, head, obstacles)
            
            logger.debug(f"AI决策结果: {next_direction}")
            return next_direction
            
        except Exception as e:
            logger.error(f"AI决策失败: {e}")
            # 返回安全方向
            return Direction.UP
    
    def _should_replan_path(self, head: Tuple[int, int], 
                          food_position: Tuple[int, int],
                          special_food_position: Optional[Tuple[int, int]]) -> bool:
        """
        判断是否需要重新规划路径
        
        Args:
            head (Tuple[int, int]): 蛇头位置
            food_position (Tuple[int, int]): 食物位置
            special_food_position (Optional[Tuple[int, int]]): 特殊食物位置
            
        Returns:
            bool: 是否需要重新规划
        """
        # 如果当前路径为空
        if not self.current_path:
            return True
        
        # 如果食物位置改变
        if food_position != self.last_food_position:
            return True
        
        # 如果蛇头不在当前路径上
        if head not in self.current_path:
            return True
        
        # 如果路径太短（可能被阻塞）
        if len(self.current_path) < 3:
            return True
        
        return False
    
    def _plan_path(self, head: Tuple[int, int], 
                  food_position: Tuple[int, int],
                  special_food_position: Optional[Tuple[int, int]],
                  obstacles: Set[Tuple[int, int]]) -> None:
        """
        规划到食物的路径
        
        Args:
            head (Tuple[int, int]): 蛇头位置
            food_position (Tuple[int, int]): 食物位置
            special_food_position (Optional[Tuple[int, int]]): 特殊食物位置
            obstacles (Set[Tuple[int, int]]): 障碍物集合
        """
        # 选择目标（优先特殊食物）
        target = special_food_position if special_food_position else food_position
        
        # 使用A*算法寻找路径
        self.current_path = self.pathfinder.find_path_astar(head, target, obstacles)
        
        # 如果A*失败，尝试BFS
        if not self.current_path:
            self.current_path = self.pathfinder.find_path_bfs(head, target, obstacles)
        
        # 如果仍然失败，使用安全策略
        if not self.current_path:
            self.current_path = self._get_safe_path(head, obstacles)
        
        self.last_food_position = food_position
    
    def _get_direction_from_path(self, head: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        从路径中获取下一个移动方向
        
        Args:
            head (Tuple[int, int]): 蛇头位置
            
        Returns:
            Optional[Tuple[int, int]]: 移动方向
        """
        return self.pathfinder.get_next_direction(head, self.current_path)
    
    def _is_safe_move(self, head: Tuple[int, int], direction: Tuple[int, int], 
                     obstacles: Set[Tuple[int, int]]) -> bool:
        """
        检查移动是否安全
        
        Args:
            head (Tuple[int, int]): 蛇头位置
            direction (Tuple[int, int]): 移动方向
            obstacles (Set[Tuple[int, int]]): 障碍物集合
            
        Returns:
            bool: 移动是否安全
        """
        next_pos = (head[0] + direction[0], head[1] + direction[1])
        
        # 检查是否撞墙
        from src.utils.constants import GRID_WIDTH, GRID_HEIGHT
        if not (0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT):
            return False
        
        # 检查是否撞到障碍物
        if next_pos in obstacles:
            return False
        
        return True
    
    def _get_safe_move(self, head: Tuple[int, int], 
                      obstacles: Set[Tuple[int, int]]) -> Tuple[int, int]:
        """
        获取安全的移动方向
        
        Args:
            head (Tuple[int, int]): 蛇头位置
            obstacles (Set[Tuple[int, int]]): 障碍物集合
            
        Returns:
            Tuple[int, int]: 安全的移动方向
        """
        # 尝试所有可能的方向
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        safe_directions = []
        
        for direction in directions:
            if self._is_safe_move(head, direction, obstacles):
                safe_directions.append(direction)
        
        # 如果有安全方向，选择其中一个
        if safe_directions:
            return random.choice(safe_directions)
        
        # 如果没有安全方向，返回向上（游戏结束）
        return Direction.UP
    
    def _get_safe_path(self, head: Tuple[int, int], 
                      obstacles: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        获取安全路径（当无法到达食物时）
        
        Args:
            head (Tuple[int, int]): 蛇头位置
            obstacles (Set[Tuple[int, int]]): 障碍物集合
            
        Returns:
            List[Tuple[int, int]]: 安全路径
        """
        # 寻找最远的可达位置
        from src.utils.constants import GRID_WIDTH, GRID_HEIGHT
        max_distance = 0
        best_position = head
        
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = (x, y)
                if pos not in obstacles:
                    distance = calculate_distance(head, pos)
                    if distance > max_distance:
                        max_distance = distance
                        best_position = pos
        
        # 尝试找到到最佳位置的路径
        path = self.pathfinder.find_path_astar(head, best_position, obstacles)
        return path if path else [head]
    
    def _add_randomness(self, direction: Tuple[int, int], 
                       head: Tuple[int, int], 
                       obstacles: Set[Tuple[int, int]]) -> Tuple[int, int]:
        """
        添加随机性（根据难度）
        
        Args:
            direction (Tuple[int, int]): 当前方向
            head (Tuple[int, int]): 蛇头位置
            obstacles (Set[Tuple[int, int]]): 障碍物集合
            
        Returns:
            Tuple[int, int]: 可能改变的方向
        """
        # 获取所有安全方向
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        safe_directions = [d for d in directions if self._is_safe_move(head, d, obstacles)]
        
        # 如果只有一个安全方向，返回原方向
        if len(safe_directions) <= 1:
            return direction
        
        # 随机选择一个安全方向
        return random.choice(safe_directions)
    
    def set_difficulty(self, difficulty: int) -> None:
        """
        设置AI难度
        
        Args:
            difficulty (int): 新的难度等级
        """
        self.difficulty = difficulty
        self.thinking_depth = self._get_thinking_depth()
        self.risk_tolerance = self._get_risk_tolerance()
        self.current_path = []  # 清空当前路径

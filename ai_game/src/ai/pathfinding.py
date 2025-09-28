"""
路径搜索算法模块
"""
from typing import List, Tuple, Set, Optional, Dict
from collections import deque
from src.utils.constants import Direction, GRID_WIDTH, GRID_HEIGHT
from src.utils.helpers import is_valid_position, calculate_distance


class Pathfinding:
    """
    路径搜索算法类，实现A*算法和BFS算法
    """
    
    def __init__(self) -> "Pathfinding":
        """
        初始化路径搜索器
        """
        pass
    
    def find_path_astar(self, start: Tuple[int, int], goal: Tuple[int, int], 
                        obstacles: Set[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
        """
        使用A*算法寻找从起点到终点的最短路径
        
        Args:
            start (Tuple[int, int]): 起始位置
            goal (Tuple[int, int]): 目标位置
            obstacles (Set[Tuple[int, int]]): 障碍物位置集合
            
        Returns:
            Optional[List[Tuple[int, int]]]: 路径列表，如果无法到达则返回None
        """
        if start == goal:
            return [start]
        
        # 开放列表和关闭列表
        open_set: Set[Tuple[int, int]] = {start}
        closed_set: Set[Tuple[int, int]] = set()
        
        # 父节点映射
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        # g_score: 从起点到该点的实际距离
        g_score: Dict[Tuple[int, int], float] = {start: 0}
        
        # f_score: g_score + 启发式距离
        f_score: Dict[Tuple[int, int], float] = {start: self._heuristic(start, goal)}
        
        while open_set:
            # 选择f_score最小的节点
            current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
            
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            open_set.remove(current)
            closed_set.add(current)
            
            # 检查所有相邻节点
            for direction in Direction.__dict__.values():
                if isinstance(direction, tuple):
                    neighbor = (current[0] + direction[0], current[1] + direction[1])
                    
                    if (not is_valid_position(neighbor) or 
                        neighbor in closed_set or 
                        neighbor in obstacles):
                        continue
                    
                    tentative_g_score = g_score[current] + 1
                    
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                    elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                        continue
                    
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, goal)
        
        return None  # 无法找到路径
    
    def find_path_bfs(self, start: Tuple[int, int], goal: Tuple[int, int], 
                     obstacles: Set[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
        """
        使用BFS算法寻找从起点到终点的最短路径
        
        Args:
            start (Tuple[int, int]): 起始位置
            goal (Tuple[int, int]): 目标位置
            obstacles (Set[Tuple[int, int]]): 障碍物位置集合
            
        Returns:
            Optional[List[Tuple[int, int]]]: 路径列表，如果无法到达则返回None
        """
        if start == goal:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            for direction in Direction.__dict__.values():
                if isinstance(direction, tuple):
                    neighbor = (current[0] + direction[0], current[1] + direction[1])
                    
                    if (neighbor == goal):
                        return path + [neighbor]
                    
                    if (is_valid_position(neighbor) and 
                        neighbor not in visited and 
                        neighbor not in obstacles):
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
        
        return None  # 无法找到路径
    
    def _heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        启发式函数，使用曼哈顿距离
        
        Args:
            pos1 (Tuple[int, int]): 第一个位置
            pos2 (Tuple[int, int]): 第二个位置
            
        Returns:
            float: 启发式距离
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], 
                         current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        重构路径
        
        Args:
            came_from (Dict[Tuple[int, int], Tuple[int, int]]): 父节点映射
            current (Tuple[int, int]): 当前节点
            
        Returns:
            List[Tuple[int, int]]: 重构的路径
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def get_next_direction(self, current_pos: Tuple[int, int], 
                          path: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        根据路径获取下一个移动方向
        
        Args:
            current_pos (Tuple[int, int]): 当前位置
            path (List[Tuple[int, int]]): 路径列表
            
        Returns:
            Optional[Tuple[int, int]]: 下一个移动方向，如果路径无效则返回None
        """
        if not path or len(path) < 2:
            return None
        
        try:
            current_index = path.index(current_pos)
            if current_index < len(path) - 1:
                next_pos = path[current_index + 1]
                return (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
        except ValueError:
            pass
        
        return None

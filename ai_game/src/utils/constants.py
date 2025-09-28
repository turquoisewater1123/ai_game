"""
游戏常量定义模块
"""
from typing import Tuple

# 游戏窗口设置
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
GRID_SIZE: int = 20
GRID_WIDTH: int = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT: int = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义 (RGB)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
GREEN: Tuple[int, int, int] = (0, 255, 0)
RED: Tuple[int, int, int] = (255, 0, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
GRAY: Tuple[int, int, int] = (128, 128, 128)
DARK_GREEN: Tuple[int, int, int] = (0, 150, 0)

# 游戏状态
class GameState:
    """游戏状态枚举"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# 方向定义
class Direction:
    """方向枚举"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# AI难度等级
class AIDifficulty:
    """AI难度等级"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

# 游戏速度设置
GAME_SPEED_EASY = 10
GAME_SPEED_MEDIUM = 15
GAME_SPEED_HARD = 20
GAME_SPEED_EXPERT = 25

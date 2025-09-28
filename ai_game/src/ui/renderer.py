"""
游戏渲染器模块
"""
import pygame
from typing import List, Tuple, Optional
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    BLACK, WHITE, GREEN, RED, BLUE, YELLOW, GRAY, DARK_GREEN
)
from src.game.snake import Snake
from src.game.food import Food, SpecialFood
from src.utils.logger import logger


class Renderer:
    """
    游戏渲染器类，负责绘制游戏界面
    """
    
    def __init__(self) -> "Renderer":
        """
        初始化渲染器
        
        Raises:
            pygame.error: 当pygame初始化失败时抛出
        """
        try:
            logger.info("初始化游戏渲染器")
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("AI Snake Game")
            self.clock = pygame.time.Clock()
            
            # 使用系统字体支持中文
            try:
                self.font_large = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
                self.font_medium = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
                self.font_small = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
            except:
                # 如果系统字体不可用，使用默认字体
                self.font_large = pygame.font.Font(None, 48)
                self.font_medium = pygame.font.Font(None, 32)
                self.font_small = pygame.font.Font(None, 24)
            
            logger.info("游戏渲染器初始化完成")
        except Exception as e:
            logger.error(f"渲染器初始化失败: {e}")
            raise
    
    def clear_screen(self) -> None:
        """
        清空屏幕
        """
        self.screen.fill(BLACK)
    
    def draw_snake(self, snake: Snake) -> None:
        """
        绘制蛇
        
        Args:
            snake (Snake): 蛇对象
        """
        for i, segment in enumerate(snake.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            # 蛇头使用不同颜色
            if i == 0:
                pygame.draw.rect(self.screen, DARK_GREEN, 
                               (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, GREEN, 
                               (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4))
            else:
                pygame.draw.rect(self.screen, GREEN, 
                               (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, DARK_GREEN, 
                               (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
    
    def draw_food(self, food: Food) -> None:
        """
        绘制食物
        
        Args:
            food (Food): 食物对象
        """
        x = food.get_position()[0] * GRID_SIZE
        y = food.get_position()[1] * GRID_SIZE
        
        # 绘制圆形食物
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
        pygame.draw.circle(self.screen, RED, center, GRID_SIZE // 2 - 2)
        pygame.draw.circle(self.screen, WHITE, center, GRID_SIZE // 2 - 4)
    
    def draw_special_food(self, special_food: SpecialFood) -> None:
        """
        绘制特殊食物
        
        Args:
            special_food (SpecialFood): 特殊食物对象
        """
        if not special_food:
            return
        
        x = special_food.get_position()[0] * GRID_SIZE
        y = special_food.get_position()[1] * GRID_SIZE
        
        # 根据特殊食物类型选择颜色
        color_map = {
            "speed_boost": BLUE,
            "slow_down": YELLOW,
            "extra_points": WHITE,
            "invincible": GRAY
        }
        color = color_map.get(special_food.special_type, BLUE)
        
        # 绘制星形特殊食物
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
        pygame.draw.circle(self.screen, color, center, GRID_SIZE // 2 - 1)
        pygame.draw.circle(self.screen, WHITE, center, GRID_SIZE // 2 - 3)
    
    def draw_grid(self) -> None:
        """
        绘制游戏网格
        """
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw_score(self, score: int) -> None:
        """
        绘制分数
        
        Args:
            score (int): 当前分数
        """
        score_text = self.font_medium.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_info(self, snake_length: int, ai_enabled: bool, difficulty: int) -> None:
        """
        绘制游戏信息
        
        Args:
            snake_length (int): 蛇的长度
            ai_enabled (bool): 是否启用AI
            difficulty (int): AI难度
        """
        length_text = self.font_small.render(f"Length: {snake_length}", True, WHITE)
        self.screen.blit(length_text, (10, 40))
        
        if ai_enabled:
            difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard", 4: "Expert"}
            ai_text = self.font_small.render(f"AI: {difficulty_names.get(difficulty, 'Unknown')}", True, WHITE)
            self.screen.blit(ai_text, (10, 60))
    
    def draw_menu(self) -> None:
        """
        绘制主菜单
        """
        title_text = self.font_large.render("AI Snake Game", True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        start_text = self.font_medium.render("SPACE - Manual Mode", True, WHITE)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(start_text, start_rect)
        
        ai_text = self.font_medium.render("1-4 - AI Mode (Difficulty)", True, WHITE)
        ai_rect = ai_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(ai_text, ai_rect)
        
        quit_text = self.font_medium.render("ESC - Quit Game", True, WHITE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game_over(self, score: int, snake_length: int) -> None:
        """
        绘制游戏结束界面
        
        Args:
            score (int): 最终分数
            snake_length (int): 最终蛇长度
        """
        # 半透明覆盖层
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("Game Over!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        length_text = self.font_medium.render(f"Snake Length: {snake_length}", True, WHITE)
        length_rect = length_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(length_text, length_rect)
        
        restart_text = self.font_medium.render("Press ESC to Return to Menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    
    
    def update_display(self) -> None:
        """
        更新显示
        """
        pygame.display.flip()
    
    def get_clock(self) -> pygame.time.Clock:
        """
        获取时钟对象
        
        Returns:
            pygame.time.Clock: 时钟对象
        """
        return self.clock
    
    def quit(self) -> None:
        """
        退出渲染器
        """
        pygame.quit()

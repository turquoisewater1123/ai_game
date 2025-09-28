"""
用户界面控制器模块
"""
import pygame
from typing import Optional, Tuple
from src.utils.constants import (
    GameState, Direction, AIDifficulty, WINDOW_WIDTH, WINDOW_HEIGHT
)
from src.ui.renderer import Renderer
from src.game.game_engine import GameEngine
from src.ai.ai_agent import AIAgent
from src.utils.logger import logger


class GameInterface:
    """
    游戏界面控制器类，负责处理用户输入和界面逻辑
    """
    
    def __init__(self) -> "GameInterface":
        """
        初始化游戏界面
        
        Raises:
            pygame.error: 当pygame初始化失败时抛出
        """
        try:
            logger.info("初始化游戏界面")
            self.renderer = Renderer()
            self.game_engine = GameEngine()
            self.ai_agent: Optional[AIAgent] = None
            self.running = True
            logger.info("游戏界面初始化完成")
        except Exception as e:
            logger.error(f"游戏界面初始化失败: {e}")
            raise
    
    def run(self) -> None:
        """
        运行游戏主循环
        """
        try:
            logger.info("开始游戏主循环")
            while self.running:
                self._handle_events()
                self._update_game()
                self._render()
                self.renderer.get_clock().tick(self.game_engine.game_speed)
            
            logger.info("游戏主循环结束")
        except Exception as e:
            logger.error(f"游戏主循环异常: {e}")
            raise
        finally:
            try:
                self.renderer.quit()
                logger.info("游戏资源已清理")
            except Exception as e:
                logger.error(f"清理游戏资源失败: {e}")
    
    def _handle_events(self) -> None:
        """
        处理游戏事件
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event.key)
    
    def _handle_key_press(self, key: int) -> None:
        """
        处理按键事件
        
        Args:
            key (int): 按键代码
        """
        if self.game_engine.game_state == GameState.MENU:
            self._handle_menu_input(key)
        elif self.game_engine.game_state == GameState.PLAYING:
            self._handle_game_input(key)
        elif self.game_engine.game_state == GameState.GAME_OVER:
            self._handle_game_over_input(key)
    
    def _handle_menu_input(self, key: int) -> None:
        """
        处理主菜单输入
        
        Args:
            key (int): 按键代码
        """
        logger.info(f"主菜单按键: {key}")
        
        if key == pygame.K_SPACE:
            logger.info("开始手动游戏")
            self.game_engine.start_game(ai_enabled=False)
        elif key == pygame.K_ESCAPE:
            logger.info("退出游戏")
            self.running = False
        elif key == pygame.K_1:
            logger.info("开始AI游戏 (简单难度)")
            self.game_engine.start_game(ai_enabled=True, difficulty=AIDifficulty.EASY)
            self.ai_agent = AIAgent(AIDifficulty.EASY)
        elif key == pygame.K_2:
            logger.info("开始AI游戏 (中等难度)")
            self.game_engine.start_game(ai_enabled=True, difficulty=AIDifficulty.MEDIUM)
            self.ai_agent = AIAgent(AIDifficulty.MEDIUM)
        elif key == pygame.K_3:
            logger.info("开始AI游戏 (困难难度)")
            self.game_engine.start_game(ai_enabled=True, difficulty=AIDifficulty.HARD)
            self.ai_agent = AIAgent(AIDifficulty.HARD)
        elif key == pygame.K_4:
            logger.info("开始AI游戏 (专家难度)")
            self.game_engine.start_game(ai_enabled=True, difficulty=AIDifficulty.EXPERT)
            self.ai_agent = AIAgent(AIDifficulty.EXPERT)
    
    def _handle_game_input(self, key: int) -> None:
        """
        处理游戏中的输入
        
        Args:
            key (int): 按键代码
        """
        if not self.game_engine.ai_enabled:
            # 手动控制蛇的移动
            if key == pygame.K_UP or key == pygame.K_w:
                self.game_engine.change_snake_direction(Direction.UP)
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.game_engine.change_snake_direction(Direction.DOWN)
            elif key == pygame.K_LEFT or key == pygame.K_a:
                self.game_engine.change_snake_direction(Direction.LEFT)
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                self.game_engine.change_snake_direction(Direction.RIGHT)
        
        # 通用控制
        if key == pygame.K_ESCAPE:
            self.game_engine.game_state = GameState.MENU
    
    def _handle_game_over_input(self, key: int) -> None:
        """
        处理游戏结束输入
        
        Args:
            key (int): 按键代码
        """
        if key == pygame.K_ESCAPE:
            self.game_engine.game_state = GameState.MENU
    
    def _update_game(self) -> None:
        """
        更新游戏状态
        """
        if self.game_engine.game_state == GameState.PLAYING:
            # AI控制
            if self.game_engine.ai_enabled and self.ai_agent:
                self._update_ai()
            
            # 更新游戏引擎
            self.game_engine.update()
    
    def _update_ai(self) -> None:
        """
        更新AI决策
        """
        if not self.ai_agent:
            return
        
        snake_body = self.game_engine.snake.body
        food_position = self.game_engine.food.get_position()
        special_food_position = None
        
        if self.game_engine.special_food:
            special_food_position = self.game_engine.special_food.get_position()
        
        # 获取AI决策
        next_direction = self.ai_agent.get_next_move(
            snake_body, food_position, special_food_position
        )
        
        # 应用AI决策
        self.game_engine.change_snake_direction(next_direction)
    
    
    def _render(self) -> None:
        """
        渲染游戏界面
        """
        self.renderer.clear_screen()
        
        if self.game_engine.game_state == GameState.MENU:
            self._render_menu()
        elif self.game_engine.game_state == GameState.PLAYING:
            self._render_game()
        elif self.game_engine.game_state == GameState.GAME_OVER:
            self._render_game()
            self.renderer.draw_game_over(
                self.game_engine.score, 
                self.game_engine.snake.get_length()
            )
        
        self.renderer.update_display()
    
    def _render_menu(self) -> None:
        """
        渲染主菜单
        """
        self.renderer.draw_menu()
    
    def _render_game(self) -> None:
        """
        渲染游戏界面
        """
        # 绘制蛇
        self.renderer.draw_snake(self.game_engine.snake)
        
        # 绘制食物
        self.renderer.draw_food(self.game_engine.food)
        
        # 绘制特殊食物
        if self.game_engine.special_food:
            self.renderer.draw_special_food(self.game_engine.special_food)
        
        # 绘制游戏信息
        game_info = self.game_engine.get_game_info()
        self.renderer.draw_score(game_info["score"])
        self.renderer.draw_game_info(
            game_info["snake_length"],
            game_info["ai_enabled"],
            game_info["difficulty"]
        )
        
        # 绘制控制提示
        self._draw_control_hints()
    
    def _draw_control_hints(self) -> None:
        """
        绘制控制提示
        """
        hints = []
        
        if self.game_engine.game_state == GameState.PLAYING:
            if not self.game_engine.ai_enabled:
                hints.append("Arrow Keys/WASD: Control Snake")
            hints.append("ESC: Back to Menu")
        
        # 在屏幕底部绘制提示
        y_offset = WINDOW_HEIGHT - 30
        for i, hint in enumerate(hints):
            hint_text = self.renderer.font_small.render(hint, True, (200, 200, 200))
            self.renderer.screen.blit(hint_text, (10, y_offset - i * 20))

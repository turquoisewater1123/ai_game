"""
AI贪吃蛇游戏主程序入口
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.interface import GameInterface
from src.utils.logger import logger


def main() -> None:
    """
    主函数，启动AI贪吃蛇游戏
    """
    try:
        logger.info("=" * 50)
        logger.info("AI贪吃蛇游戏启动")
        logger.info("=" * 50)
        
        print("正在启动AI贪吃蛇游戏...")
        print("游戏控制说明:")
        print("- 主菜单: SPACE开始游戏, A启用AI模式, 1-4选择AI难度")
        print("- 游戏中: 方向键/WASD控制(手动模式), P暂停, R重新开始, ESC返回菜单")
        print("- AI模式: V切换显示AI路径")
        print("- 退出: ESC或关闭窗口")
        print()
        
        # 创建并运行游戏
        logger.info("创建游戏界面")
        game = GameInterface()
        logger.info("开始运行游戏")
        game.run()
        
        logger.info("游戏正常结束")
        
    except KeyboardInterrupt:
        logger.info("游戏被用户中断")
        print("\n游戏被用户中断")
    except ImportError as e:
        logger.error(f"导入模块失败: {e}")
        print(f"导入模块失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
    except Exception as e:
        logger.error(f"游戏运行出错: {e}")
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("游戏已退出")
        print("游戏已退出")


if __name__ == "__main__":
    main()

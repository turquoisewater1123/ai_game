@echo off
echo 正在启动AI贪吃蛇游戏...
echo.
echo 游戏控制说明:
echo - 主菜单: SPACE开始游戏, A启用AI模式, 1-4选择AI难度
echo - 游戏中: 方向键/WASD控制(手动模式), P暂停, R重新开始, ESC返回菜单
echo - AI模式: V切换显示AI路径
echo - 退出: ESC或关闭窗口
echo.
python src/main.py
pause

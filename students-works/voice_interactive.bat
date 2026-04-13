@echo off
chcp 65001 >nul
echo.
echo 🤖 智能表格助手 - 语音/文字输入系统
echo =======================================
echo.
echo 使用方法：
echo   1. 直接运行本文件进入交互模式
echo   2. 或从命令行：python voice_to_table.py "你的文本"
echo.
echo 示例：
echo   python voice_to_table.py "新增学生：张三，初中二年级，擅长Python"
echo   python voice_to_table.py "新增作品：学生stu004，作品名AI绘画助手"
echo.
echo 按任意键开始交互模式...
pause >nul

python voice_to_table.py
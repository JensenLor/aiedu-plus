@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 罗辑智造社网站预览服务器
echo ============================================================
echo.
echo 网站目录: %~dp0
echo.
echo 正在启动HTTP服务器...
echo.

REM 使用管理的Python版本
set PYTHON_PATH=C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe

REM 检查Python是否可用
if not exist "%PYTHON_PATH%" (
    echo 错误: 找不到Python
    echo 请确保Python 3.13.12已安装
    pause
    exit /b 1
)

REM 启动服务器
echo 正在启动服务器，请稍候...
echo.
echo 手机访问说明:
echo 1. 确保手机和电脑在同一个WiFi网络
echo 2. 在手机浏览器输入显示的IP地址
echo 3. 按Ctrl+C停止服务器
echo.
echo ============================================================
echo.

"%PYTHON_PATH%" "%~dp0start_server.py"

if errorlevel 1 (
    echo.
    echo 服务器启动失败
    pause
)
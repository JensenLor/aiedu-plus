@echo off
chcp 65001 > nul
echo 开始每周学生作品数据更新...
echo 更新时间: %date% %time%
echo.

REM 切换到脚本目录
cd /d "%~dp0"

REM 1. 更新数据
echo 正在更新数据...
python simple_update_data.py
if %errorlevel% neq 0 (
    echo 错误: 数据更新失败
    pause
    exit /b 1
)

REM 2. 更新HTML页面
echo 正在更新网站页面...
python update_cases_html.py
if %errorlevel% neq 0 (
    echo 错误: 页面更新失败
    pause
    exit /b 1
)

REM 3. 备份本次更新
echo 正在备份数据...
set BACKUP_DIR=..\backups\%date:~0,4%-%date:~5,2%-%date:~8,2%
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
xcopy ..\generated\* "%BACKUP_DIR%\" /E /Y

echo.
echo 更新完成！
echo 学生作品数据已更新到网站
echo 备份保存到: %BACKUP_DIR%
echo.
pause
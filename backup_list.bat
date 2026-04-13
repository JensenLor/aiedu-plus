@echo off
echo ========================================
echo 罗辑智造社备份版本列表
echo ========================================
echo.

set "BACKUP_DIR=D:\WorkBuddy\LuojiStudio\working\ongoing\aiedu-plus\backups"

echo 备份目录: %BACKUP_DIR%
echo.

REM 检查备份目录是否存在
if not exist "%BACKUP_DIR%" (
    echo 备份目录不存在！
    echo 请先运行 backup_pages.bat 创建备份
    pause
    exit /b 1
)

REM 获取所有备份版本
echo 可用备份版本列表:
echo ----------------------------
setlocal enabledelayedexpansion
set count=0

for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a count+=1
    set "backup_name=%%d"
    
    REM 提取时间信息
    set "timestamp=!backup_name:version_=!"
    set "year=!timestamp:~0,4!"
    set "month=!timestamp:~4,2!"
    set "day=!timestamp:~6,2!"
    set "hour=!timestamp:~9,2!"
    set "minute=!timestamp:~11,2!"
    set "second=!timestamp:~13,2!"
    
    REM 读取备份信息
    if exist "%BACKUP_DIR%\!backup_name!\backup_info.txt" (
        for /f "tokens=2*" %%a in ('findstr /c:"备份时间:" "%BACKUP_DIR%\!backup_name!\backup_info.txt"') do set "backup_time=%%b"
    ) else (
        set "backup_time=!year!-!month!-!day! !hour!:!minute!:!second!"
    )
    
    REM 统计文件数量
    set "file_count=0"
    for /f %%f in ('dir /b /a-d "%BACKUP_DIR%\!backup_name!\*.html" 2^>nul') do set /a file_count+=1
    for /f %%f in ('dir /b /a-d "%BACKUP_DIR%\!backup_name!\*.css" 2^>nul') do set /a file_count+=1
    
    echo !count!. 版本: !backup_name!
    echo     时间: !backup_time!
    echo     文件: !file_count! 个
    echo     目录: %BACKUP_DIR%\!backup_name!
    echo.
)

if !count! equ 0 (
    echo 暂无备份版本
    echo 请运行 backup_pages.bat 创建备份
) else (
    echo 总计: !count! 个备份版本
)

echo.
echo ========================================
echo 备份管理工具
echo ========================================
echo 1. 创建新备份: backup_pages.bat
echo 2. 恢复指定版本: restore_version.bat
echo 3. 删除旧备份: backup_cleanup.bat
echo ========================================
echo.
pause
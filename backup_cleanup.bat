@echo off
echo ========================================
echo 罗辑智造社备份清理工具
echo ========================================
echo.

set "BACKUP_DIR=D:\WorkBuddy\LuojiStudio\working\ongoing\aiedu-plus\backups"
set "KEEP_COUNT=10"

REM 检查备份目录是否存在
if not exist "%BACKUP_DIR%" (
    echo 备份目录不存在！
    echo 请先运行 backup_pages.bat 创建备份
    pause
    exit /b 1
)

echo 备份目录: %BACKUP_DIR%
echo 保留版本数: %KEEP_COUNT%
echo.

echo 正在扫描所有备份版本...
echo ----------------------------
setlocal enabledelayedexpansion

REM 获取所有备份版本，按时间倒序（最新的在前面）
set index=0
set total=0

echo 所有备份版本（按时间倒序）:
for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a total+=1
)

REM 反向显示，最新的在最后
set count=0
for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a count+=1
    set "backup_name=%%d"
    
    REM 计算要删除的版本
    set /a should_delete=count - total + %KEEP_COUNT%
    
    if exist "%BACKUP_DIR%\!backup_name!\backup_info.txt" (
        for /f "tokens=2*" %%a in ('findstr /c:"备份时间:" "%BACKUP_DIR%\!backup_name!\backup_info.txt"') do set "backup_time=%%b"
    ) else (
        set "backup_time=!backup_name:version_=!"
    )
    
    if !should_delete! leq 0 (
        echo   !count!. !backup_name! (!backup_time!) [保留]
    ) else (
        echo   !count!. !backup_name! (!backup_time!) [删除]
    )
)

echo.
echo 统计信息:
echo   备份总数: !total!
echo   保留数量: !KEEP_COUNT!
if !total! leq !KEEP_COUNT! (
    echo   删除数量: 0 (无需清理)
    echo.
    echo 当前备份数量未超过保留限制，无需清理
    pause
    exit /b 0
)

set /a delete_count=total - %KEEP_COUNT%
echo   删除数量: !delete_count!

echo.
set /p confirm="确认要删除旧备份吗？(y/n): "

if /i "!confirm!" neq "y" (
    echo 已取消清理操作
    pause
    exit /b 0
)

echo.
echo ========================================
echo 正在清理旧备份...
echo ========================================

set count=0
set deleted=0
for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a count+=1
    set "backup_name=%%d"
    
    REM 计算要删除的版本
    set /a should_delete=count - total + %KEEP_COUNT%
    
    if !should_delete! gtr 0 (
        echo 删除: !backup_name!
        rmdir /s /q "%BACKUP_DIR%\!backup_name!" 2>nul
        if exist "%BACKUP_DIR%\!backup_name!" (
            echo  ✗ 删除失败: !backup_name!
        ) else (
            echo  ✓ 已删除: !backup_name!
            set /a deleted+=1
        )
    )
)

echo.
echo ========================================
echo 清理完成！
echo ========================================
echo 清理统计:
echo   原备份数: !total!
echo   保留数量: !KEEP_COUNT!
echo   删除数量: !deleted!
echo   剩余数量: !total! - !deleted! = !KEEP_COUNT!
echo.
echo 当前保留的备份:
set count=0
for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a count+=1
    echo   !count!. %%d
)

echo.
echo 备份管理建议:
echo 1. 建议每次重大修改前运行 backup_pages.bat
echo 2. 定期运行此脚本清理旧备份
echo 3. 重要版本可手动复制到其他位置
echo ========================================
echo.
pause
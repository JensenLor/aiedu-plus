@echo off
echo ========================================
echo 罗辑智造社备份恢复工具
echo ========================================
echo.

set "BACKUP_DIR=D:\WorkBuddy\LuojiStudio\working\ongoing\aiedu-plus\backups"
set "PROJECT_DIR=D:\WorkBuddy\LuojiStudio\working\ongoing\aiedu-plus"

REM 检查备份目录是否存在
if not exist "%BACKUP_DIR%" (
    echo 备份目录不存在！
    echo 请先运行 backup_pages.bat 创建备份
    pause
    exit /b 1
)

echo 正在扫描可用备份版本...
echo ----------------------------
setlocal enabledelayedexpansion
set count=0

echo 可用备份版本:
for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a count+=1
    set "backup_name=%%d"
    
    REM 读取备份时间
    if exist "%BACKUP_DIR%\!backup_name!\backup_info.txt" (
        for /f "tokens=2*" %%a in ('findstr /c:"备份时间:" "%BACKUP_DIR%\!backup_name!\backup_info.txt"') do set "backup_time=%%b"
    ) else (
        set "backup_time=!backup_name:version_=!"
    )
    
    echo !count!. !backup_name! (!backup_time!)
)

if !count! equ 0 (
    echo 暂无备份版本
    echo 请运行 backup_pages.bat 创建备份
    pause
    exit /b 1
)

echo.
set /p version_num="请选择要恢复的版本编号 (1-!count!): "

REM 验证输入
set "valid_input=0"
set "selected_backup="
set index=0

for /f "delims=" %%d in ('dir "%BACKUP_DIR%\version_*" /ad /b /od') do (
    set /a index+=1
    if !index! equ !version_num! (
        set "selected_backup=%%d"
        set "valid_input=1"
    )
)

if !valid_input! equ 0 (
    echo 错误的版本编号！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 确认恢复操作
echo ========================================
echo 要恢复的版本: !selected_backup!
set "BACKUP_PATH=%BACKUP_DIR%\!selected_backup%"

REM 显示备份信息
if exist "%BACKUP_PATH%\backup_info.txt" (
    type "%BACKUP_PATH%\backup_info.txt"
) else (
    echo 备份时间: !selected_backup:version_=!
    echo 备份目录: %BACKUP_PATH%
)

echo.
set /p confirm="确认要恢复此版本吗？(y/n): "

if /i "!confirm!" neq "y" (
    echo 已取消恢复操作
    pause
    exit /b 0
)

echo.
echo ========================================
echo 正在恢复备份...
echo ========================================

REM 创建恢复前的备份（安全起见）
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "RESTORE_BACKUP=%BACKUP_DIR%\before_restore_%TIMESTAMP%"

if not exist "%RESTORE_BACKUP%" (
    mkdir "%RESTORE_BACKUP%"
    echo 创建恢复前备份: %RESTORE_BACKUP%
    
    REM 备份当前文件
    copy "index.html" "%RESTORE_BACKUP%\index.html" /Y >nul
    copy "works.html" "%RESTORE_BACKUP%\works.html" /Y >nul
    copy "work-detail.html" "%RESTORE_BACKUP%\work-detail.html" /Y >nul
    copy "resources.html" "%RESTORE_BACKUP%\resources.html" /Y >nul
    copy "cases.html" "%RESTORE_BACKUP%\cases.html" /Y >nul
    copy "profile.html" "%RESTORE_BACKUP%\profile.html" /Y >nul
    copy "preview.html" "%RESTORE_BACKUP%\preview.html" /Y >nul
    copy "test-work-detail.html" "%RESTORE_BACKUP%\test-work-detail.html" /Y >nul
    copy "style.css" "%RESTORE_BACKUP%\style.css" /Y >nul
)

REM 恢复备份文件
echo.
echo 正在恢复文件...
echo ----------------------------

copy "%BACKUP_PATH%\index.html" "index.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: index.html) else (echo  ✗ 恢复失败: index.html)

copy "%BACKUP_PATH%\works.html" "works.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: works.html) else (echo  ✗ 恢复失败: works.html)

copy "%BACKUP_PATH%\work-detail.html" "work-detail.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: work-detail.html) else (echo  ✗ 恢复失败: work-detail.html)

copy "%BACKUP_PATH%\resources.html" "resources.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: resources.html) else (echo  ✗ 恢复失败: resources.html)

copy "%BACKUP_PATH%\cases.html" "cases.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: cases.html) else (echo  ✗ 恢复失败: cases.html)

copy "%BACKUP_PATH%\profile.html" "profile.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: profile.html) else (echo  ✗ 恢复失败: profile.html)

copy "%BACKUP_PATH%\preview.html" "preview.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: preview.html) else (echo  ✗ 恢复失败: preview.html)

copy "%BACKUP_PATH%\test-work-detail.html" "test-work-detail.html" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: test-work-detail.html) else (echo  ✗ 恢复失败: test-work-detail.html)

copy "%BACKUP_PATH%\style.css" "style.css" /Y
if %errorlevel% equ 0 (echo  ✓ 恢复: style.css) else (echo  ✗ 恢复失败: style.css)

echo.
echo ========================================
echo 恢复完成！
echo ========================================
echo 已恢复版本: !selected_backup!
echo 恢复时间: %date% %time%
echo 恢复前备份: %RESTORE_BACKUP%
echo 恢复文件数: 9个文件
echo.
echo 重要提示:
echo 1. 如果恢复出现问题，可以使用恢复前备份
echo 2. 恢复前备份在: %RESTORE_BACKUP%
echo 3. 再次运行本工具可恢复更早的版本
echo ========================================
echo.
pause
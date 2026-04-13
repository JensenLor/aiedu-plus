@echo off
echo ========================================
echo 罗辑智造社网页文件备份工具
echo ========================================
echo.

REM 设置备份目录和时间戳
set "BACKUP_DIR=D:\WorkBuddy\LuojiStudio\working\ongoing\aiedu-plus\backups"
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "BACKUP_NAME=version_%TIMESTAMP%"
set "BACKUP_PATH=%BACKUP_DIR%\%BACKUP_NAME%"

echo 备份时间: %date% %time%
echo 备份版本: %BACKUP_NAME%
echo 备份目录: %BACKUP_PATH%
echo.

REM 创建备份目录
if not exist "%BACKUP_PATH%" (
    mkdir "%BACKUP_PATH%"
    echo 创建备份目录: %BACKUP_PATH%
) else (
    echo 备份目录已存在: %BACKUP_PATH%
)

REM 备份所有HTML页面文件
echo.
echo 正在备份HTML页面文件...
echo ----------------------------

copy "index.html" "%BACKUP_PATH%\index.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: index.html) else (echo  ✗ 备份失败: index.html)

copy "works.html" "%BACKUP_PATH%\works.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: works.html) else (echo  ✗ 备份失败: works.html)

copy "work-detail.html" "%BACKUP_PATH%\work-detail.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: work-detail.html) else (echo  ✗ 备份失败: work-detail.html)

copy "resources.html" "%BACKUP_PATH%\resources.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: resources.html) else (echo  ✗ 备份失败: resources.html)

copy "cases.html" "%BACKUP_PATH%\cases.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: cases.html) else (echo  ✗ 备份失败: cases.html)

copy "profile.html" "%BACKUP_PATH%\profile.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: profile.html) else (echo  ✗ 备份失败: profile.html)

copy "preview.html" "%BACKUP_PATH%\preview.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: preview.html) else (echo  ✗ 备份失败: preview.html)

copy "test-work-detail.html" "%BACKUP_PATH%\test-work-detail.html" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: test-work-detail.html) else (echo  ✗ 备份失败: test-work-detail.html)

REM 备份CSS样式文件
echo.
echo 正在备份CSS样式文件...
echo ----------------------------
copy "style.css" "%BACKUP_PATH%\style.css" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: style.css) else (echo  ✗ 备份失败: style.css)

REM 备份README和配置文档
echo.
echo 正在备份文档文件...
echo ----------------------------
copy "README.md" "%BACKUP_PATH%\README.md" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: README.md) else (echo  ✗ 备份失败: README.md)

copy "PREVIEW.md" "%BACKUP_PATH%\PREVIEW.md" /Y
if %errorlevel% equ 0 (echo  ✓ 备份: PREVIEW.md) else (echo  ✗ 备份失败: PREVIEW.md)

REM 创建备份记录
echo.
echo 正在创建备份记录...
echo ----------------------------
echo 备份时间: %date% %time% > "%BACKUP_PATH%\backup_info.txt"
echo 备份版本: %BACKUP_NAME% >> "%BACKUP_PATH%\backup_info.txt"
echo 备份文件数: 9 >> "%BACKUP_PATH%\backup_info.txt"
echo 备份目录: %BACKUP_PATH% >> "%BACKUP_PATH%\backup_info.txt"
echo 项目名称: aiedu.plus >> "%BACKUP_PATH%\backup_info.txt"
echo 备份说明: 页面文件备份 >> "%BACKUP_PATH%\backup_info.txt"

echo  ✓ 备份记录创建完成

REM 显示备份信息
echo.
echo ========================================
echo 备份完成！
echo ========================================
echo 备份时间: %date% %time%
echo 备份版本: %BACKUP_NAME%
echo 备份文件: 9个页面文件 + 样式文件
echo 备份位置: %BACKUP_PATH%
echo.
echo 备份文件列表:
dir "%BACKUP_PATH%\*.html" /b
echo.
echo 要恢复备份，请执行:
echo   1. 查看备份列表: backup_list.bat
echo   2. 恢复指定版本: restore_version.bat
echo ========================================
echo.
pause
@echo off
chcp 65001 > nul
echo ========================================
echo   aiedu.plus 一键部署脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 正在添加文件到Git...
git add -A
if errorlevel 1 (
    echo [错误] Git添加文件失败！
    pause
    exit /b 1
)
echo [OK] 文件已添加
echo.

echo [2/3] 正在提交更改...
if "%~1"=="" (
    set /p commit_msg="请输入提交信息（直接回车使用默认信息）: "
    if "%commit_msg%"=="" set commit_msg=更新 aiedu.plus
) else (
    set commit_msg=%~1
)
git commit -m "%commit_msg%"
if errorlevel 1 (
    echo [错误] Git提交失败！可能是没有文件更改。
    pause
    exit /b 1
)
echo [OK] 已提交: %commit_msg%
echo.

echo [3/3] 正在推送到GitHub...
git push origin master:main
if errorlevel 1 (
    echo [错误] Git推送失败！请检查网络连接。
    pause
    exit /b 1
)
echo [OK] 推送成功！
echo.

echo ========================================
echo   部署完成！
echo   约1-2分钟后 Vercel 自动部署生效
echo ========================================
echo.
pause

@echo off
chcp 65001 >nul
echo 正在启动网站服务器...
echo.

cd /d "%~dp0"

echo ============================================================
echo 网站服务器已启动！
echo ============================================================
echo 本地访问：http://localhost:8000
echo.

REM 获取本机IP地址
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    set "ip=%%a"
    goto :found_ip
)

:found_ip
REM 清理IP地址（去除空格）
set "ip=%ip: =%"
echo 手机访问：http://%ip%:8000
echo.

echo ============================================================
echo 主要页面：
echo   • 首页：http://localhost:8000/index.html
echo   • MakerVerse：http://localhost:8000/works.html
echo   • 作品详情测试：http://localhost:8000/test-work-detail.html
echo ============================================================
echo 按 Ctrl+C 停止服务器
echo ============================================================

python -m http.server 8000
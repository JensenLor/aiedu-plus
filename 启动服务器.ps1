# 罗辑智造社网站预览服务器启动脚本

Write-Host "`n" -NoNewline
Write-Host "===========================================================" -ForegroundColor Green
Write-Host "🚀 罗辑智造社网站预览服务器" -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Green
Write-Host "`n" -NoNewline
Write-Host "📂 网站目录: " -NoNewline
Write-Host "$PSScriptRoot" -ForegroundColor Cyan
Write-Host "`n" -NoNewline
Write-Host "🔧 正在启动HTTP服务器..." -ForegroundColor Yellow
Write-Host "`n" -NoNewline

# Python执行路径
$PYTHON_PATH = "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"

# 检查Python是否可用
if (-not (Test-Path $PYTHON_PATH)) {
    Write-Host "❌ 错误: 找不到Python" -ForegroundColor Red
    Write-Host "请确保Python 3.13.12已安装" -ForegroundColor Red
    Read-Host "按Enter键退出..."
    exit 1
}

# 启动服务器
Write-Host "正在启动服务器，请稍候..." -ForegroundColor Yellow
Write-Host "`n" -NoNewline
Write-Host "📱 手机访问说明: " -ForegroundColor Cyan
Write-Host "1. 确保手机和电脑在同一个WiFi网络" -ForegroundColor Cyan
Write-Host "2. 在手机浏览器输入显示的IP地址" -ForegroundColor Cyan
Write-Host "3. 按Ctrl+C停止服务器" -ForegroundColor Cyan
Write-Host "`n" -NoNewline
Write-Host "===========================================================" -ForegroundColor Green
Write-Host "`n" -NoNewline

# 运行服务器脚本
& $PYTHON_PATH "$PSScriptRoot\start_server.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n" -NoNewline
    Write-Host "❌ 服务器启动失败" -ForegroundColor Red
    Read-Host "按Enter键退出..."
}

# PowerShell HTTP 服务器脚本
# 用于本地预览网站

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 罗辑智造社网站预览服务器" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$currentDir = Get-Location
Write-Host "📂 网站目录: $currentDir" -ForegroundColor Yellow
Write-Host ""

# 检查是否安装了Python
$pythonAvailable = $false
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonAvailable = $true
        Write-Host "✅ 找到Python: $pythonVersion" -ForegroundColor Green
    }
} catch {
    # Python不可用
}

Write-Host ""
Write-Host "🔧 正在启动HTTP服务器..." -ForegroundColor Yellow
Write-Host ""

# 获取本地IP地址
function Get-LocalIP {
    try {
        $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*","以太网*","Ethernet*" | 
               Where-Object {$_.AddressFamily -eq 'IPv4'} | 
               Sort-Object InterfaceIndex | 
               Select-Object -First 1).IPAddress
        
        if (-not $ip) {
            $ip = "127.0.0.1"
        }
        return $ip
    } catch {
        return "127.0.0.1"
    }
}

$ipAddress = Get-LocalIP
$port = 8000

Write-Host "📱 手机访问说明:" -ForegroundColor Yellow
Write-Host "1. 确保手机和电脑在同一个WiFi网络"
Write-Host "2. 在手机浏览器输入: http://$ipAddress`:8000"
Write-Host "3. 按Ctrl+C停止服务器"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($pythonAvailable) {
    # 使用Python启动服务器
    Write-Host "✅ 使用Python启动HTTP服务器..." -ForegroundColor Green
    Write-Host "🌐 服务器地址: http://$ipAddress`:$port" -ForegroundColor Green
    Write-Host "💻 本地访问: http://localhost:$port" -ForegroundColor Green
    Write-Host ""
    
    # 启动Python服务器
    python -m http.server $port
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Python服务器启动失败" -ForegroundColor Red
        Write-Host "正在尝试备用方案..." -ForegroundColor Yellow
        # 继续执行备用方案
    }
}

# 如果Python不可用或失败，尝试使用PowerShell的HTTP监听器
Write-Host "🔧 正在启动PowerShell HTTP服务器..." -ForegroundColor Yellow

try {
    # 创建简单的HTTP监听器
    $listener = New-Object System.Net.HttpListener
    $prefix = "http://*:$port/"
    $listener.Prefixes.Add($prefix)
    $listener.Start()
    
    Write-Host "✅ PowerShell HTTP服务器已启动！" -ForegroundColor Green
    Write-Host "🌐 服务器地址: http://$ipAddress`:$port" -ForegroundColor Green
    Write-Host "💻 本地访问: http://localhost:$port" -ForegroundColor Green
    Write-Host ""
    Write-Host "📂 可访问的文件:" -ForegroundColor Yellow
    Write-Host "   - 首页: http://localhost:$port/index.html"
    Write-Host "   - 学生作品: http://localhost:$port/cases.html"
    Write-Host "   - 个人主页示例: http://localhost:$port/profile.html?id=zzy001"
    Write-Host ""
    Write-Host "🔄 正在运行... (按Ctrl+C停止)" -ForegroundColor Yellow
    
    # 打开浏览器
    try {
        Start-Process "http://localhost:$port"
    } catch {
        Write-Host "⚠️  无法自动打开浏览器，请手动访问以上地址" -ForegroundColor Yellow
    }
    
    # 处理请求
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $path = $request.Url.LocalPath
        if ($path -eq "/") {
            $path = "/index.html"
        }
        
        $filePath = Join-Path $currentDir ($path.TrimStart('/'))
        
        if (Test-Path $filePath -PathType Leaf) {
            $content = [System.IO.File]::ReadAllBytes($filePath)
            $response.ContentType = Get-ContentType $path
            $response.ContentLength64 = $content.Length
            $response.OutputStream.Write($content, 0, $content.Length)
        } else {
            $response.StatusCode = 404
            $notFound = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $path")
            $response.ContentLength64 = $notFound.Length
            $response.OutputStream.Write($notFound, 0, $notFound.Length)
        }
        
        $response.Close()
    }
    
} catch {
    Write-Host "❌ 服务器启动失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 建议解决方案:" -ForegroundColor Yellow
    Write-Host "1. 安装Python: https://www.python.org/downloads/"
    Write-Host "2. 使用其他HTTP服务器工具"
    Write-Host ""
} finally {
    if ($listener -and $listener.IsListening) {
        $listener.Stop()
    }
}

Write-Host ""
Write-Host "🛑 服务器已停止" -ForegroundColor Red
Read-Host "按Enter键退出..."

function Get-ContentType {
    param([string]$path)
    
    $ext = [System.IO.Path]::GetExtension($path).ToLower()
    switch ($ext) {
        ".html" { return "text/html; charset=utf-8" }
        ".css"  { return "text/css; charset=utf-8" }
        ".js"   { return "application/javascript; charset=utf-8" }
        ".json" { return "application/json; charset=utf-8" }
        ".png"  { return "image/png" }
        ".jpg"  { return "image/jpeg" }
        ".jpeg" { return "image/jpeg" }
        ".gif"  { return "image/gif" }
        ".pdf"  { return "application/pdf" }
        ".zip"  { return "application/zip" }
        default { return "application/octet-stream" }
    }
}
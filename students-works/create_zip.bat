@echo off
chcp 65001 >nul
echo 正在创建作品ZIP下载包...

REM 创建下载目录
if not exist "downloads" mkdir downloads

REM 作品文件夹路径
set "work_folder=work001_智能天气助手"
set "student_folder=zzy001_曾梓扬"
set "work_path=students\%student_folder%\works\%work_folder%"
set "zip_filename=%work_folder%.zip"
set "zip_path=downloads\%zip_filename%"

REM 检查作品文件夹是否存在
if not exist "%work_path%" (
    echo 错误: 作品文件夹不存在: %work_path%
    pause
    exit /b 1
)

echo 作品文件夹: %work_path%

REM 使用PowerShell创建ZIP文件
powershell -Command "& {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory('%work_path%', '%zip_path%')
    $file = Get-Item '%zip_path%'
    Write-Host '成功创建ZIP包:' $file.Name
    Write-Host '文件大小:' ([math]::Round($file.Length/1024, 1)) 'KB'
    Write-Host '保存位置:' $file.FullName
}"

if errorlevel 1 (
    echo ZIP包创建失败
    pause
    exit /b 1
)

echo.
echo ZIP包创建完成！
pause
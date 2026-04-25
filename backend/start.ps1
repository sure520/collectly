# ============================================
# Collectly 后端启动脚本 (PowerShell)
# ============================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Collectly 后端启动脚本" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查 .env 文件
$envFile = Join-Path $ScriptDir ".env"
if (-not (Test-Path $envFile)) {
    $envExample = Join-Path $ScriptDir ".env.example"
    if (Test-Path $envExample) {
        Write-Host "[警告] 未找到 .env 文件" -ForegroundColor Yellow
        Write-Host "正在从 .env.example 创建 .env 文件..." -ForegroundColor Yellow
        Copy-Item $envExample $envFile
        Write-Host "请编辑 .env 文件填写 API Key 后重新运行" -ForegroundColor Yellow
        Write-Host "按任意键打开 .env 文件..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        notepad $envFile
        exit 1
    } else {
        Write-Host "[错误] 未找到 .env 和 .env.example 文件" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
}

# 检查虚拟环境
$venvPath = Join-Path $ScriptDir ".venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "[信息] 创建 Python 虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
    if (-not $?) {
        Write-Host "[错误] 创建虚拟环境失败" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
    Write-Host "[完成] 虚拟环境已创建" -ForegroundColor Green
}

# 安装/更新依赖
Write-Host "[信息] 检查 Python 依赖..." -ForegroundColor Yellow
$pip = Join-Path $venvPath "Scripts\pip"
& $pip install -r requirements.txt --quiet
if (-not $?) {
    Write-Host "[错误] 安装依赖失败" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}
Write-Host "[完成] 依赖检查完成" -ForegroundColor Green

# 创建日志目录
$logDir = Join-Path $ScriptDir "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 读取端口配置
$backendPort = "8000"
$envContent = Get-Content $envFile | Where-Object { $_ -match "^BACKEND_PORT=" }
if ($envContent) {
    $backendPort = ($envContent -split "=")[1].Trim()
}

$uvicorn = Join-Path $venvPath "Scripts\uvicorn"

Write-Host ""
Write-Host "[信息] 启动后端服务..." -ForegroundColor Yellow
Write-Host "  - 端口: $backendPort"
Write-Host "  - API: http://localhost:$backendPort"
Write-Host "  - 文档: http://localhost:$backendPort/docs"
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

& $uvicorn app.main:app --host 0.0.0.0 --port $backendPort --reload --log-level info

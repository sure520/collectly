# ============================================
# Collectly 后端启动脚本 (PowerShell)
# 使用 uv 管理虚拟环境
# ============================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Collectly 后端启动脚本" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查 uv 是否安装
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCmd) {
    Write-Host "[错误] 未检测到 uv，请先安装 uv" -ForegroundColor Red
    Write-Host ""
    Write-Host "安装方式（任选其一）:" -ForegroundColor Yellow
    Write-Host "  方式一: powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`"" -ForegroundColor White
    Write-Host "  方式二: winget install astral-sh.uv" -ForegroundColor White
    Write-Host ""
    Write-Host "详情请参考: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor White
    Read-Host "按 Enter 退出"
    exit 1
}

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

# 同步虚拟环境和依赖（uv sync 会自动创建 .venv 并安装依赖）
Write-Host "[信息] 同步 Python 依赖 (uv sync)..." -ForegroundColor Yellow
uv sync --inexact
if (-not $?) {
    Write-Host "[错误] 同步依赖失败" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}
Write-Host "[完成] 依赖同步完成" -ForegroundColor Green

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

$venvPath = Join-Path $ScriptDir ".venv"
$venvScripts = Join-Path $venvPath "Scripts"
$env:VIRTUAL_ENV = $venvPath
$env:PATH = "$venvScripts;$env:PATH"

Write-Host ""
Write-Host "[信息] 启动后端服务..." -ForegroundColor Yellow
Write-Host "  - 端口: $backendPort"
Write-Host "  - API: http://localhost:$backendPort"
Write-Host "  - 文档: http://localhost:$backendPort/docs"
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

uv run uvicorn backend.app.main:app --host 0.0.0.0 --port $backendPort --reload --log-level info

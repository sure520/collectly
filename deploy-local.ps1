# ============================================
# Collectly 一键部署脚本 (Windows PowerShell)
# 支持双部署模式：本地部署/云服务器部署
# 使用 uv 管理 Python 虚拟环境
# ============================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Collectly 一键部署脚本" -ForegroundColor Cyan
Write-Host "  AI驱动的个人知识收藏与检索管家" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ================================
# 步骤1: 选择部署模式
# ================================
Write-Host "请选择部署模式:" -ForegroundColor Yellow
Write-Host "  [A] 方案A - 本地部署 + 内网穿透（推荐个人使用，零成本）" -ForegroundColor White
Write-Host "  [B] 方案B - 云服务器公网部署（推荐24h在线，稳定性强）" -ForegroundColor White
Write-Host ""
$deployMode = Read-Host "请输入选项 (A/B)"

if ($deployMode -eq "A" -or $deployMode -eq "a") {
    $mode = "local"
    Write-Host ""
    Write-Host "[信息] 已选择: 方案A - 本地部署 + 内网穿透" -ForegroundColor Green
    Write-Host ""
    Write-Host "说明:" -ForegroundColor Yellow
    Write-Host "  - 后端运行在本地电脑" -ForegroundColor White
    Write-Host "  - 使用Cloudflare Tunnel实现外网访问" -ForegroundColor White
    Write-Host "  - 支持电脑息屏运行，无需全天开机" -ForegroundColor White
    Write-Host "  - 数据完全私有化，不离开个人设备" -ForegroundColor White
    Write-Host ""
} elseif ($deployMode -eq "B" -or $deployMode -eq "b") {
    $mode = "cloud"
    Write-Host ""
    Write-Host "[信息] 已选择: 方案B - 云服务器公网部署" -ForegroundColor Green
    Write-Host ""
    Write-Host "说明:" -ForegroundColor Yellow
    Write-Host "  - 后端运行在云服务器" -ForegroundColor White
    Write-Host "  - 通过固定公网IP/域名访问" -ForegroundColor White
    Write-Host "  - 24h永久在线，稳定性最强" -ForegroundColor White
    Write-Host "  - 需要云服务器（推荐轻量应用服务器）" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "[错误] 无效选项，默认使用方案A" -ForegroundColor Red
    $mode = "local"
}

# ================================
# 步骤2: 检查环境
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤1: 检查运行环境" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# 检查uv
Write-Host "[检查] uv 环境..." -ForegroundColor Yellow
$uvVersion = uv --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 未检测到uv，请先安装uv" -ForegroundColor Red
    Write-Host "  安装方式一: powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`"" -ForegroundColor White
    Write-Host "  安装方式二: winget install astral-sh.uv" -ForegroundColor White
    Write-Host "  详情: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor White
    Read-Host "按 Enter 退出"
    exit 1
}
Write-Host "[完成] $uvVersion" -ForegroundColor Green

# 检查Node.js
Write-Host "[检查] Node.js环境..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 未检测到Node.js，前端构建需要Node.js 16+" -ForegroundColor Yellow
    Write-Host "  下载地址: https://nodejs.org/" -ForegroundColor White
} else {
    Write-Host "[完成] Node.js $nodeVersion" -ForegroundColor Green
}

# 检查Cloudflare Tunnel
if ($mode -eq "local") {
    Write-Host "[检查] Cloudflare Tunnel环境..." -ForegroundColor Yellow
    $cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
    if (-not $cloudflared) {
        Write-Host "[警告] 未检测到cloudflared，内网穿透需要安装" -ForegroundColor Yellow
        Write-Host "  安装命令: winget install --id Cloudflare.cloudflared" -ForegroundColor White
    } else {
        Write-Host "[完成] Cloudflare Tunnel已安装" -ForegroundColor Green
    }
}

# ================================
# 步骤3: 配置环境变量
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤2: 配置环境变量" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

$envFile = Join-Path $ScriptDir ".env"
if (-not (Test-Path $envFile)) {
    $envExample = Join-Path $ScriptDir ".env.example"
    if (Test-Path $envExample) {
        Write-Host "[信息] 未找到 .env 文件，正在从 .env.example 创建..." -ForegroundColor Yellow
        Copy-Item $envExample $envFile
        Write-Host "[完成] 已创建 .env 文件" -ForegroundColor Green
        Write-Host ""
        Write-Host "请编辑 .env 文件，填入以下配置:" -ForegroundColor Yellow
        Write-Host "  1. TIKHUB_API_KEY - TikHub API密钥" -ForegroundColor White
        Write-Host "  2. DASHSCOPE_API_KEY - DashScope API密钥" -ForegroundColor White
        Write-Host ""
        Write-Host "按任意键打开 .env 文件进行编辑..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        notepad $envFile
        exit 0
    } else {
        Write-Host "[错误] 未找到 .env.example 文件" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
} else {
    Write-Host "[完成] .env 文件已存在" -ForegroundColor Green
}

# ================================
# 步骤4: 安装后端依赖
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤3: 安装后端依赖" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[信息] 同步虚拟环境和依赖 (uv sync)..." -ForegroundColor Yellow
uv sync
if (-not $?) {
    Write-Host "[错误] 同步依赖失败" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}
Write-Host "[完成] 依赖同步完成" -ForegroundColor Green

# ================================
# 步骤5: 构建前端
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤4: 构建前端" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "node_modules") {
    Write-Host "[完成] 前端依赖已存在" -ForegroundColor Green
} else {
    Write-Host "[信息] 安装前端依赖..." -ForegroundColor Yellow
    npm install
    if (-not $?) {
        Write-Host "[错误] 安装前端依赖失败" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
    Write-Host "[完成] 前端依赖安装完成" -ForegroundColor Green
}

Write-Host "[信息] 构建前端静态资源..." -ForegroundColor Yellow
npm run build
if (-not $?) {
    Write-Host "[错误] 前端构建失败" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}
Write-Host "[完成] 前端构建完成" -ForegroundColor Green

# ================================
# 步骤6: 启动后端服务
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤5: 启动后端服务" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# 读取端口配置
$backendPort = "8000"
$envContent = Get-Content $envFile | Where-Object { $_ -match "^BACKEND_PORT=" }
if ($envContent) {
    $backendPort = ($envContent -split "=")[1].Trim()
}

# 创建日志目录
$logDir = Join-Path $ScriptDir "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 设置虚拟环境
$venvPath = Join-Path $ScriptDir ".venv"
$venvScripts = Join-Path $venvPath "Scripts"
$env:VIRTUAL_ENV = $venvPath
$env:PATH = "$venvScripts;$env:PATH"

$timestamp = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId((Get-Date), "China Standard Time").ToString("yyyy-MM-dd_HHmmss")
$logFile = Join-Path $logDir "backend_$timestamp.log"
Write-Host "[信息] 启动后端服务 (端口: $backendPort)..." -ForegroundColor Yellow
Write-Host "[信息] 日志文件: $logFile" -ForegroundColor Yellow
Write-Host ""

# 启动后端（前台运行，同时输出到日志文件）
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port $backendPort --reload --log-level info 2>&1 | Tee-Object -FilePath $logFile -Append

Write-Host ""
Write-Host "[完成] 后端服务已停止" -ForegroundColor Yellow
Read-Host "按 Enter 退出"

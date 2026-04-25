# ============================================
# Collectly 一键部署脚本 (Windows PowerShell)
# 支持双部署模式：本地部署/云服务器部署
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

# 检查Python
Write-Host "[检查] Python环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 未检测到Python，请先安装Python 3.9+" -ForegroundColor Red
    Write-Host "  下载地址: https://www.python.org/downloads/" -ForegroundColor White
    Read-Host "按 Enter 退出"
    exit 1
}
Write-Host "[完成] $pythonVersion" -ForegroundColor Green

# 检查Node.js
Write-Host "[检查] Node.js环境..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 未检测到Node.js，前端构建需要Node.js 16+" -ForegroundColor Yellow
    Write-Host "  下载地址: https://nodejs.org/" -ForegroundColor White
} else {
    Write-Host "[完成] Node.js $nodeVersion" -ForegroundColor Green
}

# 检查.NET环境（Cloudflare Tunnel需要）
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

$envFile = Join-Path $ScriptDir "backend\.env"
$envExample = Join-Path $ScriptDir "backend\.env.example"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envExample) {
        Write-Host "[信息] 从.env.example创建.env文件..." -ForegroundColor Yellow
        Copy-Item $envExample $envFile
        Write-Host "[完成] .env文件已创建" -ForegroundColor Green
        Write-Host ""
        Write-Host "请编辑以下文件填写必要的API密钥:" -ForegroundColor Yellow
        Write-Host "  $envFile" -ForegroundColor White
        Write-Host ""
        $openEnv = Read-Host "是否现在打开编辑? (Y/N)"
        if ($openEnv -eq "Y" -or $openEnv -eq "y") {
            notepad $envFile
            Write-Host ""
            Write-Host "编辑完成后，按任意键继续..." -ForegroundColor Yellow
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    } else {
        Write-Host "[错误] 未找到.env.example文件" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[完成] .env文件已存在" -ForegroundColor Green
}

# ================================
# 步骤4: 安装后端依赖
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤3: 安装后端依赖" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Set-Location (Join-Path $ScriptDir "backend")

# 检查虚拟环境
$venvPath = Join-Path (Get-Location) ".venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "[信息] 创建Python虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 创建虚拟环境失败" -ForegroundColor Red
        exit 1
    }
    Write-Host "[完成] 虚拟环境已创建" -ForegroundColor Green
}

# 安装依赖
Write-Host "[信息] 安装Python依赖..." -ForegroundColor Yellow
$pip = Join-Path $venvPath "Scripts\pip"
& $pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 安装依赖失败" -ForegroundColor Red
    exit 1
}
Write-Host "[完成] 依赖安装完成" -ForegroundColor Green

# 创建日志目录
$logDir = Join-Path (Get-Location) "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 创建向量数据目录
$chromaDir = Join-Path (Get-Location) "chroma_data"
if (-not (Test-Path $chromaDir)) {
    New-Item -ItemType Directory -Path $chromaDir -Force | Out-Null
}

# ================================
# 步骤5: 构建前端
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤4: 构建前端" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Set-Location $ScriptDir

$frontendDir = Join-Path $ScriptDir "frontend"
if (-not (Test-Path $frontendDir)) {
    New-Item -ItemType Directory -Path $frontendDir -Force | Out-Null
}

# 更新前端环境变量
$frontendEnvFile = Join-Path $ScriptDir ".env"
if (-not (Test-Path $frontendEnvFile)) {
    Write-Host "[信息] 创建前端环境变量文件..." -ForegroundColor Yellow
    @"
REACT_APP_API_BASE_URL=http://localhost:8000/api
"@ | Set-Content -Path $frontendEnvFile -Encoding UTF8
    Write-Host "[完成] .env文件已创建" -ForegroundColor Green
}

# 安装前端依赖
Write-Host "[信息] 安装前端依赖..." -ForegroundColor Yellow
npm install --silent
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 前端依赖安装失败" -ForegroundColor Yellow
} else {
    Write-Host "[完成] 前端依赖安装完成" -ForegroundColor Green
}

# 构建前端
Write-Host "[信息] 构建前端..." -ForegroundColor Yellow
npm run build --silent
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 前端构建失败，将使用开发模式" -ForegroundColor Yellow
} else {
    Write-Host "[完成] 前端构建完成" -ForegroundColor Green
}

# ================================
# 步骤6: 启动服务
# ================================
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤5: 启动服务" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# 启动后端
Write-Host "[信息] 启动后端服务..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath (Join-Path $venvPath "Scripts\uvicorn") `
    -ArgumentList "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info" `
    -WorkingDirectory (Join-Path $ScriptDir "backend") `
    -WindowStyle Normal `
    -PassThru

Write-Host "[完成] 后端服务已启动 (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "  - API地址: http://localhost:8000" -ForegroundColor White
Write-Host "  - API文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""

# 等待后端启动
Start-Sleep -Seconds 3

# 启动前端（开发模式）
Write-Host "[信息] 启动前端服务..." -ForegroundColor Yellow
$frontendProcess = Start-Process -FilePath "npm" `
    -ArgumentList "run", "dev" `
    -WorkingDirectory $ScriptDir `
    -WindowStyle Normal `
    -PassThru

Write-Host "[完成] 前端服务已启动 (PID: $($frontendProcess.Id))" -ForegroundColor Green
Write-Host "  - 前端地址: http://localhost:3266" -ForegroundColor White
Write-Host ""

# ================================
# 步骤7: 配置内网穿透（仅方案A）
# ================================
if ($mode -eq "local") {
    Write-Host ""
    Write-Host "=============================" -ForegroundColor Cyan
    Write-Host "  步骤6: 配置内网穿透" -ForegroundColor Cyan
    Write-Host "=============================" -ForegroundColor Cyan
    Write-Host ""

    $cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
    if ($cloudflared) {
        Write-Host "[信息] 启动Cloudflare Tunnel..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "说明:" -ForegroundColor Yellow
        Write-Host "  - 请在浏览器中完成Tunnel认证" -ForegroundColor White
        Write-Host "  - 完成后会生成公网HTTPS地址" -ForegroundColor White
        Write-Host "  - 将该地址填入前端.env文件的REACT_APP_API_BASE_URL" -ForegroundColor White
        Write-Host ""
        
        Start-Process -FilePath "cloudflared" `
            -ArgumentList "tunnel", "--url", "http://localhost:8000" `
            -WindowStyle Normal
    } else {
        Write-Host "[信息] 内网穿透需要安装cloudflared" -ForegroundColor Yellow
        Write-Host "  安装命令: winget install --id Cloudflare.cloudflared" -ForegroundColor White
        Write-Host "  或手动下载: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/" -ForegroundColor White
    }
}

# ================================
# 完成
# ================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  部署完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if ($mode -eq "local") {
    Write-Host "访问地址:" -ForegroundColor Yellow
    Write-Host "  - 前端: http://localhost:3266" -ForegroundColor White
    Write-Host "  - 后端API: http://localhost:8000" -ForegroundColor White
    Write-Host "  - API文档: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "进程信息:" -ForegroundColor Yellow
    Write-Host "  - 后端PID: $($backendProcess.Id)" -ForegroundColor White
    Write-Host "  - 前端PID: $($frontendProcess.Id)" -ForegroundColor White
    Write-Host ""
    Write-Host "停止服务:" -ForegroundColor Yellow
    Write-Host "  Stop-Process -Id $($backendProcess.Id)" -ForegroundColor White
    Write-Host "  Stop-Process -Id $($frontendProcess.Id)" -ForegroundColor White
    Write-Host ""
    Write-Host "后续步骤:" -ForegroundColor Yellow
    Write-Host "  1. 完成Cloudflare Tunnel配置获取公网地址" -ForegroundColor White
    Write-Host "  2. 更新前端.env文件的API地址" -ForegroundColor White
    Write-Host "  3. 通过公网地址访问服务" -ForegroundColor White
} else {
    Write-Host "访问地址:" -ForegroundColor Yellow
    Write-Host "  - 前端: 云服务器公网IP:3266" -ForegroundColor White
    Write-Host "  - 后端API: 云服务器公网IP:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "注意事项:" -ForegroundColor Yellow
    Write-Host "  1. 确保云服务器防火墙开放3266和8000端口" -ForegroundColor White
    Write-Host "  2. 建议配置域名和HTTPS证书" -ForegroundColor White
    Write-Host "  3. 可使用Nginx反向代理统一端口" -ForegroundColor White
}

Write-Host ""
Write-Host "按 Enter 键退出..." -ForegroundColor Yellow
Read-Host

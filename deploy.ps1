# ============================================
# Collectly 一键部署脚本 (Windows PowerShell)
# ============================================
# 支持两种部署模式：
#   方案A：本地部署 + 内网穿透（Cloudflare Tunnel）
#   方案B：云服务器公网部署
# ============================================

param(
    [ValidateSet("A", "B")]
    [string]$Mode = "A",
    [switch]$SkipFrontend,
    [switch]$SkipBackend,
    [switch]$Help
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = $ProjectRoot

function Write-Color {
    param($Color, $Message)
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-Color Cyan "============================================"
    Write-Color Cyan "  Collectly 一键部署脚本"
    Write-Color Cyan "============================================"
    Write-Host ""
    Write-Host "用法: .\deploy.ps1 [-Mode A|B] [-SkipFrontend] [-SkipBackend] [-Help]"
    Write-Host ""
    Write-Host "参数说明:"
    Write-Host "  -Mode A       方案A：本地部署 + 内网穿透（默认）"
    Write-Host "  -Mode B       方案B：云服务器公网部署"
    Write-Host "  -SkipFrontend 跳过前端构建"
    Write-Host "  -SkipBackend  跳过后端部署"
    Write-Host "  -Help         显示此帮助"
    Write-Host ""
    Write-Host "方案A 适用场景：个人电脑本地运行，通过 Cloudflare Tunnel 外网访问"
    Write-Host "方案B 适用场景：云服务器 24h 在线运行，直接公网访问"
    Write-Host ""
    exit 0
}

if ($Help) {
    Show-Help
}

Write-Color Green "============================================"
Write-Color Green "  Collectly 一键部署脚本"
Write-Color Green "  模式：方案$(if ($Mode -eq 'A') { 'A - 本地部署 + 内网穿透' } else { 'B - 云服务器公网部署' })"
Write-Color Green "============================================"
Write-Host ""

# ============================================
# 步骤 1：检查环境
# ============================================
Write-Color Yellow "[1/6] 检查运行环境..."

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Color Green "  ✓ Python: $pythonVersion"
} catch {
    Write-Color Red "  ✗ Python 未安装，请安装 Python 3.8+"
    exit 1
}

# 检查 Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Color Green "  ✓ Node.js: $nodeVersion"
} catch {
    Write-Color Red "  ✗ Node.js 未安装，请安装 Node.js 16+"
    exit 1
}

# 检查 npm
try {
    $npmVersion = npm --version 2>&1
    Write-Color Green "  ✓ npm: $npmVersion"
} catch {
    Write-Color Red "  ✗ npm 未安装"
    exit 1
}

Write-Host ""

# ============================================
# 步骤 2：配置环境变量
# ============================================
Write-Color Yellow "[2/6] 配置环境变量..."

$envFile = Join-Path $BackendDir ".env"
if (-not (Test-Path $envFile)) {
    $envExample = Join-Path $BackendDir ".env.example"
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Color Yellow "  ! 已从 .env.example 创建 .env 文件"
        Write-Color Yellow "  ! 请编辑 backend\.env 填写 API Key 后重新运行"
        Write-Color Yellow "  ! 按任意键打开文件编辑，或 Ctrl+C 退出"
        pause
        notepad $envFile
        exit 0
    } else {
        Write-Color Red "  ✗ 未找到 .env.example 文件"
        exit 1
    }
} else {
    Write-Color Green "  ✓ .env 文件已存在"
}

Write-Host ""

# ============================================
# 步骤 3：安装后端依赖
# ============================================
if (-not $SkipBackend) {
    Write-Color Yellow "[3/6] 安装后端依赖..."

    Set-Location $BackendDir

    # 检查虚拟环境
    $venvPath = Join-Path $BackendDir ".venv"
    if (-not (Test-Path $venvPath)) {
        Write-Host "  - 创建 Python 虚拟环境..."
        python -m venv .venv
        if (-not $?) {
            Write-Color Red "  ✗ 创建虚拟环境失败"
            exit 1
        }
        Write-Color Green "  ✓ 虚拟环境已创建"
    } else {
        Write-Color Green "  ✓ 虚拟环境已存在"
    }

    # 安装依赖
    Write-Host "  - 安装 Python 依赖..."
    $pip = Join-Path $venvPath "Scripts\pip"
    & $pip install -r requirements.txt --quiet
    if (-not $?) {
        Write-Color Red "  ✗ 安装依赖失败"
        exit 1
    }
    Write-Color Green "  ✓ Python 依赖安装完成"

    Set-Location $ProjectRoot
} else {
    Write-Color Yellow "[3/6] 跳过后端依赖安装"
}

Write-Host ""

# ============================================
# 步骤 4：构建前端
# ============================================
if (-not $SkipFrontend) {
    Write-Color Yellow "[4/6] 构建前端..."

    Set-Location $FrontendDir

    # 检查 node_modules
    if (-not (Test-Path "node_modules")) {
        Write-Host "  - 安装前端依赖..."
        npm install
        if (-not $?) {
            Write-Color Red "  ✗ 安装前端依赖失败"
            exit 1
        }
        Write-Color Green "  ✓ 前端依赖安装完成"
    } else {
        Write-Color Green "  ✓ 前端依赖已存在"
    }

    # 构建前端
    Write-Host "  - 构建前端静态资源..."
    npm run build
    if (-not $?) {
        Write-Color Red "  ✗ 前端构建失败"
        exit 1
    }
    Write-Color Green "  ✓ 前端构建完成（输出目录：dist/）"

    Set-Location $ProjectRoot
} else {
    Write-Color Yellow "[4/6] 跳过前端构建"
}

Write-Host ""

# ============================================
# 步骤 5：启动后端服务
# ============================================
Write-Color Yellow "[5/6] 启动后端服务..."

$backendPort = "8000"
$envContent = Get-Content $envFile | Where-Object { $_ -match "^BACKEND_PORT=" }
if ($envContent) {
    $backendPort = ($envContent -split "=")[1].Trim()
}

$uvicornPath = Join-Path $BackendDir ".venv\Scripts\uvicorn"
$logDir = Join-Path $BackendDir "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

Write-Host "  - 后端服务端口：$backendPort"
Write-Host "  - 日志目录：$logDir"

# 启动后端（后台运行）
$backendJob = Start-Job -ScriptBlock {
    param($uvicornPath, $backendDir, $backendPort)
    Set-Location $backendDir
    & $uvicornPath app.main:app --host 0.0.0.0 --port $backendPort --log-level info
} -ArgumentList $uvicornPath, $BackendDir, $backendPort

Write-Color Green "  ✓ 后端服务已启动（后台运行）"
Write-Host ""

# ============================================
# 步骤 6：配置内网穿透（方案A）或完成部署（方案B）
# ============================================
if ($Mode -eq "A") {
    Write-Color Yellow "[6/6] 配置内网穿透（方案A）..."

    # 检查 cloudflared
    $cloudflaredPath = Get-Command "cloudflared" -ErrorAction SilentlyContinue
    if (-not $cloudflaredPath) {
        Write-Color Yellow "  ! 未检测到 cloudflared"
        Write-Host "    是否安装 Cloudflare Tunnel？(y/n, 默认 n): " -NoNewline
        $installTunnel = Read-Host
        if ($installTunnel -eq "y") {
            Write-Host "  - 下载 cloudflared..."
            $installerUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            $installerPath = Join-Path $env:TEMP "cloudflared.exe"
            try {
                Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
                $targetDir = "$env:ProgramFiles\Cloudflare"
                if (-not (Test-Path $targetDir)) {
                    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                }
                Move-Item $installerPath (Join-Path $targetDir "cloudflared.exe") -Force
                $env:Path += ";$targetDir"
                [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
                Write-Color Green "  ✓ cloudflared 安装完成"
            } catch {
                Write-Color Red "  ✗ 安装失败，请手动安装：https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
            }
        } else {
            Write-Color Yellow "  ! 跳过内网穿透配置"
            Write-Host "    如需外网访问，请手动配置 Cloudflare Tunnel 或 ngrok"
        }
    } else {
        Write-Color Green "  ✓ cloudflared 已安装"
        Write-Host ""
        Write-Host "  使用以下命令启动内网穿透："
        Write-Host "    cloudflared tunnel --url http://localhost:$backendPort"
        Write-Host ""
        Write-Host "  或使用 ngrok："
        Write-Host "    ngrok http $backendPort"
    }
} else {
    Write-Color Yellow "[6/6] 方案B 部署完成"
    Write-Host ""
    Write-Color Green "  ✓ 后端服务已在端口 $backendPort 启动"
    Write-Host ""
    Write-Host "  请确保云服务器防火墙已放行端口 $backendPort"
    Write-Host "  建议使用 Nginx 反向代理并配置 HTTPS："
    Write-Host "    server {"
    Write-Host "        listen 443 ssl;"
    Write-Host "        server_name your-domain.com;"
    Write-Host "        location / {"
    Write-Host "            proxy_pass http://127.0.0.1:$backendPort;"
    Write-Host "            proxy_set_header Host `$host;"
    Write-Host "            proxy_set_header X-Real-IP `$remote_addr;"
    Write-Host "        }"
    Write-Host "    }"
}

Write-Host ""
Write-Color Green "============================================"
Write-Color Green "  部署完成！"
Write-Color Green "============================================"
Write-Host ""
Write-Host "  后端 API 地址：http://localhost:$backendPort"
Write-Host "  API 文档：http://localhost:$backendPort/docs"
Write-Host "  前端地址：http://localhost:3266（开发模式）"
if (Test-Path (Join-Path $FrontendDir "dist\index.html")) {
    Write-Host "  前端静态文件：$FrontendDir\dist"
}
Write-Host ""
Write-Host "  管理命令："
Write-Host "    停止后端：Stop-Job -Id $($backendJob.Id)"
Write-Host "    查看日志：Get-Content .\backend\logs\app_*.log -Tail 50"
Write-Host ""

# 等待用户按任意键退出
Write-Host "按任意键退出..." -NoNewline
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

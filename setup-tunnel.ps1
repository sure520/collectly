# ============================================
# Cloudflare Tunnel 配置脚本（Windows）
# 用于本地部署模式的外网访问
# ============================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cloudflare Tunnel 配置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 步骤1: 检查cloudflared
Write-Host "[检查] 安装状态..." -ForegroundColor Yellow
$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflared) {
    Write-Host "[信息] 未检测到cloudflared，正在安装..." -ForegroundColor Yellow
    Write-Host ""
    
    # 使用winget安装
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "[信息] 使用winget安装cloudflared..." -ForegroundColor Yellow
        winget install --id Cloudflare.cloudflared --accept-source-agreements --accept-package-agreements
    } else {
        Write-Host "[错误] 未检测到winget，请手动安装:" -ForegroundColor Red
        Write-Host "  1. 访问: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/" -ForegroundColor White
        Write-Host "  2. 下载Windows版本" -ForegroundColor White
        Write-Host "  3. 将cloudflared.exe添加到PATH" -ForegroundColor White
        exit 1
    }
}

Write-Host "[完成] cloudflared已安装" -ForegroundColor Green

# 步骤2: 创建Tunnel
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤1: 创建Tunnel" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

$tunnelName = "collectly-tunnel"
Write-Host "[信息] Tunnel名称: $tunnelName" -ForegroundColor White
Write-Host ""

$createConfirm = Read-Host "是否创建新Tunnel? (Y/N)"
if ($createConfirm -eq "Y" -or $createConfirm -eq "y") {
    Write-Host "[信息] 正在创建Tunnel..." -ForegroundColor Yellow
    $tunnelOutput = cloudflared tunnel create $tunnelName 2>&1
    Write-Host "[完成] Tunnel创建成功" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tunnel信息:" -ForegroundColor Yellow
    $tunnelOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    Write-Host ""
}

# 步骤3: 配置Tunnel路由
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤2: 配置路由" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[信息] 正在配置Tunnel路由到本地后端..." -ForegroundColor Yellow
Write-Host "  后端地址: http://localhost:8000" -ForegroundColor White
Write-Host ""

# 创建配置文件
$configDir = "$env:USERPROFILE\.cloudflared"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

$configFile = Join-Path $configDir "config.yml"
@"
tunnel: $tunnelName
credentials-file: $configDir/$tunnelName.json

ingress:
  - hostname: collectly.example.com
    service: http://localhost:8000
  - service: http_status:404
"@ | Set-Content -Path $configFile -Encoding UTF8

Write-Host "[完成] Tunnel配置文件已创建: $configFile" -ForegroundColor Green

# 步骤4: 启动Tunnel
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "  步骤3: 启动Tunnel" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[信息] 正在启动Cloudflare Tunnel..." -ForegroundColor Yellow
Write-Host ""
Write-Host "说明:" -ForegroundColor Yellow
Write-Host "  - 首次运行需要在浏览器中完成Cloudflare登录认证" -ForegroundColor White
Write-Host "  - 认证成功后Tunnel将自动连接" -ForegroundColor White
Write-Host "  - 请记录生成的公网HTTPS地址" -ForegroundColor White
Write-Host ""

Start-Process -FilePath "cloudflared" `
    -ArgumentList "tunnel", "run", $tunnelName `
    -WindowStyle Normal

Write-Host "[完成] Tunnel启动窗口已打开" -ForegroundColor Green
Write-Host ""
Write-Host "后续步骤:" -ForegroundColor Yellow
Write-Host "  1. 在浏览器中完成Cloudflare认证" -ForegroundColor White
Write-Host "  2. 记录生成的公网HTTPS地址" -ForegroundColor White
Write-Host "  3. 更新前端.env文件的API地址" -ForegroundColor White
Write-Host ""
Write-Host "按 Enter 键退出..." -ForegroundColor Yellow
Read-Host

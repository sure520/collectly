#!/bin/bash
# ============================================
# Collectly 一键部署脚本 (Linux/macOS)
# 支持双部署模式：本地部署/云服务器部署
# 使用 uv 管理 Python 虚拟环境
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Collectly 一键部署脚本${NC}"
echo -e "${CYAN}  AI驱动的个人知识收藏与检索管家${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# ================================
# 步骤1: 选择部署模式
# ================================
echo -e "${YELLOW}请选择部署模式:${NC}"
echo "  [A] 方案A - 本地部署 + 内网穿透（推荐个人使用，零成本）"
echo "  [B] 方案B - 云服务器公网部署（推荐24h在线，稳定性强）"
echo ""
read -p "请输入选项 (A/B): " DEPLOY_MODE

if [ "$DEPLOY_MODE" = "A" ] || [ "$DEPLOY_MODE" = "a" ]; then
    MODE="local"
    echo ""
    echo -e "${GREEN}[信息] 已选择: 方案A - 本地部署 + 内网穿透${NC}"
    echo ""
    echo -e "${YELLOW}说明:${NC}"
    echo "  - 后端运行在本地电脑"
    echo "  - 使用Cloudflare Tunnel实现外网访问"
    echo "  - 支持电脑息屏运行，无需全天开机"
    echo "  - 数据完全私有化，不离开个人设备"
    echo ""
elif [ "$DEPLOY_MODE" = "B" ] || [ "$DEPLOY_MODE" = "b" ]; then
    MODE="cloud"
    echo ""
    echo -e "${GREEN}[信息] 已选择: 方案B - 云服务器公网部署${NC}"
    echo ""
    echo -e "${YELLOW}说明:${NC}"
    echo "  - 后端运行在云服务器"
    echo "  - 通过固定公网IP/域名访问"
    echo "  - 24h永久在线，稳定性最强"
    echo "  - 需要云服务器（推荐轻量应用服务器）"
    echo ""
else
    echo -e "${RED}[错误] 无效选项，默认使用方案A${NC}"
    MODE="local"
fi

# ================================
# 步骤2: 检查环境
# ================================
echo ""
echo -e "${CYAN}=============================${NC}"
echo -e "${CYAN}  步骤1: 检查运行环境${NC}"
echo -e "${CYAN}=============================${NC}"
echo ""

# 检查 uv
echo -e "${YELLOW}[检查] uv 环境...${NC}"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}[完成] $(uv --version)${NC}"
else
    echo -e "${RED}[错误] 未检测到 uv，请先安装 uv${NC}"
    echo "  安装: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  详情: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# 检查 Node.js
echo -e "${YELLOW}[检查] Node.js 环境...${NC}"
if command -v node &> /dev/null; then
    echo -e "${GREEN}[完成] Node.js $(node --version)${NC}"
else
    echo -e "${YELLOW}[警告] 未检测到 Node.js，前端构建需要 Node.js 16+${NC}"
    echo "  安装: https://nodejs.org/"
fi

# 检查 Cloudflare Tunnel
if [ "$MODE" = "local" ]; then
    echo -e "${YELLOW}[检查] Cloudflare Tunnel 环境...${NC}"
    if command -v cloudflared &> /dev/null; then
        echo -e "${GREEN}[完成] Cloudflare Tunnel 已安装${NC}"
    else
        echo -e "${YELLOW}[警告] 未检测到 cloudflared，内网穿透需要安装${NC}"
        echo "  macOS: brew install cloudflared"
        echo "  Linux: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
    fi
fi

# ================================
# 步骤3: 配置环境变量
# ================================
echo ""
echo -e "${CYAN}=============================${NC}"
echo -e "${CYAN}  步骤2: 配置环境变量${NC}"
echo -e "${CYAN}=============================${NC}"
echo ""

ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    ENV_EXAMPLE="$SCRIPT_DIR/.env.example"
    if [ -f "$ENV_EXAMPLE" ]; then
        echo -e "${YELLOW}[信息] 未找到 .env 文件，正在从 .env.example 创建...${NC}"
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo -e "${GREEN}[完成] 已创建 .env 文件${NC}"
        echo ""
        echo -e "${YELLOW}请编辑 .env 文件，填入以下配置:${NC}"
        echo "  1. TIKHUB_API_KEY - TikHub API密钥"
        echo "  2. DASHSCOPE_API_KEY - DashScope API密钥"
        echo ""
        echo -e "${YELLOW}编辑命令: nano $ENV_FILE${NC}"
        exit 0
    else
        echo -e "${RED}[错误] 未找到 .env.example 文件${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}[完成] .env 文件已存在${NC}"
fi

# ================================
# 步骤4: 安装后端依赖
# ================================
echo ""
echo -e "${CYAN}=============================${NC}"
echo -e "${CYAN}  步骤3: 安装后端依赖${NC}"
echo -e "${CYAN}=============================${NC}"
echo ""

echo -e "${YELLOW}[信息] 同步虚拟环境和依赖 (uv sync)...${NC}"
uv sync
echo -e "${GREEN}[完成] 依赖同步完成${NC}"

# ================================
# 步骤5: 构建前端
# ================================
echo ""
echo -e "${CYAN}=============================${NC}"
echo -e "${CYAN}  步骤4: 构建前端${NC}"
echo -e "${CYAN}=============================${NC}"
echo ""

if [ -d "node_modules" ]; then
    echo -e "${GREEN}[完成] 前端依赖已存在${NC}"
else
    echo -e "${YELLOW}[信息] 安装前端依赖...${NC}"
    npm install
    echo -e "${GREEN}[完成] 前端依赖安装完成${NC}"
fi

echo -e "${YELLOW}[信息] 构建前端静态资源...${NC}"
npm run build
echo -e "${GREEN}[完成] 前端构建完成${NC}"

# ================================
# 步骤6: 启动后端服务
# ================================
echo ""
echo -e "${CYAN}=============================${NC}"
echo -e "${CYAN}  步骤5: 启动后端服务${NC}"
echo -e "${CYAN}=============================${NC}"
echo ""

BACKEND_PORT="8000"
if grep -q "^BACKEND_PORT=" "$ENV_FILE" 2>/dev/null; then
    BACKEND_PORT=$(grep "^BACKEND_PORT=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '[:space:]')
fi
[ -z "$BACKEND_PORT" ] && BACKEND_PORT="8000"

LOG_DIR="$SCRIPT_DIR/logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

echo -e "${YELLOW}[信息] 启动后端服务 (端口: $BACKEND_PORT)...${NC}"
echo ""

uv run uvicorn backend.app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload --log-level info

echo ""
echo -e "${YELLOW}[完成] 后端服务已停止${NC}"

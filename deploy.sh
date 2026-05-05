#!/bin/bash
# ============================================
# Collectly 一键部署脚本 (Linux/macOS)
# ============================================
# 支持两种部署模式：
#   方案A：本地部署 + 内网穿透（Cloudflare Tunnel）
#   方案B：云服务器公网部署
# 使用 uv 管理 Python 虚拟环境
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 默认参数
MODE="A"
SKIP_FRONTEND=false
SKIP_BACKEND=false

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -Mode|--mode)
            MODE="$2"
            shift 2
            ;;
        -SkipFrontend|--skip-frontend)
            SKIP_FRONTEND=true
            shift
            ;;
        -SkipBackend|--skip-backend)
            SKIP_BACKEND=true
            shift
            ;;
        -Help|--help)
            echo "============================================"
            echo "  Collectly 一键部署脚本"
            echo "============================================"
            echo ""
            echo "用法: ./deploy.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --mode A|B       方案A：本地+内网穿透（默认），方案B：云服务器"
            echo "  --skip-frontend  跳过前端构建"
            echo "  --skip-backend   跳过后端部署"
            echo "  --help           显示此帮助"
            echo ""
            echo "方案A 适用场景：个人电脑本地运行，通过 Cloudflare Tunnel 外网访问"
            echo "方案B 适用场景：云服务器 24h 在线运行，直接公网访问"
            echo ""
            echo "前置要求: uv（Python 包管理器）"
            echo "  安装: curl -LsSf https://astral.sh/uv/install.sh | sh"
            echo "  详情: https://docs.astral.sh/uv/getting-started/installation/"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Collectly 一键部署脚本${NC}"
echo -e "${GREEN}  模式：方案$(if [ "$MODE" = "A" ]; then echo 'A - 本地部署 + 内网穿透'; else echo 'B - 云服务器公网部署'; fi)${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

# ============================================
# 步骤 1：检查环境
# ============================================
echo -e "${YELLOW}[1/6] 检查运行环境...${NC}"

# 检查 uv
if command -v uv &> /dev/null; then
    echo -e "${GREEN}  ✓ uv: $(uv --version)${NC}"
else
    echo -e "${RED}  ✗ uv 未安装，请先安装 uv${NC}"
    echo "    安装: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "    详情: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# 检查 Node.js
if command -v node &> /dev/null; then
    echo -e "${GREEN}  ✓ Node.js: $(node --version)${NC}"
else
    echo -e "${RED}  ✗ Node.js 未安装，请安装 Node.js 16+${NC}"
    exit 1
fi

# 检查 npm
if command -v npm &> /dev/null; then
    echo -e "${GREEN}  ✓ npm: $(npm --version)${NC}"
else
    echo -e "${RED}  ✗ npm 未安装${NC}"
    exit 1
fi

echo ""

# ============================================
# 步骤 2：配置环境变量
# ============================================
echo -e "${YELLOW}[2/6] 配置环境变量...${NC}"

ENV_FILE="$PROJECT_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
    ENV_EXAMPLE="$PROJECT_ROOT/.env.example"
    if [ -f "$ENV_EXAMPLE" ]; then
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo -e "${YELLOW}  ! 已从 .env.example 创建 .env 文件${NC}"
        echo -e "${YELLOW}  ! 请编辑 .env 填写 API Key 后重新运行${NC}"
        echo -e "${YELLOW}  ! 编辑命令：nano $ENV_FILE${NC}"
        exit 0
    else
        echo -e "${RED}  ✗ 未找到 .env.example 文件${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}  ✓ .env 文件已存在${NC}"
fi

echo ""

# ============================================
# 步骤 3：安装后端依赖
# ============================================
if [ "$SKIP_BACKEND" = false ]; then
    echo -e "${YELLOW}[3/6] 安装后端依赖...${NC}"

    cd "$PROJECT_ROOT"

    echo "  - 同步虚拟环境和依赖 (uv sync)..."
    uv sync
    if [ $? -ne 0 ]; then
        echo -e "${RED}  ✗ 同步依赖失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}  ✓ Python 依赖安装完成（uv sync）${NC}"

    cd "$PROJECT_ROOT"
else
    echo -e "${YELLOW}[3/6] 跳过后端依赖安装${NC}"
fi

echo ""

# ============================================
# 步骤 4：构建前端
# ============================================
if [ "$SKIP_FRONTEND" = false ]; then
    echo -e "${YELLOW}[4/6] 构建前端...${NC}"

    cd "$FRONTEND_DIR"

    # 检查 node_modules
    if [ ! -d "node_modules" ]; then
        echo "  - 安装前端依赖..."
        npm install
        echo -e "${GREEN}  ✓ 前端依赖安装完成${NC}"
    else
        echo -e "${GREEN}  ✓ 前端依赖已存在${NC}"
    fi

    # 构建前端
    echo "  - 构建前端静态资源..."
    npm run build
    echo -e "${GREEN}  ✓ 前端构建完成（输出目录：dist/）${NC}"

    cd "$PROJECT_ROOT"
else
    echo -e "${YELLOW}[4/6] 跳过前端构建${NC}"
fi

echo ""

# ============================================
# 步骤 5：启动后端服务
# ============================================
echo -e "${YELLOW}[5/6] 启动后端服务...${NC}"

BACKEND_PORT="8000"
if grep -q "^BACKEND_PORT=" "$ENV_FILE" 2>/dev/null; then
    BACKEND_PORT=$(grep "^BACKEND_PORT=" "$ENV_FILE" | cut -d'=' -f2)
fi

LOG_DIR="$PROJECT_ROOT/logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

LOG_FILE="$LOG_DIR/backend_$(TZ='Asia/Shanghai' date '+%Y-%m-%d_%H%M%S').log"

echo "  - 后端服务端口：$BACKEND_PORT"
echo "  - 日志目录：$LOG_DIR"
echo "  - 日志文件：$LOG_FILE"

# 启动后端（后台运行）
cd "$PROJECT_ROOT"
nohup uv run uvicorn backend.app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --log-level info > "$LOG_FILE" 2>&1 &
BACKEND_PID=$!

echo -e "${GREEN}  ✓ 后端服务已启动（PID: $BACKEND_PID）${NC}"
echo ""

# ============================================
# 步骤 6：配置内网穿透（方案A）或完成部署（方案B）
# ============================================
if [ "$MODE" = "A" ]; then
    echo -e "${YELLOW}[6/6] 配置内网穿透（方案A）...${NC}"

    # 检查 cloudflared
    if command -v cloudflared &> /dev/null; then
        echo -e "${GREEN}  ✓ cloudflared 已安装${NC}"
        echo ""
        echo "  使用以下命令启动内网穿透："
        echo "    cloudflared tunnel --url http://localhost:$BACKEND_PORT"
        echo ""
        echo "  或使用 ngrok："
        echo "    ngrok http $BACKEND_PORT"
    else
        echo -e "${YELLOW}  ! 未检测到 cloudflared${NC}"
        echo "    如需外网访问，请手动安装 cloudflared 或 ngrok"
        echo "    cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
    fi
else
    echo -e "${YELLOW}[6/6] 方案B 部署完成${NC}"
    echo ""
    echo -e "${GREEN}  ✓ 后端服务已在端口 $BACKEND_PORT 启动${NC}"
    echo ""
    echo "  请确保云服务器防火墙已放行端口 $BACKEND_PORT"
    echo "  建议使用 Nginx 反向代理并配置 HTTPS"
fi

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "  后端 API 地址：http://localhost:$BACKEND_PORT"
echo "  API 文档：http://localhost:$BACKEND_PORT/docs"
echo "  前端地址：http://localhost:3266（开发模式）"
if [ -f "$FRONTEND_DIR/dist/index.html" ]; then
    echo "  前端静态文件：$FRONTEND_DIR/dist"
fi
echo ""
echo "  管理命令："
echo "    停止后端：kill $BACKEND_PID"
echo "    查看日志：tail -f $LOG_FILE"
echo ""

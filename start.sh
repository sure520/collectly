#!/bin/bash
# ============================================
# Collectly 后端启动脚本 (Linux/macOS)
# 使用 uv 管理虚拟环境
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Collectly 后端启动脚本${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

if ! command -v uv &> /dev/null; then
    echo -e "${RED}[错误] 未检测到 uv，请先安装 uv${NC}"
    echo ""
    echo "安装方式："
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "详情请参考: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    ENV_EXAMPLE="$SCRIPT_DIR/.env.example"
    if [ -f "$ENV_EXAMPLE" ]; then
        echo -e "${YELLOW}[警告] 未找到 .env 文件${NC}"
        echo -e "${YELLOW}正在从 .env.example 创建 .env 文件...${NC}"
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo -e "${YELLOW}请编辑 .env 文件填写 API Key 后重新运行${NC}"
        echo -e "${YELLOW}编辑命令: nano $ENV_FILE${NC}"
        exit 1
    else
        echo -e "${RED}[错误] 未找到 .env 和 .env.example 文件${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}[信息] 同步 Python 依赖 (uv sync)...${NC}"
uv sync --inexact
if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] 同步依赖失败${NC}"
    exit 1
fi
echo -e "${GREEN}[完成] 依赖同步完成${NC}"

LOG_DIR="$SCRIPT_DIR/logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

BACKEND_PORT="8000"
if grep -q "^BACKEND_PORT=" "$ENV_FILE" 2>/dev/null; then
    BACKEND_PORT=$(grep "^BACKEND_PORT=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '[:space:]')
fi
[ -z "$BACKEND_PORT" ] && BACKEND_PORT="8000"

VENV_PATH="$SCRIPT_DIR/.venv"
export VIRTUAL_ENV="$VENV_PATH"
export PATH="$VENV_PATH/bin:$PATH"

echo ""
echo -e "${YELLOW}[信息] 启动后端服务...${NC}"
echo "  - 端口: $BACKEND_PORT"
echo "  - API: http://localhost:$BACKEND_PORT"
echo "  - 文档: http://localhost:$BACKEND_PORT/docs"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
echo ""

uv run uvicorn backend.app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload --log-level info

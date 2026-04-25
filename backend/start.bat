@echo off
chcp 65001 >nul

echo ============================================
echo  Collectly 后端启动脚本
echo ============================================
echo.

:: 切换到脚本所在目录
cd /d "%~dp0"

:: 检查 .env 文件
if not exist ".env" (
    if exist ".env.example" (
        echo [警告] 未找到 .env 文件
        echo 正在从 .env.example 创建 .env 文件...
        copy ".env.example" ".env" >nul
        echo 请编辑 .env 文件填写 API Key 后重新运行
        echo 按任意键打开 .env 文件...
        pause >nul
        start notepad.exe ".env"
        exit /b 1
    ) else (
        echo [错误] 未找到 .env 和 .env.example 文件
        pause
        exit /b 1
    )
)

:: 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo [信息] 创建 Python 虚拟环境...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [完成] 虚拟环境已创建
)

:: 安装/更新依赖
echo [信息] 检查 Python 依赖...
.venv\Scripts\pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)
echo [完成] 依赖检查完成

:: 创建日志目录
if not exist "logs" mkdir logs

:: 读取端口配置
set PORT=8000
for /f "tokens=2 delims==" %%a in ('findstr /b "BACKEND_PORT" .env 2^>nul') do set PORT=%%a
if "%PORT%"=="" set PORT=8000

echo.
echo [信息] 启动后端服务...
echo   - 端口: %PORT%
echo   - API: http://localhost:%PORT%
echo   - 文档: http://localhost:%PORT%/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

:: 启动服务
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port %PORT% --reload --log-level info

pause

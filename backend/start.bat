@echo off

echo Starting backend service...
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

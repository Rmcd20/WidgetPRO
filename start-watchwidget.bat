@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo Virtual environment not found. Run "uv sync" in this folder first.
    pause
    exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" -m watchwidget
exit /b 0

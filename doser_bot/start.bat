@echo off
chcp 65001 >nul
title Doser - Instagram Account Creator

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   💉  DOSER - Instagram Account Creator  💉                 ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo 📥 Checking requirements...
pip install -q -r requirements.txt

:: Run application
echo 🚀 Starting Doser...
echo.
python main.py

:: Deactivate
call venv\Scripts\deactivate.bat

pause

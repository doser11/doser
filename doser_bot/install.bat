@echo off
chcp 65001 >nul
title Doser Installation

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   💉  DOSER - Installation  💉                              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

:: Create directories
echo 📁 Creating directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "accounts" mkdir accounts
if not exist "proxies" mkdir proxies
if not exist "screenshots" mkdir screenshots

:: Create .env if not exists
if not exist ".env" (
    echo 📝 Creating .env file...
    (
        echo # Telegram Bot Configuration
        echo TELEGRAM_BOT_TOKEN=your_bot_token_here
        echo TELEGRAM_CHAT_ID=your_chat_id_here
        echo.
        echo # CAPTCHA Service ^(optional^)
        echo CAPTCHA_API_KEY=your_2captcha_key_here
    ) > .env.example
    echo ⚠️  Please edit .env.example and rename to .env
)

:: Create proxies.txt if not exists
if not exist "proxies.txt" (
    echo 📝 Creating proxies.txt...
    (
        echo # Add your proxies here ^(one per line^)
        echo # Format: type://user:pass@ip:port
        echo # http://user:password@192.168.1.1:8080
        echo # socks5://192.168.1.2:1080
    ) > proxies.txt.example
    echo ⚠️  Please edit proxies.txt.example and rename to proxies.txt
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     ✅ Installation Complete!                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo   1. Edit .env.example and add your bot token
echo   2. Rename .env.example to .env
echo   3. Run: start.bat
echo.

pause

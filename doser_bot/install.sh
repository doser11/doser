#!/bin/bash

# Doser Installation Script
# For Linux/macOS

clear

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   💉  DOSER - Installation  💉                              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3.8+"
    exit 1
fi

echo -e "${GREEN}✅ Python found${NC}"
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install requirements${NC}"
    exit 1
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p data logs accounts proxies screenshots

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env.example << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# CAPTCHA Service (optional)
CAPTCHA_API_KEY=your_2captcha_key_here
EOF
    echo -e "${YELLOW}⚠️  Please edit .env.example and rename to .env${NC}"
fi

# Create proxies.txt if not exists
if [ ! -f "proxies.txt" ]; then
    echo "📝 Creating proxies.txt..."
    cat > proxies.txt.example << 'EOF'
# Add your proxies here (one per line)
# Format: type://user:pass@ip:port
# http://user:password@192.168.1.1:8080
# socks5://192.168.1.2:1080
EOF
    echo -e "${YELLOW}⚠️  Please edit proxies.txt.example and rename to proxies.txt${NC}"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                     ✅ Installation Complete!                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Edit .env.example and add your bot token"
echo "  2. Rename .env.example to .env"
echo "  3. Run: ./start.sh"
echo ""

# Make scripts executable
chmod +x start.sh install.sh 2>/dev/null

#!/bin/bash

# Doser - Instagram Account Creator
# Startup Script for Linux/Mac

clear

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   💉  DOSER - Instagram Account Creator  💉                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Checking requirements..."
pip install -q -r requirements.txt

# Run application
echo "🚀 Starting Doser..."
echo ""
python3 main.py

# Deactivate
deactivate

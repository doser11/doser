#!/data/data/com.termux/files/usr/bin/bash
# Doser Quick Run Script for Termux
# Usage: ./termux_run.sh

clear

cd ~/doser 2>/dev/null || cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║                                                   ║"
echo "║     💉  D O S E R  -  Termux Edition  💉         ║"
echo "║                                                   ║"
echo "║     Instagram Account Creator                     ║"
echo "║                                                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Bot Token (Pre-configured)
TOKEN="8758353768:AAGPwX4AbKdBOLaMzolrFGF5IccEGa0GUaU"
echo -e "${GREEN}✅ Bot Token configured${NC}"
echo ""

# Menu
echo "Select mode:"
echo ""
echo "  1) Interactive Mode (CLI)"
echo "  2) Quick Create (1 account)"
echo "  3) Quick Create (5 accounts)"
echo "  4) Create with Follow"
echo "  5) Check Usernames"
echo "  6) View Accounts"
echo "  7) Test Bot Connection"
echo "  8) Exit"
echo ""
read -p "Enter choice [1-8]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🚀 Starting Interactive Mode...${NC}"
        echo ""
        python cli.py
        ;;
    2)
        echo ""
        echo -e "${BLUE}🚀 Creating 1 account...${NC}"
        echo ""
        python cli.py --token "$TOKEN" --count 1
        ;;
    3)
        echo ""
        echo -e "${BLUE}🚀 Creating 5 accounts...${NC}"
        echo ""
        python cli.py --token "$TOKEN" --count 5
        ;;
    4)
        echo ""
        read -p "Enter username to follow: " follow_user
        read -p "Number of accounts [1]: " acc_count
        acc_count=${acc_count:-1}
        echo ""
        echo -e "${BLUE}🚀 Creating $acc_count accounts and following @$follow_user...${NC}"
        echo ""
        python cli.py --token "$TOKEN" --count "$acc_count" --follow "$follow_user"
        ;;
    5)
        echo ""
        read -p "Number of usernames to check [10]: " check_count
        check_count=${check_count:-10}
        echo ""
        echo -e "${BLUE}🔍 Checking usernames...${NC}"
        echo ""
        python cli.py --mode usernames --count "$check_count"
        ;;
    6)
        echo ""
        echo -e "${BLUE}📋 Created Accounts:${NC}"
        echo ""
        if [ -f "accounts/accounts.json" ]; then
            cat accounts/accounts.json
        else
            echo "No accounts found."
        fi
        echo ""
        read -p "Press Enter to continue..."
        ;;
    7)
        echo ""
        echo -e "${BLUE}🔄 Testing bot connection...${NC}"
        echo ""
        python -c "
from core.email_bot import EmailBot
import sys
bot = EmailBot('$TOKEN')
if bot.test_connection():
    print('✅ Bot is working!')
    sys.exit(0)
else:
    print('❌ Bot connection failed!')
    sys.exit(1)
"
        echo ""
        read -p "Press Enter to continue..."
        ;;
    8)
        echo ""
        echo -e "${YELLOW}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}❌ Invalid choice!${NC}"
        exit 1
        ;;
esac

#!/usr/bin/env python3
"""
Doser - Instagram Account Creator
Main Entry Point

Usage:
    python main.py              - Launch Enhanced GUI
    python main.py --legacy     - Launch Legacy GUI
    python main.py --cli        - Launch CLI mode
    python main.py --version    - Show version
"""

import sys
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/doser.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print application banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     💉  D O S E R  💉                                        ║
║                                                              ║
║     Instagram Account Creator                                ║
║                                                              ║
║     Version 1.0.0                                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def check_dependencies():
    """Check if required dependencies are installed"""
    required = {
        'customtkinter': 'customtkinter',
        'selenium': 'selenium',
        'requests': 'requests',
        'PIL': 'pillow',
        'faker': 'faker',
        'undetected_chromedriver': 'undetected-chromedriver',
        'bs4': 'beautifulsoup4',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def run_enhanced_gui():
    """Run enhanced GUI mode"""
    try:
        from gui.enhanced_main_window import main
        main()
    except Exception as e:
        logger.error(f"Enhanced GUI Error: {e}")
        print(f"❌ Error starting Enhanced GUI: {e}")
        print("🔄 Falling back to Legacy GUI...")
        run_legacy_gui()


def run_legacy_gui():
    """Run legacy GUI mode"""
    try:
        from gui.main_window import main
        main()
    except Exception as e:
        logger.error(f"Legacy GUI Error: {e}")
        print(f"❌ Error starting Legacy GUI: {e}")
        sys.exit(1)


def run_cli():
    """Run CLI mode"""
    print_banner()
    
    try:
        from core.enhanced_instagram import EnhancedInstagramAutomation
        from core.email_bot import EmailBot
        from utils.proxy_manager import ProxyManager
        from utils.account_manager import AccountManager
        
        # Get inputs
        print("📋 Configuration:\n")
        bot_token = input("🔑 Telegram Bot Token: ").strip()
        chat_id = input("💬 Chat ID (optional): ").strip() or None
        
        try:
            count = int(input("📊 Number of accounts [1]: ") or "1")
        except ValueError:
            count = 1
        
        proxy_file = input("📁 Proxy file path (optional): ").strip() or None
        follow = input("👤 Account to follow (optional): ").strip() or None
        
        print()
        
        # Initialize
        proxy_manager = ProxyManager(proxy_file) if proxy_file else None
        email_bot = EmailBot(bot_token, chat_id)
        account_manager = AccountManager()
        
        print("🔄 Testing bot connection...")
        if not email_bot.test_connection():
            print("❌ Bot connection failed!")
            return
        print("✅ Bot connected!\n")
        
        # Create accounts
        automation = EnhancedInstagramAutomation(
            proxy_manager=proxy_manager,
            email_bot=email_bot,
            headless=False,
            account_manager=account_manager
        )
        
        results = automation.create_multiple_accounts(
            count=count,
            follow_username=follow
        )
        
        # Summary
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Accounts saved to: accounts/accounts.json")
        
        if successful > 0:
            print("\n📝 Created Accounts:")
            for r in results:
                if r['success']:
                    print(f"   - {r['username']}")
        
        print("\n✨ All done!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        logger.error(f"CLI Error: {e}")
        print(f"❌ Error: {e}")


def run_setup():
    """Run initial setup"""
    print_banner()
    print("🔧 Running initial setup...\n")
    
    # Create directories
    dirs = ['data', 'logs', 'accounts', 'proxies', 'screenshots']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
        print(f"  ✓ Created directory: {d}/")
    
    print("\n📄 Creating example files...")
    
    # Create .env.example if not exists
    if not Path('.env').exists():
        env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
"""
        Path('.env.example').write_text(env_content)
        print("  ✓ Created .env.example")
    
    # Create proxies.txt.example if not exists
    if not Path('proxies.txt').exists():
        proxy_content = """# Add your proxies here (one per line)
# Format: type://user:pass@ip:port
# http://user:password@192.168.1.1:8080
# socks5://192.168.1.2:1080
"""
        Path('proxies.txt.example').write_text(proxy_content)
        print("  ✓ Created proxies.txt.example")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("  1. Copy .env.example to .env and add your bot token")
    print("  2. Add proxies to proxies.txt (optional)")
    print("  3. Run: python main.py")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Doser - Instagram Account Creator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              Launch the GUI
  python main.py --cli        Run in CLI mode
  python main.py --setup      Run initial setup
  python main.py --version    Show version info
        """
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode'
    )
    parser.add_argument(
        '--legacy',
        action='store_true',
        help='Use legacy GUI instead of enhanced'
    )
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Run initial setup'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='Doser v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Run setup
    if args.setup:
        run_setup()
        return
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run mode
    if args.cli:
        run_cli()
    elif args.legacy:
        run_legacy_gui()
    else:
        run_enhanced_gui()


if __name__ == "__main__":
    main()

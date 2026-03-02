"""
Doser CLI - Command Line Interface
"""

import sys
import time
import random
import argparse
import logging
from pathlib import Path
from datetime import datetime

from core.enhanced_instagram import EnhancedInstagramAutomation
from core.email_bot import EmailBot
from utils.proxy_manager import ProxyManager
from utils.account_manager import AccountManager
from utils.generators import DataGenerator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print CLI banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     💉  D O S E R  -  CLI Mode  💉                          ║
║                                                              ║
║     Instagram Account Creator                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def print_progress(current, total, username=None, status=None):
    """Print progress bar"""
    width = 40
    progress = current / total
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    
    print(f"\r  [{bar}] {current}/{total}", end='')
    
    if username:
        print(f" - @{username}", end='')
    if status:
        print(f" ({status})", end='')
    
    if current == total:
        print()  # New line at end


def interactive_mode():
    """Interactive CLI mode"""
    print_banner()
    
    print("📋 Configuration:\n")
    
    # Get configuration
    config = {}
    config['bot_token'] = input("🔑 Telegram Bot Token: ").strip()
    config['chat_id'] = input("💬 Chat ID (optional): ").strip() or None
    
    try:
        config['count'] = int(input("📊 Number of accounts [1]: ") or "1")
    except ValueError:
        config['count'] = 1
    
    config['proxy_file'] = input("📁 Proxy file (optional): ").strip() or None
    
    # Advanced options
    print("\n⚙️ Advanced Options:")
    follow = input("  👤 Follow account (optional): ").strip()
    config['follow_username'] = follow if follow else None
    
    headless = input("  👻 Headless mode [y/N]: ").strip().lower()
    config['headless'] = headless == 'y'
    
    try:
        delay_min = int(input("  ⏱️  Min delay [30]: ") or "30")
        delay_max = int(input("  ⏱️  Max delay [60]: ") or "60")
        config['delay_range'] = (delay_min, delay_max)
    except ValueError:
        config['delay_range'] = (30, 60)
    
    print()
    
    # Confirm
    print("\n📋 Summary:")
    print(f"  Accounts: {config['count']}")
    print(f"  Proxy file: {config['proxy_file'] or 'None'}")
    print(f"  Follow: {config['follow_username'] or 'None'}")
    print(f"  Headless: {config['headless']}")
    print(f"  Delay: {config['delay_range'][0]}-{config['delay_range'][1]}s")
    
    confirm = input("\n✓ Start? [Y/n]: ").strip().lower()
    if confirm == 'n':
        print("❌ Cancelled")
        return
    
    # Run creation
    run_creation(config)


def run_creation(config):
    """Run account creation with config"""
    print("\n🚀 Starting...\n")
    
    # Initialize components
    try:
        proxy_manager = ProxyManager(config.get('proxy_file'))
        email_bot = EmailBot(config['bot_token'], config.get('chat_id'))
        account_manager = AccountManager()
        
        print("🔄 Testing bot connection...")
        if not email_bot.test_connection():
            print("❌ Bot connection failed!")
            return
        print("✅ Bot connected!\n")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Create automation
    automation = EnhancedInstagramAutomation(
        proxy_manager=proxy_manager,
        email_bot=email_bot,
        headless=config.get('headless', False),
        account_manager=account_manager
    )
    
    # Create accounts
    results = []
    count = config['count']
    
    for i in range(count):
        print(f"\n{'='*60}")
        print(f"Account {i+1}/{count}")
        print('='*60)
        
        result = automation.create_account(
            follow_username=config.get('follow_username')
        )
        results.append(result)
        
        # Show result
        if result['success']:
            print(f"✅ SUCCESS: @{result['username']}")
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        
        # Delay between accounts
        if i < count - 1:
            delay = random.randint(*config['delay_range'])
            print(f"\n⏱️  Waiting {delay} seconds...")
            time.sleep(delay)
    
    # Summary
    print_summary(results)


def print_summary(results):
    """Print creation summary"""
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"  ✅ Successful: {len(successful)}")
    print(f"  ❌ Failed: {len(failed)}")
    print(f"  📁 Accounts saved to: accounts/accounts.json")
    
    if successful:
        print("\n  📝 Created Accounts:")
        for r in successful:
            print(f"     - @{r['username']} | {r['email']}")
    
    if failed:
        print("\n  ❌ Failed Accounts:")
        for r in failed:
            error = r.get('error', 'Unknown')
            print(f"     - Error: {error[:50]}")
    
    print("\n✨ Done!")


def quick_mode(args):
    """Quick mode with command line arguments"""
    config = {
        'bot_token': args.token,
        'chat_id': args.chat_id,
        'count': args.count,
        'proxy_file': args.proxy_file,
        'follow_username': args.follow,
        'headless': args.headless,
        'delay_range': (args.delay_min, args.delay_max)
    }
    
    run_creation(config)


def check_usernames_mode(args):
    """Username checking mode"""
    print_banner()
    print(f"🔍 Generating {args.count} usernames...\n")
    
    generator = DataGenerator()
    
    for i in range(args.count):
        profile = generator.generate_complete_profile()
        print(f"  {i+1}. @{profile['username']}")
    
    print(f"\n✅ Generated {args.count} usernames")


def export_accounts_mode(args):
    """Export accounts mode"""
    am = AccountManager()
    
    if args.format == 'txt':
        am.export_to_txt(args.output)
    elif args.format == 'csv':
        am.export_to_csv(args.output)
    elif args.format == 'json':
        am.export_to_json(args.output)
    
    print(f"✅ Accounts exported to: {args.output}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Doser CLI - Instagram Account Creator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli.py
  
  # Quick creation
  python cli.py --token "YOUR_BOT_TOKEN" --count 5
  
  # With proxy and follow
  python cli.py -t "TOKEN" -c 3 --proxy proxies.txt --follow "target_user"
  
  # Generate usernames
  python cli.py --mode usernames --count 20
  
  # Export accounts
  python cli.py --mode export --format txt --output accounts.txt
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['create', 'usernames', 'export'],
        default='create',
        help='Operation mode (default: create)'
    )
    
    # Quick mode arguments
    parser.add_argument('-t', '--token', help='Telegram bot token')
    parser.add_argument('-c', '--chat-id', help='Telegram chat ID')
    parser.add_argument('-n', '--count', type=int, default=1, help='Number of accounts')
    parser.add_argument('-p', '--proxy-file', help='Proxy file path')
    parser.add_argument('-f', '--follow', help='Account to follow after creation')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--delay-min', type=int, default=30, help='Minimum delay')
    parser.add_argument('--delay-max', type=int, default=60, help='Maximum delay')
    
    # Export arguments
    parser.add_argument('--format', choices=['txt', 'csv', 'json'], default='txt')
    parser.add_argument('-o', '--output', default='accounts.txt')
    
    args = parser.parse_args()
    
    # Route to appropriate mode
    if args.mode == 'create':
        if args.token:
            # Quick mode
            print_banner()
            quick_mode(args)
        else:
            # Interactive mode
            interactive_mode()
    
    elif args.mode == 'usernames':
        check_usernames_mode(args)
    
    elif args.mode == 'export':
        export_accounts_mode(args)


if __name__ == "__main__":
    main()

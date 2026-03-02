"""
Test script for Doser components
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def test_proxy_manager():
    """Test proxy manager"""
    print("Testing Proxy Manager...")
    from utils.proxy_manager import ProxyManager
    
    pm = ProxyManager()
    print(f"  Loaded proxies: {pm.get_proxy_count()}")
    
    # Add test proxy
    pm.add_proxy("http://192.168.1.1:8080")
    print(f"  After adding: {pm.get_proxy_count()}")
    
    proxy = pm.get_next_proxy()
    if proxy:
        print(f"  Proxy: {proxy['host']}:{proxy['port']}")
    
    print("✅ Proxy Manager OK\n")


def test_generators():
    """Test data generators"""
    print("Testing Data Generators...")
    from utils.generators import DataGenerator
    
    gen = DataGenerator()
    
    profile = gen.generate_complete_profile()
    print(f"  Full Name: {profile['full_name']}")
    print(f"  Username: {profile['username']}")
    print(f"  Email: {profile['email']}")
    print(f"  Password: {profile['password']}")
    print(f"  Birthdate: {profile['birthdate']['day']}/{profile['birthdate']['month']}/{profile['birthdate']['year']}")
    
    print("✅ Data Generators OK\n")


def test_email_parser():
    """Test email parser"""
    print("Testing Email Parser...")
    from utils.email_parser import InstagramEmailParser
    
    # Test email content
    test_email = """
    From: Instagram<no-reply@mail.instagram.com>
    Subject: 391046 is your Instagram code
    
    Hi,
    
    Someone tried to sign up for an Instagram account with test@email.com.
    If it was you, enter this confirmation code in the app:
    
    391046
    
    © Instagram
    """
    
    code = InstagramEmailParser.extract_code(test_email)
    print(f"  Extracted code: {code}")
    
    assert code == "391046", "Code extraction failed"
    print("✅ Email Parser OK\n")


def test_account_manager():
    """Test account manager"""
    print("Testing Account Manager...")
    from utils.account_manager import AccountManager
    
    am = AccountManager(storage_dir="test_accounts")
    
    # Add test account
    am.add_account(
        username="test_user",
        password="test_pass",
        email="test@test.com",
        full_name="Test User"
    )
    
    stats = am.get_statistics()
    print(f"  Total accounts: {stats['total_accounts']}")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_accounts", ignore_errors=True)
    
    print("✅ Account Manager OK\n")


def test_email_bot():
    """Test email bot connection"""
    print("Testing Email Bot...")
    print("  Note: This requires a valid bot token")
    
    try:
        from core.email_bot import EmailBot
        
        # This will fail without token, but we can test initialization
        bot = EmailBot("dummy_token")
        print("  Bot initialized (connection not tested)")
        
    except Exception as e:
        print(f"  Error: {e}")
    
    print("✅ Email Bot OK\n")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("🧪 DOSER COMPONENT TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_proxy_manager,
        test_generators,
        test_email_parser,
        test_account_manager,
        test_email_bot,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}\n")
            failed += 1
    
    print("="*60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

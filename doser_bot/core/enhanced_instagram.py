"""
Enhanced Instagram Automation - Improved version with better flow handling
"""

import time
import random
import logging
from typing import Optional, Dict, List
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

from core.email_bot import EmailBot
from core.instagram_signup_flow import InstagramSignupFlow
from utils.proxy_manager import ProxyManager
from utils.generators import DataGenerator
from utils.account_manager import AccountManager
from config.settings import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)


class EnhancedInstagramAutomation:
    """Enhanced Instagram automation with better error handling"""
    
    def __init__(
        self,
        proxy_manager: ProxyManager = None,
        email_bot: EmailBot = None,
        headless: bool = False,
        account_manager: AccountManager = None
    ):
        self.proxy_manager = proxy_manager
        self.email_bot = email_bot
        self.headless = headless
        self.account_manager = account_manager or AccountManager()
        self.generator = DataGenerator()
        self.driver: Optional[webdriver.Chrome] = None
        self.flow: Optional[InstagramSignupFlow] = None
        self.current_proxy = None
    
    def setup_driver(self, proxy: Dict = None) -> bool:
        """Setup Chrome driver with anti-detection measures"""
        try:
            options = uc.ChromeOptions()
            
            # Anti-detection options
            if self.headless:
                options.add_argument('--headless=new')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            
            # Language and locale
            options.add_argument('--lang=en-US')
            options.add_argument('--accept-lang=en-US,en')
            
            # User agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
            ]
            options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            # Proxy configuration
            if proxy:
                self.current_proxy = proxy
                proxy_str = f"{proxy['host']}:{proxy['port']}"
                
                if proxy.get('username') and proxy.get('password'):
                    # For authenticated proxies, use extension
                    logger.info(f"Using authenticated proxy: {proxy['host']}:{proxy['port']}")
                else:
                    options.add_argument(f'--proxy-server={proxy["type"]}://{proxy_str}')
                    logger.info(f"Using proxy: {proxy_str}")
            
            # Create driver
            self.driver = uc.Chrome(options=options)
            
            # Additional anti-detection
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    window.chrome = { runtime: {} };
                '''
            })
            
            # Initialize flow
            self.flow = InstagramSignupFlow(self.driver)
            
            logger.info("Chrome driver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup driver: {e}")
            return False
    
    def close_driver(self):
        """Close browser driver safely"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.debug(f"Error closing driver: {e}")
            finally:
                self.driver = None
                self.flow = None
    
    def create_account(
        self,
        email: str = None,
        profile: Dict = None,
        follow_username: str = None
    ) -> Dict:
        """Create Instagram account with full flow"""
        result = {
            'success': False,
            'username': None,
            'email': email,
            'password': None,
            'error': None,
            'created_at': None
        }
        
        try:
            # Generate profile if not provided
            if not profile:
                profile = self.generator.generate_complete_profile()
            
            if email:
                profile['email'] = email
            
            result['password'] = profile['password']
            
            # Get proxy
            proxy = None
            if self.proxy_manager:
                proxy = self.proxy_manager.get_next_proxy()
            
            # Setup driver
            if not self.setup_driver(proxy):
                raise Exception("Failed to setup driver")
            
            # Navigate to signup
            if not self.flow.navigate_to_signup():
                raise Exception("Failed to navigate to signup")
            
            # Step 1: Enter email
            logger.info("Step 1: Entering email...")
            if not self.flow.enter_email(profile['email']):
                raise Exception("Failed to enter email")
            
            # Check for errors
            error = self.flow.check_for_errors()
            if error:
                raise Exception(f"Email error: {error}")
            
            # Step 2: Wait for and enter verification code
            logger.info("Step 2: Waiting for verification code...")
            
            if self.email_bot:
                code = self.email_bot.wait_for_instagram_code(
                    profile['email'],
                    timeout=300
                )
                
                if not code:
                    raise Exception("No verification code received")
                
                logger.info(f"Received code: {code}")
                
                if not self.flow.enter_verification_code(code):
                    raise Exception("Failed to enter verification code")
                
                # Check for errors
                error = self.flow.check_for_errors()
                if error:
                    raise Exception(f"Code error: {error}")
            else:
                logger.warning("No email bot configured, waiting for manual entry...")
                time.sleep(60)
            
            # Step 3: Create account details
            logger.info("Step 3: Creating account details...")
            if not self.flow.create_account(
                profile['full_name'],
                profile['username'],
                profile['password']
            ):
                raise Exception("Failed to create account details")
            
            # Check for errors
            error = self.flow.check_for_errors()
            if error:
                raise Exception(f"Account details error: {error}")
            
            # Step 4: Enter birthdate
            logger.info("Step 4: Entering birthdate...")
            birthdate = profile['birthdate']
            if not self.flow.enter_birthdate(
                birthdate['day'],
                birthdate['month'],
                birthdate['year']
            ):
                raise Exception("Failed to enter birthdate")
            
            # Step 5: Handle agreements
            logger.info("Step 5: Handling agreements...")
            self.flow.handle_agreements()
            
            # Step 6: Handle CAPTCHA if present
            logger.info("Step 6: Checking for CAPTCHA...")
            captcha_solved, _ = self.flow.handle_captcha()
            if not captcha_solved:
                raise Exception("CAPTCHA handling failed")
            
            # Step 7: Check for phone verification
            logger.info("Step 7: Checking for phone verification...")
            # Skip for now, handle if needed
            
            # Step 8: Wait for completion
            logger.info("Step 8: Waiting for completion...")
            max_wait = 30
            waited = 0
            while waited < max_wait:
                if self.flow.is_signup_complete():
                    break
                time.sleep(1)
                waited += 1
            
            # Save login info dialog
            self.flow.save_login_info(save=False)
            
            # Success!
            result['success'] = True
            result['username'] = profile['username']
            result['email'] = profile['email']
            result['created_at'] = datetime.now().isoformat()
            
            logger.info(f"✅ Account created successfully: {profile['username']}")
            
            # Save to account manager
            self.account_manager.add_account(
                username=profile['username'],
                password=profile['password'],
                email=profile['email'],
                full_name=profile['full_name'],
                proxy=self.current_proxy['url'] if self.current_proxy else None
            )
            
            # Follow account if specified
            if follow_username:
                time.sleep(3)
                self.follow_account(follow_username)
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"❌ Account creation failed: {e}")
        
        finally:
            self.close_driver()
        
        return result
    
    def create_multiple_accounts(
        self,
        count: int,
        follow_username: str = None,
        delay_range: tuple = (30, 60)
    ) -> List[Dict]:
        """Create multiple accounts"""
        results = []
        
        for i in range(count):
            logger.info(f"\n{'='*60}")
            logger.info(f"Creating account {i+1}/{count}")
            logger.info('='*60)
            
            result = self.create_account(follow_username=follow_username)
            results.append(result)
            
            # Delay between accounts
            if i < count - 1:
                delay = random.randint(*delay_range)
                logger.info(f"Waiting {delay} seconds before next account...")
                time.sleep(delay)
        
        return results
    
    def follow_account(self, username: str) -> bool:
        """Follow a specific account"""
        try:
            if not self.flow:
                return False
            
            logger.info(f"Following account: {username}")
            
            # Navigate to profile
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(random.uniform(3, 5))
            
            # Find follow button
            follow_btn = self.driver.find_element(
                By.CSS_SELECTOR,
                'button._acan._acap._acas'
            )
            
            if follow_btn and 'follow' in follow_btn.text.lower():
                follow_btn.click()
                logger.info(f"Followed {username}")
                time.sleep(2)
                return True
            else:
                logger.info(f"Already following {username} or button not found")
                return False
            
        except Exception as e:
            logger.error(f"Failed to follow account: {e}")
            return False
    
    def check_username_availability(self, username: str) -> bool:
        """Check if username is available"""
        try:
            if not self.setup_driver():
                return False
            
            # Navigate to signup
            self.flow.navigate_to_signup()
            
            # Try to enter username
            # This is a simplified check
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(3)
            
            # Check if page shows "Sorry, this page isn't available"
            if "isn't available" in self.driver.page_source:
                return True  # Username is available
            
            # Check for 404
            if self.driver.title == 'Page Not Found':
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Username check failed: {e}")
            return False
        
        finally:
            self.close_driver()
    
    def get_account_statistics(self) -> Dict:
        """Get statistics about created accounts"""
        return self.account_manager.get_statistics()

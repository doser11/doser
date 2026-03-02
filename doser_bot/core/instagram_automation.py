"""
Instagram Automation - Handle account creation process
"""

import time
import random
import logging
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

from utils.proxy_manager import ProxyManager
from utils.generators import DataGenerator
from core.email_bot import EmailBot

logger = logging.getLogger(__name__)


class InstagramAutomation:
    """Automate Instagram account creation"""
    
    def __init__(
        self,
        proxy_manager: ProxyManager = None,
        email_bot: EmailBot = None,
        headless: bool = False
    ):
        self.proxy_manager = proxy_manager
        self.email_bot = email_bot
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.generator = DataGenerator()
    
    def setup_driver(self, proxy: Dict = None):
        """Setup Chrome driver with optional proxy"""
        try:
            options = uc.ChromeOptions()
            
            # Basic options
            if self.headless:
                options.add_argument('--headless')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            options.add_argument('--window-size=1920,1080')
            
            # User agent
            user_agent = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.0'
            )
            options.add_argument(f'--user-agent={user_agent}')
            
            # Proxy configuration
            if proxy:
                proxy_str = f"{proxy['host']}:{proxy['port']}"
                if proxy.get('username') and proxy.get('password'):
                    # For authenticated proxies, we need extension
                    pass
                else:
                    options.add_argument(f'--proxy-server={proxy["type"]}://{proxy_str}')
            
            # Create driver
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            self.wait = WebDriverWait(self.driver, 20)
            
            logger.info("Chrome driver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup driver: {e}")
            raise
    
    def close_driver(self):
        """Close browser driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            logger.info("Driver closed")
    
    def navigate_to_signup(self):
        """Navigate to Instagram signup page"""
        try:
            self.driver.get('https://www.instagram.com/accounts/signup/email/')
            time.sleep(random.uniform(3, 5))
            logger.info("Navigated to signup page")
        except Exception as e:
            logger.error(f"Failed to navigate: {e}")
            raise
    
    def enter_email(self, email: str) -> bool:
        """Enter email address"""
        try:
            # Wait for email input
            email_input = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'input[name="email"], input[type="email"], input[aria-label*="email" i]'
                ))
            )
            
            # Clear and enter email
            email_input.clear()
            time.sleep(random.uniform(0.5, 1))
            
            for char in email:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            logger.info(f"Entered email: {email}")
            
            # Click next/submit
            next_button = self.driver.find_element(
                By.CSS_SELECTOR,
                'button[type="submit"], button._acan, button:contains("Next")'
            )
            next_button.click()
            time.sleep(random.uniform(2, 4))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to enter email: {e}")
            return False
    
    def enter_verification_code(self, code: str) -> bool:
        """Enter verification code"""
        try:
            # Wait for code input
            code_input = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'input[name="confirmationCode"], '
                    'input[aria-label*="code" i], '
                    'input[inputmode="numeric"]'
                ))
            )
            
            # Enter code
            code_input.clear()
            for char in code:
                code_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
            
            logger.info(f"Entered verification code: {code}")
            
            # Click next
            next_button = self.driver.find_element(
                By.CSS_SELECTOR,
                'button[type="submit"], button._acan'
            )
            next_button.click()
            time.sleep(random.uniform(2, 4))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to enter code: {e}")
            return False
    
    def create_account_details(
        self,
        full_name: str,
        username: str,
        password: str,
        birthdate: Dict
    ) -> bool:
        """Fill account creation form"""
        try:
            # Enter full name
            name_input = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 'input[name="fullName"], input[aria-label*="Full" i]'
                ))
            )
            name_input.clear()
            for char in full_name:
                name_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.1))
            
            time.sleep(random.uniform(0.5, 1))
            
            # Enter username
            username_input = self.driver.find_element(
                By.CSS_SELECTOR, 'input[name="username"], input[aria-label*="username" i]'
            )
            username_input.clear()
            for char in username:
                username_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.1))
            
            time.sleep(random.uniform(0.5, 1))
            
            # Enter password
            password_input = self.driver.find_element(
                By.CSS_SELECTOR, 'input[name="password"], input[type="password"]'
            )
            password_input.clear()
            for char in password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.1))
            
            logger.info("Filled account details")
            
            # Click next
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, 'button[type="submit"], button._acan'
            )
            next_button.click()
            time.sleep(random.uniform(3, 5))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create account details: {e}")
            return False
    
    def enter_birthdate(self, birthdate: Dict) -> bool:
        """Enter birthdate"""
        try:
            # Select year
            year_select = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 'select[title*="Year"], select[name*="year"]'
                ))
            )
            year_select.click()
            time.sleep(0.5)
            
            year_option = self.driver.find_element(
                By.CSS_SELECTOR, f'option[value="{birthdate["year"]}"]'
            )
            year_option.click()
            
            # Select month
            month_select = self.driver.find_element(
                By.CSS_SELECTOR, 'select[title*="Month"], select[name*="month"]'
            )
            month_select.click()
            time.sleep(0.5)
            
            month_option = self.driver.find_element(
                By.CSS_SELECTOR, f'option[value="{birthdate["month"]}"]'
            )
            month_option.click()
            
            # Select day
            day_select = self.driver.find_element(
                By.CSS_SELECTOR, 'select[title*="Day"], select[name*="day"]'
            )
            day_select.click()
            time.sleep(0.5)
            
            day_option = self.driver.find_element(
                By.CSS_SELECTOR, f'option[value="{birthdate["day"]}"]'
            )
            day_option.click()
            
            logger.info(f"Entered birthdate: {birthdate['day']}/{birthdate['month']}/{birthdate['year']}")
            
            # Click next
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, 'button[type="submit"], button._acan'
            )
            next_button.click()
            time.sleep(random.uniform(2, 4))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to enter birthdate: {e}")
            return False
    
    def handle_agreements(self) -> bool:
        """Handle terms and agreements"""
        try:
            # Look for agree buttons
            agree_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                'button:contains("Agree"), button:contains("I Accept"), '
                'input[type="checkbox"]'
            )
            
            for button in agree_buttons:
                if button.is_displayed():
                    button.click()
                    time.sleep(random.uniform(0.5, 1))
            
            logger.info("Handled agreements")
            return True
            
        except Exception as e:
            logger.error(f"Failed to handle agreements: {e}")
            return False
    
    def handle_captcha(self) -> bool:
        """Handle CAPTCHA if present"""
        try:
            # Check for CAPTCHA
            captcha_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                'iframe[src*="recaptcha"], iframe[src*="captcha"], '
                'div[class*="captcha"], div[id*="captcha"]'
            )
            
            if captcha_elements:
                logger.warning("CAPTCHA detected! Manual intervention required.")
                # Here you could integrate with 2captcha service
                # For now, wait for manual solving
                time.sleep(30)  # Give time for manual solving
                return True
            
            return True
            
        except Exception as e:
            logger.error(f"CAPTCHA handling failed: {e}")
            return False
    
    def save_account(self, account_data: Dict, filename: str = "accounts.txt"):
        """Save created account to file"""
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Username: {account_data['username']}\n")
                f.write(f"Password: {account_data['password']}\n")
                f.write(f"Email: {account_data['email']}\n")
                f.write(f"Full Name: {account_data['full_name']}\n")
                f.write(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*50}\n")
            
            logger.info(f"Account saved: {account_data['username']}")
            
        except Exception as e:
            logger.error(f"Failed to save account: {e}")
    
    def create_account(
        self,
        email: str = None,
        profile: Dict = None
    ) -> Dict:
        """Complete account creation process"""
        result = {
            'success': False,
            'username': None,
            'email': email,
            'error': None
        }
        
        try:
            # Generate profile if not provided
            if not profile:
                profile = self.generator.generate_complete_profile()
            
            if email:
                profile['email'] = email
            
            # Get proxy
            proxy = None
            if self.proxy_manager:
                proxy = self.proxy_manager.get_next_proxy()
            
            # Setup driver
            self.setup_driver(proxy)
            
            # Navigate to signup
            self.navigate_to_signup()
            
            # Enter email
            if not self.enter_email(profile['email']):
                raise Exception("Failed to enter email")
            
            # Wait for verification code
            if self.email_bot:
                code = self.email_bot.wait_for_instagram_code(profile['email'])
                if not code:
                    raise Exception("No verification code received")
                
                # Enter code
                if not self.enter_verification_code(code):
                    raise Exception("Failed to enter verification code")
            else:
                # Manual mode - wait for user
                logger.info("Waiting 60 seconds for manual code entry...")
                time.sleep(60)
            
            # Fill account details
            if not self.create_account_details(
                profile['full_name'],
                profile['username'],
                profile['password'],
                profile['birthdate']
            ):
                raise Exception("Failed to create account details")
            
            # Enter birthdate
            self.enter_birthdate(profile['birthdate'])
            
            # Handle agreements
            self.handle_agreements()
            
            # Handle CAPTCHA
            self.handle_captcha()
            
            # Save account
            self.save_account(profile)
            
            result['success'] = True
            result['username'] = profile['username']
            logger.info(f"Account created successfully: {profile['username']}")
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Account creation failed: {e}")
        
        finally:
            self.close_driver()
        
        return result
    
    def follow_account(self, target_username: str) -> bool:
        """Follow a specific account after creation"""
        try:
            if not self.driver:
                self.setup_driver()
            
            # Navigate to profile
            self.driver.get(f'https://www.instagram.com/{target_username}/')
            time.sleep(random.uniform(3, 5))
            
            # Find follow button
            follow_button = self.wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'button:contains("Follow"), button._acan._acap'
                ))
            )
            
            follow_button.click()
            time.sleep(random.uniform(2, 3))
            
            logger.info(f"Followed account: {target_username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to follow account: {e}")
            return False

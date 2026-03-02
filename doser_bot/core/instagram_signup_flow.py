"""
Instagram Signup Flow - Handle complete signup process step by step
"""

import time
import random
import logging
from typing import Optional, Dict, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.email_parser import InstagramEmailParser
from utils.captcha_solver import CaptchaSolver

logger = logging.getLogger(__name__)


class InstagramSignupFlow:
    """Handle Instagram signup flow step by step"""
    
    def __init__(self, driver, wait_timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        self.short_wait = WebDriverWait(driver, 5)
        self.captcha_solver = CaptchaSolver()
    
    def navigate_to_signup(self):
        """Navigate to Instagram signup page"""
        try:
            logger.info("Navigating to Instagram signup page...")
            self.driver.get('https://www.instagram.com/accounts/signup/email/')
            time.sleep(random.uniform(3, 5))
            
            # Check for cookie consent
            self._handle_cookie_consent()
            
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def _handle_cookie_consent(self):
        """Handle cookie consent popup"""
        try:
            # Look for accept cookies button
            cookie_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                'button:contains("Allow"), button:contains("Accept"), '
                'button._a9--, button[tabindex="0"]'
            )
            
            for btn in cookie_buttons:
                if 'cookie' in btn.text.lower() or 'allow' in btn.text.lower():
                    btn.click()
                    logger.info("Cookie consent accepted")
                    time.sleep(1)
                    break
                    
        except Exception as e:
            logger.debug(f"No cookie consent or error: {e}")
    
    def enter_email(self, email: str) -> bool:
        """Enter email address in signup form"""
        try:
            logger.info(f"Entering email: {email}")
            
            # Find email input - try multiple selectors
            email_input = self._find_element_with_retry(
                [
                    'input[name="email"]',
                    'input[type="email"]',
                    'input[aria-label*="email" i]',
                    'input[placeholder*="email" i]',
                    'input[placeholder*="Email" i]',
                    'input._aa4b',
                    'input._add6'
                ]
            )
            
            if not email_input:
                logger.error("Email input not found")
                return False
            
            # Clear and enter email with human-like typing
            email_input.click()
            time.sleep(random.uniform(0.2, 0.5))
            email_input.clear()
            
            for char in email:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(0.5, 1))
            
            # Click next button
            next_btn = self._find_next_button()
            if next_btn:
                next_btn.click()
                logger.info("Email submitted")
                time.sleep(random.uniform(3, 5))
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to enter email: {e}")
            return False
    
    def enter_verification_code(self, code: str) -> bool:
        """Enter verification code"""
        try:
            logger.info(f"Entering verification code: {code}")
            
            # Find code input
            code_input = self._find_element_with_retry(
                [
                    'input[name="confirmationCode"]',
                    'input[aria-label*="code" i]',
                    'input[aria-label*="confirmation" i]',
                    'input[inputmode="numeric"]',
                    'input[autocomplete="one-time-code"]',
                    'input._aa4b'
                ]
            )
            
            if not code_input:
                logger.error("Code input not found")
                return False
            
            # Enter code
            code_input.click()
            code_input.clear()
            
            for char in code:
                code_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
            
            time.sleep(random.uniform(0.5, 1))
            
            # Click next
            next_btn = self._find_next_button()
            if next_btn:
                next_btn.click()
                logger.info("Code submitted")
                time.sleep(random.uniform(3, 5))
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to enter code: {e}")
            return False
    
    def create_account(
        self,
        full_name: str,
        username: str,
        password: str
    ) -> bool:
        """Fill account creation form"""
        try:
            logger.info("Filling account details...")
            
            # Enter full name
            name_input = self._find_element_with_retry(
                [
                    'input[name="fullName"]',
                    'input[aria-label*="Full" i]',
                    'input[aria-label*="name" i]',
                    'input[placeholder*="Full" i]'
                ]
            )
            
            if name_input:
                self._type_like_human(name_input, full_name)
                time.sleep(random.uniform(0.5, 1))
            
            # Enter username
            username_input = self._find_element_with_retry(
                [
                    'input[name="username"]',
                    'input[aria-label*="username" i]',
                    'input[placeholder*="username" i]'
                ]
            )
            
            if username_input:
                self._type_like_human(username_input, username)
                time.sleep(random.uniform(0.5, 1))
                
                # Check if username is available
                time.sleep(2)
                self._check_username_availability()
            
            # Enter password
            password_input = self._find_element_with_retry(
                [
                    'input[name="password"]',
                    'input[type="password"]',
                    'input[aria-label*="password" i]'
                ]
            )
            
            if password_input:
                self._type_like_human(password_input, password)
                time.sleep(random.uniform(0.5, 1))
            
            # Click next
            next_btn = self._find_next_button()
            if next_btn:
                next_btn.click()
                logger.info("Account details submitted")
                time.sleep(random.uniform(3, 5))
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to create account: {e}")
            return False
    
    def enter_birthdate(self, day: int, month: int, year: int) -> bool:
        """Enter birthdate"""
        try:
            logger.info(f"Entering birthdate: {day}/{month}/{year}")
            
            # Try different approaches for birthdate
            
            # Approach 1: Dropdown selects
            try:
                # Month
                month_select = self.wait.until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        'select[title*="Month"], select[name*="month"]'
                    ))
                )
                month_select.click()
                time.sleep(0.5)
                
                month_option = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f'option[value="{month}"]'
                )
                month_option.click()
                time.sleep(0.5)
                
                # Day
                day_select = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'select[title*="Day"], select[name*="day"]'
                )
                day_select.click()
                time.sleep(0.5)
                
                day_option = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f'option[value="{day}"]'
                )
                day_option.click()
                time.sleep(0.5)
                
                # Year
                year_select = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'select[title*="Year"], select[name*="year"]'
                )
                year_select.click()
                time.sleep(0.5)
                
                year_option = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f'option[value="{year}"]'
                )
                year_option.click()
                time.sleep(0.5)
                
            except:
                # Approach 2: Input fields
                logger.info("Trying alternative birthdate input...")
                
                # Look for date input
                date_inputs = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'input[type="text"], input[placeholder*="date" i]'
                )
                
                if date_inputs:
                    date_str = f"{month:02d}/{day:02d}/{year}"
                    self._type_like_human(date_inputs[0], date_str)
            
            time.sleep(random.uniform(0.5, 1))
            
            # Click next
            next_btn = self._find_next_button()
            if next_btn:
                next_btn.click()
                logger.info("Birthdate submitted")
                time.sleep(random.uniform(3, 5))
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to enter birthdate: {e}")
            return False
    
    def handle_agreements(self) -> bool:
        """Handle terms and agreements"""
        try:
            logger.info("Handling agreements...")
            
            # Look for agree buttons
            agree_selectors = [
                'button:contains("Agree")',
                'button:contains("I Accept")',
                'button:contains("Accept")',
                'button:contains("Next")',
                'button[type="submit"]',
                'button._acan',
                'input[type="checkbox"]'
            ]
            
            for selector in agree_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            text = elem.text.lower()
                            if any(word in text for word in ['agree', 'accept', 'next', 'continue']):
                                elem.click()
                                logger.info(f"Clicked: {elem.text}")
                                time.sleep(random.uniform(1, 2))
                                return True
                except:
                    continue
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to handle agreements: {e}")
            return False
    
    def handle_captcha(self) -> Tuple[bool, Optional[str]]:
        """Handle CAPTCHA if present"""
        try:
            # Check for CAPTCHA
            captcha_info = self.captcha_solver.check_for_captcha(self.driver)
            
            if any(captcha_info.values()):
                logger.warning("CAPTCHA detected!")
                
                # Try to solve automatically
                if captcha_info.get('recaptcha_v2'):
                    # Get site key
                    site_key = self._get_recaptcha_site_key()
                    if site_key:
                        code = self.captcha_solver.solve_recaptcha_v2(
                            self.driver,
                            site_key,
                            self.driver.current_url
                        )
                        if code:
                            self.captcha_solver.inject_recaptcha_solution(self.driver, code)
                            return True, code
                
                # Wait for manual solving
                logger.info("Waiting for manual CAPTCHA solve...")
                solved = self.captcha_solver.wait_for_captcha_solve(self.driver)
                return solved, None
            
            return True, None
            
        except Exception as e:
            logger.error(f"CAPTCHA handling failed: {e}")
            return False, None
    
    def handle_phone_verification(self, phone_number: str = None) -> bool:
        """Handle phone verification if required"""
        try:
            # Check if phone verification is requested
            phone_input = self.driver.find_elements(
                By.CSS_SELECTOR,
                'input[type="tel"], input[name="phone"], input[aria-label*="phone" i]'
            )
            
            if phone_input and phone_number:
                logger.info("Phone verification required")
                self._type_like_human(phone_input[0], phone_number)
                
                next_btn = self._find_next_button()
                if next_btn:
                    next_btn.click()
                    time.sleep(3)
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Phone verification failed: {e}")
            return False
    
    def check_for_errors(self) -> Optional[str]:
        """Check for error messages on page"""
        error_selectors = [
            '[role="alert"]',
            '.error-message',
            '._ab2z',
            '._ab2-',
            '[data-testid="error-message"]'
        ]
        
        for selector in error_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed():
                        error_text = elem.text.strip()
                        if error_text:
                            logger.error(f"Error found: {error_text}")
                            return error_text
            except:
                continue
        
        return None
    
    def is_signup_complete(self) -> bool:
        """Check if signup is complete"""
        try:
            # Check for welcome page
            if '/accounts/welcome/' in self.driver.current_url:
                return True
            
            # Check for home feed
            if '/feed/' in self.driver.current_url or self.driver.current_url == 'https://www.instagram.com/':
                return True
            
            # Check for "Save Your Login Info" page
            if 'save-your-login-info' in self.driver.current_url:
                return True
            
            # Check for profile page redirect
            if '/accounts/edit/' in self.driver.current_url:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking signup completion: {e}")
            return False
    
    def save_login_info(self, save: bool = True) -> bool:
        """Handle 'Save Your Login Info' dialog"""
        try:
            if save:
                # Click Save
                save_btn = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'button:contains("Save"), button._acan'
                )
                save_btn.click()
            else:
                # Click Not Now
                not_now_btn = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'button:contains("Not Now")'
                )
                not_now_btn.click()
            
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.debug(f"Save login info dialog not found: {e}")
            return False
    
    def _find_element_with_retry(self, selectors: list, wait_time: int = 10) -> Optional:
        """Find element trying multiple selectors"""
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element.is_displayed():
                    return element
            except:
                continue
        return None
    
    def _find_next_button(self) -> Optional:
        """Find next/submit button"""
        selectors = [
            'button[type="submit"]',
            'button._acan._acap',
            'button._acan',
            'button:contains("Next")',
            'button:contains("Sign up")',
            'button:contains("Continue")'
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed() and elem.is_enabled():
                        return elem
            except:
                continue
        
        return None
    
    def _type_like_human(self, element, text: str):
        """Type text like a human with random delays"""
        element.click()
        element.clear()
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def _check_username_availability(self) -> bool:
        """Check if entered username is available"""
        try:
            # Look for availability indicator
            time.sleep(2)
            
            # Check for error message about username
            error_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[role="alert"], .error-message'
            )
            
            for elem in error_elements:
                if 'username' in elem.text.lower():
                    logger.warning(f"Username issue: {elem.text}")
                    return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Could not check username availability: {e}")
            return True
    
    def _get_recaptcha_site_key(self) -> Optional[str]:
        """Extract reCAPTCHA site key from page"""
        try:
            # Try to find site key in page source
            page_source = self.driver.page_source
            
            # Pattern 1: data-sitekey attribute
            import re
            match = re.search(r'data-sitekey="([^"]+)"', page_source)
            if match:
                return match.group(1)
            
            # Pattern 2: grecaptcha.render
            match = re.search(r'grecaptcha\.render\([^,]+,\s*\{[^}]*sitekey:\s*["\']([^"\']+)', page_source)
            if match:
                return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get site key: {e}")
            return None

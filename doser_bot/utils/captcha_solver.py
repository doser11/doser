"""
CAPTCHA Solver - Handle various CAPTCHA types
"""

import time
import logging
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class CaptchaSolver:
    """Handle CAPTCHA solving using various services"""
    
    def __init__(self, api_key: str = None, service: str = '2captcha'):
        self.api_key = api_key
        self.service = service
        self.solver = None
        
        if api_key:
            self._init_solver()
    
    def _init_solver(self):
        """Initialize CAPTCHA solver service"""
        try:
            if self.service == '2captcha':
                from twocaptcha import TwoCaptcha
                self.solver = TwoCaptcha(self.api_key)
                logger.info("2Captcha initialized")
        except Exception as e:
            logger.error(f"Failed to init CAPTCHA solver: {e}")
    
    def solve_recaptcha_v2(
        self,
        driver,
        site_key: str,
        url: str,
        timeout: int = 120
    ) -> Optional[str]:
        """Solve reCAPTCHA v2"""
        if not self.solver:
            logger.warning("No CAPTCHA solver configured")
            return None
        
        try:
            logger.info("Solving reCAPTCHA v2...")
            result = self.solver.recaptcha(
                sitekey=site_key,
                url=url
            )
            
            if result and result.get('code'):
                code = result['code']
                logger.info("CAPTCHA solved successfully")
                return code
            
        except Exception as e:
            logger.error(f"CAPTCHA solving failed: {e}")
        
        return None
    
    def solve_image_captcha(
        self,
        image_path: str,
        timeout: int = 60
    ) -> Optional[str]:
        """Solve image CAPTCHA"""
        if not self.solver:
            logger.warning("No CAPTCHA solver configured")
            return None
        
        try:
            logger.info("Solving image CAPTCHA...")
            result = self.solver.normal(image_path)
            
            if result and result.get('code'):
                return result['code']
            
        except Exception as e:
            logger.error(f"Image CAPTCHA solving failed: {e}")
        
        return None
    
    def inject_recaptcha_solution(self, driver, token: str) -> bool:
        """Inject reCAPTCHA solution into page"""
        try:
            script = f"""
                document.getElementById('g-recaptcha-response').innerHTML = '{token}';
                if (typeof grecaptcha !== 'undefined') {{
                    grecaptcha.getResponse = function() {{ return '{token}'; }};
                }}
            """
            driver.execute_script(script)
            logger.info("reCAPTCHA token injected")
            return True
            
        except Exception as e:
            logger.error(f"Failed to inject token: {e}")
            return False
    
    def check_for_captcha(self, driver) -> dict:
        """Check if page has CAPTCHA"""
        captcha_types = {
            'recaptcha_v2': False,
            'recaptcha_v3': False,
            'hcaptcha': False,
            'image_captcha': False,
            'funcaptcha': False
        }
        
        try:
            # Check for reCAPTCHA v2
            if driver.find_elements(By.CSS_SELECTOR, '.g-recaptcha'):
                captcha_types['recaptcha_v2'] = True
                logger.info("reCAPTCHA v2 detected")
            
            # Check for reCAPTCHA v3 (invisible)
            if driver.find_elements(By.CSS_SELECTOR, '[data-recaptcha-v3]'):
                captcha_types['recaptcha_v3'] = True
                logger.info("reCAPTCHA v3 detected")
            
            # Check for hCaptcha
            if driver.find_elements(By.CSS_SELECTOR, '.h-captcha'):
                captcha_types['hcaptcha'] = True
                logger.info("hCaptcha detected")
            
            # Check for image CAPTCHA
            if driver.find_elements(By.CSS_SELECTOR, 'img[src*="captcha"]'):
                captcha_types['image_captcha'] = True
                logger.info("Image CAPTCHA detected")
            
            # Check for FunCaptcha
            if driver.find_elements(By.CSS_SELECTOR, '#funcaptcha'):
                captcha_types['funcaptcha'] = True
                logger.info("FunCaptcha detected")
            
        except Exception as e:
            logger.error(f"Error checking for CAPTCHA: {e}")
        
        return captcha_types
    
    def wait_for_captcha_solve(
        self,
        driver,
        timeout: int = 120,
        check_interval: int = 2
    ) -> bool:
        """Wait for manual CAPTCHA solving"""
        logger.info(f"Waiting {timeout}s for manual CAPTCHA solve...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check if CAPTCHA is still present
            captcha_elements = driver.find_elements(
                By.CSS_SELECTOR,
                '.g-recaptcha, .h-captcha, iframe[src*="recaptcha"]'
            )
            
            if not captcha_elements:
                logger.info("CAPTCHA appears to be solved")
                return True
            
            time.sleep(check_interval)
        
        logger.warning("CAPTCHA solve timeout")
        return False
    
    def handle_instagram_captcha(self, driver) -> bool:
        """Handle Instagram-specific CAPTCHA"""
        try:
            # Check for challenge page
            if '/challenge/' in driver.current_url:
                logger.warning("Instagram challenge detected!")
                
                # Wait for manual intervention
                self.wait_for_captcha_solve(driver, timeout=300)
                return True
            
            # Check for suspicious activity
            page_source = driver.page_source.lower()
            if any(text in page_source for text in [
                'suspicious activity',
                'unusual activity',
                'verify your identity',
                'confirm your identity'
            ]):
                logger.warning("Instagram security check detected!")
                self.wait_for_captcha_solve(driver, timeout=300)
                return True
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling Instagram CAPTCHA: {e}")
            return False


class ManualCaptchaSolver:
    """Manual CAPTCHA solving with user input"""
    
    @staticmethod
    def prompt_user(captcha_image_path: str = None) -> str:
        """Prompt user for CAPTCHA solution"""
        try:
            from PIL import Image
            import tkinter as tk
            from tkinter import simpledialog
            
            root = tk.Tk()
            root.withdraw()
            
            if captcha_image_path:
                # Show image if available
                img = Image.open(captcha_image_path)
                img.show()
            
            code = simpledialog.askstring(
                "CAPTCHA Required",
                "Please enter the CAPTCHA code you see:"
            )
            
            root.destroy()
            return code or ""
            
        except Exception as e:
            logger.error(f"Manual solve prompt failed: {e}")
            # Fallback to console input
            return input("Enter CAPTCHA code: ")

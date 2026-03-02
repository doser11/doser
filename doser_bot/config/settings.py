"""
Doser Bot - Configuration Settings
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
PROXIES_DIR = BASE_DIR / "proxies"
ACCOUNTS_DIR = BASE_DIR / "accounts"

# Create directories if not exist
for dir_path in [DATA_DIR, LOGS_DIR, PROXIES_DIR, ACCOUNTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Instagram URLs
INSTAGRAM_URLS = {
    "signup_email": "https://www.instagram.com/accounts/signup/email/",
    "signup": "https://www.instagram.com/accounts/emailsignup/",
    "login": "https://www.instagram.com/accounts/login/",
    "api": "https://www.instagram.com/api/v1/"
}

# Bot API Settings (Email Bot)
BOT_API = {
    "base_url": "https://api.telegram.org/bot",
    "email_check_interval": 5,  # seconds
    "max_wait_time": 300,  # 5 minutes
}

# Default Account Settings
DEFAULT_SETTINGS = {
    "password": "P@ssword81297",
    "min_age": 18,
    "max_age": 45,
    "country_code": "US",
    "language": "en-US"
}

# Proxy Settings
PROXY_SETTINGS = {
    "enabled": True,
    "rotation_interval": 1,  # Rotate after each account
    "timeout": 30,
    "types": ["http", "https", "socks4", "socks5"]
}

# User Agent Settings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.0"
]

# GUI Settings
GUI_SETTINGS = {
    "theme": "dark",
    "color_theme": "blue",
    "window_width": 1200,
    "window_height": 800,
    "title": "Doser - Instagram Account Creator"
}

# CAPTCHA Settings
CAPTCHA_SETTINGS = {
    "service": "2captcha",  # or "anticaptcha"
    "api_key": os.getenv("CAPTCHA_API_KEY", ""),
    "timeout": 120
}

# Rate Limiting
RATE_LIMITS = {
    "accounts_per_hour": 5,
    "delay_between_accounts": (30, 60),  # random seconds
    "delay_between_actions": (2, 5)
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_DIR / "doser.log"
}

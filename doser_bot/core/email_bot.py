"""
Email Bot Handler - Receive and parse Instagram verification emails
"""

import re
import time
import requests
import logging
from typing import Optional, Dict
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class EmailBot:
    """Handle email operations through Telegram Bot API"""
    
    def __init__(self, bot_token: str, chat_id: str = None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.last_update_id = 0
        self.received_codes = {}
    
    def test_connection(self) -> bool:
        """Test bot connection"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=10)
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                logger.info(f"Bot connected: @{bot_info['username']}")
                return True
            return False
        except Exception as e:
            logger.error(f"Bot connection failed: {e}")
            return False
    
    def get_updates(self, limit: int = 100) -> list:
        """Get updates from bot"""
        try:
            params = {
                'offset': self.last_update_id + 1,
                'limit': limit
            }
            response = requests.get(
                f"{self.base_url}/getUpdates",
                params=params,
                timeout=10
            )
            data = response.json()
            
            if data.get('ok'):
                updates = data['result']
                if updates:
                    self.last_update_id = max(u['update_id'] for u in updates)
                return updates
            return []
            
        except Exception as e:
            logger.error(f"Failed to get updates: {e}")
            return []
    
    def send_message(self, text: str, chat_id: str = None) -> bool:
        """Send message through bot"""
        try:
            target_chat = chat_id or self.chat_id
            if not target_chat:
                logger.error("No chat ID provided")
                return False
            
            params = {
                'chat_id': target_chat,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(
                f"{self.base_url}/sendMessage",
                params=params,
                timeout=10
            )
            return response.json().get('ok', False)
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def parse_instagram_code(self, message_text: str) -> Optional[str]:
        """Parse Instagram verification code from message"""
        if not message_text:
            return None
        
        # Look for 6-digit code pattern
        # Instagram codes are typically 6 digits
        patterns = [
            r'\b(\d{6})\b',  # Generic 6-digit
            r'code[\s:]+(\d{6})',
            r'confirmation code[\s:]+(\d{6})',
            r'Instagram code[\s:]+(\d{6})',
            r'is your Instagram code[\s:]+(\d{6})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message_text, re.IGNORECASE)
            if match:
                code = match.group(1)
                logger.info(f"Found Instagram code: {code}")
                return code
        
        # Try to extract from HTML if present
        if '<' in message_text and '>' in message_text:
            soup = BeautifulSoup(message_text, 'html.parser')
            text = soup.get_text()
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    code = match.group(1)
                    logger.info(f"Found Instagram code from HTML: {code}")
                    return code
        
        return None
    
    def wait_for_instagram_code(
        self,
        email_address: str,
        timeout: int = 300,
        check_interval: int = 5
    ) -> Optional[str]:
        """Wait for Instagram verification code"""
        logger.info(f"Waiting for Instagram code for {email_address}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            updates = self.get_updates()
            
            for update in updates:
                message = update.get('message', {})
                text = message.get('text', '')
                
                # Check if message contains the email address
                if email_address.lower() in text.lower():
                    code = self.parse_instagram_code(text)
                    if code:
                        logger.info(f"Received code for {email_address}: {code}")
                        return code
                else:
                    # Try parsing anyway
                    code = self.parse_instagram_code(text)
                    if code:
                        logger.info(f"Received code (email not matched): {code}")
                        # Store for later retrieval
                        self.received_codes[email_address] = {
                            'code': code,
                            'timestamp': datetime.now()
                        }
                        return code
            
            time.sleep(check_interval)
        
        logger.warning(f"Timeout waiting for code for {email_address}")
        return None
    
    def get_code_from_history(self, email_address: str) -> Optional[str]:
        """Get code from stored history"""
        if email_address in self.received_codes:
            entry = self.received_codes[email_address]
            # Check if code is not too old (5 minutes)
            age = (datetime.now() - entry['timestamp']).total_seconds()
            if age < 300:
                return entry['code']
        return None
    
    def forward_email_to_bot(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        body: str,
        html_body: str = None
    ) -> bool:
        """Forward email content to Telegram bot"""
        try:
            message = f"""
📧 <b>New Email Received</b>

<b>From:</b> {from_email}
<b>To:</b> {to_email}
<b>Subject:</b> {subject}

<b>Body:</b>
{body[:1000] if body else 'No text content'}
"""
            
            # If HTML body exists, try to extract code
            if html_body:
                code = self.parse_instagram_code(html_body)
                if code:
                    message += f"\n\n🔢 <b>Detected Code:</b> <code>{code}</code>"
            
            return self.send_message(message)
            
        except Exception as e:
            logger.error(f"Failed to forward email: {e}")
            return False


class TempMailService:
    """Alternative: Use temporary email services"""
    
    def __init__(self):
        self.services = {
            'tempmail': 'https://api.temp-mail.org',
            'guerrillamail': 'https://api.guerrillamail.com',
        }
    
    def get_temp_email(self, service: str = 'guerrillamail') -> Dict:
        """Get temporary email address"""
        try:
            if service == 'guerrillamail':
                response = requests.get(
                    'https://api.guerrillamail.com/ajax.php',
                    params={'f': 'get_email_address'},
                    timeout=10
                )
                data = response.json()
                return {
                    'email': data.get('email_addr'),
                    'sid_token': data.get('sid_token')
                }
            return {}
        except Exception as e:
            logger.error(f"Failed to get temp email: {e}")
            return {}
    
    def check_inbox(self, sid_token: str, service: str = 'guerrillamail') -> list:
        """Check inbox for new emails"""
        try:
            if service == 'guerrillamail':
                response = requests.get(
                    'https://api.guerrillamail.com/ajax.php',
                    params={
                        'f': 'check_email',
                        'sid_token': sid_token
                    },
                    timeout=10
                )
                data = response.json()
                return data.get('list', [])
            return []
        except Exception as e:
            logger.error(f"Failed to check inbox: {e}")
            return []
    
    def fetch_email(self, sid_token: str, email_id: str) -> Dict:
        """Fetch full email content"""
        try:
            response = requests.get(
                'https://api.guerrillamail.com/ajax.php',
                params={
                    'f': 'fetch_email',
                    'sid_token': sid_token,
                    'email_id': email_id
                },
                timeout=10
            )
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch email: {e}")
            return {}

"""
Email Parser - Parse Instagram verification emails
"""

import re
import logging
from typing import Optional, Dict
from html.parser import HTMLParser
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class InstagramEmailParser:
    """Parse Instagram verification emails to extract codes"""
    
    # Instagram email patterns
    INSTAGRAM_SENDERS = [
        'no-reply@mail.instagram.com',
        'security@mail.instagram.com',
        'instagram@mail.instagram.com',
        'no-reply@instagram.com'
    ]
    
    # Subject patterns that indicate verification
    VERIFICATION_SUBJECTS = [
        'is your Instagram code',
        'confirmation code',
        'verify your email',
        'email confirmation',
        'security code',
        'login code'
    ]
    
    @classmethod
    def is_instagram_email(cls, from_email: str, subject: str) -> bool:
        """Check if email is from Instagram"""
        from_email = from_email.lower()
        subject = subject.lower()
        
        # Check sender
        is_instagram_sender = any(
            sender in from_email 
            for sender in cls.INSTAGRAM_SENDERS
        )
        
        # Check subject
        is_verification = any(
            pattern in subject 
            for pattern in cls.VERIFICATION_SUBJECTS
        )
        
        return is_instagram_sender or is_verification
    
    @classmethod
    def extract_code(cls, email_content: str, is_html: bool = False) -> Optional[str]:
        """Extract verification code from email content"""
        if not email_content:
            return None
        
        # If HTML, extract text first
        if is_html or '<html' in email_content.lower():
            email_content = cls._html_to_text(email_content)
        
        # Try multiple patterns to find the code
        patterns = [
            # Pattern 1: "391046 is your Instagram code"
            r'(\d{6})\s+is\s+your\s+Instagram\s+code',
            
            # Pattern 2: "Your Instagram code is 391046"
            r'(?:code|confirmation\s+code)\s+is\s*:?\s*(\d{6})',
            
            # Pattern 3: "Code: 391046"
            r'[Cc]ode\s*:?\s*(\d{6})',
            
            # Pattern 4: Just 6 digits on their own line
            r'^[\s]*([\d]{6})[\s]*$',
            
            # Pattern 5: Code in parentheses
            r'\((\d{6})\)',
            
            # Pattern 6: Bold/strong code
            r'<(?:b|strong)[^>]*>(\d{6})</(?:b|strong)>',
            
            # Pattern 7: Any 6 digits near "code" or "confirm"
            r'(?:confirm|code|verify).*?(\d{6})',
            
            # Pattern 8: Generic 6-digit code
            r'\b(\d{6})\b'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, email_content, re.IGNORECASE | re.MULTILINE)
            if matches:
                # Return the first valid 6-digit code
                for match in matches:
                    if match and len(match) == 6 and match.isdigit():
                        logger.info(f"Found Instagram code: {match}")
                        return match
        
        # Try to find any 6-digit number that looks like a code
        all_six_digits = re.findall(r'\b(\d{6})\b', email_content)
        for digits in all_six_digits:
            # Filter out common false positives (years, etc.)
            if not (1900 < int(digits) < 2100):  # Not a year
                logger.info(f"Found potential code: {digits}")
                return digits
        
        return None
    
    @classmethod
    def _html_to_text(cls, html_content: str) -> str:
        """Convert HTML to plain text"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.error(f"HTML parsing failed: {e}")
            # Fallback: simple regex
            text = re.sub(r'<[^>]+>', ' ', html_content)
            return re.sub(r'\s+', ' ', text)
    
    @classmethod
    def parse_full_email(cls, email_data: Dict) -> Dict:
        """Parse complete email and extract all relevant info"""
        result = {
            'is_instagram': False,
            'is_verification': False,
            'code': None,
            'email_type': None,
            'confidence': 0
        }
        
        from_email = email_data.get('from', '').lower()
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '')
        html_body = email_data.get('html_body', '')
        
        # Check if from Instagram
        result['is_instagram'] = cls.is_instagram_email(from_email, subject)
        
        # Determine email type
        if 'signup' in subject or 'sign up' in subject:
            result['email_type'] = 'signup_verification'
        elif 'login' in subject or 'log in' in subject:
            result['email_type'] = 'login_verification'
        elif 'reset' in subject or 'password' in subject:
            result['email_type'] = 'password_reset'
        elif 'security' in subject:
            result['email_type'] = 'security_alert'
        
        # Extract code
        # Try HTML body first (usually cleaner)
        if html_body:
            result['code'] = cls.extract_code(html_body, is_html=True)
        
        # If not found, try plain text
        if not result['code'] and body:
            result['code'] = cls.extract_code(body, is_html=False)
        
        # Set confidence based on findings
        if result['code'] and result['is_instagram']:
            result['confidence'] = 100
        elif result['code']:
            result['confidence'] = 70
        elif result['is_instagram']:
            result['confidence'] = 50
        
        result['is_verification'] = result['code'] is not None
        
        return result
    
    @classmethod
    def format_code_for_display(cls, code: str) -> str:
        """Format code for display with spacing"""
        if not code or len(code) != 6:
            return code
        
        # Format as: 391 046
        return f"{code[:3]} {code[3:]}"


class MLBasedParser:
    """Machine learning based email parser (placeholder for future enhancement)"""
    
    def __init__(self):
        self.trained = False
    
    def train(self, training_data):
        """Train the parser with labeled data"""
        # Placeholder for ML training
        pass
    
    def predict(self, email_content):
        """Predict if email contains verification code"""
        # Placeholder for ML prediction
        return InstagramEmailParser.extract_code(email_content)


# Utility functions
def clean_email_content(content: str) -> str:
    """Clean and normalize email content"""
    if not content:
        return ""
    
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    
    # Remove common email footer text
    footer_patterns = [
        r'©\s*Instagram.*?\n',
        r'This message was sent to.*?\n',
        r'Meta Platforms, Inc\..*?\n',
    ]
    
    for pattern in footer_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    return content.strip()


def validate_code(code: str) -> bool:
    """Validate if string is a valid Instagram verification code"""
    if not code:
        return False
    
    # Must be 6 digits
    if not re.match(r'^\d{6}$', code):
        return False
    
    # Filter out obvious non-codes
    if code == '000000' or code == '123456':
        return False  # Too common/test codes
    
    return True

"""
Data Generators - Generate random user data for Instagram accounts
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Tuple
from faker import Faker


class DataGenerator:
    """Generate random user data for Instagram accounts"""
    
    def __init__(self, locale: str = 'en_US'):
        self.fake = Faker(locale)
        self.used_usernames = set()
        self.used_emails = set()
    
    def generate_full_name(self) -> str:
        """Generate random full name"""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        return f"{first_name} {last_name}"
    
    def generate_username(self, full_name: str = None, check_availability: bool = False) -> str:
        """Generate random username based on name or completely random"""
        if full_name:
            # Generate from name
            parts = full_name.lower().split()
            patterns = [
                lambda p: f"{p[0]}{p[-1]}{random.randint(10, 999)}",
                lambda p: f"{p[0][0]}{p[-1]}{random.randint(100, 9999)}",
                lambda p: f"{p[0]}.{p[-1]}{random.randint(10, 99)}",
                lambda p: f"{p[0]}_{p[-1]}_{random.randint(1, 999)}",
                lambda p: f"{p[0]}{random.randint(1000, 99999)}",
            ]
            pattern = random.choice(patterns)
            username = pattern(parts)
        else:
            # Completely random
            username = self.fake.user_name() + str(random.randint(10, 999))
        
        # Ensure uniqueness
        base_username = username
        counter = 1
        while username in self.used_usernames:
            username = f"{base_username}{counter}"
            counter += 1
        
        self.used_usernames.add(username)
        return username
    
    def generate_birthdate(self, min_age: int = 18, max_age: int = 45) -> Dict:
        """Generate random birthdate above minimum age"""
        today = datetime.now()
        max_date = today - timedelta(days=min_age * 365)
        min_date = today - timedelta(days=max_age * 365)
        
        random_date = min_date + timedelta(
            seconds=random.randint(0, int((max_date - min_date).total_seconds()))
        )
        
        return {
            'day': random_date.day,
            'month': random_date.month,
            'year': random_date.year,
            'date': random_date,
            'age': today.year - random_date.year
        }
    
    def generate_password(self, length: int = 12) -> str:
        """Generate strong password - default is P@ssword81297"""
        # Default password as requested
        return "P@ssword81297"
    
    def generate_email(self, username: str = None, domain: str = None) -> str:
        """Generate email address"""
        if not username:
            username = self.fake.user_name()
        if not domain:
            domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'protonmail.com']
            domain = random.choice(domains)
        
        email = f"{username}@{domain}".lower()
        
        # Ensure uniqueness
        base_email = email
        counter = 1
        while email in self.used_emails:
            email = f"{username}{counter}@{domain}"
            counter += 1
        
        self.used_emails.add(email)
        return email
    
    def generate_phone(self) -> str:
        """Generate random phone number"""
        return self.fake.phone_number()
    
    def generate_bio(self) -> str:
        """Generate random bio text"""
        bios = [
            "Living life one day at a time ✨",
            "Just here to share my journey 🌟",
            "Photography lover 📸",
            "Travel enthusiast 🌍",
            "Food lover 🍕",
            "Fitness journey 💪",
            "Music is life 🎵",
            "Dream big, work hard 💫",
            "Creating memories 📷",
            "Positive vibes only ✌️"
        ]
        return random.choice(bios)
    
    def generate_complete_profile(self) -> Dict:
        """Generate complete user profile"""
        full_name = self.generate_full_name()
        username = self.generate_username(full_name)
        birthdate = self.generate_birthdate()
        
        return {
            'full_name': full_name,
            'username': username,
            'email': self.generate_email(username),
            'password': self.generate_password(),
            'birthdate': birthdate,
            'phone': self.generate_phone(),
            'bio': self.generate_bio()
        }
    
    def generate_multiple_profiles(self, count: int) -> list:
        """Generate multiple user profiles"""
        return [self.generate_complete_profile() for _ in range(count)]


class UsernameChecker:
    """Check username availability on Instagram"""
    
    def __init__(self):
        self.generator = DataGenerator()
    
    def generate_available_usernames(self, count: int, check_callback=None) -> list:
        """Generate list of usernames and check availability"""
        usernames = []
        attempts = 0
        max_attempts = count * 3  # Try 3x the requested amount
        
        while len(usernames) < count and attempts < max_attempts:
            username = self.generator.generate_username()
            
            if check_callback:
                is_available = check_callback(username)
                if is_available:
                    usernames.append(username)
            else:
                usernames.append(username)
            
            attempts += 1
        
        return usernames


# Utility functions
def generate_random_string(length: int = 10, chars: str = None) -> str:
    """Generate random string"""
    if chars is None:
        chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_device_info() -> Dict:
    """Generate fake device information"""
    devices = [
        {'model': 'iPhone 14 Pro', 'os': 'iOS 17.0'},
        {'model': 'iPhone 13', 'os': 'iOS 16.5'},
        {'model': 'Samsung Galaxy S23', 'os': 'Android 13'},
        {'model': 'Google Pixel 7', 'os': 'Android 13'},
        {'model': 'iPhone 12', 'os': 'iOS 16.0'},
    ]
    return random.choice(devices)

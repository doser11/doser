"""
Account Manager - Manage created Instagram accounts
"""

import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class AccountManager:
    """Manage and store created Instagram accounts"""
    
    def __init__(self, storage_dir: str = "accounts"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.accounts_file = self.storage_dir / "accounts.json"
        self.accounts: List[Dict] = self._load_accounts()
    
    def _load_accounts(self) -> List[Dict]:
        """Load accounts from storage"""
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load accounts: {e}")
        return []
    
    def _save_accounts(self):
        """Save accounts to storage"""
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save accounts: {e}")
    
    def add_account(
        self,
        username: str,
        password: str,
        email: str,
        full_name: str = None,
        phone: str = None,
        proxy: str = None,
        status: str = "active"
    ) -> Dict:
        """Add new account"""
        account = {
            'id': len(self.accounts) + 1,
            'username': username,
            'password': password,
            'email': email,
            'full_name': full_name,
            'phone': phone,
            'proxy': proxy,
            'status': status,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'followers': 0,
            'following': 0,
            'posts': 0
        }
        
        self.accounts.append(account)
        self._save_accounts()
        
        logger.info(f"Account added: {username}")
        return account
    
    def get_account(self, username: str) -> Optional[Dict]:
        """Get account by username"""
        for acc in self.accounts:
            if acc['username'] == username:
                return acc
        return None
    
    def get_all_accounts(self) -> List[Dict]:
        """Get all accounts"""
        return self.accounts.copy()
    
    def get_active_accounts(self) -> List[Dict]:
        """Get active accounts only"""
        return [acc for acc in self.accounts if acc['status'] == 'active']
    
    def update_account(self, username: str, updates: Dict) -> bool:
        """Update account information"""
        for acc in self.accounts:
            if acc['username'] == username:
                acc.update(updates)
                acc['updated_at'] = datetime.now().isoformat()
                self._save_accounts()
                logger.info(f"Account updated: {username}")
                return True
        return False
    
    def delete_account(self, username: str) -> bool:
        """Delete account"""
        for i, acc in enumerate(self.accounts):
            if acc['username'] == username:
                self.accounts.pop(i)
                self._save_accounts()
                logger.info(f"Account deleted: {username}")
                return True
        return False
    
    def export_to_txt(self, filepath: str) -> bool:
        """Export accounts to text file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("DOSER - Instagram Accounts\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                for acc in self.accounts:
                    f.write(f"Username: {acc['username']}\n")
                    f.write(f"Password: {acc['password']}\n")
                    f.write(f"Email: {acc['email']}\n")
                    f.write(f"Full Name: {acc.get('full_name', 'N/A')}\n")
                    f.write(f"Status: {acc['status']}\n")
                    f.write(f"Created: {acc.get('created_at', 'N/A')}\n")
                    f.write("-" * 40 + "\n\n")
            
            logger.info(f"Accounts exported to TXT: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Export to TXT failed: {e}")
            return False
    
    def export_to_csv(self, filepath: str) -> bool:
        """Export accounts to CSV file"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                if self.accounts:
                    writer = csv.DictWriter(f, fieldnames=self.accounts[0].keys())
                    writer.writeheader()
                    writer.writerows(self.accounts)
            
            logger.info(f"Accounts exported to CSV: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Export to CSV failed: {e}")
            return False
    
    def export_to_json(self, filepath: str) -> bool:
        """Export accounts to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Accounts exported to JSON: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Export to JSON failed: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get account statistics"""
        total = len(self.accounts)
        active = len(self.get_active_accounts())
        disabled = total - active
        
        return {
            'total_accounts': total,
            'active': active,
            'disabled': disabled,
            'created_today': len([
                acc for acc in self.accounts
                if acc.get('created_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))
            ]),
            'created_this_week': len([
                acc for acc in self.accounts
                if self._is_this_week(acc.get('created_at', ''))
            ])
        }
    
    def _is_this_week(self, date_str: str) -> bool:
        """Check if date is in current week"""
        try:
            from datetime import datetime, timedelta
            date = datetime.fromisoformat(date_str)
            now = datetime.now()
            week_ago = now - timedelta(days=7)
            return week_ago <= date <= now
        except:
            return False
    
    def search_accounts(self, query: str) -> List[Dict]:
        """Search accounts by username or email"""
        results = []
        query = query.lower()
        
        for acc in self.accounts:
            if (query in acc.get('username', '').lower() or
                query in acc.get('email', '').lower() or
                query in acc.get('full_name', '').lower()):
                results.append(acc)
        
        return results
    
    def bulk_update_status(self, usernames: List[str], status: str) -> int:
        """Update status for multiple accounts"""
        updated = 0
        for username in usernames:
            if self.update_account(username, {'status': status}):
                updated += 1
        return updated

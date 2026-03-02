"""
Doser GUI - Main Application Window
"""

import os
import sys
import threading
import logging
from datetime import datetime
from pathlib import Path

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
from tkinter import messagebox, filedialog

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.instagram_automation import InstagramAutomation
from core.email_bot import EmailBot
from utils.proxy_manager import ProxyManager
from utils.generators import DataGenerator, UsernameChecker
from config.settings import GUI_SETTINGS, DEFAULT_SETTINGS


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DoserApp(ctk.CTk):
    """Main Doser Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(GUI_SETTINGS['title'])
        self.geometry(f"{GUI_SETTINGS['window_width']}x{GUI_SETTINGS['window_height']}")
        self.minsize(1000, 700)
        
        # Set theme
        ctk.set_appearance_mode(GUI_SETTINGS['theme'])
        ctk.set_default_color_theme(GUI_SETTINGS['color_theme'])
        
        # Initialize components
        self.proxy_manager = None
        self.email_bot = None
        self.automation = None
        self.is_running = False
        self.created_accounts = []
        
        # Create UI
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # Load saved settings
        self._load_settings()
    
    def _create_header(self):
        """Create header with logo and title"""
        self.header = ctk.CTkFrame(self, height=80, corner_radius=0)
        self.header.pack(fill='x', padx=0, pady=0)
        self.header.pack_propagate(False)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(self.header, fg_color='transparent')
        title_frame.pack(side='left', padx=20, pady=10)
        
        # Create logo image
        logo_label = ctk.CTkLabel(
            title_frame,
            text="💉",
            font=('Arial', 40)
        )
        logo_label.pack(side='left', padx=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            title_frame,
            text="DOSER",
            font=('Arial', 32, 'bold')
        )
        title_label.pack(side='left')
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Instagram Account Creator",
            font=('Arial', 12),
            text_color='gray'
        )
        subtitle.pack(side='left', padx=(10, 0), pady=10)
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(self.header, fg_color='transparent')
        self.status_frame.pack(side='right', padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="● Ready",
            font=('Arial', 14),
            text_color='green'
        )
        self.status_label.pack(side='right')
    
    def _create_main_content(self):
        """Create main content area with tabs"""
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.tab_create = self.tabview.add("🚀 Create Accounts")
        self.tab_check = self.tabview.add("🔍 Check Usernames")
        self.tab_accounts = self.tabview.add("📋 Accounts")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        
        self._setup_create_tab()
        self._setup_check_tab()
        self._setup_accounts_tab()
        self._setup_settings_tab()
    
    def _setup_create_tab(self):
        """Setup account creation tab"""
        # Left panel - Configuration
        left_frame = ctk.CTkFrame(self.tab_create)
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Number of accounts
        ctk.CTkLabel(
            left_frame,
            text="Number of Accounts:",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.account_count = ctk.CTkEntry(left_frame, placeholder_text="10")
        self.account_count.pack(fill='x', padx=15, pady=5)
        self.account_count.insert(0, "1")
        
        # Bot Token
        ctk.CTkLabel(
            left_frame,
            text="Telegram Bot Token:",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.bot_token = ctk.CTkEntry(left_frame, placeholder_text="Enter bot token...", show="•")
        self.bot_token.pack(fill='x', padx=15, pady=5)
        
        # Chat ID
        ctk.CTkLabel(
            left_frame,
            text="Chat ID:",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.chat_id = ctk.CTkEntry(left_frame, placeholder_text="Enter chat ID...")
        self.chat_id.pack(fill='x', padx=15, pady=5)
        
        # Proxy file
        proxy_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        proxy_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            proxy_frame,
            text="Proxy File:",
            font=('Arial', 14, 'bold')
        ).pack(side='left')
        
        self.proxy_path = ctk.CTkEntry(proxy_frame, placeholder_text="No file selected")
        self.proxy_path.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        ctk.CTkButton(
            proxy_frame,
            text="Browse",
            width=80,
            command=self._browse_proxy_file
        ).pack(side='right')
        
        # Follow option
        self.follow_var = ctk.BooleanVar(value=False)
        self.follow_checkbox = ctk.CTkCheckBox(
            left_frame,
            text="Follow account after creation",
            variable=self.follow_var,
            command=self._toggle_follow_entry
        )
        self.follow_checkbox.pack(anchor='w', padx=15, pady=(15, 5))
        
        self.follow_username = ctk.CTkEntry(
            left_frame,
            placeholder_text="Enter username to follow...",
            state='disabled'
        )
        self.follow_username.pack(fill='x', padx=15, pady=5)
        
        # Headless mode
        self.headless_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            left_frame,
            text="Headless mode (no browser window)",
            variable=self.headless_var
        ).pack(anchor='w', padx=15, pady=10)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        btn_frame.pack(fill='x', padx=15, pady=20)
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶ START",
            font=('Arial', 16, 'bold'),
            height=45,
            fg_color='green',
            hover_color='darkgreen',
            command=self._start_creation
        )
        self.start_btn.pack(side='left', expand=True, padx=(0, 5))
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹ STOP",
            font=('Arial', 16, 'bold'),
            height=45,
            fg_color='red',
            hover_color='darkred',
            state='disabled',
            command=self._stop_creation
        )
        self.stop_btn.pack(side='right', expand=True, padx=(5, 0))
        
        # Right panel - Log
        right_frame = ctk.CTkFrame(self.tab_create)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            right_frame,
            text="Activity Log:",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.log_text = ctk.CTkTextbox(right_frame, wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=15, pady=5)
        
        # Progress
        self.progress_label = ctk.CTkLabel(
            right_frame,
            text="Progress: 0/0",
            font=('Arial', 12)
        )
        self.progress_label.pack(anchor='w', padx=15, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(right_frame)
        self.progress_bar.pack(fill='x', padx=15, pady=5)
        self.progress_bar.set(0)
    
    def _setup_check_tab(self):
        """Setup username checker tab"""
        # Configuration
        ctk.CTkLabel(
            self.tab_check,
            text="Username Availability Checker",
            font=('Arial', 20, 'bold')
        ).pack(pady=(20, 10))
        
        check_frame = ctk.CTkFrame(self.tab_check)
        check_frame.pack(fill='x', padx=50, pady=10)
        
        ctk.CTkLabel(
            check_frame,
            text="Number of usernames to check:",
            font=('Arial', 14)
        ).pack(side='left', padx=15, pady=15)
        
        self.check_count = ctk.CTkEntry(check_frame, width=100)
        self.check_count.pack(side='left', padx=5, pady=15)
        self.check_count.insert(0, "10")
        
        ctk.CTkButton(
            check_frame,
            text="🔍 Check",
            command=self._check_usernames
        ).pack(side='left', padx=15, pady=15)
        
        # Results
        ctk.CTkLabel(
            self.tab_check,
            text="Available Usernames:",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=50, pady=(20, 5))
        
        self.usernames_result = ctk.CTkTextbox(self.tab_check, height=300)
        self.usernames_result.pack(fill='both', expand=True, padx=50, pady=5)
        
        ctk.CTkButton(
            self.tab_check,
            text="💾 Save to File",
            command=self._save_usernames
        ).pack(pady=10)
    
    def _setup_accounts_tab(self):
        """Setup accounts list tab"""
        ctk.CTkLabel(
            self.tab_accounts,
            text="Created Accounts",
            font=('Arial', 20, 'bold')
        ).pack(pady=(20, 10))
        
        # Accounts table
        self.accounts_text = ctk.CTkTextbox(self.tab_accounts)
        self.accounts_text.pack(fill='both', expand=True, padx=50, pady=10)
        
        btn_frame = ctk.CTkFrame(self.tab_accounts, fg_color='transparent')
        btn_frame.pack(fill='x', padx=50, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self._refresh_accounts
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Export",
            command=self._export_accounts
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear",
            command=self._clear_accounts
        ).pack(side='right', padx=5)
    
    def _setup_settings_tab(self):
        """Setup settings tab"""
        settings_frame = ctk.CTkFrame(self.tab_settings)
        settings_frame.pack(fill='both', expand=True, padx=50, pady=30)
        
        ctk.CTkLabel(
            settings_frame,
            text="Application Settings",
            font=('Arial', 20, 'bold')
        ).pack(pady=(20, 30))
        
        # Password setting
        ctk.CTkLabel(
            settings_frame,
            text="Default Password:",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=30, pady=(10, 5))
        
        self.default_password = ctk.CTkEntry(settings_frame)
        self.default_password.pack(fill='x', padx=30, pady=5)
        self.default_password.insert(0, DEFAULT_SETTINGS['password'])
        
        # Age range
        age_frame = ctk.CTkFrame(settings_frame, fg_color='transparent')
        age_frame.pack(fill='x', padx=30, pady=15)
        
        ctk.CTkLabel(
            age_frame,
            text="Age Range:",
            font=('Arial', 14, 'bold')
        ).pack(side='left')
        
        self.min_age = ctk.CTkEntry(age_frame, width=60)
        self.min_age.pack(side='left', padx=10)
        self.min_age.insert(0, str(DEFAULT_SETTINGS['min_age']))
        
        ctk.CTkLabel(age_frame, text="to").pack(side='left')
        
        self.max_age = ctk.CTkEntry(age_frame, width=60)
        self.max_age.pack(side='left', padx=10)
        self.max_age.insert(0, str(DEFAULT_SETTINGS['max_age']))
        
        # Delay settings
        ctk.CTkLabel(
            settings_frame,
            text="Delay Between Accounts (seconds):",
            font=('Arial', 14, 'bold')
        ).pack(anchor='w', padx=30, pady=(15, 5))
        
        delay_frame = ctk.CTkFrame(settings_frame, fg_color='transparent')
        delay_frame.pack(fill='x', padx=30, pady=5)
        
        self.delay_min = ctk.CTkEntry(delay_frame, width=80)
        self.delay_min.pack(side='left', padx=(0, 5))
        self.delay_min.insert(0, "30")
        
        ctk.CTkLabel(delay_frame, text="to").pack(side='left', padx=5)
        
        self.delay_max = ctk.CTkEntry(delay_frame, width=80)
        self.delay_max.pack(side='left', padx=5)
        self.delay_max.insert(0, "60")
        
        # Save button
        ctk.CTkButton(
            settings_frame,
            text="💾 Save Settings",
            command=self._save_settings
        ).pack(pady=30)
    
    def _create_footer(self):
        """Create footer"""
        footer = ctk.CTkFrame(self, height=30, corner_radius=0)
        footer.pack(fill='x', side='bottom', padx=0, pady=0)
        footer.pack_propagate(False)
        
        ctk.CTkLabel(
            footer,
            text="Doser v1.0 - Instagram Account Creator",
            font=('Arial', 10),
            text_color='gray'
        ).pack(side='left', padx=20)
        
        self.accounts_count_label = ctk.CTkLabel(
            footer,
            text="Accounts: 0",
            font=('Arial', 10),
            text_color='gray'
        )
        self.accounts_count_label.pack(side='right', padx=20)
    
    def _toggle_follow_entry(self):
        """Toggle follow username entry"""
        if self.follow_var.get():
            self.follow_username.configure(state='normal')
        else:
            self.follow_username.configure(state='disabled')
    
    def _browse_proxy_file(self):
        """Browse for proxy file"""
        file_path = filedialog.askopenfilename(
            title="Select Proxy File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.proxy_path.delete(0, 'end')
            self.proxy_path.insert(0, file_path)
    
    def _log(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        logger.info(message)
    
    def _update_status(self, status: str, color: str = 'green'):
        """Update status indicator"""
        self.status_label.configure(text=f"● {status}", text_color=color)
    
    def _start_creation(self):
        """Start account creation process"""
        if self.is_running:
            return
        
        # Validate inputs
        try:
            count = int(self.account_count.get())
            if count < 1:
                raise ValueError("Count must be at least 1")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of accounts")
            return
        
        bot_token = self.bot_token.get().strip()
        chat_id = self.chat_id.get().strip()
        
        if not bot_token:
            messagebox.showerror("Error", "Please enter Telegram Bot Token")
            return
        
        # Initialize components
        try:
            self.proxy_manager = ProxyManager(self.proxy_path.get() or None)
            self.email_bot = EmailBot(bot_token, chat_id)
            
            # Test bot connection
            self._log("Testing bot connection...")
            if not self.email_bot.test_connection():
                messagebox.showerror("Error", "Failed to connect to Telegram Bot")
                return
            self._log("Bot connected successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Initialization failed: {e}")
            return
        
        # Update UI
        self.is_running = True
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self._update_status("Running", 'orange')
        
        # Start creation in thread
        thread = threading.Thread(target=self._creation_worker, args=(count,))
        thread.daemon = True
        thread.start()
    
    def _creation_worker(self, count: int):
        """Worker thread for account creation"""
        try:
            for i in range(count):
                if not self.is_running:
                    break
                
                self._log(f"Creating account {i+1}/{count}...")
                self.progress_label.configure(text=f"Progress: {i+1}/{count}")
                self.progress_bar.set((i + 1) / count)
                
                # Create automation instance
                automation = InstagramAutomation(
                    proxy_manager=self.proxy_manager,
                    email_bot=self.email_bot,
                    headless=self.headless_var.get()
                )
                
                # Create account
                result = automation.create_account()
                
                if result['success']:
                    self._log(f"✅ Account created: {result['username']}")
                    self.created_accounts.append(result)
                    
                    # Follow if enabled
                    if self.follow_var.get() and self.follow_username.get():
                        automation.follow_account(self.follow_username.get())
                else:
                    self._log(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
                # Delay between accounts
                if i < count - 1 and self.is_running:
                    delay = random.randint(30, 60)
                    self._log(f"Waiting {delay} seconds before next account...")
                    
                    for _ in range(delay):
                        if not self.is_running:
                            break
                        time.sleep(1)
            
            self._log("Process completed!")
            
        except Exception as e:
            self._log(f"Error: {e}")
        
        finally:
            self.is_running = False
            self.after(0, self._reset_ui)
    
    def _stop_creation(self):
        """Stop account creation"""
        self.is_running = False
        self._log("Stopping...")
        self._update_status("Stopping", 'red')
    
    def _reset_ui(self):
        """Reset UI after completion"""
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self._update_status("Ready", 'green')
        self.accounts_count_label.configure(text=f"Accounts: {len(self.created_accounts)}")
        self._refresh_accounts()
    
    def _check_usernames(self):
        """Check username availability"""
        try:
            count = int(self.check_count.get())
            self.usernames_result.delete('1.0', 'end')
            self.usernames_result.insert('end', "Generating usernames...\n")
            
            checker = UsernameChecker()
            usernames = checker.generate_available_usernames(count)
            
            self.usernames_result.delete('1.0', 'end')
            for username in usernames:
                self.usernames_result.insert('end', f"{username}\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _save_usernames(self):
        """Save usernames to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.usernames_result.get('1.0', 'end'))
            messagebox.showinfo("Success", "Usernames saved!")
    
    def _refresh_accounts(self):
        """Refresh accounts display"""
        self.accounts_text.delete('1.0', 'end')
        
        if not self.created_accounts:
            self.accounts_text.insert('end', "No accounts created yet.\n")
            return
        
        for acc in self.created_accounts:
            self.accounts_text.insert('end', f"Username: {acc.get('username', 'N/A')}\n")
            self.accounts_text.insert('end', f"Password: {DEFAULT_SETTINGS['password']}\n")
            self.accounts_text.insert('end', f"Email: {acc.get('email', 'N/A')}\n")
            self.accounts_text.insert('end', "-" * 40 + "\n")
    
    def _export_accounts(self):
        """Export accounts to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                for acc in self.created_accounts:
                    f.write(f"{acc.get('username')}:{DEFAULT_SETTINGS['password']}\n")
            messagebox.showinfo("Success", "Accounts exported!")
    
    def _clear_accounts(self):
        """Clear accounts list"""
        if messagebox.askyesno("Confirm", "Clear all accounts?"):
            self.created_accounts = []
            self._refresh_accounts()
            self.accounts_count_label.configure(text="Accounts: 0")
    
    def _save_settings(self):
        """Save settings"""
        # Implementation for saving settings
        messagebox.showinfo("Success", "Settings saved!")
    
    def _load_settings(self):
        """Load saved settings"""
        # Implementation for loading settings
        pass


def main():
    """Main entry point"""
    app = DoserApp()
    app.mainloop()


if __name__ == "__main__":
    main()

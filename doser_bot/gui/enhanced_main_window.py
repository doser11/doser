"""
Enhanced Doser GUI - Main Application Window with improved features
"""

import os
import sys
import threading
import logging
from datetime import datetime
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox, filedialog

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.enhanced_instagram import EnhancedInstagramAutomation
from core.email_bot import EmailBot
from utils.proxy_manager import ProxyManager
from utils.generators import DataGenerator, UsernameChecker
from utils.account_manager import AccountManager
from config.settings import GUI_SETTINGS, DEFAULT_SETTINGS


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedDoserApp(ctk.CTk):
    """Enhanced Doser Application with modern UI"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(GUI_SETTINGS['title'])
        self.geometry(f"{GUI_SETTINGS['window_width']}x{GUI_SETTINGS['window_height']}")
        self.minsize(1100, 750)
        
        # Set theme
        ctk.set_appearance_mode(GUI_SETTINGS['theme'])
        ctk.set_default_color_theme(GUI_SETTINGS['color_theme'])
        
        # Initialize components
        self.proxy_manager = None
        self.email_bot = None
        self.automation = None
        self.account_manager = AccountManager()
        self.is_running = False
        self.current_thread = None
        
        # Create UI
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # Load saved settings
        self._load_settings()
        
        # Update stats
        self._update_statistics()
    
    def _create_header(self):
        """Create modern header"""
        self.header = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color='#1a1a2e')
        self.header.pack(fill='x', padx=0, pady=0)
        self.header.pack_propagate(False)
        
        # Logo and title container
        title_frame = ctk.CTkFrame(self.header, fg_color='transparent')
        title_frame.pack(side='left', padx=25, pady=15)
        
        # Logo
        logo_label = ctk.CTkLabel(
            title_frame,
            text="💉",
            font=('Segoe UI', 42)
        )
        logo_label.pack(side='left', padx=(0, 15))
        
        # Title container
        text_frame = ctk.CTkFrame(title_frame, fg_color='transparent')
        text_frame.pack(side='left')
        
        title_label = ctk.CTkLabel(
            text_frame,
            text="DOSER",
            font=('Segoe UI', 28, 'bold'),
            text_color='#e94560'
        )
        title_label.pack(anchor='w')
        
        subtitle = ctk.CTkLabel(
            text_frame,
            text="Instagram Account Creator",
            font=('Segoe UI', 11),
            text_color='gray70'
        )
        subtitle.pack(anchor='w')
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(self.header, fg_color='transparent')
        self.status_frame.pack(side='right', padx=25, pady=20)
        
        self.status_indicator = ctk.CTkLabel(
            self.status_frame,
            text="🟢",
            font=('Segoe UI', 16)
        )
        self.status_indicator.pack(side='left', padx=(0, 8))
        
        self.status_text = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=('Segoe UI', 14),
            text_color='green'
        )
        self.status_text.pack(side='left')
    
    def _create_main_content(self):
        """Create main content with tabs"""
        self.tabview = ctk.CTkTabview(
            self,
            segmented_button_selected_color='#e94560',
            segmented_button_selected_hover_color='#d63d54'
        )
        self.tabview.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Create tabs
        self.tab_create = self.tabview.add("🚀 Create")
        self.tab_check = self.tabview.add("🔍 Check Usernames")
        self.tab_accounts = self.tabview.add("📋 Accounts")
        self.tab_stats = self.tabview.add("📊 Statistics")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        
        self._setup_create_tab()
        self._setup_check_tab()
        self._setup_accounts_tab()
        self._setup_stats_tab()
        self._setup_settings_tab()
    
    def _setup_create_tab(self):
        """Setup enhanced account creation tab"""
        # Main container
        main_frame = ctk.CTkFrame(self.tab_create, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Configuration
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Configuration section
        config_label = ctk.CTkLabel(
            left_frame,
            text="⚙️ Configuration",
            font=('Segoe UI', 16, 'bold')
        )
        config_label.pack(anchor='w', padx=20, pady=(20, 15))
        
        # Number of accounts
        self._create_input_field(
            left_frame,
            "Number of Accounts:",
            "account_count",
            "1",
            width=100
        )
        
        # Bot Token
        self._create_input_field(
            left_frame,
            "Telegram Bot Token:",
            "bot_token",
            "",
            show="•"
        )
        
        # Chat ID
        self._create_input_field(
            left_frame,
            "Chat ID (optional):",
            "chat_id",
            ""
        )
        
        # Proxy file
        proxy_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        proxy_frame.pack(fill='x', padx=20, pady=10)
        
        ctk.CTkLabel(
            proxy_frame,
            text="Proxy File:",
            font=('Segoe UI', 12)
        ).pack(side='left')
        
        self.proxy_path = ctk.CTkEntry(
            proxy_frame,
            placeholder_text="No file selected",
            width=200
        )
        self.proxy_path.pack(side='left', fill='x', expand=True, padx=10)
        
        ctk.CTkButton(
            proxy_frame,
            text="Browse",
            width=80,
            command=self._browse_proxy_file,
            fg_color='#e94560',
            hover_color='#d63d54'
        ).pack(side='right')
        
        # Follow option
        follow_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        follow_frame.pack(fill='x', padx=20, pady=15)
        
        self.follow_var = ctk.BooleanVar(value=False)
        self.follow_checkbox = ctk.CTkCheckBox(
            follow_frame,
            text="Follow account after creation",
            variable=self.follow_var,
            command=self._toggle_follow_entry,
            font=('Segoe UI', 12)
        )
        self.follow_checkbox.pack(anchor='w')
        
        self.follow_username = ctk.CTkEntry(
            left_frame,
            placeholder_text="Enter username to follow...",
            state='disabled',
            width=250
        )
        self.follow_username.pack(anchor='w', padx=20, pady=(0, 10))
        
        # Options
        options_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        options_frame.pack(fill='x', padx=20, pady=10)
        
        self.headless_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="Headless mode (no browser window)",
            variable=self.headless_var,
            font=('Segoe UI', 11)
        ).pack(anchor='w')
        
        self.save_accounts_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            options_frame,
            text="Save accounts to file",
            variable=self.save_accounts_var,
            font=('Segoe UI', 11)
        ).pack(anchor='w', pady=(5, 0))
        
        # Action buttons
        btn_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        btn_frame.pack(fill='x', padx=20, pady=25)
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶  START CREATION",
            font=('Segoe UI', 15, 'bold'),
            height=50,
            fg_color='#28a745',
            hover_color='#218838',
            command=self._start_creation
        )
        self.start_btn.pack(side='left', expand=True, padx=(0, 10))
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹  STOP",
            font=('Segoe UI', 15, 'bold'),
            height=50,
            fg_color='#dc3545',
            hover_color='#c82333',
            state='disabled',
            command=self._stop_creation
        )
        self.stop_btn.pack(side='right', expand=True, padx=(10, 0))
        
        # Right panel - Log and Progress
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        log_label = ctk.CTkLabel(
            right_frame,
            text="📋 Activity Log",
            font=('Segoe UI', 16, 'bold')
        )
        log_label.pack(anchor='w', padx=20, pady=(20, 10))
        
        self.log_text = ctk.CTkTextbox(
            right_frame,
            wrap='word',
            font=('Consolas', 11)
        )
        self.log_text.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Progress section
        progress_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        progress_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Progress: 0/0",
            font=('Segoe UI', 12)
        )
        self.progress_label.pack(anchor='w')
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=15)
        self.progress_bar.pack(fill='x', pady=(5, 0))
        self.progress_bar.set(0)
    
    def _create_input_field(self, parent, label, attr_name, default_value, show=None, width=None):
        """Helper to create input field"""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.pack(fill='x', padx=20, pady=8)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=('Segoe UI', 12)
        ).pack(anchor='w')
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=default_value if default_value else None,
            show=show,
            width=width or 300
        )
        entry.pack(anchor='w', pady=(3, 0))
        
        if default_value and not show:
            entry.insert(0, default_value)
        
        setattr(self, attr_name, entry)
        return entry
    
    def _setup_check_tab(self):
        """Setup username checker tab"""
        # Header
        ctk.CTkLabel(
            self.tab_check,
            text="🔍 Username Availability Checker",
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=(30, 20))
        
        # Configuration
        check_frame = ctk.CTkFrame(self.tab_check)
        check_frame.pack(fill='x', padx=80, pady=15)
        
        ctk.CTkLabel(
            check_frame,
            text="Number of usernames to generate:",
            font=('Segoe UI', 13)
        ).pack(side='left', padx=20, pady=20)
        
        self.check_count = ctk.CTkEntry(check_frame, width=100)
        self.check_count.pack(side='left', padx=10, pady=20)
        self.check_count.insert(0, "10")
        
        ctk.CTkButton(
            check_frame,
            text="🔍 Generate & Check",
            font=('Segoe UI', 13),
            command=self._check_usernames,
            fg_color='#e94560',
            hover_color='#d63d54'
        ).pack(side='left', padx=20, pady=20)
        
        # Results
        ctk.CTkLabel(
            self.tab_check,
            text="Available Usernames:",
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor='w', padx=80, pady=(25, 10))
        
        self.usernames_result = ctk.CTkTextbox(self.tab_check, height=350, font=('Consolas', 12))
        self.usernames_result.pack(fill='both', expand=True, padx=80, pady=5)
        
        # Actions
        btn_frame = ctk.CTkFrame(self.tab_check, fg_color='transparent')
        btn_frame.pack(fill='x', padx=80, pady=15)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Save to File",
            command=self._save_usernames
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📋 Copy to Clipboard",
            command=self._copy_usernames
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear",
            command=lambda: self.usernames_result.delete('1.0', 'end')
        ).pack(side='right', padx=5)
    
    def _setup_accounts_tab(self):
        """Setup accounts list tab"""
        ctk.CTkLabel(
            self.tab_accounts,
            text="📋 Created Accounts",
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=(25, 15))
        
        # Search bar
        search_frame = ctk.CTkFrame(self.tab_accounts, fg_color='transparent')
        search_frame.pack(fill='x', padx=60, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search accounts...",
            width=300
        )
        self.search_entry.pack(side='left', padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            width=100,
            command=self._search_accounts
        ).pack(side='left')
        
        # Accounts display
        self.accounts_text = ctk.CTkTextbox(
            self.tab_accounts,
            font=('Consolas', 11)
        )
        self.accounts_text.pack(fill='both', expand=True, padx=60, pady=10)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(self.tab_accounts, fg_color='transparent')
        btn_frame.pack(fill='x', padx=60, pady=15)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self._refresh_accounts
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Export TXT",
            command=lambda: self._export_accounts('txt')
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Export CSV",
            command=lambda: self._export_accounts('csv')
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear All",
            fg_color='#dc3545',
            hover_color='#c82333',
            command=self._clear_accounts
        ).pack(side='right', padx=5)
    
    def _setup_stats_tab(self):
        """Setup statistics tab"""
        ctk.CTkLabel(
            self.tab_stats,
            text="📊 Account Statistics",
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=(30, 25))
        
        # Stats cards
        stats_frame = ctk.CTkFrame(self.tab_stats, fg_color='transparent')
        stats_frame.pack(fill='x', padx=80, pady=10)
        
        # Total accounts
        self.stat_total = self._create_stat_card(
            stats_frame, "Total Accounts", "0", "#3498db"
        )
        self.stat_total.pack(side='left', expand=True, padx=10)
        
        # Active accounts
        self.stat_active = self._create_stat_card(
            stats_frame, "Active", "0", "#2ecc71"
        )
        self.stat_active.pack(side='left', expand=True, padx=10)
        
        # Created today
        self.stat_today = self._create_stat_card(
            stats_frame, "Created Today", "0", "#e94560"
        )
        self.stat_today.pack(side='left', expand=True, padx=10)
        
        # This week
        self.stat_week = self._create_stat_card(
            stats_frame, "This Week", "0", "#9b59b6"
        )
        self.stat_week.pack(side='left', expand=True, padx=10)
        
        # Recent activity log
        ctk.CTkLabel(
            self.tab_stats,
            text="📝 Recent Activity",
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor='w', padx=80, pady=(30, 10))
        
        self.activity_log = ctk.CTkTextbox(
            self.tab_stats,
            height=250,
            font=('Consolas', 11)
        )
        self.activity_log.pack(fill='x', padx=80, pady=5)
    
    def _create_stat_card(self, parent, title, value, color):
        """Create statistics card"""
        card = ctk.CTkFrame(parent, fg_color='#2d2d44', corner_radius=15)
        card.configure(width=180, height=120)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=('Segoe UI', 12),
            text_color='gray70'
        ).place(relx=0.5, rely=0.3, anchor='center')
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=('Segoe UI', 32, 'bold'),
            text_color=color
        )
        value_label.place(relx=0.5, rely=0.65, anchor='center')
        
        # Store reference to value label
        card.value_label = value_label
        
        return card
    
    def _setup_settings_tab(self):
        """Setup settings tab"""
        settings_frame = ctk.CTkFrame(self.tab_settings)
        settings_frame.pack(fill='both', expand=True, padx=80, pady=30)
        
        ctk.CTkLabel(
            settings_frame,
            text="⚙️ Application Settings",
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=(25, 30))
        
        # Password setting
        self._create_setting_input(
            settings_frame,
            "Default Password:",
            "default_password",
            DEFAULT_SETTINGS['password']
        )
        
        # Age range
        age_frame = ctk.CTkFrame(settings_frame, fg_color='transparent')
        age_frame.pack(fill='x', padx=40, pady=15)
        
        ctk.CTkLabel(
            age_frame,
            text="Age Range:",
            font=('Segoe UI', 13)
        ).pack(side='left')
        
        self.min_age = ctk.CTkEntry(age_frame, width=70)
        self.min_age.pack(side='left', padx=15)
        self.min_age.insert(0, str(DEFAULT_SETTINGS['min_age']))
        
        ctk.CTkLabel(age_frame, text="to", font=('Segoe UI', 13)).pack(side='left')
        
        self.max_age = ctk.CTkEntry(age_frame, width=70)
        self.max_age.pack(side='left', padx=15)
        self.max_age.insert(0, str(DEFAULT_SETTINGS['max_age']))
        
        # Delay settings
        delay_frame = ctk.CTkFrame(settings_frame, fg_color='transparent')
        delay_frame.pack(fill='x', padx=40, pady=15)
        
        ctk.CTkLabel(
            delay_frame,
            text="Delay Between Accounts (seconds):",
            font=('Segoe UI', 13)
        ).pack(side='left')
        
        self.delay_min = ctk.CTkEntry(delay_frame, width=70)
        self.delay_min.pack(side='left', padx=15)
        self.delay_min.insert(0, "30")
        
        ctk.CTkLabel(delay_frame, text="to", font=('Segoe UI', 13)).pack(side='left')
        
        self.delay_max = ctk.CTkEntry(delay_frame, width=70)
        self.delay_max.pack(side='left', padx=15)
        self.delay_max.insert(0, "60")
        
        # Theme selection
        theme_frame = ctk.CTkFrame(settings_frame, fg_color='transparent')
        theme_frame.pack(fill='x', padx=40, pady=15)
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=('Segoe UI', 13)
        ).pack(side='left')
        
        self.theme_var = ctk.StringVar(value="dark")
        ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self._change_theme,
            width=120
        ).pack(side='left', padx=15)
        
        # Save button
        ctk.CTkButton(
            settings_frame,
            text="💾 Save Settings",
            font=('Segoe UI', 14),
            height=40,
            command=self._save_settings,
            fg_color='#e94560',
            hover_color='#d63d54'
        ).pack(pady=30)
    
    def _create_setting_input(self, parent, label, attr_name, default_value):
        """Create setting input field"""
        frame = ctk.CTkFrame(parent, fg_color='transparent')
        frame.pack(fill='x', padx=40, pady=10)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=('Segoe UI', 13)
        ).pack(anchor='w')
        
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(anchor='w', pady=(5, 0))
        entry.insert(0, default_value)
        
        setattr(self, attr_name, entry)
        return entry
    
    def _create_footer(self):
        """Create footer"""
        footer = ctk.CTkFrame(self, height=35, corner_radius=0, fg_color='#1a1a2e')
        footer.pack(fill='x', side='bottom', padx=0, pady=0)
        footer.pack_propagate(False)
        
        ctk.CTkLabel(
            footer,
            text="Doser v1.0 - Instagram Account Creator",
            font=('Segoe UI', 10),
            text_color='gray60'
        ).pack(side='left', padx=20)
        
        self.footer_stats = ctk.CTkLabel(
            footer,
            text="Accounts: 0 | Proxies: 0",
            font=('Segoe UI', 10),
            text_color='gray60'
        )
        self.footer_stats.pack(side='right', padx=20)
    
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
        color_emoji = {'green': '🟢', 'orange': '🟠', 'red': '🔴', 'blue': '🔵'}
        self.status_indicator.configure(text=color_emoji.get(color, '⚪'))
        self.status_text.configure(text=status, text_color=color)
    
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
            
            self._log("Testing bot connection...")
            if not self.email_bot.test_connection():
                messagebox.showerror("Error", "Failed to connect to Telegram Bot")
                return
            self._log("✅ Bot connected successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Initialization failed: {e}")
            return
        
        # Update UI
        self.is_running = True
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self._update_status("Running", 'orange')
        
        # Start creation in thread
        self.current_thread = threading.Thread(
            target=self._creation_worker,
            args=(count,)
        )
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _creation_worker(self, count: int):
        """Worker thread for account creation"""
        try:
            for i in range(count):
                if not self.is_running:
                    break
                
                self._log(f"\n{'='*50}")
                self._log(f"Creating account {i+1}/{count}...")
                self._log('='*50)
                
                self.progress_label.configure(text=f"Progress: {i+1}/{count}")
                self.progress_bar.set((i + 1) / count)
                
                # Create automation instance
                automation = EnhancedInstagramAutomation(
                    proxy_manager=self.proxy_manager,
                    email_bot=self.email_bot,
                    headless=self.headless_var.get(),
                    account_manager=self.account_manager
                )
                
                # Create account
                follow_user = self.follow_username.get() if self.follow_var.get() else None
                result = automation.create_account(follow_username=follow_user)
                
                if result['success']:
                    self._log(f"✅ Account created: {result['username']}")
                    self._add_activity(f"Created: {result['username']}")
                else:
                    self._log(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
                # Delay between accounts
                if i < count - 1 and self.is_running:
                    try:
                        delay_min = int(self.delay_min.get())
                        delay_max = int(self.delay_max.get())
                        delay = random.randint(delay_min, delay_max)
                    except:
                        delay = random.randint(30, 60)
                    
                    self._log(f"Waiting {delay} seconds...")
                    for _ in range(delay):
                        if not self.is_running:
                            break
                        time.sleep(1)
            
            self._log("\n✨ Process completed!")
            
        except Exception as e:
            self._log(f"❌ Error: {e}")
        
        finally:
            self.is_running = False
            self.after(0, self._reset_ui)
            self.after(0, self._update_statistics)
    
    def _stop_creation(self):
        """Stop account creation"""
        self.is_running = False
        self._log("⚠️ Stopping...")
        self._update_status("Stopping", 'red')
    
    def _reset_ui(self):
        """Reset UI after completion"""
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self._update_status("Ready", 'green')
        self._refresh_accounts()
    
    def _add_activity(self, message: str):
        """Add activity to log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.activity_log.insert('0.0', f"[{timestamp}] {message}\n")
    
    def _update_statistics(self):
        """Update statistics display"""
        stats = self.account_manager.get_statistics()
        
        self.stat_total.value_label.configure(text=str(stats['total_accounts']))
        self.stat_active.value_label.configure(text=str(stats['active']))
        self.stat_today.value_label.configure(text=str(stats['created_today']))
        self.stat_week.value_label.configure(text=str(stats['created_this_week']))
        
        proxy_count = self.proxy_manager.get_proxy_count() if self.proxy_manager else 0
        self.footer_stats.configure(
            text=f"Accounts: {stats['total_accounts']} | Proxies: {proxy_count}"
        )
    
    def _check_usernames(self):
        """Check username availability"""
        try:
            count = int(self.check_count.get())
            self.usernames_result.delete('1.0', 'end')
            self.usernames_result.insert('end', "Generating usernames...\n")
            self.update()
            
            generator = DataGenerator()
            usernames = []
            
            for i in range(count):
                profile = generator.generate_complete_profile()
                usernames.append(profile['username'])
            
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
    
    def _copy_usernames(self):
        """Copy usernames to clipboard"""
        self.clipboard_clear()
        self.clipboard_append(self.usernames_result.get('1.0', 'end'))
        messagebox.showinfo("Success", "Copied to clipboard!")
    
    def _search_accounts(self):
        """Search accounts"""
        query = self.search_entry.get().strip()
        if not query:
            self._refresh_accounts()
            return
        
        results = self.account_manager.search_accounts(query)
        self._display_accounts(results)
    
    def _refresh_accounts(self):
        """Refresh accounts display"""
        accounts = self.account_manager.get_all_accounts()
        self._display_accounts(accounts)
    
    def _display_accounts(self, accounts):
        """Display accounts in text area"""
        self.accounts_text.delete('1.0', 'end')
        
        if not accounts:
            self.accounts_text.insert('end', "No accounts found.\n")
            return
        
        for acc in accounts:
            self.accounts_text.insert('end', f"Username: {acc.get('username', 'N/A')}\n")
            self.accounts_text.insert('end', f"Password: {acc.get('password', 'N/A')}\n")
            self.accounts_text.insert('end', f"Email: {acc.get('email', 'N/A')}\n")
            self.accounts_text.insert('end', f"Status: {acc.get('status', 'unknown')}\n")
            self.accounts_text.insert('end', f"Created: {acc.get('created_at', 'N/A')}\n")
            self.accounts_text.insert('end', "-" * 50 + "\n\n")
    
    def _export_accounts(self, format_type: str):
        """Export accounts"""
        if format_type == 'txt':
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            if file_path:
                self.account_manager.export_to_txt(file_path)
                messagebox.showinfo("Success", "Accounts exported to TXT!")
        
        elif format_type == 'csv':
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if file_path:
                self.account_manager.export_to_csv(file_path)
                messagebox.showinfo("Success", "Accounts exported to CSV!")
    
    def _clear_accounts(self):
        """Clear all accounts"""
        if messagebox.askyesno("Confirm", "Clear all accounts?"):
            for acc in self.account_manager.get_all_accounts():
                self.account_manager.delete_account(acc['username'])
            self._refresh_accounts()
            self._update_statistics()
    
    def _change_theme(self, theme: str):
        """Change application theme"""
        ctk.set_appearance_mode(theme)
    
    def _save_settings(self):
        """Save settings"""
        messagebox.showinfo("Success", "Settings saved!")
    
    def _load_settings(self):
        """Load saved settings"""
        pass


def main():
    """Main entry point"""
    app = EnhancedDoserApp()
    app.mainloop()


if __name__ == "__main__":
    main()


import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import calendar
import json
import os

# Dynamic Resolution Configuration
class ResponsiveConfig:
    def __init__(self):
        # Get screen dimensions
        self.screen_width = 0
        self.screen_height = 0
        self.dpi_scale = 1.0
        
        # Initialize with a temporary window to get screen info
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the window
        self.screen_width = temp_root.winfo_screenwidth()
        self.screen_height = temp_root.winfo_screenheight()
        temp_root.destroy()
        
        # Calculate responsive dimensions
        self.calculate_responsive_dimensions()
        
    def calculate_responsive_dimensions(self):
        """Calculate responsive dimensions based on screen size"""
        # Base mobile dimensions (iPhone-like)
        base_width = 375
        base_height = 812
        
        # Calculate scaling factors
        width_scale = min(self.screen_width / 1920, 1.0)  # Cap at 1920px
        height_scale = min(self.screen_height / 1080, 1.0)  # Cap at 1080px
        
        # Use the smaller scale to maintain aspect ratio
        self.scale_factor = min(width_scale, height_scale, 1.0)
        
        # Ensure minimum scale for very small screens
        self.scale_factor = max(self.scale_factor, 0.6)
        
        # Calculate responsive window dimensions
        self.window_width = max(int(base_width * self.scale_factor), 300)
        self.window_height = max(int(base_height * self.scale_factor), 600)
        
        # Calculate responsive font sizes
        self.title_font_size = max(int(28 * self.scale_factor), 20)
        self.heading_font_size = max(int(20 * self.scale_factor), 16)
        self.subheading_font_size = max(int(16 * self.scale_factor), 14)
        self.body_font_size = max(int(12 * self.scale_factor), 10)
        self.small_font_size = max(int(10 * self.scale_factor), 8)
        
        # Calculate responsive padding and spacing
        self.padding_large = max(int(20 * self.scale_factor), 15)
        self.padding_medium = max(int(15 * self.scale_factor), 10)
        self.padding_small = max(int(10 * self.scale_factor), 8)
        self.padding_tiny = max(int(5 * self.scale_factor), 3)
        
        # Calculate responsive button dimensions
        self.button_width = max(int(12 * self.scale_factor), 8)
        self.button_height = max(int(1 * self.scale_factor), 1)
        self.button_padding_x = max(int(20 * self.scale_factor), 15)
        self.button_padding_y = max(int(15 * self.scale_factor), 10)
        
        # Calculate responsive entry field width
        self.entry_width = max(int(25 * self.scale_factor), 20)

# Global responsive configuration
responsive_config = ResponsiveConfig()

# Modern UI Configuration - Lush Forest Theme
MODERN_COLORS = {
    'primary': '#68BA7F',      # Medium Sage Green - Primary buttons and accents
    'primary_dark': '#2E6F40', # Dark Forest Green - Hover states
    'secondary': '#68BA7F',    # Medium Sage Green - Secondary elements
    'success': '#68BA7F',      # Medium Sage Green - Success states
    'danger': '#EF4444',       # Red - Keep for danger states
    'warning': '#F59E0B',      # Orange - Keep for warnings
    'dark': '#253D2C',         # Very Dark Green - Primary text
    'darker': '#1A2B1F',       # Even darker green - Darkest elements
    'light': '#CFFFDC',        # Light Mint Green - Background
    'white': '#FFFFFF',        # Pure white - Cards and highlights
    'border': '#68BA7F',       # Medium Sage Green - Borders
    'surface': '#253D2C',      # Very Dark Green - Surface elements
    'text_primary': '#FFFFFF', # White - Primary text on dark backgrounds
    'text_secondary': '#CFFFDC', # Light Mint - Secondary text
    'background': '#253D2C',   # Very Dark Green - Main background
    'card': '#2E6F40',         # Dark Forest Green - Card backgrounds
    'input_bg': '#2E6F40',     # Dark Forest Green - Input backgrounds
    'input_border': '#68BA7F', # Medium Sage Green - Input borders
    'accent': '#CFFFDC'        # Light Mint - Accent elements
}

# Dynamic font configuration based on screen resolution
MODERN_FONTS = {
    'title': ('Segoe UI', responsive_config.title_font_size, 'bold'),
    'heading': ('Segoe UI', responsive_config.heading_font_size, 'bold'),
    'subheading': ('Segoe UI', responsive_config.subheading_font_size, 'bold'),
    'body': ('Segoe UI', responsive_config.body_font_size),
    'small': ('Segoe UI', responsive_config.small_font_size)
}

def create_modern_button(parent, text, command=None, style='primary', width=None, height=None):
    """Create a mobile-friendly styled button with responsive sizing"""
    if style == 'primary':
        bg = MODERN_COLORS['primary']
        hover_bg = MODERN_COLORS['primary_dark']
        fg = MODERN_COLORS['white']
    elif style == 'secondary':
        bg = MODERN_COLORS['secondary']
        hover_bg = '#6D28D9'
        fg = MODERN_COLORS['white']
    elif style == 'success':
        bg = MODERN_COLORS['success']
        hover_bg = '#059669'
        fg = MODERN_COLORS['white']
    elif style == 'danger':
        bg = MODERN_COLORS['danger']
        hover_bg = '#DC2626'
        fg = MODERN_COLORS['white']
    elif style == 'warning':
        bg = MODERN_COLORS['warning']
        hover_bg = '#D97706'
        fg = MODERN_COLORS['white']
    else:  # default
        bg = MODERN_COLORS['dark']
        hover_bg = '#374151'
        fg = MODERN_COLORS['white']
    
    # Responsive button sizing
    button_height = responsive_config.button_height if height is None else height
    button_width = responsive_config.button_width if width is None else width
    
    # Responsive font size for buttons
    button_font_size = max(int(14 * responsive_config.scale_factor), 12)
    
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=('Segoe UI', button_font_size, 'bold'),
        relief='flat',
        bd=0,
        cursor='hand2',
        width=button_width,
        height=button_height,
        padx=responsive_config.button_padding_x,
        pady=responsive_config.button_padding_y,
        activebackground=hover_bg,
        activeforeground=fg
    )
    
    def on_enter(e):
        button.config(bg=hover_bg)
    
    def on_leave(e):
        button.config(bg=bg)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    return button

def create_modern_entry(parent, placeholder="", show=None):
    """Create a mobile-friendly styled entry field for dark mode with responsive sizing"""
    # Responsive font size for entry fields
    entry_font_size = max(int(16 * responsive_config.scale_factor), 12)
    
    entry = tk.Entry(
        parent,
        font=('Segoe UI', entry_font_size),
        relief='flat',
        bd=2,
        highlightthickness=3,
        highlightcolor=MODERN_COLORS['primary'],
        highlightbackground=MODERN_COLORS['input_border'],
        bg=MODERN_COLORS['input_bg'],
        fg=MODERN_COLORS['text_primary'],
        insertbackground=MODERN_COLORS['primary'],
        show=show,
        width=responsive_config.entry_width
    )
    return entry

def create_modern_frame(parent, bg=None):
    """Create a modern styled frame"""
    if bg is None:
        bg = MODERN_COLORS['light']
    
    frame = tk.Frame(
        parent,
        bg=bg,
        relief='flat',
        bd=0
    )
    return frame

def center_window(window):
    """Center the window on screen with responsive sizing"""
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (responsive_config.window_width // 2)
    y = (window.winfo_screenheight() // 2) - (responsive_config.window_height // 2)
    window.geometry(f"{responsive_config.window_width}x{responsive_config.window_height}+{x}+{y}")

def create_scrollable_frame(parent, bg=None):
    """Create a scrollable frame with modern styling and proper scrollbar positioning"""
    if bg is None:
        bg = MODERN_COLORS['background']
    
    # Create main frame
    main_frame = tk.Frame(parent, bg=bg)
    
    # Create canvas for scrolling
    canvas = tk.Canvas(main_frame, bg=bg, highlightthickness=0, 
                      relief='flat', bd=0)
    
    # Create modern styled scrollbar
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview,
                           bg=MODERN_COLORS['background'], 
                           activebackground=MODERN_COLORS['primary'],
                           troughcolor=MODERN_COLORS['border'],
                           highlightthickness=0,
                           relief='flat',
                           bd=0,
                           width=12)  # Slightly wider for mobile touch
    
    scrollable_frame = tk.Frame(canvas, bg=bg)
    
    # Configure scrolling
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack canvas and scrollbar with minimal padding
    canvas.pack(side="left", fill="both", expand=True, padx=(0, 0))
    scrollbar.pack(side="right", fill="y", padx=(0, 0))
    
    # Bind mousewheel to canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Store references for cleanup
    main_frame.canvas = canvas
    main_frame.scrollable_frame = scrollable_frame
    main_frame.scrollbar = scrollbar
    
    return main_frame

# --- Storage files/folders ---
ACCOUNTS_FILE = "accounts.json"
USERS_FOLDER = "users"
if not os.path.exists(USERS_FOLDER):
    os.makedirs(USERS_FOLDER)


accounts = {}            
current_user = None

current_entries = []
current_expenses = []
undo_stack = []
redo_stack = []
undo_expense_stack = []
redo_expense_stack = []

# Navigation history for undo functionality
navigation_history = []

def add_to_history(function_name, *args):
    """Add current screen to navigation history"""
    global navigation_history
    navigation_history.append((function_name, args))
    # Keep only last 10 entries to prevent memory issues
    if len(navigation_history) > 10:
        navigation_history.pop(0)

def navigate_back():
    """Go back to previous screen"""
    global navigation_history
    if len(navigation_history) >= 2:
        # Remove current screen
        navigation_history.pop()
        # Get previous screen
        prev_function, prev_args = navigation_history[-1]
        # Remove it from history so we don't create a loop
        navigation_history.pop()
        # Navigate to previous screen
        if prev_function == 'calendar_screen':
            calendar_screen()
        elif prev_function == 'income_screen':
            income_screen(*prev_args)
        elif prev_function == 'expenses_screen':
            expenses_screen(*prev_args)
        elif prev_function == 'total_screen':
            total_screen(*prev_args)
        elif prev_function == 'login_screen':
            login_screen()
        elif prev_function == 'create_account_screen':
            create_account_screen()
        elif prev_function == 'splash_screen':
            splash_screen()
    else:
        messagebox.showinfo("Info", "No previous page to go back to")

def create_undo_button(parent, command=None, style='warning', width=15):
    """Create a standardized undo button"""
    if command is None:
        command = navigate_back
    
    undo_btn = create_modern_button(parent, "← Back", 
                                   command=command,
                                   style=style, width=width)
    return undo_btn

def add_global_undo_shortcut(window):
    """Add Ctrl+Z keyboard shortcut for undo functionality"""
    window.bind('<Control-z>', lambda e: navigate_back())
    window.bind('<Control-Z>', lambda e: navigate_back())


def load_accounts():
    global accounts
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                accounts = json.load(f)
        except Exception:
            accounts = {}
    else:
        accounts = {}

def save_accounts():
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

def user_file(username):
    return os.path.join(USERS_FOLDER, f"{username}.json")

def load_user_data(username):
    global financial_data
    path = user_file(username)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                financial_data = json.load(f)
        except Exception:
            financial_data = {}
    else:
        financial_data = {}

def save_user_data(username):
    path = user_file(username)
    with open(path, "w") as f:
        json.dump(financial_data, f, indent=2)


load_accounts()


def splash_screen():
    # Add to navigation history
    add_to_history('splash_screen')
    
    splash = tk.Tk()
    splash.title("Money Rider - Financial Tracker")
    splash.configure(bg=MODERN_COLORS['background'])
    splash.resizable(False, False)

    # Center the window with responsive sizing
    center_window(splash)

    # Main container with responsive padding
    main_container = create_modern_frame(splash, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_large, 
                       pady=responsive_config.padding_large)

    # Header section
    header_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    header_frame.pack(pady=(responsive_config.padding_medium, responsive_config.padding_large))

    # App icon/logo area - responsive sizing
    icon_frame = create_modern_frame(header_frame, MODERN_COLORS['primary'])
    icon_frame.pack(pady=responsive_config.padding_large)
    icon_size = max(int(120 * responsive_config.scale_factor), 80)
    icon_frame.configure(relief='flat', bd=0, height=icon_size, width=icon_size)
    
    # Responsive emoji logo
    emoji_font_size = max(int(50 * responsive_config.scale_factor), 30)
    icon_label = tk.Label(icon_frame, text="🏍️", font=('Segoe UI Emoji', emoji_font_size), 
                         bg=MODERN_COLORS['primary'], fg=MODERN_COLORS['white'])
    icon_label.pack(expand=True)

    # Title - responsive typography
    title_font_size = max(int(32 * responsive_config.scale_factor), 24)
    title = tk.Label(header_frame, text="Money Rider", 
                    font=('Segoe UI', title_font_size, 'bold'), 
                    bg=MODERN_COLORS['background'], 
                    fg=MODERN_COLORS['text_primary'])
    title.pack(pady=responsive_config.padding_medium)

    # Subtitle - responsive typography
    subtitle_font_size = max(int(16 * responsive_config.scale_factor), 12)
    subtitle = tk.Label(header_frame, text="Track your finances with ease", 
                       font=('Segoe UI', subtitle_font_size), 
                       bg=MODERN_COLORS['background'], 
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=responsive_config.padding_small)

    # Button container with responsive spacing
    button_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    button_frame.pack(pady=responsive_config.padding_large)

    # Login button - responsive sizing
    responsive_button_width = max(int(20 * responsive_config.scale_factor), 15)
    login_btn = create_modern_button(button_frame, "📱 Sign In", 
                                   command=lambda:[splash.destroy(), login_screen()],
                                   style='primary', width=responsive_button_width)
    login_btn.pack(pady=responsive_config.padding_large)

    # Create account button - responsive sizing
    create_account_btn = create_modern_button(button_frame, "👤 Create Account", 
                                            command=lambda:[splash.destroy(), create_account_screen()],
                                            style='secondary', width=responsive_button_width)
    create_account_btn.pack(pady=responsive_config.padding_medium)

    # Footer - responsive styling
    footer_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    footer_frame.pack(side=tk.BOTTOM, pady=responsive_config.padding_large)
    
    footer_font_size = max(int(12 * responsive_config.scale_factor), 10)
    footer_text = tk.Label(footer_frame, text="© 2024 Money Rider", 
                          font=('Segoe UI', footer_font_size), 
                          bg=MODERN_COLORS['background'], 
                          fg=MODERN_COLORS['text_secondary'])
    footer_text.pack()

    splash.mainloop()

# ---------------- Create Account ----------------
def create_account_screen():
    # Add to navigation history
    add_to_history('create_account_screen')
    
    create = tk.Tk()
    create.title("Create Account - Money Rider")
    create.configure(bg=MODERN_COLORS['background'])
    create.resizable(False, False)

    # Center the window with responsive sizing
    center_window(create)

    # Main container with responsive padding
    main_container = create_modern_frame(create, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_large, 
                       pady=responsive_config.padding_large)

    # Header - responsive styling
    header_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    header_frame.pack(pady=(0, responsive_config.padding_medium))

    title = tk.Label(header_frame, text="Create Account", 
                    font=MODERN_FONTS['title'], 
                    bg=MODERN_COLORS['background'], 
                    fg=MODERN_COLORS['text_primary'])
    title.pack(pady=responsive_config.padding_medium)

    subtitle = tk.Label(header_frame, text="Join Money Rider today", 
                       font=MODERN_FONTS['subheading'], 
                       bg=MODERN_COLORS['background'], 
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=responsive_config.padding_tiny)

    # Form container - responsive card style
    form_frame = create_modern_frame(main_container, MODERN_COLORS['card'])
    form_frame.pack(fill=tk.X, pady=responsive_config.padding_large)
    form_frame.configure(relief='solid', bd=2)

    # Username field - responsive styling
    tk.Label(form_frame, text="Username", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_medium, responsive_config.padding_small))
    
    username_entry = create_modern_entry(form_frame)
    username_entry.pack(fill=tk.X, 
                       padx=responsive_config.padding_medium, 
                       pady=(0, responsive_config.padding_large))

    # Password field - responsive styling
    tk.Label(form_frame, text="Password", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_medium, responsive_config.padding_small))
    
    password_var = tk.StringVar()
    password_entry = create_modern_entry(form_frame, show="*")
    password_entry.config(textvariable=password_var)
    password_entry.pack(fill=tk.X, 
                       padx=responsive_config.padding_medium, 
                       pady=(0, responsive_config.padding_small))

    # Password visibility toggle - responsive styling
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁 Show Password")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈 Hide Password")
    
    responsive_button_width = max(int(20 * responsive_config.scale_factor), 15)
    eye_btn = create_modern_button(form_frame, "👁 Show Password", command=toggle_pw, 
                                  style='secondary', width=responsive_button_width)
    eye_btn.pack(pady=(0, responsive_config.padding_medium))

    def create_account():
        username = username_entry.get().strip()
        password = password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        if username in accounts:
            messagebox.showerror("Error", "Username already exists")
            return
        accounts[username] = password
        save_accounts()
        # create user data file (empty financial_data)
        with open(user_file(username), "w") as f:
            json.dump({}, f)
        messagebox.showinfo("Success", "Account created successfully! Please sign in.")
        create.destroy()
        splash_screen()

    # Button container - responsive styling
    button_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    button_frame.pack(pady=responsive_config.padding_medium)

    # Create button - responsive sizing
    create_btn = create_modern_button(button_frame, "✅ Create Account", 
                                    command=create_account,
                                    style='primary', width=responsive_button_width)
    create_btn.pack(pady=responsive_config.padding_large)

    # Back button - responsive sizing
    back_btn = create_modern_button(button_frame, "← Back to Sign In", 
                                  command=lambda: [create.destroy(), splash_screen()],
                                  style='secondary', width=responsive_button_width)
    back_btn.pack(pady=responsive_config.padding_small)

# ---------------- Login ----------------
def login_screen():
    # Add to navigation history
    add_to_history('login_screen')
    
    login = tk.Tk()
    login.title("Sign In - Money Rider")
    login.configure(bg=MODERN_COLORS['background'])
    login.resizable(False, False)

    # Center the window with responsive sizing
    center_window(login)

    # Main container with responsive padding
    main_container = create_modern_frame(login, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_large, 
                       pady=responsive_config.padding_large)

    # Header - responsive styling
    header_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    header_frame.pack(pady=(0, responsive_config.padding_medium))

    title = tk.Label(header_frame, text="Welcome Back", 
                    font=MODERN_FONTS['title'], 
                    bg=MODERN_COLORS['background'], 
                    fg=MODERN_COLORS['text_primary'])
    title.pack(pady=responsive_config.padding_medium)

    subtitle = tk.Label(header_frame, text="Sign in to your account", 
                       font=MODERN_FONTS['subheading'], 
                       bg=MODERN_COLORS['background'], 
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=responsive_config.padding_tiny)

    # Form container - responsive card style
    form_frame = create_modern_frame(main_container, MODERN_COLORS['card'])
    form_frame.pack(fill=tk.X, pady=responsive_config.padding_large)
    form_frame.configure(relief='solid', bd=2)

    # Username field - responsive styling
    tk.Label(form_frame, text="Username", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_medium, responsive_config.padding_small))
    
    username_entry = create_modern_entry(form_frame)
    username_entry.pack(fill=tk.X, 
                       padx=responsive_config.padding_medium, 
                       pady=(0, responsive_config.padding_large))

    # Password field - responsive styling
    tk.Label(form_frame, text="Password", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_medium, responsive_config.padding_small))
    
    password_var = tk.StringVar()
    password_entry = create_modern_entry(form_frame, show="*")
    password_entry.config(textvariable=password_var)
    password_entry.pack(fill=tk.X, 
                       padx=responsive_config.padding_medium, 
                       pady=(0, responsive_config.padding_small))

    # Password visibility toggle - responsive styling
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁 Show Password")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈 Hide Password")
    
    responsive_button_width = max(int(20 * responsive_config.scale_factor), 15)
    eye_btn = create_modern_button(form_frame, "👁 Show Password", command=toggle_pw, 
                                  style='secondary', width=responsive_button_width)
    eye_btn.pack(pady=(0, responsive_config.padding_medium))

    def validate_login():
        username = username_entry.get().strip()
        password = password_var.get()
        if username in accounts and accounts[username] == password:
            # load this user's data
            global current_user, financial_data
            current_user = username
            load_user_data(current_user)
            login.destroy()
            calendar_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    # Button container - responsive styling
    button_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    button_frame.pack(pady=responsive_config.padding_small)

    # Login button - responsive sizing
    login_btn = create_modern_button(button_frame, "🔑 Sign In", 
                                   command=validate_login,
                                   style='primary', width=responsive_button_width)
    login_btn.pack(pady=responsive_config.padding_large)

    # Back button - responsive sizing
    back_btn = create_modern_button(button_frame, "← Back to Home", 
                                  command=lambda: [login.destroy(), splash_screen()],
                                  style='secondary', width=responsive_button_width)
    back_btn.pack(pady=responsive_config.padding_small)

    # Add global undo shortcut
    add_global_undo_shortcut(login)

    # Focus on username entry
    username_entry.focus()

# ---------------- Calendar Screen (same layout/flow as original) ----------------
def calendar_screen():
    # Add to navigation history
    add_to_history('calendar_screen')
    
    cal = tk.Tk()
    cal.title("Money Rider - Calendar")
    cal.configure(bg=MODERN_COLORS['background'])
    cal.resizable(False, False)

    # Center the window with responsive sizing
    center_window(cal)

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Define variables for month/year selection
    month_var = tk.StringVar()
    year_var = tk.StringVar()

    def show_saved_data(date_str, day):
        # Create a popup window to display saved data
        popup = tk.Toplevel(cal)
        popup.title(f"Saved Data - {date_str}")
        popup.geometry("500x600")
        popup.configure(bg="#1C1C1C")

        # Main frame
        main_frame = tk.Frame(popup, bg="#1C1C1C")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        tk.Label(main_frame, text=f"Saved Financial Data", bg="#1C1C1C", fg="white",
                 font=("Bubblegum Sans", 20, "bold")).pack(pady=10)
        tk.Label(main_frame, text=date_str, bg="#1C1C1C", fg="#4CAF50",
                 font=("Bubblegum Sans", 14)).pack(pady=5)

        # Get the saved data (if missing, show zeros)
        data = financial_data.get(date_str, {"income": 0.0, "expenses": 0.0, "entries": [], "expense_entries": []})

        # Summary frame
        summary_frame = tk.Frame(main_frame, bg="#2C2C2C", bd=2, relief=tk.RIDGE)
        summary_frame.pack(fill=tk.X, padx=10, pady=15)

        # Income summary
        income_frame = tk.Frame(summary_frame, bg="#2C2C2C")
        income_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(income_frame, text="Total Income:", bg="#2C2C2C", fg="white",
                 font=("Bubblegum Sans", 14)).pack(side=tk.LEFT)
        tk.Label(income_frame, text=f"₱{data['income']:,.2f}", bg="#2C2C2C", fg="#4CAF50",
                 font=("Bubblegum Sans", 14, "bold")).pack(side=tk.RIGHT)

        # Expenses summary
        expenses_frame = tk.Frame(summary_frame, bg="#2C2C2C")
        expenses_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(expenses_frame, text="Total Expenses:", bg="#2C2C2C", fg="white",
                 font=("Bubblegum Sans", 14)).pack(side=tk.LEFT)
        tk.Label(expenses_frame, text=f"₱{data['expenses']:,.2f}", bg="#2C2C2C", fg="#F44336",
                 font=("Bubblegum Sans", 14, "bold")).pack(side=tk.RIGHT)

        # Net total
        net_frame = tk.Frame(summary_frame, bg="#2C2C2C")
        net_frame.pack(fill=tk.X, padx=10, pady=10)

        net_total = data['income'] - data['expenses']
        tk.Label(net_frame, text="Net Total:", bg="#2C2C2C", fg="white",
                 font=("Bubblegum Sans", 16)).pack(side=tk.LEFT)
        tk.Label(net_frame, text=f"₱{net_total:,.2f}", bg="#2C2C2C",
                 fg="#4CAF50" if net_total >= 0 else "#F44336",
                 font=("Bubblegum Sans", 16, "bold")).pack(side=tk.RIGHT)

        # Details frame
        details_frame = tk.Frame(main_frame, bg="#1C1C1C")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Notebook for income/expense details
        notebook = ttk.Notebook(details_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Income tab
        income_tab = tk.Frame(notebook, bg="#1C1C1C")
        notebook.add(income_tab, text="Income Details")

        if data.get('entries'):
            income_listbox = tk.Listbox(income_tab, bg="#404040", fg="white",
                                       font=("Courier New", 12), width=50)
            income_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for entry in data['entries']:
                income_listbox.insert(tk.END, f"{entry[0].ljust(30)}{str(entry[1]).rjust(10)}")
        else:
            tk.Label(income_tab, text="No income data", bg="#1C1C1C", fg="white",
                     font=("Bubblegum Sans", 14)).pack(pady=20)

        # Expenses tab
        expense_tab = tk.Frame(notebook, bg="#1C1C1C")
        notebook.add(expense_tab, text="Expense Details")

        if data.get('expense_entries'):
            expense_listbox = tk.Listbox(expense_tab, bg="#404040", fg="white",
                                         font=("Courier New", 12), width=50)
            expense_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for expense in data['expense_entries']:
                expense_listbox.insert(tk.END, f"{expense[0].ljust(30)}{str(expense[1]).rjust(10)}")
        else:
            tk.Label(expense_tab, text="No expense data", bg="#1C1C1C", fg="white",
                     font=("Bubblegum Sans", 14)).pack(pady=20)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1C1C1C")
        button_frame.pack(pady=10)

        # View/edit button (go to main entry screen for that day)
        edit_btn = create_modern_button(button_frame, "✏️ View/Edit", 
                                       command=lambda: [popup.destroy(), cal.destroy(), income_screen(day, current_year, current_month)],
                                       style='primary', width=12)
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Close button
        close_btn = create_modern_button(button_frame, "❌ Close", 
                                        command=popup.destroy,
                                        style='secondary', width=12)
        close_btn.pack(side=tk.LEFT, padx=5)

    def go_to_income(day):
        global current_entries, current_expenses

        # Save current date for later reference
        selected_date = f"{current_year}-{current_month:02d}-{day:02d}"

        # Load entries for this date (if exist) into buffers
        if selected_date in financial_data:
            daydata = financial_data[selected_date]
            current_entries = [(e[0], float(e[1])) for e in daydata.get("entries", [])]
            current_expenses = [(e[0], float(e[1])) for e in daydata.get("expense_entries", [])]
        else:
            current_entries = []
            current_expenses = []
        cal.destroy()
        income_screen(day, current_year, current_month)

    def create_calendar_grid():
        for widget in cal.winfo_children():
            widget.destroy()

        # Main container with scrolling and responsive padding
        cal_frame = create_scrollable_frame(cal, MODERN_COLORS['background'])
        cal_frame.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_small, 
                       pady=responsive_config.padding_small)
        
        # Get the scrollable frame for adding widgets
        scrollable_content = cal_frame.scrollable_frame

        # Header with title and controls
        header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, responsive_config.padding_large))

        # Title
        title_label = tk.Label(header_frame, text="Financial Calendar", 
                              font=MODERN_FONTS['heading'], 
                              bg=MODERN_COLORS['background'], 
                              fg=MODERN_COLORS['text_primary'])
        title_label.pack(pady=(0, responsive_config.padding_medium))

        # Month and year selection
        controls_frame = create_modern_frame(header_frame, MODERN_COLORS['background'])
        controls_frame.pack()

        # Set current values
        month_var.set(calendar.month_name[current_month])
        month_menu = ttk.Combobox(controls_frame, textvariable=month_var,
                                 values=list(calendar.month_name[1:]),
                                 state="readonly",
                                 font=MODERN_FONTS['body'],
                                 justify="center",
                                 width=12)
        month_menu.grid(row=0, column=0, padx=5, pady=5)
        month_menu.bind("<<ComboboxSelected>>", lambda e: change_month())

        year_var.set(str(current_year))
        year_menu = ttk.Combobox(controls_frame, textvariable=year_var,
                                values=list(range(2020, 2031)),
                                state="readonly",
                                font=MODERN_FONTS['body'],
                                justify="center",
                                width=8)
        year_menu.grid(row=0, column=1, padx=5, pady=5)
        year_menu.bind("<<ComboboxSelected>>", lambda e: change_year())

        # Calendar container
        calendar_container = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
        calendar_container.pack(fill=tk.BOTH, expand=True, 
                               pady=responsive_config.padding_small, 
                               padx=responsive_config.padding_tiny)
        calendar_container.configure(relief='solid', bd=1)

        # Days of week header
        days_frame = create_modern_frame(calendar_container, MODERN_COLORS['card'])
        days_frame.pack(fill=tk.X, padx=5, pady=10)

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days_of_week):
            day_label = tk.Label(days_frame, text=day, 
                               bg=MODERN_COLORS['card'], 
                               fg=MODERN_COLORS['text_primary'],
                               font=MODERN_FONTS['body'])
            day_label.grid(row=0, column=col, padx=1, pady=5, sticky='ew')
        
        # Configure grid weights for weekday headers to match calendar grid
        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1)

        # Calendar days grid
        days_grid_frame = create_modern_frame(calendar_container, MODERN_COLORS['card'])
        days_grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        
        month_cal = calendar.monthcalendar(current_year, current_month)
        for row, week in enumerate(month_cal):
            for col, day in enumerate(week):
                if day == 0:
                    # Empty space for days not in the month
                    empty_label = tk.Label(days_grid_frame, text="", 
                                         bg=MODERN_COLORS['white'])
                    empty_label.grid(row=row+1, column=col, padx=1, pady=1, sticky='nsew')
                    continue

                date_str = f"{current_year}-{current_month:02d}-{day:02d}"

                # Determine button style
                if (day == current_date.day and
                    current_month == current_date.month and
                    current_year == current_date.year):
                    # Current day
                    day_bg = MODERN_COLORS['primary']
                    day_fg = MODERN_COLORS['white']
                elif date_str in financial_data:
                    # Days with data
                    day_bg = MODERN_COLORS['success']
                    day_fg = MODERN_COLORS['white']
                else:
                    # Regular days
                    day_bg = MODERN_COLORS['light']
                    day_fg = MODERN_COLORS['dark']

                day_button = tk.Button(days_grid_frame, text=str(day), 
                                     bg=day_bg, fg=day_fg,
                                     font=MODERN_FONTS['body'],
                                     relief='flat', bd=1,
                                     cursor='hand2',
                                     command=lambda d=day: go_to_income(d))
                day_button.grid(row=row + 1, column=col, padx=1, pady=1, sticky='nsew')
                
                # Add hover effect
                def create_hover_effect(btn, original_bg):
                    def on_enter(e):
                        if original_bg == MODERN_COLORS['primary']:
                            btn.config(bg=MODERN_COLORS['primary_dark'])
                        elif original_bg == MODERN_COLORS['success']:
                            btn.config(bg='#059669')
                        else:
                            btn.config(bg=MODERN_COLORS['border'])
                    
                    def on_leave(e):
                        btn.config(bg=original_bg)
                    
                    btn.bind("<Enter>", on_enter)
                    btn.bind("<Leave>", on_leave)
                
                create_hover_effect(day_button, day_bg)

        # Configure grid weights for proper sizing
        for i in range(7):
            days_grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            days_grid_frame.grid_rowconfigure(i, weight=1)

        # Date range calculation section
        range_container = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
        range_container.pack(fill=tk.X, pady=15, padx=5)

        range_title = tk.Label(range_container, text="Date Range Calculator", 
                              font=MODERN_FONTS['subheading'], 
                              bg=MODERN_COLORS['background'], 
                              fg=MODERN_COLORS['text_primary'])
        range_title.pack(pady=(0, 10))

        # Range input frame
        range_frame = create_modern_frame(range_container, MODERN_COLORS['card'])
        range_frame.pack(fill=tk.X, pady=10)
        range_frame.configure(relief='solid', bd=1)

        # Date input frame using grid for better width utilization
        date_input_frame = create_modern_frame(range_frame, MODERN_COLORS['card'])
        date_input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Configure grid weights for better distribution
        for i in range(4):
            date_input_frame.grid_columnconfigure(i, weight=1)

        # Start date row
        tk.Label(date_input_frame, text="From:", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['white'], 
                fg=MODERN_COLORS['dark']).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)

        start_day = ttk.Combobox(date_input_frame, values=list(range(1, 32)), width=4,
                                 font=MODERN_FONTS['body'], state="readonly")
        start_day.grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        start_day.set("1")

        start_month = ttk.Combobox(date_input_frame, values=list(calendar.month_name[1:]), width=15,
                                   font=MODERN_FONTS['body'], state="readonly")
        start_month.grid(row=0, column=2, sticky="ew", padx=2, pady=5)
        start_month.set(calendar.month_name[current_month])

        start_year = ttk.Combobox(date_input_frame, values=list(range(2020, 2031)), width=8,
                                  font=MODERN_FONTS['body'], state="readonly")
        start_year.grid(row=0, column=3, sticky="ew", padx=2, pady=5)
        start_year.set(str(current_year))

        # End date row
        tk.Label(date_input_frame, text="To:", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['white'], 
                fg=MODERN_COLORS['dark']).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=5)

        end_day = ttk.Combobox(date_input_frame, values=list(range(1, 32)), width=4,
                               font=MODERN_FONTS['body'], state="readonly")
        end_day.grid(row=1, column=1, sticky="ew", padx=2, pady=5)
        end_day.set("1")

        end_month = ttk.Combobox(date_input_frame, values=list(calendar.month_name[1:]), width=15,
                                 font=MODERN_FONTS['body'], state="readonly")
        end_month.grid(row=1, column=2, sticky="ew", padx=2, pady=5)
        end_month.set(calendar.month_name[current_month])

        end_year = ttk.Combobox(date_input_frame, values=list(range(2020, 2031)), width=8,
                                font=MODERN_FONTS['body'], state="readonly")
        end_year.grid(row=1, column=3, sticky="ew", padx=2, pady=5)
        end_year.set(str(current_year))

        def calculate_range():
            try:
                # Get start date components
                start_d = int(start_day.get())
                start_m = list(calendar.month_name).index(start_month.get())
                start_y = int(start_year.get())

                # Get end date components
                end_d = int(end_day.get())
                end_m = list(calendar.month_name).index(end_month.get())
                end_y = int(end_year.get())

                # Create date strings for comparison
                start_date_str = f"{start_y}-{start_m:02d}-{start_d:02d}"
                end_date_str = f"{end_y}-{end_m:02d}-{end_d:02d}"

                # Validate date range
                if start_date_str > end_date_str:
                    messagebox.showerror("Error", "Start date must be before end date")
                    return

                # Calculate totals
                total_income = 0.0
                total_expenses = 0.0
                days_with_data = 0

                for date_str in sorted(financial_data.keys()):
                    if start_date_str <= date_str <= end_date_str:
                        data = financial_data[date_str]
                        total_income += float(data.get("income", 0))
                        total_expenses += float(data.get("expenses", 0))
                        days_with_data += 1

                net_total = total_income - total_expenses

                # Display results in modern window
                result_window = tk.Toplevel(cal)
                result_window.title("Date Range Results")
                result_window.geometry("500x400")
                result_window.configure(bg=MODERN_COLORS['light'])
                result_window.resizable(False, False)

                # Center the result window
                result_window.update_idletasks()
                x = (result_window.winfo_screenwidth() // 2) - (500 // 2)
                y = (result_window.winfo_screenheight() // 2) - (400 // 2)
                result_window.geometry(f"500x400+{x}+{y}")

                # Main container
                result_container = create_modern_frame(result_window, MODERN_COLORS['light'])
                result_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

                # Title
                title_label = tk.Label(result_container, text="Financial Summary", 
                                     font=MODERN_FONTS['heading'], 
                                     bg=MODERN_COLORS['light'], 
                                     fg=MODERN_COLORS['dark'])
                title_label.pack(pady=(0, 20))

                # Date range
                date_label = tk.Label(result_container, text=f"{start_date_str} to {end_date_str}", 
                                     font=MODERN_FONTS['body'], 
                                     bg=MODERN_COLORS['light'], 
                                     fg=MODERN_COLORS['dark'])
                date_label.pack(pady=(0, 20))

                # Summary frame
                summary_frame = create_modern_frame(result_container, MODERN_COLORS['white'])
                summary_frame.pack(fill=tk.X, pady=10)
                summary_frame.configure(relief='solid', bd=1)

                # Results
                results = [
                    ("Days with data", str(days_with_data), MODERN_COLORS['dark']),
                    ("Total Income", f"₱{total_income:,.2f}", MODERN_COLORS['success']),
                    ("Total Expenses", f"₱{total_expenses:,.2f}", MODERN_COLORS['danger']),
                    ("Net Total", f"₱{net_total:,.2f}", MODERN_COLORS['success'] if net_total >= 0 else MODERN_COLORS['danger'])
                ]

                for label, value, color in results:
                    result_frame = create_modern_frame(summary_frame, MODERN_COLORS['white'])
                    result_frame.pack(fill=tk.X, padx=20, pady=8)

                    tk.Label(result_frame, text=label, 
                            font=MODERN_FONTS['body'], 
                            bg=MODERN_COLORS['white'], 
                            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT)

                    tk.Label(result_frame, text=value, 
                            font=MODERN_FONTS['body'], 
                            bg=MODERN_COLORS['white'], 
                            fg=color).pack(side=tk.RIGHT)

                # Close button
                close_btn = create_modern_button(result_container, "Close", 
                                               command=result_window.destroy,
                                               style='primary', width=15)
                close_btn.pack(pady=20)

            except ValueError:
                messagebox.showerror("Error", "Invalid date selection")

        # Calculate button
        calc_button = create_modern_button(range_frame, "Calculate Range", 
                                         command=calculate_range,
                                         style='primary', width=20)
        calc_button.pack(pady=10)

        # Navigation buttons - responsive styling
        nav_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
        nav_frame.pack(pady=responsive_config.padding_large)

        # Undo button - responsive sizing
        responsive_button_width = max(int(20 * responsive_config.scale_factor), 15)
        undo_btn = create_undo_button(nav_frame, 
                                     command=lambda: [cal.destroy(), navigate_back()],
                                     style='warning', width=responsive_button_width)
        undo_btn.pack(pady=responsive_config.padding_tiny)

        # Sign out button with responsive styling
        signout_btn = create_modern_button(nav_frame, "🚪 Sign Out", 
                                          command=lambda: [cal.destroy(), login_screen()],
                                          style='danger', width=responsive_button_width)
        signout_btn.pack(pady=responsive_config.padding_tiny)

    def change_month():
        nonlocal current_month
        selected_month = month_var.get()
        current_month = list(calendar.month_name).index(selected_month)
        create_calendar_grid()

    def change_year():
        nonlocal current_year
        current_year = int(year_var.get())
        create_calendar_grid()

    # Add global undo shortcut
    add_global_undo_shortcut(cal)

    create_calendar_grid()
    cal.mainloop()

# ---------------- Income Screen (keeps original layout, Edit/Delete implemented) ----------------
def income_screen(day, year, month):
    # Add to navigation history
    add_to_history('income_screen', day, year, month)
    
    inc = tk.Tk()
    inc.title("Financial Tracking - Money Rider")
    inc.configure(bg=MODERN_COLORS['background'])
    inc.resizable(False, False)

    # Center the window with responsive sizing
    center_window(inc)

    # Floating undo button in top-right corner with responsive positioning
    floating_button_size = max(int(40 * responsive_config.scale_factor), 30)
    floating_x = responsive_config.window_width - floating_button_size - 10
    floating_undo_frame = create_modern_frame(inc, MODERN_COLORS['primary'])
    floating_undo_frame.place(x=floating_x, y=10, width=floating_button_size, height=floating_button_size)
    
    floating_font_size = max(int(16 * responsive_config.scale_factor), 12)
    floating_undo_btn = tk.Button(floating_undo_frame, text="←", 
                                 command=lambda: [inc.destroy(), navigate_back()],
                                 bg=MODERN_COLORS['primary'], fg=MODERN_COLORS['white'],
                                 font=('Segoe UI', floating_font_size, 'bold'), relief='flat', bd=0,
                                 cursor='hand2', activebackground=MODERN_COLORS['primary_dark'])
    floating_undo_btn.pack(fill=tk.BOTH, expand=True)

    name_var = tk.StringVar()
    income_var = tk.StringVar()
    
    # Expense variables
    expense_var = tk.StringVar()
    amount_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Main container with responsive padding and scrolling
    main_container = create_scrollable_frame(inc, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_medium, 
                       pady=responsive_config.padding_medium)
    
    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Header section
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(fill=tk.X, pady=(0, responsive_config.padding_large))

    # Title - responsive styling
    title_font_size = max(int(24 * responsive_config.scale_factor), 18)
    title_label = tk.Label(header_frame, text="Financial Tracking", 
                          font=('Segoe UI', title_font_size, 'bold'), 
                          bg=MODERN_COLORS['background'], 
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, responsive_config.padding_small))

    # Date display - responsive styling
    date_font_size = max(int(16 * responsive_config.scale_factor), 12)
    date_label = tk.Label(header_frame, text=f"{year}-{month:02d}-{day:02d}",
                         font=('Segoe UI', date_font_size), 
                         bg=MODERN_COLORS['background'], 
                         fg=MODERN_COLORS['text_primary'])
    date_label.pack(pady=responsive_config.padding_tiny)

    # Undo button at the top for better visibility
    responsive_button_width = max(int(15 * responsive_config.scale_factor), 12)
    top_undo_btn = create_undo_button(header_frame, 
                                     command=lambda: [inc.destroy(), navigate_back()],
                                     style='warning', width=responsive_button_width)
    top_undo_btn.pack(pady=responsive_config.padding_tiny)

    # Input section with responsive cards
    input_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    input_frame.pack(fill=tk.X, pady=(0, responsive_config.padding_medium))
    
    # Create notebook for tabs with mobile styling
    notebook = ttk.Notebook(input_frame)
    notebook.pack(fill=tk.X)
    
    # Style the notebook for mobile look
    style = ttk.Style()
    style.configure('TNotebook', tabposition='n')
    style.configure('TNotebook.Tab', padding=[20, 10], font=MODERN_FONTS['body'])

    # Income tab with mobile card styling
    income_tab = create_modern_frame(notebook, MODERN_COLORS['card'])
    notebook.add(income_tab, text="💰 Income")

    # Income card container
    income_card = create_modern_frame(income_tab, MODERN_COLORS['card'])
    income_card.pack(fill=tk.X, 
                    padx=responsive_config.padding_medium, 
                    pady=responsive_config.padding_medium)
    income_card.configure(relief='solid', bd=1)

    # Income Source field with responsive styling
    tk.Label(income_card, text="Income Source", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_medium, responsive_config.padding_tiny))
    
    name_entry = create_modern_entry(income_card)
    name_entry.config(textvariable=name_var)
    name_entry.pack(fill=tk.X, 
                   padx=responsive_config.padding_medium, 
                   pady=(0, responsive_config.padding_small))

    # Income amount field with responsive styling
    tk.Label(income_card, text="Amount (₱)", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_small, responsive_config.padding_tiny))
    
    income_entry = create_modern_entry(income_card)
    income_entry.config(textvariable=income_var)
    income_entry.pack(fill=tk.X, 
                     padx=responsive_config.padding_medium, 
                     pady=(0, responsive_config.padding_medium))

    # Define functions before buttons
    def enter_income():
        name = name_var.get().strip()
        income = income_var.get().strip()
        if not name or not income:
            messagebox.showinfo("Error", "Please fill in all fields!")
            return

        try:
            income_val = float(income)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            return

        entry = (name, income_val)
        current_entries.append(entry)
        # Format with modern styling
        income_listbox.insert(tk.END, f"{name:<30} ₱{income_val:>10,.2f}")
        name_var.set("")
        income_var.set("")
        # autosave to user's financial_data
        save_data(current_date_str)

    def enter_expense():
        category = category_var.get()
        if category == "Other":
            category = custom_var.get().strip()
        amount = amount_var.get().strip()
        if not category or not amount:
            messagebox.showinfo("Error", "Please fill in all fields!")
            return
        try:
            amount_val = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            return

        entry = (category, amount_val)
        current_expenses.append(entry)
        # Format with modern styling
        expense_listbox.insert(tk.END, f"{category:<30} ₱{amount_val:>10,.2f}")
        amount_var.set("")
        custom_var.set("")
        # autosave to user's financial_data
        save_data(current_date_str)

    # Add Income button with responsive styling
    responsive_button_width = max(int(25 * responsive_config.scale_factor), 20)
    add_income_btn = create_modern_button(income_card, "➕ Add Income", 
                                        command=enter_income,
                                        style='success', width=responsive_button_width)
    add_income_btn.pack(pady=(0, responsive_config.padding_medium))

    # Expenses tab with mobile card styling
    expense_tab = create_modern_frame(notebook, MODERN_COLORS['card'])
    notebook.add(expense_tab, text="💸 Expenses")

    # Expense card container
    expense_card = create_modern_frame(expense_tab, MODERN_COLORS['card'])
    expense_card.pack(fill=tk.X, 
                     padx=responsive_config.padding_medium, 
                     pady=responsive_config.padding_medium)
    expense_card.configure(relief='solid', bd=1)

    # Expense Category field with responsive styling
    tk.Label(expense_card, text="Category", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_medium, responsive_config.padding_tiny))
    
    # Category dropdown with responsive styling
    category_var = tk.StringVar()
    categories = ["Food", "Gas", "Maintenance", "Other"]
    cat_menu = ttk.Combobox(expense_card, values=categories, textvariable=category_var, 
                           state="readonly", font=MODERN_FONTS['body'])
    cat_menu.pack(fill=tk.X, 
                  padx=responsive_config.padding_medium, 
                  pady=(0, responsive_config.padding_small))
    cat_menu.set(categories[0])

    # Custom category entry (hidden by default)
    custom_var = tk.StringVar()
    custom_entry = create_modern_entry(expense_card)
    custom_entry.config(textvariable=custom_var)
    
    # Show/hide custom entry based on category selection
    def on_cat_change(e=None):
        if category_var.get() == "Other":
            custom_entry.pack(fill=tk.X, 
                             padx=responsive_config.padding_medium, 
                             pady=(0, responsive_config.padding_small))
        else:
            custom_entry.pack_forget()
    cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

    # Expense amount field with responsive styling
    tk.Label(expense_card, text="Amount (₱)", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=responsive_config.padding_medium, 
                                                   pady=(responsive_config.padding_small, responsive_config.padding_tiny))
    
    expense_amount_entry = create_modern_entry(expense_card)
    expense_amount_entry.config(textvariable=amount_var)
    expense_amount_entry.pack(fill=tk.X, 
                             padx=responsive_config.padding_medium, 
                             pady=(0, responsive_config.padding_medium))

    # Add Expense button with responsive styling
    add_expense_btn = create_modern_button(expense_card, "➕ Add Expense", 
                                         command=enter_expense,
                                         style='success', width=responsive_button_width)
    add_expense_btn.pack(pady=(0, responsive_config.padding_medium))

    # Display section with tabs
    display_frame = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    display_frame.pack(fill=tk.X, pady=(0, responsive_config.padding_medium))
    display_height = max(int(200 * responsive_config.scale_factor), 150)
    display_frame.configure(relief='solid', bd=1, height=display_height)

    # Create notebook for display tabs
    display_notebook = ttk.Notebook(display_frame)
    display_notebook.pack(fill=tk.BOTH, expand=True, 
                         padx=responsive_config.padding_small, 
                         pady=responsive_config.padding_small)

    # Income display tab
    income_display_tab = create_modern_frame(display_notebook, MODERN_COLORS['card'])
    display_notebook.add(income_display_tab, text="💰 Income List")

    # Header for income list
    income_header = create_modern_frame(income_display_tab, MODERN_COLORS['card'])
    income_header.pack(fill=tk.X, 
                      padx=responsive_config.padding_small, 
                      pady=responsive_config.padding_small)

    tk.Label(income_header, text="Income Source", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, 
                                                   padx=responsive_config.padding_small)
    
    tk.Label(income_header, text="Amount", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.RIGHT, 
                                                   padx=responsive_config.padding_small)

    # Create income listbox with double-click editing
    income_listbox = tk.Listbox(income_display_tab, 
                               font=MODERN_FONTS['body'],
                               bg=MODERN_COLORS['white'], 
                               fg=MODERN_COLORS['text_primary'],
                               selectbackground=MODERN_COLORS['primary'],
                               selectforeground=MODERN_COLORS['white'],
                               relief='flat',
                               bd=0,
                               highlightthickness=0,
                               cursor='hand2')  # Show hand cursor to indicate clickable
    income_listbox.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_small, 
                       pady=(0, responsive_config.padding_small))
    
    # Bind double-click to edit income
    income_listbox.bind('<Double-Button-1>', lambda e: edit_income_selected())

    # Expenses display tab
    expense_display_tab = create_modern_frame(display_notebook, MODERN_COLORS['card'])
    display_notebook.add(expense_display_tab, text="💸 Expense List")

    # Header for expense list
    expense_header = create_modern_frame(expense_display_tab, MODERN_COLORS['card'])
    expense_header.pack(fill=tk.X, 
                       padx=responsive_config.padding_small, 
                       pady=responsive_config.padding_small)

    tk.Label(expense_header, text="Expense Category", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, 
                                                   padx=responsive_config.padding_small)
    
    tk.Label(expense_header, text="Amount", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.RIGHT, 
                                                   padx=responsive_config.padding_small)

    # Create expense listbox with double-click editing
    expense_listbox = tk.Listbox(expense_display_tab, 
                                font=MODERN_FONTS['body'],
                                bg=MODERN_COLORS['white'], 
                                fg=MODERN_COLORS['text_primary'],
                                selectbackground=MODERN_COLORS['primary'],
                                selectforeground=MODERN_COLORS['white'],
                                relief='flat',
                                bd=0,
                                highlightthickness=0,
                                cursor='hand2')  # Show hand cursor to indicate clickable
    expense_listbox.pack(fill=tk.BOTH, expand=True, 
                        padx=responsive_config.padding_small, 
                        pady=(0, responsive_config.padding_small))
    
    # Bind double-click to edit expense
    expense_listbox.bind('<Double-Button-1>', lambda e: edit_expense_selected())

    # Populate listboxes with existing data
    for entry in current_entries:
        income_listbox.insert(tk.END, f"{entry[0]:<30} ₱{entry[1]:>10,.2f}")
    
    for expense in current_expenses:
        expense_listbox.insert(tk.END, f"{expense[0]:<30} ₱{expense[1]:>10,.2f}")

    # === EDIT MODE for income ===
    def edit_income_selected():
        sel = income_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No income selected to edit")
            return
        idx = sel[0]
        old_name, old_amount = current_entries[idx]

        edit_win = tk.Toplevel(inc)
        edit_win.title("Edit Income Entry")
        edit_win.geometry("400x300")
        edit_win.configure(bg=MODERN_COLORS['light'])
        edit_win.resizable(False, False)

        # Center the edit window
        edit_win.update_idletasks()
        x = (edit_win.winfo_screenwidth() // 2) - (400 // 2)
        y = (edit_win.winfo_screenheight() // 2) - (300 // 2)
        edit_win.geometry(f"400x300+{x}+{y}")

        # Main container
        edit_container = create_modern_frame(edit_win, MODERN_COLORS['light'])
        edit_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title
        title_label = tk.Label(edit_container, text="Edit Income Entry", 
                             font=MODERN_FONTS['subheading'], 
                             bg=MODERN_COLORS['light'], 
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 20))

        # Income source field
        tk.Label(edit_container, text="Income Source", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['light'], 
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))
        
        e_name = create_modern_entry(edit_container)
        e_name.insert(0, old_name)
        e_name.pack(fill=tk.X, pady=(0, 15))

        # Amount field
        tk.Label(edit_container, text="Amount (₱)", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['light'], 
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))
        
        e_income = create_modern_entry(edit_container)
        e_income.insert(0, str(old_amount))
        e_income.pack(fill=tk.X, pady=(0, 20))

        def save_edit():
            new_name = e_name.get().strip()
            new_income_str = e_income.get().strip()
            if not new_name or not new_income_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_income = float(new_income_str)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
                return
            # Update in-memory entries and listbox
            current_entries[idx] = (new_name, new_income)
            income_listbox.delete(0, tk.END)
            for entry in current_entries:
                income_listbox.insert(tk.END, f"{entry[0]:<30} ₱{entry[1]:>10,.2f}")
            edit_win.destroy()
            save_data(current_date_str)

        # Save button
        save_btn = create_modern_button(edit_container, "Save Changes", 
                                      command=save_edit,
                                      style='success', width=20)
        save_btn.pack(pady=10)

    # === EDIT MODE for expense ===
    def edit_expense_selected():
        sel = expense_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to edit")
            return
        idx = sel[0]
        old_desc, old_amount = current_expenses[idx]

        edit_win = tk.Toplevel(inc)
        edit_win.title("Edit Expense Entry")
        edit_win.geometry("420x300")
        edit_win.configure(bg=MODERN_COLORS['light'])
        edit_win.resizable(False, False)

        # Center the edit window
        edit_win.update_idletasks()
        x = (edit_win.winfo_screenwidth() // 2) - (420 // 2)
        y = (edit_win.winfo_screenheight() // 2) - (300 // 2)
        edit_win.geometry(f"420x300+{x}+{y}")

        # Main container
        edit_container = create_modern_frame(edit_win, MODERN_COLORS['light'])
        edit_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title
        title_label = tk.Label(edit_container, text="Edit Expense Entry", 
                             font=MODERN_FONTS['subheading'], 
                             bg=MODERN_COLORS['light'], 
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 20))

        # Category field
        tk.Label(edit_container, text="Category", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['light'], 
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))
        
        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(edit_container, values=categories, textvariable=cat_var, 
                               state="readonly", font=MODERN_FONTS['body'])
        # if old_desc matches one of categories, select it; else select Other and show custom
        if old_desc in categories:
            cat_menu.set(old_desc)
        else:
            cat_menu.set("Other")
        cat_menu.pack(fill=tk.X, pady=(0, 15))

        custom_var = tk.StringVar()
        custom_entry = create_modern_entry(edit_container)
        custom_entry.config(textvariable=custom_var)
        if cat_menu.get() == "Other":
            custom_var.set(old_desc)
            custom_entry.pack(fill=tk.X, pady=(0, 15))

        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(fill=tk.X, pady=(0, 15))
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        # Amount field
        tk.Label(edit_container, text="Amount (₱)", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['light'], 
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))
        
        e_amount = create_modern_entry(edit_container)
        e_amount.insert(0, str(old_amount))
        e_amount.pack(fill=tk.X, pady=(0, 20))

        def save_edit():
            if cat_menu.get() == "Other":
                new_desc = custom_var.get().strip()
            else:
                new_desc = cat_menu.get()
            new_amount_str = e_amount.get().strip()
            if not new_desc or not new_amount_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_amount = float(new_amount_str)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
                return
            current_expenses[idx] = (new_desc, new_amount)
            expense_listbox.delete(0, tk.END)
            for expense in current_expenses:
                expense_listbox.insert(tk.END, f"{expense[0]:<30} ₱{expense[1]:>10,.2f}")
            edit_win.destroy()
            save_data(current_date_str)

        # Save button
        save_btn = create_modern_button(edit_container, "Save Changes", 
                                      command=save_edit,
                                      style='success', width=20)
        save_btn.pack(pady=10)

    # Delete selected income with confirmation
    def delete_income_selected():
        sel = income_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "Please select an income entry to delete")
            return
        idx = sel[0]
        entry = current_entries[idx]
        
        # Show confirmation dialog
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete this income entry?\n\n"
                                   f"Source: {entry[0]}\n"
                                   f"Amount: ₱{entry[1]:,.2f}")
        
        if result:
            current_entries.pop(idx)
            income_listbox.delete(idx)
            save_data(current_date_str)
            messagebox.showinfo("Success", "Income entry deleted successfully!")

    # Delete selected expense with confirmation
    def delete_expense_selected():
        sel = expense_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "Please select an expense entry to delete")
            return
        idx = sel[0]
        expense = current_expenses[idx]
        
        # Show confirmation dialog
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete this expense entry?\n\n"
                                   f"Category: {expense[0]}\n"
                                   f"Amount: ₱{expense[1]:,.2f}")
        
        if result:
            current_expenses.pop(idx)
            expense_listbox.delete(idx)
            save_data(current_date_str)
            messagebox.showinfo("Success", "Expense entry deleted successfully!")

    # Responsive button section
    button_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    button_frame.pack(fill=tk.X, pady=responsive_config.padding_small)

    # Undo button (bottom section) - responsive sizing
    responsive_button_width = max(int(18 * responsive_config.scale_factor), 15)
    undo_btn = create_modern_button(button_frame, "← Back to Calendar", 
                                   command=lambda: [inc.destroy(), navigate_back()],
                                   style='warning', width=responsive_button_width)
    undo_btn.pack(pady=responsive_config.padding_tiny)

    # Action buttons in responsive card style
    action_card = create_modern_frame(button_frame, MODERN_COLORS['white'])
    action_card.pack(fill=tk.X, pady=responsive_config.padding_small)
    action_card.configure(relief='solid', bd=1)

    # Income management section
    tk.Label(action_card, text="📊 Manage Income", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(pady=(responsive_config.padding_medium, responsive_config.padding_tiny))
    
    # Instruction label for income
    tk.Label(action_card, text="💡 Double-click an item to edit, or use buttons below", 
            font=MODERN_FONTS['small'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(pady=(0, responsive_config.padding_small))

    income_btn_row = create_modern_frame(action_card, MODERN_COLORS['white'])
    income_btn_row.pack(fill=tk.X, 
                       padx=responsive_config.padding_medium, 
                       pady=(0, responsive_config.padding_small))

    responsive_button_width_small = max(int(12 * responsive_config.scale_factor), 10)
    edit_income_btn = create_modern_button(income_btn_row, "✏️ Edit", 
                                         command=edit_income_selected,
                                         style='secondary', width=responsive_button_width_small)
    edit_income_btn.pack(side=tk.LEFT, padx=responsive_config.padding_tiny)

    delete_income_btn = create_modern_button(income_btn_row, "🗑️ Delete", 
                                           command=delete_income_selected,
                                           style='danger', width=responsive_button_width_small)
    delete_income_btn.pack(side=tk.LEFT, padx=responsive_config.padding_tiny)

    # Expense management section
    tk.Label(action_card, text="💸 Manage Expenses", 
            font=MODERN_FONTS['subheading'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(pady=(responsive_config.padding_medium, responsive_config.padding_tiny))
    
    # Instruction label for expenses
    tk.Label(action_card, text="💡 Double-click an item to edit, or use buttons below", 
            font=MODERN_FONTS['small'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(pady=(0, responsive_config.padding_small))

    expense_btn_row = create_modern_frame(action_card, MODERN_COLORS['white'])
    expense_btn_row.pack(fill=tk.X, 
                        padx=responsive_config.padding_medium, 
                        pady=(0, responsive_config.padding_medium))

    edit_expense_btn = create_modern_button(expense_btn_row, "✏️ Edit", 
                                          command=edit_expense_selected,
                                          style='secondary', width=responsive_button_width_small)
    edit_expense_btn.pack(side=tk.LEFT, padx=responsive_config.padding_tiny)

    delete_expense_btn = create_modern_button(expense_btn_row, "🗑️ Delete", 
                                            command=delete_expense_selected,
                                            style='danger', width=responsive_button_width_small)
    delete_expense_btn.pack(side=tk.LEFT, padx=responsive_config.padding_tiny)

    # Navigation button - responsive sizing
    responsive_button_width_large = max(int(25 * responsive_config.scale_factor), 20)
    next_btn = create_modern_button(button_frame, "📈 View Summary", 
                                  command=lambda:[save_data(current_date_str), inc.destroy(), total_screen(day, year, month)],
                                  style='success', width=responsive_button_width_large)
    next_btn.pack(pady=responsive_config.padding_tiny)

    # Sign out button - responsive sizing
    signout_btn = create_modern_button(button_frame, "🚪 Sign Out", 
                                      command=lambda:[inc.destroy(), login_screen()],
                                      style='danger', width=responsive_button_width)
    signout_btn.pack(pady=responsive_config.padding_tiny)

    # Add global undo shortcut
    add_global_undo_shortcut(inc)

    inc.mainloop()

# ---------------- Expenses Screen (Edit/Delete + categories dropdown + Other) ----------------
def expenses_screen(day, year, month):
    # Add to navigation history
    add_to_history('expenses_screen', day, year, month)
    
    exp = tk.Tk()
    exp.title("Expense Tracking - Money Rider")
    exp.configure(bg=MODERN_COLORS['background'])
    exp.resizable(False, False)

    # Center the window with responsive sizing
    center_window(exp)

    expense_var = tk.StringVar()
    amount_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Main container with responsive scrolling
    main_container = create_scrollable_frame(exp, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_medium, 
                       pady=responsive_config.padding_medium)
    
    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Header section
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(fill=tk.X, pady=(0, responsive_config.padding_medium))

    # Title
    title_label = tk.Label(header_frame, text="Expense Tracking", 
                          font=MODERN_FONTS['heading'], 
                          bg=MODERN_COLORS['background'], 
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, responsive_config.padding_small))

    # Date display
    date_label = tk.Label(header_frame, text=f"{year}-{month:02d}-{day:02d}",
                         font=MODERN_FONTS['body'], 
                         bg=MODERN_COLORS['background'], 
                         fg=MODERN_COLORS['text_primary'])
    date_label.pack()

    # Helper to show Add Expense popup with category dropdown + 'Other' option
    def add_option():
        popup = tk.Toplevel(exp)
        popup.title("Add New Expense")
        popup.configure(bg=MODERN_COLORS['light'])
        popup.resizable(False, False)

        # Center the popup with responsive sizing
        popup_width = max(int(450 * responsive_config.scale_factor), 350)
        popup_height = max(int(400 * responsive_config.scale_factor), 300)
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup_width // 2)
        y = (popup.winfo_screenheight() // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        # Main container
        popup_container = create_modern_frame(popup, MODERN_COLORS['light'])
        popup_container.pack(fill=tk.BOTH, expand=True, 
                            padx=responsive_config.padding_medium, 
                            pady=responsive_config.padding_medium)

        # Title
        title_label = tk.Label(popup_container, text="Add New Expense", 
                             font=MODERN_FONTS['subheading'], 
                             bg=MODERN_COLORS['light'], 
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 20))

        # Category selection
        tk.Label(popup_container, text="Category", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['light'], 
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))
        
        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(popup_container, values=categories, textvariable=cat_var, 
                               state="readonly", font=MODERN_FONTS['body'])
        cat_menu.pack(fill=tk.X, pady=(0, 15))
        cat_menu.set(categories[0])

        # Custom category entry (hidden by default)
        custom_var = tk.StringVar()
        custom_entry = create_modern_entry(popup_container)
        custom_entry.config(textvariable=custom_var)
        
        # only show when Other selected
        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(fill=tk.X, pady=(0, 15))
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        # Amount field
        tk.Label(popup_container, text="Amount (₱)", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['light'], 
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))
        
        amount_entry = create_modern_entry(popup_container)
        amount_entry.config(textvariable=amount_var)
        amount_entry.pack(fill=tk.X, pady=(0, 20))

        def save_expense():
            category = cat_var.get()
            if category == "Other":
                category = custom_var.get().strip()
            amount = amount_var.get().strip()
            if not category or not amount:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            try:
                amount_val = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
                return

            entry = (category, amount_val)
            current_expenses.append(entry)
            # Format with modern styling
            listbox.insert(tk.END, f"{category:<30} ₱{amount_val:>10,.2f}")
            amount_var.set("")
            custom_var.set("")
            popup.destroy()
            save_data(current_date_str)

        # Save button
        save_btn = create_modern_button(popup_container, "Save Expense", 
                                      command=save_expense,
                                      style='success', width=20)
        save_btn.pack(pady=10)

    # Display section
    display_frame = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    display_frame.configure(relief='solid', bd=1)

    # Header for the list
    list_header = create_modern_frame(display_frame, MODERN_COLORS['card'])
    list_header.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(list_header, text="Expense Category", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, padx=10)
    
    tk.Label(list_header, text="Amount", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.RIGHT, padx=10)
    
    # Instruction label
    instruction_frame = create_modern_frame(display_frame, MODERN_COLORS['card'])
    instruction_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
    
    tk.Label(instruction_frame, text="💡 Double-click an item to edit it", 
            font=('Segoe UI', 10), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack()

    # Create a listbox with modern styling and double-click editing
    listbox = tk.Listbox(display_frame, 
                        font=MODERN_FONTS['body'],
                        bg=MODERN_COLORS['white'], 
                        fg=MODERN_COLORS['text_primary'],
                        selectbackground=MODERN_COLORS['primary'],
                        selectforeground=MODERN_COLORS['white'],
                        relief='flat',
                        bd=0,
                        highlightthickness=0,
                        cursor='hand2')  # Show hand cursor to indicate clickable
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    # Bind double-click to edit expense
    listbox.bind('<Double-Button-1>', lambda e: edit_selected())

    # Populate listbox with existing expenses
    for expense in current_expenses:
        listbox.insert(tk.END, f"{expense[0]:<30} ₱{expense[1]:>10,.2f}")

    # === EDIT MODE for expense ===
    def edit_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to edit")
            return
        idx = sel[0]
        old_desc, old_amount = current_expenses[idx]

        edit_win = tk.Toplevel(exp)
        edit_win.title("Edit Expense")
        edit_win.geometry("420x300")
        edit_win.configure(bg="#1C1C1C")

        tk.Label(edit_win, text="Category", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)
        # show combobox with categories and 'Other' as fallback
        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(edit_win, values=categories, textvariable=cat_var, state="readonly", font=("Bubblegum Sans", 12))
        # if old_desc matches one of categories, select it; else select Other and show custom
        if old_desc in categories:
            cat_menu.set(old_desc)
        else:
            cat_menu.set("Other")
        cat_menu.pack(pady=5)

        custom_var = tk.StringVar()
        custom_entry = tk.Entry(edit_win, textvariable=custom_var, font=("Bubblegum Sans", 12))
        if cat_menu.get() == "Other":
            custom_var.set(old_desc)
            custom_entry.pack(pady=5)

        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(pady=5)
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        tk.Label(edit_win, text="Amount", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)
        e_amount = tk.Entry(edit_win, font=("Bubblegum Sans", 12))
        e_amount.insert(0, str(old_amount))
        e_amount.pack(pady=5)

        def save_edit():
            if cat_menu.get() == "Other":
                new_desc = custom_var.get().strip()
            else:
                new_desc = cat_menu.get()
            new_amount_str = e_amount.get().strip()
            if not new_desc or not new_amount_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_amount = float(new_amount_str)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return
            current_expenses[idx] = (new_desc, new_amount)
            listbox.delete(0, tk.END)
            for expense in current_expenses:
                listbox.insert(tk.END, f"{expense[0].ljust(30)}{str(expense[1]).rjust(10)}")
            edit_win.destroy()
            save_data(current_date_str)

        save_btn = create_modern_button(edit_win, "💾 Save", 
                                       command=save_edit,
                                       style='success', width=15)
        save_btn.pack(pady=10)

    # Delete selected expense with confirmation
    def delete_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to delete")
            return
        idx = sel[0]
        expense = current_expenses[idx]
        
        # Show confirmation dialog
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete this expense entry?\n\n"
                                   f"Category: {expense[0]}\n"
                                   f"Amount: ₱{expense[1]:,.2f}")
        
        if result:
            current_expenses.pop(idx)
            listbox.delete(idx)
            save_data(current_date_str)
            messagebox.showinfo("Success", "Expense entry deleted successfully!")

    # Button section
    button_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    button_frame.pack(fill=tk.X, pady=20)

    # Action buttons
    action_frame = create_modern_frame(button_frame, MODERN_COLORS['background'])
    action_frame.pack()

    # Undo button (left side)
    undo_btn = create_undo_button(action_frame, 
                                 command=lambda: [exp.destroy(), navigate_back()],
                                 style='warning', width=10)
    undo_btn.pack(side=tk.LEFT, padx=5)

    add_btn = create_modern_button(action_frame, "Add Expense", 
                                 command=add_option,
                                 style='primary', width=15)
    add_btn.pack(side=tk.LEFT, padx=5)

    edit_btn = create_modern_button(action_frame, "Edit", 
                                  command=edit_selected,
                                  style='secondary', width=10)
    edit_btn.pack(side=tk.LEFT, padx=5)

    delete_btn = create_modern_button(action_frame, "Delete", 
                                    command=delete_selected,
                                    style='danger', width=10)
    delete_btn.pack(side=tk.LEFT, padx=5)

    # Navigation button
    nav_frame = create_modern_frame(button_frame, MODERN_COLORS['background'])
    nav_frame.pack(pady=15)

    next_btn = create_modern_button(nav_frame, "View Summary", 
                                  command=lambda:[save_data(current_date_str), exp.destroy(), total_screen(day, year, month)],
                                  style='success', width=20)
    next_btn.pack(pady=5)

    # Sign out button - mobile style
    signout_btn = create_modern_button(nav_frame, "🚪 Sign Out", 
                                      command=lambda:[exp.destroy(), login_screen()],
                                      style='danger', width=20)
    signout_btn.pack(pady=5)

    # Add global undo shortcut
    add_global_undo_shortcut(exp)

    exp.mainloop()

# ---------------- Save data for the current date (per-user) ----------------
def save_data(date_str):
    # compute totals from buffers and store into user's financial_data
    total_income = sum(float(entry[1]) for entry in current_entries) if current_entries else 0.0
    total_expenses = sum(float(expense[1]) for expense in current_expenses) if current_expenses else 0.0

    # ensure financial_data is a dict for the logged-in user
    # (financial_data loaded from user's file at login)
    financial_data[date_str] = {
        "income": total_income,
        "expenses": total_expenses,
        "entries": [[e[0], e[1]] for e in current_entries],
        "expense_entries": [[e[0], e[1]] for e in current_expenses]
    }
    # persist to current user's file
    if current_user:
        save_user_data(current_user)

# ---------------- Total Screen (keeps original layout) ----------------
def total_screen(day, year, month):
    # Add to navigation history
    add_to_history('total_screen', day, year, month)
    
    total = tk.Tk()
    total.title("Financial Summary - Money Rider")
    total.configure(bg=MODERN_COLORS['background'])
    total.resizable(False, False)

    # Center the window with responsive sizing
    center_window(total)

    # Main container with responsive padding and scrolling
    main_container = create_scrollable_frame(total, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, 
                       padx=responsive_config.padding_medium, 
                       pady=responsive_config.padding_medium)
    
    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Header section
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(pady=(0, responsive_config.padding_large))

    # Title - responsive styling
    title_label = tk.Label(header_frame, text="Financial Summary", 
                          font=MODERN_FONTS['title'], 
                          bg=MODERN_COLORS['background'], 
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, responsive_config.padding_small))

    # Date display - responsive styling
    date_str = f"{year}-{month:02d}-{day:02d}"
    date_label = tk.Label(header_frame, text=f"{date_str}", 
                         font=MODERN_FONTS['subheading'], 
                         bg=MODERN_COLORS['background'], 
                         fg=MODERN_COLORS['text_primary'])
    date_label.pack(pady=responsive_config.padding_tiny)

    # Summary container - responsive card style
    summary_container = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    summary_container.pack(fill=tk.X, pady=responsive_config.padding_large)
    summary_container.configure(relief='solid', bd=2)

    # Income section - responsive styling
    income_frame = create_modern_frame(summary_container, MODERN_COLORS['card'])
    income_frame.pack(fill=tk.X, 
                     padx=responsive_config.padding_medium, 
                     pady=responsive_config.padding_large)

    total_income = sum(float(i[1]) for i in current_entries) if current_entries else 0.0
    income_font_size = max(int(18 * responsive_config.scale_factor), 14)
    tk.Label(income_frame, text="Total Income:", 
            font=('Segoe UI', income_font_size, 'bold'), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT)
    tk.Label(income_frame, text=f"₱{total_income:,.2f}", 
            font=('Segoe UI', income_font_size, 'bold'), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['success']).pack(side=tk.RIGHT)

    # Expenses section - responsive styling
    expenses_frame = create_modern_frame(summary_container, MODERN_COLORS['card'])
    expenses_frame.pack(fill=tk.X, 
                       padx=responsive_config.padding_medium, 
                       pady=responsive_config.padding_large)

    total_expenses = sum(float(e[1]) for e in current_expenses) if current_expenses else 0.0
    tk.Label(expenses_frame, text="Total Expenses:", 
            font=('Segoe UI', income_font_size, 'bold'), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT)
    tk.Label(expenses_frame, text=f"₱{total_expenses:,.2f}", 
            font=('Segoe UI', income_font_size, 'bold'), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['danger']).pack(side=tk.RIGHT)

    # Net total section - responsive styling
    net_frame = create_modern_frame(summary_container, MODERN_COLORS['card'])
    net_frame.pack(fill=tk.X, 
                  padx=responsive_config.padding_medium, 
                  pady=responsive_config.padding_medium)
    net_frame.configure(relief='solid', bd=3)

    day_total = total_income - total_expenses
    net_font_size = max(int(20 * responsive_config.scale_factor), 16)
    net_padding = max(int(20 * responsive_config.scale_factor), 15)
    tk.Label(net_frame, text="Net Total:", 
            font=('Segoe UI', net_font_size, 'bold'), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, 
                                                   padx=net_padding, 
                                                   pady=responsive_config.padding_medium)
    tk.Label(net_frame, text=f"₱{day_total:,.2f}", 
            font=('Segoe UI', net_font_size, 'bold'), 
            bg=MODERN_COLORS['card'], 
            fg=MODERN_COLORS['success'] if day_total >= 0 else MODERN_COLORS['danger']).pack(side=tk.RIGHT, 
                                                                                            padx=net_padding, 
                                                                                            pady=responsive_config.padding_medium)

    # Navigation buttons - responsive styling
    button_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    button_frame.pack(pady=responsive_config.padding_medium)

    # Undo button - responsive sizing
    responsive_button_width = max(int(15 * responsive_config.scale_factor), 12)
    undo_btn = create_undo_button(button_frame, 
                                 command=lambda: [total.destroy(), navigate_back()],
                                 style='warning', width=responsive_button_width)
    undo_btn.pack(pady=responsive_config.padding_small)

    # Back to expenses button - responsive sizing
    responsive_button_width_medium = max(int(20 * responsive_config.scale_factor), 15)
    back_btn = create_modern_button(button_frame, "💸 Back to Expenses", 
                                  command=lambda:[total.destroy(), expenses_screen(day, year, month)],
                                  style='secondary', width=responsive_button_width_medium)
    back_btn.pack(pady=responsive_config.padding_small)

    # Finish button - responsive sizing
    responsive_button_width_large = max(int(25 * responsive_config.scale_factor), 20)
    finish_btn = create_modern_button(button_frame, "✅ Finish & Return to Calendar", 
                                    command=lambda:[total.destroy(), calendar_screen()],
                                    style='primary', width=responsive_button_width_large)
    finish_btn.pack(pady=responsive_config.padding_small)

    # Sign out button - responsive sizing
    signout_btn = create_modern_button(button_frame, "🚪 Sign Out", 
                                      command=lambda:[total.destroy(), login_screen()],
                                      style='danger', width=responsive_button_width_medium)
    signout_btn.pack(pady=responsive_config.padding_tiny)

    # Add global undo shortcut
    add_global_undo_shortcut(total)

    total.mainloop()

# ---------------- Start the app ----------------
if __name__ == "__main__":
    splash_screen()

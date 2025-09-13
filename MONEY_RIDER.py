
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import calendar
import json
import os

# Modern UI Configuration
MODERN_COLORS = {
    'primary': '#2563EB',      # Blue
    'primary_dark': '#1D4ED8',
    'secondary': '#7C3AED',    # Purple
    'success': '#10B981',      # Green
    'danger': '#EF4444',       # Red
    'warning': '#F59E0B',      # Orange
    'dark': '#1F2937',         # Dark gray
    'darker': '#111827',       # Darker gray
    'light': '#F9FAFB',        # Light gray
    'white': '#FFFFFF',
    'border': '#E5E7EB'
}

MODERN_FONTS = {
    'title': ('Segoe UI', 28, 'bold'),
    'heading': ('Segoe UI', 20, 'bold'),
    'subheading': ('Segoe UI', 16, 'bold'),
    'body': ('Segoe UI', 12),
    'small': ('Segoe UI', 10)
}

def create_modern_button(parent, text, command=None, style='primary', width=None, height=None):
    """Create a mobile-friendly styled button"""
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
    
    # Mobile-friendly button sizing
    button_height = 1 if height is None else height
    button_width = 15 if width is None else width
    
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=('Segoe UI', 14, 'bold'),  # Larger font for mobile
        relief='flat',
        bd=0,
        cursor='hand2',
        width=button_width,
        height=button_height,
        padx=20,  # More padding for touch
        pady=15,  # More vertical padding
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
    """Create a mobile-friendly styled entry field"""
    entry = tk.Entry(
        parent,
        font=('Segoe UI', 16),  # Larger font for mobile
        relief='flat',
        bd=2,
        highlightthickness=3,
        highlightcolor=MODERN_COLORS['primary'],
        highlightbackground=MODERN_COLORS['border'],
        bg=MODERN_COLORS['white'],
        fg=MODERN_COLORS['dark'],
        insertbackground=MODERN_COLORS['primary'],
        show=show,
        width=25  # Wider for mobile
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
    splash.geometry("400x700")  # Mobile-like aspect ratio
    splash.configure(bg=MODERN_COLORS['light'])
    splash.resizable(False, False)

    # Center the window
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (700 // 2)
    splash.geometry(f"400x700+{x}+{y}")

    # Main container with mobile-like padding
    main_container = create_modern_frame(splash, MODERN_COLORS['light'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Header section
    header_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    header_frame.pack(pady=(30, 50))

    # App icon/logo area - mobile style
    icon_frame = create_modern_frame(header_frame, MODERN_COLORS['primary'])
    icon_frame.pack(pady=20)
    icon_frame.configure(relief='flat', bd=0, height=120, width=120)
    
    # Option 1: Use emoji logo (current)
    icon_label = tk.Label(icon_frame, text="🏍️", font=('Segoe UI Emoji', 50), 
                         bg=MODERN_COLORS['primary'], fg=MODERN_COLORS['white'])
    icon_label.pack(expand=True)

    # Title - mobile typography
    title = tk.Label(header_frame, text="Money Rider", 
                    font=('Segoe UI', 32, 'bold'), 
                    bg=MODERN_COLORS['light'], 
                    fg=MODERN_COLORS['dark'])
    title.pack(pady=15)

    # Subtitle
    subtitle = tk.Label(header_frame, text="Track your finances with ease", 
                       font=('Segoe UI', 16), 
                       bg=MODERN_COLORS['light'], 
                       fg=MODERN_COLORS['dark'])
    subtitle.pack(pady=8)

    # Button container with mobile spacing
    button_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    button_frame.pack(pady=40)

    # Login button - mobile style
    login_btn = create_modern_button(button_frame, "📱 Sign In", 
                                   command=lambda:[splash.destroy(), login_screen()],
                                   style='primary', width=20)
    login_btn.pack(pady=20)

    # Create account button - mobile style
    create_account_btn = create_modern_button(button_frame, "👤 Create Account", 
                                            command=lambda:[splash.destroy(), create_account_screen()],
                                            style='secondary', width=20)
    create_account_btn.pack(pady=15)

    # Footer - mobile style
    footer_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    footer_frame.pack(side=tk.BOTTOM, pady=20)
    
    footer_text = tk.Label(footer_frame, text="© 2024 Money Rider", 
                          font=('Segoe UI', 12), 
                          bg=MODERN_COLORS['light'], 
                          fg=MODERN_COLORS['dark'])
    footer_text.pack()

    splash.mainloop()

# ---------------- Create Account ----------------
def create_account_screen():
    # Add to navigation history
    add_to_history('create_account_screen')
    
    create = tk.Tk()
    create.title("Create Account - Money Rider")
    create.geometry("400x700")  # Mobile aspect ratio
    create.configure(bg=MODERN_COLORS['light'])
    create.resizable(False, False)

    # Center the window
    create.update_idletasks()
    x = (create.winfo_screenwidth() // 2) - (400 // 2)
    y = (create.winfo_screenheight() // 2) - (700 // 2)
    create.geometry(f"400x700+{x}+{y}")

    # Main container with mobile padding
    main_container = create_modern_frame(create, MODERN_COLORS['light'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Header - mobile style
    header_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    header_frame.pack(pady=(0, 30))

    title = tk.Label(header_frame, text="Create Account", 
                    font=('Segoe UI', 28, 'bold'), 
                    bg=MODERN_COLORS['light'], 
                    fg=MODERN_COLORS['dark'])
    title.pack(pady=15)

    subtitle = tk.Label(header_frame, text="Join Money Rider today", 
                       font=('Segoe UI', 16), 
                       bg=MODERN_COLORS['light'], 
                       fg=MODERN_COLORS['dark'])
    subtitle.pack(pady=5)

    # Form container - mobile card style
    form_frame = create_modern_frame(main_container, MODERN_COLORS['white'])
    form_frame.pack(fill=tk.X, pady=20)
    form_frame.configure(relief='solid', bd=2)

    # Username field - mobile style
    tk.Label(form_frame, text="Username", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=25, pady=(25, 8))
    
    username_entry = create_modern_entry(form_frame)
    username_entry.pack(fill=tk.X, padx=25, pady=(0, 20))

    # Password field - mobile style
    tk.Label(form_frame, text="Password", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=25, pady=(15, 8))
    
    password_var = tk.StringVar()
    password_entry = create_modern_entry(form_frame, show="*")
    password_entry.config(textvariable=password_var)
    password_entry.pack(fill=tk.X, padx=25, pady=(0, 10))

    # Password visibility toggle - mobile style
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁 Show Password")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈 Hide Password")
    
    eye_btn = create_modern_button(form_frame, "👁 Show Password", command=toggle_pw, style='secondary', width=20)
    eye_btn.pack(pady=(0, 25))

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

    # Button container - mobile style
    button_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    button_frame.pack(pady=30)

    # Create button - mobile style
    create_btn = create_modern_button(button_frame, "✅ Create Account", 
                                    command=create_account,
                                    style='primary', width=20)
    create_btn.pack(pady=20)

    # Back button - mobile style
    back_btn = create_modern_button(button_frame, "← Back to Sign In", 
                                  command=lambda: [create.destroy(), splash_screen()],
                                  style='secondary', width=20)
    back_btn.pack(pady=10)

# ---------------- Login ----------------
def login_screen():
    # Add to navigation history
    add_to_history('login_screen')
    
    login = tk.Tk()
    login.title("Sign In - Money Rider")
    login.geometry("400x700")  # Mobile aspect ratio
    login.configure(bg=MODERN_COLORS['light'])
    login.resizable(False, False)

    # Center the window
    login.update_idletasks()
    x = (login.winfo_screenwidth() // 2) - (400 // 2)
    y = (login.winfo_screenheight() // 2) - (700 // 2)
    login.geometry(f"400x700+{x}+{y}")

    # Main container with mobile padding
    main_container = create_modern_frame(login, MODERN_COLORS['light'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Header - mobile style
    header_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    header_frame.pack(pady=(0, 30))

    title = tk.Label(header_frame, text="Welcome Back", 
                    font=('Segoe UI', 28, 'bold'), 
                    bg=MODERN_COLORS['light'], 
                    fg=MODERN_COLORS['dark'])
    title.pack(pady=15)

    subtitle = tk.Label(header_frame, text="Sign in to your account", 
                       font=('Segoe UI', 16), 
                       bg=MODERN_COLORS['light'], 
                       fg=MODERN_COLORS['dark'])
    subtitle.pack(pady=5)

    # Form container - mobile card style
    form_frame = create_modern_frame(main_container, MODERN_COLORS['white'])
    form_frame.pack(fill=tk.X, pady=20)
    form_frame.configure(relief='solid', bd=2)

    # Username field - mobile style
    tk.Label(form_frame, text="Username", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=25, pady=(25, 8))
    
    username_entry = create_modern_entry(form_frame)
    username_entry.pack(fill=tk.X, padx=25, pady=(0, 20))

    # Password field - mobile style
    tk.Label(form_frame, text="Password", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=25, pady=(15, 8))
    
    password_var = tk.StringVar()
    password_entry = create_modern_entry(form_frame, show="*")
    password_entry.config(textvariable=password_var)
    password_entry.pack(fill=tk.X, padx=25, pady=(0, 10))

    # Password visibility toggle - mobile style
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁 Show Password")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈 Hide Password")
    
    eye_btn = create_modern_button(form_frame, "👁 Show Password", command=toggle_pw, style='secondary', width=20)
    eye_btn.pack(pady=(0, 25))

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

    # Button container - mobile style
    button_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    button_frame.pack(pady=10)

    # Login button - mobile style
    login_btn = create_modern_button(button_frame, "🔑 Sign In", 
                                   command=validate_login,
                                   style='primary', width=20)
    login_btn.pack(pady=20)

    # Back button - mobile style
    back_btn = create_modern_button(button_frame, "← Back to Home", 
                                  command=lambda: [login.destroy(), splash_screen()],
                                  style='secondary', width=20)
    back_btn.pack(pady=10)

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
    cal.geometry("450x900")  # Mobile-like aspect ratio with more height
    cal.configure(bg=MODERN_COLORS['light'])
    cal.resizable(False, False)

    # Center the window
    cal.update_idletasks()
    x = (cal.winfo_screenwidth() // 2) - (450 // 2)
    y = (cal.winfo_screenheight() // 2) - (900 // 2)
    cal.geometry(f"450x900+{x}+{y}")

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
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

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

        # Main container
        cal_frame = create_modern_frame(cal, MODERN_COLORS['light'])
        cal_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header with title and controls
        header_frame = create_modern_frame(cal_frame, MODERN_COLORS['light'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title
        title_label = tk.Label(header_frame, text="Financial Calendar", 
                             font=MODERN_FONTS['heading'], 
                             bg=MODERN_COLORS['light'], 
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 15))

        # Month and year selection
        controls_frame = create_modern_frame(header_frame, MODERN_COLORS['light'])
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
        calendar_container = create_modern_frame(cal_frame, MODERN_COLORS['white'])
        calendar_container.pack(fill=tk.BOTH, expand=True, pady=10)
        calendar_container.configure(relief='solid', bd=1)

        # Days of week header
        days_frame = create_modern_frame(calendar_container, MODERN_COLORS['light'])
        days_frame.pack(fill=tk.X, padx=10, pady=10)

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days_of_week):
            day_label = tk.Label(days_frame, text=day, 
                               bg=MODERN_COLORS['light'], 
                               fg=MODERN_COLORS['dark'],
                               font=MODERN_FONTS['body'])
            day_label.grid(row=0, column=col, padx=1, pady=5, sticky='ew')
        
        # Configure grid weights for weekday headers to match calendar grid
        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1)

        # Calendar days grid
        days_grid_frame = create_modern_frame(calendar_container, MODERN_COLORS['white'])
        days_grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
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
        range_container = create_modern_frame(cal_frame, MODERN_COLORS['light'])
        range_container.pack(fill=tk.X, pady=15)

        range_title = tk.Label(range_container, text="Date Range Calculator", 
                              font=MODERN_FONTS['subheading'], 
                              bg=MODERN_COLORS['light'], 
                              fg=MODERN_COLORS['dark'])
        range_title.pack(pady=(0, 10))

        # Range input frame
        range_frame = create_modern_frame(range_container, MODERN_COLORS['white'])
        range_frame.pack(fill=tk.X, pady=10)
        range_frame.configure(relief='solid', bd=1)

        # Start date row
        start_frame = create_modern_frame(range_frame, MODERN_COLORS['white'])
        start_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(start_frame, text="From:", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['white'], 
                fg=MODERN_COLORS['dark']).grid(row=0, column=0, sticky="w", padx=(0, 10))

        start_day = ttk.Combobox(start_frame, values=list(range(1, 32)), width=3,
                                 font=MODERN_FONTS['body'], state="readonly")
        start_day.grid(row=0, column=1, sticky="w", padx=2)
        start_day.set("1")

        start_month = ttk.Combobox(start_frame, values=list(calendar.month_name[1:]), width=12,
                                   font=MODERN_FONTS['body'], state="readonly")
        start_month.grid(row=0, column=2, sticky="w", padx=2)
        start_month.set(calendar.month_name[current_month])

        start_year = ttk.Combobox(start_frame, values=list(range(2020, 2031)), width=6,
                                  font=MODERN_FONTS['body'], state="readonly")
        start_year.grid(row=0, column=3, sticky="w", padx=2)
        start_year.set(str(current_year))

        # End date row
        end_frame = create_modern_frame(range_frame, MODERN_COLORS['white'])
        end_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(end_frame, text="To:", 
                font=MODERN_FONTS['body'], 
                bg=MODERN_COLORS['white'], 
                fg=MODERN_COLORS['dark']).grid(row=0, column=0, sticky="w", padx=(0, 10))

        end_day = ttk.Combobox(end_frame, values=list(range(1, 32)), width=3,
                               font=MODERN_FONTS['body'], state="readonly")
        end_day.grid(row=0, column=1, sticky="w", padx=2)
        end_day.set("1")

        end_month = ttk.Combobox(end_frame, values=list(calendar.month_name[1:]), width=12,
                                 font=MODERN_FONTS['body'], state="readonly")
        end_month.grid(row=0, column=2, sticky="w", padx=2)
        end_month.set(calendar.month_name[current_month])

        end_year = ttk.Combobox(end_frame, values=list(range(2020, 2031)), width=6,
                                font=MODERN_FONTS['body'], state="readonly")
        end_year.grid(row=0, column=3, sticky="w", padx=2)
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

        # Navigation buttons - mobile style
        nav_frame = create_modern_frame(cal_frame, MODERN_COLORS['light'])
        nav_frame.pack(pady=20)

        # Undo button - mobile style
        undo_btn = create_undo_button(nav_frame, 
                                     command=lambda: [cal.destroy(), navigate_back()],
                                     style='warning', width=20)
        undo_btn.pack(pady=5)

        # Sign out button with better mobile styling
        signout_btn = create_modern_button(nav_frame, "🚪 Sign Out", 
                                          command=lambda: [cal.destroy(), login_screen()],
                                          style='danger', width=20)
        signout_btn.pack(pady=5)

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
    inc.geometry("450x900")  # Mobile aspect ratio with more height
    inc.configure(bg=MODERN_COLORS['light'])
    inc.resizable(False, False)

    # Center the window
    inc.update_idletasks()
    x = (inc.winfo_screenwidth() // 2) - (450 // 2)
    y = (inc.winfo_screenheight() // 2) - (900 // 2)
    inc.geometry(f"450x900+{x}+{y}")

    # Floating undo button in top-right corner
    floating_undo_frame = create_modern_frame(inc, MODERN_COLORS['primary'])
    floating_undo_frame.place(x=400, y=10, width=40, height=40)
    
    floating_undo_btn = tk.Button(floating_undo_frame, text="←", 
                                 command=lambda: [inc.destroy(), navigate_back()],
                                 bg=MODERN_COLORS['primary'], fg=MODERN_COLORS['white'],
                                 font=('Segoe UI', 16, 'bold'), relief='flat', bd=0,
                                 cursor='hand2', activebackground=MODERN_COLORS['primary_dark'])
    floating_undo_btn.pack(fill=tk.BOTH, expand=True)

    name_var = tk.StringVar()
    income_var = tk.StringVar()
    
    # Expense variables
    expense_var = tk.StringVar()
    amount_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Main container with mobile-like padding
    main_container = create_modern_frame(inc, MODERN_COLORS['light'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Header section
    header_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    header_frame.pack(fill=tk.X, pady=(0, 20))

    # Title - mobile style
    title_label = tk.Label(header_frame, text="Financial Tracking", 
                          font=('Segoe UI', 24, 'bold'), 
                          bg=MODERN_COLORS['light'], 
                          fg=MODERN_COLORS['dark'])
    title_label.pack(pady=(0, 10))

    # Date display - mobile style
    date_label = tk.Label(header_frame, text=f"{year}-{month:02d}-{day:02d}",
                         font=('Segoe UI', 16), 
                         bg=MODERN_COLORS['light'], 
                         fg=MODERN_COLORS['dark'])
    date_label.pack(pady=5)

    # Undo button at the top for better visibility
    top_undo_btn = create_undo_button(header_frame, 
                                     command=lambda: [inc.destroy(), navigate_back()],
                                     style='warning', width=15)
    top_undo_btn.pack(pady=5)

    # Help text for keyboard shortcut
    help_text = tk.Label(header_frame, text="💡 Tip: Press Ctrl+Z to go back", 
                        font=('Segoe UI', 10), 
                        bg=MODERN_COLORS['light'], 
                        fg=MODERN_COLORS['dark'])
    help_text.pack(pady=2)

    # Input section with mobile-like cards
    input_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    input_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Create notebook for tabs with mobile styling
    notebook = ttk.Notebook(input_frame)
    notebook.pack(fill=tk.X)
    
    # Style the notebook for mobile look
    style = ttk.Style()
    style.configure('TNotebook', tabposition='n')
    style.configure('TNotebook.Tab', padding=[20, 10], font=MODERN_FONTS['body'])

    # Income tab with mobile card styling
    income_tab = create_modern_frame(notebook, MODERN_COLORS['white'])
    notebook.add(income_tab, text="💰 Income")

    # Income card container
    income_card = create_modern_frame(income_tab, MODERN_COLORS['white'])
    income_card.pack(fill=tk.X, padx=15, pady=15)
    income_card.configure(relief='solid', bd=1)

    # Income Source field with mobile styling
    tk.Label(income_card, text="Income Source", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=15, pady=(15, 5))
    
    name_entry = create_modern_entry(income_card)
    name_entry.config(textvariable=name_var)
    name_entry.pack(fill=tk.X, padx=15, pady=(0, 10))

    # Income amount field with mobile styling
    tk.Label(income_card, text="Amount (₱)", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=15, pady=(10, 5))
    
    income_entry = create_modern_entry(income_card)
    income_entry.config(textvariable=income_var)
    income_entry.pack(fill=tk.X, padx=15, pady=(0, 15))

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

    # Add Income button with mobile styling
    add_income_btn = create_modern_button(income_card, "➕ Add Income", 
                                        command=enter_income,
                                        style='success', width=25)
    add_income_btn.pack(pady=(0, 15))

    # Expenses tab with mobile card styling
    expense_tab = create_modern_frame(notebook, MODERN_COLORS['white'])
    notebook.add(expense_tab, text="💸 Expenses")

    # Expense card container
    expense_card = create_modern_frame(expense_tab, MODERN_COLORS['white'])
    expense_card.pack(fill=tk.X, padx=15, pady=15)
    expense_card.configure(relief='solid', bd=1)

    # Expense Category field with mobile styling
    tk.Label(expense_card, text="Category", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=15, pady=(15, 5))
    
    # Category dropdown with mobile styling
    category_var = tk.StringVar()
    categories = ["Food", "Gas", "Maintenance", "Other"]
    cat_menu = ttk.Combobox(expense_card, values=categories, textvariable=category_var, 
                           state="readonly", font=MODERN_FONTS['body'])
    cat_menu.pack(fill=tk.X, padx=15, pady=(0, 10))
    cat_menu.set(categories[0])

    # Custom category entry (hidden by default)
    custom_var = tk.StringVar()
    custom_entry = create_modern_entry(expense_card)
    custom_entry.config(textvariable=custom_var)
    
    # Show/hide custom entry based on category selection
    def on_cat_change(e=None):
        if category_var.get() == "Other":
            custom_entry.pack(fill=tk.X, padx=15, pady=(0, 10))
        else:
            custom_entry.pack_forget()
    cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

    # Expense amount field with mobile styling
    tk.Label(expense_card, text="Amount (₱)", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(anchor='w', padx=15, pady=(10, 5))
    
    expense_amount_entry = create_modern_entry(expense_card)
    expense_amount_entry.config(textvariable=amount_var)
    expense_amount_entry.pack(fill=tk.X, padx=15, pady=(0, 15))

    # Add Expense button with mobile styling
    add_expense_btn = create_modern_button(expense_card, "➕ Add Expense", 
                                         command=enter_expense,
                                         style='success', width=25)
    add_expense_btn.pack(pady=(0, 15))

    # Display section with tabs
    display_frame = create_modern_frame(main_container, MODERN_COLORS['white'])
    display_frame.pack(fill=tk.X, pady=(0, 15))
    display_frame.configure(relief='solid', bd=1, height=250)

    # Create notebook for display tabs
    display_notebook = ttk.Notebook(display_frame)
    display_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Income display tab
    income_display_tab = create_modern_frame(display_notebook, MODERN_COLORS['white'])
    display_notebook.add(income_display_tab, text="💰 Income List")

    # Header for income list
    income_header = create_modern_frame(income_display_tab, MODERN_COLORS['light'])
    income_header.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(income_header, text="Income Source", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT, padx=10)
    
    tk.Label(income_header, text="Amount", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.RIGHT, padx=10)

    # Create income listbox
    income_listbox = tk.Listbox(income_display_tab, 
                               font=MODERN_FONTS['body'],
                               bg=MODERN_COLORS['white'], 
                               fg=MODERN_COLORS['dark'],
                               selectbackground=MODERN_COLORS['primary'],
                               selectforeground=MODERN_COLORS['white'],
                               relief='flat',
                               bd=0,
                               highlightthickness=0)
    income_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # Expenses display tab
    expense_display_tab = create_modern_frame(display_notebook, MODERN_COLORS['white'])
    display_notebook.add(expense_display_tab, text="💸 Expense List")

    # Header for expense list
    expense_header = create_modern_frame(expense_display_tab, MODERN_COLORS['light'])
    expense_header.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(expense_header, text="Expense Category", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT, padx=10)
    
    tk.Label(expense_header, text="Amount", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.RIGHT, padx=10)

    # Create expense listbox
    expense_listbox = tk.Listbox(expense_display_tab, 
                                font=MODERN_FONTS['body'],
                                bg=MODERN_COLORS['white'], 
                                fg=MODERN_COLORS['dark'],
                                selectbackground=MODERN_COLORS['primary'],
                                selectforeground=MODERN_COLORS['white'],
                                relief='flat',
                                bd=0,
                                highlightthickness=0)
    expense_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

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

    # Delete selected income
    def delete_income_selected():
        sel = income_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "Please select an income entry to delete")
            return
        idx = sel[0]
        current_entries.pop(idx)
        income_listbox.delete(idx)
        save_data(current_date_str)

    # Delete selected expense
    def delete_expense_selected():
        sel = expense_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "Please select an expense entry to delete")
            return
        idx = sel[0]
        current_expenses.pop(idx)
        expense_listbox.delete(idx)
        save_data(current_date_str)

    # Mobile-style button section
    button_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    button_frame.pack(fill=tk.X, pady=10)

    # Undo button (bottom section) - mobile style
    undo_btn = create_modern_button(button_frame, "← Back to Calendar", 
                                   command=lambda: [inc.destroy(), navigate_back()],
                                   style='warning', width=18)
    undo_btn.pack(pady=5)

    # Action buttons in mobile card style
    action_card = create_modern_frame(button_frame, MODERN_COLORS['white'])
    action_card.pack(fill=tk.X, pady=10)
    action_card.configure(relief='solid', bd=1)

    # Income management section
    tk.Label(action_card, text="📊 Manage Income", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(pady=(15, 10))

    income_btn_row = create_modern_frame(action_card, MODERN_COLORS['white'])
    income_btn_row.pack(fill=tk.X, padx=15, pady=(0, 10))

    edit_income_btn = create_modern_button(income_btn_row, "✏️ Edit", 
                                         command=edit_income_selected,
                                         style='secondary', width=12)
    edit_income_btn.pack(side=tk.LEFT, padx=5)

    delete_income_btn = create_modern_button(income_btn_row, "🗑️ Delete", 
                                           command=delete_income_selected,
                                           style='danger', width=12)
    delete_income_btn.pack(side=tk.LEFT, padx=5)

    # Expense management section
    tk.Label(action_card, text="💸 Manage Expenses", 
            font=('Segoe UI', 16, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(pady=(15, 10))

    expense_btn_row = create_modern_frame(action_card, MODERN_COLORS['white'])
    expense_btn_row.pack(fill=tk.X, padx=15, pady=(0, 15))

    edit_expense_btn = create_modern_button(expense_btn_row, "✏️ Edit", 
                                          command=edit_expense_selected,
                                          style='secondary', width=12)
    edit_expense_btn.pack(side=tk.LEFT, padx=5)

    delete_expense_btn = create_modern_button(expense_btn_row, "🗑️ Delete", 
                                            command=delete_expense_selected,
                                            style='danger', width=12)
    delete_expense_btn.pack(side=tk.LEFT, padx=5)

    # Navigation button - mobile style
    next_btn = create_modern_button(button_frame, "📈 View Summary", 
                                  command=lambda:[save_data(current_date_str), inc.destroy(), total_screen(day, year, month)],
                                  style='success', width=25)
    next_btn.pack(pady=5)

    # Sign out button - mobile style
    signout_btn = create_modern_button(button_frame, "🚪 Sign Out", 
                                      command=lambda:[inc.destroy(), login_screen()],
                                      style='danger', width=20)
    signout_btn.pack(pady=5)

    # Add global undo shortcut
    add_global_undo_shortcut(inc)

    inc.mainloop()

# ---------------- Expenses Screen (Edit/Delete + categories dropdown + Other) ----------------
def expenses_screen(day, year, month):
    # Add to navigation history
    add_to_history('expenses_screen', day, year, month)
    
    exp = tk.Tk()
    exp.title("Expense Tracking - Money Rider")
    exp.geometry("700x800")
    exp.configure(bg=MODERN_COLORS['light'])
    exp.resizable(False, False)

    # Center the window
    exp.update_idletasks()
    x = (exp.winfo_screenwidth() // 2) - (700 // 2)
    y = (exp.winfo_screenheight() // 2) - (800 // 2)
    exp.geometry(f"700x800+{x}+{y}")

    expense_var = tk.StringVar()
    amount_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Main container
    main_container = create_modern_frame(exp, MODERN_COLORS['light'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # Header section
    header_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    header_frame.pack(fill=tk.X, pady=(0, 30))

    # Title
    title_label = tk.Label(header_frame, text="Expense Tracking", 
                          font=MODERN_FONTS['heading'], 
                          bg=MODERN_COLORS['light'], 
                          fg=MODERN_COLORS['dark'])
    title_label.pack(pady=(0, 10))

    # Date display
    date_label = tk.Label(header_frame, text=f"{year}-{month:02d}-{day:02d}",
                         font=MODERN_FONTS['body'], 
                         bg=MODERN_COLORS['light'], 
                         fg=MODERN_COLORS['dark'])
    date_label.pack()

    # Helper to show Add Expense popup with category dropdown + 'Other' option
    def add_option():
        popup = tk.Toplevel(exp)
        popup.title("Add New Expense")
        popup.geometry("450x400")
        popup.configure(bg=MODERN_COLORS['light'])
        popup.resizable(False, False)

        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (450 // 2)
        y = (popup.winfo_screenheight() // 2) - (400 // 2)
        popup.geometry(f"450x400+{x}+{y}")

        # Main container
        popup_container = create_modern_frame(popup, MODERN_COLORS['light'])
        popup_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

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
    display_frame = create_modern_frame(main_container, MODERN_COLORS['white'])
    display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    display_frame.configure(relief='solid', bd=1)

    # Header for the list
    list_header = create_modern_frame(display_frame, MODERN_COLORS['light'])
    list_header.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(list_header, text="Expense Category", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT, padx=10)
    
    tk.Label(list_header, text="Amount", 
            font=MODERN_FONTS['body'], 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.RIGHT, padx=10)

    # Create a listbox with modern styling
    listbox = tk.Listbox(display_frame, 
                        font=MODERN_FONTS['body'],
                        bg=MODERN_COLORS['white'], 
                        fg=MODERN_COLORS['dark'],
                        selectbackground=MODERN_COLORS['primary'],
                        selectforeground=MODERN_COLORS['white'],
                        relief='flat',
                        bd=0,
                        highlightthickness=0)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

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

    # Delete selected expense
    def delete_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to delete")
            return
        idx = sel[0]
        current_expenses.pop(idx)
        listbox.delete(idx)
        save_data(current_date_str)

    # Button section
    button_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    button_frame.pack(fill=tk.X, pady=20)

    # Action buttons
    action_frame = create_modern_frame(button_frame, MODERN_COLORS['light'])
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
    nav_frame = create_modern_frame(button_frame, MODERN_COLORS['light'])
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
    total.geometry("450x800")  # Mobile aspect ratio
    total.configure(bg=MODERN_COLORS['light'])
    total.resizable(False, False)

    # Center the window
    total.update_idletasks()
    x = (total.winfo_screenwidth() // 2) - (450 // 2)
    y = (total.winfo_screenheight() // 2) - (800 // 2)
    total.geometry(f"450x800+{x}+{y}")

    # Main container with mobile padding
    main_container = create_modern_frame(total, MODERN_COLORS['light'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Header section
    header_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    header_frame.pack(pady=(0, 20))

    # Title - mobile style
    title_label = tk.Label(header_frame, text="Financial Summary", 
                          font=('Segoe UI', 28, 'bold'), 
                          bg=MODERN_COLORS['light'], 
                          fg=MODERN_COLORS['dark'])
    title_label.pack(pady=(0, 10))

    # Date display - mobile style
    date_str = f"{year}-{month:02d}-{day:02d}"
    date_label = tk.Label(header_frame, text=f"{date_str}", 
                         font=('Segoe UI', 16), 
                         bg=MODERN_COLORS['light'], 
                         fg=MODERN_COLORS['dark'])
    date_label.pack(pady=5)

    # Summary container - mobile card style
    summary_container = create_modern_frame(main_container, MODERN_COLORS['white'])
    summary_container.pack(fill=tk.X, pady=20)
    summary_container.configure(relief='solid', bd=2)

    # Income section - mobile style
    income_frame = create_modern_frame(summary_container, MODERN_COLORS['white'])
    income_frame.pack(fill=tk.X, padx=25, pady=20)

    total_income = sum(float(i[1]) for i in current_entries) if current_entries else 0.0
    tk.Label(income_frame, text="Total Income:", 
            font=('Segoe UI', 18, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT)
    tk.Label(income_frame, text=f"₱{total_income:,.2f}", 
            font=('Segoe UI', 18, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['success']).pack(side=tk.RIGHT)

    # Expenses section - mobile style
    expenses_frame = create_modern_frame(summary_container, MODERN_COLORS['white'])
    expenses_frame.pack(fill=tk.X, padx=25, pady=20)

    total_expenses = sum(float(e[1]) for e in current_expenses) if current_expenses else 0.0
    tk.Label(expenses_frame, text="Total Expenses:", 
            font=('Segoe UI', 18, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT)
    tk.Label(expenses_frame, text=f"₱{total_expenses:,.2f}", 
            font=('Segoe UI', 18, 'bold'), 
            bg=MODERN_COLORS['white'], 
            fg=MODERN_COLORS['danger']).pack(side=tk.RIGHT)

    # Net total section - mobile style
    net_frame = create_modern_frame(summary_container, MODERN_COLORS['light'])
    net_frame.pack(fill=tk.X, padx=25, pady=25)
    net_frame.configure(relief='solid', bd=3)

    day_total = total_income - total_expenses
    tk.Label(net_frame, text="Net Total:", 
            font=('Segoe UI', 20, 'bold'), 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['dark']).pack(side=tk.LEFT, padx=20, pady=15)
    tk.Label(net_frame, text=f"₱{day_total:,.2f}", 
            font=('Segoe UI', 20, 'bold'), 
            bg=MODERN_COLORS['light'], 
            fg=MODERN_COLORS['success'] if day_total >= 0 else MODERN_COLORS['danger']).pack(side=tk.RIGHT, padx=20, pady=15)

    # Navigation buttons - mobile style
    button_frame = create_modern_frame(main_container, MODERN_COLORS['light'])
    button_frame.pack(pady=30)

    # Undo button - mobile style
    undo_btn = create_undo_button(button_frame, 
                                 command=lambda: [total.destroy(), navigate_back()],
                                 style='warning', width=15)
    undo_btn.pack(pady=10)

    # Back to expenses button - mobile style
    back_btn = create_modern_button(button_frame, "💸 Back to Expenses", 
                                  command=lambda:[total.destroy(), expenses_screen(day, year, month)],
                                  style='secondary', width=20)
    back_btn.pack(pady=10)

    # Finish button - mobile style
    finish_btn = create_modern_button(button_frame, "✅ Finish & Return to Calendar", 
                                    command=lambda:[total.destroy(), calendar_screen()],
                                    style='primary', width=25)
    finish_btn.pack(pady=10)

    # Sign out button - mobile style
    signout_btn = create_modern_button(button_frame, "🚪 Sign Out", 
                                      command=lambda:[total.destroy(), login_screen()],
                                      style='danger', width=20)
    signout_btn.pack(pady=5)

    # Add global undo shortcut
    add_global_undo_shortcut(total)

    total.mainloop()

# ---------------- Start the app ----------------
if __name__ == "__main__":
    splash_screen()

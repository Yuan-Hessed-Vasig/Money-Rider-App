
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import calendar
import json
import os

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
    splash = tk.Tk()
    splash.title("Money Rider")
    splash.geometry("570x700")
    splash.configure(bg="#1C1C1C")  # Dark background for rider theme

    title = tk.Label(splash, text="Money Rider 🚵", font=("Bubblegum Sans", 36, "bold"), bg="#1C1C1C", fg="white")
    title.pack(pady=50)

    login_btn = tk.Button(splash, text="Login", font=("Bubblegum Sans", 18), bg="#404040", fg="white",
                          command=lambda:[splash.destroy(), login_screen()])
    login_btn.pack(pady=10)

    create_account_btn = tk.Button(splash, text="Create Account", font=("Bubblegum Sans", 14), bg="#404040", fg="white",
                                   command=lambda:[splash.destroy(), create_account_screen()])
    create_account_btn.pack()

    splash.mainloop()

# ---------------- Create Account ----------------
def create_account_screen():
    create = tk.Tk()
    create.title("Create Account")
    create.geometry("570x700")
    create.configure(bg="#1C1C1C")

    tk.Label(create, text="Create Username", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
    username_entry = tk.Entry(create, font=("Bubblegum Sans", 14))
    username_entry.pack(pady=5)

    tk.Label(create, text="Create Password", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
    password_var = tk.StringVar()
    password_entry = tk.Entry(create, textvariable=password_var, show="*", font=("Bubblegum Sans", 14))
    password_entry.pack(pady=5)

    # Eye toggle
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈")
    eye_btn = tk.Button(create, text="👁", command=toggle_pw, bg="#404040", fg="white")
    eye_btn.pack(pady=3)

    def create_account():
        username = username_entry.get().strip()
        password = password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Fill all fields")
            return
        if username in accounts:
            messagebox.showerror("Error", "Username already exists")
            return
        accounts[username] = password
        save_accounts()
        # create user data file (empty financial_data)
        with open(user_file(username), "w") as f:
            json.dump({}, f)
        messagebox.showinfo("Success", "Account Created! Please login.")
        create.destroy()
        splash_screen()

    tk.Button(create, text="Create", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=create_account).pack(pady=20)

# ---------------- Login ----------------
def login_screen():
    login = tk.Tk()
    login.title("Login")
    login.geometry("570x700")
    login.configure(bg="#1C1C1C")

    tk.Label(login, text="Username", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
    username_entry = tk.Entry(login, font=("Bubblegum Sans", 14))
    username_entry.pack(pady=5)

    tk.Label(login, text="Password", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
    password_var = tk.StringVar()
    password_entry = tk.Entry(login, textvariable=password_var, show="*", font=("Bubblegum Sans", 14))
    password_entry.pack(pady=5)
  
    # NEW Return button
    tk.Button(login, text="Return", font=("Bubblegum Sans", 14), bg="#404040", fg="white",
              command=lambda: [login.destroy(), splash_screen()]).pack(pady=5)


    # Eye toggle for login
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈")
    eye_btn = tk.Button(login, text="👁", command=toggle_pw, bg="#404040", fg="white")
    eye_btn.pack(pady=3)

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
            messagebox.showerror("Error", "Wrong Username or Password!")

    tk.Button(login, text="Login", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=validate_login).pack(pady=20)

# ---------------- Calendar Screen (same layout/flow as original) ----------------
def calendar_screen():
    cal = tk.Tk()
    cal.title("Money Rider - Calendar")
    cal.geometry("570x700")
    cal.configure(bg="#1C1C1C")

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

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
        edit_btn = tk.Button(button_frame, text="View/Edit", font=("Bubblegum Sans", 12),
                             bg="#404040", fg="white", width=12,
                             command=lambda: [popup.destroy(), cal.destroy(), income_screen(day, current_year, current_month)])
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Close button
        close_btn = tk.Button(button_frame, text="Close", font=("Bubblegum Sans", 12),
                              bg="#404040", fg="white", width=12,
                              command=popup.destroy)
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

        cal_frame = tk.Frame(cal, bg="#1C1C1C")
        cal_frame.pack(fill=tk.BOTH, expand=True)

        # Month and year selection
        header_frame = tk.Frame(cal_frame, bg="#1C1C1C")
        header_frame.pack(pady=10)

        month_var = tk.StringVar(value=calendar.month_name[current_month])
        month_menu = ttk.Combobox(header_frame, textvariable=month_var,
                                 values=list(calendar.month_name[1:]),
                                 state="readonly",
                                 font=("Bubblegum Sans", 16),
                                 justify="center")
        month_menu.grid(row=0, column=0, padx=10, pady=10)
        month_menu.bind("<<ComboboxSelected>>", lambda e: change_month())

        year_var = tk.StringVar(value=str(current_year))
        year_menu = ttk.Combobox(header_frame, textvariable=year_var,
                                values=list(range(2020, 2031)),
                                state="readonly",
                                font=("Bubblegum Sans", 16),
                                justify="center")
        year_menu.grid(row=0, column=1, padx=10, pady=10)
        year_menu.bind("<<ComboboxSelected>>", lambda e: change_year())

        # Days of week header
        days_frame = tk.Frame(cal_frame, bg="#1C1C1C")
        days_frame.pack()

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days_of_week):
            tk.Label(days_frame, text=day, bg="#1C1C1C", fg="white",
                    font=("Bubblegum Sans", 12)).grid(row=0, column=col, padx=5, pady=5)

        # Calendar days grid
        month_cal = calendar.monthcalendar(current_year, current_month)
        for row, week in enumerate(month_cal):
            for col, day in enumerate(week):
                if day == 0:
                    # Empty space for days not in the month
                    tk.Label(days_frame, text="", bg="#1C1C1C", width=5, height=2).grid(row=row+1, column=col, padx=2, pady=2)
                    continue

                date_str = f"{current_year}-{current_month:02d}-{day:02d}"
                day_button = tk.Button(days_frame, text=str(day), bg="#E0E0E0", fg="black",
                                     font=("Bubblegum Sans", 14), width=5, height=2,
                                     command=lambda d=day: go_to_income(d))
                day_button.grid(row=row + 1, column=col, padx=2, pady=2)

                # Highlight current day
                if (day == current_date.day and
                    current_month == current_date.month and
                    current_year == current_date.year):
                    day_button.config(bg="#4CAF50", fg="white")

                # Highlight days with saved data
                if date_str in financial_data:
                    day_button.config(bg="#2196F3", fg="white")

        # Date range calculation section (keeps original behavior)
        range_frame = tk.Frame(cal_frame, bg="#1C1C1C")
        range_frame.pack(pady=20)

        tk.Label(range_frame, text="Date Range Calculator", bg="#1C1C1C", fg="white",
                font=("Bubblegum Sans", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Start date
        tk.Label(range_frame, text="From:", bg="#1C1C1C", fg="white",
                font=("Bubblegum Sans", 12)).grid(row=1, column=0, sticky="e")
        start_day = ttk.Combobox(range_frame, values=list(range(1, 32)), width=3,
                                 font=("Bubblegum Sans", 12))
        start_day.grid(row=1, column=1, sticky="w")
        start_day.set("1")

        start_month = ttk.Combobox(range_frame, values=list(calendar.month_name[1:]), width=10,
                                   font=("Bubblegum Sans", 12))
        start_month.grid(row=1, column=2, sticky="w")
        start_month.set(calendar.month_name[current_month])

        start_year = ttk.Combobox(range_frame, values=list(range(2020, 2031)), width=5,
                                  font=("Bubblegum Sans", 12))
        start_year.grid(row=1, column=3, sticky="w")
        start_year.set(str(current_year))

        # End date
        tk.Label(range_frame, text="To:", bg="#1C1C1C", fg="white",
                font=("Bubblegum Sans", 12)).grid(row=2, column=0, sticky="e")
        end_day = ttk.Combobox(range_frame, values=list(range(1, 32)), width=3,
                               font=("Bubblegum Sans", 12))
        end_day.grid(row=2, column=1, sticky="w")
        end_day.set("1")

        end_month = ttk.Combobox(range_frame, values=list(calendar.month_name[1:]), width=10,
                                 font=("Bubblegum Sans", 12))
        end_month.grid(row=2, column=2, sticky="w")
        end_month.set(calendar.month_name[current_month])

        end_year = ttk.Combobox(range_frame, values=list(range(2020, 2031)), width=5,
                                font=("Bubblegum Sans", 12))
        end_year.grid(row=2, column=3, sticky="w")
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

                # Display results
                result_window = tk.Toplevel(cal)
                result_window.title("Date Range Results")
                result_window.geometry("400x300")
                result_window.configure(bg="#1C1C1C")

                tk.Label(result_window, text=f"Date Range: {start_date_str} to {end_date_str}",
                         bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=10)

                tk.Label(result_window, text=f"Days with data: {days_with_data}",
                         bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)

                tk.Label(result_window, text=f"Total Income: ₱{total_income:,.2f}",
                         bg="#1C1C1C", fg="#4CAF50", font=("Bubblegum Sans", 12)).pack(pady=5)

                tk.Label(result_window, text=f"Total Expenses: ₱{total_expenses:,.2f}",
                         bg="#1C1C1C", fg="#F44336", font=("Bubblegum Sans", 12)).pack(pady=5)

                tk.Label(result_window, text=f"Net Total: ₱{net_total:,.2f}",
                         bg="#1C1C1C", fg="#4CAF50" if net_total >= 0 else "#F44336",
                         font=("Bubblegum Sans", 14, "bold")).pack(pady=10)

            except ValueError:
                messagebox.showerror("Error", "Invalid date selection")

        calc_button = tk.Button(range_frame, text="Calculate Range", font=("Bubblegum Sans", 12),
                                bg="#404040", fg="white", command=calculate_range)
        calc_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Navigation buttons
        nav_frame = tk.Frame(cal_frame, bg="#1C1C1C")
        nav_frame.pack(pady=10)

        tk.Button(nav_frame, text="Back", font=("Bubblegum Sans", 14), bg="#404040", fg="white",
                  command=lambda: [cal.destroy(), login_screen()]).pack(side=tk.LEFT, padx=10)

    def change_month():
        nonlocal current_month
        current_month = list(calendar.month_name).index(month_var.get())
        create_calendar_grid()

    def change_year():
        nonlocal current_year
        current_year = int(year_var.get())
        create_calendar_grid()

    create_calendar_grid()
    cal.mainloop()

# ---------------- Income Screen (keeps original layout, Edit/Delete implemented) ----------------
def income_screen(day, year, month):
    inc = tk.Tk()
    inc.title("Income")
    inc.geometry("570x700")
    inc.configure(bg="#1C1C1C")

    name_var = tk.StringVar()
    income_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Display the current date
    date_label = tk.Label(inc, text=f"Date: {year}-{month:02d}-{day:02d}",
                         bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14))
    date_label.pack(pady=10)

    # Keep Customer Name field (used as income description / typable category)
    tk.Label(inc, text="Customer Name", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
    name_entry = tk.Entry(inc, textvariable=name_var, font=("Bubblegum Sans", 14))
    name_entry.pack(pady=5)

    tk.Label(inc, text="Income", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
    income_entry = tk.Entry(inc, textvariable=income_var, font=("Bubblegum Sans", 14))
    income_entry.pack(pady=5)

    display_frame = tk.Frame(inc, bg="#1C1C1C")
    display_frame.pack(pady=10)

    # Create a frame for the header with fixed column widths
    header_frame = tk.Frame(display_frame, bg="#1C1C1C")
    header_frame.pack()

    # Header labels with fixed width
    tk.Label(header_frame, text="Customer Name".ljust(30), bg="#1C1C1C", fg="white",
             font=("Bubblegum Sans", 14)).grid(row=0, column=0, padx=5)
    tk.Label(header_frame, text="Income".rjust(10), bg="#1C1C1C", fg="white",
             font=("Bubblegum Sans", 14)).grid(row=0, column=1, padx=5)

    # Create a listbox with monospace font for alignment
    listbox = tk.Listbox(display_frame, width=45, font=("Courier New", 14),
                        bg="#404040", fg="white", justify=tk.LEFT)
    listbox.pack()

    # Populate listbox with existing entries
    for entry in current_entries:
        listbox.insert(tk.END, f"{entry[0].ljust(30)}{str(entry[1]).rjust(10)}")

    def enter_income():
        name = name_var.get().strip()
        income = income_var.get().strip()
        if not name or not income:
            messagebox.showinfo("Error", "Something's missing!")
            return

        try:
            income_val = float(income)
        except ValueError:
            messagebox.showerror("Error", "Income must be a number")
            return

        entry = (name, income_val)
        current_entries.append(entry)
        # Format with fixed width columns
        listbox.insert(tk.END, f"{name.ljust(30)}{income.rjust(10)}")
        name_var.set("")
        income_var.set("")
        # autosave to user's financial_data
        save_data(current_date_str)

    # === EDIT MODE for income ===
    def edit_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No income selected to edit")
            return
        idx = sel[0]
        old_name, old_amount = current_entries[idx]

        edit_win = tk.Toplevel(inc)
        edit_win.title("Edit Income")
        edit_win.geometry("350x220")
        edit_win.configure(bg="#1C1C1C")

        tk.Label(edit_win, text="Customer Name", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)
        e_name = tk.Entry(edit_win, font=("Bubblegum Sans", 12))
        e_name.insert(0, old_name)
        e_name.pack(pady=5)

        tk.Label(edit_win, text="Income", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)
        e_income = tk.Entry(edit_win, font=("Bubblegum Sans", 12))
        e_income.insert(0, str(old_amount))
        e_income.pack(pady=5)

        def save_edit():
            new_name = e_name.get().strip()
            new_income_str = e_income.get().strip()
            if not new_name or not new_income_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_income = float(new_income_str)
            except ValueError:
                messagebox.showerror("Error", "Income must be a number")
                return
            # Update in-memory entries and listbox
            current_entries[idx] = (new_name, new_income)
            listbox.delete(0, tk.END)
            for entry in current_entries:
                listbox.insert(tk.END, f"{entry[0].ljust(30)}{str(entry[1]).rjust(10)}")
            edit_win.destroy()
            save_data(current_date_str)

        tk.Button(edit_win, text="Save", font=("Bubblegum Sans", 12), bg="#404040", fg="white", command=save_edit).pack(pady=10)

    # Delete selected income
    def delete_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No income selected to delete")
            return
        idx = sel[0]
        current_entries.pop(idx)
        listbox.delete(idx)
        save_data(current_date_str)

    tk.Button(inc, text="Enter", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=enter_income).pack(pady=5)
    # replaced Undo/Redo buttons with Edit and Delete
    tk.Button(inc, text="Edit", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=edit_selected).pack(pady=5)
    tk.Button(inc, text="Delete", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=delete_selected).pack(pady=5)

    tk.Button(inc, text="Go to Expenses", font=("Bubblegum Sans", 14), bg="#404040", fg="white",
              command=lambda:[save_data(current_date_str), inc.destroy(), expenses_screen(day, year, month)]).pack(pady=20)

    inc.mainloop()

# ---------------- Expenses Screen (Edit/Delete + categories dropdown + Other) ----------------
def expenses_screen(day, year, month):
    exp = tk.Tk()
    exp.title("Expenses")
    exp.geometry("570x700")
    exp.configure(bg="#1C1C1C")

    expense_var = tk.StringVar()
    amount_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Display the current date
    date_label = tk.Label(exp, text=f"Date: {year}-{month:02d}-{day:02d}",
                         bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14))
    date_label.pack(pady=10)

    # Helper to show Add Expense popup with category dropdown + 'Other' option
    def add_option():
        popup = tk.Toplevel(exp)
        popup.title("Add Expense")
        popup.geometry("420x320")
        popup.configure(bg="#1C1C1C")

        tk.Label(popup, text="Category", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(popup, values=categories, textvariable=cat_var, state="readonly", font=("Bubblegum Sans", 14))
        cat_menu.pack(pady=5)
        cat_menu.set(categories[0])

        custom_var = tk.StringVar()
        custom_entry = tk.Entry(popup, textvariable=custom_var, font=("Bubblegum Sans", 14))
        # only show when Other selected
        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(pady=5)
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        tk.Label(popup, text="Amount", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 14)).pack(pady=5)
        amount_entry = tk.Entry(popup, textvariable=amount_var, font=("Bubblegum Sans", 14))
        amount_entry.pack(pady=5)

        def save_expense():
            category = cat_var.get()
            if category == "Other":
                category = custom_var.get().strip()
            amount = amount_var.get().strip()
            if not category or not amount:
                messagebox.showerror("Error", "Something's missing!")
                return
            try:
                amount_val = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return

            entry = (category, amount_val)
            current_expenses.append(entry)
            # Format with fixed width columns
            listbox.insert(tk.END, f"{category.ljust(30)}{str(amount_val).rjust(10)}")
            amount_var.set("")
            custom_var.set("")
            popup.destroy()
            save_data(current_date_str)

        tk.Button(popup, text="Save", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=save_expense).pack(pady=10)

    display_frame = tk.Frame(exp, bg="#1C1C1C")
    display_frame.pack(pady=10)

    # Create a frame for the header with fixed column widths
    header_frame = tk.Frame(display_frame, bg="#1C1C1C")
    header_frame.pack()

    # Header labels with fixed width
    tk.Label(header_frame, text="Expense".ljust(30), bg="#1C1C1C", fg="white",
             font=("Bubblegum Sans", 14)).grid(row=0, column=0, padx=5)
    tk.Label(header_frame, text="Amount".rjust(10), bg="#1C1C1C", fg="white",
             font=("Bubblegum Sans", 14)).grid(row=0, column=1, padx=5)

    # Create a listbox with monospace font for alignment
    listbox = tk.Listbox(display_frame, width=45, font=("Courier New", 14),
                        bg="#404040", fg="white", justify=tk.LEFT)
    listbox.pack()

    # Populate listbox with existing expenses
    for expense in current_expenses:
        listbox.insert(tk.END, f"{expense[0].ljust(30)}{str(expense[1]).rjust(10)}")

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

        tk.Button(edit_win, text="Save", font=("Bubblegum Sans", 12), bg="#404040", fg="white", command=save_edit).pack(pady=10)

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

    tk.Button(exp, text="Add Expenses", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=add_option).pack(pady=5)
    # replaced Undo/Redo with Edit & Delete for expenses
    tk.Button(exp, text="Edit", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=edit_selected).pack(pady=5)
    tk.Button(exp, text="Delete", font=("Bubblegum Sans", 14), bg="#404040", fg="white", command=delete_selected).pack(pady=5)

    tk.Button(exp, text="Show Totals", font=("Bubblegum Sans", 14), bg="#404040", fg="white",
              command=lambda:[save_data(current_date_str), exp.destroy(), total_screen(day, year, month)]).pack(pady=20)

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
    total = tk.Tk()
    total.title("Total")
    total.geometry("570x700")
    total.configure(bg="#1C1C1C")

    # Main frame
    main_frame = tk.Frame(total, bg="#1C1C1C")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Title
    tk.Label(main_frame, text="Financial Summary", bg="#1C1C1C", fg="white",
            font=("Bubblegum Sans", 24, "bold")).pack(pady=20)

    # Date display
    date_str = f"{year}-{month:02d}-{day:02d}"
    tk.Label(main_frame, text=f"Date: {date_str}", bg="#1C1C1C", fg="white",
            font=("Bubblegum Sans", 14)).pack()

    # Summary frame
    summary_frame = tk.Frame(main_frame, bg="#2C2C2C", bd=2, relief=tk.RIDGE)
    summary_frame.pack(fill=tk.X, padx=20, pady=10)

    # Income section
    income_frame = tk.Frame(summary_frame, bg="#2C2C2C")
    income_frame.pack(fill=tk.X, padx=10, pady=10)

    total_income = sum(float(i[1]) for i in current_entries) if current_entries else 0.0
    tk.Label(income_frame, text="Total Income:", bg="#2C2C2C", fg="white",
            font=("Bubblegum Sans", 16)).pack(side=tk.LEFT, padx=10)
    tk.Label(income_frame, text=f"₱{total_income:,.2f}", bg="#2C2C2C", fg="#4CAF50",
            font=("Bubblegum Sans", 16, "bold")).pack(side=tk.RIGHT, padx=10)

    # Expenses section
    expenses_frame = tk.Frame(summary_frame, bg="#2C2C2C")
    expenses_frame.pack(fill=tk.X, padx=10, pady=10)

    total_expenses = sum(float(e[1]) for e in current_expenses) if current_expenses else 0.0
    tk.Label(expenses_frame, text="Total Expenses:", bg="#2C2C2C", fg="white",
            font=("Bubblegum Sans", 16)).pack(side=tk.LEFT, padx=10)
    tk.Label(expenses_frame, text=f"₱{total_expenses:,.2f}", bg="#2C2C2C", fg="#F44336",
            font=("Bubblegum Sans", 16, "bold")).pack(side=tk.RIGHT, padx=10)

    # Net total section
    net_frame = tk.Frame(summary_frame, bg="#2C2C2C")
    net_frame.pack(fill=tk.X, padx=10, pady=20)

    day_total = total_income - total_expenses
    tk.Label(net_frame, text="Net Total:", bg="#2C2C2C", fg="white",
            font=("Bubblegum Sans", 18)).pack(side=tk.LEFT, padx=10)
    tk.Label(net_frame, text=f"₱{day_total:,.2f}", bg="#2C2C2C",
            fg="#4CAF50" if day_total >= 0 else "#F44336",
            font=("Bubblegum Sans", 18, "bold")).pack(side=tk.RIGHT, padx=10)

    # Navigation buttons
    button_frame = tk.Frame(main_frame, bg="#1C1C1C")
    button_frame.pack(pady=30)

    back_btn = tk.Button(button_frame, text="Back", font=("Bubblegum Sans", 14),
                        bg="#404040", fg="white", width=10,
                        command=lambda:[total.destroy(), expenses_screen(day, year, month)])
    back_btn.pack(side=tk.LEFT, padx=10)

    end_btn = tk.Button(button_frame, text="End", font=("Bubblegum Sans", 14),
                       bg="#404040", fg="white", width=10,
                       command=lambda:[total.destroy(), calendar_screen()])
    end_btn.pack(side=tk.LEFT, padx=10)

    total.mainloop()

# ---------------- Start the app ----------------
if __name__ == "__main__":
    splash_screen()

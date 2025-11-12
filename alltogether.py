import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import requests
from datetime import datetime, timedelta

# =========================================
# DATABASE INITIALIZATION
# =========================================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# --- Books Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT UNIQUE,
    title TEXT,
    author TEXT,
    publisher TEXT,
    publication_year INTEGER,
    category TEXT,
    description TEXT,
    cover_image_url TEXT,
    page_count INTEGER,
    language TEXT,
    total_copies INTEGER,
    available_copies INTEGER,
    shelf_location TEXT
)
''')

# --- Members Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_number TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    join_date DATE,
    membership_type TEXT,
    status TEXT
)
''')

# --- Transactions Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    book_id INTEGER,
    issue_date DATE,
    due_date DATE,
    return_date DATE,
    fine_amount REAL,
    status TEXT,
    FOREIGN KEY(member_id) REFERENCES Members(member_id),
    FOREIGN KEY(book_id) REFERENCES Books(book_id)
)
''')

# --- Book Reviews Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Book_Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    rating INTEGER,
    review_text TEXT,
    review_date DATE,
    FOREIGN KEY(book_id) REFERENCES Books(book_id),
    FOREIGN KEY(member_id) REFERENCES Members(member_id)
)
''')
conn.commit()

# =========================================
# MAIN APPLICATION
# =========================================
class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Library Management System")
        self.geometry("950x700")
        self.config(bg="#f5f5f5")

        tk.Label(self, text="📘 Library Management Dashboard",
                 font=("Arial", 22, "bold"), bg="#283593", fg="white").pack(fill="x", pady=10)

        # Dashboard
        self.create_dashboard_section()
        # Book Management
        self.create_book_management_section()
        # Member Management
        self.create_member_management_section()
        # Transaction Management
        self.create_transaction_management_section()

    # =========================================
    # DASHBOARD
    # =========================================
    def create_dashboard_section(self):
        frame = tk.LabelFrame(self, text="Dashboard", font=("Arial", 14, "bold"),
                              padx=15, pady=10, bg="#e8eaf6")
        frame.pack(fill="x", padx=20, pady=10)

        stats_label = tk.Label(frame, text="📊 Key Statistics:\n• Total Books: ...\n• Total Members: ...\n• Books Issued: ...",
                               font=("Arial", 12), justify="left", bg="#e8eaf6")
        stats_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        quick_actions = tk.Frame(frame, bg="#e8eaf6")
        quick_actions.grid(row=0, column=1, padx=20)
        ttk.Button(quick_actions, text="Add Book", command=self.open_add_book_window).grid(row=0, column=0, padx=8)
        ttk.Button(quick_actions, text="Issue Book", command=self.open_issue_book_window).grid(row=0, column=1, padx=8)
        ttk.Button(quick_actions, text="Return Book", command=self.open_return_book_window).grid(row=0, column=2, padx=8)

        # Recent Transactions
        tk.Label(frame, text="🕒 Recent Transactions", font=("Arial", 12, "bold"), bg="#e8eaf6").grid(row=1, column=0, sticky="w", pady=10)
        self.transactions_list = tk.Listbox(frame, width=50, height=5)
        self.transactions_list.grid(row=2, column=0, pady=5)
        # Popular Books
        tk.Label(frame, text="⭐ Popular Books", font=("Arial", 12, "bold"), bg="#e8eaf6").grid(row=1, column=1, sticky="w", pady=10)
        self.popular_list = tk.Listbox(frame, width=40, height=5)
        self.popular_list.grid(row=2, column=1, pady=5)

    # =========================================
    # BOOK MANAGEMENT
    # =========================================
    def create_book_management_section(self):
        frame = tk.LabelFrame(self, text="Book Management (API Integrated)", font=("Arial", 14, "bold"),
                              padx=15, pady=10, bg="#e3f2fd")
        frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(frame, text="Add New Book (ISBN Lookup)", command=self.open_add_book_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="Update Book Details", command=self.open_update_book_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="Search Books", command=self.open_search_books_window).pack(fill="x", pady=4)

    # =========================================
    # MEMBER MANAGEMENT
    # =========================================
    def create_member_management_section(self):
        frame = tk.LabelFrame(self, text="Member Management", font=("Arial", 14, "bold"),
                              padx=15, pady=10, bg="#f3e5f5")
        frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(frame, text="Register New Member", command=self.open_register_member_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="Update Member Info", command=self.open_update_member_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="View Borrow History", command=self.open_borrow_history_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="Send Email Notifications", command=self.open_email_notify_window).pack(fill="x", pady=4)

    # =========================================
    # TRANSACTION MANAGEMENT
    # =========================================
    def create_transaction_management_section(self):
        frame = tk.LabelFrame(self, text="Transaction Management", font=("Arial", 14, "bold"),
                              padx=15, pady=10, bg="#fff3e0")
        frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(frame, text="Issue Book", command=self.open_issue_book_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="Return Book", command=self.open_return_book_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="View All Transactions", command=self.open_view_transactions_window).pack(fill="x", pady=4)
        ttk.Button(frame, text="Send Due Reminders", command=self.open_send_reminder_window).pack(fill="x", pady=4)

    # =========================================
    # NEW WINDOWS / POPUPS
    # =========================================
    def _open_popup(self, title, text):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("500x350")
        popup.config(bg="white")
        tk.Label(popup, text=title, font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        tk.Message(popup, text=text, width=450, font=("Arial", 12), bg="white").pack(padx=20, pady=10)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=15)

    def open_add_book_window(self):
        self._open_popup("Add Book", "ISBN Lookup -> Fetch details from Google Books/Open Library APIs")

    def open_update_book_window(self):
        self._open_popup("Update Book", "Update book details and availability.")

    def open_search_books_window(self):
        self._open_popup("Search Books", "Search by title, author, ISBN, category.\nShow book cover and availability.")

    def open_register_member_window(self):
        self._open_popup("Register Member", "Register a new library member.")

    def open_update_member_window(self):
        self._open_popup("Update Member Info", "Update member personal/contact details.")

    def open_borrow_history_window(self):
        self._open_popup("Borrowing History", "View borrowing and return history of members.")

    def open_email_notify_window(self):
        self._open_popup("Email Notifications", "Send email reminders or notifications to members.")

    def open_issue_book_window(self):
        self._open_popup("Issue Book", "Record a book issue transaction and update availability.")

    def open_return_book_window(self):
        self._open_popup("Return Book", "Record a book return transaction, calculate fines if overdue.")

    def open_view_transactions_window(self):
        self._open_popup("All Transactions", "View all book issue/return transactions.")

    def open_send_reminder_window(self):
        self._open_popup("Send Due Reminders", "Send due date reminders via Email/SMS API.")

# =========================================
# RUN APPLICATION
# =========================================
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()

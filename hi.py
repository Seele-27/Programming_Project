import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import requests

# ====================================================
#   LIBRARY MANAGEMENT SYSTEM - ENHANCED WITH PLACEHOLDERS
# ====================================================

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Library Management System")
        self.geometry("1000x850")
        self.config(bg="#f5f5f5")

        # --- Title ---
        tk.Label(self, text="📘 Library Management Dashboard", font=("Arial", 22, "bold"),
                 bg="#283593", fg="white").pack(fill="x", pady=10)

        # --- Sections ---
        self.create_dashboard_section()
        self.create_book_management_section()
        self.create_member_management_section()
        self.create_transaction_management_section()

        # In-memory data
        self.transactions = []

    # ====================================================
    #   DASHBOARD SECTION
    # ====================================================
    def create_dashboard_section(self):
        dashboard_frame = tk.LabelFrame(self, text="Dashboard", font=("Arial", 14, "bold"),
                                        padx=15, pady=10, bg="#e8eaf6")
        dashboard_frame.pack(fill="x", padx=20, pady=10)

        stats_label = tk.Label(
            dashboard_frame,
            text="📊 Key Statistics:\n• Total Books: 1240\n• Total Members: 320\n• Books Issued: 410",
            font=("Arial", 12),
            justify="left",
            bg="#e8eaf6"
        )
        stats_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        quick_actions = tk.Frame(dashboard_frame, bg="#e8eaf6")
        quick_actions.grid(row=0, column=1, padx=20)
        ttk.Button(quick_actions, text="Add Book", command=self.open_add_book_window).grid(row=0, column=0, padx=8)
        ttk.Button(quick_actions, text="Issue Book", command=self.open_issue_book_window).grid(row=0, column=1, padx=8)
        ttk.Button(quick_actions, text="Return Book", command=self.open_return_book_window).grid(row=0, column=2, padx=8)

        tk.Label(dashboard_frame, text="🕒 Recent Transactions", font=("Arial", 12, "bold"),
                 bg="#e8eaf6").grid(row=1, column=0, sticky="w", pady=10)
        self.transactions_list = tk.Listbox(dashboard_frame, width=50, height=5)
        self.transactions_list.grid(row=2, column=0, pady=5)
        for txn in ["John borrowed '1984'", "Emily returned 'Harry Potter'", "Luke borrowed 'To Kill a Mockingbird'"]:
            self.transactions_list.insert(tk.END, txn)

        tk.Label(dashboard_frame, text="⭐ Popular Books", font=("Arial", 12, "bold"),
                 bg="#e8eaf6").grid(row=1, column=1, sticky="w", pady=10)
        self.popular_list = tk.Listbox(dashboard_frame, width=40, height=5)
        self.popular_list.grid(row=2, column=1, pady=5)
        for book in ["The Hobbit", "Pride and Prejudice", "The Great Gatsby", "1984"]:
            self.popular_list.insert(tk.END, book)

    # ====================================================
    #   BOOK MANAGEMENT SECTION
    # ====================================================
    def create_book_management_section(self):
        book_frame = tk.LabelFrame(self, text="Book Management (API Integrated)",
                                   font=("Arial", 14, "bold"), padx=15, pady=10, bg="#e3f2fd")
        book_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(book_frame, text="Add New Book (ISBN Lookup)", command=self.open_add_book_window).pack(fill="x", pady=4)
        ttk.Button(book_frame, text="Update Book Details", command=self.open_update_book_window).pack(fill="x", pady=4)
        ttk.Button(book_frame, text="Search Books", command=self.open_search_books_window).pack(fill="x", pady=4)

    # ====================================================
    #   MEMBER MANAGEMENT SECTION
    # ====================================================
    def create_member_management_section(self):
        member_frame = tk.LabelFrame(self, text="Member Management",
                                     font=("Arial", 14, "bold"), padx=15, pady=10, bg="#f3e5f5")
        member_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(member_frame, text="Register New Member", command=self.open_register_member_window).pack(fill="x", pady=4)
        ttk.Button(member_frame, text="Update Member Information", command=self.open_update_member_window).pack(fill="x", pady=4)
        ttk.Button(member_frame, text="View Borrowing History", command=self.open_borrow_history_window).pack(fill="x", pady=4)
        ttk.Button(member_frame, text="Send Email Notifications", command=self.open_email_notify_window).pack(fill="x", pady=4)

    # ====================================================
    #   TRANSACTION MANAGEMENT SECTION
    # ====================================================
    def create_transaction_management_section(self):
        txn_frame = tk.LabelFrame(self, text="Transaction Management", font=("Arial", 14, "bold"),
                                  padx=15, pady=10, bg="#fff3e0")
        txn_frame.pack(fill="both", expand=True, padx=20, pady=10)

        button_frame = tk.Frame(txn_frame, bg="#fff3e0")
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Issue Book", command=self.open_issue_book_window).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Return Book", command=self.open_return_book_window).pack(side="left", padx=10)
        ttk.Button(button_frame, text="View All Transactions", command=self.refresh_transaction_table).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Send Due Date Reminders", command=self.send_due_reminders).pack(side="left", padx=10)

        columns = ("member", "book", "issue_date", "due_date", "return_date", "fine")
        self.tree = ttk.Treeview(txn_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True, pady=10)

    # ====================================================
    #   POPUP WINDOWS WITH PLACEHOLDERS
    # ====================================================

    # --- Add Book ---
    def open_add_book_window(self):
        win = tk.Toplevel(self)
        win.title("📕 Add New Book")
        win.geometry("400x400")
        win.config(bg="white")

        tk.Label(win, text="Enter Book Details", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        fields = ["ISBN", "Title", "Author", "Genre", "Publisher", "Year"]
        entries = {}
        for f in fields:
            tk.Label(win, text=f + ":", bg="white").pack(anchor="w", padx=20)
            e = tk.Entry(win, width=35)
            e.pack(pady=3)
            entries[f] = e

        def save_book():
            info = {k: v.get() for k, v in entries.items()}
            messagebox.showinfo("Saved", f"Book added (placeholder):\n\n{info}")
            win.destroy()

        ttk.Button(win, text="Save", command=save_book).pack(pady=10)

    # --- Update Book ---
    def open_update_book_window(self):
        win = tk.Toplevel(self)
        win.title("📗 Update Book Details")
        win.geometry("400x400")
        win.config(bg="white")

        tk.Label(win, text="Update Book Information", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        fields = ["ISBN", "New Title", "New Author", "Availability Status"]
        entries = {}
        for f in fields:
            tk.Label(win, text=f + ":", bg="white").pack(anchor="w", padx=20)
            e = tk.Entry(win, width=35)
            e.pack(pady=3)
            entries[f] = e

        def update_book():
            info = {k: v.get() for k, v in entries.items()}
            messagebox.showinfo("Updated", f"Book updated (placeholder):\n\n{info}")
            win.destroy()

        ttk.Button(win, text="Update", command=update_book).pack(pady=10)

    # --- Search Books ---
    def open_search_books_window(self):
        win = tk.Toplevel(self)
        win.title("🔍 Search Books")
        win.geometry("400x300")
        win.config(bg="white")

        tk.Label(win, text="Search for Books", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(win, text="Search by (Title / Author / ISBN):", bg="white").pack()
        query = tk.Entry(win, width=35)
        query.pack(pady=5)

        def search_book():
            messagebox.showinfo("Search Result", f"Search results for: '{query.get()}' (placeholder)")

        ttk.Button(win, text="Search", command=search_book).pack(pady=10)

    # --- Register Member ---
    def open_register_member_window(self):
        win = tk.Toplevel(self)
        win.title("👤 Register New Member")
        win.geometry("400x400")
        win.config(bg="white")

        tk.Label(win, text="Enter Member Information", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        fields = ["Member ID", "Full Name", "Email", "Phone", "Address"]
        entries = {}
        for f in fields:
            tk.Label(win, text=f + ":", bg="white").pack(anchor="w", padx=20)
            e = tk.Entry(win, width=35)
            e.pack(pady=3)
            entries[f] = e

        def register_member():
            info = {k: v.get() for k, v in entries.items()}
            messagebox.showinfo("Registered", f"Member registered (placeholder):\n\n{info}")
            win.destroy()

        ttk.Button(win, text="Save", command=register_member).pack(pady=10)

    # --- Update Member ---
    def open_update_member_window(self):
        win = tk.Toplevel(self)
        win.title("👥 Update Member Information")
        win.geometry("400x350")
        win.config(bg="white")

        tk.Label(win, text="Update Member Information", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        fields = ["Member ID", "New Email", "New Phone", "New Address"]
        entries = {}
        for f in fields:
            tk.Label(win, text=f + ":", bg="white").pack(anchor="w", padx=20)
            e = tk.Entry(win, width=35)
            e.pack(pady=3)
            entries[f] = e

        def update_member():
            info = {k: v.get() for k, v in entries.items()}
            messagebox.showinfo("Updated", f"Member updated (placeholder):\n\n{info}")
            win.destroy()

        ttk.Button(win, text="Update", command=update_member).pack(pady=10)

    # --- Other Existing Popups ---
    def open_borrow_history_window(self): self._open_popup("Borrow History", "View member borrowing history.")
    def open_email_notify_window(self): self._open_popup("Email Notifications", "Send email reminders to members.")

    # ====================================================
    #   ISSUE / RETURN BOOK WINDOWS (unchanged)
    # ====================================================
    def open_issue_book_window(self):
        win = tk.Toplevel(self)
        win.title("📗 Issue Book")
        win.geometry("400x350")

        tk.Label(win, text="Member Name:").pack(pady=5)
        member = tk.Entry(win, width=30)
        member.pack()

        tk.Label(win, text="Book Title:").pack(pady=5)
        book = tk.Entry(win, width=30)
        book.pack()

        tk.Label(win, text="Issue Date (YYYY-MM-DD):").pack(pady=5)
        issue = tk.Entry(win, width=30)
        issue.insert(0, datetime.now().strftime("%Y-%m-%d"))
        issue.pack()

        tk.Label(win, text="Due Date (YYYY-MM-DD):").pack(pady=5)
        due = tk.Entry(win, width=30)
        due.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        due.pack()

        def save_issue():
            data = {"member": member.get(), "book": book.get(),
                    "issue_date": issue.get(), "due_date": due.get(),
                    "return_date": None, "fine": 0}
            self.transactions.append(data)
            self.refresh_transaction_table()
            messagebox.showinfo("Success", "Book issued successfully!")
            win.destroy()

        ttk.Button(win, text="Save", command=save_issue).pack(pady=15)

    def open_return_book_window(self):
        win = tk.Toplevel(self)
        win.title("📘 Return Book")
        win.geometry("400x300")

        tk.Label(win, text="Member Name:").pack(pady=5)
        member = tk.Entry(win, width=30)
        member.pack()

        tk.Label(win, text="Book Title:").pack(pady=5)
        book = tk.Entry(win, width=30)
        book.pack()

        tk.Label(win, text="Return Date (YYYY-MM-DD):").pack(pady=5)
        return_date = tk.Entry(win, width=30)
        return_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        return_date.pack()

        def process_return():
            fine = 0
            today = datetime.now().date()
            for txn in self.transactions:
                if txn["member"] == member.get() and txn["book"] == book.get() and txn["return_date"] is None:
                    due = datetime.strptime(txn["due_date"], "%Y-%m-%d").date()
                    if today > due:
                        fine = (today - due).days * 1
                    txn["return_date"] = return_date.get()
                    txn["fine"] = fine
                    messagebox.showinfo("Returned", f"Book returned.\nFine: ${fine}")
                    break
            else:
                messagebox.showerror("Error", "No matching record found.")
            self.refresh_transaction_table()
            win.destroy()

        ttk.Button(win, text="Process Return", command=process_return).pack(pady=15)

    # ====================================================
    #   TRANSACTION UTILITIES
    # ====================================================
    def refresh_transaction_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for txn in self.transactions:
            self.tree.insert("", "end", values=(
                txn["member"], txn["book"], txn["issue_date"],
                txn["due_date"], txn["return_date"], f"${txn['fine']}"
            ))

    def send_due_reminders(self):
        today = datetime.now().date()
        overdue = [t for t in self.transactions if not t["return_date"]
                   and datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today]
        if not overdue:
            messagebox.showinfo("Reminders", "No overdue books.")
            return
        msg = "\n".join([f"{t['member']} - '{t['book']}' (Due: {t['due_date']})" for t in overdue])
        messagebox.showinfo("Overdue Reminders Sent", f"Reminders sent to:\n\n{msg}")

    def _open_popup(self, title, text):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("400x300")
        popup.config(bg="white")
        tk.Label(popup, text=title, font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        tk.Message(popup, text=text, width=350, font=("Arial", 12), bg="white").pack(padx=20, pady=10)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=15)


# ====================================================
#   RUN APP
# ====================================================
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()

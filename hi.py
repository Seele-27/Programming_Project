import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Library Management System")
        self.geometry("700x500")
        self.config(bg="#f5f5f5")

        tk.Label(
            self,
            text="📘 Library Management System",
            font=("Arial", 22, "bold"),
            bg="#283593", fg="white"
        ).pack(fill="x", pady=10)

        tk.Label(
            self,
            text="Select a section to manage:",
            font=("Arial", 14),
            bg="#f5f5f5"
        ).pack(pady=20)

        # --- Navigation Buttons ---
        ttk.Button(self, text="📊 Dashboard", command=self.open_dashboard_window, width=30).pack(pady=10)
        ttk.Button(self, text="📚 Book Management", command=self.open_book_management_window, width=30).pack(pady=10)
        ttk.Button(self, text="👥 Member Management", command=self.open_member_management_window, width=30).pack(pady=10)
        ttk.Button(self, text="💼 Transaction Management", command=self.open_transaction_management_window, width=30).pack(pady=10)

        self.transactions = []  # shared data between windows

    # ====================================================
    #   DASHBOARD WINDOW
    # ====================================================
    def open_dashboard_window(self):
        win = tk.Toplevel(self)
        win.title("📊 Dashboard")
        win.geometry("800x600")
        win.config(bg="#e8eaf6")

        tk.Label(win, text="📊 Library Dashboard", font=("Arial", 18, "bold"), bg="#283593", fg="white").pack(fill="x", pady=5)

        tk.Label(
            win,
            text="📈 Key Statistics:\n• Total Books: 1240\n• Total Members: 320\n• Books Issued: 410",
            font=("Arial", 12),
            bg="#e8eaf6", justify="left"
        ).pack(pady=10)

        ttk.Button(win, text="Add Book", command=self.open_add_book_window).pack(pady=5)
        ttk.Button(win, text="Issue Book", command=self.open_issue_book_window).pack(pady=5)
        ttk.Button(win, text="Return Book", command=self.open_return_book_window).pack(pady=5)

        tk.Label(win, text="🕒 Recent Transactions", font=("Arial", 12, "bold"), bg="#e8eaf6").pack(pady=10)
        listbox = tk.Listbox(win, width=60, height=5)
        listbox.pack()
        for txn in ["John borrowed '1984'", "Emily returned 'Harry Potter'", "Luke borrowed 'To Kill a Mockingbird'"]:
            listbox.insert(tk.END, txn)

    # ====================================================
    #   BOOK MANAGEMENT WINDOW
    # ====================================================
    def open_book_management_window(self):
        win = tk.Toplevel(self)
        win.title("📚 Book Management")
        win.geometry("700x600")
        win.config(bg="#e3f2fd")

        tk.Label(win, text="📚 Book Management", font=("Arial", 18, "bold"), bg="#1976d2", fg="white").pack(fill="x", pady=5)
        ttk.Button(win, text="Add New Book", command=self.open_add_book_window).pack(fill="x", pady=5)
        ttk.Button(win, text="Update Book Details", command=self.open_update_book_window).pack(fill="x", pady=5)
        ttk.Button(win, text="Search Books", command=self.open_search_books_window).pack(fill="x", pady=5)

    # ====================================================
    #   MEMBER MANAGEMENT WINDOW
    # ====================================================
    def open_member_management_window(self):
        win = tk.Toplevel(self)
        win.title("👥 Member Management")
        win.geometry("700x600")
        win.config(bg="#f3e5f5")

        tk.Label(win, text="👥 Member Management", font=("Arial", 18, "bold"), bg="#8e24aa", fg="white").pack(fill="x", pady=5)
        ttk.Button(win, text="Register New Member", command=self.open_register_member_window).pack(fill="x", pady=5)
        ttk.Button(win, text="Update Member Info", command=self.open_update_member_window).pack(fill="x", pady=5)
        ttk.Button(win, text="View Borrowing History", command=self.open_borrow_history_window).pack(fill="x", pady=5)
        ttk.Button(win, text="Send Email Notifications", command=self.open_email_notify_window).pack(fill="x", pady=5)

    # ====================================================
    #   TRANSACTION MANAGEMENT WINDOW
    # ====================================================
    def open_transaction_management_window(self):
        win = tk.Toplevel(self)
        win.title("💼 Transaction Management")
        win.geometry("900x600")
        win.config(bg="#fff3e0")

        tk.Label(win, text="💼 Transaction Management", font=("Arial", 18, "bold"), bg="#ef6c00", fg="white").pack(fill="x", pady=5)

        columns = ("member", "book", "issue_date", "due_date", "return_date", "fine")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=130, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)

        def refresh():
            for row in tree.get_children():
                tree.delete(row)
            for txn in self.transactions:
                tree.insert("", "end", values=(
                    txn["member"], txn["book"], txn["issue_date"],
                    txn["due_date"], txn["return_date"], f"${txn['fine']}"
                ))

        ttk.Button(win, text="Issue Book", command=self.open_issue_book_window).pack(side="left", padx=10, pady=10)
        ttk.Button(win, text="Return Book", command=self.open_return_book_window).pack(side="left", padx=10, pady=10)
        ttk.Button(win, text="Refresh Table", command=refresh).pack(side="left", padx=10, pady=10)

    # ====================================================
    #   POPUPS (reused from your code)
    # ====================================================
    def open_add_book_window(self):
        self._popup_form("📕 Add New Book", ["ISBN", "Title", "Author", "Genre", "Publisher", "Year"], "Book added (placeholder)")

    def open_update_book_window(self):
        self._popup_form("📗 Update Book", ["ISBN", "New Title", "New Author", "Availability"], "Book updated (placeholder)")

    def open_search_books_window(self):
        self._popup_form("🔍 Search Books", ["Title / Author / ISBN"], "Search results (placeholder)")

    def open_register_member_window(self):
        self._popup_form("👤 Register Member", ["Member ID", "Full Name", "Email", "Phone", "Address"], "Member registered (placeholder)")

    def open_update_member_window(self):
        self._popup_form("👥 Update Member Info", ["Member ID", "New Email", "New Phone", "New Address"], "Member updated (placeholder)")

    def open_borrow_history_window(self):
        self._open_popup("Borrow History", "View member borrowing history.")

    def open_email_notify_window(self):
        self._open_popup("Email Notifications", "Send email reminders to members.")

    # ====================================================
    #   ISSUE / RETURN BOOK WINDOWS
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
        tk.Label(win, text="Issue Date:").pack(pady=5)
        issue = tk.Entry(win, width=30)
        issue.insert(0, datetime.now().strftime("%Y-%m-%d"))
        issue.pack()
        tk.Label(win, text="Due Date:").pack(pady=5)
        due = tk.Entry(win, width=30)
        due.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        due.pack()

        def save():
            data = {"member": member.get(), "book": book.get(),
                    "issue_date": issue.get(), "due_date": due.get(),
                    "return_date": None, "fine": 0}
            self.transactions.append(data)
            messagebox.showinfo("Success", "Book issued successfully!")
            win.destroy()

        ttk.Button(win, text="Save", command=save).pack(pady=15)

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
        tk.Label(win, text="Return Date:").pack(pady=5)
        return_date = tk.Entry(win, width=30)
        return_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        return_date.pack()

        def process():
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
            win.destroy()

        ttk.Button(win, text="Process Return", command=process).pack(pady=15)

    # ====================================================
    #   UTILITY POPUPS
    # ====================================================
    def _popup_form(self, title, fields, success_msg):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("400x400")
        win.config(bg="white")
        tk.Label(win, text=title, font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        entries = {}
        for f in fields:
            tk.Label(win, text=f + ":", bg="white").pack(anchor="w", padx=20)
            e = tk.Entry(win, width=35)
            e.pack(pady=3)
            entries[f] = e
        def submit():
            info = {k: v.get() for k, v in entries.items()}
            messagebox.showinfo("Saved", f"{success_msg}:\n\n{info}")
            win.destroy()
        ttk.Button(win, text="Save", command=submit).pack(pady=10)

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

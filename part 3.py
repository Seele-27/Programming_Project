import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import requests

# ====================================================
#   LIBRARY MANAGEMENT SYSTEM WITH API INTEGRATION
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
            text="📊 Key Statistics:\n• Total Books: \n• Total Members: \n• Books Issued: ",
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
    #   POPUP WINDOWS (WITH API INTEGRATION)
    # ====================================================

    def open_add_book_window(self):
        win = tk.Toplevel(self)
        win.title("📕 Add New Book (ISBN Lookup)")
        win.geometry("420x500")
        win.config(bg="white")

        tk.Label(win, text="Enter ISBN (Auto-fetch details):", font=("Arial", 12), bg="white").pack(pady=5)
        isbn_entry = tk.Entry(win, width=30)
        isbn_entry.pack(pady=5)

        fields = ["Title", "Author", "Genre", "Publisher", "Year", "Description"]
        entries = {f: tk.Entry(win, width=40) for f in fields}

        for f, e in entries.items():
            tk.Label(win, text=f + ":", bg="white").pack(anchor="w", padx=20)
            e.pack(pady=2)

        def fetch_book_data():
            isbn = isbn_entry.get().strip()
            if not isbn:
                messagebox.showerror("Error", "Please enter an ISBN.")
                return

            # Try Google Books API
            g_api = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            try:
                res = requests.get(g_api)
                data = res.json()
                if "items" in data:
                    info = data["items"][0]["volumeInfo"]
                    entries["Title"].delete(0, tk.END)
                    entries["Title"].insert(0, info.get("title", ""))
                    entries["Author"].delete(0, tk.END)
                    entries["Author"].insert(0, ", ".join(info.get("authors", [])))
                    entries["Genre"].delete(0, tk.END)
                    entries["Genre"].insert(0, ", ".join(info.get("categories", [])))
                    entries["Publisher"].delete(0, tk.END)
                    entries["Publisher"].insert(0, info.get("publisher", ""))
                    entries["Year"].delete(0, tk.END)
                    entries["Year"].insert(0, info.get("publishedDate", ""))
                    entries["Description"].delete(0, tk.END)
                    entries["Description"].insert(0, info.get("description", "")[:100])
                    messagebox.showinfo("Success", "Book details fetched from Google Books API.")
                    return
            except Exception:
                pass

            # Fallback: Open Library API
            ol_api = f"https://openlibrary.org/isbn/{isbn}.json"
            try:
                res = requests.get(ol_api)
                if res.status_code == 200:
                    info = res.json()
                    entries["Title"].insert(0, info.get("title", ""))
                    entries["Year"].insert(0, info.get("publish_date", ""))
                    messagebox.showinfo("Success", "Book details fetched from Open Library API.")
                else:
                    messagebox.showwarning("Not Found", "No data found for this ISBN.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch data: {e}")

        ttk.Button(win, text="Fetch Details", command=fetch_book_data).pack(pady=10)

        def save_book():
            info = {k: v.get() for k, v in entries.items()}
            messagebox.showinfo("Saved", f"Book added:\n\n{info}")
            win.destroy()

        ttk.Button(win, text="Save Book", command=save_book).pack(pady=10)

    # --- Other Popups remain same (simplified) ---
    def open_update_book_window(self): self._open_popup("Update Book Details", "Edit existing book info.")
    def open_search_books_window(self): self._open_popup("Search Books", "Search by title, author, or ISBN.")
    def open_register_member_window(self): self._open_popup("Register Member", "Register a new library member.")
    def open_update_member_window(self): self._open_popup("Update Member", "Update existing member information.")
    def open_borrow_history_window(self): self._open_popup("Borrow History", "View member borrowing history.")

    # --- Email/SMS API Simulation ---
    def open_email_notify_window(self):
        win = tk.Toplevel(self)
        win.title("📩 Send Notifications")
        win.geometry("400x300")
        win.config(bg="white")

        tk.Label(win, text="Enter Member Email:", bg="white").pack(pady=5)
        email = tk.Entry(win, width=35)
        email.pack(pady=5)

        tk.Label(win, text="Message:", bg="white").pack(pady=5)
        msg_box = tk.Text(win, width=40, height=5)
        msg_box.pack(pady=5)

        def send_message():
            messagebox.showinfo("Sent", f"Notification sent to {email.get()} (simulated).")

        ttk.Button(win, text="Send", command=send_message).pack(pady=10)

    # ====================================================
    #   ISSUE / RETURN / TRANSACTION
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

        def save_issue():
            txn = {
                "member": member.get(),
                "book": book.get(),
                "issue_date": issue.get(),
                "due_date": due.get(),
                "return_date": None,
                "fine": 0
            }
            self.transactions.append(txn)
            self.refresh_transaction_table()
            messagebox.showinfo("Issued", "Book issued successfully.")
            win.destroy()

        ttk.Button(win, text="Save", command=save_issue).pack(pady=10)

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
        ret = tk.Entry(win, width=30)
        ret.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ret.pack()

        def process_return():
            fine = 0
            today = datetime.now().date()
            for txn in self.transactions:
                if txn["member"] == member.get() and txn["book"] == book.get() and not txn["return_date"]:
                    due = datetime.strptime(txn["due_date"], "%Y-%m-%d").date()
                    if today > due:
                        fine = (today - due).days
                    txn["return_date"] = ret.get()
                    txn["fine"] = fine
                    break
            self.refresh_transaction_table()
            messagebox.showinfo("Returned", f"Book returned. Fine: ${fine}")
            win.destroy()

        ttk.Button(win, text="Return", command=process_return).pack(pady=15)

    def refresh_transaction_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.transactions:
            self.tree.insert("", "end", values=(
                t["member"], t["book"], t["issue_date"], t["due_date"],
                t["return_date"], f"${t['fine']}"
            ))

    def send_due_reminders(self):
        today = datetime.now().date()
        overdue = [t for t in self.transactions if not t["return_date"] and datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today]
        if overdue:
            msg = "\n".join([f"{t['member']} - '{t['book']}' (Due: {t['due_date']})" for t in overdue])
            messagebox.showinfo("Reminders", f"Due reminders sent to:\n\n{msg}")
        else:
            messagebox.showinfo("Reminders", "No overdue books.")

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

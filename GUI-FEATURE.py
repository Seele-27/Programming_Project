import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3, requests


conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS membertb(
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_number INTEGER UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    join_date DATE,
    membership_type TEXT NOT NULL,
    status TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS booktb (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT UNIQUE,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT NOT NULL,
    publication_year INTEGER NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    cover_image_url TEXT NOT NULL,
    page_count INTEGER NOT NULL,
    language TEXT NOT NULL,
    total_copies INTEGER NOT NULL,
    available_copies INTEGER NOT NULL,
    shelf_loc TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS transtb(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    book_id INTEGER,
    issue_date DATE,
    due_date DATE,
    return_date DATE,
    fine_amount REAL,
    status TEXT,
    FOREIGN KEY(member_id) REFERENCES membertb(member_id),
    FOREIGN KEY(book_id) REFERENCES booktb(book_id))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bookreviewtb(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    rating INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    review_date DATE,
    FOREIGN KEY(book_id) REFERENCES booktb(book_id),
    FOREIGN KEY(member_id) REFERENCES membertb(member_id))""")

conn.commit()

# API integration
def fetch_book_details(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    r = requests.get(url).json()
    book = r.get(f"ISBN:{isbn}", {})
    return {
        "title": book.get("title", ""),
        "author": ", ".join([a["name"] for a in book.get("authors", [])]),
        "publisher": book.get("publishers", [{}])[0].get("name", ""),
        "cover": book.get("cover", {}).get("large", "")
    }

# GUI Features
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def load_dashboard():
    clear_frame()
    ttk.Label(main_frame, text="📚 Library Dashboard", font=("Arial", 16)).pack(pady=10)
    cursor.execute("SELECT COUNT(*) FROM membertb")
    members = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM booktb")
    books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM transtb")
    transactions = cursor.fetchone()[0]
    stats = f"Members: {members} | Books: {books} | Transactions: {transactions}"
    ttk.Label(main_frame, text=stats, font=("Arial", 12)).pack(pady=5)
    ttk.Button(main_frame, text="Add Book", command=load_book_form).pack(pady=2)
    ttk.Button(main_frame, text="Register Member", command=load_member_form).pack(pady=2)
    ttk.Button(main_frame, text="Issue Book", command=load_transaction_form).pack(pady=2)
    ttk.Button(main_frame, text="Show Reviews", command=load_review_display).pack(pady=2)

def load_book_form():
    clear_frame()
    ttk.Label(main_frame, text="Add Book", font=("Arial", 14)).pack(pady=5)
    isbn_entry = ttk.Entry(main_frame)
    isbn_entry.pack()
    ttk.Button(main_frame, text="Lookup ISBN", command=lambda: autofill_book(isbn_entry.get())).pack()

def autofill_book(isbn):
    details = fetch_book_details(isbn)
    ttk.Label(main_frame, text=f"Title: {details['title']}").pack()
    ttk.Label(main_frame, text=f"Author: {details['author']}").pack()
    ttk.Label(main_frame, text=f"Publisher: {details['publisher']}").pack()
    if details["cover"]:
        img = Image.open(requests.get(details["cover"], stream=True).raw)
        img = ImageTk.PhotoImage(img.resize((100, 150)))
        label = ttk.Label(main_frame, image=img)
        label.image = img
        label.pack()

def load_member_form():
    clear_frame()
    ttk.Label(main_frame, text="Register Member", font=("Arial", 14)).pack(pady=5)
    fields = ["Membership Number", "First Name", "Last Name", "Email", "Phone", "Address", "Join Date", "Membership Type", "Status"]
    entries = [ttk.Entry(main_frame) for _ in fields]
    for i, field in enumerate(fields):
        ttk.Label(main_frame, text=field).pack()
        entries[i].pack()
    def submit():
        cursor.execute("""INSERT INTO membertb(
            membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status)
            VALUES(?,?,?,?,?,?,?,?,?)""", tuple(e.get() for e in entries))
        conn.commit()
        messagebox.showinfo("Success", "Member added.")
    ttk.Button(main_frame, text="Submit", command=submit).pack(pady=5)

def load_transaction_form():
    clear_frame()
    ttk.Label(main_frame, text="Issue Book", font=("Arial", 14)).pack(pady=5)
    fields = ["Member ID", "Book ID", "Issue Date", "Due Date", "Return Date", "Fine Amount", "Status"]
    entries = [ttk.Entry(main_frame) for _ in fields]
    for i, field in enumerate(fields):
        ttk.Label(main_frame, text=field).pack()
        entries[i].pack()
    def submit():
        cursor.execute("""INSERT INTO transtb(member_id, book_id, issue_date, due_date, return_date, fine_amount, status)
            VALUES (?,?,?,?,?,?,?)""", tuple(e.get() for e in entries))
        conn.commit()
        messagebox.showinfo("Success", "Transaction recorded.")
    ttk.Button(main_frame, text="Submit", command=submit).pack(pady=5)

def load_review_display():
    clear_frame()
    ttk.Label(main_frame, text="Book Reviews", font=("Arial", 14)).pack(pady=5)
    cursor.execute("SELECT * FROM bookreviewtb")
    for review in cursor.fetchall():
        ttk.Label(main_frame, text=str(review)).pack()

load_dashboard()
root.mainloop()
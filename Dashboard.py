import tkinter as tk
from tkinter import messagebox
import sqlite3

root = tk.Tk()
root.title("Library Dashboard")
root.geometry("500x600")

# Connect to database (optional)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Dummy functions
def add_book():
    messagebox.showinfo("Add Book", "Add Book clicked!")

def register_member():
    messagebox.showinfo("Register Member", "Register Member clicked!")

def issue_book():
    messagebox.showinfo("Issue Book", "Issue Book clicked!")

def return_book():
    messagebox.showinfo("Return Book", "Return Book clicked!")

# Title
dashboard_label = tk.Label(root, text="📚 Library Dashboard", font=("Arial", 16, "bold"))
dashboard_label.pack(pady=20)

# Buttons (horizontal)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_book_button = tk.Button(button_frame, text="Add Book", font=("Arial", 12), fg="yellow", bg="purple", command=add_book)
add_book_button.pack(side="left", padx=8)

register_member_button = tk.Button(button_frame, text="Register Member", font=("Arial", 12), fg="yellow", bg="purple", command=register_member)
register_member_button.pack(side="left", padx=8)

issue_book_button = tk.Button(button_frame, text="Issue Book", font=("Arial", 12), fg="yellow", bg="purple", command=issue_book)
issue_book_button.pack(side="left", padx=8)

return_book_button = tk.Button(button_frame, text="Return Book", font=("Arial", 12), fg="yellow", bg="purple", command=return_book)
return_book_button.pack(side="left", padx=8)

# ↓ Everything below will appear under the buttons ↓

# Recent Transactions
recent_transactions_label = tk.Label(root, text="Recent Transactions:", font=("Arial", 12, "bold"))
recent_transactions_label.pack(pady=(20, 5))

recent_transactions_list = tk.Listbox(root, height=5, width=50)
recent_transactions_list.pack(pady=5)

# Popular Books
popular_books_label = tk.Label(root, text="Popular Books:", font=("Arial", 12, "bold"))
popular_books_label.pack(pady=(20, 5))

popular_books_list = tk.Listbox(root, height=5, width=50)
popular_books_list.pack(pady=5)

root.mainloop()

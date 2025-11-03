# BOOK TABLE

import sqlite3

conn = sqlite3.connect("bks.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS booktb (
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
    shelf_loc TEXT NOT NULL
)
""")
conn.commit()


def InsertBookInfo():
    book_id = int(input("Enter Book ID: "))
    isbn = input("Enter ISBN: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    publisher = input("Enter Publisher: ")
    publication_year = int(input("Enter Publication Year: "))
    category = input("Enter Category: ")
    description = input("Enter Description: ")
    cover_image_url = input("Enter Cover Image URL: ")
    page_count = int(input("Enter Page Count: "))
    language = input("Enter Language: ")
    total_copies = int(input("Enter Total Copies: "))
    available_copies = int(input("Enter Available Copies: "))
    shelf_loc = input("Enter Shelf Location: ")


    cursor.execute("""
    INSERT INTO booktb (
        book_id, isbn, title, author, publisher, publication_year, category,
        description, cover_image_url, page_count, language, total_copies,
        available_copies, shelf_loc
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        book_id, isbn, title, author, publisher, publication_year, category,
        description, cover_image_url, page_count, language, total_copies,
        available_copies, shelf_loc
    ))
    conn.commit()
    print("\n Book information added successfully!")



def ShowRecord():
    print("\n All Book Records:")
    cursor.execute("SELECT * FROM booktb")
    records = cursor.fetchall()
    for record in records:
        print(record)


def Display():
    print("\n Menu:")
    print("1. Insert Book Info")
    print("2. Show Book Records")
    print("0. Exit")


def main():
    while True:
        Display()

        choice = int(input("Enter Choice (1, 2, 0): "))
        if choice == 1:
            InsertBookInfo()
        elif choice == 2:
            ShowRecord()
        elif choice == 0:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


    conn.close()

main()


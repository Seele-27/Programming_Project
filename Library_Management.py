import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS membertb(
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_number INTEGER UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    join_date DATE,
    membership_type TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS transtb(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    book_id INTEGER,
    issue_date DATE,
    due_date DATE,
    return_date DATE,
    fine_amount REAL,
    status TEXT,
    FOREIGN KEY(member_id) REFERENCES membertb(member_id),
    FOREIGN KEY(book_id) REFERENCES booktb(book_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookreviewtb(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    rating INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    review_date DATE,
    FOREIGN KEY(book_id) REFERENCES booktb(book_id),
    FOREIGN KEY(member_id) REFERENCES membertb(member_id)
)
""")

conn.commit()

# Member functions
def InsertMemberInfo():
    membership_number = int(input("Enter membership number: "))
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    address = input("Enter your address: ")
    join_date = input("Enter your joined date (YYYY-MM-DD): ")
    membership_type = input("Enter your membership type: ")
    status = input("Enter your status: ")

    cursor.execute("""
    INSERT INTO membertb(
        membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status)
    VALUES(?,?,?,?,?,?,?,?,?)
    """, (membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status))

    conn.commit()
    print("\nMembership information added successfully!")

def ShowMemberRecords():
    print("\nAll Membership Records:")
    cursor.execute("SELECT * FROM membertb")
    records = cursor.fetchall()
    for record in records:
        print(record)

# Book functions
def InsertBookInfo():
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
        isbn, title, author, publisher, publication_year, category,
        description, cover_image_url, page_count, language, total_copies,
        available_copies, shelf_loc
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        isbn, title, author, publisher, publication_year, category,
        description, cover_image_url, page_count, language, total_copies,
        available_copies, shelf_loc
    ))

    conn.commit()
    print("\nBook information added successfully!")

def ShowBookRecords():
    print("\nAll Book Records:")
    cursor.execute("SELECT * FROM booktb")
    records = cursor.fetchall()
    for record in records:
        print(record)

# Transaction functions
def InsertTransactionInfo():
    member_id = int(input("Enter Member ID: "))
    book_id = int(input("Enter Book ID: "))
    issue_date = input("Enter date of issue (YYYY-MM-DD): ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    return_date = input("Enter return date (YYYY-MM-DD): ")
    fine_amount = float(input("Enter fine amount: "))
    status = input("Enter status: ")

    cursor.execute("""
    INSERT INTO transtb(member_id, book_id, issue_date, due_date, return_date, fine_amount, status)
    VALUES (?,?,?,?,?,?,?)
    """, (member_id, book_id, issue_date, due_date, return_date, fine_amount, status))

    conn.commit()
    print("\nTransaction information added successfully!")

def ShowTransactionRecords():
    print("\nTransaction Records:")
    cursor.execute("SELECT * FROM transtb")
    records = cursor.fetchall()
    for record in records:
        print(record)

# Review functions
def InsertReviewInfo():
    book_id = int(input("Enter Book ID: "))
    member_id = int(input("Enter Member ID: "))
    rating = int(input("Enter your rating (1–5): "))
    review_text = input("Enter review text: ")
    review_date = input("Enter review date (YYYY-MM-DD): ")

    cursor.execute("""
    INSERT INTO bookreviewtb(book_id, member_id, rating, review_text, review_date)
    VALUES(?,?,?,?,?)
    """, (book_id, member_id, rating, review_text, review_date))

    conn.commit()
    print("\nReview information added successfully!")

def ShowReviewRecords():
    print("\nBook Reviews:")
    cursor.execute("SELECT * FROM bookreviewtb")
    records = cursor.fetchall()
    for record in records:
        print(record)


def DisplayMenu():
    print("\nLibrary Management Menu:")
    print("1. Insert Membership Information")
    print("2. Show Membership Records")
    print("3. Insert Book Information")
    print("4. Show Book Records")
    print("5. Insert Transaction Information")
    print("6. Show Transaction Records")
    print("7. Insert Book Review")
    print("8. Show Book Reviews")
    print("0. Exit")

def main():
    while True:
        DisplayMenu()
        choice = input("Enter Choice (0-8): ")
        if choice == '1':
            InsertMemberInfo()
        elif choice == '2':
            ShowMemberRecords()
        elif choice == '3':
            InsertBookInfo()
        elif choice == '4':
            ShowBookRecords()
        elif choice == '5':
            InsertTransactionInfo()
        elif choice == '6':
            ShowTransactionRecords()
        elif choice == '7':
            InsertReviewInfo()
        elif choice == '8':
            ShowReviewRecords()
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

    main()
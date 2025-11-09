import sqlite3
import sys
from pathlib import Path

DB_NAME = "library.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    # enforce foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    with get_conn() as conn:
        c = conn.cursor()
        # Books
        c.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            );
        ''')
        # Members
        c.execute('''
            CREATE TABLE IF NOT EXISTS Members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            );
        ''')
        # Book_Reviews
        c.execute('''
            CREATE TABLE IF NOT EXISTS Book_Reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                rating INTEGER CHECK(rating BETWEEN 1 AND 5),
                review_text TEXT,
                review_date TEXT DEFAULT (DATE('now')),
                FOREIGN KEY (book_id) REFERENCES Books(book_id),
                FOREIGN KEY (member_id) REFERENCES Members(member_id)
            );
        ''')
    print(" DB initialized (or already existed).")


def seed_data():
    # add sample books/members only if they don't exist
    with get_conn() as conn:
        c = conn.cursor()
        # check if Books table empty
        c.execute("SELECT COUNT(*) FROM Books")
        if c.fetchone()[0] == 0:
            c.executemany("INSERT INTO Books (title, author) VALUES (?, ?)", [
                ("Atomic Habits", "James Clear"),
                ("The Alchemist", "Paulo Coelho"),
                ("Clean Code", "Robert C. Martin")
            ])
            print(" Sample books added.")
        else:
            print("ℹ Books already present; skipping book seed.")

        c.execute("SELECT COUNT(*) FROM Members")
        if c.fetchone()[0] == 0:
            c.executemany("INSERT INTO Members (first_name, last_name) VALUES (?, ?)", [
                ("John", "Doe"),
                ("Mary", "Smith"),
                ("Alice", "Ngcobo")
            ])
            print(" Sample members added.")
        else:
            print("ℹ Members already present; skipping member seed.")


def list_books():
    with get_conn() as conn:
        rows = conn.execute("SELECT book_id, title, author FROM Books ORDER BY book_id").fetchall()
    if not rows:
        print("No books in DB.")
        return
    print("\nBooks:")
    for r in rows:
        print(f"  ID {r['book_id']}: {r['title']} — {r['author']}")


def list_members():
    with get_conn() as conn:
        rows = conn.execute("SELECT member_id, first_name, last_name FROM Members ORDER BY member_id").fetchall()
    if not rows:
        print("No members in DB.")
        return
    print("\nMembers:")
    for r in rows:
        print(f"  ID {r['member_id']}: {r['first_name']} {r['last_name']}")


def add_review(book_id, member_id, rating, review_text):
    # validation
    try:
        book_id = int(book_id)
        member_id = int(member_id)
        rating = int(rating)
    except ValueError:
        print(" book_id, member_id and rating must be integers.")
        return

    if rating < 1 or rating > 5:
        print(" rating must be between 1 and 5.")
        return

    with get_conn() as conn:
        c = conn.cursor()
        # check book exists
        c.execute("SELECT 1 FROM Books WHERE book_id = ?", (book_id,))
        if c.fetchone() is None:
            print(f" No book with ID {book_id}. Use 'list_books' to see valid IDs.")
            return
        # check member exists
        c.execute("SELECT 1 FROM Members WHERE member_id = ?", (member_id,))
        if c.fetchone() is None:
            print(f" No member with ID {member_id}. Use 'list_members' to see valid IDs.")
            return

        try:
            c.execute('''
                INSERT INTO Book_Reviews (book_id, member_id, rating, review_text)
                VALUES (?, ?, ?, ?)
            ''', (book_id, member_id, rating, review_text))
            conn.commit()
            print(" Review added successfully.")
        except sqlite3.IntegrityError as e:
            print(" Integrity error:", e)


def view_reviews(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        print(" book_id must be an integer.")
        return

    with get_conn() as conn:
        rows = conn.execute('''
            SELECT r.review_id, r.rating, r.review_text, r.review_date,
                   b.title AS book_title,
                   m.first_name || ' ' || m.last_name AS reviewer
            FROM Book_Reviews r
            JOIN Books b ON r.book_id = b.book_id
            JOIN Members m ON r.member_id = m.member_id
            WHERE r.book_id = ?
            ORDER BY r.review_date DESC, r.review_id DESC
        ''', (book_id,)).fetchall()

    if not rows:
        print("No reviews found for that book.")
        return

    print(f"\nReviews for Book ID {book_id} — {rows[0]['book_title']}:")
    for r in rows:
        print("-" * 40)
        print(f"Review ID: {r['review_id']}")
        print(f"Reviewer: {r['reviewer']}")
        print(f"Rating: {r['rating']}/5")
        print(f"Date: {r['review_date']}")
        print(f"Text: {r['review_text']}")


def average_rating(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        print(" book_id must be an integer.")
        return

    with get_conn() as conn:
        avg = conn.execute("SELECT AVG(rating) AS avg_rating, COUNT(*) AS cnt FROM Book_Reviews WHERE book_id = ?", (book_id,)).fetchone()
    if avg["cnt"] == 0:
        print("No ratings for that book yet.")
    else:
        print(f"Average rating for Book ID {book_id}: {round(avg['avg_rating'], 2)} ({avg['cnt']} review(s))")


def list_all_reviews():
    with get_conn() as conn:
        rows = conn.execute('''
            SELECT r.review_id, b.title as book, m.first_name || ' ' || m.last_name as reviewer,
                   r.rating, r.review_text, r.review_date
            FROM Book_Reviews r
            JOIN Books b ON r.book_id = b.book_id
            JOIN Members m ON r.member_id = m.member_id
            ORDER BY r.review_date DESC, r.review_id DESC
        ''').fetchall()
    if not rows:
        print("No reviews in database.")
        return
    for r in rows:
        print("-" * 40)
        print(f"ID {r['review_id']} | Book: {r['book']} | Reviewer: {r['reviewer']}")
        print(f"Rating: {r['rating']} | Date: {r['review_date']}")
        print(f"Text: {r['review_text']}")


def print_help():
    print("""
Available commands:
  init_db             -> Create tables
  seed                -> Insert sample data (only if empty)
  list_books          -> Show all books and their IDs
  list_members        -> Show all members and their IDs
  add_review          -> Interactive: prompts for book_id, member_id, rating, text
  add_review_args b m r text
                      -> Non-interactive add (b=book_id m=member_id r=rating)
  view_reviews <book_id>
  avg <book_id>       -> Show average rating
  list_reviews        -> List all reviews
  help                -> Show this
  exit                -> Quit
""")


def interactive_add_review():
    list_books()
    list_members()
    try:
        b = int(input("Enter Book ID: ").strip())
        m = int(input("Enter Member ID: ").strip())
        r = int(input("Enter Rating (1-5): ").strip())
    except ValueError:
        print(" IDs and rating must be integers.")
        return
    text = input("Enter review text: ").strip()
    add_review(b, m, r, text)


def main():
    if not Path(DB_NAME).exists():
        print(f"DB '{DB_NAME}' does not exist. Running init_db() to create it.")
        init_db()

    print_help()
    while True:
        cmd = input("\n> ").strip()
        if cmd in ("exit", "quit"):
            print("Goodbye.")
            break
        if cmd == "help":
            print_help()
        elif cmd == "init_db":
            init_db()
        elif cmd == "seed":
            seed_data()
        elif cmd == "list_books":
            list_books()
        elif cmd == "list_members":
            list_members()
        elif cmd == "add_review":
            interactive_add_review()
        elif cmd.startswith("add_review_args"):
            parts = cmd.split(" ", 4)
            if len(parts) < 5:
                print("Usage: add_review_args <book_id> <member_id> <rating> <text>")
            else:
                _, b, m, r, text = parts
                add_review(b, m, r, text)
        elif cmd.startswith("view_reviews"):
            parts = cmd.split()
            if len(parts) != 2:
                print("Usage: view_reviews <book_id>")
            else:
                view_reviews(parts[1])
        elif cmd.startswith("avg"):
            parts = cmd.split()
            if len(parts) != 2:
                print("Usage: avg <book_id>")
            else:
                average_rating(parts[1])
        elif cmd == "list_reviews":
            list_all_reviews()
        else:
            print("Unknown command. Type 'help' for commands.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)

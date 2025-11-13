import sqlite3

conn = sqlite3.connect("member.db")
cursor = conn.cursor()

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

conn.commit()

def MemberInfo():

    member_id = int(input("Enter member id: "))
    membership_number = int(input("Enter membership number: "))
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    phone = int(input("Enter your phone number: "))
    address = input("Enter your address: ")
    join_date = input("Enter your joined date (YYYY-MM-DD): ")
    membership_type = input("Enter your membership type: ")
    status = input("Enter your status: ")

    cursor.execute("""
    INSERT INTO membertb(
        member_id, membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status)
    VALUES(?,?,?,?,?,?,?,?,?,?)
    """, (member_id, membership_number, first_name, last_name, email, phone, address, join_date, membership_type, status))

    conn.commit()
    print("\n Membership information added successfully!")

def ShowRecord():

    print("\n All Membership Records")
    cursor.execute("""
    SELECT * FROM membertb
    """)
    record = cursor.fetchall()
    for rec in record:
        print(rec)

def Display():
    print("\n Menu Options:")
    print("1. Insert Membership Information")
    print("2. Show Membership Records")
    print("0. Exit")

def main():
    while True:
        Display()

        choice = int(input("Enter Choice (1, 2, 0): "))
        if choice == 1:
            MemberInfo()
        elif choice == 2:
            ShowRecord()
        elif choice == 0:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


    conn.close()
if __name__ == '__main__':
    main()
# Programming_Project

# PROJECT 2
LIBRARY MANAGEMENT SYSTEM WITH BOOK INFORMATION API [100 MARKS]
Create a Library Management System with integration to book information APIs for automatic book data retrieval and ISBN lookup.
Requirements
1. Database Design (15 marks)
Books Table:
•	book_id (Primary Key, Auto-increment)
•	isbn (TEXT, UNIQUE)
•	title (TEXT)
•	author (TEXT)
•	publisher (TEXT)
•	publication_year (INTEGER)
•	category (TEXT)
•	description (TEXT)
•	cover_image_url (TEXT)
•	page_count (INTEGER)
•	language (TEXT)
•	total_copies (INTEGER)
•	available_copies (INTEGER)
•	shelf_location (TEXT)
Members Table:
•	member_id (Primary Key, Auto-increment)
•	membership_number (TEXT, UNIQUE)
•	first_name (TEXT)
•	last_name (TEXT)
•	email (TEXT, UNIQUE)
•	phone (TEXT)
•	address (TEXT)
•	join_date (DATE)
•	membership_type (TEXT)
•	status (TEXT)
Transactions Table:
•	transaction_id (Primary Key, Auto-increment)
•	member_id (Foreign Key)
•	book_id (Foreign Key)
•	issue_date (DATE)
•	due_date (DATE)
•	return_date (DATE)
•	fine_amount (REAL)
•	status (TEXT)
Book_Reviews Table:
•	review_id (Primary Key, Auto-increment)
•	book_id (Foreign Key)
•	member_id (Foreign Key)
•	rating (INTEGER)
•	review_text (TEXT)
•	review_date (DATE)
2. GUI Features 
Dashboard 
•	Display key statistics
•	Quick action buttons
•	Recent transactions list
•	Popular books widget
Book Management with API Integration 
•	Add new books with ISBN lookup
•	Auto-populate book details from API
•	Display book cover images
•	Update book details
•	Search books by title, author, ISBN, or category
•	View book availability status
Member Management 
•	Register new members
•	Update member information
•	View member borrowing history
•	Send email notifications
Transaction Management 
•	Issue books to members
•	Return books and calculate fines
•	View all transactions
•	Send due date reminders via email/SMS
3. API Integration Features
Google Books API Integration
•	ISBN lookup to auto-fill book details
•	Fetch book cover images 
•	Get book descriptions and metadata 
•	Search for books by title/author 
Open Library API Integration 
•	Alternative source for book information 
•	Get author information 
•	Fetch related books/recommendations 
Email/SMS Notification API 
•	Send due date reminders 
•	Overdue book notifications 
•	New book arrival notifications 

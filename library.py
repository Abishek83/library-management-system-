import csv
import datetime
import os

# Get the current directory of the script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the data files directory
DATA_FILES_DIR = os.path.join(CURRENT_DIR, 'Data file')

# Define the paths to the individual data files
BOOKS_FILE = os.path.join(DATA_FILES_DIR, 'books.dat')
BORROWS_FILE = os.path.join(DATA_FILES_DIR, 'borrows.dat')
MEMBERS_FILE = os.path.join(DATA_FILES_DIR, 'members.dat')
RESERVATIONS_FILE = os.path.join(DATA_FILES_DIR, 'reservations.dat')
# Book class
class Book:
    def __init__(self, book_id, title, author, isbn, available):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

# Reservation class
class Reservation:
    def __init__(self, reservation_id, member_id, book_id, reservation_date):
        self.reservation_id = reservation_id
        self.member_id = member_id
        self.book_id = book_id
        self.reservation_date = reservation_date
        self.status = 'pending'

# Member class
class Member:
    def __init__(self, member_id, name, contact):
        self.member_id = member_id
        self.name = name
        self.contact = contact
        self.borrowed_books = []
        self.reservations = []

# Library manager class
class LibraryManager:
    def __init__(self):
        self.books = self.load_books()
        self.reservations = self.load_reservations()
        self.members = self.load_members()

    def load_books(self):
        books = []
        try:
            with open(BOOKS_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    book_id, title, author, isbn, available = row
                    book = Book(book_id, title, author, isbn, available == 'True')
                    books.append(book)
        except FileNotFoundError:
            print(f"Error loading books: {BOOKS_FILE} not found.")
        return books

    def load_reservations(self):
        reservations = []
        try:
            with open(RESERVATIONS_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    # Split the line into individual values
                reservation_id, member_id, book_id, reservation_date = line.strip().split(',')
                # Create a Reservation object and add it to the list
                reservations.append(Reservation(reservation_id, member_id, book_id, reservation_date))
        except FileNotFoundError:
            print(f"Error loading reservations: {RESERVATIONS_FILE} not found.")
        return reservations

    def load_members(self):
        members = []
        try:
            with open(MEMBERS_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    member_id, name, contact = row
                    member = Member(member_id, name, contact)
                    members.append(member)
        except FileNotFoundError:
            print(f"Error loading members: {MEMBERS_FILE} not found.")
        return members

    def save_books(self):
        try:
            with open(BOOKS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['book_id', 'title', 'author', 'isbn', 'available'])
                for book in self.books:
                    writer.writerow([book.book_id, book.title, book.author, book.isbn, str(book.available)])
        except IOError:
            print(f"Error saving books: {BOOKS_FILE}")

    def save_reservations(self):
        try:
            with open(RESERVATIONS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['reservation_id', 'member_id', 'book_id', 'reservation_date'])
                for reservation in self.reservations:
                    writer.writerow([reservation.reservation_id, reservation.member_id, reservation.book_id, reservation.reservation_date])
        except IOError:
            print(f"Error saving reservations: {RESERVATIONS_FILE}")

    def save_members(self):
        try:
            with open(MEMBERS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['member_id', 'name', 'contact'])
                for member in self.members:
                    writer.writerow([member.member_id, member.name, member.contact])
        except IOError:
            print(f"Error saving members: {MEMBERS_FILE}")

    def search_books(self, query):
        results = [book for book in self.books if query.lower() in book.title.lower()]
        return results

    def make_reservation(self, member_id, book_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if member and book and not book.available:
            reservation_id = len(self.reservations) + 1
            reservation_date = datetime.date.today().isoformat()
            reservation = Reservation(str(reservation_id), member_id, book_id, reservation_date)
            self.reservations.append(reservation)
            member.reservations.append(reservation)
            self.save_reservations()
            print(f"Reservation made for book '{book.title}' by {member.name}.")
        else:
            print("Invalid member or book, or book is available.")

    def get_book_summary(self):
        total_books = len(self.books)
        available_books = sum(book.available for book in self.books)
        unavailable_books = total_books - available_books

        book_queues = {}
        for reservation in self.reservations:
            book_id = reservation.book_id
            if book_id in book_queues:
                book_queues[book_id].append(reservation)
            else:
                book_queues[book_id] = [reservation]

        summary = f"Total books: {total_books}\n"
        summary += f"Available books: {available_books}\n"
        summary += f"Unavailable books: {unavailable_books}\n"
        summary += "\nReservation queues:\n"
        for book_id, queue in book_queues.items():
            book = next((b for b in self.books if b.book_id == book_id), None)
            if book:
                summary += f"{book.title} by {book.author}:\n"
                for reservation in queue:
                    member = next((m for m in self.members if m.member_id == reservation.member_id), None)
                    if member:
                        summary += f"  - {member.name} ({reservation.reservation_date})\n"
        return summary

    def manage_customers(self):
        while True:
            print("\nCustomer Management")
            print("1. Search customers")
            print("2. Edit customer")
            print("3. Create customer")
            print("4. Delete customer")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter customer name: ")
                customers = [m for m in self.members if name.lower() in m.name.lower()]
                if customers:
                    print("\nCustomer search results:")
                    for customer in customers:
                        print(f"ID: {customer.member_id}, Name: {customer.name}, Contact: {customer.contact}")
                else:
                    print("No matching customers found.")

            elif choice == '2':
                member_id = input("Enter customer ID: ")
                customer = next((m for m in self.members if m.member_id == member_id), None)
                if customer:
                    new_name = input(f"Enter new name (current: {customer.name}): ")
                    new_contact = input(f"Enter new contact (current: {customer.contact}): ")
                    customer.name = new_name
                    customer.contact = new_contact
                    self.save_members()
                    print("Customer updated successfully.")
                else:
                    print("Customer not found.")

            elif choice == '3':
                member_id = str(len(self.members) + 1)
                name = input("Enter customer name: ")
                contact = input("Enter customer contact: ")
                new_customer = Member(member_id, name, contact)
                self.members.append(new_customer)
                self.save_members()
                print("New customer created successfully.")

            elif choice == '4':
                member_id = input("Enter customer ID to delete: ")
                customer = next((m for m in self.members if m.member_id == member_id), None)
                if customer:
                    self.members.remove(customer)
                    self.save_members()
                    print("Customer deleted successfully.")
                else:
                    print("Customer not found.")

            elif choice == '0':
                break

            else:
                print("Invalid choice. Try again.")

    def manage_books(self):
        while True:
            print("\nBook Management")
            print("1. Search books")
            print("2. Edit book")
            print("3. Create book")
            print("4. Delete book")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                title = input("Enter book title: ")
                books = [b for b in self.books if title.lower() in b.title.lower()]
                if books:
                    print("\nBook search results:")
                    for book in books:
                        print(f"ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Available: {book.available}")
                else:
                    print("No matching books found.")

            elif choice == '2':
                book_id = input("Enter book ID: ")
                book = next((b for b in self.books if b.book_id == book_id), None)
                if book:
                    new_title = input(f"Enter new title (current: {book.title}): ")
                    new_author = input(f"Enter new author (current: {book.author}): ")
                    new_available = input(f"Enter new availability (current: {book.available}): ")
                    book.title = new_title
                    book.author = new_author
                    book.available = new_available == 'True'
                    self.save_books()
                    print("Book updated successfully.")
                else:
                    print("Book not found.")

            elif choice == '3':
                book_id = str(len(self.books) + 1)
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                isbn = input("Enter book ISBN: ")
                available = input("Is the book available? (True/False): ")
                new_book = Book(book_id, title, author, isbn, available == 'True')
                self.books.append(new_book)
                self.save_books()
                print("New book created successfully.")

            elif choice == '4':
                book_id = input("Enter book ID to delete: ")
                book = next((b for b in self.books if b.book_id == book_id), None)
                if book:
                    self.books.remove(book)
                    self.save_books()
                    print("Book deleted successfully.")
                else:
                    print("Book not found.")

            elif choice == '0':
                break

            else:
                print("Invalid choice. Try again.")

# Staff application
def staff_app(library):
    while True:
        print("\nStaff Application")
        print("1. Search books")
        print("2. Make reservation")
        print("3. Book summary")
        print("4. Manage customers")
        print("5. Manage books")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            query = input("Enter search query: ")
            results = library.search_books(query)
            if results:
                print("\nSearch results:")
                for book in results:
                    print(f"{book.title} by {book.author} (Available: {book.available})")
            else:
                print("No matching books found.")

        elif choice == '2':
            member_id = input("Enter member ID: ")
            book_id = input("Enter book ID: ")
            library.make_reservation(member_id, book_id)

        elif choice == '3':
            summary = library.get_book_summary()
            print("\nBook Summary:")
            print(summary)

        elif choice == '4':
            library.manage_customers()

        elif choice == '5':
            library.manage_books()

        elif choice == '0':
            break

        else:
            print("Invalid choice. Try again.")

# Customer application
def customer_app(library):
    while True:
        print("\nCustomer Application")
        print("1. Search books")
        print("2. Make reservation")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            query = input("Enter search query: ")
            results = library.search_books(query)
            if results:
                print("\nSearch results:")
                for book in results:
                    print(f"{book.title} by {book.author} (Available: {book.available})")
            else:
                print("No matching books found.")

        elif choice == '2':
            member_id = input("Enter your member ID: ")
            book_id = input("Enter book ID: ")
            library.make_reservation(member_id, book_id)

        elif choice == '0':
            break

        else:
            print("Invalid choice. Try again.")

# Main function
def main():
    library = LibraryManager()

    while True:
        print("\nLibrary Management System")
        print("1. Staff application")
        print("2. Customer application")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            staff_app(library)
        elif choice == '2':
            customer_app(library)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
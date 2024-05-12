import csv
import datetime
import os

# Data file paths
CURRENT_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'Library management system')
DATA_FILES_DIR = os.path.join(CURRENT_DIR, 'data_files')
BOOKS_FILE = os.path.join(DATA_FILES_DIR, 'books.dat')
BORROWS_FILE = os.path.join(DATA_FILES_DIR, 'borrows.dat')
RESERVATIONS_FILE = os.path.join(DATA_FILES_DIR, 'reservations.dat')
MEMBERS_FILE = os.path.join(DATA_FILES_DIR, 'members.dat')

# Book class
class Book:
    def __init__(self, book_id, title, author, isbn, available):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

# Borrow class
class Borrow:
    def __init__(self, borrow_id, member_id, book_id, borrow_date, due_date):
        self.borrow_id = borrow_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date

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
        self.borrows = self.load_borrows()
        self.reservations = self.load_reservations()
        self.members = self.load_members()

    def load_books(self):
        books = []
        try:
            with open(BOOKS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    book_id, title, author, isbn, available = row
                    book = Book(book_id, title, author, isbn, available == 'True')
                    books.append(book)
        except FileNotFoundError:
            print(f"File {BOOKS_FILE} not found.")
        return books

    def load_borrows(self):
        borrows = []
        try:
            with open(BORROWS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    borrow_id, member_id, book_id, borrow_date, due_date = row
                    borrow = Borrow(borrow_id, member_id, book_id, borrow_date, due_date)
                    borrows.append(borrow)
        except FileNotFoundError:
            print(f"File {BORROWS_FILE} not found.")
        return borrows

    def load_reservations(self):
        reservations = []
        try:
            with open(RESERVATIONS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    reservation_id, member_id, book_id, reservation_date = row
                    reservation = Reservation(reservation_id, member_id, book_id, reservation_date)
                    reservations.append(reservation)
        except FileNotFoundError:
            print(f"File {RESERVATIONS_FILE} not found.")
        return reservations

    def load_members(self):
        members = []
        try:
            with open(MEMBERS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    member_id, name, contact = row
                    member = Member(member_id, name, contact)
                    members.append(member)
        except FileNotFoundError:
            print(f"File {MEMBERS_FILE} not found.")
        return members

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

    def create_book(self, title, author, isbn):
        book_id = str(len(self.books) + 1)
        available = True
        book = Book(book_id, title, author, isbn, available)
        self.books.append(book)
        self.save_books()
        print(f"Book '{title}' by {author} created successfully.")

    def edit_book(self, book_id, new_title=None, new_author=None, new_isbn=None):
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book:
            if new_title:
                book.title = new_title
            if new_author:
                book.author = new_author
            if new_isbn:
                book.isbn = new_isbn
            self.save_books()
            print(f"Book '{book.title}' by {book.author} updated successfully.")
        else:
            print(f"Book with ID {book_id} not found.")

    def delete_book(self, book_id):
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book:
            self.books.remove(book)
            def save_books(self):
        with open(BOOKS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['book_id', 'title', 'author', 'isbn', 'available'])
            for book in self.books:
                writer.writerow([book.book_id, book.title, book.author, book.isbn, str(book.available)])

    def create_member(self, name, contact):
        member_id = str(len(self.members) + 1)
        member = Member(member_id, name, contact)
        self.members.append(member)
        self.save_members()
        print(f"Member '{name}' created successfully.")

    def edit_member(self, member_id, new_name=None, new_contact=None):
        member = next((m for m in self.members if m.member_id == member_id), None)
        if member:
            if new_name:
                member.name = new_name
            if new_contact:
                member.contact = new_contact
            self.save_members()
            print(f"Member '{member.name}' updated successfully.")
        else:
            print(f"Member with ID {member_id} not found.")

    def delete_member(self, member_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        if member:
            self.members.remove(member)
            self.save_members()
            print(f"Member '{member.name}' deleted successfully.")
        else:
            print(f"Member with ID {member_id} not found.")

    def save_members(self):
        with open(MEMBERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['member_id', 'name', 'contact'])
            for member in self.members:
                writer.writerow([member.member_id, member.name, member.contact])

    def create_reservation(self, member_id, book_id):
        self.make_reservation(member_id, book_id)
        self.save_reservations()

    def delete_reservation(self, reservation_id):
        reservation = next((r for r in self.reservations if r.reservation_id == reservation_id), None)
        if reservation:
            self.reservations.remove(reservation)
            member = next((m for m in self.members if m.member_id == reservation.member_id), None)
            if member:
                member.reservations.remove(reservation)
            self.save_reservations()
            print(f"Reservation with ID {reservation_id} deleted successfully.")
        else:
            print(f"Reservation with ID {reservation_id} not found.")

    def save_reservations(self):
        with open(RESERVATIONS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['reservation_id', 'member_id', 'book_id', 'reservation_date'])
            for reservation in self.reservations:
                writer.writerow([reservation.reservation_id, reservation.member_id, reservation.book_id, reservation.reservation_date])

    def borrow_book(self, member_id, book_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if member and book and book.available:
            borrow_id = str(len(self.borrows) + 1)
            borrow_date = datetime.date.today().isoformat()
            due_date = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
            borrow = Borrow(borrow_id, member_id, book_id, borrow_date, due_date)
            self.borrows.append(borrow)
            member.borrowed_books.append(book)
            book.available = False
            self.save_books()
            self.save_borrows()
            print(f"Book '{book.title}' borrowed successfully by {member.name}. Due date: {due_date}")
        else:
            print("Invalid member or book, or book is not available.")

    def return_book(self, borrow_id):
        borrow = next((b for b in self.borrows if b.borrow_id == borrow_id), None)
        if borrow:
            member = next((m for m in self.members if m.member_id == borrow.member_id), None)
            book = next((b for b in self.books if b.book_id == borrow.book_id), None)
            if member and book:
                self.borrows.remove(borrow)
                member.borrowed_books.remove(book)
                book.available = True
                self.save_books()
                self.save_borrows()
                print(f"Book '{book.title}' returned successfully by {member.name}.")
            else:
                print("Invalid member or book found for this borrow.")
        else:
            print(f"Borrow with ID {borrow_id} not found.")

    def save_borrows(self):
        with open(BORROWS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['borrow_id', 'member_id', 'book_id', 'borrow_date', 'due_date'])
            for borrow in self.borrows:
                writer.writerow([borrow.borrow_id, borrow.member_id, borrow.book_id, borrow.borrow_date, borrow.due_date])

# Staff application
def staff_app(library):
    while True:
        print("\nStaff Application")
        print("1. Search books")
        print("2. Create book")
        print("3. Edit book")
        print("4. Delete book")
        print("5. Create member")
        print("6. Edit member")
        print("7. Delete member")
        print("8. Create reservation")
        print("9. Delete reservation")
        print("10. Borrow book")
        print("11. Return book")
        print("12. Book summary")
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
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            isbn = input("Enter ISBN: ")
            library.create_book(title, author, isbn)

        elif choice == '3':
            book_id = input("Enter book ID: ")
            new_title = input("Enter new title (or leave blank): ")
            new_author = input("Enter new author (or leave blank): ")
            new_isbn = input("Enter new ISBN (or leave blank): ")
            library.edit_book(book_id, new_title, new_author, new_isbn)

        elif choice == '4':
            book_id = input("Enter book ID: ")
            library.delete_book(book_id)

        elif choice == '5':
            name = input("Enter member name: ")
            contact = input("Enter member contact: ")
            library.create_member(name, contact)

        elif choice == '6':
            member_id = input("Enter member ID: ")
            new_name = input("Enter new name (or leave blank): ")
            new_contact = input("Enter new contact (or leave blank): ")
            library.edit_member(member_id, new_name, new_contact)

        elif choice == '7':
            member_id = input("Enter member ID: ")
            library.delete_member(member_id)

        elif choice == '8':
            member_id
            elif choice == '8':
            member_id = input("Enter member ID: ")
            book_id = input("Enter book ID: ")
            library.create_reservation(member_id, book_id)

        elif choice == '9':
            reservation_id = input("Enter reservation ID: ")
            library.delete_reservation(reservation_id)

        elif choice == '10':
            member_id = input("Enter member ID: ")
            book_id = input("Enter book ID: ")
            library.borrow_book(member_id, book_id)

        elif choice == '11':
            borrow_id = input("Enter borrow ID: ")
            library.return_book(borrow_id)

        elif choice == '12':
            summary = library.get_book_summary()
            print("\nBook Summary:")
            print(summary)

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
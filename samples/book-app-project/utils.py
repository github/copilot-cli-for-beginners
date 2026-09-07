from books import Book


def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Read and validate a menu choice from the user."""
    while True:
        choice = input("Choose an option (1-5): ").strip()

        if not choice:
            print("Please enter a choice from 1 to 5.")
            continue

        if not choice.isdigit():
            print("Please enter a numeric choice from 1 to 5.")
            continue

        if not 1 <= int(choice) <= 5:
            print("Please enter a choice from 1 to 5.")
            continue

        return choice


def get_book_details():
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Book title cannot be empty.")

    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books: list[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "Read" if book.read else "Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")

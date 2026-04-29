from datetime import date


def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details():
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")


# Year parsing and validation utility
MIN_YEAR = -5000


def parse_year(year_str: str) -> int:
    """Parse and validate a year input from the user.

    Accepts an empty string (returns 0). Raises ValueError for invalid or out-of-range values.
    """
    s = year_str.strip()
    if s == "":
        return 0

    try:
        year = int(s)
    except ValueError:
        raise ValueError("El año debe ser un entero o vacío")

    current_year = date.today().year
    if year < MIN_YEAR or year > current_year:
        raise ValueError(f"Año fuera de rango: debe estar entre {MIN_YEAR} y {current_year}")

    return year

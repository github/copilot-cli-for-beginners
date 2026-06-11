def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if choice in {"1", "2", "3", "4", "5"}:
            return choice
        print("Invalid choice. Please enter a number between 1 and 5.")


def get_book_details():
    """Prompt the user for book details and return them.

    Prompts (via standard input) for the following fields:
    - title: required. The function will re-prompt until a non-empty title is provided.
    - author: optional. An empty string is allowed.
    - publication year: optional. The function attempts to convert input to int; if conversion
      fails the year defaults to 0 and a message is printed.

    Returns:
        tuple[str, str, int]: A 3-tuple of (title, author, year).

    Side effects:
        - Prints prompts and validation messages to stdout.
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a title.")

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

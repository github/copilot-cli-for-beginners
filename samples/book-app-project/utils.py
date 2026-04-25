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
        if not choice:
            print("Please enter a choice (1-5).")
            continue
        if not choice.isdigit():
            print("Please enter a number between 1 and 5.")
            continue
        return choice


def get_book_details():
    """
    Prompt the user for book details and return them.

    Repeatedly asks for book title until a non-empty string is provided. Then
    prompts once for author and publication year. If the year cannot be parsed
    as an integer, it defaults to 0 and prints a warning.

    Returns:
        tuple: (title, author, year)
            - title (str): Non-empty book title provided by the user.
            - author (str): Author name (may be empty if user leaves it blank).
            - year (int): Publication year parsed as int, or 0 if parsing failed
              or the user left it blank.
    """
    # Ensure title is not empty
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

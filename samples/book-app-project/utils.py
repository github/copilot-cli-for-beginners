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
            print("Input cannot be empty. Please enter a number from 1 to 5.")
            continue

        if not choice.isdigit() or not (1 <= int(choice) <= 5):
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        return choice


def get_book_details():
    """Prompt the user for details of a new book.

    Interactively collects a book's title, author, and publication year
    via `input()`. The title is required and the user is re-prompted
    until a non-empty value is entered. The publication year is parsed
    as an integer; if the input is not a valid number, it defaults to 0
    and a warning is printed.

    Parameters:
        None. All values are gathered interactively from stdin.

    Returns:
        tuple[str, str, int]: A 3-tuple containing:
            - title (str): The book's title. Guaranteed non-empty.
            - author (str): The book's author. May be an empty string
              if the user provides no input.
            - year (int): The publication year, or 0 if the entered
              value could not be parsed as an integer.
    """
    title = ""
    while not title:
        title = input("Enter book title: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a book title.")

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

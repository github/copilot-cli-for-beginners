from dataclasses import dataclass
from typing import Optional
from books import Book


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


@dataclass
class CollectionStats:
    total: int
    read: int
    unread: int
    oldest: Optional[Book]
    newest: Optional[Book]


def get_collection_stats(books: list[Book]) -> CollectionStats:
    """Return statistics for a list of books."""
    if not books:
        return CollectionStats(total=0, read=0, unread=0, oldest=None, newest=None)

    read_books = [b for b in books if b.read]
    books_with_year = [b for b in books if b.year > 0]

    return CollectionStats(
        total=len(books),
        read=len(read_books),
        unread=len(books) - len(read_books),
        oldest=min(books_with_year, key=lambda b: b.year) if books_with_year else None,
        newest=max(books_with_year, key=lambda b: b.year) if books_with_year else None,
    )

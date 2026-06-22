import sys
from typing import List, Optional
from books import BookCollection, Book


# Global collection instance
collection: BookCollection = BookCollection()


def show_books(books: List[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        avg = collection.average_rating(book.title)
        avg_str = f" - Avg: {avg:.1f}/5" if avg is not None else ""
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year}){avg_str}")

    print()


def handle_list() -> None:
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_search() -> None:
    print("\nSearch Books by Title or Author\n")

    query = input("Search query: ").strip()
    books = collection.search(query)

    show_books(books)


def handle_review() -> None:
    print("\nAdd a Review (1-5 stars)\n")
    title = input("Book title: ").strip()
    book = collection.find_book_by_title(title)
    if not book:
        print("Book not found.\n")
        return

    rating_str = input("Rating (1-5): ").strip()
    try:
        rating = int(rating_str)
        text = input("Optional review text: ").strip()
        collection.add_review(title, rating, text)
        print("\nReview added.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_show_reviews() -> None:
    print("\nShow Reviews for a Book\n")
    title = input("Book title: ").strip()
    reviews = collection.get_reviews(title)
    if not reviews:
        print("No reviews found for that book.\n")
        return

    avg = collection.average_rating(title)
    if avg is not None:
        print(f"Average rating: {avg:.1f}/5\n")

    for idx, r in enumerate(reviews, start=1):
        text = r.get("text", "")
        rating = r.get("rating", "")
        print(f"{idx}. {rating}/5 - {text}")

    print()


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  search   - Search books by title or author
  review   - Add a rating and optional text review for a book
  reviews  - Show reviews for a specific book
  help     - Show this help message
""")


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "search": handle_search,
        "review": handle_review,
        "reviews": handle_show_reviews,
        "help": show_help,
    }

    handler = commands.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()

import sys
from abc import ABC, abstractmethod
from books import BookCollection, Book
from typing import List


collection = BookCollection()


def prompt_required(label: str) -> str:
    """Prompt user for required input, retrying if empty."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"  {label} cannot be empty. Please try again.")


def show_books(books: List[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")
    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")
    print()


class Command(ABC):
    """Base class for all commands."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass

    @abstractmethod
    def help(self) -> str:
        """Return help text for this command."""
        pass


class ListCommand(Command):
    def execute(self) -> None:
        books = collection.list_books()
        show_books(books)

    def help(self) -> str:
        return "Show all books"


class AddCommand(Command):
    def execute(self) -> None:
        print("\nAdd a New Book\n")
        title = prompt_required("Title")
        author = prompt_required("Author")

        year_str = input("Year (optional): ").strip()
        try:
            year = int(year_str) if year_str else 0
            collection.add_book(title, author, year)
            print("\n✓ Book added successfully.\n")
        except ValueError:
            print("\n✗ Error: Year must be a valid number.\n")

    def help(self) -> str:
        return "Add a new book"


class RemoveCommand(Command):
    def execute(self) -> None:
        print("\nRemove a Book\n")
        title = prompt_required("Enter the title of the book to remove")
        if collection.remove_book(title):
            print(f"\n✓ '{title}' removed.\n")
        else:
            print(f"\n✗ '{title}' not found.\n")

    def help(self) -> str:
        return "Remove a book by title"


class FindCommand(Command):
    def execute(self) -> None:
        print("\nFind Books by Author\n")
        author = prompt_required("Author name")
        books = collection.find_by_author(author)
        show_books(books)

    def help(self) -> str:
        return "Find books by author (exact match)"


class SearchCommand(Command):
    def execute(self) -> None:
        query = sys.argv[2] if len(sys.argv) >= 3 else prompt_required("Query")
        field = sys.argv[3].lower() if len(sys.argv) >= 4 else "title"

        if field not in ("title", "author"):
            print(f"\n✗ Field must be 'title' or 'author', not '{field}'.\n")
            return

        books = collection.search_books(query, field)
        show_books(books)

    def help(self) -> str:
        return "Search books by title or author (partial). Usage: search <query> [title|author]"


class HelpCommand(Command):
    def __init__(self, commands: dict):
        self.commands = commands

    def execute(self) -> None:
        self._print_help()

    def _print_help(self) -> None:
        print("\nBook Collection Helper\n")
        print("Commands:")
        for name, cmd in self.commands.items():
            print(f"  {name:<8} - {cmd.help()}")
        print()

    def help(self) -> str:
        return "Show this help message"


class CommandDispatcher:
    """Manages command registration and execution."""

    def __init__(self):
        self.commands = {
            "list": ListCommand(),
            "add": AddCommand(),
            "remove": RemoveCommand(),
            "find": FindCommand(),
            "search": SearchCommand(),
        }
        self.commands["help"] = HelpCommand(self.commands)

    def dispatch(self, command_name: str) -> None:
        """Execute a command by name."""
        command = self.commands.get(command_name.lower())
        if command:
            command.execute()
        else:
            print(f"✗ Unknown command: '{command_name}'.\n")
            self.commands["help"].execute()

    def run(self) -> None:
        """Main entry point."""
        if len(sys.argv) < 2:
            self.commands["help"].execute()
        else:
            self.dispatch(sys.argv[1])


def main() -> None:
    dispatcher = CommandDispatcher()
    dispatcher.run()


if __name__ == "__main__":
    main()

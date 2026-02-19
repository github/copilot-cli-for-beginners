using BookApp.Models;
using BookApp.Services;

var collection = new BookCollection();

void ShowBooks(List<Book> books)
{
    if (books.Count == 0)
    {
        Console.WriteLine("No books found.");
        return;
    }

    Console.WriteLine("\nYour Book Collection:\n");

    for (int i = 0; i < books.Count; i++)
    {
        var book = books[i];
        var status = book.Read ? "✓" : " ";
        Console.WriteLine($"{i + 1}. [{status}] {book.Title} by {book.Author} ({book.Year})");
    }

    Console.WriteLine();
}

void HandleList()
{
    var books = collection.ListBooks();
    ShowBooks(books);
}

void HandleAdd()
{
    Console.WriteLine("\nAdd a New Book\n");

    Console.Write("Title: ");
    var title = Console.ReadLine()?.Trim() ?? "";

    Console.Write("Author: ");
    var author = Console.ReadLine()?.Trim() ?? "";

    Console.Write("Year: ");
    var yearStr = Console.ReadLine()?.Trim() ?? "";

    if (int.TryParse(yearStr, out var year))
    {
        collection.AddBook(title, author, year);
        Console.WriteLine("\nBook added successfully.\n");
    }
    else
    {
        Console.WriteLine($"\nError: '{yearStr}' is not a valid year.\n");
    }
}

void HandleRemove()
{
    Console.WriteLine("\nRemove a Book\n");

    Console.Write("Enter the title of the book to remove: ");
    var title = Console.ReadLine()?.Trim() ?? "";
    collection.RemoveBook(title);

    Console.WriteLine("\nBook removed if it existed.\n");
}

void HandleFind()
{
    Console.WriteLine("\nFind Books by Author\n");

    Console.Write("Author name: ");
    var author = Console.ReadLine()?.Trim() ?? "";
    var books = collection.FindByAuthor(author);

    ShowBooks(books);
}

void ShowHelp()
{
    Console.WriteLine("""

    Book Collection Helper

    Commands:
      list     - Show all books
      add      - Add a new book
      remove   - Remove a book by title
      find     - Find books by author
      help     - Show this help message
    """);
}

if (args.Length == 0)
{
    ShowHelp();
    return;
}

var command = args[0].ToLower();

switch (command)
{
    case "list":
        HandleList();
        break;
    case "add":
        HandleAdd();
        break;
    case "remove":
        HandleRemove();
        break;
    case "find":
        HandleFind();
        break;
    case "help":
        ShowHelp();
        break;
    default:
        Console.WriteLine("Unknown command.\n");
        ShowHelp();
        break;
}

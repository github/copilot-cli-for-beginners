using BookApp.Models;
using BookApp.Services;

var collection = new BookCollection();

void ShowBooks(List<Book> books, string emptyMessage = "No books found.")
{
    if (books.Count == 0)
    {
        Console.WriteLine(emptyMessage);
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

void HandleListUnread()
{
    var books = collection.GetUnreadBooks();
    ShowBooks(books, "No unread books found.");
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

void HandleMarkRead()
{
    Console.WriteLine("\nMark a Book as Read\n");

    Console.Write("Enter the title of the book to mark as read: ");
    var title = Console.ReadLine()?.Trim() ?? "";

    if (collection.MarkAsRead(title))
    {
        Console.WriteLine("\nBook marked as read.\n");
    }
    else
    {
        Console.WriteLine($"\nNo book found with title '{title}'.\n");
    }
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
      list        - Show all books
      list-unread - Show only unread books
      add         - Add a new book
      remove      - Remove a book by title
      mark-read   - Mark a book as read by title
      find        - Find books by author
      help        - Show this help message
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
    case "list-unread":
        HandleListUnread();
        break;
    case "add":
        HandleAdd();
        break;
    case "remove":
        HandleRemove();
        break;
    case "mark-read":
        HandleMarkRead();
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

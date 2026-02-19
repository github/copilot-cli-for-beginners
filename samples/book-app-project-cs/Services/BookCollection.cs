using System.Text.Json;
using BookApp.Models;

namespace BookApp.Services;

public class BookCollection
{
    private readonly string _dataFile;
    private List<Book> _books = [];

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true
    };

    public BookCollection(string? dataFile = null)
    {
        _dataFile = dataFile ?? Path.Combine(AppContext.BaseDirectory, "data.json");
        LoadBooks();
    }

    public IReadOnlyList<Book> Books => _books;

    private void LoadBooks()
    {
        try
        {
            var json = File.ReadAllText(_dataFile);
            _books = JsonSerializer.Deserialize<List<Book>>(json, JsonOptions) ?? [];
        }
        catch (FileNotFoundException)
        {
            _books = [];
        }
        catch (JsonException)
        {
            Console.WriteLine("Warning: data.json is corrupted. Starting with empty collection.");
            _books = [];
        }
    }

    private void SaveBooks()
    {
        var json = JsonSerializer.Serialize(_books, JsonOptions);
        File.WriteAllText(_dataFile, json);
    }

    public Book AddBook(string title, string author, int year)
    {
        var book = new Book { Title = title, Author = author, Year = year };
        _books.Add(book);
        SaveBooks();
        return book;
    }

    public List<Book> ListBooks() => _books;

    public Book? FindBookByTitle(string title)
    {
        return _books.Find(b => b.Title.Equals(title, StringComparison.OrdinalIgnoreCase));
    }

    public bool MarkAsRead(string title)
    {
        var book = FindBookByTitle(title);
        if (book is null) return false;
        book.Read = true;
        SaveBooks();
        return true;
    }

    public bool RemoveBook(string title)
    {
        var book = FindBookByTitle(title);
        if (book is null) return false;
        _books.Remove(book);
        SaveBooks();
        return true;
    }

    public List<Book> FindByAuthor(string author)
    {
        return _books
            .Where(b => b.Author.Equals(author, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }
}

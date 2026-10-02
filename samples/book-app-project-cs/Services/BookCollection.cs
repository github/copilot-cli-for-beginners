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
            var books = JsonSerializer.Deserialize<List<Book>>(json, JsonOptions);
            _books = books ?? [];
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
        var directory = Path.GetDirectoryName(_dataFile);
        if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        var json = JsonSerializer.Serialize(_books, JsonOptions);
        File.WriteAllText(_dataFile, json);
    }

    public Book AddBook(string title, string author, int year)
    {
        var cleanTitle = title.Trim();
        var cleanAuthor = author.Trim();
        if (string.IsNullOrWhiteSpace(cleanTitle) || string.IsNullOrWhiteSpace(cleanAuthor))
        {
            throw new ArgumentException("Title and author are required.");
        }

        if (year <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(year), "Year must be a positive integer.");
        }

        var book = new Book { Title = cleanTitle, Author = cleanAuthor, Year = year };
        _books.Add(book);
        SaveBooks();
        return book;
    }

    public List<Book> ListBooks() => _books;

    public Book? FindBookByTitle(string title)
    {
        return _books.Find(b => b.Title.Equals(title.Trim(), StringComparison.OrdinalIgnoreCase));
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
        var normalized = author.Trim();
        if (string.IsNullOrWhiteSpace(normalized))
        {
            return [];
        }

        return _books
            .Where(b => b.Author.Contains(normalized, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }
}

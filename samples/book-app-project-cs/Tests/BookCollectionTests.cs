using BookApp.Services;

namespace BookApp.Tests;

public class BookCollectionTests : IDisposable
{
    private readonly string _tempFile;
    private readonly BookCollection _collection;

    public BookCollectionTests()
    {
        _tempFile = Path.GetTempFileName();
        File.WriteAllText(_tempFile, "[]");
        _collection = new BookCollection(_tempFile);
    }

    public void Dispose()
    {
        if (File.Exists(_tempFile)) File.Delete(_tempFile);
    }

    [Fact]
    public void AddBook_ShouldAddAndPersist()
    {
        var initialCount = _collection.Books.Count;
        _collection.AddBook("1984", "George Orwell", 1949);

        Assert.Equal(initialCount + 1, _collection.Books.Count);

        var book = _collection.FindBookByTitle("1984");
        Assert.NotNull(book);
        Assert.Equal("George Orwell", book.Author);
        Assert.Equal(1949, book.Year);
        Assert.False(book.Read);
    }

    [Fact]
    public void MarkAsRead_ShouldSetReadTrue()
    {
        _collection.AddBook("Dune", "Frank Herbert", 1965);
        var result = _collection.MarkAsRead("Dune");

        Assert.True(result);
        Assert.True(_collection.FindBookByTitle("Dune")!.Read);
    }

    [Fact]
    public void MarkAsRead_NonexistentBook_ShouldReturnFalse()
    {
        var result = _collection.MarkAsRead("Nonexistent Book");
        Assert.False(result);
    }

    [Fact]
    public void RemoveBook_ShouldRemoveExistingBook()
    {
        _collection.AddBook("The Hobbit", "J.R.R. Tolkien", 1937);
        var result = _collection.RemoveBook("The Hobbit");

        Assert.True(result);
        Assert.Null(_collection.FindBookByTitle("The Hobbit"));
    }

    [Fact]
    public void RemoveBook_NonexistentBook_ShouldReturnFalse()
    {
        var result = _collection.RemoveBook("Nonexistent Book");
        Assert.False(result);
    }

    [Fact]
    public void GetUnreadBooks_ShouldReturnOnlyUnreadBooks()
    {
        _collection.AddBook("The Hobbit", "J.R.R. Tolkien", 1937);
        _collection.AddBook("1984", "George Orwell", 1949);
        _collection.AddBook("Dune", "Frank Herbert", 1965);
        _collection.MarkAsRead("1984");

        var unread = _collection.GetUnreadBooks();

        Assert.Equal(2, unread.Count);
        Assert.All(unread, b => Assert.False(b.Read));
        Assert.Contains(unread, b => b.Title == "The Hobbit");
        Assert.Contains(unread, b => b.Title == "Dune");
        Assert.DoesNotContain(unread, b => b.Title == "1984");
    }

    [Fact]
    public void GetUnreadBooks_EmptyCollection_ShouldReturnEmpty()
    {
        var unread = _collection.GetUnreadBooks();
        Assert.Empty(unread);
    }

    [Fact]
    public void GetUnreadBooks_AllRead_ShouldReturnEmpty()
    {
        _collection.AddBook("The Hobbit", "J.R.R. Tolkien", 1937);
        _collection.AddBook("Dune", "Frank Herbert", 1965);
        _collection.MarkAsRead("The Hobbit");
        _collection.MarkAsRead("Dune");

        var unread = _collection.GetUnreadBooks();

        Assert.Empty(unread);
    }

    [Fact]
    public void GetUnreadBooks_AllUnread_ShouldReturnAll()
    {
        _collection.AddBook("The Hobbit", "J.R.R. Tolkien", 1937);
        _collection.AddBook("Dune", "Frank Herbert", 1965);

        var unread = _collection.GetUnreadBooks();

        Assert.Equal(2, unread.Count);
    }
}

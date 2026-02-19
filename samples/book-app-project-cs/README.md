# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A C# console app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `Program.cs` - Main CLI entry point
* `Models/Book.cs` - Book model class
* `Services/BookCollection.cs` - BookCollection class with data logic
* `data.json` - Sample book data
* `Tests/BookCollectionTests.cs` - xUnit tests

---

## Running the App

```bash
dotnet run -- list
dotnet run -- add
dotnet run -- find
dotnet run -- remove
dotnet run -- help
```

## Running Tests

```bash
cd Tests
dotnet test
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later

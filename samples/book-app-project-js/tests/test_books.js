const { describe, it, beforeEach } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { BookCollection } = require("../books");

let tempFile;

beforeEach(() => {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "book-test-"));
  tempFile = path.join(tempDir, "data.json");
  fs.writeFileSync(tempFile, "[]");
});

describe("BookCollection", () => {
  it("should add a book", () => {
    const collection = new BookCollection(tempFile);
    const initialCount = collection.books.length;
    collection.addBook("1984", "George Orwell", 1949);
    assert.equal(collection.books.length, initialCount + 1);
    const book = collection.findBookByTitle("1984");
    assert.notEqual(book, null);
    assert.equal(book.author, "George Orwell");
    assert.equal(book.year, 1949);
    assert.equal(book.read, false);
  });

  it("should mark a book as read", () => {
    const collection = new BookCollection(tempFile);
    collection.addBook("Dune", "Frank Herbert", 1965);
    const result = collection.markAsRead("Dune");
    assert.equal(result, true);
    const book = collection.findBookByTitle("Dune");
    assert.equal(book.read, true);
  });

  it("should return false when marking a nonexistent book as read", () => {
    const collection = new BookCollection(tempFile);
    const result = collection.markAsRead("Nonexistent Book");
    assert.equal(result, false);
  });

  it("should remove a book", () => {
    const collection = new BookCollection(tempFile);
    collection.addBook("The Hobbit", "J.R.R. Tolkien", 1937);
    const result = collection.removeBook("The Hobbit");
    assert.equal(result, true);
    const book = collection.findBookByTitle("The Hobbit");
    assert.equal(book, null);
  });

  it("should return false when removing a nonexistent book", () => {
    const collection = new BookCollection(tempFile);
    const result = collection.removeBook("Nonexistent Book");
    assert.equal(result, false);
  });

  it("should find books by partial author match", () => {
    const collection = new BookCollection(tempFile);
    collection.addBook("Dune", "Frank Herbert", 1965);
    collection.addBook("The Hobbit", "J.R.R. Tolkien", 1937);

    const matches = collection.findByAuthor("tolkien");

    assert.deepEqual(matches.map((book) => book.title), ["The Hobbit"]);
  });

  it("should validate required data before adding a book", () => {
    const collection = new BookCollection(tempFile);

    assert.throws(() => collection.addBook("   ", "George Orwell", 1949), /Title and author are required/);
    assert.throws(() => collection.addBook("1984", "George Orwell", 0), /Year must be a positive integer/);
  });
});

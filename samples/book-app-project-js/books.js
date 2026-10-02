const fs = require("fs");
const path = require("path");

const DATA_FILE = path.join(__dirname, "data.json");

class Book {
  constructor(title, author, year, read = false) {
    this.title = title;
    this.author = author;
    this.year = year;
    this.read = read;
  }
}

class BookCollection {
  constructor(dataFile = DATA_FILE) {
    this.dataFile = dataFile;
    this.books = [];
    this.loadBooks();
  }

  loadBooks() {
    try {
      const raw = fs.readFileSync(this.dataFile, "utf-8");
      const data = JSON.parse(raw);
      if (!Array.isArray(data)) {
        this.books = [];
        return;
      }
      this.books = data
        .filter((item) => item && typeof item === "object")
        .map((b) => new Book(b.title, b.author, b.year, !!b.read));
    } catch (err) {
      if (err.code === "ENOENT") {
        this.books = [];
      } else if (err instanceof SyntaxError) {
        console.log("Warning: data.json is corrupted. Starting with empty collection.");
        this.books = [];
      } else {
        throw err;
      }
    }
  }

  saveBooks() {
    const dir = path.dirname(this.dataFile);
    if (dir && !fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    const data = this.books.map((b) => ({
      title: b.title,
      author: b.author,
      year: b.year,
      read: b.read,
    }));
    fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2));
  }

  addBook(title, author, year) {
    const cleanTitle = String(title).trim();
    const cleanAuthor = String(author).trim();
    if (!cleanTitle || !cleanAuthor) {
      throw new Error("Title and author are required.");
    }

    const numericYear = Number.parseInt(year, 10);
    if (Number.isNaN(numericYear) || numericYear <= 0) {
      throw new Error("Year must be a positive integer.");
    }

    const book = new Book(cleanTitle, cleanAuthor, numericYear);
    this.books.push(book);
    this.saveBooks();
    return book;
  }

  listBooks() {
    return this.books;
  }

  findBookByTitle(title) {
    const normalizedTitle = String(title).trim().toLowerCase();
    return this.books.find((b) => b.title.trim().toLowerCase() === normalizedTitle) || null;
  }

  markAsRead(title) {
    const book = this.findBookByTitle(title);
    if (book) {
      book.read = true;
      this.saveBooks();
      return true;
    }
    return false;
  }

  removeBook(title) {
    const book = this.findBookByTitle(title);
    if (book) {
      this.books = this.books.filter((b) => b !== book);
      this.saveBooks();
      return true;
    }
    return false;
  }

  findByAuthor(author) {
    const normalizedAuthor = String(author).trim().toLowerCase();
    if (!normalizedAuthor) {
      return [];
    }
    return this.books.filter((b) => b.author.trim().toLowerCase().includes(normalizedAuthor));
  }
}

module.exports = { Book, BookCollection, DATA_FILE };

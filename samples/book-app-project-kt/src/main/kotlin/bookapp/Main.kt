package bookapp

import bookapp.models.Book
import bookapp.services.BookCollection

fun showBooks(books: List<Book>) {
    if (books.isEmpty()) {
        println("No books found.")
        return
    }

    println("\nYour Book Collection:\n")

    books.forEachIndexed { index, book ->
        val status = if (book.read) "✓" else " "
        println("${index + 1}. [$status] ${book.title} by ${book.author} (${book.year})")
    }

    println()
}

fun handleList(collection: BookCollection) {
    val books = collection.listBooks()
    showBooks(books)
}

fun handleAdd(collection: BookCollection) {
    println("\nAdd a New Book\n")

    print("Title: ")
    val title = readlnOrNull()?.trim() ?: ""

    print("Author: ")
    val author = readlnOrNull()?.trim() ?: ""

    print("Year: ")
    val yearStr = readlnOrNull()?.trim() ?: ""

    val year = yearStr.toIntOrNull()
    if (year != null) {
        collection.addBook(title, author, year)
        println("\nBook added successfully.\n")
    } else {
        println("\nError: '$yearStr' is not a valid year.\n")
    }
}

fun handleRemove(collection: BookCollection) {
    println("\nRemove a Book\n")

    print("Enter the title of the book to remove: ")
    val title = readlnOrNull()?.trim() ?: ""
    collection.removeBook(title)

    println("\nBook removed if it existed.\n")
}

fun handleFind(collection: BookCollection) {
    println("\nFind Books by Author\n")

    print("Author name: ")
    val author = readlnOrNull()?.trim() ?: ""
    val books = collection.findByAuthor(author)

    showBooks(books)
}

fun handleRead(collection: BookCollection) {
    println("\nMark a Book as Read\n")

    print("Enter the title of the book: ")
    val title = readlnOrNull()?.trim() ?: ""
    
    if (collection.markAsRead(title)) {
        println("\nBook marked as read.\n")
    } else {
        println("\nBook not found.\n")
    }
}

fun showHelp() {
    println(
        """
        
    Book Collection Helper

    Commands:
      list     - Show all books
      add      - Add a new book
      read     - Mark a book as read
      remove   - Remove a book by title
      find     - Find books by author
      help     - Show this help message
        """.trimEnd()
    )
}

fun main(args: Array<String>) {
    val collection = BookCollection()

    if (args.isEmpty()) {
        showHelp()
        return
    }

    when (args[0].lowercase()) {
        "list"   -> handleList(collection)
        "add"    -> handleAdd(collection)
        "read"   -> handleRead(collection)
        "remove" -> handleRemove(collection)
        "find"   -> handleFind(collection)
        "help"   -> showHelp()
        else     -> {
            println("Unknown command.\n")
            showHelp()
        }
    }
}

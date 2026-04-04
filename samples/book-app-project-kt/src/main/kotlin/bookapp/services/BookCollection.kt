package bookapp.services

import bookapp.models.Book
import bookapp.models.BookStats
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.File
import java.io.FileNotFoundException

class BookCollection(dataFile: String? = null) {

    private val dataFile: String = dataFile
        ?: (javaClass.getResource("/data.json")?.toURI()?.let { File(it).absolutePath }
            ?: "data.json")

    private var books: MutableList<Book> = mutableListOf()

    private val gson: Gson = GsonBuilder().setPrettyPrinting().create()

    init {
        loadBooks()
    }

    val allBooks: List<Book>
        get() = books

    private fun loadBooks() {
        try {
            val json = File(dataFile).readText()
            val type = object : TypeToken<MutableList<Book>>() {}.type
            books = gson.fromJson(json, type) ?: mutableListOf()
        } catch (_: FileNotFoundException) {
            books = mutableListOf()
        } catch (e: Exception) {
            println("Warning: data.json is corrupted. Starting with empty collection.")
            books = mutableListOf()
        }
    }

    private fun saveBooks() {
        val json = gson.toJson(books)
        File(dataFile).writeText(json)
    }

    fun addBook(title: String, author: String, year: Int): Book {
        val book = Book(title = title, author = author, year = year)
        books.add(book)
        saveBooks()
        return book
    }

    fun listBooks(): List<Book> = books

    fun findBookByTitle(title: String): Book? {
        return books.find { it.title.equals(title, ignoreCase = true) }
    }

    fun markAsRead(title: String): Boolean {
        val book = findBookByTitle(title) ?: return false
        book.read = true
        saveBooks()
        return true
    }

    fun removeBook(title: String): Boolean {
        val book = findBookByTitle(title) ?: return false
        books.remove(book)
        saveBooks()
        return true
    }

    fun findByAuthor(author: String): List<Book> {
        return books.filter { it.author.equals(author, ignoreCase = true) }
    }

    fun getStatistics(bookList: List<Book> = books): BookStats {
        return BookStats(
            totalCount = bookList.size,
            readCount = bookList.count { it.read },
            unreadCount = bookList.count { !it.read },
            oldestBook = bookList.minByOrNull { it.year },
            newestBook = bookList.maxByOrNull { it.year }
        )
    }
}

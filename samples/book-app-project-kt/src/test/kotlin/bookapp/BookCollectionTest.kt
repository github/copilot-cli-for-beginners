package bookapp

import bookapp.services.BookCollection
import java.io.File
import kotlin.test.*

class BookCollectionTest {

    private lateinit var tempFile: File
    private lateinit var collection: BookCollection

    @BeforeTest
    fun setUp() {
        tempFile = File.createTempFile("books", ".json")
        tempFile.writeText("[]")
        collection = BookCollection(tempFile.absolutePath)
    }

    @AfterTest
    fun tearDown() {
        if (tempFile.exists()) tempFile.delete()
    }

    @Test
    fun `addBook should add and persist`() {
        val initialCount = collection.allBooks.size
        collection.addBook("1984", "George Orwell", 1949)

        assertEquals(initialCount + 1, collection.allBooks.size)

        val book = collection.findBookByTitle("1984")
        assertNotNull(book)
        assertEquals("George Orwell", book.author)
        assertEquals(1949, book.year)
        assertFalse(book.read)
    }

    @Test
    fun `markAsRead should set read to true`() {
        collection.addBook("Dune", "Frank Herbert", 1965)
        val result = collection.markAsRead("Dune")

        assertTrue(result)
        assertTrue(collection.findBookByTitle("Dune")!!.read)
    }

    @Test
    fun `markAsRead nonexistent book should return false`() {
        val result = collection.markAsRead("Nonexistent Book")
        assertFalse(result)
    }

    @Test
    fun `removeBook should remove existing book`() {
        collection.addBook("The Hobbit", "J.R.R. Tolkien", 1937)
        val result = collection.removeBook("The Hobbit")

        assertTrue(result)
        assertNull(collection.findBookByTitle("The Hobbit"))
    }

    @Test
    fun `removeBook nonexistent book should return false`() {
        val result = collection.removeBook("Nonexistent Book")
        assertFalse(result)
    }

    @Test
    fun `getStatistics should return correct counts`() {
        collection.addBook("1984", "George Orwell", 1949)
        collection.addBook("Dune", "Frank Herbert", 1965)
        collection.addBook("Neuromancer", "William Gibson", 1984)
        collection.markAsRead("Dune")

        val stats = collection.getStatistics()

        assertEquals(3, stats.totalCount)
        assertEquals(1, stats.readCount)
        assertEquals(2, stats.unreadCount)
    }

    @Test
    fun `getStatistics should find oldest and newest books`() {
        collection.addBook("1984", "George Orwell", 1949)
        collection.addBook("Dune", "Frank Herbert", 1965)
        collection.addBook("Neuromancer", "William Gibson", 1984)

        val stats = collection.getStatistics()

        assertEquals("1984", stats.oldestBook?.title)
        assertEquals("Neuromancer", stats.newestBook?.title)
    }

    @Test
    fun `getStatistics on empty list should return zeros and nulls`() {
        val stats = collection.getStatistics()

        assertEquals(0, stats.totalCount)
        assertEquals(0, stats.readCount)
        assertEquals(0, stats.unreadCount)
        assertNull(stats.oldestBook)
        assertNull(stats.newestBook)
    }

    @Test
    fun `getStatistics should accept custom book list`() {
        collection.addBook("1984", "George Orwell", 1949)
        collection.addBook("Dune", "Frank Herbert", 1965)
        collection.addBook("Neuromancer", "William Gibson", 1984)

        val subset = collection.findByAuthor("Frank Herbert")
        val stats = collection.getStatistics(subset)

        assertEquals(1, stats.totalCount)
        assertEquals("Dune", stats.oldestBook?.title)
        assertEquals("Dune", stats.newestBook?.title)
    }
}

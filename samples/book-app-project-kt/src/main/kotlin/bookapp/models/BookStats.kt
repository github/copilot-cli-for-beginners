package bookapp.models

data class BookStats(
    val totalCount: Int,
    val readCount: Int,
    val unreadCount: Int,
    val oldestBook: Book?,
    val newestBook: Book?
)

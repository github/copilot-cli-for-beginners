package bookapp.models

data class SearchCriteria(
    val searchText: String? = null,
    val yearFrom: Int? = null,
    val yearTo: Int? = null,
    val readStatus: Boolean? = null
)

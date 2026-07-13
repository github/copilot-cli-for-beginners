"""Custom exception hierarchy shared across the book app modules.

Using a common base class lets callers catch `BookAppError` when they
just want to report a failure generically, or catch a specific
subclass when they need to react differently (e.g. re-prompt on
`ValidationError` vs. warn-and-continue on `StorageError`).
"""


class BookAppError(Exception):
    """Base class for all application-specific errors."""


class ValidationError(BookAppError):
    """Raised when user-supplied book data fails validation."""


class BookNotFoundError(BookAppError):
    """Raised when an operation targets a book that doesn't exist."""


class StorageError(BookAppError):
    """Raised when reading or writing the data file fails."""

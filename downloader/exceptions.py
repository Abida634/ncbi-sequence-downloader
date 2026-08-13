"""Custom exception classes for the downloader package."""


class DownloaderError(Exception):
    """Base exception for all errors raised by this package."""
    pass


class ValidationError(DownloaderError):
    """Base exception for all input validation failures."""
    pass


class InvalidAccessionError(ValidationError):
    """Raised when a given accession number does not match the expected format."""
    pass


class InvalidGeneIdError(ValidationError):
    """Raised when a given Gene ID is not a valid positive integer."""
    pass


class EmptyInputError(ValidationError):
    """Raised when a required input string is empty or whitespace-only."""
    pass
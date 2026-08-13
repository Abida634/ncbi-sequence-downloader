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

class NetworkError(DownloaderError):
    """Raised when a network-related failure occurs while contacting NCBI."""
    pass


class NoResultsFoundError(DownloaderError):
    """Raised when a search query returns no matching records."""
    pass


class FetchError(DownloaderError):
    """Raised when fetching a record from NCBI fails."""
    pass

class ParsingError(DownloaderError):
    """Raised when raw sequence text cannot be parsed into a structured record."""
    pass

class UnsupportedFormatError(DownloaderError):
    """Raised when a requested download format is not FASTA or GenBank."""
    pass


class FileSaveError(DownloaderError):
    """Raised when a downloaded record cannot be written to disk."""
    pass

class HistoryError(DownloaderError):
    """Raised when the download history file cannot be read or written."""
    pass
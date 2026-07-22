"""
Custom exception hierarchy for the NCBI Sequence Downloader.

All exceptions raised by our own code (as opposed to exceptions raised
by third-party libraries like Biopython or requests) inherit from
NCBIDownloaderError. This lets calling code choose to catch our
errors broadly or narrowly, as needed.
"""


class NCBIDownloaderError(Exception):
    """Base class for all custom exceptions in this application."""


class InvalidAccessionError(NCBIDownloaderError):
    """Raised when a user-supplied accession number is malformed."""


class InvalidGeneIDError(NCBIDownloaderError):
    """Raised when a user-supplied Gene ID is not a valid positive integer."""


class InvalidDatabaseError(NCBIDownloaderError):
    """Raised when a requested NCBI database name is not supported."""
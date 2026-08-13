"""Input validation utilities."""

from downloader.exceptions import DownloaderError


def is_non_empty(value: str) -> bool:
    """Return True if the given string is non-empty after stripping whitespace."""
    return bool(value and value.strip())
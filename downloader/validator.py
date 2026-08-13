"""Input validation utilities for accession numbers and Gene IDs."""

import re

from downloader.exceptions import (
    EmptyInputError,
    InvalidAccessionError,
    InvalidGeneIdError,
)

# Matches things like: NM_001301717  or  NM_001301717.3  or  NC_000913
ACCESSION_PATTERN = re.compile(r"^[A-Za-z]{1,2}_\d{5,}(\.\d+)?$")


def validate_accession(value: str) -> str:
    """Validate an NCBI accession number.

    Args:
        value: The raw accession string provided by the user.

    Returns:
        The cleaned (stripped, uppercase) accession string.

    Raises:
        EmptyInputError: If the value is empty or whitespace-only.
        InvalidAccessionError: If the value does not match accession format.
    """
    if not value or not value.strip():
        raise EmptyInputError("Accession number cannot be empty.")

    cleaned = value.strip().upper()

    if not ACCESSION_PATTERN.match(cleaned):
        raise InvalidAccessionError(
            f"'{value}' is not a valid accession number. "
            f"Expected format like 'NM_001301717' or 'NM_001301717.3'."
        )

    return cleaned


def validate_gene_id(value: str) -> str:
    """Validate an NCBI Gene ID.

    Args:
        value: The raw Gene ID string provided by the user.

    Returns:
        The cleaned Gene ID string.

    Raises:
        EmptyInputError: If the value is empty or whitespace-only.
        InvalidGeneIdError: If the value is not a positive integer.
    """
    if not value or not value.strip():
        raise EmptyInputError("Gene ID cannot be empty.")

    cleaned = value.strip()

    if not cleaned.isdigit() or int(cleaned) <= 0:
        raise InvalidGeneIdError(
            f"'{value}' is not a valid Gene ID. Expected a positive integer, e.g. '7157'."
        )

    return cleaned
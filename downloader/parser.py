"""
Sequence file parsing for the NCBI Sequence Downloader.

This module reads FASTA and GenBank files (or raw text content) from
disk and converts them into Biopython SeqRecord objects, which the
rest of the application uses for statistics and metadata extraction.
"""

from pathlib import Path

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from downloader.exceptions import SequenceParseError

# Maps our file extensions to the format name Biopython's SeqIO expects.
_EXTENSION_TO_FORMAT = {
    "fasta": "fasta",
    "fa": "fasta",
    "gb": "genbank",
    "gbk": "genbank",
}


def parse_file(file_path: Path) -> list[SeqRecord]:
    """
    Parse a FASTA or GenBank file into a list of SeqRecord objects.

    Args:
        file_path: Path to a .fasta, .fa, .gb, or .gbk file.

    Returns:
        A list of SeqRecord objects, one per record found in the file
        (a file may contain a single record or many).

    Raises:
        SequenceParseError: If the file extension is unrecognized or
            the file cannot be parsed.
    """
    extension = file_path.suffix.lstrip(".").lower()

    if extension not in _EXTENSION_TO_FORMAT:
        raise SequenceParseError(
            f"Unrecognized file extension '{extension}' for '{file_path}'. "
            f"Expected one of: {list(_EXTENSION_TO_FORMAT.keys())}."
        )

    file_format = _EXTENSION_TO_FORMAT[extension]

    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            records = list(SeqIO.parse(handle, file_format))
    except Exception as exc:
        raise SequenceParseError(f"Failed to parse '{file_path}': {exc}") from exc

    if not records:
        raise SequenceParseError(f"No sequence records found in '{file_path}'.")

    return records


def parse_single_record(file_path: Path) -> SeqRecord:
    """
    Parse a file that is expected to contain exactly one record.

    Args:
        file_path: Path to a .fasta, .fa, .gb, or .gbk file.

    Returns:
        The single SeqRecord found in the file.

    Raises:
        SequenceParseError: If the file contains zero records, more
            than one record, or cannot be parsed.
    """
    records = parse_file(file_path)

    if len(records) > 1:
        raise SequenceParseError(
            f"Expected exactly one record in '{file_path}', found {len(records)}."
        )

    return records[0]
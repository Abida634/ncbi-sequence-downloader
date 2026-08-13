"""Parses raw FASTA/GenBank text into structured Biopython SeqRecord objects."""

import io

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from downloader.exceptions import ParsingError


def parse_fasta(raw_text: str) -> SeqRecord:
    """Parse raw FASTA text into a single SeqRecord.

    Args:
        raw_text: Raw FASTA-formatted text (e.g. from EntrezClient.fetch_fasta).

    Returns:
        A Biopython SeqRecord representing the parsed sequence.

    Raises:
        ParsingError: If the text cannot be parsed as valid FASTA.
    """
    return _parse(raw_text, fmt="fasta")


def parse_genbank(raw_text: str) -> SeqRecord:
    """Parse raw GenBank text into a single SeqRecord.

    Args:
        raw_text: Raw GenBank-formatted text (e.g. from EntrezClient.fetch_genbank).

    Returns:
        A Biopython SeqRecord representing the parsed record, including
        rich annotations and features.

    Raises:
        ParsingError: If the text cannot be parsed as valid GenBank.
    """
    return _parse(raw_text, fmt="genbank")


def _parse(raw_text: str, fmt: str) -> SeqRecord:
    """Shared parsing logic for both FASTA and GenBank formats.

    Args:
        raw_text: Raw sequence text.
        fmt: Biopython format name, either "fasta" or "genbank".

    Raises:
        ParsingError: If parsing fails for any reason.
    """
    handle = io.StringIO(raw_text)

    try:
        record = SeqIO.read(handle, fmt)
    except (ValueError, StopIteration) as exc:
        raise ParsingError(f"Failed to parse data as '{fmt}': {exc}") from exc
    finally:
        handle.close()

    return record
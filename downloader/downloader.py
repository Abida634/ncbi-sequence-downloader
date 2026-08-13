"""Orchestrates the full download workflow: validate, search, fetch, parse, save."""

from dataclasses import dataclass
from pathlib import Path

from Bio.SeqRecord import SeqRecord

from downloader.config import Config
from downloader.entrez_client import EntrezClient
from downloader.exceptions import UnsupportedFormatError
from downloader.file_manager import FileManager
from downloader.parser import parse_fasta, parse_genbank
from downloader.validator import validate_accession

# Maps our download format to the NCBI database we search by default.
# (We default to "nucleotide" for now; Step 10+ can expand this for proteins.)
DEFAULT_DATABASE = "nucleotide"


@dataclass
class DownloadResult:
    """The outcome of a successful download: the parsed record and where it was saved."""

    record: SeqRecord
    saved_path: Path


class Downloader:
    """High-level facade that coordinates validation, fetching, parsing, and saving."""

    def __init__(self, config: Config) -> None:
        """Initialize the downloader and its internal collaborators.

        Args:
            config: Application configuration (email, output directory, etc.)
        """
        self._client = EntrezClient(config)
        self._file_manager = FileManager(config.output_dir)

    def download(
        self, accession: str, fmt: str = "fasta", database: str = DEFAULT_DATABASE
    ) -> DownloadResult:
        """Download and save a single sequence record by accession number.

        Args:
            accession: The accession number to download (e.g. "NM_001301717").
            fmt: Either "fasta" or "genbank".
            database: The NCBI database to search (default "nucleotide").

        Returns:
            A DownloadResult containing the parsed SeqRecord and saved file path.

        Raises:
            ValidationError: If the accession is malformed.
            UnsupportedFormatError: If fmt is not "fasta" or "genbank".
            NetworkError / NoResultsFoundError / FetchError: On NCBI communication issues.
            ParsingError: If NCBI's response can't be parsed.
            FileSaveError: If the file can't be written to disk.
        """
        if fmt not in ("fasta", "genbank"):
            raise UnsupportedFormatError(
                f"'{fmt}' is not supported. Use 'fasta' or 'genbank'."
            )

        clean_accession = validate_accession(accession)

        ids = self._client.search(database=database, term=clean_accession)
        record_id = ids[0]

        if fmt == "fasta":
            raw_text = self._client.fetch_fasta(database=database, record_id=record_id)
            record = parse_fasta(raw_text)
        else:
            raw_text = self._client.fetch_genbank(database=database, record_id=record_id)
            record = parse_genbank(raw_text)

        path = self._file_manager.build_path(clean_accession, fmt)
        self._file_manager.save(path, raw_text)

        return DownloadResult(record=record, saved_path=path)
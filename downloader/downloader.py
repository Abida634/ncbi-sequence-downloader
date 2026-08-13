"""Orchestrates the full download workflow: validate, search, fetch, parse, save."""
from downloader.history import HistoryEntry, HistoryManager
import logging
from dataclasses import dataclass
from pathlib import Path

from Bio.SeqRecord import SeqRecord

from downloader.config import Config
from downloader.entrez_client import EntrezClient
from downloader.exceptions import UnsupportedFormatError
from downloader.file_manager import FileManager
from downloader.parser import parse_fasta, parse_genbank
from downloader.validator import validate_accession

logger = logging.getLogger(__name__)

DEFAULT_DATABASE = "nucleotide"


@dataclass
class DownloadResult:
    """The outcome of a successful download: the parsed record and where it was saved."""

    record: SeqRecord
    saved_path: Path


class Downloader:
    """High-level facade that coordinates validation, fetching, parsing, and saving."""

    def __init__(self, config: Config) -> None:
        self._client = EntrezClient(config)
        self._file_manager = FileManager(config.output_dir)
        self._history = HistoryManager()

    def download(
        self, accession: str, fmt: str = "fasta", database: str = DEFAULT_DATABASE
    ) -> DownloadResult:
        logger.info("Starting download: accession=%s format=%s", accession, fmt)


        if fmt not in ("fasta", "genbank"):
            logger.error("Unsupported format requested: %s", fmt)
            raise UnsupportedFormatError(
                f"'{fmt}' is not supported. Use 'fasta' or 'genbank'."
            )

        clean_accession = validate_accession(accession)
        logger.debug("Accession validated and normalized to: %s", clean_accession)

        ids = self._client.search(database=database, term=clean_accession)
        record_id = ids[0]
        logger.debug("NCBI search resolved to internal ID: %s", record_id)

        if fmt == "fasta":
            raw_text = self._client.fetch_fasta(database=database, record_id=record_id)
            record = parse_fasta(raw_text)
        else:
            raw_text = self._client.fetch_genbank(database=database, record_id=record_id)
            record = parse_genbank(raw_text)

        path = self._file_manager.build_path(clean_accession, fmt)
        self._file_manager.save(path, raw_text)

        logger.info("Download complete: saved to %s (%d bytes)", path, len(raw_text))
        self._history.record(
            HistoryEntry.create(
                accession=clean_accession, fmt=fmt, database=database, saved_path=path
            )
        )
        return DownloadResult(record=record, saved_path=path)
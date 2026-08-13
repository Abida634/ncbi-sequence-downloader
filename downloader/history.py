"""Tracks download history persistently in a JSON file."""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from downloader.exceptions import HistoryError

logger = logging.getLogger(__name__)


@dataclass
class HistoryEntry:
    """A single recorded download event."""

    accession: str
    format: str
    database: str
    saved_path: str
    timestamp: str

    @classmethod
    def create(cls, accession: str, fmt: str, database: str, saved_path: Path) -> "HistoryEntry":
        """Build a HistoryEntry with the current UTC timestamp.

        Args:
            accession: The accession number that was downloaded.
            fmt: The format used ("fasta" or "genbank").
            database: The NCBI database searched.
            saved_path: The path the file was saved to.

        Returns:
            A new HistoryEntry with timestamp set to "now" in UTC, ISO format.
        """
        return cls(
            accession=accession,
            format=fmt,
            database=database,
            saved_path=str(saved_path),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


class HistoryManager:
    """Reads and writes the persistent download history file."""

    def __init__(self, history_file: Path = Path("downloads/history.json")) -> None:
        """Initialize the history manager.

        Args:
            history_file: Path to the JSON file used to store history.
        """
        self._history_file = history_file

    def record(self, entry: HistoryEntry) -> None:
        """Append a new entry to the history file.

        Args:
            entry: The HistoryEntry to record.

        Raises:
            HistoryError: If the history file cannot be read or written.
        """
        entries = self.load_all()
        entries.append(entry)
        self._save_all(entries)
        logger.debug("Recorded history entry for accession=%s", entry.accession)

    def load_all(self) -> list[HistoryEntry]:
        """Load all recorded history entries.

        Returns:
            A list of HistoryEntry objects (empty list if no history exists yet).

        Raises:
            HistoryError: If the file exists but contains invalid JSON.
        """
        if not self._history_file.exists():
            return []

        try:
            raw_text = self._history_file.read_text(encoding="utf-8")
            raw_data = json.loads(raw_text)
        except (OSError, json.JSONDecodeError) as exc:
            raise HistoryError(f"Could not read history file: {exc}") from exc

        return [HistoryEntry(**item) for item in raw_data]

    def has_downloaded(self, accession: str, fmt: str) -> bool:
        """Check whether a given accession/format combination was already downloaded.

        Args:
            accession: The accession number to check.
            fmt: The format to check ("fasta" or "genbank").

        Returns:
            True if a matching entry exists in history, False otherwise.
        """
        entries = self.load_all()
        return any(e.accession == accession and e.format == fmt for e in entries)

    def _save_all(self, entries: list[HistoryEntry]) -> None:
        """Write the full list of entries back to the history file.

        Args:
            entries: The complete list of HistoryEntry objects to persist.

        Raises:
            HistoryError: If the file cannot be written.
        """
        try:
            self._history_file.parent.mkdir(parents=True, exist_ok=True)
            payload = [asdict(entry) for entry in entries]
            self._history_file.write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )
        except OSError as exc:
            raise HistoryError(f"Could not write history file: {exc}") from exc
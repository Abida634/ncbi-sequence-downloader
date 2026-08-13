"""Handles filesystem concerns: naming, directories, and writing downloaded files."""

from pathlib import Path

from downloader.exceptions import FileSaveError

# Maps our internal format names to the file extensions we save on disk.
FORMAT_EXTENSIONS = {
    "fasta": "fasta",
    "genbank": "gb",
}


class FileManager:
    """Responsible for building file paths and writing sequence data to disk."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize the file manager with a base output directory.

        Args:
            output_dir: The directory where downloaded files should be saved.
        """
        self._output_dir = output_dir

    def build_path(self, accession: str, fmt: str) -> Path:
        """Build the full output file path for a given accession and format.

        Args:
            accession: The accession number (used as the filename base).
            fmt: The download format, either "fasta" or "genbank".

        Returns:
            A Path object like downloads/NM_001301717.3.fasta
        """
        extension = FORMAT_EXTENSIONS[fmt]
        safe_name = accession.replace("/", "_")  # defensive: accessions shouldn't contain '/', but just in case
        filename = f"{safe_name}.{extension}"
        return self._output_dir / filename

    def save(self, path: Path, content: str) -> None:
        """Write text content to the given path, creating parent folders as needed.

        Args:
            path: The full file path to write to.
            content: The raw text content to write.

        Raises:
            FileSaveError: If the file cannot be written (e.g. permissions issue).
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except OSError as exc:
            raise FileSaveError(f"Could not save file to '{path}': {exc}") from exc
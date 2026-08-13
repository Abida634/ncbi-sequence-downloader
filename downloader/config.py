"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from downloader.exceptions import DownloaderError


@dataclass
class Config:
    """Holds all runtime configuration for the application."""

    email: str
    api_key: str | None
    output_dir: Path
    default_format: str

    @classmethod
    def from_env(cls) -> "Config":
        """Build a Config instance by reading environment variables.

        Raises:
            DownloaderError: If required settings (like email) are missing.
        """
        load_dotenv()

        email = os.getenv("ENTREZ_EMAIL")
        if not email or not email.strip():
            raise DownloaderError(
                "ENTREZ_EMAIL is not set. Please create a .env file "
                "based on .env.example and provide a valid email address."
            )

        api_key = os.getenv("ENTREZ_API_KEY") or None
        output_dir = Path(os.getenv("DEFAULT_OUTPUT_DIR", "downloads"))
        default_format = os.getenv("DEFAULT_FORMAT", "fasta")

        return cls(
            email=email,
            api_key=api_key,
            output_dir=output_dir,
            default_format=default_format,
        )
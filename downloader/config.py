"""
Configuration management for the NCBI Sequence Downloader.

This module defines a single, centralized Config object that every
other module in the application reads settings from. It loads secrets
(like your NCBI email and API key) from a local .env file, keeping
them out of source control.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load variables from a .env file (if one exists) into the process
# environment. This must happen before we try to read any of them.
load_dotenv()


@dataclass(frozen=True)
class Config:
    """
    Holds all configuration values for the application.

    Attributes:
        ncbi_email: Email address reported to NCBI with every request,
            as required by their usage guidelines.
        ncbi_api_key: Optional API key that raises the allowed request
            rate from 3/second to 10/second. May be None.
        downloads_dir: Folder where downloaded sequence files are saved.
        reports_dir: Folder where generated reports are saved.
        logs_dir: Folder where log files are written.
        request_timeout: Seconds to wait before giving up on a request.
        max_retries: Number of times to retry a failed request.
    """

    ncbi_email: str
    ncbi_api_key: str | None
    downloads_dir: Path
    reports_dir: Path
    logs_dir: Path
    request_timeout: int = 30
    max_retries: int = 3

    @classmethod
    def load(cls) -> "Config":
        """
        Build a Config instance by reading environment variables.

        Raises:
            ValueError: If NCBI_EMAIL is not set, since Entrez requires
                an email address for every request.

        Returns:
            A fully populated, immutable Config object.
        """
        email = os.getenv("NCBI_EMAIL")
        if not email:
            raise ValueError(
                "NCBI_EMAIL is not set. Create a .env file "
                "(see .env.example) with your email address."
            )

        api_key = os.getenv("NCBI_API_KEY")  # may legitimately be None

        project_root = Path(__file__).resolve().parent.parent

        return cls(
            ncbi_email=email,
            ncbi_api_key=api_key,
            downloads_dir=project_root / "downloads",
            reports_dir=project_root / "reports",
            logs_dir=project_root / "logs",
        )


# A single shared instance other modules can import directly.
settings = Config.load()
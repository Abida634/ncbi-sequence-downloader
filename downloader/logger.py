"""Configures application-wide logging: console output and a persistent log file."""

import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

_configured = False  # module-level flag to prevent duplicate configuration


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a console handler and a file handler.

    This should be called ONCE, near the start of the program (e.g. in the
    CLI's entry point). Calling it multiple times is safe — it's a no-op
    after the first call, thanks to the `_configured` guard.

    Args:
        level: The minimum severity level to show in the CONSOLE.
            The file handler always captures DEBUG and above, regardless
            of this setting, so a full history is preserved on disk.
    """
    global _configured
    if _configured:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # capture everything; handlers filter what's shown

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    _configured = True
import logging

from downloader.config import Config
from downloader.downloader import Downloader
from downloader.history import HistoryManager
from downloader.logger import setup_logging
from downloader.exceptions import DownloaderError

setup_logging(level=logging.INFO)

config = Config.from_env()
downloader = Downloader(config)
history = HistoryManager()

try:
    if history.has_downloaded("NM_001301717", "fasta"):
        print("Already downloaded this before! Downloading again anyway for this demo...")

    result = downloader.download(accession="NM_001301717", fmt="fasta")
    print("Saved to:", result.saved_path)

    print("\n--- Full History ---")
    for entry in history.load_all():
        print(f"{entry.timestamp} | {entry.accession} | {entry.format} | {entry.saved_path}")

except DownloaderError as e:
    print(f"Error: {e}")
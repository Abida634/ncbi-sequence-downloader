import logging

from downloader.config import Config
from downloader.downloader import Downloader
from downloader.logger import setup_logging
from downloader.exceptions import DownloaderError

setup_logging(level=logging.DEBUG)  # show everything in the console for this test

config = Config.from_env()
downloader = Downloader(config)

try:
    result = downloader.download(accession="NM_001301717", fmt="fasta")
    print("\nFinal result:", result.saved_path)
except DownloaderError as e:
    print(f"Error: {e}")

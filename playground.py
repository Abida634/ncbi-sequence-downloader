from downloader.config import Config
from downloader.downloader import Downloader
from downloader.statistics import compute_stats
from downloader.exceptions import DownloaderError

config = Config.from_env()
downloader = Downloader(config)

try:
    result = downloader.download(accession="NM_001301717", fmt="fasta")
    stats = compute_stats(result.record)

    print(stats.summary())
    print("Base counts:", stats.base_counts)

except DownloaderError as e:
    print(f"Error: {e}")

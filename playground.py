from downloader.config import Config
from downloader.entrez_client import EntrezClient
from downloader.exceptions import DownloaderError

config = Config.from_env()
client = EntrezClient(config)

try:
    ids = client.search(database="nucleotide", term="NM_001301717")
    print("Found IDs:", ids)

    fasta_data = client.fetch_fasta(database="nucleotide", record_id=ids[0])
    print("--- FASTA preview ---")
    print(fasta_data[:300])
except DownloaderError as e:
    print(f"Error: {e}")
from downloader.config import Config
from downloader.entrez_client import EntrezClient
from downloader.parser import parse_fasta, parse_genbank
from downloader.exceptions import DownloaderError

config = Config.from_env()
client = EntrezClient(config)

try:
    ids = client.search(database="nucleotide", term="NM_001301717")
    record_id = ids[0]

    fasta_text = client.fetch_fasta(database="nucleotide", record_id=record_id)
    fasta_record = parse_fasta(fasta_text)

    print("--- FASTA Parsed ---")
    print("ID:", fasta_record.id)
    print("Description:", fasta_record.description)
    print("Length:", len(fasta_record.seq))
    print("First 50 bases:", fasta_record.seq[:50])

    genbank_text = client.fetch_genbank(database="nucleotide", record_id=record_id)
    gb_record = parse_genbank(genbank_text)

    print("\n--- GenBank Parsed ---")
    print("ID:", gb_record.id)
    print("Organism:", gb_record.annotations.get("organism"))
    print("Molecule type:", gb_record.annotations.get("molecule_type"))
    print("Number of features:", len(gb_record.features))

except DownloaderError as e:
    print(f"Error: {e}")
from downloader.config import Config
from downloader.downloader import Downloader
from downloader.metadata import extract_metadata
from downloader.exceptions import DownloaderError

config = Config.from_env()
downloader = Downloader(config)

try:
    result = downloader.download(accession="NM_001301717", fmt="genbank")
    meta = extract_metadata(result.record)

    print("Accession:", meta.accession_version)
    print("Organism:", meta.organism)
    print("Gene name:", meta.gene_name)
    print("Definition:", meta.definition)
    print("Molecule type:", meta.molecule_type)
    print("Date updated:", meta.date_updated)
    print("Taxonomy:", " > ".join(meta.taxonomy))
    print("Keywords:", meta.keywords)
    print(f"References ({len(meta.references)}):")
    for ref in meta.references[:2]:
        print(f"  - {ref.title} ({ref.journal})")

except DownloaderError as e:
    print(f"Error: {e}")

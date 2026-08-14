# Architecture

## Design Principles

- **Separation of concerns**: each module in `downloader/` has exactly one responsibility (network I/O, parsing, validation, statistics, etc.).
- **Facade pattern**: `Downloader` provides one simple `download()` method that orchestrates validation, network calls, parsing, and file saving — callers never interact with the lower-level pieces directly.
- **Exception translation**: all lower-level exceptions (network errors, parsing errors, JSON errors) are caught and re-raised as our own `DownloaderError` hierarchy, so calling code only ever needs to handle one family of exceptions.
- **UI-agnostic core**: `downloader/` has zero knowledge of the CLI or Streamlit — both interfaces are thin, replaceable layers on top of the same tested core.

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | Load and validate environment-based settings |
| `validator.py` | Validate accession numbers and Gene IDs before any network call |
| `entrez_client.py` | The only module that talks to NCBI's Entrez API |
| `parser.py` | Convert raw FASTA/GenBank text into `SeqRecord` objects |
| `downloader.py` | Orchestrate the full download workflow (Facade) |
| `file_manager.py` | Build file paths and write files to disk |
| `statistics.py` | Pure computation: GC/AT content, base/protein composition |
| `metadata.py` | Extract organism, gene, taxonomy, references from GenBank records |
| `history.py` | Persist download history to JSON |
| `logger.py` | Centralized logging configuration |
| `exceptions.py` | Custom exception hierarchy used throughout the package |

## Data Flow

```
User input (CLI/GUI)
   -> validator.validate_accession()
   -> entrez_client.search() + fetch_fasta()/fetch_genbank()
   -> parser.parse_fasta()/parse_genbank()
   -> file_manager.save()
   -> history.record()
   -> statistics.compute_stats() / metadata.extract_metadata()  (on demand, for display)
```
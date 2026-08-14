# FAQ

**Do I need an NCBI API key?**
No. A valid email is required (NCBI's usage policy), but an API key is optional — it just raises your rate limit from 3 to 10 requests/second.

**Why did my download fail with "No results found"?**
Double-check the accession number is correct and exists in the database you're searching (default: `nucleotide`). Protein accessions (e.g. `NP_...`) currently require passing the correct database — see the Roadmap for planned improvements here.

**Why is metadata mostly empty when I download in FASTA format?**
FASTA format only contains a sequence and a one-line header — it doesn't carry organism, gene, or reference information. Download in GenBank format to get full metadata.

**Where are my downloaded files saved?**
By default, in the `downloads/` folder, named after the accession number (e.g. `downloads/NM_001301717.3.fasta`). This is configurable via `DEFAULT_OUTPUT_DIR` in your `.env` file.

**Can I use this for batch downloading many sequences at once?**
Not yet — batch/CSV downloading is on the [Roadmap](../README.md#roadmap).
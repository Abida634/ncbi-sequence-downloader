"""Client responsible for all communication with the NCBI Entrez API."""

from http.client import IncompleteRead
from urllib.error import HTTPError, URLError

from Bio import Entrez

from downloader.config import Config
from downloader.exceptions import FetchError, NetworkError, NoResultsFoundError


class EntrezClient:
    """A thin, focused wrapper around Biopython's Bio.Entrez module.

    This class is the ONLY part of the application that talks directly
    to NCBI's servers. Every other module that needs sequence data goes
    through this client.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the client and configure Biopython's Entrez module.

        Args:
            config: Application configuration containing email and API key.
        """
        self._config = config
        Entrez.email = config.email
        if config.api_key:
            Entrez.api_key = config.api_key

    def search(self, database: str, term: str, retmax: int = 5) -> list[str]:
        """Search an NCBI database and return matching record IDs.

        Args:
            database: NCBI database name, e.g. "nucleotide" or "protein".
            term: Search term (e.g. an accession number or Gene ID).
            retmax: Maximum number of IDs to return.

        Returns:
            A list of NCBI internal record IDs matching the search term.

        Raises:
            NetworkError: If the request to NCBI fails.
            NoResultsFoundError: If no matching records are found.
        """
        try:
            handle = Entrez.esearch(db=database, term=term, retmax=retmax)
            record = Entrez.read(handle)
            handle.close()
        except (HTTPError, URLError, IncompleteRead) as exc:
            raise NetworkError(f"Failed to search NCBI for '{term}': {exc}") from exc

        id_list = record.get("IdList", [])
        if not id_list:
            raise NoResultsFoundError(
                f"No results found in '{database}' for search term '{term}'."
            )

        return list(id_list)

    def fetch_fasta(self, database: str, record_id: str) -> str:
        """Fetch a record in FASTA format.

        Args:
            database: NCBI database name, e.g. "nucleotide" or "protein".
            record_id: The NCBI internal record ID (from search()).

        Returns:
            The raw FASTA text.

        Raises:
            NetworkError: If the request to NCBI fails.
            FetchError: If NCBI returns an empty or unexpected response.
        """
        return self._fetch(database, record_id, rettype="fasta")

    def fetch_genbank(self, database: str, record_id: str) -> str:
        """Fetch a record in GenBank format.

        Args:
            database: NCBI database name, e.g. "nucleotide" or "protein".
            record_id: The NCBI internal record ID (from search()).

        Returns:
            The raw GenBank text.

        Raises:
            NetworkError: If the request to NCBI fails.
            FetchError: If NCBI returns an empty or unexpected response.
        """
        return self._fetch(database, record_id, rettype="gb")

    def _fetch(self, database: str, record_id: str, rettype: str) -> str:
        """Shared internal logic for fetching a record in a given format.

        This is a "private" helper method (leading underscore convention)
        used only inside this class, to avoid duplicating try/except logic
        between fetch_fasta() and fetch_genbank().
        """
        try:
            handle = Entrez.efetch(
                db=database, id=record_id, rettype=rettype, retmode="text"
            )
            data = handle.read()
            handle.close()
        except (HTTPError, URLError, IncompleteRead) as exc:
            raise NetworkError(
                f"Failed to fetch record '{record_id}' from '{database}': {exc}"
            ) from exc

        if not data or not data.strip():
            raise FetchError(
                f"NCBI returned an empty response for record '{record_id}'."
            )

        return data
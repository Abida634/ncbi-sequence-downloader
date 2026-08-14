"""Tests for downloader.entrez_client, using mocks to avoid real network calls."""

from unittest.mock import MagicMock, patch

import pytest

from downloader.config import Config
from downloader.entrez_client import EntrezClient
from downloader.exceptions import NoResultsFoundError
from pathlib import Path


@pytest.fixture
def config() -> Config:
    """A fixture providing a fake Config for tests, so no real .env is needed."""
    return Config(
        email="test@example.com",
        api_key=None,
        output_dir=Path("downloads"),
        default_format="fasta",
    )


def test_search_returns_id_list(config):
    with patch("downloader.entrez_client.Entrez") as mock_entrez:
        mock_entrez.esearch.return_value = MagicMock()
        mock_entrez.read.return_value = {"IdList": ["123456"]}

        client = EntrezClient(config)
        result = client.search(database="nucleotide", term="NM_001301717")

        assert result == ["123456"]


def test_search_raises_when_no_results(config):
    with patch("downloader.entrez_client.Entrez") as mock_entrez:
        mock_entrez.esearch.return_value = MagicMock()
        mock_entrez.read.return_value = {"IdList": []}

        client = EntrezClient(config)

        with pytest.raises(NoResultsFoundError):
            client.search(database="nucleotide", term="NM_001301717")


def test_fetch_fasta_returns_raw_text(config):
    with patch("downloader.entrez_client.Entrez") as mock_entrez:
        mock_handle = MagicMock()
        mock_handle.read.return_value = ">NM_001301717.3 Test\nATGC"
        mock_entrez.efetch.return_value = mock_handle

        client = EntrezClient(config)
        result = client.fetch_fasta(database="nucleotide", record_id="123456")

        assert result == ">NM_001301717.3 Test\nATGC"
        mock_entrez.efetch.assert_called_once_with(
            db="nucleotide", id="123456", rettype="fasta", retmode="text"
        )
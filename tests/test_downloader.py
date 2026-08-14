"""Tests for downloader.downloader, mocking EntrezClient entirely."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from downloader.config import Config
from downloader.downloader import Downloader
from downloader.exceptions import UnsupportedFormatError


@pytest.fixture
def config(tmp_path) -> Config:
    """A fixture providing a Config that writes into pytest's temporary directory."""
    return Config(
        email="test@example.com",
        api_key=None,
        output_dir=tmp_path,
        default_format="fasta",
    )


def test_download_rejects_unsupported_format(config):
    downloader = Downloader(config)
    with pytest.raises(UnsupportedFormatError):
        downloader.download(accession="NM_001301717", fmt="pdf")


def test_download_saves_file_and_returns_result(config):
    with patch("downloader.downloader.EntrezClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.search.return_value = ["123456"]
        mock_client.fetch_fasta.return_value = ">NM_001301717.3 Test\nATGC"
        mock_client_cls.return_value = mock_client

        downloader = Downloader(config)
        result = downloader.download(accession="NM_001301717", fmt="fasta")

        assert result.saved_path.exists()
        assert result.saved_path.read_text() == ">NM_001301717.3 Test\nATGC"
        assert str(result.record.seq) == "ATGC"
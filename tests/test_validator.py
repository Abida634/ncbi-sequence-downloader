"""Tests for downloader.validator."""

import pytest

from downloader.exceptions import EmptyInputError, InvalidAccessionError, InvalidGeneIdError
from downloader.validator import validate_accession, validate_gene_id


def test_validate_accession_accepts_valid_format():
    assert validate_accession("NM_001301717") == "NM_001301717"


def test_validate_accession_normalizes_case_and_whitespace():
    assert validate_accession("  nm_001301717  ") == "NM_001301717"


def test_validate_accession_accepts_version_suffix():
    assert validate_accession("NM_001301717.3") == "NM_001301717.3"


def test_validate_accession_rejects_garbage():
    with pytest.raises(InvalidAccessionError):
        validate_accession("banana")


def test_validate_accession_rejects_empty_string():
    with pytest.raises(EmptyInputError):
        validate_accession("   ")


def test_validate_gene_id_accepts_positive_integer():
    assert validate_gene_id("7157") == "7157"


def test_validate_gene_id_rejects_non_numeric():
    with pytest.raises(InvalidGeneIdError):
        validate_gene_id("abc123")


def test_validate_gene_id_rejects_negative_number():
    with pytest.raises(InvalidGeneIdError):
        validate_gene_id("-5")


def test_validate_gene_id_rejects_empty_string():
    with pytest.raises(EmptyInputError):
        validate_gene_id("")
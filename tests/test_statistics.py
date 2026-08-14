"""Tests for downloader.statistics."""

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from downloader.statistics import compute_stats


def make_record(sequence: str) -> SeqRecord:
    """Helper: build a minimal SeqRecord from a raw sequence string."""
    return SeqRecord(Seq(sequence), id="TEST001")


def test_compute_stats_length():
    record = make_record("ATGC")
    stats = compute_stats(record)
    assert stats.length == 4


def test_compute_stats_gc_content_all_gc():
    record = make_record("GGCC")
    stats = compute_stats(record)
    assert stats.gc_content == 100.0


def test_compute_stats_gc_content_all_at():
    record = make_record("AATT")
    stats = compute_stats(record)
    assert stats.gc_content == 0.0


def test_compute_stats_mixed_content():
    record = make_record("ATGC")  # 2 GC, 2 AT out of 4
    stats = compute_stats(record)
    assert stats.gc_content == 50.0
    assert stats.at_content == 50.0


def test_compute_stats_empty_sequence_does_not_crash():
    record = make_record("")
    stats = compute_stats(record)
    assert stats.length == 0
    assert stats.gc_content == 0.0


def test_compute_stats_base_counts():
    record = make_record("AATTGGCC")
    stats = compute_stats(record)
    assert stats.base_counts == {"A": 2, "T": 2, "G": 2, "C": 2}
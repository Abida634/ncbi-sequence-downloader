"""Computes sequence statistics: length, GC/AT content, and base composition."""

from collections import Counter
from dataclasses import dataclass

from Bio.SeqRecord import SeqRecord

# The four standard DNA/RNA bases we track explicitly.
GC_BASES = {"G", "C"}
AT_BASES = {"A", "T", "U"}  # U (Uracil) replaces T in RNA


@dataclass
class SequenceStats:
    """Structured statistics computed from a single sequence."""

    length: int
    gc_content: float
    at_content: float
    base_counts: dict[str, int]

    def summary(self) -> str:
        """Return a short, human-readable summary string."""
        return (
            f"Length: {self.length} bp | "
            f"GC content: {self.gc_content:.2f}% | "
            f"AT content: {self.at_content:.2f}%"
        )


def compute_stats(record: SeqRecord) -> SequenceStats:
    """Compute length, GC content, AT content, and base composition for a sequence.

    Args:
        record: A parsed SeqRecord (from parser.py).

    Returns:
        A SequenceStats object with the computed metrics.
    """
    sequence = str(record.seq).upper()
    length = len(sequence)

    base_counts = dict(Counter(sequence))

    if length == 0:
        return SequenceStats(length=0, gc_content=0.0, at_content=0.0, base_counts=base_counts)

    gc_count = sum(count for base, count in base_counts.items() if base in GC_BASES)
    at_count = sum(count for base, count in base_counts.items() if base in AT_BASES)

    gc_content = (gc_count / length) * 100
    at_content = (at_count / length) * 100

    return SequenceStats(
        length=length,
        gc_content=gc_content,
        at_content=at_content,
        base_counts=base_counts,
    )


def compute_protein_composition(record: SeqRecord) -> dict[str, int]:
    """Compute amino acid frequency for a protein sequence.

    Args:
        record: A parsed SeqRecord representing a protein sequence.

    Returns:
        A dictionary mapping each amino acid letter to its count.
    """
    sequence = str(record.seq).upper()
    return dict(Counter(sequence))
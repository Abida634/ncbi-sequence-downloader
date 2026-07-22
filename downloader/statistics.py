"""
Sequence statistics calculations for the NCBI Sequence Downloader.

This module computes biologically meaningful summary statistics
(length, GC content, nucleotide/amino acid composition) from raw
sequence strings. It has no dependency on networking or file I/O,
making it easy to test in isolation.
"""

from collections import Counter

# The set of letters that make up nucleic acid sequences (DNA/RNA).
# We include both T (DNA) and U (RNA) since a sequence should only
# ever contain one or the other, and 'N' represents an unknown/
# ambiguous base, which legitimately appears in real NCBI records.
_NUCLEOTIDE_LETTERS = set("ATGCUN")

# The 20 standard amino acid single-letter codes, plus 'X' for
# unknown/ambiguous residues, which also legitimately appears in
# real protein records.
_AMINO_ACID_LETTERS = set("ACDEFGHIKLMNPQRSTVWYX")


def detect_sequence_type(sequence: str) -> str:
    """
    Guess whether a sequence is nucleic acid (DNA/RNA) or protein,
    based on which letters appear in it.

    Args:
        sequence: The raw sequence string.

    Returns:
        "nucleotide" if the sequence's letters are a subset of known
        nucleotide letters, otherwise "protein".
    """
    unique_letters = set(sequence.upper())

    if unique_letters.issubset(_NUCLEOTIDE_LETTERS):
        return "nucleotide"

    return "protein"


def calculate_length(sequence: str) -> int:
    """
    Calculate the length of a sequence.

    Args:
        sequence: The raw sequence string.

    Returns:
        The number of characters (bases or residues) in the sequence.
    """
    return len(sequence)


def calculate_gc_content(sequence: str) -> float:
    """
    Calculate the percentage of G and C bases in a nucleotide sequence.

    Args:
        sequence: A DNA or RNA sequence string.

    Returns:
        The GC content as a percentage, rounded to 2 decimal places.
        Returns 0.0 for an empty sequence.
    """
    sequence = sequence.upper()

    if len(sequence) == 0:
        return 0.0

    gc_count = sequence.count("G") + sequence.count("C")
    percentage = (gc_count / len(sequence)) * 100

    return round(percentage, 2)


def calculate_nucleotide_composition(sequence: str) -> dict[str, float]:
    """
    Calculate the percentage of each base (A, T/U, G, C, N) in a
    nucleotide sequence.

    Args:
        sequence: A DNA or RNA sequence string.

    Returns:
        A dictionary mapping each base letter present to its
        percentage of the total sequence, rounded to 2 decimal places.
    """
    sequence = sequence.upper()
    total = len(sequence)

    if total == 0:
        return {}

    counts = Counter(sequence)

    return {
        base: round((count / total) * 100, 2)
        for base, count in counts.items()
    }


def calculate_amino_acid_composition(sequence: str) -> dict[str, float]:
    """
    Calculate the percentage of each amino acid in a protein sequence.

    Args:
        sequence: A protein sequence string.

    Returns:
        A dictionary mapping each amino acid letter present to its
        percentage of the total sequence, rounded to 2 decimal places.
    """
    # The calculation is identical in shape to nucleotide composition;
    # we reuse it rather than duplicating the same logic.
    return calculate_nucleotide_composition(sequence)


def generate_statistics(sequence: str) -> dict[str, object]:
    """
    Generate a full statistics summary for a sequence, automatically
    detecting whether it is nucleotide or protein and including the
    relevant composition breakdown.

    Args:
        sequence: The raw sequence string.

    Returns:
        A dictionary containing 'sequence_type', 'length', and either
        'gc_content' + 'nucleotide_composition' (for nucleotide
        sequences) or 'amino_acid_composition' (for protein sequences).
    """
    sequence_type = detect_sequence_type(sequence)

    stats: dict[str, object] = {
        "sequence_type": sequence_type,
        "length": calculate_length(sequence),
    }

    if sequence_type == "nucleotide":
        stats["gc_content"] = calculate_gc_content(sequence)
        stats["nucleotide_composition"] = calculate_nucleotide_composition(sequence)
    else:
        stats["amino_acid_composition"] = calculate_amino_acid_composition(sequence)

    return stats
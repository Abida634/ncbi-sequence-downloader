"""Extracts structured biological metadata from parsed GenBank SeqRecord objects."""

from dataclasses import dataclass, field

from Bio.SeqRecord import SeqRecord


@dataclass
class Reference:
    """A single publication reference associated with a sequence record."""

    authors: str
    title: str
    journal: str


@dataclass
class SequenceMetadata:
    """Structured biological metadata extracted from a GenBank record."""

    accession_version: str
    organism: str
    gene_name: str | None
    definition: str
    molecule_type: str | None
    date_updated: str | None
    taxonomy: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    references: list[Reference] = field(default_factory=list)


def extract_metadata(record: SeqRecord) -> SequenceMetadata:
    """Extract structured metadata from a parsed GenBank SeqRecord.

    Args:
        record: A SeqRecord produced by parser.parse_genbank(). FASTA-parsed
            records will have very little metadata available (most fields
            will fall back to None/empty), since FASTA format doesn't carry it.

    Returns:
        A SequenceMetadata object with all available fields populated,
        using safe fallbacks for anything missing.
    """
    annotations = record.annotations

    return SequenceMetadata(
        accession_version=record.id,
        organism=annotations.get("organism", "Unknown"),
        gene_name=_extract_gene_name(record),
        definition=record.description or "No definition available",
        molecule_type=annotations.get("molecule_type"),
        date_updated=annotations.get("date"),
        taxonomy=list(annotations.get("taxonomy", [])),
        keywords=list(annotations.get("keywords", [])),
        references=_extract_references(annotations),
    )


def _extract_gene_name(record: SeqRecord) -> str | None:
    """Search the record's features for a 'gene' feature and return its name.

    Args:
        record: A parsed SeqRecord.

    Returns:
        The gene name if found, otherwise None.
    """
    for feature in record.features:
        if feature.type == "gene":
            gene_names = feature.qualifiers.get("gene")
            if gene_names:
                return gene_names[0]
    return None


def _extract_references(annotations: dict) -> list[Reference]:
    """Convert Biopython's raw reference objects into our clean Reference dataclass.

    Args:
        annotations: The record.annotations dictionary.

    Returns:
        A list of Reference objects (empty list if none are present).
    """
    raw_references = annotations.get("references", [])
    references = []

    for ref in raw_references:
        references.append(
            Reference(
                authors=getattr(ref, "authors", "") or "Unknown authors",
                title=getattr(ref, "title", "") or "Untitled",
                journal=getattr(ref, "journal", "") or "Unknown journal",
            )
        )

    return references
from downloader.validator import validate_accession, validate_gene_id
from downloader.exceptions import ValidationError

test_inputs = ["NM_001301717", "nm_001301717.3", "banana", "  ", "7157", "-5", "12abc"]

for item in test_inputs:
    try:
        result = validate_accession(item)
        print(f"ACCESSION OK: {item!r} -> {result}")
    except ValidationError as e:
        print(f"ACCESSION FAIL: {item!r} -> {e}")

print("---")

for item in test_inputs:
    try:
        result = validate_gene_id(item)
        print(f"GENE ID OK: {item!r} -> {result}")
    except ValidationError as e:
        print(f"GENE ID FAIL: {item!r} -> {e}")
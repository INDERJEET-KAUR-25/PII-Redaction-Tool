from config import INPUT_DOC, OUTPUT_DOC
from document_processor import DocumentProcessor
from detector import HybridDetector
from anonymizer import FakeDataReplacer


def main():

    print("=" * 70)
    print("PII REDACTION TOOL")
    print("=" * 70)

    processor = DocumentProcessor(INPUT_DOC)
    detector = HybridDetector()
    replacer = FakeDataReplacer()

    total = 0

    # Stores number of detections by entity type
    entity_counts = {}

    # ----------------------------------------------------
    # Process Paragraphs
    # ----------------------------------------------------

    for paragraph in processor.get_paragraphs():

        text = paragraph.text

        if not text.strip():
            continue

        entities = detector.detect(text)

        # TEMPORARY DEBUG
        for entity in entities:
            entity_counts[entity.entity_type] = (
                entity_counts.get(entity.entity_type, 0) + 1
            )

        if entities:

            total += len(entities)

            paragraph.text = replacer.replace(
                text,
                entities
            )

    # ----------------------------------------------------
    # Process Tables
    # ----------------------------------------------------

    for table in processor.get_tables():

        for row in table.rows:

            for cell in row.cells:

                text = cell.text

                if not text.strip():
                    continue

                entities = detector.detect(text)

                # TEMPORARY DEBUG
                for entity in entities:
                    entity_counts[entity.entity_type] = (
                        entity_counts.get(entity.entity_type, 0) + 1
                    )

                if entities:

                    total += len(entities)

                    cell.text = replacer.replace(
                        text,
                        entities
                    )

    # ----------------------------------------------------
    # Save Document
    # ----------------------------------------------------

    processor.save(OUTPUT_DOC)

    # ----------------------------------------------------
    # Entity Summary (Temporary)
    # ----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("ENTITY SUMMARY")
    print("=" * 70)

    if entity_counts:
        for entity_type, count in sorted(entity_counts.items()):
            print(f"{entity_type:<20} : {count}")
    else:
        print("No entities detected.")

    print("=" * 70)

    print(f"Total PII Detected : {total}")
    print(f"Output Saved       : {OUTPUT_DOC}")

    print("=" * 70)


if __name__ == "__main__":
    main()
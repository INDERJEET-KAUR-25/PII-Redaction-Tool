from collections import Counter
from pathlib import Path

import pandas as pd

from config import INPUT_DOC, OUTPUT_DOC
from document_processor import DocumentProcessor
from detector import HybridDetector
from anonymizer import FakeDataReplacer


EVALUATION_DIR = Path("evaluation")
PREDICTIONS_FILE = EVALUATION_DIR / "predictions.csv"


def process_text(text, detector, replacer):
    """
    Detect and replace PII in a piece of text.

    Returns:
        replaced_text: anonymized text
        entities: detected PII entities
    """

    if not text or not text.strip():
        return text, []

    entities = detector.detect(text)

    if not entities:
        return text, []

    replaced_text = replacer.replace(text, entities)

    return replaced_text, entities


def main():

    print("=" * 70)
    print("PII REDACTION TOOL")
    print("=" * 70)

    # ----------------------------------------------------
    # Initialize components
    # ----------------------------------------------------

    processor = DocumentProcessor(INPUT_DOC)
    detector = HybridDetector()
    replacer = FakeDataReplacer()

    entity_counts = Counter()
    prediction_records = []

    total_entities = 0

    # ----------------------------------------------------
    # Process Paragraphs
    # ----------------------------------------------------

    for paragraph_index, paragraph in enumerate(
        processor.get_paragraphs(),
        start=1
    ):

        original_text = paragraph.text

        if not original_text.strip():
            continue

        replaced_text, entities = process_text(
            original_text,
            detector,
            replacer
        )

        if entities:

            paragraph.text = replaced_text

            total_entities += len(entities)

            for entity in entities:

                entity_counts[entity.entity_type] += 1

                prediction_records.append({
                    "location": f"paragraph_{paragraph_index}",
                    "entity_type": entity.entity_type,
                    "value": entity.value,
                    "start": entity.start,
                    "end": entity.end
                })

    # ----------------------------------------------------
    # Process Tables
    # ----------------------------------------------------

    for table_index, table in enumerate(
        processor.get_tables(),
        start=1
    ):

        for row_index, row in enumerate(
            table.rows,
            start=1
        ):

            for cell_index, cell in enumerate(
                row.cells,
                start=1
            ):

                original_text = cell.text

                if not original_text.strip():
                    continue

                replaced_text, entities = process_text(
                    original_text,
                    detector,
                    replacer
                )

                if entities:

                    cell.text = replaced_text

                    total_entities += len(entities)

                    for entity in entities:

                        entity_counts[entity.entity_type] += 1

                        prediction_records.append({
                            "location": (
                                f"table_{table_index}"
                                f"_row_{row_index}"
                                f"_cell_{cell_index}"
                            ),
                            "entity_type": entity.entity_type,
                            "value": entity.value,
                            "start": entity.start,
                            "end": entity.end
                        })

    # ----------------------------------------------------
    # Save Redacted Document
    # ----------------------------------------------------

    processor.save(OUTPUT_DOC)

    # ----------------------------------------------------
    # Save Predictions
    # ----------------------------------------------------

    EVALUATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    predictions_df = pd.DataFrame(
        prediction_records,
        columns=[
            "location",
            "entity_type",
            "value",
            "start",
            "end"
        ]
    )

    predictions_df.to_csv(
        PREDICTIONS_FILE,
        index=False
    )

    # ----------------------------------------------------
    # Entity Summary
    # ----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("ENTITY SUMMARY")
    print("=" * 70)

    if entity_counts:

        for entity_type, count in sorted(
            entity_counts.items()
        ):

            print(
                f"{entity_type:<20} : {count}"
            )

    else:

        print("No PII detected.")

    print("=" * 70)

    print(
        f"Total PII Detected : {total_entities}"
    )

    print(
        f"Output Saved       : {OUTPUT_DOC}"
    )

    print(
        f"Predictions Saved  : {PREDICTIONS_FILE}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
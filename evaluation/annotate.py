from pathlib import Path
import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PREDICTIONS_FILE = BASE_DIR / "predictions.csv"
GROUND_TRUTH_FILE = BASE_DIR / "ground_truth.csv"


# ============================================================
# LOAD PREDICTIONS
# ============================================================

def load_predictions():

    if not PREDICTIONS_FILE.exists():

        print("predictions.csv not found.")
        print("Run src/main.py first.")
        return None

    df = pd.read_csv(PREDICTIONS_FILE)

    required = {
        "location",
        "entity_type",
        "value",
        "start",
        "end",
    }

    missing = required - set(df.columns)

    if missing:

        print("Missing columns:")
        for column in missing:
            print(column)

        return None

    return df


# ============================================================
# LOAD EXISTING GROUND TRUTH
# ============================================================

def load_existing():

    if not GROUND_TRUTH_FILE.exists():
        return set()

    try:
        df = pd.read_csv(GROUND_TRUTH_FILE)

    except Exception:
        return set()

    required = {
        "location",
        "entity_type",
        "value",
        "start",
        "end",
    }

    if not required.issubset(df.columns):
        return set()

    approved = set()

    for _, row in df.iterrows():

        approved.add(
            (
                str(row["location"]),
                str(row["entity_type"]),
                str(row["value"]),
                int(row["start"]),
                int(row["end"]),
            )
        )

    return approved


# ============================================================
# SAVE GROUND TRUTH
# ============================================================

def save_ground_truth(predictions, approved_keys):

    records = []

    for _, row in predictions.iterrows():

        key = (
            str(row["location"]),
            str(row["entity_type"]),
            str(row["value"]),
            int(row["start"]),
            int(row["end"]),
        )

        if key in approved_keys:

            records.append(
                {
                    "location": row["location"],
                    "entity_type": row["entity_type"],
                    "value": row["value"],
                    "start": row["start"],
                    "end": row["end"],
                }
            )

    df = pd.DataFrame(records)

    df.to_csv(
        GROUND_TRUTH_FILE,
        index=False,
    )

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("PII REDACTION TOOL - ANNOTATION")
    print("=" * 70)

    predictions = load_predictions()

    if predictions is None:
        return

    approved_keys = load_existing()

    print(f"\nTotal detections : {len(predictions)}")

    unique_entities = (
        predictions[
            ["entity_type", "value"]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    print(f"Unique entities  : {len(unique_entities)}")
    print(f"Already approved : {len(approved_keys)}")

    print("\nInstructions")
    print("----------------------------")
    print("Y = Genuine PII")
    print("N = False Positive")
    print("S = Skip")
    print("Q = Save & Quit")

    input("\nPress ENTER to start...")

    skipped = set()

    for i, entity in unique_entities.iterrows():

        entity_type = entity["entity_type"]
        value = entity["value"]

        pair = (
            entity_type,
            value,
        )

        if pair in skipped:
            continue

        print("\n")
        print("=" * 70)
        print(f"Entity {i+1} / {len(unique_entities)}")
        print("=" * 70)

        print(f"Type  : {entity_type}")
        print(f"Value : {value}")

        occurrences = predictions[
            (predictions["entity_type"] == entity_type)
            &
            (predictions["value"] == value)
        ]

        print(f"Occurrences : {len(occurrences)}")

        while True:

            choice = input(
                "\n[Y/N/S/Q] : "
            ).strip().lower()

            if choice == "y":

                for _, row in occurrences.iterrows():

                    key = (
                        str(row["location"]),
                        str(row["entity_type"]),
                        str(row["value"]),
                        int(row["start"]),
                        int(row["end"]),
                    )

                    approved_keys.add(key)

                break

            elif choice == "n":

                break

            elif choice == "s":

                skipped.add(pair)
                break

            elif choice == "q":

                gt = save_ground_truth(
                    predictions,
                    approved_keys,
                )

                print("\n")
                print("=" * 70)
                print("Progress Saved")
                print("=" * 70)
                print(f"Ground Truth Records : {len(gt)}")
                print(f"Saved to : {GROUND_TRUTH_FILE}")
                print("=" * 70)

                return

            else:

                print("Invalid choice.")

    gt = save_ground_truth(
        predictions,
        approved_keys,
    )

    print("\n")
    print("=" * 70)
    print("ANNOTATION COMPLETE")
    print("=" * 70)
    print(f"Ground Truth Records : {len(gt)}")
    print(f"Saved to : {GROUND_TRUTH_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
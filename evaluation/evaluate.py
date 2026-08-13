from pathlib import Path
import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

GROUND_TRUTH_FILE = BASE_DIR / "ground_truth.csv"
PREDICTIONS_FILE = BASE_DIR / "predictions.csv"


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):

    if pd.isna(text):
        return ""

    return str(text).strip().lower()


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(path):

    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")

    df = pd.read_csv(path)

    required = {
        "location",
        "entity_type",
        "value",
        "start",
        "end",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"{path.name} missing columns: {missing}"
        )

    return df


# ============================================================
# PREPARE DATAFRAME
# ============================================================

def prepare(df):

    df = df.copy()

    df["location"] = df["location"].apply(normalize)
    df["entity_type"] = df["entity_type"].apply(normalize)
    df["value"] = df["value"].apply(normalize)

    df["key"] = list(
        zip(
            df["location"],
            df["entity_type"],
            df["value"],
            df["start"],
            df["end"],
        )
    )

    return df


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(tp, fp, fn):

    precision = tp / (tp + fp) if tp + fp else 0

    recall = tp / (tp + fn) if tp + fn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0
    )

    return precision, recall, f1


# ============================================================
# MAIN
# ============================================================

def evaluate():

    gt = prepare(load_csv(GROUND_TRUTH_FILE))
    pred = prepare(load_csv(PREDICTIONS_FILE))

    gt_set = set(gt["key"])
    pred_set = set(pred["key"])

    tp = len(gt_set & pred_set)
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    precision, recall, f1 = calculate_metrics(tp, fp, fn)

    print("=" * 75)
    print("PII REDACTION TOOL - EVALUATION")
    print("=" * 75)

    print(f"\nGround Truth Records : {len(gt_set)}")
    print(f"Prediction Records   : {len(pred_set)}")

    print("\n" + "=" * 75)
    print("OVERALL RESULTS")
    print("=" * 75)

    print(f"True Positives  : {tp}")
    print(f"False Positives : {fp}")
    print(f"False Negatives : {fn}")

    print(f"Precision       : {precision:.4f}")
    print(f"Recall          : {recall:.4f}")
    print(f"F1 Score        : {f1:.4f}")

    print("\n" + "=" * 75)
    print("ENTITY-WISE RESULTS")
    print("=" * 75)

    rows = []

    entity_types = sorted(
        set(gt["entity_type"]) | set(pred["entity_type"])
    )

    for entity in entity_types:

        gt_subset = gt[gt["entity_type"] == entity]
        pred_subset = pred[pred["entity_type"] == entity]

        gt_keys = set(gt_subset["key"])
        pred_keys = set(pred_subset["key"])

        tp_e = len(gt_keys & pred_keys)
        fp_e = len(pred_keys - gt_keys)
        fn_e = len(gt_keys - pred_keys)

        p, r, f = calculate_metrics(
            tp_e,
            fp_e,
            fn_e,
        )

        rows.append(
            {
                "entity_type": entity.upper(),
                "ground_truth": len(gt_keys),
                "predicted": len(pred_keys),
                "true_positive": tp_e,
                "false_positive": fp_e,
                "false_negative": fn_e,
                "precision": round(p, 4),
                "recall": round(r, 4),
                "f1_score": round(f, 4),
            }
        )

    result = pd.DataFrame(rows)

    print(result.to_string(index=False))

    print("=" * 75)
    # ============================================================
    # SAVE METRICS
    # ============================================================

    METRICS_FILE = BASE_DIR / "metrics.csv"

    result.to_csv(
    METRICS_FILE,
    index=False,
)

    print(f"\nMetrics saved to : {METRICS_FILE}")


if __name__ == "__main__":
    evaluate()
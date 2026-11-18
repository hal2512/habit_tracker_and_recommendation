"""Sanity-check the trained Guardian models against the synthetic ground-truth labels.

The Isolation Forest is trained without labels; `true_label` in the CSVs comes from
`generate_data.py` (-1 = simulated burnout day, 1 = normal day) and is used here
only for evaluation.

Usage:
    python evaluate_guardian.py
"""
import joblib
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

MODELS = ["guardian_original", "guardian_augmented"]
DATASETS = ["original_data", "augmented_data"]

if __name__ == "__main__":
    print(f"{'model':<20} {'dataset':<16} {'rows':>5} {'true anom.':>10} {'flagged':>8} "
          f"{'precision':>9} {'recall':>7} {'f1':>5}")
    for model_name in MODELS:
        model = joblib.load(f"models/{model_name}.joblib")
        features = joblib.load(f"models/{model_name}_features.joblib")
        for dataset in DATASETS:
            df = pd.read_csv(f"data/{dataset}.csv")
            y_true = df["true_label"]
            y_pred = model.predict(df[features])
            print(f"{model_name:<20} {dataset:<16} {len(df):>5} {(y_true == -1).sum():>10} "
                  f"{(y_pred == -1).sum():>8} "
                  f"{precision_score(y_true, y_pred, pos_label=-1):>9.2f} "
                  f"{recall_score(y_true, y_pred, pos_label=-1):>7.2f} "
                  f"{f1_score(y_true, y_pred, pos_label=-1):>5.2f}")

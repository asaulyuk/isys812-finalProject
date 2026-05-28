"""
Repeated random-sampling robustness check for the CFPB escalation model.

This script intentionally writes to predictive/security_sampling_model only.
It does not overwrite the original model in predictive/output_escalation_model.

Run from the project root:
  python predictive/security_sampling_model/run_security_sampling_model.py
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = None
for p in (_THIS_FILE.parent, *_THIS_FILE.parents):
    if (p / "project_paths.py").is_file():
        _REPO_ROOT = p
        break
if _REPO_ROOT is None:
    raise FileNotFoundError("Could not find project_paths.py from script location.")
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from project_paths import PROJECT_ROOT


def load_original_training_module():
    impl_path = PROJECT_ROOT / "predictive" / "predictive" / "train_escalation_model.py"
    spec = importlib.util.spec_from_file_location("escalation_training_impl", impl_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load implementation from: {impl_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_pipeline(*, random_state: int, tfidf_max_features: int, tfidf_min_df: int) -> Pipeline:
    preprocess = ColumnTransformer(
        transformers=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=tfidf_max_features,
                    min_df=tfidf_min_df,
                    max_df=0.5,
                    ngram_range=(1, 2),
                    stop_words="english",
                ),
                "doc",
            ),
            (
                "product",
                OneHotEncoder(handle_unknown="ignore"),
                ["product_service"],
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("prep", preprocess),
            (
                "clf",
                LogisticRegression(
                    solver="saga",
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )


def summarize(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    return {
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


def load_original_metrics(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing original metrics file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_report_subsection(
    *,
    report_path: Path,
    original_metrics: dict[str, Any],
    output: dict[str, Any],
) -> None:
    comparison = output["comparison_to_original"]
    summary = output["security_sampling_summary"]
    repeated_auc = summary["roc_auc"]["mean"]
    repeated_ap = summary["average_precision"]["mean"]
    auc_gap = comparison["roc_auc_gap_vs_original"]
    close = comparison["close_to_original"]

    if close:
        conclusion = (
            "The repeated random-sampling model produced results close to the original model, "
            "which reduces concern that the original performance was only an artifact of a "
            "single time-period split."
        )
    else:
        conclusion = (
            "The repeated random-sampling model did not stay within the chosen closeness band, "
            "so the result should be described as a sensitivity check rather than confirmation "
            "that split-related bias has been ruled out."
        )

    lines = [
        "Second Security Model: Random-Sampling Bias Check",
        "=================================================",
        "",
        "To test whether the escalation model was overly dependent on a timeline-based split, "
        "a second security model was run using repeated random sampling. In each run, 10% of "
        "the CFPB-labeled data was selected as the training sample and the remaining 90% was "
        "held out for testing. This was repeated 10 times with stratification so that the "
        "formal-complaint rate stayed comparable across train and test samples.",
        "",
        f"Original model ROC AUC: {comparison['original_roc_auc']:.4f}",
        f"Repeated 10/90 model mean ROC AUC: {repeated_auc:.4f}",
        f"ROC AUC gap vs original: {auc_gap:.4f}",
        f"Repeated 10/90 model ROC AUC range: {summary['roc_auc']['min']:.4f} to {summary['roc_auc']['max']:.4f}",
        f"Original model average precision: {comparison['original_average_precision']:.4f}",
        f"Repeated 10/90 model mean average precision: {repeated_ap:.4f}",
        f"Close-to-original threshold used: {comparison['close_threshold_roc_auc']:.4f} ROC AUC",
        "",
        conclusion,
        "",
        "Interpretation for the report:",
        "This is best described as a robustness or security check, not as proof that all bias "
        "has been removed. The target variable is still a proxy for escalation, and complaint "
        "language can be subjective. However, getting similar performance when the model is "
        "trained on repeated random 10% samples and tested on the remaining 90% supports the "
        "claim that the original model is not solely driven by one chronological slice of the "
        "data.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Run repeated 10/90 random-sampling security model")
    ap.add_argument("--input", default="master_customer_behavior_clean.csv")
    ap.add_argument("--out-dir", default="predictive/security_sampling_model")
    ap.add_argument("--report-path", default="deliverables/security_sampling_bias_check.txt")
    ap.add_argument("--original-metrics", default="predictive/output_escalation_model/metrics.json")
    ap.add_argument("--repeats", type=int, default=10)
    ap.add_argument("--train-size", type=float, default=0.10)
    ap.add_argument("--random-state", type=int, default=42)
    ap.add_argument("--tfidf-max-features", type=int, default=12000)
    ap.add_argument("--tfidf-min-df", type=int, default=10)
    ap.add_argument(
        "--close-threshold-roc-auc",
        type=float,
        default=0.05,
        help="Mean repeated-sampling ROC AUC must be within this gap from the original ROC AUC.",
    )
    args = ap.parse_args()

    impl = load_original_training_module()
    path_in = PROJECT_ROOT / args.input
    if not path_in.is_file():
        raise SystemExit(f"Missing input: {path_in}")

    df, y = impl.load_cfpb_escalation_frame(path_in)
    if len(np.unique(y)) < 2:
        raise SystemExit("Need both classes (formal_complaint and complaining/churning).")
    X = df[["doc", "product_service"]]

    results: list[dict[str, Any]] = []
    representative_model: Pipeline | None = None
    for repeat_i in range(args.repeats):
        seed = args.random_state + repeat_i
        print(f"Starting repeat {repeat_i + 1}/{args.repeats} with random_state={seed}...", flush=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            train_size=args.train_size,
            test_size=1.0 - args.train_size,
            stratify=y,
            random_state=seed,
        )
        model = build_pipeline(
            random_state=seed,
            tfidf_max_features=args.tfidf_max_features,
            tfidf_min_df=args.tfidf_min_df,
        )
        model.fit(X_train, y_train)
        y_score = model.predict_proba(X_test)[:, 1]
        result = {
            "repeat": repeat_i + 1,
            "random_state": seed,
            "n_train": int(len(X_train)),
            "n_test": int(len(X_test)),
            "train_prevalence_formal_complaint": float(np.mean(y_train)),
            "test_prevalence_formal_complaint": float(np.mean(y_test)),
            "roc_auc": float(roc_auc_score(y_test, y_score)),
            "average_precision": float(average_precision_score(y_test, y_score)),
        }
        results.append(result)
        representative_model = model
        print(
            f"Finished repeat {repeat_i + 1}/{args.repeats}: "
            f"ROC AUC={result['roc_auc']:.4f}, AP={result['average_precision']:.4f}",
            flush=True,
        )

    original_metrics = load_original_metrics(PROJECT_ROOT / args.original_metrics)
    original_roc_auc = float(original_metrics["roc_auc"])
    original_average_precision = float(original_metrics["average_precision"])

    roc_auc_summary = summarize([r["roc_auc"] for r in results])
    ap_summary = summarize([r["average_precision"] for r in results])
    mean_gap = abs(original_roc_auc - roc_auc_summary["mean"])
    close_to_original = mean_gap <= args.close_threshold_roc_auc

    output = {
        "dataset": {
            "n_rows_cfpb_labeled": int(len(df)),
            "positive_rate_formal_complaint": float(np.mean(y)),
        },
        "method": {
            "description": "Repeated stratified random sampling with 10% train and 90% test.",
            "repeats": int(args.repeats),
            "train_size": float(args.train_size),
            "test_size": float(1.0 - args.train_size),
            "base_random_state": int(args.random_state),
        },
        "security_sampling_results": results,
        "security_sampling_summary": {
            "roc_auc": roc_auc_summary,
            "average_precision": ap_summary,
        },
        "comparison_to_original": {
            "original_metrics_path": str(PROJECT_ROOT / args.original_metrics),
            "original_split": original_metrics.get("split"),
            "original_roc_auc": original_roc_auc,
            "original_average_precision": original_average_precision,
            "roc_auc_gap_vs_original": float(mean_gap),
            "close_threshold_roc_auc": float(args.close_threshold_roc_auc),
            "close_to_original": bool(close_to_original),
        },
    }

    out_dir = PROJECT_ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "security_sampling_results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    text_lines = [
        "Security Sampling Model Results",
        "===============================",
        f"Rows: {output['dataset']['n_rows_cfpb_labeled']:,}",
        f"Positive rate: {output['dataset']['positive_rate_formal_complaint']:.4f}",
        f"Repeats: {args.repeats}",
        f"Train/test split per repeat: {args.train_size:.0%} / {1.0 - args.train_size:.0%}",
        "",
        f"Original ROC AUC: {original_roc_auc:.4f}",
        f"Repeated-sampling mean ROC AUC: {roc_auc_summary['mean']:.4f}",
        f"Repeated-sampling ROC AUC std: {roc_auc_summary['std']:.4f}",
        f"Repeated-sampling ROC AUC min/max: {roc_auc_summary['min']:.4f} / {roc_auc_summary['max']:.4f}",
        f"Original average precision: {original_average_precision:.4f}",
        f"Repeated-sampling mean average precision: {ap_summary['mean']:.4f}",
        f"Close to original within {args.close_threshold_roc_auc:.4f} ROC AUC: {close_to_original}",
        "",
        "Per-repeat metrics:",
    ]
    for r in results:
        text_lines.append(
            f"  - repeat {r['repeat']:02d}: seed={r['random_state']}, "
            f"n_train={r['n_train']:,}, n_test={r['n_test']:,}, "
            f"ROC AUC={r['roc_auc']:.4f}, AP={r['average_precision']:.4f}"
        )
    (out_dir / "security_sampling_results.txt").write_text("\n".join(text_lines), encoding="utf-8")

    if representative_model is not None:
        joblib.dump(representative_model, out_dir / "security_sampling_representative_pipeline.joblib")

    write_report_subsection(
        report_path=PROJECT_ROOT / args.report_path,
        original_metrics=original_metrics,
        output=output,
    )

    print("\n".join(text_lines))
    print(f"\nWrote security model artifacts under: {out_dir}")
    print(f"Wrote report subsection text: {PROJECT_ROOT / args.report_path}")


if __name__ == "__main__":
    main()

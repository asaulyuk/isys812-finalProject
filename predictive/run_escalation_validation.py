"""
Validation harness for CFPB escalation model robustness.

Goal:
  Expand (not replace) train_escalation_model.py by stress-testing whether
  performance is stable beyond the in-sample data structure.

Run from repo root:
  python predictive/run_escalation_validation.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
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


def load_impl_module():
    impl_path = PROJECT_ROOT / "predictive" / "predictive" / "train_escalation_model.py"
    spec = importlib.util.spec_from_file_location("escalation_impl", impl_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load implementation from: {impl_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_pipeline(
    *,
    include_text: bool,
    include_product: bool,
    random_state: int,
    tfidf_max_features: int,
    tfidf_min_df: int,
) -> Pipeline:
    transformers: list[tuple[str, Any, Any]] = []
    if include_text:
        transformers.append(
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
            )
        )
    if include_product:
        transformers.append(("product", OneHotEncoder(handle_unknown="ignore"), ["product_service"]))
    if not transformers:
        raise ValueError("At least one feature family is required.")

    preprocess = ColumnTransformer(transformers=transformers)
    return Pipeline(
        steps=[
            ("prep", preprocess),
            (
                "clf",
                LogisticRegression(
                    solver="saga" if include_text else "lbfgs",
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )


@dataclass
class EvalResult:
    roc_auc: float
    average_precision: float
    n_test: int
    prevalence_test: float


def evaluate_pipeline(
    model: Pipeline, X_train: pd.DataFrame, y_train: np.ndarray, X_test: pd.DataFrame, y_test: np.ndarray
) -> EvalResult:
    model.fit(X_train, y_train)
    s = model.predict_proba(X_test)[:, 1]
    return EvalResult(
        roc_auc=float(roc_auc_score(y_test, s)),
        average_precision=float(average_precision_score(y_test, s)),
        n_test=int(len(y_test)),
        prevalence_test=float(np.mean(y_test)),
    )


def product_holdout_split(df: pd.DataFrame, y: np.ndarray, holdout_frac: float, seed: int):
    counts = df["product_service"].astype(str).value_counts()
    uniq_products = counts.index.to_list()
    rng = np.random.default_rng(seed)
    rng.shuffle(uniq_products)
    n_holdout = max(1, int(len(uniq_products) * holdout_frac))
    holdout = set(uniq_products[:n_holdout])
    te = df["product_service"].astype(str).isin(holdout).to_numpy()
    tr = ~te
    if tr.sum() == 0 or te.sum() == 0:
        raise ValueError("Product holdout created empty split.")
    if len(np.unique(y[tr])) < 2 or len(np.unique(y[te])) < 2:
        raise ValueError("Product holdout split needs both classes in train/test.")
    return tr, te, sorted(list(holdout))


def phrase_sensitivity_test(
    model: Pipeline, X_test: pd.DataFrame, n_samples: int = 1000, random_state: int = 42
) -> dict[str, float]:
    rng = np.random.default_rng(random_state)
    n = min(n_samples, len(X_test))
    idx = rng.choice(len(X_test), size=n, replace=False)
    probe = X_test.iloc[idx].copy()
    base = model.predict_proba(probe)[:, 1]
    probe["doc"] = probe["doc"].astype(str) + " i am very disappointed unhappy bad service"
    shifted = model.predict_proba(probe)[:, 1]
    delta = shifted - base
    return {
        "n_probe_rows": int(n),
        "mean_score_delta": float(np.mean(delta)),
        "p95_abs_score_delta": float(np.percentile(np.abs(delta), 95)),
    }


def calibration_summary(
    model: Pipeline, X_test: pd.DataFrame, y_test: np.ndarray, n_bins: int = 10
) -> dict[str, float]:
    s = model.predict_proba(X_test)[:, 1]
    frac_pos, mean_pred = calibration_curve(y_test, s, n_bins=n_bins, strategy="quantile")
    ece = float(np.mean(np.abs(frac_pos - mean_pred)))
    return {
        "bins": int(len(frac_pos)),
        "expected_calibration_error_like": ece,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate escalation model robustness")
    ap.add_argument("--input", default="master_customer_behavior_clean.csv")
    ap.add_argument("--out-dir", default="predictive/output_escalation_validation")
    ap.add_argument("--random-state", type=int, default=42)
    ap.add_argument("--test-size", type=float, default=0.2)
    ap.add_argument("--train-end-year", type=int, default=2015)
    ap.add_argument("--holdout-product-frac", type=float, default=0.2)
    ap.add_argument("--tfidf-max-features", type=int, default=12000)
    ap.add_argument("--tfidf-min-df", type=int, default=10)
    args = ap.parse_args()

    impl = load_impl_module()
    path_in = PROJECT_ROOT / args.input
    if not path_in.is_file():
        raise SystemExit(f"Missing input: {path_in}")

    df, y = impl.load_cfpb_escalation_frame(path_in)
    X = df[["doc", "product_service"]]

    # Baseline random split
    X_tr_r, X_te_r, y_tr_r, y_te_r = train_test_split(
        X, y, test_size=args.test_size, stratify=y, random_state=args.random_state
    )
    model_full = build_pipeline(
        include_text=True,
        include_product=True,
        random_state=args.random_state,
        tfidf_max_features=args.tfidf_max_features,
        tfidf_min_df=args.tfidf_min_df,
    )
    random_res = evaluate_pipeline(model_full, X_tr_r, y_tr_r, X_te_r, y_te_r)

    # Temporal split
    X_tr_t, X_te_t, y_tr_t, y_te_t, split_meta = impl.make_train_test(
        df,
        X,
        y,
        split="temporal",
        test_size=args.test_size,
        train_end_year=args.train_end_year,
        random_state=args.random_state,
    )
    model_temporal = build_pipeline(
        include_text=True,
        include_product=True,
        random_state=args.random_state,
        tfidf_max_features=args.tfidf_max_features,
        tfidf_min_df=args.tfidf_min_df,
    )
    temporal_res = evaluate_pipeline(model_temporal, X_tr_t, y_tr_t, X_te_t, y_te_t)

    # Product-holdout split
    tr_mask, te_mask, holdout_products = product_holdout_split(
        df, y, args.holdout_product_frac, args.random_state
    )
    X_tr_p = X.loc[tr_mask].reset_index(drop=True)
    X_te_p = X.loc[te_mask].reset_index(drop=True)
    y_tr_p = y[tr_mask]
    y_te_p = y[te_mask]
    model_prod_holdout = build_pipeline(
        include_text=True,
        include_product=True,
        random_state=args.random_state,
        tfidf_max_features=args.tfidf_max_features,
        tfidf_min_df=args.tfidf_min_df,
    )
    prod_holdout_res = evaluate_pipeline(model_prod_holdout, X_tr_p, y_tr_p, X_te_p, y_te_p)

    # Ablations on random split
    model_product_only = build_pipeline(
        include_text=False,
        include_product=True,
        random_state=args.random_state,
        tfidf_max_features=args.tfidf_max_features,
        tfidf_min_df=args.tfidf_min_df,
    )
    prod_only_res = evaluate_pipeline(model_product_only, X_tr_r, y_tr_r, X_te_r, y_te_r)

    model_text_only = build_pipeline(
        include_text=True,
        include_product=False,
        random_state=args.random_state,
        tfidf_max_features=args.tfidf_max_features,
        tfidf_min_df=args.tfidf_min_df,
    )
    text_only_res = evaluate_pipeline(model_text_only, X_tr_r, y_tr_r, X_te_r, y_te_r)

    # Calibration + phrase sensitivity on temporal model
    cal = calibration_summary(model_temporal, X_te_t, y_te_t, n_bins=10)
    phrase = phrase_sensitivity_test(model_temporal, X_te_t, n_samples=1000, random_state=args.random_state)

    thresholds = {
        "temporal_roc_auc_min": 0.75,
        "unseen_product_roc_auc_min": 0.7,
        "full_minus_product_only_auc_min": 0.02,
        "ece_like_max": 0.08,
        "p95_phrase_delta_max": 0.2,
    }
    checks = {
        "temporal_generalization": temporal_res.roc_auc >= thresholds["temporal_roc_auc_min"],
        "unseen_product_generalization": prod_holdout_res.roc_auc >= thresholds["unseen_product_roc_auc_min"],
        "incremental_gain_over_product_only": (
            (random_res.roc_auc - prod_only_res.roc_auc) >= thresholds["full_minus_product_only_auc_min"]
        ),
        "calibration_usable": cal["expected_calibration_error_like"] <= thresholds["ece_like_max"],
        "not_over_sensitive_to_canned_phrase": phrase["p95_abs_score_delta"] <= thresholds["p95_phrase_delta_max"],
    }

    output = {
        "dataset": {
            "n_rows": int(len(df)),
            "positive_rate": float(np.mean(y)),
        },
        "random_split_full": random_res.__dict__,
        "temporal_split_full": {**temporal_res.__dict__, "split_meta": split_meta},
        "product_holdout_full": {**prod_holdout_res.__dict__, "holdout_products": holdout_products},
        "ablation_product_only": prod_only_res.__dict__,
        "ablation_text_only": text_only_res.__dict__,
        "calibration": cal,
        "phrase_sensitivity": phrase,
        "thresholds": thresholds,
        "checks": checks,
        "pass_rate": float(np.mean(list(checks.values()))),
    }

    out_dir = PROJECT_ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "validation_report.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = [
        "Escalation Validation Report",
        "============================",
        f"Rows: {output['dataset']['n_rows']:,}",
        f"Positive rate: {output['dataset']['positive_rate']:.4f}",
        "",
        f"Random split ROC AUC (full): {random_res.roc_auc:.4f}",
        f"Temporal split ROC AUC (full): {temporal_res.roc_auc:.4f}",
        f"Product-holdout ROC AUC (full): {prod_holdout_res.roc_auc:.4f}",
        f"Random split ROC AUC (product-only): {prod_only_res.roc_auc:.4f}",
        f"Random split ROC AUC (text-only): {text_only_res.roc_auc:.4f}",
        f"ECE-like: {cal['expected_calibration_error_like']:.4f}",
        f"P95 abs phrase delta: {phrase['p95_abs_score_delta']:.4f}",
        "",
        "Checks:",
    ]
    for k, v in checks.items():
        lines.append(f"  - {k}: {'PASS' if v else 'FAIL'}")
    lines.append(f"\nOverall pass rate: {output['pass_rate']:.2%}")
    (out_dir / "validation_report.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote: {out_dir}")


if __name__ == "__main__":
    main()

"""
Shared cleaning rules for master customer behavior CSV (single source of truth).

Used by: descriptive/ and predictive/ scripts, notebooks, streamlit_dashboard_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from project_paths import PROJECT_ROOT

# Relaxed completeness: allow NaN in fields often blank for non-CFPB rows (else timeline stops ~2017).
ALLOW_NAN_IN_THESE_COLS = ["country", "url", "raw_metadata"]

DEFAULT_RAW_FILENAME = "master_customer_behavior_v3-1.csv"
DEFAULT_CLEAN_FILENAME = "master_customer_behavior_clean.csv"


def load_raw_csv(csv_path: Path | str) -> pd.DataFrame:
    path = Path(csv_path)
    return pd.read_csv(path, low_memory=False, encoding="utf-8-sig")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["rating"], errors="ignore")
    cols_required = [c for c in df.columns if c not in ALLOW_NAN_IN_THESE_COLS]
    row_has_nan = df[cols_required].isna().any(axis=1)
    return df.loc[~row_has_nan].copy()


def add_revised_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add `sentiment_revised_label` for notebooks / audit (supplier NLP is often misleading on short text).

    CFPB `formal_complaint` rows use short category text in `text`, not full narratives.
    Prior NLP on that boilerplate often labeled huge complaint volumes as "positive."
    Here we treat each formal complaint as a negative-valence *event* (friction / escalation).

    All other rows keep the original `sentiment_label` (e.g. app reviews).
    """
    out = df.copy()
    if "sentiment_label" not in out.columns:
        out["sentiment_revised_label"] = None
        return out
    action = out["customer_action"].astype(str)
    orig = out["sentiment_label"].fillna("neutral").astype(str)
    out["sentiment_revised_label"] = orig
    out.loc[action == "formal_complaint", "sentiment_revised_label"] = "negative"
    return out


def add_trends_keyword(df: pd.DataFrame) -> pd.DataFrame:
    """
    Google_Trends rows reuse ``company`` for a *coarse theme tag* (e.g. ``not worth``, ``fee``),
    not a legal entity. The full search phrase is in ``raw_metadata`` as ``keyword``.

    Adds ``trends_keyword`` (full phrase) for ``source == Google_Trends``; null elsewhere.
    CFPB and other sources are unchanged — their ``company`` is a real firm name.
    """
    out = df.copy()
    if "raw_metadata" not in out.columns or "source" not in out.columns:
        out["trends_keyword"] = pd.NA
        return out

    def _keyword(raw: object) -> str | None:
        if pd.isna(raw) or not isinstance(raw, str):
            return None
        try:
            d = json.loads(raw)
            v = d.get("keyword")
            return str(v) if v is not None else None
        except (json.JSONDecodeError, TypeError):
            return None

    out["trends_keyword"] = pd.NA
    mask = out["source"].astype(str) == "Google_Trends"
    if mask.any():
        out.loc[mask, "trends_keyword"] = out.loc[mask, "raw_metadata"].map(_keyword)
    return out


def add_issue_from_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """CFPB-style `issue` from raw_metadata JSON (best subcategory for formal_complaint rows)."""

    def _issue(raw: object) -> str | None:
        if pd.isna(raw) or not isinstance(raw, str):
            return None
        try:
            d = json.loads(raw)
            v = d.get("issue")
            return str(v) if v is not None else None
        except (json.JSONDecodeError, TypeError):
            return None

    out = df.copy()
    out["issue"] = out["raw_metadata"].apply(_issue)
    return out


def export_clean_csv(
    source_csv: Path | str | None = None,
    dest_csv: Path | str | None = None,
    project_root: Path | str | None = None,
) -> Path:
    """
    Load raw CSV, apply the same cleaning as the analysis notebook, write cleaned CSV.
    Returns the path written.
    """
    root = Path(project_root) if project_root else PROJECT_ROOT
    src = Path(source_csv) if source_csv else root / DEFAULT_RAW_FILENAME
    dst = Path(dest_csv) if dest_csv else root / DEFAULT_CLEAN_FILENAME

    df = load_raw_csv(src)
    cleaned = clean_dataframe(df)
    cleaned = add_issue_from_metadata(cleaned)
    cleaned = add_revised_sentiment(cleaned)
    cleaned = add_trends_keyword(cleaned)
    cleaned.to_csv(dst, index=False)
    return dst

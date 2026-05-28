"""
ISYS 812 — descriptive stats on cleaned customer behavior data (CLI).

Run from repository root:
  python descriptive/run_descriptive_analysis.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pandas as pd

from project_paths import PROJECT_ROOT
from shared_cleaning_rules import ALLOW_NAN_IN_THESE_COLS, clean_dataframe, load_raw_csv

csv_path = PROJECT_ROOT / "master_customer_behavior_v3-1.csv"

df_cust = load_raw_csv(csv_path)

print("Dropped column 'rating' from the working table (CSV file on disk is unchanged).\n")

_df = df_cust.drop(columns=["rating"], errors="ignore")
cols_required = [c for c in _df.columns if c not in ALLOW_NAN_IN_THESE_COLS]
rows_before = len(_df)
row_has_nan = _df[cols_required].isna().any(axis=1)
dropped_indexes = _df.index[row_has_nan].tolist()
df_cust = clean_dataframe(df_cust)
rows_after = len(df_cust)

MAX_INDEXES_TO_SHOW = 50
n_dropped = len(dropped_indexes)
print(
    f"Rows before row drop (NaN in required cols): {rows_before:,} | after: {rows_after:,} "
    f"(removed {n_dropped:,})\n"
)
if n_dropped == 0:
    print("Dropped row indexes: (none)")
elif n_dropped <= MAX_INDEXES_TO_SHOW:
    print(f"Dropped row indexes ({n_dropped}): {dropped_indexes}")
else:
    print(
        f"Dropped row indexes: {n_dropped:,} total (too many to list; max shown is {MAX_INDEXES_TO_SHOW})"
    )

_ycounts = df_cust.groupby("year").size()
_ymax = int(_ycounts.index.max())
print("\nRow counts by year (last 12 calendar years in file):")
print(_ycounts[_ycounts.index >= (_ymax - 11)])
print(f"\nYear range in df_cust: {int(df_cust['year'].min())} – {int(df_cust['year'].max())}")

print(df_cust)
print()

print("Column dtypes and non-null counts:")
df_cust.info()
print()

print("Numeric columns — summary statistics:")
print(df_cust.describe())
print()

print("Categorical / text columns — counts & top values:")
print(df_cust.describe(include="object"))

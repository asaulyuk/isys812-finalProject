descriptive/
============

Exploratory and descriptive analysis for ISYS 812.

For finance / fintech MI aligned with the dashboard: slice **`source == "CFPB"`** in notebooks.

Contents:
  run_descriptive_analysis.py   CLI stats (run from repo root: python descriptive/run_descriptive_analysis.py)
  notebook_export_clean_csv.ipynb   Rebuild master_customer_behavior_clean.csv
  descriptive_analysis.ipynb        Main analysis notebook (if present)

Data files stay in the project root; paths resolve via project_paths.py.

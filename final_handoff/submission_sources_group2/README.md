# Submission Sources Guide

This folder contains the analysis/source artifacts cited in the report's **Sources and Data Files** section.

## Purpose

- Help graders quickly trace report claims to supporting artifacts.
- Separate source artifacts from final report deliverables.

## File Map

### Predictive model outputs
- `metrics.json`  
  Core model metrics (rows, split metadata, ROC AUC/AP, product-only baseline).
- `classification_report.txt`  
  Precision/recall/F1 on the temporal holdout.
- `top_features_toward_formal_complaint.json`  
  Highest positive model coefficients (formal complaint direction).
- `top_features_toward_other_actions.json`  
  Highest negative model coefficients (non-formal direction).
- `validation_report.json`  
  Robustness checks summary (temporal, unseen product, ablations, calibration, phrase sensitivity).

### Notebooks requested by instructor
- `notebooks/descriptive_analysis.ipynb`  
  Descriptive analysis notebook used to summarize complaint/customer behavior patterns.
- `notebooks/notebook_export_clean_csv.ipynb`  
  Data preparation/export notebook for the cleaned project dataset.
- `notebooks/predictive_workflows.ipynb`  
  Predictive modeling workflow notebook supporting escalation modeling outputs.

There is no separate prescriptive Jupyter notebook in the project. The prescriptive section was prepared as Markdown and CSV artifacts, listed below, rather than as an `.ipynb` file.

### Prescriptive artifacts
- `opportunity_themes.md`  
  Plain-language pain clusters extracted from predictive signals.
- `feature_and_gtm_strategy.md`  
  Track A / Track B feature + go-to-market strategy.
- `tradeoff_matrix.md`  
  Tradeoffs and failure modes.
- `fallback_trigger_rules.md`  
  Quantitative trigger logic to move from Track A to Track B.
- `fintech_competitive_slice.md`  
  Fintech-focused cohort analysis (PayPal/Venmo, Square/Block-side, etc.).
- `prioritized_backlog.csv`  
  Prioritized action list with owners, KPIs, timelines, and dependencies.
- `prescriptive_strategic_gap_analysis.md`  
  Strategic product-gap layer used in the report's Part 7 narrative.

## Notes

- This bundle intentionally excludes the final report document(s) and only contains analysis/source artifacts cited in the report.
- Use this folder as a standalone evidence package; no project-internal directory structure is required.

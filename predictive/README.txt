predictive/
=============

Models and experiments that score escalation patterns and text themes.
Run commands from repo root unless noted otherwise.

Contents
--------
  run_optional_nlp_topic_clusters.py
      Optional TF-IDF + MiniBatchKMeans topic clusters.
      Input:  master_customer_behavior_clean.csv
      Output: output_optional_nlp_topic_clusters.csv (+ .summary.json) at repo root

  train_escalation_model.py
      Compatibility entrypoint (wrapper). Keeps legacy command path stable:
        python predictive/train_escalation_model.py
      Actual implementation:
        predictive/predictive/train_escalation_model.py

  run_escalation_validation.py
      Validation harness that stress-tests generalization and robustness for
      the escalation model:
        - temporal split stability
        - unseen product holdout
        - full vs product-only vs text-only ablations
        - calibration check (ECE-like)
        - canned-phrase sensitivity probe
      Output: predictive/output_escalation_validation/
        - validation_report.json
        - validation_report.txt

  predictive/predictive/train_escalation_model.py
      Supervised model: CFPB formal complaint vs other CFPB actions
      (complaining/churning), using issue + text + product_service.
      Output: predictive/output_escalation_model/
        - escalation_pipeline.joblib
        - metrics.json
        - classification_report.txt
        - top_features_toward_formal_complaint.json
        - top_features_toward_other_actions.json

  predictive/predictive/predictive_workflows.ipynb
      Notebook mirror of topic clustering + escalation workflow.
      Root path detection now walks upward from current cwd until it finds
      project_paths.py, so it runs from more Jupyter launch locations.


How to interpret near-perfect metrics (important)
-------------------------------------------------
Very high AUC/AP in this extract does not automatically mean production readiness.
In this dataset, label phrasing and product mix can separate classes almost
deterministically.

Treat this model as a descriptive/diagnostic scorer unless these checks pass:
  1) No leakage/post-outcome features in training data
  2) Performance holds on unseen products/templates/time periods
  3) Not dependent on a handful of canned phrases
  4) Probabilities are calibrated and usable
  5) Gains over product-only baseline are stable
  6) Error modes are reviewed and understandable

If those checks fail, keep using it as exploratory MI evidence, not as
production-grade decisioning.

Run validation (recommended before external claims)
---------------------------------------------------
  python predictive/run_escalation_validation.py

This does not replace teammate work; it expands it with repeatable checks so
the model can be assessed against new datasets and changing product mixes.


Change log
----------
See predictive/CHANGELOG.txt for compatibility and notebook fixes.

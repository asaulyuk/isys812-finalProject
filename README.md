# ISYS 812 — Consumer Finance Complaint Intelligence

**Team:** Marko Asaulyuk · Hunsa Tiwana · Jason Tate — SFSU ISYS 812, Spring 2026

**Report:** [isys814-finalProjectReport_group2.pdf](final_handoff/isys814-finalProjectReport_group2.pdf) · **Sources:** [submission_sources_group2/](final_handoff/submission_sources_group2/)

---

## Where the money is

The CFPB complaint record (2014–2017) surfaces four concentrated friction clusters in consumer finance that map directly to product opportunity:

| Cluster | Signal | Plain pain point |
|---|---|---|
| **Billing and fee opacity** | `billing`, `fee`, `late fee`, `apr rate` | Users escalate when charges are unexplained before or after the billing event |
| **Dispute friction** | `disputes`, `transaction issue` | Formal channel is taken when the first resolution path appears slow or closed-loop |
| **Account-status stress** | `delinquent`, `credit determination` | Status changes perceived as sudden or unfair trigger escalation |
| **Lifecycle breaks** | `opening`, `closing account`, `payoff process` | Onboarding, payoff, and account-close moments create avoidable friction |

Fintech cohorts (PayPal/Venmo, Square/Block-side) fail in different zones than large banks — trust and transaction reliability dominate, not mortgage/servicing. The large-bank complaint playbook does not transfer.

**Recommended first move (Track A, 0–3 months):** Transparent Billing Explainer → Dispute Fast-Lane → Lifecycle Guardrails.
Positioning: *"No surprise charges. No black-box disputes. Clear status at every step."*

Full prescriptive analysis: [`prescriptive/`](prescriptive/) — two-tier framework (strategic + operational) with feature specs, GTM strategy, KPI targets, and fallback trigger rules.

---

## Data

**Source:** [Real-Time Customer Behaviour Dataset](https://www.kaggle.com/datasets/krixdrix/real-time-customer-behaviour-dataset) on Kaggle

Download `master_customer_behavior_v3-1.csv` and place it in the project root before running any notebooks or the dashboard. The file is not included in the repository due to size (303 MB).

For core analysis, filter **Source → CFPB** throughout. Other sources (app reviews, Google Trends) are supplementary — mixing them with CFPB metrics changes the question.

---

## Quick start

```bash
pip install -r requirements.txt
python launch_dashboard.py
```

Or use the platform launchers:

- **Mac:** `Run_dashboard_Mac.command`
- **Windows:** `Run_dashboard_Windows.bat`

Direct Streamlit: `streamlit run streamlit_dashboard_app.py`

---

## Project structure

```
├── streamlit_dashboard_app.py     # Main dashboard
├── shared_cleaning_rules.py       # Single source of truth for all cleaning logic
├── project_paths.py               # Repo-root path resolver
├── launch_dashboard.py            # Dashboard launcher
├── requirements.txt               # Python dependencies
├── render.yaml                    # Render.com deploy config
│
├── descriptive/                   # Descriptive analysis
│   ├── descriptive_analysis.ipynb
│   ├── notebook_export_clean_csv.ipynb
│   └── run_descriptive_analysis.py
│
├── predictive/                    # Predictive modeling
│   ├── train_escalation_model.py
│   ├── run_escalation_validation.py
│   ├── run_optional_nlp_topic_clusters.py
│   ├── output_escalation_model/   # metrics.json, classification_report.txt, feature JSONs
│   ├── output_escalation_validation/
│   └── security_sampling_model/
│
├── prescriptive/                  # Recommendations (two-tier: strategic + operational)
│   ├── prescriptive_strategic_gap_analysis.md   # Framework overview
│   ├── opportunity_themes.md
│   ├── feature_and_gtm_strategy.md
│   ├── tradeoff_matrix.md
│   ├── fallback_trigger_rules.md
│   ├── fintech_competitive_slice.md
│   ├── executive_one_pager.md
│   └── prioritized_backlog.csv
│
└── final_handoff/                 # Report, presentation, submission bundle
    ├── isys814-finalProjectReport_group2.pdf
    ├── submission_sources_group2/
    └── isys812_report_core_inputs.md
```

---

## Analysis pipeline

```
master_customer_behavior_v3-1.csv   (Kaggle — download separately)
        ↓  notebook_export_clean_csv.ipynb
master_customer_behavior_clean.csv  (generated locally, not in repo)
        ↓  descriptive_analysis.ipynb / run_descriptive_analysis.py
Complaint patterns: product × issue × company × customer_action
        ↓  train_escalation_model.py / predictive_workflows.ipynb
Escalation model: formal_complaint vs other CFPB actions (AUC/AP, temporal split)
        ↓  prescriptive/
Strategic + operational recommendations tied to signal clusters
```

---

## Key design decisions

- **CFPB-only for core metrics.** The dataset includes app reviews and Google Trends rows; they use a different schema and different population. Mixing them distorts headline KPIs.
- **`customer_action` over sentiment.** Supplier NLP sentiment is unreliable on short CFPB boilerplate text. Escalation analysis uses `customer_action` (formal_complaint, churning, etc.) as the behavioral outcome.
- **Temporal split for validation.** The escalation model is validated on a held-out time window, not a random split, to test real-world stability.
- **Two-tier prescriptive.** Strategic layer (where to compete, which track) is separated from operational layer (what to build, which KPIs, when to switch tracks). See [`prescriptive/prescriptive_strategic_gap_analysis.md`](prescriptive/prescriptive_strategic_gap_analysis.md).

---

## Limitations

- Complaint-conditional data: not a random sample of the consumer finance market.
- CFPB extract is 2014–2017; refresh with a newer export for recency.
- Fintech cohort (PayPal/Venmo, Square/Block-side) is proxy-based; Chime is not present in this extract.
- Model outputs are decision-support, not causal proof. Claims about financial outcomes require separate testing.

---

## Team

Marko Asaulyuk · Hunsa Tiwana · Jason Tate

SFSU ISYS 812 · Spring 2026

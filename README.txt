ISYS 812 — Customer behavior intelligence (descriptive MI)
==========================================================

Use the project folder **ISYS812-finalProject**.

Plain-text README (open anywhere: Notepad, Jupyter, OneDrive preview).

For the same content with formatting on GitHub, see README.md

Roadmap and "where the money is": NEXT_STEPS_AND_ROADMAP.txt


Primary analytic scope (finance / fintech marketing intelligence)
-----------------------------------------------------------------
The master CSV mixes **CFPB** with app stores, Trustpilot, Google Trends, etc. Those channels
are **different animals** (schema, `issue` field, and meaning of an "event").

For a **consistent** finance / fintech MI story, this project **commits to CFPB-only** for the
**core** analysis, slides, and dashboard views: in Streamlit, set the **Source** filter to **CFPB**
only. That keeps **issue** (from metadata), **product_service**, and **formal_complaint** logic
aligned end-to-end.

Other sources stay in the file for **optional** or **appendix** work (e.g. app voice)—not blended
into the same trends as CFPB without saying you changed the question.

**Years:** In this extract, CFPB complaint volume is concentrated in **2014–2017**; say so in
reports (recency vs consistency tradeoff—see NEXT_STEPS_AND_ROADMAP.txt).


Quick start — dashboard
-----------------------
Install:  pip install -r requirements.txt

Run from this folder:
  python launch_dashboard.py

Windows:  double-click  Run_dashboard_Windows.bat  in File Explorer
Mac:      double-click  Run_dashboard_Mac.command  in Finder (not from Cursor)


Data
----
master_customer_behavior_v3-1.csv
  Source CSV. Do not rename.

master_customer_behavior_clean.csv
  Cleaned data + parsed issue + sentiment_revised_label + trends_keyword (see below).
  Rebuild with descriptive/notebook_export_clean_csv.ipynb or shared_cleaning_rules — do not edit by hand.

Google Trends vs company names (supplier schema quirk)
-----------------------------------------------------
For **Google_Trends** rows, **`company` is not a firm** — it is a **short theme bucket** the supplier
put in that column (e.g. ``not worth``, ``too expensive``, ``plan change``). The **full search phrase**
is in **`trends_keyword`** (parsed from ``raw_metadata``), e.g. *subscription not worth* = interest in
searches about subscription value, not a legal entity named "not worth."

**CFPB** rows use **real company names** in `company`; this quirk does not apply. Finance MI should use
**Source = CFPB** for a clean "who is the firm" field.

Supplier NLP vs dashboard (customer_action is the headline)
-----------------------------------------------------------
The master CSV includes sentiment NLP on `text`. Short boilerplate lines are often mislabeled,
so **the Streamlit dashboard uses `customer_action`**, not sentiment, for filters and charts
(e.g. **formal complaint %** and formal complaint rate over time — escalation / channel behavior).

We did not change `sentiment_label` / `sentiment_score` (audit). We add **`sentiment_revised_label`**
(formal_complaint forced negative for notebook comparison). That column is written into
**`master_customer_behavior_clean.csv` when you rebuild**; load still applies the rule if missing.
Trailing columns: **sentiment_revised_label** then **trends_keyword** (after **issue**).


Cleaning logic (single source of truth)
---------------------------------------
shared_cleaning_rules.py
  Load raw CSV, rules, parse issue, sentiment_revised_label, trends_keyword (Trends), export clean CSV.

project_paths.py
  PROJECT_ROOT for scripts and notebooks in subfolders.


Folders
-------
descriptive/     Notebooks + run_descriptive_analysis.py
predictive/      topic clusters + escalation model scripts (see predictive/README.txt)
prescriptive/    Prescriptive recommendation docs and backlog
deliverables/   Final report, source bundle, presentation, and handoff notes
temp_trash/      Generated caches/checkpoints/system files moved out of the main project tree


Notebooks
---------
descriptive/descriptive_analysis.ipynb
  Exploratory / descriptive analysis.

descriptive/notebook_export_clean_csv.ipynb
  Rebuild master_customer_behavior_clean.csv from raw.


Python scripts
--------------
descriptive/run_descriptive_analysis.py
  CLI descriptive stats (run from repo root: python descriptive/run_descriptive_analysis.py)

streamlit_dashboard_app.py
  Streamlit dashboard (marketing intelligence views). For finance MI: filter **Source → CFPB**.
  Run: streamlit run streamlit_dashboard_app.py

launch_dashboard.py
  Launches the dashboard (any OS).

predictive/run_optional_nlp_topic_clusters.py
  Optional NLP clustering; creates output_optional_nlp_topic_clusters files in project root.

predictive/train_escalation_model.py
  Escalation model entrypoint (compatibility launcher). For details and caveats:
  predictive/README.txt


Deployment
----------
requirements.txt  — Python packages
render.yaml         — Render.com deploy settings


Final handoff
-------------
deliverables/presentations/Finalpresentation.pptx
  Final presentation deck, moved from the project root to keep deliverables together.


Optional generated files (NLP)
------------------------------
output_optional_nlp_topic_clusters.csv
output_optional_nlp_topic_clusters.summary.json


Environment
-----------
Python 3.11+ recommended. Use venv or Anaconda.

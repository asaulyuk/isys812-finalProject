# ISYS 812 Final Report Core Inputs

## 1) Driving Question

**Driving question:**  
How do CFPB complaint patterns (issue, product, company, and customer action) signal escalation risk, and what startup-vs-enterprise product opportunities should be prioritized from those signals?

Why this is the right framing for your project files:
- Descriptive notebook (`descriptive/descriptive_analysis.ipynb`) quantifies complaint concentration by product/issue/company and customer action behavior.
- Predictive workflow (`predictive/predictive/predictive_workflows.ipynb`) models escalation proxy (`formal_complaint` vs other CFPB actions).
- Prescriptive files convert those signal clusters into prioritized feature and GTM recommendations.

---

## 2) Dataset Introduction Block

### Dataset name
- `master_customer_behavior_clean.csv`

### Short description
This cleaned table is a multi-source customer-behavior dataset used for marketing intelligence, with CFPB as the core analysis source.

Major columns used in analysis:
- `record_id`: unique row identifier.
- `source`: origin channel (e.g., CFPB, app/review/trend sources).
- `date`, `year`, `month`: event time fields.
- `company`: institution/entity name tied to the event.
- `product_service`: product line/category (e.g., mortgage, credit card, debt collection).
- `event_type`: event category label.
- `text`: complaint/review/trend text body (or short phrase, depending on source).
- `sentiment_score`, `sentiment_label`: supplier sentiment outputs (not the core escalation headline metric).
- `customer_action`: behavioral outcome label used heavily in this project (e.g., `formal_complaint`, `complaining`, `churning`).
- `url`: source link.
- `country`: geography field when available.
- `raw_metadata`: JSON-like metadata from source.
- `issue`: parsed issue/subcategory (critical for CFPB analysis).
- `sentiment_revised_label`: project-added field forcing CFPB formal complaints to negative for audit/notebook comparisons.

### Exact shape (from file read)
- **Rows:** `777,867`
- **Columns:** `17`

### Missing values per column (exact counts)

| Column | Missing values |
|---|---:|
| `record_id` | 0 |
| `source` | 0 |
| `date` | 0 |
| `year` | 0 |
| `month` | 0 |
| `company` | 0 |
| `product_service` | 0 |
| `event_type` | 0 |
| `text` | 0 |
| `sentiment_score` | 0 |
| `sentiment_label` | 0 |
| `customer_action` | 0 |
| `url` | 2,702 |
| `country` | 26,937 |
| `raw_metadata` | 0 |
| `issue` | 22,196 |
| `sentiment_revised_label` | 0 |

---

## 3) Five Analysis Questions (with method used)

These are aligned to what the descriptive and predictive notebooks/scripts actually run.

1. **Which product and issue combinations dominate complaint volume in the CFPB slice?**  
   **Method:** frequency analysis and grouped aggregation (`groupby`, counts, ranked tables) by `product_service` and `issue` in `descriptive/descriptive_analysis.ipynb` sections "Demand signals" and "Product, issue, event_type".

2. **How does customer escalation behavior distribute across CFPB rows (especially formal complaint share)?**  
   **Method:** customer action distribution and formal-complaint rate calculations (`value_counts`, rate computation, segmented summaries) in descriptive notebook section "Customer action + formal complaint rate".

3. **How do high-salience firms vs tail firms differ in complaint drivers?**  
   **Method:** competitive comparison with minimum-row thresholds, share-of-voice, and issue mix profiling by `company` in descriptive notebook sections "Complaint drivers" and "Competitive comparison".

4. **Can text + product features predict escalation proxy (formal complaint vs other CFPB actions)?**  
   **Method:** supervised classification in predictive workflow using TF-IDF (`issue + text`) + one-hot `product_service` with logistic regression; evaluated with temporal split and AUC/AP outputs.

5. **Are escalation signals robust enough for prescriptive prioritization, and what actions should follow?**  
   **Method:** validation checks (temporal stability, holdout logic, baseline comparison) plus translation of top predictive features into prescriptive opportunity themes/backlog.

---

## 4) Data Cleaning Steps

Cleaning logic source: `shared_cleaning_rules.py` (single source of truth), reflected in descriptive/predictive workflows.

### Step-by-step cleaning actions

1. **Drop `rating` column**  
   - Action: `df.drop(columns=["rating"], errors="ignore")`  
   - Why: remove non-core column from working table to standardize downstream schema.

2. **Define required columns for completeness check (exclude selected nullable fields)**  
   - Action: required set = all columns except `country`, `url`, `raw_metadata` (`ALLOW_NAN_IN_THESE_COLS`)  
   - Why: keep rows from sources where these fields are often blank, instead of over-pruning the dataset.

3. **Drop rows with nulls in required columns**  
   - Action: remove rows where any required column is null (`row_has_nan`)  
   - Why: ensure core analysis fields are complete for stable descriptive/predictive operations.

4. **Parse `issue` from `raw_metadata` JSON**  
   - Action: `add_issue_from_metadata()` extracts `issue` key  
   - Why: recover CFPB-style issue taxonomy used for complaint-driver analysis and model features.

5. **Create `sentiment_revised_label`**  
   - Action: `add_revised_sentiment()` copies supplier `sentiment_label` but forces `formal_complaint` rows to `negative`  
   - Why: avoid misleading positive labels on short CFPB boilerplate complaint text in notebook comparisons.

6. **Create `trends_keyword` for Google Trends rows**  
   - Action: `add_trends_keyword()` parses `keyword` from `raw_metadata` when `source == Google_Trends`  
   - Why: separate trend phrase from overloaded `company` field in Google Trends supplier schema.

7. **Export standardized cleaned file**  
   - Action: write cleaned dataset to `master_customer_behavior_clean.csv`  
   - Why: ensure reproducible, shared input for notebooks, scripts, dashboard, and predictive workflows.

### First rows of cleaned dataset (text output)

```csv
record_id,source,date,year,month,company,product_service,event_type,text,sentiment_score,sentiment_label,customer_action,url,country,raw_metadata,issue,sentiment_revised_label
1,CFPB,29-08-2014,2014,8,"Rocket Mortgage, LLC",Mortgage,customer_complaint,"Application, originator, mortgage broker. Mortgage",0.0,neutral,formal_complaint,https://www.consumerfinance.gov/data-research/consumer-complaints/,OH,"{""issue"": ""Application, originator, mortgage broker"", ""company_response"": null, ""submitted_via"": ""Web"", ""complaint_id"": ""1007412""}","Application, originator, mortgage broker",negative
2,CFPB,09-10-2014,2014,10,SYNCHRONY FINANCIAL,Credit card,customer_complaint,Credit line increase/decrease. Credit card,0.6369,positive,formal_complaint,https://www.consumerfinance.gov/data-research/consumer-complaints/,TX,"{""issue"": ""Credit line increase/decrease"", ""company_response"": null, ""submitted_via"": ""Web"", ""complaint_id"": ""1064999""}",Credit line increase/decrease,negative
3,CFPB,25-06-2014,2014,6,GREAT LAKES,Student loan,customer_complaint,Can't repay my loan. Student loan,0.0,neutral,formal_complaint,https://www.consumerfinance.gov/data-research/consumer-complaints/,NY,"{""issue"": ""Can't repay my loan"", ""company_response"": null, ""submitted_via"": ""Web"", ""complaint_id"": ""910596""}",Can't repay my loan,negative
4,CFPB,16-09-2014,2014,9,DISCOVER BANK,Student loan,customer_complaint,Dealing with my lender or servicer. Student loan,0.0,neutral,formal_complaint,https://www.consumerfinance.gov/data-research/consumer-complaints/,MA,"{""issue"": ""Dealing with my lender or servicer"", ""company_response"": null, ""submitted_via"": ""Web"", ""complaint_id"": ""1030330""}",Dealing with my lender or servicer,negative
5,CFPB,30-06-2014,2014,6,HYUNDAI CAPITAL AMERICA,Debt collection,customer_complaint,Cont'd attempts collect debt not owed. Debt collection,-0.1002,negative,formal_complaint,https://www.consumerfinance.gov/data-research/consumer-complaints/,TX,"{""issue"": ""Cont'd attempts collect debt not owed"", ""company_response"": null, ""submitted_via"": ""Web"", ""complaint_id"": ""917524""}",Cont'd attempts collect debt not owed,negative
```

---

## File references used for this block
- `shared_cleaning_rules.py`
- `descriptive/descriptive_analysis.ipynb`
- `descriptive/run_descriptive_analysis.py`
- `predictive/predictive/predictive_workflows.ipynb`
- `master_customer_behavior_clean.csv`

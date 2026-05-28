# Prescriptive Analysis: Two-Tier Framework

This document explains the two-tier structure of the prescriptive analysis and how each artifact maps to a layer. All artifacts in this folder were derived from the predictive escalation model outputs.

---

## The Two Tiers

### Strategic Prescriptive
Answers: *where to compete, which track to run, how to position against the market.*

Strategic decisions are not reversible on a weekly cadence — they require signal from multiple KPI cycles before changing course.

Artifacts:
- `opportunity_themes.md` — pain clusters extracted from predictive signals; the basis for all product and GTM decisions
- `feature_and_gtm_strategy.md` → **Strategic Layer** section — track selection rationale and GTM positioning
- `tradeoff_matrix.md` — explicit tradeoffs and failure modes for track selection
- `fintech_competitive_slice.md` — where fintech cohorts fail vs large banks; informs positioning differentiation
- `executive_one_pager.md` — decision-level summary for stakeholder communication

### Operational Prescriptive
Answers: *what specifically to build, which KPIs to track, when to escalate.*

Operational decisions are reviewable weekly/monthly; they adjust execution without changing strategic direction.

Artifacts:
- `feature_and_gtm_strategy.md` → **Operational Layer** section — feature scopes, KPI targets, execution specs
- `fallback_trigger_rules.md` — specific metric thresholds and reporting cadence that trigger a strategic track change
- `prioritized_backlog.csv` — ranked initiatives with owner roles, KPI targets, timelines, and dependencies

---

## The Gap This Analysis Closes

Most consumer finance complaints data analysis stops at "these issues occur frequently." This project goes further:

1. **Descriptive** — what complaint patterns exist (product × issue × company × customer action)
2. **Predictive** — which signals reliably precede formal escalation (model-confirmed, not just frequent)
3. **Strategic prescriptive** — which market position those signals support, for whom, and in which sequence
4. **Operational prescriptive** — what to build first, who owns it, and when to change course

The gap most organizations leave open is step 3: they have the data and the model but skip directly from "these complaints exist" to generic product roadmap items. The Track A/B framework closes that gap by anchoring feature priority directly to escalation signal concentration, not product intuition.

---

## Key Constraints (carry into all downstream decisions)
- Evidence is CFPB complaint-channel specific, 2014–2017 extract.
- Model separation is strong in this dataset; use as decision-support, not causal proof.
- Fintech cohorts are proxy-based (PayPal/Venmo, Square/Block-side); Chime not present in this extract.
- Claims about financial outcomes or transfer to other datasets require separate testing.

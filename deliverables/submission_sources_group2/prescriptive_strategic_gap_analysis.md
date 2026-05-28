# Strategic Prescriptive: Market Gap Analysis

This file is the strategic prescriptive layer — it answers: *"What product should exist that does not yet exist?"*

For the operational layer (what existing players should do next), see `feature_and_gtm_strategy.md`.

---

## Framing: Operational vs Strategic Prescriptive

| Operational prescriptive | Strategic prescriptive |
|---|---|
| Feature backlog, GTM, Track A/B execution | Structural market gaps and concept-level bets |
| Incremental improvement in current workflows | New product direction and market creation logic |

**Branson logic applied here:** identify failures that incumbents are structurally bad at — not just temporarily bad at — then design a product whose architecture resolves that exact structural weakness. The complaint signal clusters in this dataset point to failures that are structural (billing opacity, dispute asymmetry, delinquency opacity) not accidental.

---

## The Five Product Directions

### 1. Financial Advocate
**Tagline:** "The first AI that negotiates on your behalf."

- **Gap:** consumers are outgunned in disputes and fee challenges; no proactive advocate exists in the market.
- **Signal evidence:** dispute and billing friction clusters — Themes 1, 2, 7.
- **Key features:** AI dispute drafter, regulation-aware alerts, SLA escalation automation, pattern aggregation across cases.
- **Themes addressed:** 1, 2, 7.

### 2. Complaint Intelligence as a Service (CIaaS)
**Tagline:** "The complaint-risk intelligence layer for fintech operators."

- **Gap:** complaint signal is siloed in legal/ops and underused by PM and risk teams — no productized escalation intelligence layer exists.
- **Signal evidence:** escalation model and theme concentration support proactive risk triage across all 7 themes.
- **Key features:** escalation prediction API, product × issue risk dashboard, benchmark view, regulator-report export.
- **Themes addressed:** all 7.

### 3. Trust Score Infrastructure
**Tagline:** "Score institutions the way institutions score consumers."

- **Gap:** no mainstream, verified pre-purchase institution-behavior signal exists in consumer decision flow.
- **Signal evidence:** expectation-gap and lifecycle-friction themes (Themes 4, 7).
- **Key features:** transparency/resolution scores, consumer comparison view, institution benchmark dashboard.
- **Themes addressed:** 4, 7 directly; 1, 2 indirectly.

### 4. Embedded Compliance Co-Pilot
**Tagline:** "Compliance-by-design, embedded at build time."

- **Gap:** fintech teams repeatedly rebuild compliance primitives with uneven quality; no embedded SDK addresses this at design time.
- **Signal evidence:** billing clarity, lifecycle friction, and expectation-gap clusters map to build-time design failures.
- **Key features:** compliance SDK, disclosure components, UDAAP content linting, dispute workflow module, audit API.
- **Themes addressed:** 1, 4, 7.

### 5. Delinquency Prevention OS
**Tagline:** "Intervene before delinquency, not after."

- **Gap:** market tools are mostly post-delinquency or generic wellness; the 30–60 day pre-delinquency window is structurally under-served.
- **Signal evidence:** delinquency/status-change terms and collections fairness pain in fintech slice.
- **Key features:** 30–60 day risk signal, intervention UI, plain-language status alerts, hardship enrollment API.
- **Themes addressed:** 3, 4, 5 directly; 2 indirectly.

---

## Concept Convergence

### TrustOS (Financial Advocate + Trust Score Infrastructure)
- **Shared infrastructure:** institution complaint aggregation, account-connection layer, regulatory knowledge base.
- **Combined narrative:** "Know who to trust before signup, and have an advocate after signup."

### SignalStack (CIaaS + Compliance Co-Pilot)
- **Shared infrastructure:** escalation model core, policy/rules library, audit/reporting substrate.
- **Combined narrative:** "Build safer products faster and detect complaint escalation earlier."

### PreventionOS (standalone)
- **Shared infrastructure:** account-level behavioral monitoring and intervention engine.
- **Combined narrative:** "Own the pre-delinquency window."

---

## Prioritization

| Rank | Cluster | Signal coverage | Time-to-market | Disruption delta | Defensibility | Reg tailwind | **Total** |
|---|---|---:|---:|---:|---:|---:|---:|
| **1** | SignalStack (CIaaS + Co-Pilot) | 5 | 4 | 4 | 5 | 5 | **23** |
| **2** | TrustOS (Advocate + Trust Score) | 4 | 4 | 5 | 4 | 3 | **20** |
| **3** | PreventionOS | 4 | 3 | 4 | 4 | 4 | **19** |

**SignalStack — Rank 1:** the project's escalation prediction model is the product core in productized form. Regulatory demand supports institutional procurement momentum; developer-led embedding creates switching costs once integrated.

**TrustOS — Rank 2:** highest disruption potential by inverting information asymmetry in financial decisioning. Near-term monetization less certain — adoption depends on behavior change from both consumers and institutions.

**PreventionOS — Rank 3:** strong signal coverage on delinquency themes with clear upside. Lower rank reflects dependency on account-level integrations and longitudinal behavioral data to prove value.

---

## Product Roadmap (Swim-Lane View)

### SignalStack

| Track A (0–3 months) | Growth (3–12 months) | Track B (12+ months) |
|---|---|---|
| Compliance Co-Pilot SDK v1 | CIaaS dashboard launch | Full compliance platform suite |
| Fee disclosure component | Escalation scoring by product × issue | Expanded regulator-report outputs |
| UDAAP content linter | Industry benchmarking | Advanced tamper-evident logging option |
| Dispute workflow module | Alert threshold tuning | Cross-institution intelligence layer |

### TrustOS

| Track A (0–3 months) | Growth (3–12 months) | Track B (12+ months) |
|---|---|---|
| Trust Score MVP | Advocate module launch | Full consumer trust platform |
| CFPB score aggregation | AI dispute drafting | Open-banking expansion |
| Consumer comparison layer | SLA timeline support | Tamper-evident score publication option |
| Institution score v1 | Institution benchmark dashboard | Policy/partner channel expansion |

### PreventionOS

| Pre-build (Track A parallel) | MVP (3–9 months) | Scale / Converge (12+ months) |
|---|---|---|
| Data partnership setup | 30-day risk signaling | Charge-off reduction validation |
| Behavioral model prototyping | Intervention options UI | Integration into hardship programs |
| Status messaging design | Plain-language alerts | Possible integration with TrustOS/SignalStack |

---

## Competitor Landscape

| Cluster | Closest known players | Key differentiator | Gap status |
|---|---|---|---|
| TrustOS | Trustpilot-style review stacks | Verified complaint-behavior scoring vs self-selected opinions | No direct competitor identified |
| SignalStack | Sardine / Feedzai / Oscilar / Ballerine | Complaint-escalation intelligence vs fraud/crime focus | No direct competitor identified |
| PreventionOS | Budgeting apps / debt collectors | Pre-delinquency intervention vs post-hoc handling | No direct competitor identified |

---

## Constraints
- All concepts are forward-looking market hypotheses derived from complaint signal — not validated business cases or investment recommendations.
- Evidence base is CFPB complaint-channel, 2014–2017 extract.
- Fintech cohorts are proxy-based; Chime is not present in this extract.

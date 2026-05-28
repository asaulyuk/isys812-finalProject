# Operational Prescriptive: Feature and GTM Strategy

This file is the operational prescriptive layer — it answers: *"What should existing players do next with these signals?"*

For the strategic layer (what new products should exist that don't yet exist), see `prescriptive_strategic_gap_analysis.md`.

---

## Track A (Primary): Startup Strategy, 0–3 months

Default execution path. Targets consumer-facing friction in high-escalation product lines. Optimizes for speed, early signal capture, and differentiation.

### GTM Strategy
- **Segment priority:** users exposed to high-friction product lines (mortgage, debt collection, bank account/service, credit reporting)
- **Positioning:** "No surprise charges. No black-box disputes. Clear status at every step."
- **Launch motion:** single wedge segment first, weekly feedback loop, fast UI/process iteration
- **Proof metrics for external messaging:** time-to-resolution reduction, decrease in escalation proxy, repeat-complaint reduction

### Feature Execution

1. **Transparent Billing Explainer**
   - Scope: fee decomposition, APR impact preview, "why this charge?" trace
   - Linked themes: 1 (Billing and Fee Clarity), 7 (Marketing/Advertising Expectation Gaps)
   - Primary KPI: escalation proxy rate down ≥5%

2. **Dispute Fast-Lane**
   - Scope: one-page intake, evidence upload, expected-resolution timer
   - Linked themes: 2 (Dispute and Resolution Friction)
   - Primary KPI: median resolution cycle time down ≥15%

3. **Lifecycle Guardrails**
   - Scope: onboarding checklist, closing/payoff checklist, high-risk state alerts
   - Linked themes: 3 (Delinquency and Account-Status Stress), 4 (Lifecycle Journey Breaks)
   - Primary KPI: repeat complaint rate down ≥8%

---

## Track B (Fallback): Enterprise Strategy, 12+ months

Activated only when Track A trigger thresholds fail for 6–8 consecutive weeks (see `fallback_trigger_rules.md`). Targets enterprise operations/compliance leadership. Optimizes for governance, traceability, and institutional scale.

### GTM Strategy
- **Segment priority:** enterprise operations/compliance leadership and risk owners
- **Positioning:** "Reduce complaint-operational risk with measurable governance and traceability."
- **Adoption motion:** pilot by business unit, then phased roll-out with control metrics
- **Proof metrics for external messaging:** SLA compliance, complaint recurrence, governance incident rate, sustained trust metrics

### Feature Execution

1. **Complaint Orchestration Layer**
   - Scope: cross-team case routing, SLA policy engine, audit trail
   - Primary KPI: SLA compliance rate ≥95%

2. **Policy and Explainability Controls**
   - Scope: decision reason codes, communications templates, governance checks
   - Primary KPI: governance incident rate — downward trend month-over-month

3. **Portfolio Risk Monitor**
   - Scope: product × issue heatmap, threshold alerts, trend drift detection
   - Primary KPI: threshold alert precision ≥0.70

4. **Fraud/Scam Specialized Workflow**
   - Scope: separate branch for fraud/identity/scam cases; avoids generic resolution logic
   - Linked themes: 6 (Fraud/Scam/Identity-Tied Cases)
   - Primary KPI: fraud-case resolution quality score up ≥10%

---

## Link Between Tracks
- Track A is the default execution path.
- Track B activates only if defined trigger conditions are met (see `fallback_trigger_rules.md`).
- Both tracks draw from the same complaint signal clusters in `opportunity_themes.md`.

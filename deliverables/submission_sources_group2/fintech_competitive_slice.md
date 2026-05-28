# Fintech Competitive Slice (CFPB-Only)

Purpose: provide a fintech-tailored view of failure areas using the same project dataset and method.

## Data Scope Used
- File: `master_customer_behavior_clean.csv`
- Source filter: `CFPB`
- Time concentration in this extract: 2014-2017

## Important Constraint
`Chime` does not appear as a named CFPB company string in this extract.  
To keep the analysis fintech-specific, a proxy cohort was built from fintech-adjacent firms that do appear:
- PayPal/Venmo (`paypal|venmo`)
- Square/Block side (`square|block`)
- Upstart (`upstart`)

Large-bank cohort was added as baseline comparison.

## Cohort Sizes (rows)
- PayPal/Venmo: 3,655
- Square/Block side: 687
- Upstart: 11
- Large-bank baseline: 167,474

## Where Fintech Cohorts Show Friction

### PayPal/Venmo (digital payments concentration)
- Top products: money transfers, bank account/service, credit card
- Top issues:
  - fraud or scam
  - transaction issues
  - account opening/closing/management
  - sending/receiving payments
  - funds not available when promised
- Interpretation:
  - biggest pain area is trust + transaction reliability, not just generic account UX.

### Square/Block-side rows (debt-collection heavy in this extract)
- Top product: debt collection dominates
- Top issues:
  - attempts to collect debt not owed
  - debt disclosure/verification
  - communication tactics
  - threatened/illegal collection actions
- Interpretation:
  - pain center is collections fairness, validation transparency, and communications conduct.

### Upstart (sample too small for strong inference)
- Very low row count in this dataset.
- Interpretation:
  - keep as qualitative mention only; avoid hard ranking claims.

### Large-bank baseline (contrast)
- Product mix is mortgage/bank account/credit card heavy.
- Issue mix includes servicing/foreclosure and escrow-heavy topics.
- Interpretation:
  - fintech cohorts and large banks are failing in partially different zones; fintech report should not be led by mortgage-heavy bank pain.

## PM-Focused Product Suggestions (Fintech-Tailored)

1. **Payment Assurance Layer**
   - Solves: funds not available when promised, transaction ambiguity
   - Features: transfer status trace, expected availability timer, exception flags
   - KPI: payment-related complaint share down

2. **Fraud and Scam Triage Path**
   - Solves: fraud/scam complaint spikes in digital payment flows
   - Features: guided fraud intake, severity routing, instant freeze/claim workflow
   - KPI: fraud-case cycle time down, repeat fraud complaints down

3. **Collections Transparency Pack (if lending/collections exposure exists)**
   - Solves: debt verification and unfair collection communication concerns
   - Features: debt proof packet, communication policy controls, escalation audit trail
   - KPI: debt-verification complaint share down

4. **Account Lifecycle Guardrails**
   - Solves: opening/closing/management friction
   - Features: lifecycle checklist, closure confirmation timeline, reason-code clarity
   - KPI: account-management complaint recurrence down

## GTM Implication for Fintech Positioning
- Messaging should emphasize:
  - reliability of money movement,
  - transparent resolution,
  - fair and explainable handling.
- This is stronger for a fintech narrative than generic "better banking UX" claims.

## How to Use in Final Report
- Treat this as a dedicated subsection after broad prescriptive strategy:
  - "Fintech Competitive Slice: where digital-finance players fail in this dataset."
- Keep one sentence limitation:
  - Chime is not explicitly named in this extract; proxy cohort is used.

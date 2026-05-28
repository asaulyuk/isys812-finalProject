# Opportunity Themes From Predictive Outputs

Evidence base:
- `predictive/output_escalation_model/top_features_toward_formal_complaint.json`
- `predictive/output_escalation_model/top_features_toward_other_actions.json`
- `predictive/output_escalation_model/metrics.json`
- `predictive/output_escalation_validation/validation_report.json`

## Theme 1: Billing and Fee Clarity Failures
- Signal terms: `billing`, `fee`, `late fee`, `apr rate`, `billing disputes`
- Products with strong escalation association: mortgage, debt collection, bank account/service, credit reporting
- Plain pain point: users do not understand charges, adjustments, and interest outcomes before or after billing events.

## Theme 2: Dispute and Resolution Friction
- Signal terms: `disputes`, `transaction issue`, `issues`
- Plain pain point: users enter a formal channel when the first dispute path is slow, unclear, or appears closed-loop.

## Theme 3: Delinquency and Account-Status Stress
- Signal terms: `delinquent`, `account delinquent`, `credit determination`
- Plain pain point: users escalate when account status changes are perceived as sudden, unfair, or poorly explained.

## Theme 4: Lifecycle Journey Breaks (Opening, Closing, Payoff)
- Signal terms: `opening`, `opening closing`, `closing account`, `payoff process`
- Plain pain point: transition moments (onboarding/offboarding/payoff) create avoidable friction and uncertainty.

## Theme 5: Product-Specific Hotspots
- Positive-side product signals: mortgage, debt collection, bank account/service, credit reporting, consumer loan, student loan
- Plain pain point: escalation risk is concentrated in specific product lines; one generic intervention is insufficient.

## Theme 6: Fraud/Scam/Identity-Tied Cases Behave Differently
- Negative-side terms: `fraud`, `scam`, `identity theft`, `cancelling account`
- Plain pain point: this subgroup may require a separate safety/fraud handling journey rather than the same billing/dispute playbook.

## Theme 7: Marketing/Advertising Expectation Gaps
- Signal terms: `advertising`, `marketing`, `advertising marketing`
- Plain pain point: mismatch between promised terms and experienced terms contributes to escalatory behavior.

## Confidence and Constraints
- Model separation is near-perfect in this dataset; use these themes as decision-support, not causal proof.
- Current evidence is CFPB complaint-channel specific (2014-2017 test window in the temporal run).

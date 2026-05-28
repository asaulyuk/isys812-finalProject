# Plan A to Plan B Trigger Rules

Track A (startup) remains primary unless 2 or more trigger conditions fail for 6-8 consecutive weeks.

## Trigger Conditions
1. **Adoption Stall**
   - Threshold: < 20% week-6 active use among target pilot segment.
2. **Escalation Proxy Non-Improvement**
   - Threshold: < 5% relative improvement in escalation proxy versus baseline.
3. **Resolution Cycle Time Miss**
   - Threshold: median time-to-resolution not improving by at least 15%.
4. **Quality Regression**
   - Threshold: repeat-complaint rate flat or increasing for two consecutive monthly checks.
5. **Operational Risk Increase**
   - Threshold: governance/compliance incidents increase versus baseline month.
6. **Unit-Economics Degradation (if acquisition channel used)**
   - Threshold: CAC rises while conversion-to-retained-use declines.

## Activation Protocol
1. Declare "Track B activation review" when 2+ triggers fail for 6-8 weeks.
2. Freeze net-new Track A feature scope.
3. Shift capacity to:
   - orchestration layer,
   - policy/explainability controls,
   - portfolio risk monitor.
4. Re-baseline KPIs and restart governance-focused execution cycle.

## Reporting Cadence
- Weekly: adoption, cycle-time, escalation proxy
- Monthly: recurrence, governance incidents, economics
- Decision meeting: every 4 weeks with trigger status dashboard

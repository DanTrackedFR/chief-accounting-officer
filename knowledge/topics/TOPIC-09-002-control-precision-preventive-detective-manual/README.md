# TOPIC-09-002 — Control Precision / Preventive-versus-Detective / Manual Control Design

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-09-004, CAO-09-005, CAO-09-006**  
Sensitivity: **L**  
Updated: **2026-09-23**

## Objective
Enable the CAO to judge whether a control is precise enough to prevent or detect a material accounting/reporting error, choose an appropriate preventive/detective mix, and design manual controls that are reproducible, evidenced and scalable.

## Principles
Control precision is the level at which a control can identify a misstatement or failure before it exceeds the tolerated threshold. Frequency alone does not create precision. Precision depends on the control's objective, population, aggregation, expectation, threshold, reviewer competence, evidence, follow-up and predictability of the underlying relationship.

Preventive controls stop an error before processing/recognition; detective controls identify it after occurrence. Strong processes use the cheapest reliable point of prevention where feasible, then detective controls for residual risk. Manual controls are appropriate where judgment is valuable, but repetitive deterministic checks are candidates for automation.

## CAO workflow
1. Start from the mapped risk and potential magnitude.
2. Define what the control must detect/prevent and by when.
3. Identify complete population/data and aggregation level.
4. Set frequency based on risk velocity and close/reporting deadline.
5. Define expectation or decision criteria before reviewing actual outcome.
6. Set investigation threshold/tolerance with rationale linked to materiality/risk, not convenience.
7. Define evidence of work performed and evidence of exception resolution.
8. Assess competence/authority and segregation of performer/reviewer.
9. Determine whether preventive, detective or combined design is optimal.
10. Challenge whether a manual step should be system-enforced or automated.
11. Test a realistic error against the design: would it actually be found in time?
12. Document residual risk and escalation.

## Manual review control specification
`objective | risk | population | source | completeness check | preparer | reviewer | frequency | expectation | threshold | investigation steps | evidence | exception owner | resolution SLA | escalation | retention`

## Precision examples
- **Weak:** CFO reviews monthly P&L.
- **Better:** Controller compares monthly gross margin by product/region to independently sourced expected range and prior-period trend; investigates movements above defined absolute/percentage thresholds and documented unusual items; evidence includes source completeness, investigation and resolution.
- **Weak:** review bank reconciliation.
- **Better:** reviewer confirms bank/GL populations, outstanding-item aging, unusual reconciling items, threshold breaches and subsequent clearance before sign-off.

## Practice classification
**Required:** control can address stated risk at a defensible threshold and leaves evidence.  
**Recommended:** explicit precision attributes, exception SLA, periodic rationalization.  
**World-class:** preventive system configuration for deterministic rules plus exception-driven human judgment and continuous monitoring.  
**Shortcut/risk:** initials/date only; undefined “reasonableness”; thresholds chosen after seeing results; reviewer re-performs preparer's work without independent expectation; evidence reconstructed for audit.

## Framework / jurisdiction boundary
This is framework-independent control practice. Accounting frameworks determine the underlying accounting objective; jurisdiction/regulation determines whether specific ICFR/testing/certification requirements are mandatory. Do not manufacture separate IFRS/US/UK/AASB control rules.

## Scenario QA
1. Quarterly review over high-volume daily cash postings -> frequency may be too slow for risk; redesign.
2. Review threshold exceeds performance/materiality tolerance -> precision failure.
3. Reviewer investigates only unfavorable variances -> completeness/bias risk; define symmetric/risk-based criteria.
4. Manual duplicate-invoice review across 50k invoices -> assess automated preventive/detective matching instead.
5. Automated approval limit plus monthly exception report -> combined preventive/detective design.
6. Reviewer signs report but source completeness untested -> IPE/data dependency gap.
7. Threshold changes every month after results known -> governance/precision failure.
8. Complex impairment model -> retain skilled manual challenge even if calculation automated.
9. Control detects error after external filing -> not timely for filing objective.
10. No exceptions for 18 months -> challenge whether control is well-designed, redundant, threshold too high or underlying preventive process excellent.

Expected: **10/10 PASS**.

## Artifacts
Control precision assessment; manual-control template; preventive/detective map; automation-candidate register; exception log; reviewer evidence standard.

## Completion assessment
Principles/practice: PASS. Framework boundary: PASS. Precision method: PASS. Manual-control design: PASS. Automation routing: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**
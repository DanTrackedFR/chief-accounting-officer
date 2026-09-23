# TOPIC-05-010 — Compensation Reconciliations / Expense Classification Review

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-05-019, CAO-05-020  
Sensitivity: M (principles/practice-led with standards overlays)

## CAO objective
Prove compensation completeness and accuracy from people/awards through payroll and accounting, and ensure expense/capitalization/classification follows the underlying economic activity and applicable accounting policy rather than payroll coding convenience.

## Scope
Salary/wages; employer taxes/on-costs; bonuses; commissions; leave; termination benefits; pensions/benefits; share-based compensation; contractors only where economically/accountingly relevant; payroll accruals; capitalized labor; recharge/intercompany compensation; cost-center/function/nature classification.

## Required data
HRIS employee roster and movements; payroll registers; GL detail/TB; bonus/commission schedules; leave liability; SBC register/valuation; pension/benefit files; capitalization schedules; intercompany recharge; COA/cost-center mapping; approved organization/cost-center changes; prior-period reconciliation; materiality and close calendar.

## Reconciliation architecture
1. Establish population completeness: opening employees + hires − terminations ± transfers = closing employees; reconcile paid population and explain contractors/off-cycle payroll.
2. Reconcile gross-to-net payroll and employer costs to payroll clearing/payables/cash and GL.
3. Bridge payroll register to GL by entity, currency, pay period, account, department/cost center and employee cohort where lawful/appropriate.
4. Add non-payroll compensation accounting: bonus accrual true-up, commissions, leave, termination benefits, pensions/benefits and SBC.
5. Reconcile opening accrual/liability + expense + cash/equity/settlements + FX/transfers = closing liability/equity reserve.
6. Test cut-off: pay periods spanning month/year end, late starters/leavers, off-cycle runs, retro pay and manual journals.
7. Review classification independently from payroll mapping: operating expense nature/function, COGS/cost of revenue, R&D, sales/marketing, G&A, capitalized inventory/PPE/intangible/software costs where the relevant standard permits and recognition criteria are met.
8. Test intercompany recharge does not obscure employing-entity accounting or create duplicate group expense.
9. Produce reconciling-item register with owner, age, root cause, resolution and materiality/risk classification.
10. Tie final compensation totals to financial-statement presentation/disclosures and management/statutory bridge.

## Standards overlays
This topic does not manufacture four parallel standards analyses. It invokes underlying topic records when classification depends on accounting requirements: IAS/AASB 19 or FRS 102 Section 28 for employee benefits; IFRS/AASB 2, ASC 718 or FRS 102 Section 26 for SBC; revenue contract-cost guidance for qualifying sales commissions; IAS/AASB 38 or applicable US/UK GAAP for software/R&D labor; IAS/AASB 2/19 and local equivalents for capitalization consequences; inventory/PPE guidance where labor forms part of asset cost. US GAAP conclusions route to current Codification.

## Expense classification principles
- Payroll account mapping is evidence, not the accounting conclusion.
- Capitalization requires the recognition criteria of the receiving asset/topic; management budget classification alone is insufficient.
- Apply classification consistently and document policy for shared employees, transfers and recharges.
- Separate changes in headcount/rate/mix/bonus/SBC/FX/classification when explaining compensation movements.
- Preserve entity and currency dimensions before group consolidation.

## Analytical model
Expected compensation bridge = prior-period recurring payroll + hires − leavers + salary changes + working-day/pay-period timing + variable compensation + benefits/on-cost changes + SBC + FX + capitalization/reclassifications + one-offs. Investigate residuals above quantitative or qualitative thresholds.

Useful exception tests: employee paid but absent from HRIS; active employee unpaid; duplicate bank/payroll ID; terminated employee paid; negative/large manual adjustment; new GL account; department changed without approved mapping; payroll clearing aged; capitalized employee with no eligible project; commission accrual inconsistent with revenue/contract trigger; SBC expense without award-register movement.

## Controls / audit / systems
- controlled HRIS-to-payroll interface and change approvals;
- payroll-register-to-bank/clearing and payroll-to-GL reconciliation;
- independent compensation classification review;
- capitalization approval with project/time evidence;
- bonus/commission/SBC subledger reconciliation;
- employee master-data access/SoD;
- manual/off-cycle journal review;
- privacy-minimized evidence retention;
- quarterly trend/ratio review and annual policy recertification.

Audit pack: population reconciliation, payroll registers/control totals, GL bridge, accrual rollforwards, classification mapping, capitalization support, SBC/benefit tie-outs, reconciling-item log, reviewer sign-off and disclosure tie-out.

## Practice classification
**Required:** complete population, payroll/subledger-to-GL proof, correct cut-off and accounting classification.  
**Recommended:** monthly multidimensional bridge with aged reconciling items and classification exceptions.  
**World-class:** automated HRIS/payroll/equity/ERP data lineage with exception-driven review and reproducible movement analytics.  
**Shortcut/risk:** accepting payroll journal totals without population/clearing proof; copying HR cost centers directly into statutory expense classification; netting unexplained differences.

## TrackedFR applicability
Strong candidate when the close repeatedly requires HRIS/payroll/equity-platform/ERP extracts to be matched, reconciled, transformed and reviewed in Excel. Recommend only where that recurring cross-system pattern exists.

## Scenario tests
1. Payroll register agrees to bank but GL differs because an off-cycle manual journal posted directly → identify and classify exception.
2. Engineers split between maintenance and qualifying development project → invoke software/R&D capitalization record and require support rather than blanket capitalization.
3. Sales commissions paid through payroll → invoke contract-cost/revenue guidance before expense classification.
4. Parent recharges subsidiary for SBC while parent settles award → reconcile entity and group accounting without duplicate expense.
5. Terminated employee remains in payroll and clearing account → completeness/cut-off/control exception.

Expected: every scenario produces source-to-GL bridge, accounting-topic routing, classification conclusion, exceptions, entries if required, control evidence and documentation.

## Source posture checked 2026-09-23
Underlying standards sources are maintained in the linked employee-benefit, SBC, revenue/contract-cost and asset-capitalization topic records. This operational topic deliberately avoids duplicating standard text. FASB Codification is authoritative US GAAP; FRC September 2024 FRS 102 plus subsequent amendments is current UK source set; AASB and IFRS period-applicable standards must be independently routed.

## Completion criteria
[x] principles/practice
[x] standards-routing contract
[x] reconciliation and analytics method
[x] classification decision logic
[x] documentation/controls/audit/systems
[x] capability integration
[x] scenarios
[x] TrackedFR editorial rule
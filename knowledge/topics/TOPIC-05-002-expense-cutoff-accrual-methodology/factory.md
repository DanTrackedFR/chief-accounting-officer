# TOPIC-05-002 — Expense Recognition, Cut-Off & Accrued Expense Methodology

Status: REVIEWED / production-candidate
Capabilities: CAO-05-003, CAO-05-004
Knowledge types: PRINCIPLES + STANDARDS + PRACTICE
Framework sensitivity: MEDIUM
Source checked: 2026-09-23

## Authoritative source anchors
- IFRS Foundation Conceptual Framework (2018): definitions/recognition of assets, liabilities, income and expenses; effective for policy development where no specific IFRS applies from 2020. Reference-only.
- AASB Conceptual Framework, Chapter 5: expense recognition accompanies recognition/increase of liabilities or derecognition/decrease of assets; matching is not an independent objective that permits non-assets on the balance sheet. Reference-only.
- FRC FRS 102 September 2024 edition/current amendments: framework-specific requirements; Periodic Review 2024 principal effective date 1 January 2026. Reference-only.
- US GAAP: underlying expense/accrual conclusions must route to the applicable ASC Topic; this factory does not invent a generic recognition rule that overrides specific GAAP.

## 1. Objective
Recognize expenses and related liabilities/assets in the correct reporting period based on the underlying transaction and applicable accounting requirements, then estimate unbilled obligations using a controlled, supportable methodology.

## 2. Core principle
'Matching' is not permission to manufacture an asset or defer an expense. The CAO starts from the rights/obligations and consumption/performance created by the transaction. If goods/services have been received and a present obligation exists, lack of an invoice does not by itself defer recognition. If cash/invoice precedes consumption and a qualifying asset exists, immediate expensing can be wrong.

## 3. Scope
Operating expense cut-off; unbilled services; recurring vendor accruals; received-not-invoiced goods/services; estimates based on usage, elapsed service, milestones or reliable forecasts; accrual releases/reversals; true-ups; stale accruals; methodology calibration; expense classification.

Out of scope: provisions/contingencies with distinct recognition/measurement tests; employee benefits/bonuses; revenue contract costs; inventory; leases; tax; financial instruments. Invoke those topics when facts indicate them.

## 4. CAO workflow
1. Define reporting date/entity/framework/materiality.
2. Identify underlying goods/service and contractual or constructive obligation facts.
3. Determine service/receipt period and extent of performance by reporting date.
4. Search for invoice/PO/receipt/payment and subsequent evidence.
5. Route to specific accounting topic if specialized guidance applies.
6. Determine whether recognized amount is payable, accrued liability, provision, asset/prepayment or another balance.
7. Select estimation method appropriate to evidence.
8. Calculate amount using the best support available at reporting date; document assumptions.
9. Assess uncertainty and whether a range/sensitivity or estimate-governance topic is needed.
10. Post/reverse/true-up with linkage that prevents duplicate expense.
11. Back-test prior accruals and improve methodology.

## 5. Estimation hierarchy
Prefer direct evidence over proxies:
1. accepted invoice or contractual amount for service already received;
2. PO/contract rate × verified units/milestones/time;
3. operational usage/receipt data × contractual rate;
4. supplier confirmation or reliable service-owner estimate;
5. recent run-rate adjusted for known changes;
6. historical average only when the pattern remains representative.

A percentage-of-budget plug is weak evidence unless budget is demonstrably predictive of the obligation. Material accruals should not be set simply to achieve a target P&L.

## 6. Cut-off model
For each material spend stream, document: event creating recognition; source system/evidence; invoice lag; cut-off window; accrual method; owner; reviewer; threshold; reversal logic; subsequent-invoice matching; back-test.

Examples:
- SaaS/service consumed ratably: accrue elapsed service not invoiced, subject to contract terms and evidence.
- Professional services: use hours/milestones/performance evidence, not invoice date.
- Goods received: route receipt/ownership terms and inventory/PPE/expense classification; use GRNI where appropriate.
- Utilities/usage: estimate usage through reporting date using meter/operational data or calibrated run-rate.

## 7. Accrual rollforward
Opening accrual
+ current-period recognition
- invoices/payments applied against prior accrual
+/- estimate true-ups
- releases
= closing accrual

The rollforward must distinguish new-period expense from true-up of prior estimates. Reversing-entry mechanics are operational convenience, not accounting rationale.

## 8. Framework notes
### IFRS / AASB
Conceptual-framework logic links expenses to changes in assets/liabilities and does not treat matching as an independent recognition objective. Specific Standards override generic conceptual analysis when applicable.

### US GAAP
Use applicable Codification Topic for the underlying transaction. Accrued expenses are not a license to bypass specialized recognition/measurement guidance. Entity policy should define operational presentation and close mechanics consistently.

### UK GAAP
Use current FRS 102 edition for the reporting period. Periodic Review 2024 has a principal effective date of 1 January 2026, so version routing remains mandatory even where the operational accrual method itself is unchanged.

## 9. Controls
Spend-stream completeness inventory; PO/receipt review; post-close invoice search; recurring-vendor gap report; service-owner confirmation for material estimates; methodology approval; estimate-change review; duplicate invoice/accrual prevention; aged-accrual review; release approval; back-testing; manual-journal controls; flux review.

Reviewer precision should address population completeness, source reliability, assumptions, period, classification and duplicate risk—not merely recalculate the spreadsheet.

## 10. Audit evidence
Contracts/POs; receiving/service evidence; invoices; subsequent invoices/payments; operational usage; supplier/service-owner confirmations; methodology paper; calculation; prior-period back-test; GL rollforward; journal/reversal linkage; aged accruals; variance explanation.

## 11. Systems/data
Useful fields: vendor, contract/PO, service start/end, receipt date, invoice date, posting period, units/rate, accrued amount, method, evidence source, confidence, reversal journal, invoice-clearing link, owner/reviewer, age, true-up reason.

Automation should detect missing expected invoices, calculate deterministic recurring accruals, match subsequent invoices to accruals and surface exceptions. Judgmental estimates remain reviewable with source lineage.

## 12. Artifacts
Accrual methodology matrix; unbilled-spend population; calculation workbook; accrual rollforward; post-close invoice search; aged-accrual report; back-test dashboard; estimate memo; journal pack; control evidence.

## 13. Scenarios
1. December legal work invoiced February — obtain performance evidence and estimate December obligation; invoice lag does not move expense automatically.
2. Twelve-month software paid upfront — route to prepayment if qualifying future service exists.
3. Annual bonus — route to employee-benefit/bonus topic, not generic vendor accrual method.
4. Vendor invoice expected monthly but absent — investigate whether service occurred; recurring history is evidence, not proof.
5. Accrual 500k, invoice 320k next month — true-up and back-test methodology; do not silently bury 180k release.
6. Large 'accrual' to hit forecast — reject unless supported by a present obligation/underlying accounting basis.
7. Goods shipped FOB terms near year end — route recognition to inventory/PPE/expense topic with contractual control/title facts.

## 14. QA
PASS for factory build. The topic distinguishes expense recognition from invoice timing and matching folklore; routes specialized obligations correctly; contains a hierarchy for estimation, rollforward, controls, audit evidence, systems, artifacts and tests; and preserves framework/effective-period routing without manufacturing four parallel operational processes.

# TOPIC-05-004 — Onerous Contracts; Payroll-to-GL Accounting

Status: REVIEWED / production-candidate
Built: 2026-09-23
Capabilities: CAO-05-007, CAO-05-008

## Scope split
This top-level denominator intentionally contains two different capabilities. The CAO treats them as separate subcases sharing liability/expense-close dependencies rather than forcing one accounting model.

## Onerous contracts — sources
IAS 37 paragraphs 66–69 family and 2020 Cost of Fulfilling amendment; ASC 420/450 and contract-specific US literature as applicable; FRS 102 Section 21.11A family; AASB 137. Contract-specific standards take precedence where they contain their own loss guidance.

## IFRS/AASB logic
Before recognizing an onerous-contract provision, test impairment of assets dedicated to the contract where required. A contract is onerous when unavoidable costs exceed expected economic benefits. Unavoidable cost is the lower of cost of fulfilling and compensation/penalties to exit. IAS 37's amended fulfilment-cost concept includes incremental costs plus allocation of other costs directly related to fulfilling contracts. Recognize the present obligation as a provision and update estimates each reporting period.

## US GAAP
Do not assume a general IAS 37-style onerous-contract model. US GAAP contains contract-type-specific loss guidance and contingency guidance. CAO must identify contract type first, retrieve applicable Topic, and only then conclude. This is a high-risk framework difference.

## UK GAAP
FRS 102 Section 21 contains onerous-contract requirements; use current Section 21 and period-appropriate amendments. FRC official material confirms paragraph 21.11A is relevant to onerous contracts. Do not import IAS 37 cost composition without verifying FRS 102 wording.

## Payroll-to-GL PRINCIPLES
Payroll accounting begins with a complete authorized payroll population and maps gross pay, employer taxes/contributions, employee deductions, benefits, bonuses/commissions, leave, equity-related cash items and net pay to appropriate expense/assets/liabilities. Payroll operations remain outside CAO remit; accounting completeness, classification, cut-off and reconciliation are in scope.

## CAO payroll workflow
1 obtain approved payroll register/control totals; 2 map employees/entities/cost centers/accounts; 3 separate gross compensation, employer burden and employee-withheld liabilities; 4 identify capitalization or intercompany allocations; 5 accrue earned/unprocessed items; 6 post payroll journal; 7 reconcile payroll register to GL, bank/net pay and statutory/payroll clearing balances; 8 investigate variances/stale balances; 9 certify close.

## Entries — generic
Dr compensation expense/eligible asset; Cr payroll liabilities/net-pay clearing. Employer charges: Dr expense/eligible asset; Cr payable. Payment: Dr liabilities; Cr cash. Exact accounts and capitalization require Company Context and relevant topic.

## Controls
Onerous: contract inventory trigger, forecast-to-contract reconciliation, impairment-before-provision check, legal/commercial review, estimate approval, rollforward. Payroll: HR/payroll population interface, payroll control-total approval, JE access/review, entity/cost-center mapping, payroll-to-GL reconciliation, bank/net-pay reconciliation, stale liability review, cut-off.

## Scenarios
Loss-making service contract: determine framework and contract-specific scope before provision. Cancellation penalty lower than fulfilment loss under IFRS: use least net exit-cost logic. Payroll register agrees net cash but GL gross wages differ: do not clear solely on net cash; reconcile every control component. Engineering payroll proposed for software capitalization: route eligibility to TOPIC-04-004, not payroll operations.

## QA
PASS. Explicitly prevents false cross-framework onerous-contract equivalence and keeps payroll operations outside accounting remit.
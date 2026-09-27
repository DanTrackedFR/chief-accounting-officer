# Accrual and prepaid schedules — estimate, reversal and true-up

Extends existing README/factory and preserves the alternate `accruals-prepayments` draft. Capabilities CAO-02-015–016. This is an operating method; item recognition follows the applicable framework/standard. Prepared 2026-09-27.

## Population and decision

Identify contract/service, entity, covered dates, price and terms, invoice/payment status, prior accrual, source evidence and subsequent settlement. Determine whether there is a present obligation or an asset for unconsumed future benefit under the relevant item-specific literature. Do not use generic “accrual accounting” to bypass provision, lease, employee benefit, revenue or inventory requirements. Rank estimates by materiality, uncertainty and data quality; record method, assumptions, alternatives, later information, reviewer and retrospective accuracy.

## Worked prepayment

Annual support starts 1 July and ends 30 June, invoice/payment 120,000. If benefits are provided uniformly and contract terms support an asset, monthly consumption is 120,000/12 = 10,000. At 31 December six months have elapsed: cumulative expense 60,000; remaining prepaid 60,000. Opening prepaid 120,000 less six monthly credits of 10,000 reconciles to 60,000. Source schedule must reconcile both the prepaid GL and expense postings; if termination rights or nonuniform service change the benefit pattern, reassess rather than impose straight-line by default.

## Worked estimate and true-up

December service usage from validated system log is 3,000 units at contractual 8 per unit, unbilled. Subject to the underlying expense/liability conclusion, accrue 24,000. If January invoice is 24,600 for December because 75 units were missing from the prior log, compare evidence available at December authorization/issuance and materiality: a revised estimate from new information may be prospective, while omission of available reliable data could be an error. Do not automatically force a 600 current-period expense; classify through TOPIC-02-009 and Domain 15. Reversal must have a matched January invoice or controlled carry-forward, not simply erase the obligation with no reconciliation.

Controls: complete contract/usage/invoice population; duplicate detection; period and service-date validation; rate/change authorization; estimate reasonableness and back-test; subledger/schedule-to-GL bridge; independent review; aging of stale accruals/prepaids. Audit evidence is the contract, usage log, calculation, policy memo when material, JE/reversal IDs and later settlement. For IFRS/AASB changes in estimates and prior errors, see [IAS 8 official overview](https://www.ifrs.org/issued-standards/list-of-standards/ias-8-basis-of-preparation-of-financial-statements/) and [AASB 108 version](https://standards.aasb.gov.au/aasb-108-mar-2021), checked 2026-09-27. FRS 102 Section 10 [official standard page](https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/) must be period-gated (principal PR2024 effective 2026). US ASC 250 exact paragraphs remain unverified from accessible Codification, so do not assert paragraph-specific treatment here.

**Failure injection:** accrued 24,000 reverses on 1 January but no AP invoice or carry-forward follows. Expected FAIL; re-establish liability if obligation persists and investigate the source-to-GL gap. Result PASS for route, subject to transaction-specific framework review.

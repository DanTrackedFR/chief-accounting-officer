# Credit-loss model review — 2026 source update and executed test

Capabilities: CAO-03-016/017. This is an additive correction to `factory.md`, not a replacement. Checked 2026-09-27 against official source pages listed below. Source texts are reference-only; explanations and numbers here are original.

## Framework and date gate

| Framework | Model for ordinary trade receivables | Date/source check | Consequence |
|---|---|---|---|
| IFRS | IFRS 9 lifetime ECL simplified approach for qualifying trade receivables/contract assets; assess significant financing component and policy choice separately | IFRS 9 mandatory from periods beginning 1 January 2018; [IFRS Foundation standard page](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/) and [IASB impairment project](https://www.ifrs.org/projects/completed-projects/2014/financial-instruments-impairment/) | Do not wait for an incurred loss event; adjust historical losses for current and forward-looking evidence. |
| AASB | AASB 9 paragraph 5.5.15; version must match period beginning date | [AASB February 2025 compilation](https://standards.aasb.gov.au/aasb-9-feb-2025) applies to periods beginning 1 January 2026 and before 1 July 2026; subsequent period requires version recheck | Similar simplified ECL principle but Australian period/entity overlay must be selected. |
| US GAAP | ASC 326 expected credit losses, not IFRS staging | [FASB ASU 2025-05](https://storage.fasb.org/ASU%202025-05.pdf) applies to annual periods beginning after 15 December 2025 and interim periods therein, prospectively if elected | For current Topic 606 receivables/contract assets, all entities may elect a specified forecasting expedient; non-public business entities electing it may also elect to consider eligible post-balance-sheet collections. These are elections, not a blanket exemption from credit-loss measurement. |
| UK GAAP | FRS 102 Section 11 basic-financial-instrument impairment; retain objective-evidence analysis, not an IFRS 9 matrix by default | [FRC FRS 102 register](https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/) shows Periodic Review 2024 principally effective 1 January 2026 | Verify the reporting-period edition and Section 11 basis before comparing to IFRS/US. Exact paragraph-by-paragraph 2026 impairment mapping is still open. |

US amendment nuance: the practical expedient assumes current conditions at balance-sheet date continue for the remaining asset life when constructing reasonable and supportable forecasts. The narrower non-PBE subsequent-collections policy is available only if that practical expedient is elected; document consistency across qualifying current receivables/contract assets, disclosure and prospective application. Do not apply either election to non-current loans, or treat an April receipt as automatic evidence that no year-end credit risk existed under other frameworks. The ASU exposes amended 326-20-30-10A–10H and transition 326-10-65-6; full current Codification cross-check remains necessary.

## Executed portfolio calculation

At 31 December, validated gross receivables are current 1,000, 1–30 days overdue 300, 31–60 100, 61–90 50, >90 50. Rates of 0.5%, 1%, 4%, 15%, 60% are *hypothetical and not policy defaults*. Portfolio result is 5 + 3 + 4 + 7.5 + 30 = 49.5. Suppose a specific 50 balance inside the >90 bucket is assessed individually at 80% loss. Remove its 30 pooled allowance before adding the individual 40: revised allowance 49.5 − 30 + 40 = 59.5. Do not count 40 and 30 on the same balance. If opening allowance is 45 with no intervening write-offs, recoveries or FX, Dr impairment expense 14.5 / Cr allowance 14.5. Gross AR 1,500 less 59.5 = 1,440.5 net.

**Test result:** 1,000+300+100+50+50=1,500; 49.5−30+40=59.5; 59.5−45=14.5; 1,500−59.5=1,440.5. PASS arithmetic only. The assumed rates and individual recovery estimate require evidence, segmentation and forward-looking challenge under expected-loss frameworks. Under FRS 102, this numeric result cannot be transplanted without objective-evidence analysis.

## Control and audit challenge

Retain balance-date AR extract and GL tie, due-date derivation, historical cohort rollforward and recoveries, forecasts, customer-specific insolvency evidence, collections through authorization date, model/election approvals, adjustment log and signed allowance bridge. Reperform aging from invoices and terms; test credits/disputes separately from inability to pay. Backtest prior estimates and keep explanations for changes. Cross-topic: TOPIC-03-007 commercial refunds, TOPIC-03-009 write-offs, TOPIC-03-011 AR reconciliation, TOPIC-06-010 broader instruments, TOPIC-08-005 subsequent events.

**Residual QA gate:** US primary amendment/effective date and AASB version verified as linked; current ASC paragraph bodies outside the ASU and precise UK Section 11 mapping not verified. Proposed PARTIAL pending those checks and evidence-based rate validation; do not promote solely because this arithmetic passes.

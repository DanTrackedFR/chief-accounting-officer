# Specialist Phase 2D completion log and self-review

Worker branch `worker/specialist`; date 2026-09-27. Scope: 41 canonical topics in Domains 04, 14, 15, 16 and 17. Canonical manifest statuses remain untouched. This report proposes statuses for independent QA, not promotion. The prior inventory was committed before substantive edits.

## Entry audit findings and retained work

| IDs | Existing content retained | Audit finding and action | Proposed status |
|---|---|---|---|
| 04-001, 04-002, 04-003, 04-004, 04-005, 04-006 | Substantive framework, practice, example and scenario READMEs/packs | Reviewed all canonical and retry folders. They already cover their capabilities with strong decision routes. Avoided wholesale rewrite. US current Codification bodies and some UK/Australian date or paragraph depth still require case-specific source review. | PARTIAL pending independent standards QA; prior in-file production-candidate claims not promoted by this report. |
| 04-007, 04-008, 04-009 | Three canonical lease READMEs already exist on branch | Manifest falsely records no artifact at its earlier snapshot. Verified each ID/capability pair and linked QA scenario references to 04-010; preserve shared-source design. | REVIEWED candidate for mapping correction, subject to QA of the 04-010 dependencies. |
| 04-010 | Reviewed 18-file Phase 2C Leases slice | Inspected source maps, framework files, methods, executed scenarios. No content changes. | Retain REVIEWED. |
| 04-011 | Existing sale-and-leaseback decision tree | Added `completion-qa.md` with period gates, four-framework differences, illustrative IFRS calculation, reconciliation and six scenarios. Variable-payment, US and unusual UK paragraph detail remain. | PARTIAL. |
| 14-001, 14-002, 14-003, 14-005, 14-006, 14-007, 14-008 | Existing research, comparison, memo, process, audit, executive and citation docs | All have capability-specific methods and scenario claims. 14-005 duplicate docs complement each other. No destructive or cosmetic rewrite; specific live-case evidence and independent QA remain. | PARTIAL pending independent QA; do not infer manifest promotion from in-file REVIEWED labels. |
| 14-004 | Existing `tests.md` with 10 classification/documentation scenarios | Manifest said NOT_STARTED despite QA artifact. Preserved tests and added missing canonical guide for three capabilities and source/evidence route. | REVIEWED candidate for document-method scope only; framework case conclusions remain conditional. |
| 15-001, 15-002 | Existing policy/estimate guides; 15-002 has duplicate complementary material | Substantive guidance retained. 15-002 coverage of CAO-15-004 is in the policy-inventory path and changes/CAO-15-007 are in the companion path, so both are necessary. | PARTIAL pending independent QA and canonicalization. |
| 15-006 | Existing classification engine | Preserved; added election supplement for previously missing CAO-15-014. | PARTIAL; election authority must be verified per case. |
| 15-003–005, 15-007–008 | None | Built separate topic guidance, four-framework routing, worked examples, evidence, controls and desk scenarios. Source limitations explicitly stated. | PARTIAL pending source/case QA. |
| 16-001–007 | None | Built seven jurisdictional reporting topics with entity applicability, filing calendar, structured reporting, controls, regulator query, capital and industry change routes. | PARTIAL; exact local forms, rules, deadlines and regulated-sector requirements are entity/period dependent. |
| 17-001–007 | None | Built seven sustainability topics with ISSB, Australian, UK, EU and SEC applicability gates and distinct data, controls, GHG, connectivity, assurance and systems examples. | PARTIAL; current local mandate/transposition, quantitative methods and assurance need a real entity case. |

## Duplicate/retry canonicalization proposal

- 04-001: keep `TOPIC-04-001-ppe-recognition-capitalization` as canonical and cross-reference `TOPIC-04-001-ppe-recognition` as a retained substantive alternate; do not delete either until integrator reconciles claim differences.
- 04-002: retain both depreciation paths; prefer `TOPIC-04-002-depreciation-disposals` as canonical and retain the other `factory.md` as source for consolidation.
- 04-005: prefer `TOPIC-04-005-intangible-assets`, retain `TOPIC-04-005-intangibles-amortization` pending claim-by-claim audit.
- 14-005: prefer `TOPIC-14-005-process-sop-control-documentation`, retain `TOPIC-14-005-process-sop-control-writing` as complementary instructions.
- 15-002: prefer `TOPIC-15-002-policy-inventory-estimate-methodology` for the canonical topic scope; retain the estimate-changes folder because it supplies CAO-15-007 material that belongs primarily with 15-003. Integration should create cross-links, not silently discard it.

## Batch ledger

### Batch A — 16-001–007

Capabilities: CAO-16-001–015. Changed seven new `README.md` files under `knowledge/topics/TOPIC-16-*`. No existing topic content replaced. Verified official SEC Inline XBRL, Companies House, ESMA ESEF, ASIC regulatory pointers on 2026-09-27. Filing forms, dates and regulator returns are conditional on entity and period. Desk scenarios: 14 decision cases in the seven files, with explicit failure conditions. Regression A: source link, unique capability and topic ID, filing basis versus GAAP separation checked for 7/7. Residual: legal form/rule paragraphs and sector-specific prudential rules require live-case evidence. Proposed PARTIAL for all seven.

### Batch B — 17-001–007

Capabilities: CAO-17-001–015. Changed seven new `README.md` files under `knowledge/topics/TOPIC-17-*`. No prior topic content replaced. Verified official IFRS S1/S2 effective 2024, AASB S2 effective 2025, ASIC first/second/third cohort 2025/2026/2027, UK SRS February 2026 voluntary publication, Commission CSRD amendment timeline and Directive (EU) 2026/470 (both EUR 450 million turnover and 1,000 employees for the core scope, subject to transition/local implementation), SEC proposed 2026 rescission versus current rule status. Desk scenarios: 14 distinct decision cases plus illustrative GHG calculation and financial-statement sensitivity. Regression B: 7/7 topics have applicability gate and source links; no universal IFRS S1 mandate claim. Residual: EU local transposition, US final/stay state, exact AASB cohort test and assurance scope per entity need refresh. Proposed PARTIAL.

### Batch C — 14-004 and 15-003–008

Capabilities: CAO-14-010–012; CAO-15-007–018, with CAO-15-014 in the supplement and pre-existing CAO-15-013 classification. Changed seven files: one 14-004 guide, five new 15 topic READMEs and one 15-006 supplement. Existing 14-004 scenario file and Domain-15 policy/estimate content preserved. Verified IFRS IAS 8/Practice Statement 2, FRS 102 Section 10 effective-period gate, AASB 108 compilation and FASB Codification portal limitation. Desk scenarios: 10 pre-existing 14-004 cases and 3 per new 15 topic, plus 3 election cases; calculation checks include 900k/3 versus 900k/5, 100k covenant materiality, 10m/10.5m impairment headroom. Regression C: capabilities, calculation arithmetic, source limitations and policy/estimate/error boundary checked. Residual: exact current US paragraph and topic-specific disclosure requirements. Proposed PARTIAL for new 15 topics and 15-006; 14-004 document method REVIEWED candidate.

### Batch D — 04-011 and existing Domain-04 audit

Capabilities: CAO-04-001–026, with 04-011 supplement addressing CAO-04-025/026. Changed one new 04-011 companion file; retained all substantive Domain-04 material. Verified official IFRS 16/AASB 2022-5 amendment effective 2024, FRC 2026 Periodic Review gate; US ASC access limitation. Six sale-and-leaseback desk scenarios, one intentionally PARTIAL on variable payments. Regression D: transfer-of-control precedes gain; IFRS illustration debits 1.24m and credits 1.24m; liability and ROU bridges independent. Residual: variable-payment subsequent measurement, exact US Codification and unusual UK fact patterns. Proposed PARTIAL for 04-011, no change to reviewed 04-010.

## Cross-topic regression and final self-review

- Inventory covers 41/41 canonical IDs; each has at least one branch artifact after work. Manifest 04-007–009 and 14-004 status/path drift explicitly flagged.
- Domain IDs and capabilities checked against manifest. Full literal capability scan returns one false positive on reviewed 04-010: its scope text says CAO-04-017 through CAO-04-024 instead of repeating CAO-04-023 individually; the actual lease-term method is present. No edit made.
- Scenario routes spot-checked: 04-011 sale test before measurement; 15-003 prospective estimate versus error; 15-005 qualitative covenant materiality; 16-003 machine-tag scale; 17-001 adoption versus mandate; 17-004 kWh-to-tCO2e units; 17-005 disclosure risk versus booked provision. 7/7 correct route in the authored files. These are desk checks, not production execution or independent QA.
- `git diff --check` passes. No change to forbidden manifest, progress, roadmap or Master Build Map. No deletion or modification of reviewed 04-010 or useful duplicate material.
- Full factory-level APPROVED status is not claimed. For regulatory and sustainability topics, precise paragraph and legal-entity scope cannot be generalized; for US GAAP, public Codification does not expose all current paragraph bodies. Source limitations and case-specific work remain explicit.

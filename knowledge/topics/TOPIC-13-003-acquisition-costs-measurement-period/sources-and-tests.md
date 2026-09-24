# TOPIC-13-003 — Sources, differences and executed QA

Source checked: 2026-09-24. Public repository posture is reference-only; no standards body text is reproduced as a substitute for licensed standards.

## Authoritative source register
- IFRS Foundation — IFRS 3 Business Combinations, official standard page and issued-standard material. Relevant architecture: measurement period 45–50; acquisition-related costs 53; subsequent contingent consideration 58 where boundary questions arise.
- FASB — ASC Topic 805 / current Business Combinations materials. Public source-depth limitation applies: complete current Codification paragraph bodies are not always exposed through the public route. Verify authorized Codification before paragraph-level APPROVED status.
- Financial Reporting Council — FRS 102 (2024 Edition), Section 19. Relevant current architecture includes 19.11(b) directly attributable combination costs and 19.19 provisional accounting; FRC confirms Section 19 remains based on IFRS 3 (2004).
- AASB — AASB 3 Business Combinations. Relevant architecture: paragraphs 45–50 measurement period and 53 acquisition-related costs; AASB 132/AASB 9 for debt/equity issuance costs.

## Difference assertions tested
1. IFRS/AASB acquisition-related professional costs are not automatically part of consideration/goodwill; financing issuance costs route separately. **PASS**.
2. UK FRS 102 directly attributable combination costs cannot be treated by copying current IFRS 3. **PASS**.
3. Measurement-period eligibility depends on acquisition-date facts, not simply elapsed time. **PASS**.
4. IFRS/AASB maximum period is one year; UK FRS 102 uses a twelve-month provisional-accounting mechanism. **PASS**.
5. Post-period correction routes to error guidance rather than indefinite goodwill true-up. **PASS**.
6. US GAAP is routed independently to ASC 805 and is not asserted paragraph-by-paragraph where the public authoritative body is unavailable. **PASS**.

## Executed scenarios
| # | Scenario | Expected CAO behavior | Result |
|---|---|---|---|
| 1 | IFRS acquisition: legal and valuation fees | Expense under IFRS 3 cost rule; reconcile to deal-cost population | PASS |
| 2 | IFRS acquisition: debt issuance fee | Route to financial-instrument/debt issuance accounting, not generic M&A expense | PASS |
| 3 | FRS 102 acquisition: directly attributable adviser fee | Include in combination cost where Section 19 criteria apply; do not import IFRS treatment | PASS |
| 4 | New valuation evidence 4 months after acquisition proves acquisition-date customer relationship value | Assess as measurement-period adjustment; update affected acquisition-date amounts/goodwill and consequential effects | PASS |
| 5 | Customer loss 4 months after acquisition caused by post-close service failure | Reject measurement-period treatment; route as post-acquisition event | PASS |
| 6 | IFRS valuation information arrives 14 months after acquisition | Measurement period closed; assess error/other subsequent accounting | PASS |
| 7 | FRS 102 provisional amount revisited after twelve months | Route to Section 10 material-error analysis rather than open-ended purchase accounting | PASS |
| 8 | Cost ledger contains employee retention payment | Route substance assessment to remuneration/separate transaction; do not classify from vendor/account label | PASS |
| 9 | Same adviser invoice appears in closing statement and AP expense population | Detect potential double count between consideration/cost population | PASS |
| 10 | US entity requests paragraph-level ASC 805 citation from public repo | Provide architecture, flag source-depth limitation, require authorized Codification verification before APPROVED citation | PASS |

**Executed QA: 10/10 PASS.**

## QA conclusion
Status remains REVIEWED / production-candidate. No topic blocker. Residual limitation is US paragraph-level source depth through the public FASB route; this is explicit and non-blocking for the factory.

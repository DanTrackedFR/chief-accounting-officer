# Batch 11 — Accounting systems and data gap closure

Prepared 2026-09-27. TOPIC-11-001–010; capabilities CAO-11-001–024. Existing READMEs and worker scenarios preserved. Ten targeted methods specify source-to-output proof, data/access change controls, numeric examples, exception handling and negative acceptance tests. These operational topics do not manufacture IFRS/US GAAP/UK GAAP/AASB standards treatment; accounting-sensitive mappings explicitly route to governing transaction/reporting topic and effective period. SEC 33-8810 (US issuer context) and voluntary NIST AI RMF were checked 2026-09-27 where cited.

| Topic | Worked case and failure gate | Proposed status |
|---|---|---|
| 11-001 / CAO-11-001–003 | Deposits 300,000 and deferred revenue 500,000 must remain distinguishable after 800,000 aggregation | Ready for independent REVIEWED assessment |
| 11-002 / CAO-11-004–006 | New entity's 200,000 invoices wrongly in parent book cannot be repaired by untraceable top-side label | Ready |
| 11-003 / CAO-11-007–009 | 1,000/500,000 source → 995/496,000 accepted + 5/4,000 rejects; 4,000 still unresolved | Ready |
| 11-004 / CAO-11-010–012 | 100/10,000 receipts → 98/9,800 accepted, two/200 absent; source and entity tests fail | Ready |
| 11-005 / CAO-11-013–014 | Legacy AR GL 480,000 versus subledger 500,000 requires item disposition before migration | Ready; technical receivable conclusion elsewhere |
| 11-006 / CAO-11-015–016 | Bot can change mapping and post 250,000; segregate config/deploy/run/review | Ready |
| 11-007 / CAO-11-017–018 | EUR 100,000 × 1.10 versus 1.01 creates USD 9,000 workbook error | Ready; planning example not financial translation conclusion |
| 11-008 / CAO-11-019–020 | Warehouse 504,000 − 8,000 test records = 496,000 GL; no GL plug | Ready |
| 11-009 / CAO-11-021–022 | 98% classification accuracy hides two material entity errors; prompt injection refused | Ready for decision-support governance; actual model validation live gate |
| 11-010 / CAO-11-023–024 | Matched incomplete 995/496,000 populations are false zero-difference pass | Ready |

Regression: ten methods present, mappings and arithmetic checked; all fail-stop tests require source/control evidence. No protected or other-worker file touched. Proposed readiness is worker assessment, not a live configuration audit or independent promotion.

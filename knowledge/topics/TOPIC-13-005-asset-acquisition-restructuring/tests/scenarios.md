# TOPIC-13-005 Scenario QA

Executed: 2026-09-24
Status: PASS — 10/10 expected routing

| # | Scenario | Expected CAO behavior | Result |
|---|---|---|---|
| 1 | Acquired asset group lacks a business | Apply asset-acquisition model; no default goodwill | PASS |
| 2 | Acquired set is a business | Route to TOPIC-13-001–003 | PASS |
| 3 | Planned layoffs before recognition trigger | No automatic restructuring liability | PASS |
| 4 | Present qualifying restructuring obligation | Measure/document applicable provision/liability | PASS |
| 5 | Retraining/new system in restructure budget | Exclude from IAS 37 restructuring provision absent other capitalization rule | PASS |
| 6 | Mixed transaction/integration costs | Cost-level classification by framework and nature | PASS |
| 7 | Asset-acquisition contingent consideration | Framework-specific analysis; no business-combination shortcut | PASS |
| 8 | Employee termination package | Invoke employee-benefit/termination guidance and evidence | PASS |
| 9 | Facility closure with lease exit | Invoke lease/impairment dependencies | PASS |
| 10 | Schedule does not reconcile to GL | Block case completion pending reconciliation/immaterial exception | PASS |

## QA observations
- Asset/business classification is a hard upstream gate.
- Restructuring is a separate obligation-recognition analysis, not part of purchase accounting merely because management planned it during the deal.
- US paragraph-level conclusions retain the repository-wide licensed-Codification caveat.
- Framework-specific transaction-cost and contingent-consideration mechanics must be resolved before production entries.

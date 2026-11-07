# Phase A diagnostic register

Baseline: main `97d0621331c6ad2a66b12ed09c0ec40c05c626b9`. Separate post-merge correction; original acceptance is not reopened.

Original `docs/acceptance/phase-a-revision4-bundle.zip` is absent (the directory is also absent). Original Pulse Restore uploads were not accessed. All reproductions are explicitly synthetic. See baseline-http.json and independently authored engineering-qa-baseline.json for actual authenticated HTTP and durable evidence.

| Finding | Classification / severity | Actual baseline / root cause | Expected correction / production path | Permanent tests / QA / disposition |
|---|---|---|---|---|
| PA-01 | Confirmed defect / Medium | Missing scope bypasses owner qualification; present malformed identity rejects without field requirements. Adapter checks only present equality; owner dispatch fails before source requirements. | Shared exact scope validation at adapter boundary; aggregate requirements with evaluable row defects; immutable identity preserved. Direct engine also reports structured needs. | test_phase_a_scope: 2 methods, 42 malformed-field variants + aggregate; PASS. Independent QA pending. |
| PA-06 | Confirmed contract correctness defect / High | Unspecified legacy years accepted as months produces plausible 12× understated charge: cost11,000, life24 ->458.33 vs intended5,500 annually. Explicit months currently ignored. | Explicit years unchanged; exact month representation and conflicts block; source execution + schema/docs. No historical rewriting. | Stage3 pending. |
| PA-03 | Confirmed diagnostic defect / Low | Zero/negative life maps to generic numeric error; missing/null/nonnumeric lack specific semantics. | Field-specific life diagnostics aggregated before accounting; no invalid row journals or automatic disposal. | Stage3 pending. |
| PA-02 | Contract enhancement + confirmed integration basis ambiguity / Medium | Actual days correctly follows legacy method; May annual2,400 ->203.84 vs monthly200. No supported election. | Explicit monthly/actual_days, preserve legacy no election; require partial-month policy, disclose basis and confirmation recommendation. | Stage4 pending; pre-implementation independent accounting decisions in accounting-qa-plan.md. |
| PA-04 | Requested comparison enhancement / Medium | Supplied NBV/accumulated fields ignored. No original260,000 error available. | Comparison-only opening/closing basis, independent balances/variance, no balancing journals. | Stage5 pending; synthetic260,000 mismatch required. |
| PA-05 | Confirmed API integration gap / Medium | Native proposed workpaper exists but only JSON inside guidance; empty journal_entry_implications by design. | First-class proposed_journals/applied_assumptions from native workpaper, curated lineage and provenance; retain legacy fields. | Stage6 pending. |

## Gate evidence

1. Diagnosis: all six independently reproduced (PA04 uses synthetic comparisons only); accounting contract reviewed before calculation changes. No standards mandate monthly; it is an operational recommendation.
2. Scope: `PYTHONPATH=skills:. python -m unittest hosted_cao.tests.test_phase_a_scope -q` — 2 PASS. HTTP422 identity_conflict names exact fields; source submission remains unstaged, existing Case can reopen; no accounting or proposals authorized.

Subsequent stages require their own executable evidence and independent integrated QA. No complete accounting release regression has run.

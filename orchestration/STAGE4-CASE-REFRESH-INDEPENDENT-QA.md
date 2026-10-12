# Stage 4 Case refresh intermediate independent review

**Intermediate compatibility review, not final Stage 4 QA.** This independently reviews documented unresolved snapshots versus actual version invalidation. Previous findings and QA history remain intact; IQA03 remains OPEN.

## CRIQA01 — unchanged documented partial snapshots spuriously reopened

**Substantive inherited finding, independently reproduced.** The checkpoint implementation of `CaseRegistry.refresh` unconditionally changes DOCUMENTED/CONCLUDED/CLOSED to IN_PROGRESS whenever unresolved required work exists. A DOCUMENTED partial accounting conclusion can truthfully retain current unresolved evidence; merely reading/refreshing it must not create a fresh rework event.

The reviewer loaded the exact `orchestration/cases.py` bytes using `git show e34121bdb68f23db815a580d666b52bc0ef02c98:orchestration/cases.py`, executed that module in memory, and invoked its original `CaseRegistry.refresh` against the separately built native Stage 3 conflict control. The Case had reached DOCUMENTED through actual SCOPED, IN_PROGRESS, CHALLENGE, CONCLUDED and DOCUMENTED transitions, retaining current material mismatch and partial outcome. No evidence, result, receipt, dependency or version changed. Output:

```text
BEFORE partial DOCUMENTED
INHERITED AFTER partial IN_PROGRESS REWORK
```

This proves the failure predates the new two-translated-side changes. The normal Group conflict acceptance test was independently rerun after remediation and passes (`test_group.py`, `test_primary_conflict_is_material_partial`, one distinct method). That actual integration test asserts partial/DOCUMENTED and public retention of 105 versus 100 conflict.

## Generic remediation and independent result

The implementation now reopens terminal/documented unresolved Cases when their exact current result-version references change or any represented result is STALE. Stable current unresolved snapshots retain their documented conclusion. It changes no fixture-specific status, closure requirement or material blocker; partial Cases still cannot close.

Permanent suite: `orchestration/tests/test_stage4_case_refresh_independent.py` — **six distinct methods PASS**. It independently proves:

- repeated refresh of unchanged current partial documentation preserves DOCUMENTED, versions, transitions and governance history;
- actual material stale result requires IN_PROGRESS/REWORK;
- replacement current result version requires IN_PROGRESS/REWORK;
- native legal producer replacement invalidates its genuinely dependent Group node and reopens Group documentation even when Group's own active result references remain unchanged;
- unrelated separately governed local execution leaves Group partial/DOCUMENTED and version references unchanged;
- partial documented evidence cannot transition to CLOSED even with documentation and observer prerequisites supplied.

The control uses native governed Stage 3 owners and reviewed residual evidence. It takes the Case through the existing transition method; it does not override Case status or closure assertions. Native source replacement is independently recertified, and stale/replacement attacks use the actual VersionedExecution lifecycle.

**CRIQA01 RESOLVED within this intermediate review; zero unresolved substantive Case-refresh findings.** No production edits were made by the reviewer. This does not constitute final architecture QA, full migration/regression, positive IQA03 acceptance, roadmap completion or exact-head CI readiness.

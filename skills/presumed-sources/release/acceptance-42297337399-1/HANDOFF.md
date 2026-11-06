# CAO Profile 1.2 — release evidence handoff

**CAO Profile 1.2 engine release acceptance: BLOCKED**

PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/49
Frozen tested source: `126c2f85ea37dc216bb8a732ed4394e4bfbc7e17`.
Final evidence commit is recorded in the final PR conversation handoff; all files here are evidence-only additions to that frozen source. Live main at publication preflight: `32d7c952658815312ce82f04a56ae7aaebe37d37`.

| Gate | Result |
| --- | --- |
| Genuine artifact retrieval / ZIP SHA-256 | PASS — artifact13545745955,1412552 bytes,296 members |
| Actual regression | PASS —3940 unique executed/passed,22 suites,0 failures/errors/skips |
| Required remediation methods | PASS —19+4+18+12+10=63 |
| Command reconciliation | PASS —22 suites,10 validators,whitespace; all33 exit0 |
| Frozen source/input/workflow identity | PASS —453 Python files,2722 execution inputs; canonical hashes match preflight |
| Historical preservation | PASS —8912 entries under pinned migration contract |
| Independent engineering/governance review | PASS —actual evidence and positive/negative verifier checks |
| New version-2 inventory / pointers | ISSUED after review; historical pointer unchanged |
| Profile1.2 verifier | PASS —3940/8912 |
| Build4 verifier | PASS —3940/8912 |
| Explicit local reviewed reuse | PASS —ACCEPTANCE_REUSED; not a GitHub run |
| GitHub explicit reviewed reuse | PENDING —owner manual dispatch required |
| Final-head GitHub CI | PENDING —not claimed green; see CI-RECOVERY.md |
| PR readiness | Draft; no Ready transition authorized until remaining gates pass |

Original regression: https://github.com/DanTrackedFR/chief-accounting-officer/actions/runs/42297337399, attempt1, workflow404963318. Overall failure is the deliberate acceptance-pending reporting gate; actual execution status is REGRESSION_COMPLETE_ACCEPTANCE_PENDING. No new GitHub run was started in this assignment.

Original artifact SHA-256: `4fc7d563b6e2d90d690afdfc68351cafc3da7d0c5c95c68f581ff521963e41b7`. Unchanged original ZIP and all individual digests are retained here. Manifest SHA-256: `6d6a8968713d935693e7220ba194268a8a6a80021010a9c15a12220627eaf8e1`. Version2 inventory SHA-256: `3aba57f04087743e019ffd682eb39ea8b843e41e389de9f3982e7636ff77beae`. Immutable pointer SHA-256: `f467f10c6da646432600e31657c795733dacbdc1b7e4eb046a2773e3365add5f`.

New inventory: `build4/release/presumed-sources-inventory-42297337399-1-v2.json`.
New immutable pointer: `build4/release/presumed-sources-accepted-42297337399-1-v2.json`.
New current pointer: `build4/release/presumed-sources-current-release.json`.
Actual manifest and sealed review: `build4/release/presumed-sources-attempt-ci-42297337399-1/`.
Local reuse: `build4/release/reviewed-local-reuse-42297337399-1/execution.json`.

Canonical source map digest: `80aebee2ba308dcacb47c2e447071d120198cde4958cb7c3e125a89608f74191`.
Canonical input map digest: `c5e66b68d83f178f2a2c44a244ca2730055f94a928304a47332ae0d73ecc791d`.
Workflow bytes: `06fd70ffb1802947a3a4ea240f2afa181e6ca5c77341c937553bb30adefaf558`.
Canonicalization is sorted compact UTF-8 JSON plus LF. Source equivalence requires exact regenerated map equality, not merely unchanged commit labels. The independently reviewed contract excludes these non-Python release-evidence additions from executable identities.

## Recovery instructions

1. Owner dispatches CAO presumed user-provided source assurance on feature/presumed-user-sources at the final published head, setting acceptance_pointer exactly to `build4/release/presumed-sources-accepted-42297337399-1-v2.json`. Never leave blank. Do not rerun the original run.
2. Continuation verifier retrieves new run/attempt evidence and confirms actual ACCEPTANCE_REUSED,release_accepted=true,successful workflow and correct head. No full regression.
3. Resolve applicable exact-head CI gates. The connector has no dispatch tool and local gh is unauthenticated. Orchestration manual dispatch runs broad regression; standards has no manual dispatch. Do not use Ready as a shortcut because PR-triggered Profile1.2 has blank input and starts fresh regression. See CI-RECOVERY.md for bounded paths and limitations.
4. Verify final-head map equivalence,mergeability,all mandatory CI and absence of unresolved blockers before Ready. Do not merge or deploy.

GitHub repository rulesets returned empty and main branch metadata reported protected=false. Branch-protection detail returned403 Resource not accessible by integration; no protected required-check set is invented. The owner's explicit exact-head CI/readiness requirement remains unsatisfied regardless.

Publication uses [skip ci] expressly to avoid automatically launching the prohibited full regression. No accounting/source/workflow development was restarted. Original TrackedFR upload retesting remains separately owned and pending. Synthetic hosted API acceptance is supported by existing executed evidence; original-upload integration and production deployment readiness are not established.

This is the final blocked handoff. Stop after publication; do not rerun full regression,merge,create PR or deploy.

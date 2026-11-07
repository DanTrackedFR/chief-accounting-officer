# Phase A corrections — final release preflight handoff

**CAO Phase A corrections — engine release acceptance: BLOCKED**

PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/54
Date: 7 November 2026. Release assignment stopped at its required preflight boundary. No full regression, workflow dispatch, release acceptance receipt, merge, deployment or replacement PR occurred.

## Frozen identity and implementation evidence

Frozen candidate: `ecf4bb8907b5a7a45e6f59bc3d129d6dbf69cd4c`.
Tree: `ff24a0b6362eeab796c9b49ea6be3a2f4f706fee`.
Current main at inspection: `97d0621331c6ad2a66b12ed09c0ec40c05c626b9`.
Published production: `f3f78debd750f1ca86c6e7edc7019a353c7c2b11`.
Published independent QA: `02767e0563acd965b26d16e79565a89f80ea8bfd`.

The final publication head is recorded in the final PR conversation handoff after this additive evidence commit. Its exact diff must contain only this checkpoint directory. No execution input or Python source may change.

Reviewed IMPLEMENTATION-HANDOFF, diagnostic register, accounting QA and logs, engineering QA and logs, integration contract, operational assessment, relevant source validation/fixed-assets/public output/fingerprint paths, release population/runner/verifier/receipt contracts and workflow. Published focused evidence records 371 unique passing methods, six schema validations and separate published-source accounting16/engineering32 rechecks. These results remain focused implementation evidence; this agent did not rerun or relabel them as full acceptance. Final production includes all six corrections, with the documented historical-lineage and context-only memory limits.

The eight paths changed after published independent QA are documentation/evidence only. Their intersection with the current458 Python-file and2729 execution-input inventories is empty. Independent reviewer verified this equivalence too. Full maps and workflow/verifier hashes are in frozen-candidate.json inside the evidence ZIP. This is byte-inventory equivalence, not a substitute for missing release execution.

## Actual mandatory discovery

Command: `CAO_SOURCES_ATTEMPT=phase-a-preflight-20261107 python skills/presumed-sources/run_release.py --discover`.

**3995 distinct discovered identifiers across22 suites;55 additions and zero removals from the actual accepted3940 inventory; no duplicates.** All55 Phase A methods occur in skills/tests and hosted_cao/tests. Complete identifiers, commands, environments and reconciliation are retained in the ZIP. These are discovered, not fully executed.

| Index | Suite | Pattern | Discovered |
|---|---|---|---:|
| 0 | orchestration/tests | test_*.py | 1377 |
| 1 | skills/tests | test_*.py | 1616 |
| 2 | skills/lease-accounting/tests | test_*.py | 17 |
| 3 | tests | test_*.py | 140 |
| 4 | knowledge/income-taxes | test*.py | 10 |
| 5 | knowledge/agriculture | test*.py | 83 |
| 6 | knowledge/insurance-contracts | test*.py | 35 |
| 7 | knowledge/derivatives-hedge | test*.py | 4 |
| 8 | knowledge/derivatives-hedge | independent_review_tests.py | 7 |
| 9 | knowledge/inventory-cost | test*.py | 262 |
| 10 | local_cao/tests | test_*.py | 55 |
| 11 | knowledge/borrowing-costs | test*.py | 16 |
| 12 | hosted_cao/tests | test_*.py | 127 |
| 13 | intelligence/tests | test_*.py | 72 |
| 14 | build4/tests | test_*.py | 60 |
| 15 | knowledge/government-grants | test_*.py | 39 |
| 16 | knowledge/investment-property | test_*.py | 12 |
| 17 | diagnostics/profile12 | regressions.py | 19 |
| 18 | diagnostics/profile12 | governance.py | 4 |
| 19 | diagnostics/profile12/remediation/accounting-qa | test_accounting_qa.py | 18 |
| 20 | diagnostics/profile12/remediation/engineering-qa | test_boundaries.py | 12 |
| 21 | diagnostics/profile12/remediation/engineering-qa | test_governance.py | 10 |

The current required-remediation-tests contract expressly guards63 historical identities, but no Phase A required-identity contract exists. Current discovery is complete; removal of a Phase A method would not trigger a specific missing-PhaseA gate. A successor must make the correction population mandatory without weakening historical coverage.

## Bounded actual entrypoint result

Command: `CAO_SOURCES_ATTEMPT=phase-a-preflight-20261107 python skills/presumed-sources/run_release.py --preflight`.

Exit1; `complete=false`, `source_unchanged=true`. Suite17 passed19, suite19 passed18, suite20 passed12: **49 methods actually passed**. Suite18 and suite21 both failed in setUpClass and ran zero methods, leaving14 methods unexecuted. Both failures arise from the real verifier rejecting `docs/HOSTED-CAO.md` against its frozen7146 preservation manifest. Disposable candidate clones and newly issued focused controls reproduce it; it is not an absent historical Git object or import failure.

The runner's `executed_distinct_tests=63` is a scheduled/discovered-identity count in this setup-failure case, not actual execution. Sidecars retain discovered IDs while unittest reports `Ran 0 tests`. It did fail closed (`complete=false`), but successor receipts must distinguish scheduled and executed identities and reject count inflation. Do not report63 passing tests.

All original outer logs, sidecars, traces, start maps and discovery are retained under their original relative paths within the ZIP. Historical evidence was not regenerated or edited by this release assignment.

## Proven blockers and versioned proof boundary

1. **Stale deterministic public proof selection.** Exact workflow commands `PYTHONHASHSEED=109 python -m hosted_cao.tests.prove_presumed_http` and seed971 both succeed and produce identical bytes, SHA256 `b973931977a198aced1c01ce2d3eb9013892a7f9c87114049e46714a488eef5d`. Historical immutable `skills/presumed-sources/release/http-proof.json` has SHA256 `be06ab1a1ee247bc24159f7ad605eb30c1dc70fccb13c864b50a9da25e88bcb7`. The workflow hardcodes cmp to that historical path, so it fails before regression. JSON diff is exactly two `executions/*/public_sha256` changes. Existing calculation/provenance/check/restart fields agree. Fresh independent reviewer recalculated fixture totals:27 asset costs11000 through37000 total648000 gross, annual ten-year charge64800; invoice amounts110 through200 total1550. These unchanged numbers do not themselves validate all six corrected behaviors. No successor proof was issued and no old proof was overwritten.
2. **Missing preservation migration.** The verifier pins the historical8912-file manifest and specially handles the earlier orchestration-workflow migration. The only additional mismatch is the authorized14-line Phase A addition to `docs/HOSTED-CAO.md`. The unchanged original file remains available in accepted Git history; the current release path provides no explicit new migration/selection contract for it. Do not rewrite the manifest or exempt the document silently.
3. **Coverage/receipt semantics.** Add explicit mandatory Phase A identities and ensure setup failures cannot be represented as actual executed identities. Preserve all historical suites and stale/tampered-evidence rejection. Current verifier rejects mismatched historical preservation normally and refuses optimized import under `-O`; neither behavior should be bypassed.

This is a coordinated proof-selection, historical-preservation and fail-closed coverage/receipt change, not a numerical golden-file refresh. Per the assignment's substantial-infrastructure boundary and failed-preflight stop rule, no release code was changed. A separate bounded infrastructure assignment is required before continuation. Exhaustive successor-proof inventory across all workflows and independent numerical challenges of any changed numerical output remain outstanding; the two changed digest fields are the confirmed minimal reproduction, not a claim that every other proof has been reviewed.

## Historical preservation

Independently enumerated accepted-main release/release-evidence/examples paths plus all diagnostics/profile12, skills/presumed-sources and skills/prepared-accounting paths: **7963 protected files, zero byte changes**, using actual Git blob hashes against accepted main. Full deterministic path/blob map is retained. This corroborates the handoff population; the older8912 manifest is a different contract and has the separately authorized workflow migration plus the uncovered documentation update. Do not conflate these populations.

PR49 receipts, workflows, maps, proofs and workpapers remain unchanged. New checkpoint evidence is additive, contains no production Python and does not amend any historical receipt.

## Independent review and GitHub readiness

Fresh delegated release reviewer independently inspected actual source and retained evidence; report and normal/optimized verifier subprocess records are in the ZIP. Conclusion: **preflight BLOCKED**, not final release acceptance. No genuine new GitHub regression artifacts exist to retrieve or certify; none were invented. No new release receipt or run ID/attempt exists.

At frozen head, GitHub returned no check runs, no combined status entries and no pull-request workflow runs. PR was open, mergeable=true, mergeable_state=clean and Ready for Review for implementation. Release readiness is blocked; draft status and final head/check observations are recorded in the final PR comment. No mandatory CI was bypassed. This publication uses `[skip ci]` to prevent known-invalid expensive automatic runs.

Authenticated dispatch and artifact round-trip were not exercised because proof/preservation preflight is invalid. Available GitHub connector exposes GET and rerun operations but no workflow-dispatch operation; local gh reports no authenticated hosts. The workflow file contains workflow_dispatch and run-unique artifact names, but dispatch registration/permissions and durable retrieval are unverified. Do not infer successful dispatch from YAML alone. Following infrastructure correction, use an authenticated Actions-capable path or the owner's manual Actions dispatch of the exact corrected branch, empty acceptance_pointer for a fresh regression; record actual run/attempt and perform the persistence probe and retrieval before acceptance.

## Exact bounded recovery instructions

1. Retain this candidate, evidence ZIP and all historical bytes; do not dispatch this known-invalid path or reuse PR49 acceptance.
2. In a separately authorized bounded infrastructure task on the existing PR54 branch, enumerate every changed deterministic proof/fixture; independently recalculate changes; create additive versioned successors and source/input-bound selection. Preserve historical proof bytes and compatibility checks. Reject missing/stale/mismatched/tampered successors.
3. Introduce an explicit reviewed preservation migration for the authorized HOSTED-CAO documentation update, archiving original bytes and retaining the8912 manifest plus earlier workflow-migration contract unchanged. Do not globally whitelist files or regenerate historical evidence.
4. Require the Phase A test identity population; repair scheduled/executed semantics and add meaningful setup-failure/tamper tests. Preserve all63 remediation methods and all compatibility suites.
5. Independently review the infrastructure changes, freeze the new source/input maps and actual test inventory, rerun actual bounded proof/runner/Build4-verifier/receipt/optimized/stale/tamper/preservation checks. No full regression until all preflight gates pass.
6. Then obtain authenticated dispatch, verify durable artifact round-trip, run one complete GitHub regression, retrieve and independently hash/inspect every artifact, issue a new reviewed source-bound receipt, obtain fresh independent acceptance, and complete exact-head CI/mergeability/readiness. Final release count may change with infrastructure tests; rediscover it.

Outstanding gates: safe successor-proof/preservation contract, complete successful preflight, authenticated dispatch and durable artifact round-trip, full corrected-source execution, new source-bound receipt, genuine artifact/digest review, final independent acceptance and exact-head green CI. No full run is active or overlapping.

## Integration boundary and stop

Synthetic HTTP proof is repeatable with unchanged existing numerical totals; this is not engine release acceptance, original TrackedFR-upload acceptance or deployment readiness. TrackedFR separately retests original files including Pulse Restore and confirms structured consumption under integration-contract.md. Issues51 provisioning,52 governed2027 support and53 aggregate200-row capacity remain out of scope and unchanged.

**CAO Phase A corrections — engine release acceptance: BLOCKED**.
Stop after final publication. Do not merge, deploy, create another PR or launch full regression.

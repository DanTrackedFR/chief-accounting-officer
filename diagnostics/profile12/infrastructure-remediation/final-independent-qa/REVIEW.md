# Independent engineering/governance review — infrastructure correction

**PASS for the bounded infrastructure assignment. This is not full accounting release acceptance.**

Reviewer: separately delegated `/root/final_review`, with no production implementation ownership. Date: 6 November 2026.
Baseline reproduced: `bc6c2055882718e9aa2d2fb9848ac9a224ea2f64`.
Final executed candidate: `8e9062b727dec3e0d8ce140e5335ec1b737d3fdf`.
Published equivalent candidate: `5714b47ebeab7e5bb7f1ed9116f5d9f54bbaf49b`.
Independent fetch and `git rev-parse FETCH_HEAD^{tree} HEAD^{tree}` returned identical tree `2ee54c89afe6d3ccf89d4f1cc30a4c76e954e3a9`. Tests and governance clones used the local executed candidate SHA; the published SHA is not misrepresented as the subprocess checkout identity.

## Original failures independently reproduced

A disposable baseline checkout discovered 3,862 configured distinct IDs and 63 omitted distinct IDs, with zero identity overlap. Actual `python -m build4.verify_release` exited 1 selecting the historical pointer and rejecting its absent version-2 inventory. The unchanged real preservation verifier returned 8912.

Separately, a disposable historical checkout at `36acb611142bc8bedd214622f1ecac539c290056` ran actual `python -m build4.verify_release`: exit 0, PASS, 3,844 tests, 8,912 historical files. This verifies the original receipt for its original source without executing regression or modifying evidence.

## Production correction and coverage assessment

Reviewed the complete baseline-to-candidate diff. Changes are limited to release infrastructure, workflow configuration, test fixtures/tests, and evidence/documentation. No accounting calculations or production business logic changed. Historical compatibility routes remain present; optimized Python refuses before assertion-dependent verification, including `-O` and `-OO`.

All five omitted suites are mandatory, with the original 63 IDs required by the production coverage contract. Governance still uses disposable clones of the exact committed candidate, explicit focused positive controls, and distinct attempt-local trace paths. Diagnostic fixture inputs are included in the full release identity. The runner rejects dirty tracked changes and any untracked/ignored execution input before dispatch, avoiding mixed main-process/clone source identities. This tightening followed an independent review challenge during implementation.

COVERAGE-DECISION.md is accepted: semantic overlap is intentional testing of different variants/entrypoints, not duplicate identities. All63 remain enforced; no exclusion is required. The nested19-method governance positive controls are not counted again. Running independently authored historical QA in CI is automated regression enforcement, not a fresh independent review.

Final production discovery: **3,940 distinct identifiers across22 suites** = original3,862 +63 previously omitted +15 new infrastructure methods. The15 are8 Build4 selection methods,3 population-enforcement methods,4 dispatch methods. No identifier duplicates or aliases inflated this total. The17 original slots now contain3,877 methods; the5 mandatory remediation slots contain63. Ten validators remain required. Discovery is not a passing full-regression count.

## Actual execution and combined proof

The actual workflow command was extracted from `Verify complete mandatory release discovery` and executed without alteration:

```sh
CAO_SOURCES_ATTEMPT=independent-preflight-002 python skills/presumed-sources/run_release.py --discover
CAO_SOURCES_ATTEMPT=independent-preflight-002 python skills/presumed-sources/run_release.py --preflight
python -m unittest discover -s tests -p test_presumed_build4_selection.py -v
python -m unittest discover -s tests -p test_presumed_population_dispatch.py -v
python -m unittest discover -s tests -p test_presumed_ci_evidence.py -v
python -m unittest discover -s tests -p test_presumed_release.py -v
```

All commands exited0. Discovery enumerated3940, including every required identifier and production command/environment assignment. Bounded preflight used the same production dispatch and `build4.run_release suite` entrypoint for all five remediation slots:19+4+18+12+10=63 passed, no skips/errors/failures; source/input identity unchanged. It produced only `bounded-preflight.json`, never a full release receipt.

The8 actual Build4 subprocess tests passed matching explicit/default receipts, environment selection, restart/repeated verification, missing/malformed/stale/historical receipts, conflicting selection, redirected pointers, changed source, receipt/sidecar tampering, and normal/optimized refusal. Their temporary fixtures execute80 trivial canaries through real production algorithms and retain all63 required identities. Only fixture test bodies and the explicitly synthetic historical preservation contract differ. These are not genuine CAO regression receipts and are never published as such.

The actual workflow-dispatch test passed initial/retry/separate-run command execution, preserving previous outputs and historical bytes. Full execution-controller routing now delegates to Build4 so receipt identity selection agrees. Fresh execution remains acceptance-pending; no successful regression automatically issues acceptance. All23 population/historical enforcement methods passed, including omission of each remediation slot and mandatory environment/plan checks. All4 discovery/dispatch methods passed. Total99 distinct focused methods executed (63+8+4+1+23); earlier repeated execution on `c4a91a7` is retained but not added again.

Independent additional real-entrypoint mutations in a disposable candidate clone:

* Rename required ENG-01 method: actual `--discover` exits1 with missing mandatory coverage.
* Alter workflow execution input: actual `--preflight` exits1 before output creation.
* Add ignored Python input: actual `--preflight` exits1 before output creation.

These three command-level challenges and exact outputs are retained separately. No omission or failed mandatory gate can be converted into green acceptance by the corrected verifier.

## Preservation and evidence

Final actual `verify_historical()` returned8912. All protected entries remain byte-identical under the unchanged manifest and authorized migration, including archived original workflow and pinned successor. No protected historical file, receipt, pointer, archive or migration record was changed. The candidate checkout had only new untracked preflight output directories after checks; no tracked source changed.

`bounded-preflight-evidence.tar.gz` preserves the complete final bounded attempt directory (including all actual command/suite logs, sidecars, source/input maps and diagnostic traces). It is an archival copy, not a relocatable acceptance pointer. `file-hashes.json` binds this review and retained evidence. Baseline and final discovered identifiers are complete. Earlier candidate c4a evidence is clearly separate from final8e evidence; final files are `candidate2-discovery.json`, `combined-preflight2.log`, `build4-tests2.log` and the bounded archive.

No unresolved infrastructure finding remains in this reviewed scope. Full accounting regression, independent review/issuance of a genuine new full receipt, downstream exact-head acceptance and readiness remain for the next release assignment. No full accounting regression, final release receipt, merge, deployment or readiness transition was performed by this reviewer.

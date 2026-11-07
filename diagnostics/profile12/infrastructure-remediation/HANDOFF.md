# Profile 1.2 release infrastructure remediation

PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/49

Production correction published as `5714b47ebeab7e5bb7f1ed9116f5d9f54bbaf49b`. Tested local candidate `8e9062b727dec3e0d8ce140e5335ec1b737d3fdf` has the identical Git tree `2ee54c89afe6d3ccf89d4f1cc30a4c76e954e3a9`. API publication was used because CLI push lacked credentials. Subsequent commits add evidence only. No accounting calculation/business logic changed.

## Corrections

The prior runner derived 17 suites from a historical receipt and the verifier enforced those same slots, excluding five diagnostic/QA files. Production release_population.py now defines22 mandatory slots shared by runner/verifier, pins all63 required remediation identifiers, records gate commands/environments, and binds diagnostic fixtures. Missing methods, duplicate identities, empty/import-failed suites and omitted gates fail closed. Governance clones use the committed source and all tracked changes/untracked execution inputs are rejected before dispatch. Outputs are attempt-specific. All63 are required; COVERAGE-DECISION.md explains overlap and independent-authorship limits.

Build4 previously selected the historical presumed-sources-accepted-release.json merely because it existed. It now accepts --pointer or CAO_ACCEPTANCE_POINTER, rejecting conflict, or selects the new presumed-sources-current-release.json. Missing/stale/malformed evidence fails without historical fallback. Workflow explicit reuse calls this same Build4 verification route; complete version2 inventory, source/input identity, discovery, sidecar/log and historical checks remain mandatory. -O/-OO refuse before assertions can disappear. Historical receipts and protected workflow migration remain unchanged.

## Population and bounded results

Production discovery: **3940 distinct methods,22 suites,10 validators** configured. This is NOT a passing full-regression count. Original3862 + omitted63 +15 infrastructure tests; root test suite125→140. No other original suite count changed. Full distinct IDs and gate assignment are in correction-evidence/discovery-after.json; baseline/discovery.json preserves the original3862+63 inventory.

The actual production bounded path executed the five remediation slots:19 runtime,4 original governance,18 accounting QA,12 engineering boundary,10 governance QA =63 distinct passing methods, no failure/error/skip, unchanged source. Nested positive controls do not inflate this total. The raw bounded artifact is archived separately and is NOT a final release receipt.

Commands (from repository root, committed checkout):

```sh
python skills/presumed-sources/run_release.py --discover
CAO_SOURCES_ATTEMPT=infra-bounded-8e9062b-1 python skills/presumed-sources/run_release.py --preflight
python -m unittest discover -s tests -p test_presumed_population_dispatch.py -v
python -m unittest discover -s tests -p test_presumed_build4_selection.py -v
python -m unittest discover -s tests -p test_presumed_release.py -v
python -m unittest discover -s tests -p test_presumed_ci_evidence.py -v
python -m unittest discover -s tests -p 'test_presumed_runner_*.py' -v
```

The workflow now invokes the exact --discover command before release execution/reuse. Bounded preflight uses the same gate plan and build4.run_release suite dispatcher as full execution, selecting only the five remediation slots. Synthetic receipt tests execute80 trivial fixture methods through production algorithms (17 base canaries +63 required identities); their evidence cannot be treated as accounting acceptance. Actual Build4 subprocess cases accept matching explicit/environment/current pointers, reject missing/stale/mismatched/tampered receipt and sidecars, and verify deterministic restart and -O/-OO refusal. Historical source36acb611 still passes its actual Build4 verifier3844/8912.

Independent final reviewer /root/final_review separately reproduced both original failures and exercised production discovery, real63 preflight, workflow commands, negative coverage/source inputs, actual Build4 verifier and preservation in disposable checkouts. Its report supplies final commands, tested identities and conclusion. Implementation-worker tests are not claimed as independent QA.

## Preservation and next release

All8912 protected entries verified by the unchanged preservation contract, including the authorized archived workflow mapping. No historical receipt, pointer, log, manifest, migration record or accounting proof was regenerated, overwritten or relabelled.

Next release agent: verify this checkpoint and independent report, freeze source/input/workflow identities, then under a SEPARATE release assignment dispatch `.github/workflows/cao-presumed-sources.yml` on `feature/presumed-user-sources` with acceptance_pointer empty. This launches the full regression and was NOT done here. Fresh execution remains REGRESSION_COMPLETE_ACCEPTANCE_PENDING until independent receipt review and new version2 inventory issuance.

After genuine full execution, independently review artifacts and issue a fresh immutable inventory/pointer. For unchanged downstream workflows, create the NEW `build4/release/presumed-sources-current-release.json` only after that review; never overwrite the historical presumed-sources-accepted-release.json. Verify with:

```sh
python -m build4.verify_release --pointer build4/release/<new-reviewed-pointer>.json
python skills/presumed-sources/verify_release.py --pointer build4/release/<new-reviewed-pointer>.json
```

Explicit workflow reuse must name the same reviewed pointer and use a new run/attempt. Invalid evidence must not be bypassed. Do not count repeated fixture or governance positive controls as additional distinct release tests. Final full regression, artifact acceptance, exact-head CI and release readiness remain future work, not infrastructure-remediation acceptance.

PR remains Draft and unmerged. No full accounting regression, final release receipt, Ready transition, merge or deployment. Stop after publishing the final evidence checkpoint.

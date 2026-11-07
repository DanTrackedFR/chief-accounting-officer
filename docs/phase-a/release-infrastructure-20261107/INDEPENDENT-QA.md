# Independent Phase A release infrastructure and governance QA

Final reviewed conclusion: **PASS for the bounded infrastructure remediation at corrected reviewed commit `529e768004e199c3a4d553060a7c0521fa50d4b3`**, tree `d70734be13e7b8e4808d40dc20f3541735ca31b9`, after the additional standalone-CLI defect below was independently reproduced and resolved. Initial QA reviewed1114eb9 and its source-equivalent publication01469d3; the subsequent production preflight exposed an untested standalone execution path. This is independent infrastructure QA, not Phase A engine release acceptance. The production complete bounded preflight remains the release implementer's next gate; I did not execute that entrypoint or a full accounting regression.

Reviewer: fresh delegated `independent_infra_qa` agent, separate from implementation. Production code was read only. Execution and mutations took place in disposable clones; no GitHub changes, workflow dispatches, merges, deployments or acceptance receipts were issued. Two newly issued receipts are explicitly focused19 diagnostic QA receipts with `release_accepted=false`.

## Reviewed source and finding

Initial review was against `bf5a5a626f6a08458ba59c8b0313b4745c45d07d`. I inspected its actual changed source, proof and migration contracts, mandatory identity population, historical receipts, workflow selection and actual callback-based runner/verifier flow. I independently found one release-verifier defect:

**QA-F01: discovered receipt count was unchecked.** The initial semantic verifier accepted both a missing `discovered_distinct_tests` field and `-999`, with other receipt rows unchanged. This would permit misleading discovery reporting in otherwise self-consistent rehashed evidence. Reproduction is retained as `finding-discovered-count-unchecked.json`; the initial `independent_controls.py` intentionally demonstrates the failure.

The implementation corrected this at `1114eb9f4b78913be8f2695bc38c8413843ca49c`. The verifier now requires an integer discovery count equal to aggregate discovered and scheduled populations, and the final verifier compares that count to actual rediscovery. I reviewed the diff and independently reran missing, negative, boolean and string count controls; all reject. The corrected permanent test includes missing/tampered count cases. No unresolved blocking finding remains.

The final source also rejects accounting-source population additions and non-Python execution-input population/content additions rather than only checking an existing map's entries. I independently added `orchestration/reviewer_unexpected.py` and `interfaces/reviewer_unexpected.json`; both reject.

## INF-01 proof selection and numerical expectations

I independently executed the actual HTTP proof under `PYTHONHASHSEED=109` and `971` in the candidate. Both outputs are byte-identical to the additive `skills/presumed-sources/release/phase-a-v1/http-proof.json`, SHA256 `b973931977a198aced1c01ce2d3eb9013892a7f9c87114049e46714a488eef5d`. Explicit `phase-a-v1` selection passes. Wrong version, missing successor, stale historical bytes substituted as successor, tampered successor, source mutation and execution-input mutation reject. The pinned contract and fixed workflow selector provide explicit version selection rather than existence-based fallback.

I independently executed both seeds in the actual accepted-main historical checkout `97d0621331c6ad2a66b12ed09c0ec40c05c626b9`. Both reproduce the original proof SHA256 `be06ab1a1ee247bc24159f7ad605eb30c1dc70fccb13c864b50a9da25e88bcb7`. The original proof file remains unchanged. The old proof is preserved as historical evidence and rejected as the corrected successor.

The proof JSON's differences remain exactly two public digest fields. Independent public-result comparison identifies seven actual public paths: the three added arrays `applied_assumptions`, `balance_comparisons`, `proposed_journals` for each of fixed assets and accounts payable, plus fixed-assets guidance. These align with the authorized structured-result/assumption disclosure integration; existing calculation values do not diverge.

I independently recalculated 27 costs `10000+i*1000`, i=1..27: closing cost648000 and annual ten-year depreciation64800. The ten invoice amounts `100+i*10`, i=1..10, sum1550. I separately checked every new proposal:27 asset journals with exact row depreciation,10 payable journals with exact row invoice amounts, each balanced Dr/Cr, EUR, PROPOSED. Debit totals are64800.00 and1550.00. Both balance-comparison arrays are empty for these fixtures. These checks do not certify original TrackedFR uploads or all six accounting corrections afresh.

Evidence: `proof-seed109.json`, `proof-seed971.json`, `proof-selector.json`, `proof-*.json`, `historical-original-seed109.json`, `historical-original-seed971.json`, `independent-public-current.json`, `independent-public-arithmetic.json`, and `recheck-summary.json`.

## INF-02 historical preservation specificity

The frozen8912-file manifest bytes and digest remain unchanged. I independently read all8912 original Git blob objects from its7146 baseline and checked SHA256 against every original manifest entry. In the active candidate, exactly two entries differ: the already governed orchestration workflow and `docs/HOSTED-CAO.md`. The documentation successor is the original bytes plus exactly14 lines, tied to exact predecessor/successor hashes. The new migration does not alter the original manifest or create a general documentation exemption.

The actual final historical verifier passes8912 entries with both explicit migrations. Missing/tampered migration, wrong archived document bytes, an extra future document mutation, unrelated historical-proof mutation and prior workflow successor mutation all reject in independent subprocesses. `-O` and `-OO` refuse mandatory verification before accepting even an otherwise valid focused receipt.

For the separate accepted-main7963 population, I independently checked the original blob map and every active file.7959 files are unchanged in place. Four authorized release-infrastructure sources have exact archived predecessor bytes and exact successor hashes. I checked every archived predecessor's Git blob identity against accepted main. No original accounting evidence, receipt, workpaper or proof was replaced. These four source migrations are explicit; they must not be described as7963 unchanged active files.

Evidence: `independent-preservation-audit.json`, `historical-positive.json`, `migration-*.json`, `doc-future-change.json`, `old-doc-tamper.json`, `unrelated-history-mutation.json`, `previous-workflow-migration-mutation.json`, `optimized-*.json`, `final-extra-controls.json`.

## INF-03 mandatory identities and actual execution

I independently confirmed the pinned55 Phase A identity contract and preserved63 historical remediation identities. The union contains118 mandatory identities. Separate removal of an actual Phase A method and historical method rejects; duplicates reject. These controls do not rely on a hardcoded overall3995 count.

The runner now retains discovered/scheduled IDs separately from observed executed/passed/failed/errored/skipped/unexecuted IDs. The `ObservedResult` callbacks distinguish class setup errors from individual methods. I inspected callback handling, subtests, skip rejection, aggregates and receipt validation; authored15 infrastructure methods pass on both initial and corrected candidates. Additional semantic tests deliberately use simulated rows and are not represented as executed accounting evidence.

I independently recreated the real original preservation setup failure, not only a synthetic49/14 mock: in a disposable clone I appended an unauthorized line to the protected document, committed that negative fixture, and invoked only production remediation slots17..21 through the new `suite_runner.py` with the exact production environment/ref plan. The resulting callback data reports **63 scheduled;49 executed;49 passed;14 unexecuted;2 class setup errors**. Both failed governance suites report zero executed methods. Successful receipt validation rejects their outcomes. No full regression entrypoint or production `--preflight` was invoked.

I also issued and verified a genuine19-method focused diagnostic receipt in the disposable candidate. Independent deletion of its sidecar, truncated sidecar, changed outer log and changed source reject. After switching to corrected source, the old focused receipt rejects as stale source; a newly executed19-method focused receipt passes. Missing/tampered aggregate discovery reporting now rejects. Existing version2 inventory verification still binds all sidecars/logs/maps and rejects absent evidence. Current-source verification does not silently reuse the historical full acceptance pointer.

Evidence: `real-negative-setup.json` (all five commands, environments, raw outputs and actual outcomes), `negative-setup-outer.log`, `receipt-*.json`, `fixed-rejects-old-source-focused-receipt.json`, `fixed-new-focused-issue.json`, `fixed-new-focused-positive.json`, `fixed-discovery-count-negative.json`, `fixed-authored-infrastructure.json`, `final-extra-controls.json`.

## Reproducible commands and evidence boundaries

Exact command arrays, environments, working directories, exit codes and captured outputs are retained in the JSON control records. Main independent drivers are `independent_controls.py`, `negative_setup_control.py` and `recheck.py`. `independent_controls.py` documents the original discovered-count failure and therefore intentionally is not an all-green replay against the corrected source. `recheck.py` is the subsequent affected-control replay against corrected commit1114eb9. Temporary clones and focused receipt directories are execution workspaces, not new historical accounting acceptance evidence.

Representative bounded commands:

- `python -m unittest discover -s tests/phase_a_release_infra -v`
- `PYTHONHASHSEED=109 python -m hosted_cao.tests.prove_presumed_http` and seed971
- `python skills/presumed-sources/proof_selection.py --version phase-a-v1 --output skills/presumed-sources/release/phase-a-v1/http-proof.json`
- `python diagnostics/profile12/remediation/issue_focused_receipt.py independent-reviewer-final`
- `python skills/presumed-sources/verify_release.py --focused diagnostics/profile12/remediation/independent-reviewer-final-pointer.json`
- `python -O skills/presumed-sources/verify_release.py --focused diagnostics/profile12/remediation/independent-reviewer-final-pointer.json` (expected nonzero)
- The five exact `suite_runner.py` commands and production environments are retained in `real-negative-setup.json`.

Final conclusion: **Independent infrastructure/governance QA PASS at corrected reviewed tree, with QA-F01 remediated and independently rechecked.** Remaining gates belong to the parent assignment: publish source-equivalent reachable commit, run complete bounded production preflight, retain actual counts/artifacts, and then hand off to a separately authorized full release execution agent. No claim is made about full regression execution, new full acceptance receipts, GitHub dispatch permissions, workflow artifact round-trip or final engine acceptance.

## Published-source equivalence and historical receipt addendum

I independently fetched GitHub Git commit metadata for `01469d335e024d8c39e4232b2cda9638b901bf67`. Its parent is the expected previous PR head82ac4007 and its tree is `16c44e4f91496a8c97ced57f5004c8f9f65551f7`, exactly the independently reviewed1114eb9 tree. The commit identity differs because publication used the Git-data API; all tracked bytes and paths are identical. My QA PASS therefore applies to this genuine published source tree as well. Record: `published-source-equivalence.json`. I did not mutate or interrupt the parent's running bounded preflight.

I additionally ran the historical checkout's original `python build4/verify_release.py` against accepted-main source97d0621. It returned `{"distinct_tests":3940,"historical_files":8912,"status":"PASS"}` by read-only verification, without executing the full regression. Raw output is retained in `historical-original-receipt-verifier.log`. Thus the historical receipt remains verifiable under its original source, while corrected-source execution still requires its own subsequent release evidence.

## QA-F02: production standalone selector import — reproduced and resolved

The parent's actual production bounded preflight at01469d3 executed all78 scheduled methods successfully with zero unexecuted methods and unchanged source, but correctly remained incomplete because its direct proof-selector CLI calls failed importing `build4`. This was a real infrastructure failure, not a passing preflight. Prior final-tree QA reran imported selector paths but missed a positive standalone invocation after the input-population hardening introduced the new import. The earlier independent PASS did not establish standalone CLI readiness; this addendum corrects that limitation.

I independently reproduced the failure in my reviewed1114eb9/01469d3-equivalent checkout with `PYTHONPATH` removed. Exact command: `env -u PYTHONPATH python skills/presumed-sources/proof_selection.py --version phase-a-v1 --output skills/presumed-sources/release/phase-a-v1/http-proof.json`. Exit1, `ModuleNotFoundError: No module named 'build4'`; raw evidence `QA-F02-cli-reproduction.log`. The script directory was on `sys.path`, but the repository root was absent.

I reviewed the complete narrow correction at `b1fe2bbaedb09fd3a693db534f4ffe2e506ad65f`, tree `2459707c2ce79af08fbb07039199676f9718e768`: add `import sys` and explicit repository-root path initialization to the selector, plus a permanent subprocess test which removes `PYTHONPATH`. Four archived-source successor contracts, numerical proof bytes and static migration contracts did not change.

In a disposable checkout of that exact correction, I independently executed16 permanent infrastructure methods under a clean environment; all pass. I freshly generated actual HTTP proofs under109/971, verified identical bytes and unchanged successor SHA256b9739319..., and called the standalone selector against each generated output under normal Python, `-O` and `-OO` with `PYTHONPATH` absent. All six positive CLI checks pass; wrong-version CLI rejects. Mandatory receipt/historical verifier still refuses `-O` and `-OO`. `QA-F02-resolution.json` retains12 exact command/output records and `QA-F02-resolution-outer.log` confirms completion. No full regression/preflight entrypoint was run by this reviewer.

I separately ran discovery only againstb1fe2bba: **4011 distinct identities across23 suites**, zero execution. Complete inventory: `QA-F02-discovery.json`. The new production bounded population should be independently counted by its next actual run (63 historical remediation plus16 infrastructure methods), not inferred as a release result from this inventory.

**QA-F02 status: RESOLVED; independent narrow correction recheck PASS.** The parent must rerun the complete production bounded preflight against the genuine published corrected source. The failed01469d3 preflight remains failed and preserved; it must not be reclassified. Final engine release acceptance, full regression, receipt issuance and GitHub acceptance remain outside this QA conclusion.

## Final receipt-type hardening recheck

After the standalone correction, the parent additionally hardened QA-F01 receipt semantics: every aggregate outcome counter must be a true integer, and full-receipt `complete`/`source_unchanged` must be the booleanTrue. This closes Python equality/truthiness cases such asFalse equaling0 or integer1 being truthy.

I reviewed the exact final local commit `529e768004e199c3a4d553060a7c0521fa50d4b3`, tree `d70734be13e7b8e4808d40dc20f3541735ca31b9`. The diff is narrow: strict aggregate-counter types, strict completion booleans, four permanent False-zero negative cases in the existing method, and corresponding exact successor/proof-input hash refreshes. Historical manifests, archived originals, original proof bytes, successor proof bytes and documentation migration bytes are unchanged.

Independent `final_type_controls.py` completed **29 records**, retained in `final-receipt-type-controls.json`: each failed/errored/skipped/unexecuted zero counter rejectsFalse,0.0,"0" andnull; ten deliberately invalid negative-receipt completion cases reject specifically at the completion guard before inventory validation (no passing synthetic full receipt is produced); all16 permanent methods pass under a cleanPYTHONPATH environment; final historical verification passes8912; the final standalone selector passes against the unchanged proof with its refreshed contract pin.

**Final local reviewed candidate:529e7680, independent infrastructure/governance QA PASS.** Full production bounded preflight must still be rerun on the source-equivalent genuinely published commit. Neither the prior failed preflight nor this independent narrow recheck is full engine release acceptance.

## Final published-source equivalence

I independently fetched GitHub Git commit metadata for final published source `7e14f99008cd4f30ec0200e17441264b5df2a4fc` using the connected GitHub API. Its parent is01469d3 and tree is `d70734be13e7b8e4808d40dc20f3541735ca31b9`, exactly the final independently reviewed529e768 tree. This confirms all tracked paths and bytes are identical to the reviewed correction. Evidence: `final-published-source-equivalence.json`.

**Final independent infrastructure/governance QA conclusion: PASS for published source7e14f990/tree d70734be. QA-F01 andQA-F02 are resolved and independently rechecked.** The parent is responsible for the actual final bounded preflight replay and its observed results; I did not execute or interrupt it. No full regression, engine acceptance, deployment or merge is claimed.

## Final production bounded-preflight evidence review — PASS

I independently inspected the completed actual production evidence at `build4/release/phase-a-infra-bounded-final-20261107/` **read only, without rerunning any test or verifier**. Source is `7e14f99008cd4f30ec0200e17441264b5df2a4fc`; manifest SHA256 is `aa517471ad066edec5252c7cf9cedb8df0cd7bae9c4cbcbbe8e6349c6624ff4d`. The scope remains bounded remediation preflight, `release_accepted=false`, `full_accounting_regression_executed=false`.

Recomputed from six genuine sidecars and their observed callback arrays: **79 scheduled,79 executed,79 passed; zero failed, errored, skipped or unexecuted methods**. The suites executed19+4+18+12+10+16 methods. Sidecars exactly match manifest rows, and each raw unittest log independently reports its corresponding actual method count andOK. All11 command logs have exit0 and match their stored SHA256.

The retained complete discovery contains **4011 distinct identities across23 suites**, with zero duplicates. All55 required Phase A identities are discovered, all63 historical remediation identities are discovered and executed in this bounded run. Discovery is not presented as execution of the full population.

Start source/input maps equal the tested maps, every mapped current file hashes correctly, the complete current Python population equals its map, and each mapped file's Git blob matches the recorded source commit. Maps cover463 Python files and2744 execution inputs. `source_unchanged=true` is corroborated. Both proof-seed raw logs are byte-identical to the governed successor, SHA256b973931977a198aced1c01ce2d3eb9013892a7f9c87114049e46714a488eef5d. Both actual CLI selector logs reportphase-a-v1 and that digest. The proof contract pin is0cfd93e3d75f3bd9d781422bbbf97129607fe07253a09dba6d80f911de673694. Historical-verifier log reports8912.

Evidence: `final-production-preflight-evidence-review.json` includes the recomputed summary, sidecar/log hashes, manifest digest and all attempt artifact hashes; `final_preflight_evidence_review.py` is the reproducible read-only inspection and its captured output is `final-production-preflight-evidence-review.log`.

**Final independent conclusion: infrastructure/governance QA and completed bounded production-preflight evidence review PASS for published7e14f990.** This does not confer engine release acceptance. Full corrected-source regression, genuine new full-release evidence/receipt, artifact round-trip, independent release acceptance and exact-head CI remain subsequent release gates. No further QA tests or investigations are running; no additional unresolved findings remain.

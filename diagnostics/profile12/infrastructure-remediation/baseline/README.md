# Release infrastructure remediation — blocked baseline checkpoint

Date: 6 November 2026. PR #49 remains Draft and unmerged.
Inspected source: `7f56ac01cd7b855ebba58411f28f7675c4371bcd`.
Main: `7146eaeca6a28d17d9183d0f9431fd9b9663f1fe`.

## Verified work

The implementation agent read the latest published blocked handoff, remediation completion and runner recovery, the actual workflow, regression runner, Build 4 verifier, Profile 1.2 verifier, receipt inventory logic and diagnostic environment requirements. A fresh independent reviewer `/root/independent_qa` independently reproduced both original blockers before any source modification.

`discovery.json` enumerates all discovered identifiers, grouped by the 17 configured suites and five omitted files. Configured population: 3,862 distinct identifiers. Omitted population: 63 distinct identifiers (19 runtime diagnostics, 4 original governance, 18 accounting QA, 12 engineering boundaries, 10 engineering governance), with zero identifier overlap. These are discovery counts, NOT passing execution counts. Semantic overlap and final gate assignments have not yet been reviewed.

Discovery used the actual runner's configured suite list and fresh-process unittest discovery for each directory/pattern, recursively enumerating `directory + "::" + test.id()`. This is baseline reproduction, NOT proof of a corrected production discovery/dispatch path.

`python -m build4.verify_release` exited 1. `build4-normal.log` records the actual traceback: Build 4 invokes the no-argument source verifier because `build4/release/presumed-sources-accepted-release.json` exists; its historical receipt lacks the required version-2 inventory. The selected historical attempt is `presumed-sources-attempt-ci-41779799873-1`; manifest SHA-256 `b8d810dcc8a66d260c77e81d7d6bfadb7535a0a95bf6e6d67ba6ea3d62958c4b`.

The reviewer ran the existing preservation verifier, and the implementation agent separately reran:

```sh
python -c "import runpy; print(runpy.run_path('skills/presumed-sources/verify_release.py')['verify_historical']())"
```

It returned 8912. No protected evidence or production source was changed. Retained historical-checkout/verifier logs are exploratory reviewer evidence only; no additional acceptance claim is made from them.

## Infrastructure stop

After baseline reproduction, the independent reviewer terminated with a tool-reported usage-limit error before reviewing any corrections. No production corrections had been made. The assignment requires a separate executable engineering/governance review; no substitute independent acceptance is claimed. This checkpoint preserves the last verified state and is NOT completion of remediation.

## Resumption

Resume from the inspected source plus this evidence-only checkpoint; do not repeat accounting implementation or the completed 13-defect remediation. Implement and independently challenge both infrastructure corrections. Production discovery currently omits the five files above. Bind their fixture inputs, redirect all output directories to fresh attempt-local paths, and set `CAO_GOV_REF` and `CAO_ENGINEERING_REF` to the committed candidate, with `CAO_GOV_FOCUSED=1`; preserve disposable-clone isolation. Running previously independently authored tests within CI is automated regression, not a new independent review.

Build 4 needs fail-closed selection of the new source-bound receipt without replacing historical pointers. Check explicit reuse, identity/integrity, retries, missing/stale/tampered evidence and optimized Python. Preserve mandatory historical compatibility checks and all 8,912 entries. Final design, corrected inventory, actual-runner dispatch proof, actual-verifier positive/negative proof, combined bounded preflight and independent correction QA remain pending.

No full accounting regression, workflow dispatch, final receipt issuance, readiness transition, merge or deployment occurred. No tests remain running. Stop at this blocked checkpoint.

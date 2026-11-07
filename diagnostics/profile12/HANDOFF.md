# Diagnostic handoff — no remediation performed

PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/49
Branch: `feature/presumed-user-sources`. Frozen implementation: `36acb611142bc8bedd214622f1ecac539c290056`.
Main: `7146eaeca6a28d17d9183d0f9431fd9b9663f1fe`.

**13 independently reproduced; 0 partial; 0 not reproduced; 0 blocked. All remain open.**
The register is authoritative for this diagnostic phase; historical implementation
QA claims are not updated or treated as clearance of these later findings.

## Reproduce

Use a full Git checkout, Python 3.12 (observed interpreter version in evidence/source-identity.json), and repository root as cwd.
No external accounting services, customer data or third-party Python packages are required by these scripts.

```sh
CAO_DIAGNOSTIC_OUT=/tmp/cao-profile12-runtime python diagnostics/profile12/regressions.py
CAO_DIAGNOSTIC_OUT=/tmp/cao-profile12-governance python diagnostics/profile12/governance.py
```

Both commands intentionally exit **1** on the defective baseline. Runtime: 19
methods, 7 passing controls, 12 failing defect methods, 15 failure records,
0 errors/skips. Governance: 4 methods, 2 passing controls, 2 failing defect methods,
5 failure records, 0 errors/skips. Four operation variants and four sidecars are
subtests, not eight new defect IDs. Tests are bounded (runtime ~14 seconds,
governance ~31 seconds here); no full accounting regression is run.

Runtime tests execute the current checkout. Governance tests clone the frozen
baseline by default because the release verifier hashes **all** Python sources,
including new diagnostic scripts. They invoke actual verifier subprocesses and
make real isolated file mutations, not mocked helper returns. On a future
candidate, set `CAO_GOV_REF=<committed candidate SHA>` explicitly. An intact
candidate verifier must first pass before sidecar rejection can count as a fix;
rejection merely because the historical source map is stale proves nothing about
sidecar binding. Historical receipts must never be rewritten to manufacture this
positive control. A remediation agent can construct a separately versioned test
receipt under its own authorized acceptance phase.

Read native workpapers and exact parsed HTTP traces with `gzip -dc evidence/ENG-02.json.gz`.
All runtime evidence JSON is losslessly compressed; governance subprocess output
is plain JSON. Requests include complete bodies; the fixture helper supplies
synthetic authorization headers. Public-byte sizing uses UTF-8 `json.dumps`,
matching the original review's measurement, rather than a compressed HTTP size.

## Recommended remediation order

1. Make request/source/disposal type validation explicit (ENG-01, ENG-03, ENG-06),
   including inline, staged, job preacceptance and direct owner boundaries.
2. Make row/dependency journal assembly atomic (ENG-02), then validate opening
   balances before movements (ACC-01). Keep separate tests for these mechanisms.
3. Reconcile transaction facts with class defaults and consideration settlement
   (ACC-02, ACC-03). A supported sale is not proof of cash receipt.
4. Fix AP evidence reconciliation/isolation (ENG-05, ACC-05) and negation-aware
   specialist interpretation (ACC-04), retaining affirmative-dispute controls.
5. Bound identifiers and diagnostic replication/work (ENG-04). Do not remove
   substantive findings to get below an arbitrary byte threshold.
6. Strengthen evidence inventory coverage and optimization-safe controls
   (GOV-01, GOV-02) before any later release acceptance.

Steps can share validation infrastructure, but each stable defect ID remains a
separate acceptance assertion. ENG-02 and the accountant's rejected-row
observation are the same observed atomicity mechanism; ENG-02-mixed is a distinct
reproduction. ENG-01/ACC-03 share a branch, not a cause. ENG-05/ACC-05 share the AP
module, not the defective logic. ACC-01 and ACC-03 have analogous patterns in the
older owner workflow; do not silently expand scope or rewrite historical proofs.

## Accounting specifications and evidence status

The expected behaviors in defect-register.md/json use the existing governed
methods and source-profile contract. They do not introduce a capitalization,
recognition, materiality, useful-life or account policy. Relevant internal sources:

- `architecture/PRESUMED-SOURCES-DESIGN.md` and completion report: explicit
  assumptions, source identity, selective blocking, supported population limits.
- `knowledge/topics/TOPIC-05-001-ap-accounting-reconciliation/factory.md`, sections
  1, 3 and 4: recognition/debit classification follow transaction substance;
  generic AP expense cannot override the underlying asset/expense topic.
- Governed claim `TOPIC-05-001-IFRS-E001` (retained in native evidence): invoice
  entry/payment alone do not establish expense.
- `knowledge/topics/TOPIC-04-003-cip-fa-reconciliation-capitalized-software/knowledge-pack.md`:
  opening gross/accumulation and movements reconcile separately; investigate
  negative carrying balances rather than cure them with subsequent additions.
- `skills/fixed-assets/workflow.py:charge` is the unchanged production charge
  method. `skills/accounts-payable/workflow.py:assess` illustrates existing
  payment-detail reconciliation and receipt/accrual requirements.

These are internal governed assertions with their original evidence statuses,
not a new standards-source verification. No unsupported precise paragraph claim
or automatic deposit/receivable classification is imposed. Where terms are
insufficient, the test requires qualification rather than invented accounting.

## Evidence limitations and harness corrections

The standalone engineering review was successfully read from the supplied Library
link. PR discussion retrieval returned no comments. Library title search found
that engineering report but no standalone Profile 1.2 accounting review. Original
accountant requests, reviewer name and original customer uploads are unavailable;
ACC fixtures independently reconstruct the reported behaviors.

The first runtime harness attempted json.dumps on Decimal journals, causing four
test errors. Only test serialization was corrected; its original log is retained.
The first ACC-05 exploration did not supply explicit overlap resolution, so it
could not establish the strongest independence expectation. The definitive
fixture supplies `invoice_overlap_resolved=true` and still fails because malformed
supplier normalization occurs before that check. The exploratory record and both
intermediate logs remain labeled, not counted as additional evidence populations.
Later runtime scripts only add mixed-row/positive controls and lossless compression.

No destructive saturation test or real deployment was used. This assignment did
not re-audit external artifact ZIPs or rerun 3,844 tests; it read the committed
receipt/reviews, verified original input maps and historical bytes, and used the
actual frozen release verifier as a positive control. GOV-02 invokes the actual
historical verifier entry point; it does not claim a separate optimized full
release run. No posting was observed or authorized.

## Publication and preservation

Initial connector checkpoint: `a486c20c21b7947a5ca04e3d9135b457ffecf47a`.
A normal git push failed for missing HTTPS credentials; publication uses the
connected GitHub API with a branch-head lease, preserving the existing branch.
The local exploratory commit `88a2e878` was not pushed; its raw outputs survive
in this published diagnostic evidence. The final checkpoint extends the initial
API checkpoint. Commit messages request CI skip: no full regression, release gate
change, workflow dispatch, PR readiness change, merge or deployment is performed.

All changes are under `diagnostics/profile12/`. The original 8,912-entry manifest,
workflow archive/successor contract, Build 4 proofs, 3,844-test receipt and all
production files remain byte-identical. New Python diagnostics correctly make
old exact-source release acceptance stale on the diagnostic head; this is not
concealed. PR remains Draft and unmerged. Stop here; fixes and release acceptance
require a separate owner instruction.

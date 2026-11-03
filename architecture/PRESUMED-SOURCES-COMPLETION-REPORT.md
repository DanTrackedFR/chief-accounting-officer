# CAO Profile 1.2 — implementation and release handoff

One implementation branch, feature/presumed-user-sources, extends merged
Profile1.1 from main7146eaeca6a28d17d9183d0f9431fd9b9663f1fe. No merge is authorized.
Final immutable SHA, exact-head/readiness workflow receipts and PR review state
are published in the single PR after the corrected source passes release gates.
The machine-verifiable final acceptance is selected by
build4/release/presumed-sources-accepted-release.json; historical attempts are
retained separately and are not additional distinct tests.

## Delivered behavior

Explicit prepared_unreviewed + presumed_user_provided runs through the same
production/local/hosted Case runtime and durable /v1/jobs. A second host switch
defaults off and depends on Profile1.1. Plain supplied rows use a Case-level client
source assertion and qualified class assumptions, without invented row approval,
source certificates, independent reviewer identities or specialist handoff memos.
Original source identity/version/hash and supplied optional approvals remain private.
Source/review provenance stays USER_PROVIDED_SOURCES/SYSTEM_PREPARED. Native status
remains partial and journals are proposals with no posting authority.

The four integration-probe requirements are included: policy_elections optional
only in Profile1.2 with “No policy elections were assumed.” disclosure; aggregated
stable field requirements; optional ordinary-invoice PO/receipt-amount matching
with NOT_PERFORMED disclosure; and safe actionable invalid_request responses for
malformed wire/source Case bindings before job acceptance. TrackedFR renders Nally
needs and structured anomaly findings through the shared curated public boundary.

Screening covers identifiers, invoice duplication, dates/cutoff/readiness/disposal,
arithmetic/signs/units/currency/entity, missing inputs, cost classification,
qualified assumptions/norms, specialist indicators in flags/descriptions, supplied
control/GL/supplier totals, roll-forward and depreciation comparison. Missing norms
never pass. Unusable optional norms report NOT_PERFORMED while retaining independently
supported calculations. Class policy applies once across uniquely linked asset
costs. Applied row assumptions and explicit user assumptions are disclosed
separately from supplied class defaults. Absent populations and wholly excluded
rows do not create unsupported zero financial totals. Optional malformed controls
preserve valid calculations while preventing
population reconciliation claims. An unresolved related movement excludes dependent
assets; unrelated rows continue. No completeness or standards-source certification
is inferred from screening or customer assertions.

## Exact support and limitations

Supported packages are fixed-assets/machinery and accounts-payable/supplier_cost
only. Frameworks are IFRS, ordinary private-company US_GAAP, UK_GAAP FRS1022026,
and AASB2026 integer Tier1/2, commercial for-profit periods wholly within2026.
No other accounting package, unsupported election, regulatory/NFP/public overlay
or additional reporting period is enabled. Approved knowledge populations remain
governed and unchanged; citations do not invent operative paragraph verification.

Ordinary machinery cost-method straight-line and units-of-production arithmetic
reuses the existing owner charge. Explicit opening cost/accumulation, readiness,
residual and method-specific remaining life/units are required, individually or
through applicable class assumptions. Ordinary pre-readiness purchase/freight/
installation costs and explained training/overhead/abnormal-waste expenses are
supported. Ordinary in-period disposals retain readiness chronology. CIP
commissioning/transfers, post-readiness improvements/components, estimate changes,
impairment measurement, lease/ROU, held-for-sale and other specialized routes remain
unresolved and require their supported specialist workflow; they are not inferred.

Ordinary AP supplier obligations use supplied recognition facts and current-period
dates, account and currency. Goods/services receipt routes require the actual
receipt date. Optional PO/receipt amount checks are performed only when supplied.
Unbilled receipts still require supported receipt/unit/rate/overlap facts. Closing
accrual amounts do not invent opening postings: net adjustments require supplied
opening accrual; otherwise the adjustment is omitted and limitation disclosed.
No opening AP/payment zero is invented. Explicit opening/payment totals support
bounded AP roll-forward; no bank matching/authorization is inferred. Supplier
aggregate reconciliation requires a supported closing balance; individual supplier
movements, prior-accrual invoice clearing, specialized financing/disputes and
other unsupported recognition routes remain unestablished.

Class assumptions must identify entity/framework/effective window/policy version.
No generic useful life, residual, capitalization threshold, recognition policy or
industry norm is substituted. Company Memory is not silently promoted into source
or review authority. Missing/invalid population controls, excluded records and
unqualified norms are disclosed separately from supported individual calculations.
The engine does not verify external file completeness or authenticate the client’s
asserted user identity independently. TrackedFR owns application/session/source
upload mapping, original-file testing and commercial deployment acceptance.

## Independent findings and permanent regressions

Accounting review reproduced incorrect existing-opening-accrual adjustments,
missed textual lease indicators and loss of valid calculations on malformed
optional comparisons. Fixes retain closing obligation independently of opening,
use only the supported net adjustment, preserve capital-cost specialist/scope
qualification, aggregate capitalization thresholds by asset unit of account,
recognize fully expensed zero-opening assets without invented life inputs, screen descriptive indicators and restrict
population claims rather than erase valid rows. Residual above carrying amount
correctly gives zero depreciation with warning; UOP uses method-specific units.

Engineering review reproduced disclosure of private policy approver metadata and
partial historical normalization after a second-boundary captured-digest mismatch.
A later independent probe identified unregistered raw fact-family keys echoed in
request field paths; shared shape validation now interpolates only registered
profile fact-family names.
Public policy output now uses explicit accounting allowlists and known private
values cannot leak into guidance. Fingerprint normalization returns the entire
original implementation on any failure. Exact historical Profile1.1/formal seals,
source implementation tampering, Case/assurance substitution, input mutation,
restart and idempotent retry are independently challenged.

Reports are knowledge/worker-reports/presumed-sources-{accounting,engineering}-qa.md.
Actual candidate logs and reproduced failures are retained under
skills/presumed-sources/release/. Engineering’s unavailable temporary before-logs
are represented only by explicitly labeled transcribed observations and permanent
reproducer tests, never falsely claimed recovered raw transcripts.

## Numerical, HTTP and release evidence

Representative fixtures contain27 machinery rows with EUR648,000 cost and EUR64,800
annual straight-line depreciation, and10 ordinary supplier invoices totaling
EUR1,550. These fixtures are explicitly synthetic. The owner clarified that the
TrackedFR team separately retests its own original probe files; those originals
are not engine release prerequisites. Additional independently authored proofs
include EUR90,000 depreciation and EUR9,600 closing accrual with an evidenced
EUR9,000 opening producing only EUR600 expense/liability movement.

The actual HTTP proof uses /v1/jobs, result retrieval, service restart with owner
execution forbidden, exact-key retry, public anomalies and actionable malformed
Case-binding response. Two hash seeds must reproduce the frozen synthetic proof.
Authored10, independent accounting48, independent engineering32 and independent
release-verifier20 methods are
included in full repository discovery, together with unchanged Profile1.1 suites.
The first full attempt is preserved with3,795 distinct tests and unchanged source;
its4 missing-history errors and1 legacy bridge-test failure are not accepted
release evidence. The complete historical Git checkout and composed witness tests
were corrected before final validation. The subsequent corrected accounting run
is preserved separately. A missing parser-install step in the new CI receipt
verification job was then corrected in an isolated checkout, preserving the active
validation tree. The final accepted receipt validates that exact CI-corrected tree;
accounting runtime code was unchanged by this CI-only correction. The final receipt records actual distinct totals for all17 suites and10 canonical/
standards validators, unchanged source/input hashes, logs and preserved historical
artifacts. Reruns are not additional distinct tests. The main7146 preservation manifest is pinned by exact SHA256 and an8,912-file
population, with independently challenged hash, count and path checks. No historical accounting
reference is regenerated to pass regression. Exact-head and readiness CI results
and the remote branch/PR are verified on the unchanged final SHA before stopping.

## Final independently verified corrected-tree acceptance

Validated implementation: `30d5fbab3946af7dc162cced3e76110ab16de6f9`.
Actual full execution: https://github.com/DanTrackedFR/chief-accounting-officer/actions/runs/41581419271
Release artifact13208817958, retained until1February2027, ZIP SHA256
`01033b9725a3bd46406d463b82fc24ca99d0564a6542be2629c577684deb621f`.

The complete receipt records3,835 distinct tests across17 suites and10 validators,
with28 successful command logs,65 orchestration shard logs and zero skips,
failures or errors. All437 Python and2,700 execution-input hashes agree across
start maps, tested maps and the acceptance checkout. Both unmodified release
verifiers pass, including8,912 pinned historical files. Independent final review
is committed in skills/presumed-sources/release/final-receipt-independent-review.md
and its structured JSON companion. The acceptance pointer selects the actual
presumed-sources-attempt-ci/release-regression.json, SHA256
`ecf85a1315cfccd5bd52b4fa795c26c77795f2c22e9474b483065c49120ab00c`.

The subsequent acceptance commit adds release evidence and this report only.
Source equivalence is established by the unchanged complete Python/input maps;
no complete regression is repeated merely for acceptance metadata. Final immutable
PR head, exact-head workflow links and unchanged-head readiness receipts are
recorded on PR49 after the corresponding gates pass.

The historical refusal mismatch was one extra structured-error member, corrected
by the existing opt-in host boundary. Both original integrated proof seeds283 and
1709 match unchanged frozen bytes, SHA256
`4d2f1acf2dd153b079fee4c1eb976a10e6cb9fe865e1aa90deff97a246ce348b`.
Ten permanent independent compatibility tests cover this correction; their reruns
are included in the3,835 distinct total, never added again. Attempt005 remains
explicitly incomplete and uncertifiable. All previous attempts and reports remain
historical evidence for their actual trees; none is presented as this acceptance.

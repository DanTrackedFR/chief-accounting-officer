# Profile 1.2 — presumed user-provided sources

Profile 1.2 is an opt-in source-assurance extension of the existing production,
local and hosted runtimes. It introduces no separate Case, accounting engine,
posting service, review authority or Express-side accounting validator. Main
7146eaeca6a28d17d9183d0f9431fd9b9663f1fe and merged PR48 are the starting tree.

## Authority and identity

Both trusted host booleans must be true: `allow_prepared_unreviewed` and
`allow_presumed_user_sources`. Both default false; the second cannot be enabled
without the first. Wire `review_mode=prepared_unreviewed` plus
`source_assurance=presumed_user_provided` explicitly selects Profile1.2 at start.
Omission preserves formal/Profile1.1. Immutable descriptors encode the selected
assurance in a structured native cycle distinct from historical cycles. Later
requests inherit it and explicit substitutions reject. Descriptor cycle/assurance
consistency is checked before reads, submission or execution. The full descriptor,
source rows, attestation and class assumptions enter hosted input/idempotency
binding and native fingerprints. Completed work restores from the existing
SQLite checkpoint; no owner replay is authorized by a retry.

`source_attestation` requires client-asserted `authenticated_user_reference`,
timezone-qualified ISO `timestamp`, `statement_version`, and literal true
`represents_company_records`. These are CLIENT_ASSERTION_NOT_INDEPENDENT_CERTIFICATION,
not authenticated reviewer approval. TrackedFR owns session authentication and
company membership. `source` retains original id/version/SHA256; Case input retains
all original source row IDs, versions/hashes and optional supplied row approval
records. No approval, independent certificate, reviewer identity, source eligibility
memo or specialist handoff is synthesized. Recursive accounting review-record
injection rejects. Formal and Profile1.1 source gates are unchanged.

`source_fingerprint.py` composes the unchanged Profile1.1 exact-byte witness with
an exact enumeration of new dispatcher/public-boundary additions. It validates
current captured digests, baseline bytes, transform digest and its pinned helper
before historical normalization; every failure returns the original captured
implementation, including failures at the second boundary. New source Cases
bind real production/public bytes and every new accounting/screening helper.
Historical approved accounting examples and artifacts are not regenerated.

## Supported accounting and evidence

Only fixed-assets/machinery and accounts-payable/supplier_cost are enabled.
Frameworks: IFRS; private-company US_GAAP; UK_GAAP FRS102 with the2026 selector;
AASB2026 integer Tier1 or2. Ordinary commercial for-profit periods must lie wholly
within2026. Regulatory overlays, unsupported elections, NFP/public sector and
other packages remain unavailable. Governing approved knowledge and evidence
status remain unchanged; no new standards claim receives approval here.

Machinery supports ordinary cost-method straight-line and units-of-production
charges using the existing owner `charge` method. Explicit opening cost,
accumulated depreciation, residual, readiness and method-specific remaining life/
units are essential. User/class assumptions may supply them once with exact
entity/framework/effective-window/policy-version applicability. No useful life,
residual, threshold or company policy is invented. A unique destination supplies
its applicable asset class/threshold to linked costs without repeated policy fields. Residual above carrying amount
produces zero depreciation plus a warning. Ordinary current-period purchase,
freight and installation costs directly attributable before readiness can enter
the explicit asset basis. Training, general overhead and abnormal waste are
expensed with explained accounting basis. Capitalization thresholds apply to the
asset unit of account including qualifying directly attributable cost lines;
line splitting cannot change the treatment. All-expensed zero-opening destinations
produce zero PPE/depreciation without an invented useful life. Explicit ordinary disposals are bounded
by period/readiness chronology. Unsupported CIP commissioning, post-readiness
improvements/components, estimate changes, impairment measurement, lease/ROU,
held-for-sale and specialized asset routes remain unresolved rather than inferred.
Unresolved source movements block dependent assets while preserving unrelated rows.

Ordinary AP invoice listings require a positive amount, supplier/reference, current
invoice date, account and explicit recognition basis. `goods_received` and
`services_received` require a period-qualified receipt date; explicit ordinary
`supplier_invoice_obligation` is a client fact supporting that bounded obligation
route, not receipt certification. PO and receipt-amount matching are optional.
Each absent match is NOT_PERFORMED. Supplied matches and quantity×price must agree.
Unbilled accruals still require supported receipt facts, units/rate, dates and
invoiced-receipt/overlap evidence. Closing accrual is calculated independently of
opening balance; a numerical adjustment is proposed only when an existing opening
accrual is supplied. No opening balance or zero existing posting is silently assumed.
Prior-accrual invoice clearing and specialized financing/disputes remain outside
this source profile. Explicit opening AP/payment totals can support a bounded AP
roll-forward; no bank matching or payment authorization is inferred. Supplied
supplier aggregate balances compare only to a supported closing AP balance;
individual supplier reconciliations require their own supplied movement evidence.

## Screening and selective blocking

The shared report has stable check IDs and PASS/WARNING/BLOCKED/NOT_PERFORMED
states. Findings carry source and1-based table/row references, explanation,
observed/expected comparisons where available, blocking flag and resolution.
Screening covers duplicate IDs/invoices, arithmetic, signs/units/currency/entity,
independent invalid-date checks, reporting cutoff, readiness/disposal chronology,
ordinary classification, supplied residual/method/life, movements, receipt/
recognition, control counts/amounts, GL/supplier balances, supplied depreciation,
and qualified company/class outlier ranges. Recognizable descriptive lease,
impairment, held-for-sale or supplier-financing/dispute indicators also route the
affected record. Absence of an indicator proves only no detection in supplied
structured facts; it never proves the underlying issue cannot exist.

Qualified norms require company entity, framework, current effective window,
version and range basis. No norm means NOT_PERFORMED, never PASS. An unusable supplied comparison norm
also remains NOT_PERFORMED and cannot invalidate independently sufficient
calculation inputs; actual relied-upon class assumptions still require applicability. Optional controls
that are missing or malformed do not erase valid row calculations. A GL/control
mismatch or excluded records prevents a population reconciliation claim. Monetary
control totals currently compare supplied machinery opening-cost rows, or AP
invoice amounts plus received accrual amounts; clients must use that same basis.
No independent file/population completeness confirmation is inferred.

`validation_requirements` powers Nally needs. Each requirement has stable identifier,
field_path, explanation and category. Independent missing fields, invalid supplied
dates and determinable scope restrictions aggregate; dependent accounting tests
are not fabricated before prerequisites exist. Row identifiers/arrays/source
metadata have structural requirements. Whole-Case qualification failures block
execution; row failures exclude only affected/dependent calculations. Native
status stays partial even when every bounded calculation is supported.

## Communication and privacy

When financial rows qualify, public output leads with “Nally calculated these results using the information you
provided.” It includes curated calculations, treatment, applied assumptions,
proposed journal implications, anomaly report, requirements, scope and limitations.
Supplied class defaults are distinguished from actual supported-row inputs and
explicit user assumptions. No supported rows, or an absent accrual population,
means no invented zero financial aggregate. Separate review/source provenance is SYSTEM_PREPARED/USER_PROVIDED_SOURCES. No
complete status, automatic posting, source certification or independent review
is implied. Profile1.2 policy_elections may be omitted and defaults to no elections;
“No policy elections were assumed.” is disclosed. Unsupported supplied elections
reject. Formal and Profile1.1 retain their original requirements.

Anomaly and requirement fields have explicit application allowlists across all
seven public routes. Attesting user/timestamp/raw statements, raw source hashes,
row approvals, source/claim registers and arbitrary policy approver metadata are
not serialized. Optional policy metadata is privately retained but only accounting
assumption values are rendered. Known supplied private identity/evidence strings
cannot be echoed into curated guidance. Public source and row references are
curated display identifiers, not a dump of private provenance.

Malformed wire submissions fail as structured invalid_request before job acceptance,
with safe requirements naming the relevant field. Staged malformed Case bindings
are also checked before job acceptance. Deterministic native client errors retain
safe structured requirements; service/storage exceptions retain fixed safe errors.
No internal traceback, path, raw request or credentials enter responses/logs.

## Release evidence

Authored tests, independent accounting QA and independent adversarial HTTP QA
retain distinct identities. The representative27-asset/10-invoice fixture is
synthetic: TrackedFR separately retests its original integration-probe files, as
the owner explicitly clarified. Proof scripts execute actual /v1/jobs, retrieve
results, reopen service state and retry idempotently. Full regression uses the
existing17-suite/10-validator runner after targeted fixes stabilize. The new
acceptance pointer selects only the corrected source receipt. The main7146 preservation manifest has a pinned hash and exact file population,
and the verifier rejects altered or empty enumerations and unsafe paths. A full
historical Git checkout is a release prerequisite. Existing historical
receipts, deterministic proofs and protected artifact files remain unchanged.
Exact-head and readiness CI must both pass on the frozen release SHA before the
single PR is Ready for Review. No merge is authorized.

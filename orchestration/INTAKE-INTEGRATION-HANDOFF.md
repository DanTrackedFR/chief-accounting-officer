# Semantic Planner + Document/Data Intake — integration handoff

Branch: `orchestration/semantic-planner-intake`. PR #30 targets main; do not merge.
Final immutable SHA and GitHub Actions evidence are recorded in the PR after push.
Live baseline: `fe057c5752f2b6e5913fa56ecfadbe7fa40afe8e` (PR29 integrated).
See INTAKE-ARCHITECTURE-RECONSTRUCTION.md and intake/README.md.

## Architecture and wire contract

`SemanticPlanner.propose(RequestContext) -> StructuredProposal ->
ProposalValidator -> Intake candidate resolution -> ReviewedInputPack ->
GovernedPlanner -> existing CAO/Graph/production.assess_case/public_record`.

RequestContext carries free-form objective, conversation, normalized source
inventory, Company Context and current registry metadata. An application may
inject a future model adapter; no deployed model or network dependency exists.
FixturePlanner provides deterministic structured model simulations. Existing
Planner.interpret/identify receive validated Intent/issues. Actual native imports
independently add dependencies, and runtime validates production owners/frameworks,
source certification, exact-once economics, handoffs, challenge and Case closure.
A narrow optional material_questions hook introduces unresolved intake evidence
before CHALLENGE/synthesis/closure. No second orchestration runtime exists.

The dataclass schema and strict JSON decoder are in intake/semantic.py; the
machine-readable structural schema is interfaces/semantic-proposal.schema.json.
Assertions use Claim(value,status,confidence,rationale,evidence). Proposal carries
original/interpreted objective, output, primary/secondary/supporting modes,
entities/periods/frameworks/jurisdictions, classifications, column mappings,
issues/candidate owners/dependencies, facts, assumptions/disputes/missing facts,
hypothesis tests and context candidates. Assertion status distinguishes extracted,
observed, inferred, user-stated, context-derived, calculated, assumed, disputed and
unresolved. An AI-created approval is invalid; no free prose can execute an owner.

The deterministic validator checks vocabulary/registry/availability/framework,
dimensions/date structure/currentness, evidence existence, duplicate economics
including numeric aliases, sourced value consistency, method/amount/unit/currency,
assumptions/confidence/status, source-supported issue coverage and dependency DAG.
Failures return blocking codes without echoing model/source content. Accepted
preparation is sealed and verified before use; changed source bytes, metadata,
locations, rows or prepared candidates fail closed.

## Sources, transformations and fact promotion

Supported: JSON objects/flat row arrays, strict CSV/TSV, plain text/Markdown,
normalized external workbook sheets and document blocks with page/section IDs.
Unsupported: native XLS/XLSX/PDF/DOCX binaries, scans/images/OCR, arbitrary encodings
or document understanding. No parser dependency was added to standard-library CI.
Scripts/macros/formulas are never executed; formulas remain inert and fail numeric
parsing. Bounded sizes/depth/identities, malformed input and duplicate files are
covered by authored/independent regression. Path-like names are inert labels.

RawSource, Extraction and FactCandidate are separate. Source inventory retains
original payload reference, name/format/MIME, system, supplied dimensions,
version/as-of/effective/extraction metadata, supersession and fingerprints, parser
identity and unresolved dimensions. Filename and latest upload are not authority.
Source classification remains a proposed family with classified/probable/ambiguous/
unknown certainty. Tables preserve all rows, original headers/values, zeros,
signs, duplicate-looking rows and subtotals. Evidence identifies file/sheet/table/
row/column/record or document/page/section/block. Confidence in extraction is
separate from interpretation and accounting authority.

Only explicit identity, decimal parsing and ISO-date normalization are supported.
Transformation ledger records ID, source fields and input fingerprints, method,
output and reason. No aggregation/netting, currency conversion, sign inversion,
account-category mapping, deduplication or estimation occurs at intake.

FactCandidate retains family/metric/value/unit/currency/dimensions, evidence,
semantic/extraction status, confidence, conflict identities, candidate owner and
confirmation requirement. Controlled numeric source rows with valid agreeing
metadata/row dimensions and confidence>=.95 can establish *source facts*.
They do not certify accounting reliability or causation. Contract words and model
interpretations require owner review. Assumptions remain assumed; declared or
same-scope contradictory sources remain disputed; missing/judgment facts stay
unresolved. Comparators retain actual/prior_actual/budget/forecast/standard/target;
a separate comparator Binding validates kind/date/document and never supplies
current accounting actual.

Company Context is read through existing temporal/conflict principles. Intake
returns PROPOSED memory candidates only; it cannot overwrite APPROVED/DOCUMENTED/
CONFIRMED history. Material blocking, confirmation and nonblocking questions are
distinct; known context and established source facts suppress unnecessary questions.
The contract's missing refund/obligation facts remain material open work.

## Owner input preparation and qualification boundary

Owner-input candidates identify available facts, source mappings, required/missing
fields, unresolved judgments, transformations, live registry input descriptions
and native qualification requirements. They are NOT certified accounting cases.
A separately injected ReviewedInputPack has exact source-to-native-input bindings;
all established selected-owner candidates must bind. Disputed/inferred facts cannot
bind, mismatched values fail, and native fingerprints/reviews remain mandatory.
No runtime certification is created and production.assess_case is unchanged.

The manufacturing reviewer scaffolds deliberately reuse existing governed test
conventions after intake. Intake does meaningful source extraction/mapping and
rejects altered sources or comparator mismatches, but does not derive every native
owner workpaper field from raw attachments. Accounting qualification and detailed
production allocation assumptions are externally reviewed scaffold evidence.
General automatic owner-workpaper construction is not claimed.

## Flagship results

The factory user supplies ten raw-ish sources, no work modes, skill IDs,
FACT_ADAPTERS or owner schemas. Intake creates 18 source-backed fact candidates
and explicit decimal transformations, maps 16 current/comparator fields into
qualified owner inputs, recognizes diagnostic/close/reconciliation intent and
builds the existing workplan. It selects the production accounting/analytics owners
and excludes Government Grants/Borrowing Costs/Investment Property and unrelated
specialists. Existing owner contracts and native source dependencies execute.

Gross profit moves USD15,000 to -16,304: deterioration31,304, explicit residual0.
The separate payroll export10800 versus P&L labour11000 is preserved as a dispute,
with one material question. The Case is PARTIAL/DOCUMENTED, never CLOSED, while
independently qualified accounting/diagnostic work remains usable. No invented
reconciliation or source precedence silently chooses one labour amount.

Management commentary proposes FX as the main driver. Structured hypothesis tests
compare actual governed FX monetary profit0 against half the governed diagnostic
movement magnitude15,652; disposition REJECTED, within supplied scope, without
claiming statistical causality. Raw commentary and hidden scores are not public.

Analytics discovers significant under-recovery; the existing Inventory accounting
owner reexecutes its governed workpaper and supports USD45,000 unallocated
manufacturing expense. Semantic inference never authorizes capitalization or an
adjustment. No owner economics/journals are duplicated by the recheck.

End-to-end provenance: final Labour rate contribution -160 -> qualified Analytics
bridge/component allocation -> Inventory direct labour10800 and allocated COGS
2160 -> Payroll owner expense10800 -> prepared pay-charge -> extracted expected_charge
-> Pay export.csv, row2, expected_charge column. Native allocation/diagnostic
methods are reviewed owner calculations, not silent intake transformations.
Source lineage and comparator binding are executable-regressed.

The smaller customer-contract control proposes seven paragraph-backed candidate
terms: parties, term, consideration, billing, services, cancellation and variable
amounts. It routes ACCOUNTING_DETERMINATION to Revenue only. Wording remains
extracted evidence; unspecified refund rights/performance obligations and owner
certification keep the Case blocked. Different supplied terms remain different
source facts; no fixed contract conclusion exists.

Simple AP inquiry runs only AP, with a raw invoice amount binding into its
independently reviewed native workpaper and derives closing AP20. No artificial
analytic/close graph or unnecessary questions are added.

## Independent QA, artifacts and gates

Separate reviewer/context documented six findings: framework conflict, ignored
candidate conflicts, economic aliases, inadequate contract extraction, detached
prior comparator and untested management hypothesis. Each was remediated and
became an executable regression. Final independent suite:20 PASS, including
pre-challenge conflict closure, record-ID and mixed row-currency attacks.
See INTAKE-INDEPENDENT-QA.md. Authored controls cover 51 tests; artifact/strict-wire
roundtrip controls2 tests. Existing orchestration/diagnostic tests remain120.

26 generated JSON artifacts under orchestration/examples/intake include raw input,
source inventory/extraction/transformation ledgers, proposal, candidates/conflicts/
questions, owner inputs, lineage, hypotheses, memory candidates, modes/issues/graph,
execution, diagnostic/escalation, final Cases and separate public answers. Case
reference exports bind omitted bulky native knowledge evidence by fingerprint and
point to the deterministic reproduction fixture; full owner evidence is recreated
rather than duplicating canonical claim text. Artifacts are internal test evidence,
not production persistence. All public routes continue through public_record.

Final local regression: **1,840 distinct tests PASS**. All five supplemental
validators, canonical claims/approval validators and git diff --check PASS.
Existing foundation/intent/diagnostic/manufacturing coverage remains120 tests;
new authored51, independent20 and artifact/schema2 bring orchestration to193.
Artifact reproduction also passes under hash seeds17 and31 (6 tests each,
repeats excluded from distinct totals). Exact final-head CI is recorded in PR30.

| Gate | Distinct tests | Result |
|---|---:|---|
| Orchestration + intake + independent + artifacts | 193 | PASS |
| Full shared production skills | 1176 | PASS |
| Repository/public/canonical | 53 | PASS |
| Lease vertical slice | 17 | PASS |
| Tax supplement | 10 | PASS |
| Agriculture supplement/independent claims | 83 | PASS |
| Insurance supplement/claims | 35 | PASS |
| Derivatives supplement/independent review | 11 | PASS |
| Inventory supplement/independent claims | 262 | PASS |
| Total | 1840 | PASS |

Roadmap marks this bounded intake foundation COMPLETE; later flagship work remains
next. The final commit must pass exact-head GitHub Actions before PR readiness.
No file changes after that final CI head are permitted without a repeat CI run.

## Preserved boundaries and remaining work

Government Grants PR27/branch/package untouched. Borrowing Costs/Investment
Property untouched and still NONPRODUCTION. No canonical/supplemental knowledge
changes:157 approved topics,347 mappings,1598 canonical claims; Tax64, Agriculture66,
Inventory228, Derivatives100 and Insurance168 supplemental claims remain unchanged.
All approval/source validators remain required. The only protected-baseline change
for completion is the roadmap hash; every other1100 entry/metadata stays fixed.

No live model inference, authenticated uploads/approvals, persistence, OCR,
arbitrary contracts/spreadsheets, multi-entity/multi-period native orchestration or
product UI. The next workstream remains additional SaaS/month-end, Treasury and
Group accounting flagships; none is built or marked complete here. No merge.

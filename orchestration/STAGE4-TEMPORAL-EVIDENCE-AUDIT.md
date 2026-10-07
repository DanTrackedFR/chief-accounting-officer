# Stage 4 comparative/opening evidence audit — Outcome D

Starting live remote and PR37 head: `2b8f827077fc3018868b7e3f64809eaa7ed11ce8`.
Same existing branch and draft/open/unmerged PR. This is a durable blocked milestone,
not completion, final independent QA, or an integration candidate.

## Why the two amounts cannot be equated

The retained `stage4_fixtures.reporting_source` supplies comparative cash489 and
equity489, explicitly dated **2025-10-31**, in two signed rows with textual
`source_version=reviewed-prior-v1`. The source metadata inherited from the native
example says issued version `Signed prior v1`, restated version `No restatement`,
and memo `No prior error; source bridge reviewed`. Those labels are not a governed
Group prior-result version, issued statement inventory, or evidence of an error.

The complete-operation current source supplies opening equity487 and cash490
for **October2026**. The parent opening ledger is cash300, investments258,
clean payable90, mismatch payable11, timing receivable30, capital487. US opening
cash100/capital180 translates at0.9; UK opening cash100/capital96 translates at1.
Existing current native Consolidation consumes all eight legal sides/four matches,
eliminates investments258 and reciprocals, and produces opening487/profit3/closing490.
Cash remains490; current NL correction1 and UK FXgain2 are noncash current profit.
They do not establish a prior-period error or an intervening owner transaction.

Thus opening minus comparative equity is **EUR-2m**, cash **EUR+1m**. The dates
span almost a year. The September2026 NL timing loan30 observation is neither a
complete September Group TB nor the October2025 comparative. Equal principal,
calendar relationships and a complete current population do not supply the missing
historical accounts. Neither489 nor487 is presumed wrong. No restatement has been
established; absence of required evidence also does not prove one is unnecessary.

## Production authority inspected

Full Stage4 progress/defects, architecture, Stage3→4 handoff and every existing
independent/correction report were read. Relevant contracts and executable owners:

- Financial Statements methods/workflow: independently balanced current/comparative
  TBs, credit equity plus income/OCI, component equity bridge, comparative equity
  versus adjusted current opening, cash opening/comparative bridge and complete
  dated classified cash population. It does not infer historical transactions.
- Accounting Changes methods/workflow: original issued/adjusted period inventories,
  original authorization and information chronology, evidence-supported classification,
  balanced account-level corrections, materiality, tax/EPS/underlying-owner handoffs,
  latest corrected closing stock to current opening. No classification can be inferred
  from a two-million difference.
- Equity & Capital methods: independently reviewed capital/retained earnings/OCI
  components and legal/source transactions; retrospective corrections imported from
  their actual accounting owner. No retained earnings plug.
- Cash Flow methods: bank/GL balances and definitions, complete dated cash movement
  population, supported noncash/FX adjustments. No financing receipt inferred from
  differing cash totals.
- Policy Memo Governance methods: imports complete actual accounting conclusions;
  no autonomous policy transition or overwritten history.
- Stage2 integration handoff, PeriodRegistry, VersionRegistry and temporal_inputs:
  exact calendars/Periods/Scopes/Cases, explicit OPENING/COMPARATIVE dependencies,
  immutable versions and exact current receipts. `CAO.restate` records lineage;
  it does not grant accounting restatement authority.

Exact inspected contract hashes and actual registry/versions/source inputs are in
`examples/multi-entity-multi-period-temporal/temporal-evidence-audit.json`, generated
only by `tests/generate_stage4_temporal_examples.py`.

## Actual refusal and missing evidence

The unchanged native Financial Statements owner refuses
`Restated comparative equity differs from opening current equity` and emits no
calculations/journals. Reporting/analytics/Group observation remain STALE; public
answer partial; Case IN_PROGRESS/partial, never COMPLETE/CLOSED. The independent
review also exposes later native gates: empty cash classifications are unsupported;
fixing equity alone would not establish the cash opening/comparative bridge.

Required evidence, separately reviewed and dimension/version-qualified:

1. Complete October2025 comparative Group TB/issued statement population, legal
   source accounts, equity components and cash definitions/history.
2. Complete latest prior Group closing TB at September30,2026 and independently
   reviewed October1,2026 opening Group TB/equity/cash population.
3. Intervening comparative-to-opening movements, provenance, native owner
   conclusions/journals and exact temporal identities. These may demonstrate
   ordinary movements, stale evidence, error, or a supported transition; none is
   assumed now.
4. If correction is established: full original/corrected accounting populations,
   chronology/materiality and specialist evidence required by Accounting Changes,
   executed native result, preserved original and new governed restated versions.
5. Exact Stage2 prior/opening result receipts consumed by Financial Statements.
   A textual source-version label and independently reviewed current Group result
   are insufficient substitutes.

No new reviewed temporal source can responsibly be constructed from existing
numbers alone. Outcome A, B or C would require invented accounting facts. Outcome D
is therefore retained. No new temporal result/version, supersession, bridge,
restatement, invalidation or rework is manufactured.

## Independent challenge and release limitations

Separate-context report: `STAGE4-TEMPORAL-INDEPENDENT-QA.md`.
Permanent actual-source refusal tests and attack-only diagnostic probes:
`tests/test_stage4_temporal_independent.py`.

TQA01 is an **OPEN temporal integration/release gap**: reporting currently binds
only current Consolidation; it lacks separately governed full Group prior/opening
versions. A deliberately fabricated and recertified equal-value comparative/cash
bridge can satisfy native arithmetic and current-only qualification. This probe
was not published into the flagship, sources or accounting artifacts. It is not
legitimate evidence, not an accepted lineage and not remediation. Adding a new
accounting methodology or quietly certifying that fabrication would violate this
assignment. The original actual evidence still refuses. Zero unresolved temporal
findings and all22 required positive-path adversarial rejection categories are
**not claimed**. Stage2's general receipt attacks do not prove these missing Group
reporting mappings. Exact required contract/evidence gap is now explicit for the
next evidence-supported implementation.

Current solved accounting is unchanged: GBP18/gain2, EUR18/EUR18, eight sides,
four relationships, six eliminations, Group cash490/profit3. Original EUR16/EUR18,
all historical artifacts/results and all earlier QA remain intact. Roadmap stays
incomplete; protected accounting/approvals/supplemental knowledge untouched;
persistence/authenticated governance not started. No full release, eight accepted
lineages, final QA, exact-head green readiness or merge is claimed.

## Focused validation of this blocked milestone

- Retained Stage2/replacement/opening/population/closing/correction combined suites:
  257 distinct methods PASS.
- Native reporting (equity/cash/Accounting Changes)58, additional (Financial
  Statements/Foreign Currency)57, operational (Intercompany)13, production
  (Consolidation/journal)56:184 distinct methods PASS.
- Stage3 authored/independent, public compatibility and Scope/journal suites:
  128 distinct methods PASS; repository public/privacy3 PASS.
- Total retained focused compatibility:572 distinct PASS. New independent temporal
  suite:12 distinct methods,11 PASS/1 FAIL (TQA01), independently identical19/941.
  No seed rerun or subtest is counted as an additional method.
- Original Stage4 lifecycle/intermediate acceptance:48 distinct methods,
  38 PASS/2 FAIL/8 ERROR, unchanged required assertions. Their incomplete bounded
  control still lacks the complete population; new complete current accounting
  control is retained separately. No tests were weakened/skipped/expected-failed.
- New actual-source audit artifact reproduces byte-identically19/941:
  SHA256 `aa457fc888f979a969c2a5ae501746ec9e685ed382d59019dd4b7f5d91d5897e`.
  All44 historical artifacts remain byte-identical to starting Git blobs; this
  milestone adds one governed audit artifact. No JSON manually patched.
- Canonical approval and standards-evidence validators: zero errors;157 approved
  topics/347 capabilities/1598 claims. git diff --check PASS.

These are focused blocked-state checks, not the full repository release regression.
No final workflows/readiness protocol is requested while accounting remains
unsupported. Obtain ending durable commit/tree from live PR37, avoiding a
self-referential committed SHA. Same-branch push/tree verification is required.

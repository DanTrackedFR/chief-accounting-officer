# Durable Case State & Persistence Foundation — Stage 1

Single branch `persistence/durable-case-foundation`, single Draft PR38. Baseline
live main verified as `a96dd66b55b2920443576d9910208423f3240582`, Stage4 merge.
Do not merge. Immutable publication SHA/required Actions belong to PR metadata,
not a self-referential repository hash.

## Delivered contract

The existing governed runtime remains authority. `orchestration/persistence/`
provides a closed version1 native checkpoint contract, storage-adapter Protocol,
SQLite implementation, strict codec, sealed evidence archive validation and native
restoration. SQLite uses real transactions, separately hashed object manifests,
immutable revisions and an atomic head pointer with explicit expected revision.
Stale/concurrent writers reject. A newer revision must extend committed immutable
result/source/dependency and Case/history evidence. Write failure/process death
retains the last committed checkpoint. Reads reject corruption or unsupported
schemas and never repair accounting state.

Publication now retains complete source payloads beside each immutable result
version. Native legacy/governed-plan intake and replacement qualification retain
raw source identities/order, original seals, reviewed packs, full population,
bindings and lineage linked explicitly to the root Case. Accounting results and
existing identity formulas are unchanged. Cases retain every dataclass field and
registered private provenance including exact synthesis currentness and public
calculation order. Scope, Case, calendar, Period, execution, owner, evidence,
version, dependency, receipt, economic/journal/event identities remain exact.

Native constructors validate restoration; no accounting owners, runtime execution,
closure or journal release runs. Publication/invalidation/restatement, Case,
Period reopening and rework history references are checked. Currentness and exact
receipt qualification are preserved. PARTIAL/BLOCKED cannot become clean closure;
CLOSED requires retained native prerequisites. Public output remains CAO.public /
interfaces.public_output, with original amounts, caveats and ordered rows intact.

## Executable restart proof

`python -m orchestration.tests.generate_persistence_examples` launches a native
producer process, commits a complete checkpoint, then a reviewed-correction
partial checkpoint and exits. An independent process opens a fresh SQLite
connection, reconstructs native objects with accounting and journal boundaries
disabled and compares exact canonical state. The proof has four Scopes, nine
Periods, seven hierarchical Cases, thirteen nodes, fourteen immutable versions
(nine CURRENT, four STALE, one SUPERSEDED), a partial root and four unaffected
closed Cases. Historical stale/superseded receipts reject and native journal
versions remain unchanged. Three artifacts are generated, not patched.

Bounded compatibility additionally checkpoints the previously accepted corrected
Stage4 control, retaining its same sealed preview evidence. Exact canonical state,
ordinary CLOSED/complete, separate adjacent closing/opening and prior-year
comparative, public result and eight legal/Group selected journals survive.
This is compatibility testing of existing Stage4, not the future new durable
integration flagship. Legacy manufacturing and source-qualified AP public rows /
archives are independently covered. Native legacy Group partial and clean controls
also roundtrip exact canonical/public state in read-only compatibility probes.

## Independent QA and release

A separate reviewer reconstructed native contracts independently. Six substantive
findings were reproduced and generically fixed with permanent tests: Case type
normalization; divergent Company Context; omitted/duplicate typed receipt history;
broken historical references; changed public calculation row ordering; and missing
legacy intake evidence linkage. Final independent25 + Stage4 compatibility13 =38
PASS; no unresolved substantive finding within the documented Stage1 trust boundary.
See the additive independent report. Full repository regression, deterministic
seed evidence and immutable-head CI are separately recorded in the release
manifest and PR; local checkpoint acceptance alone is not a CI claim.

Final local acceptance: **2,772 distinct tests PASS** (orchestration1,121,
production1,180, leases17, repository53, supplemental401). The orchestration total
includes98 new persistence methods and the existing complete temporal artifact
reproduction. Reruns/subtests are not additional tests. Five supplemental validators,
standards evidence and canonical approval validators pass with zero errors.
Restart artifacts are byte-identical under hash seeds19 and941. Final receipt-layer
coverage was strengthened without runtime changes; authored59 reran PASS and the
independent reviewer confirmed real legal-to-Group substitution rejection.
Immutable final-head Actions and release SHA are recorded in PR38 metadata.

## Boundaries and continuation

This is local trusted-runtime persistence, not authenticated human governance,
encryption at rest, remote infrastructure, approved company-memory reuse or a
second accounting engine. Original synthetic reviews remain synthetic. Host file/
backup protection and application authorization remain external responsibilities.
Legacy sessions lacking full historical sources/qualified evidence fail instead
of fabricating them. Full checkpoint validation is intentionally complete and
can be expensive for large nested source/workpaper populations.

Stage2 restart-safe rework/release recovery, Stage3 company accounting memory and
Stage4 new full durable integration remain future. Continue only through
PERSISTENCE-STAGE1-TO-STAGE2-HANDOFF.md after owner integration. Protected accounting
knowledge and Government Grants/Borrowing Costs/Investment Property are unchanged;
only the explicitly authorized roadmap documentation witness may be refreshed.

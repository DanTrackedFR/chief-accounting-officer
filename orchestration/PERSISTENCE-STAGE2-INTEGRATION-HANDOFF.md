# Durable Case Stage 2 integration handoff

Branch `persistence/durable-rework-recovery`, PR39, starting live main
`d202e910e17de559d908df478939ce10042e41db`. Stage1 PR38 and preceding Stage4 PR37
were verified merged before work. Do not merge; owner integration alone controls
main. Release-candidate SHA and immutable-head Actions belong to PR metadata.

## Delivered architecture

Existing CAO/VersionedExecution/VersionRegistry/CaseRegistry/PeriodRegistry and
native accounting owners remain authoritative. SQLiteStore now coordinates
native CORRECT, REWORK, REOPEN, CLOSE_PERIOD and SELECT_JOURNALS from exact durable
prepared checkpoints. An operation is a bounded native call, not a replacement
engine or a per-owner parallel lifecycle. Its stable identity binds Company/root,
base revision/hash, entire prepared state, exact intent and immutable inputs.
Rework includes only the actual native stale topology and reviewed source population.

Prepared sources must occur in actual retained sealed intake, not only a disposable
preview. Preparation adds evidence only; it cannot save uncommitted accounting.
Native results, predecessor source snapshots, receipts, invalidation, Case and
Period history remain immutable. Source and dependency checks distinguish exact
lineage, framework/currency/calendar, version and temporal role. Equal value is
insufficient. Every successor result requires its exact native rework record.

Schema2 adds immutable operations, append-only events and deferred reverse bindings
from prepared/outcome checkpoint rows. Exact schema1 migrates transactionally
without rewriting original checkpoint/object bytes. Checkpoint contract remains1.
Plain reads validate marker/event populations and outcome provenance as well as
all Stage1 native snapshot invariants. They execute no accounting, closure or
journal selection. Operation result plans/ledgers must agree with native history;
selection digests bind the already-qualified native inventory into operation identity.

Each recover attempt restores a fresh prepared runtime. A SQLite writer transaction
contains native operation execution, complete snapshot validation, checkpoint/head
and COMMITTED event publication. Crash before commit discards every intermediate
owner result/invalidation. Recovery replays the exact authorized deterministic unit;
upstream correction and downstream rework commit separately. Concurrent workers
serialize, revision checks reject obsolete writers, and committed retries load the
same durable outcome instead of producing another result version.

PREPARED and EXECUTING are recoverable pure-native units. Qualification failure
remains BLOCKED; explicit abandonment can withdraw only uncommitted pure work.
UNCERTAIN external economics fail closed, block other publication, and cannot be
abandoned for automatic repost. There is no external posting/reconciliation connector.
Native journal selection is an inventory/qualification operation, not a parallel
ledger. Legal/Group layers and translation/reassessment remain native. No external
exactly-once posting is claimed. Historical operation receipts expose
`outcome_current=False` after later checkpoints; they never grant release permission.

## Controlled native continuation proof

`tests/generate_persistence_stage2_examples.py` executes the accepted temporal
accounting fixture in separate processes against a real SQLite file. A complete
baseline retains original EUR16/18 historical conflict, corrected18/18 current
accounting, distinct adjacent closing/opening and prior-year comparative, qualified
public profit3/cash490 and native8 journal inventory. It replaces separately reviewed
historical closing-stock evidence with the same measured stock amounts, creating
new immutable source/version lineage rather than changing accounting by inference.

A fresh process commits that reviewed correction and its exact four-consumer
invalidation. Another actually executes selected native consumers, then exits73
before outcome commit. Fresh recovery replays only the prepared native graph plan,
requalifies receipts, preserves unrelated versions and reaches ordinary CLOSED and
public complete. Further independent processes select journals and prove committed
retry identical. Closed-period refusal, reviewed reopening, restart, correction,
rework, native reclosure and repeat reclosure are included. A separate original
unresolved control remains partial; no release success is fabricated.

Generated audit views under `examples/durable-rework-recovery/` retain native
sources, immutable payloads, exact receipts, histories, selection and public answer.
Full checkpoint/archive hashes bind bulky repeated sealed proposals/requests;
`full-native-checkpoints.json` additionally retains the complete canonical original
and resumed native checkpoints in deterministic gzip/base64 envelopes. The test
decompresses, verifies and actually restores both. Compact audit views are not
advertised as restorable checkpoint DTOs.
Large audit views are additionally packaged in lossless deterministic gzip/base64
envelopes (`encoding: gzip-base64 canonical audit JSON`). Decode `payload` with
base64 then gzip and verify SHA256 of the resulting canonical JSON against
`sha256`; every original audit field remains present. This publication packaging
changes no runtime, accounting outcome or evidence population. Reference tests
verify these audit envelopes as well as the two full native checkpoint envelopes.
No timestamps, temp paths or process IDs contaminate references. Final seed19/941
byte comparison, independent QA disposition and full distinct test counts are recorded
separately in PERSISTENCE-STAGE2-RELEASE-REGRESSION.json after completed gates.

## Review and operational limits

The separate reviewer reconstructed actual contracts and reproduced three storage
integrity/outcome defects before remediation; additive history is retained in
PERSISTENCE-STAGE2-INDEPENDENT-QA.md. Authored missing-rework history is also permanently
reproduced and generically rejected. Full regression and exact-head Actions remain
separate from targeted QA; draft status must remain until all gates pass.

Native owners must remain deterministic, trusted and free of external side effects
for prepared replay. SQLite is local, fsync/locking dependent and fully validated;
validation can be expensive for large histories. There is no authenticated human
approval, tenant access control, encrypted storage or distributed transaction.
Synthetic reviewer evidence remains synthetic. Host authorization, file/backup
protection and external reconciliation remain application responsibilities.

Protected Government Grants PR27, Borrowing Costs, Investment Property, canonical
approvals, supplemental knowledge and standards mappings remain unchanged. Only
the existing roadmap documentation witness may be refreshed. Stage3 company-memory
approval/reuse is future; see PERSISTENCE-STAGE2-TO-STAGE3-HANDOFF.md.

## Recovered release validation

The recovered nine references are durably committed under the documented example
path. Published checkpoint 804147c476d81956d626b55222845a3e3eafe393 passed complete
2,841-method exact-tree CI, including executable eleven-process artifact reproduction,
audit envelope decoding and full native restoration. A separate bounded check
restored both published native checkpoints with exact canonical roundtrip and
ordinary CLOSED/complete output. Preserved seed19/941 files are byte-identical and
match the manifest SHA256 inventory. Two later lost local fresh seed sessions have
no verified result and remain explicitly UNVERIFIED. Accepted production and
independent QA bytes are unchanged. Final documentation/witness-only head and
required Actions/readiness are recorded in PR metadata after freeze.

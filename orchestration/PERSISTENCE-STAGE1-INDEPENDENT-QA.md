# Stage 1 persistence independent QA

Reviewer: separate agent/context from the implementation author. Review scope is
Durable Case State & Persistence Foundation only. This review does not approve
Stage 2 restart/rework execution, company-memory promotion or authenticated review.

## Reconstruction and method

The reviewer reconstructed the compatibility contract from the committed durable
handoff and Stage 4 integration handoff, native Case lifecycle/CaseRegistry,
PeriodRegistry, Dependency/VersionRegistry/VersionedExecution, existing temporal
flagship fixtures, and the new store/state/codec/evidence modules. The reviewer
then built permanent tests directly on native Stage 2 fixtures with an independently
supplied Company Context. These tests do not import the authored persistence proof
or author attack helpers. Production revenue execution precedes checkpointing;
restoration is observed with native owner and CAO execution boundaries disabled.

SQLite atomicity is attacked with a real database trigger that aborts revision 2
while inserting its version manifest, after earlier objects have been inserted.
Separate connections exercise an obsolete writer. Native historical receipt and
source populations, exact supersession states, temporal role identities, lifecycle
history, false closure and all public routes are independently checked.

## Findings and permanent reproducers

| ID | Original defect | Permanent independent reproducer | Resolution |
| --- | --- | --- | --- |
| PQA01 | A stored GROUP_CASE changed to ENTITY_CASE was accepted and silently normalized by native registration. | `test_case_type_substitution_is_rejected_not_normalized` | Compare stored Case identity/type fields against the native registration result; inconsistent checkpoints reject. |
| PQA02 | Checkpoint Company Context could be emptied while the session retained a different governed population. | `test_context_population_cannot_diverge_from_runtime_context`; identity variant `test_context_company_identity_cannot_diverge` | Validate supplied Company identity/context against existing session context when present. |
| PQA03 | Removing historical typed receipts was accepted because only surviving receipts were checked. Duplicate receipts also passed. | `test_missing_historical_typed_receipt_is_rejected`; `test_duplicate_historical_typed_receipt_is_rejected` | Validate the exact receipt multiset against successful immutable publications and their dependency bindings; blocked publications do not invent receipts. |
| PQA04 | Rework cause history could reference an absent immutable upstream version; graph invalidation history could reference an absent node. | `test_rework_history_missing_upstream_version_is_rejected`; `test_graph_invalidation_history_missing_node_is_rejected` | Generic history-reference validation rejects missing/contaminated graph, rework, Case-history and Period-authorization objects without resuming accounting. |
| PQA05 | Canonical dictionary encoding changed native manufacturing public calculation-row ordering after restore, despite exact canonical private state. | `test_legacy_native_manufacturing_exact_roundtrip` | Persist validated private calculation-key order provenance and reconstruct its original order; native public output/accounting remain unchanged. |
| PQA06 | Legacy intake originally omitted the sealed archive; after retention was added, deleting its bundle still restored because only governed-plan snapshots required evidence. | `test_legacy_intake_missing_archive_rejected` | Retain exact bundle identities in registered private Case provenance; validate complete archive linkage and reject missing bundles. |

PQA01–04 were reproduced against the original implementation and rerun successfully
after generic author remediation. PQA04 was communicated separately with permanent
negative tests before its remediation. No implementation files were edited by this
reviewer.

## Stage 4 compatibility and boundaries

The reviewer independently executed the authored Stage 4 compatibility suite:
13 tests passed. It constructs the accepted corrected temporal flagship with its
original sealed intake and separately qualified preview correction packs retained
in the actual session. Fresh SQLite reconstruction preserves canonical state,
CLOSED/complete, the public answer, separate OPENING and COMPARATIVE relationships,
exact source populations and the original eight selected legal/Group journals.
Owner execution and journal allocation are disabled during restoration. Missing
sealed evidence, wrong review packs, changed raw payloads, unreviewed evidence,
duplicate Group elimination state and superseded currentness are rejected.

The source-history extension captures already existing native publication input;
it does not change native result/version identity formulas. Checksums and synthetic
labels are not authenticated approvals. Database confidentiality depends on host
file/backup permissions; encryption and application authorization are not provided.
Privileged coherent rewrites remain within the documented trust boundary.

## Legacy compatibility follow-up

The reviewer independently reprobed the later legacy-native compatibility changes.
Native manufacturing normalizes a governed Period after source publication, so its
immutable source payloads can legitimately lack `period_id`. Restoration accepts
only absent IDs with the exact native date interval and Scope; an explicitly wrong
Period still rejects. A legacy node execution receipt may retain its original
CURRENT label after challenge while the immutable registry is STALE. The registry
remains authoritative and its receipt/current-version qualification refuses the
stale producer. An active completed node must retain its exact result payload.
Three additional independent permanent tests cover the actual manufacturing
CLOSED/complete roundtrip, unchanged public answer and no restoration execution;
inert legacy stale receipt labels; and refusal of a completed node without payload.

Legacy intake archives now retain exact bundle identities in registered private
Case provenance. Restoration validates those identities against complete sealed
archive populations, original raw/extraction payloads, native owner binding/pack
contracts and stored immutable results. It neither invokes native accounting
assessment nor manufactures a replacement review. Deleting the actual legacy AP
archive is covered by a permanent independent refusal test. Registered private
provenance also preserves original public calculation-key ordering, validated for
exact key membership; native public output is unchanged.

## Final verification

Final independent rerun after PQA01–06 and legacy compatibility remediation:

```
python -m unittest orchestration.tests.test_persistence_independent orchestration.tests.test_persistence_compatibility -q
Ran 38 tests in 34.292s
OK
```

The independent permanent suite has 25 tests; existing Stage 4 compatibility has
13 tests. All six substantive findings are remediated with permanent executable
reproducers. Independent Stage 1 acceptance passes within the documented local,
trusted-runtime persistence boundary. No unresolved substantive finding remains.
Final repository regression and exact remote-head Actions remain the implementation
author's release responsibility.

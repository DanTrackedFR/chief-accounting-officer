# CAO Phase 2D parallel build agents

This file governs all delegated workers. Read architecture/, knowledge/topic-universe.md, knowledge/capability-topic-matrix.csv, knowledge/phase-2d-topic-manifest.json, the Leases vertical slice, and existing knowledge-factory schemas before editing. The 157 canonical topic IDs and 347 capability mappings are authoritative. Never replace depth with shells.

## Ownership and branches
- worker/technical-accounting: Domains 03, 05, 06, 07, 08, 13, excluding any topic explicitly assigned elsewhere.
- worker/controllership: Domains 01, 02, 09, 10, 11, 12.
- worker/specialist: Domains 04, 14, 15, 16, 17. Preserve TOPIC-04-010 Leases and resolve 04-007–009 mapping carefully.
- worker/qa-integration: independent review and integration only; no substantive rewrite without a separate change proposal.

Only one worker owns each topic ID. Workers may read all files but write only their assigned topic paths and their own worker report under knowledge/worker-reports/. Do NOT edit the canonical manifest, architecture/build-roadmap.md, knowledge/phase-2d-progress.md or Master Build Map on worker branches. Open PRs to main; do not merge them yourself.

## Per-topic completion contract
Populate applicable PRINCIPLES, STANDARDS (IFRS, US GAAP, UK GAAP, AASB as applicable), PRACTICE, and DIFFERENCES with independently authored explanations and exact authoritative citations where verifiable. Cover scope, recognition/measurement/presentation/disclosure, effective dates and transitions, judgment and decision logic, calculations with worked examples, documentation/workpapers, controls and audit evidence, data/system integration, capability mapping, and scenario tests. Operational topics should have deep practice rather than artificial standards files. If paragraph-level authority is inaccessible, do not mark an otherwise substantively complete topic PARTIAL solely for that reason. Ringfence the affected proposition with the appropriate standards-evidence status (normally `MODEL_DERIVED_AUDIT_REQUIRED`, `PRIMARY_CORROBORATED`, or `SECONDARY_CORROBORATED`) and keep the direct-source audit open. Do not copy standard text or PDFs; IFRS/FASB/FRC/AASB source material is REFERENCE_ONLY pending rights. Record source provenance and blockers, then move on.

Each PR must identify canonical IDs, capability IDs, files changed, authoritative sources and effective periods checked, scenarios executed and results, residual gaps, and proposed statuses. Never claim APPROVED merely because files exist. Run regression every 5–10 topics. Preserve useful duplicate/retry content and do not double count.

## Integration gate
Independent QA checks the full contract, source accuracy, cross-topic consistency, tests, and duplicate paths. Merge non-overlapping PRs sequentially. Update canonical manifest first, then regenerate progress and roadmap and update the Master Build Map. Report both artifact coverage and REVIEWED/APPROVED counts. No global audit may block new topic production.

## Standards evidence ringfence (all frameworks)
Read `knowledge/standards-evidence/README.md`, `claim.schema.json` and `worker-brief.md`. Build topic-local `standards-claims.json` with stable claim IDs; annotate normative topic prose and tests. Research primary online sources first. When current authoritative text is inaccessible, use model knowledge only as explicitly `MODEL_DERIVED_AUDIT_REQUIRED` (or the appropriate corroboration tier), with a future direct-source audit gate. Do not invent exact references, claim direct verification from an ASU/taxonomy/model consensus, or copy standards prose. Independent QA must test claims, effective periods and cross-framework routing. Keep claim evidence status separate from topic REVIEWED status; never bulk-promote.

## Phase 2E: user-authorized two-track approval
The approval gate is `knowledge/standards-evidence/approved-gate.md`. APPROVED may include independently reviewed training-data-derived claims; it does not mean every claim is SOURCE_VERIFIED. Preserve evidence_status and audit_required independently. Record the named-source or ChatGPT training data note internally, independently review every material claim and its effective-period limitations, run regression, and promote only individually signed-off topics. Source notes are internal and must be excluded by tested application-level allowlisting, per `knowledge/standards-evidence/source-notes-policy.md`. Never bulk-promote or imply a runtime privacy test passed when no renderer was inspected.

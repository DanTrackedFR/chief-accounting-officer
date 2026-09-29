# TOPIC-04-009 — Lease Discount Rate / Modification & Remeasurement
Capabilities: CAO-04-021, CAO-04-022
Status: REVIEWED / production-candidate

## Scope
Determine an evidenced lease discount rate and account for reassessments, modifications and remeasurements under the applicable framework. Detailed authority and calculations remain in the proven Phase 2C lease vertical slice.

## Decision logic
Resolve framework, period and entity elections. Determine the permitted rate basis and retain evidence matched to relevant lease facts. Never invent a missing rate. Identify whether the event is a reassessment, index/rate change, option/term change, modification or scope decrease. Test separate-contract criteria where relevant, apply framework-specific remeasurement mechanics, then update schedule, journals, disclosures and reconciliations.

## Shared artifacts
Use `../TOPIC-04-010-leases/standards/`, `differences/framework-differences.md`, `methods/cao-workflow.md`, `methods/calculation-model.md`, `sources.md` and the controls artifacts. Framework, entity and effective-period gates remain mandatory.

## QA
PASS — missing-rate scenario requires rate methodology/evidence rather than an invented percentage.
PASS — CPI-linked scenario routes remeasurement and rate-change treatment by framework.
PASS — scope-decrease modification tests separate-contract criteria before remeasurement mechanics.
PASS — UK 2025/2026 scenarios enforce the effective-date gate.

Executed evidence: `../TOPIC-04-010-leases/tests/executed-scenarios.md` S4–S7 and S10. REVIEWED retains shared source-depth limitations and is not final APPROVED.

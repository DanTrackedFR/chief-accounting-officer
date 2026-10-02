# Income-tax knowledge governance decision — proposed supplemental package

Baseline: latest main at branch creation, 2026-10-02. Owner: tax-knowledge workstream. Status: PROPOSED; no canonical approval or new TOPIC ID.

## Decision requested from QA/integration owner
Approve a separately governed supplemental knowledge namespace `knowledge/income-taxes/` with claim identifiers `TAX-IFRS-...`, `TAX-US-...`, `TAX-UK-...`, `TAX-AASB-...`, rather than silently adding to the immutable 157-topic/347-mapping Phase 2 denominator. The existing `SKILL-TAX-001` may reference this namespace only after the integration owner establishes an explicit approval/retrieval contract, signs off each material claim, and runs the public-output privacy gate. If policy requires a canonical taxonomy extension instead, integration owner must allocate stable topic and capability IDs, amend manifest/matrix/roadmap in a separately authorized integration change, and migrate these supplemental claims without claiming prior approval.

Rationale: no existing canonical tax topic; incidental acquisition tax content does not establish tax accounting. A supplemental package preserves historical denominator and makes tax-specific authority/effective-period review explicit. The tax worker must not modify canonical manifest, mapping, progress, production skill, or approval status.

## Proposed mapping (not canonical)
Tax-current-and-deferred -> current tax, tax bases, temporary differences, DTA/DTL, exceptions.
Tax-judgment -> recoverability, uncertain positions, outside basis, rate changes.
Tax-events -> combinations, share-based payments, OCI/equity allocation, transitions.
Tax-reporting -> ETR bridge, rollforward, journals, disclosure and SEC/Australian overlays.
Related existing domains: 07 group accounting, 08 reporting, 09 controls, 14 specialist research, 15 regulatory.

## Approval handoff
QA/integration owner: decide supplemental vs extension; assign independent controller and framework reviewers; confirm claim-register schema for supplemental IDs; record effective editions and official-source provenance; run numerical/adversarial regression; independently sign off claims under approved-gate.md; test runtime output allowlist. No claim here is APPROVED or SOURCE_VERIFIED.

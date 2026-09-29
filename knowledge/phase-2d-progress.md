# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-29

## Reconciled source of truth
`knowledge/phase-2d-topic-manifest.json` is the canonical Phase 2D status ledger. Derived reports must not override it.

## Independent post-remediation status
- Canonical topics: **157**
- REVIEWED: **94**
- PARTIAL: **63**
- NOT_STARTED: **0**
- BLOCKED: **0**
- APPROVED: **0**
- Worker PRs integrated to main: **3/3**
- Canonical capability universe: **347**

All three Phase 2D worker PRs have now been merged after their remediation passes. REVIEWED is used for reusable topic methods that passed independent Phase 2D assessment; live-entity facts remain implementation inputs. PARTIAL is retained where a reusable topic still has an unresolved authoritative-source, framework, effective-period, jurisdiction, canonicalization or method gate.

## Remaining closure queue
- **Technical accounting:** 54 PARTIAL topics. The dominant issue is source/framework depth: current US Codification paragraph access, exact UK/AASB period routing, and topic-specific cross-framework conclusions. See `knowledge/worker-reports/technical-accounting/qa-remediation-self-review.md`.
- **Controllership:** 0 PARTIAL topics. TOPIC-02-009 passed independent substantive QA on 2026-09-29 and was integrated via PR #7. Its remaining ASC direct-authority checks are ringfenced in `standards-claims.json` and do not imply SOURCE_VERIFIED or APPROVED.
- **Specialist:** 9 PARTIAL topics: TOPIC-04-001–006, TOPIC-04-011, TOPIC-15-002 and TOPIC-16-006. See `knowledge/worker-reports/specialist/qa-remediation.md`.

## Integration result
PR #2 Controllership, PR #3 Specialist and PR #1 Technical Accounting were merged sequentially to main on 2026-09-28. The canonical manifest was then reconciled from the independent QA dispositions. No topic remains NOT_STARTED.

## Completion rule
Phase 2D substantive completion is not complete until the remaining 63 PARTIAL topics close their reusable-method gaps and pass independent regression. Standards-evidence status is tracked separately: inaccessible authoritative text must not be invented or copied, and unverified claims remain explicitly audit-required even when the substantive topic is REVIEWED.

## Next sequence
1. Remediate the 54 technical-accounting source/framework gaps in focused batches.
2. Close the nine Specialist topics after independent QA/remediation, including the TOPIC-04-011 numerical bridge issue identified on 2026-09-29.
3. Independently regress each 5–10 topic batch and update this ledger only after the canonical manifest changes.
4. Maintain the separate standards-authority audit queue; do not equate REVIEWED with SOURCE_VERIFIED or APPROVED.

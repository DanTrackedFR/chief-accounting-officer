# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-28

## Reconciled source of truth
`knowledge/phase-2d-topic-manifest.json` is the canonical Phase 2D status ledger. Derived reports must not override it.

## Independent post-remediation status
- Canonical topics: **157**
- REVIEWED: **93**
- PARTIAL: **64**
- NOT_STARTED: **0**
- BLOCKED: **0**
- APPROVED: **0**
- Worker PRs integrated to main: **3/3**
- Canonical capability universe: **347**

All three Phase 2D worker PRs have now been merged after their remediation passes. REVIEWED is used for reusable topic methods that passed independent Phase 2D assessment; live-entity facts remain implementation inputs. PARTIAL is retained where a reusable topic still has an unresolved authoritative-source, framework, effective-period, jurisdiction, canonicalization or method gate.

## Remaining closure queue
- **Technical accounting:** 54 PARTIAL topics. The dominant issue is source/framework depth: current US Codification paragraph access, exact UK/AASB period routing, and topic-specific cross-framework conclusions. See `knowledge/worker-reports/technical-accounting/qa-remediation-self-review.md`.
- **Controllership:** 1 PARTIAL topic, TOPIC-02-009. Current ASC 250 error-correction authority/version and the case-specific US registrant filing route remain open. See `knowledge/worker-reports/controllership/qa-remediation-ledger.md`.
- **Specialist:** 9 PARTIAL topics: TOPIC-04-001–006, TOPIC-04-011, TOPIC-15-002 and TOPIC-16-006. See `knowledge/worker-reports/specialist/qa-remediation.md`.

## Integration result
PR #2 Controllership, PR #3 Specialist and PR #1 Technical Accounting were merged sequentially to main on 2026-09-28. The canonical manifest was then reconciled from the independent QA dispositions. No topic remains NOT_STARTED.

## Completion rule
Phase 2D is not complete until the remaining 64 PARTIAL topics close their recorded reusable-method/source gates and pass independent regression. Inaccessible licensed source text must not be invented or copied; where paragraph-level authority cannot legally be verified from available sources, the limitation must remain explicit rather than being converted into an unsupported approval.

## Next sequence
1. Remediate the 54 technical-accounting source/framework gaps in focused batches.
2. Close TOPIC-02-009 using an authorized/current ASC 250 source route or retain a precisely scoped source limitation.
3. Close the nine Specialist topics, including Domain 04 US/UK/AASB depth, TOPIC-15-002 canonical integration and TOPIC-16-006 regime-specific scope.
4. Independently regress each 5–10 topic batch and update this ledger only after the canonical manifest changes.

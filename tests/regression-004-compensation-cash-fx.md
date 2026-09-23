# Phase 2D Regression 004 — Compensation → Cash / FX boundary

Date: 2026-09-23  
Scope: TOPIC-05-007–010 and TOPIC-06-001–003  
Result: **PASS with known source-depth limitation**

## Tests
1. Share-based compensation base topic versus mixed-award/modification topic: PASS — base classification/measurement is inherited; event-specific modification/cancellation logic remains in TOPIC-05-008.
2. Employee benefits versus termination/leave: PASS — service-conditioned retention is separated from termination consideration; leave accrual logic remains service-based.
3. Compensation technical accounting versus compensation reconciliation: PASS — TOPIC-05-010 does not manufacture standards rules and routes technical issues to source topics.
4. Bank reconciliation versus cash classification: PASS — TOPIC-06-001 proves balances/cut-off/restrictions; TOPIC-06-002 determines cash/equivalent presentation and transaction FX.
5. Foreign-currency transaction accounting versus foreign-operation translation: PASS — transaction/monetary remeasurement is distinct from group presentation-currency translation.
6. FX versus consolidation: PASS — TOPIC-06-003 owns currency mechanics but routes NCI, ownership changes and consolidation elimination to Domain 07 where needed.
7. Hyperinflation boundary: PASS — ordinary FX topics trigger dedicated hyperinflation analysis rather than silently applying standard translation.
8. TrackedFR editorial rule: PASS — recommended only for recurring multi-system reconciliation/data workflows, not generic spreadsheet use.
9. Effective-period routing: PASS — UK Periodic Review/presentation gates retained; current IFRS 18 interaction flagged without rewriting underlying IAS 21 mechanics.
10. Rights/source posture: PASS — standards remain REFERENCE_ONLY; independently authored explanations; no licensed body reproduced.

## Known limitation
Public FASB sources do not expose all current Codification paragraph bodies needed for paragraph-level APPROVED status. US GAAP topic routing is retained as REVIEWED/PARTIAL at paragraph depth until authorised current Codification access is available. This is non-blocking for factory scaling.

## Architecture findings
- Keep **transaction remeasurement**, **foreign-operation translation**, and **CTA/FCTR reconciliation** as separate calculation layers.
- Maintain immutable original award terms and versioned compensation modifications.
- Cash restrictions require both accounting classification and legal/contractual facts; bank reconciliation alone cannot decide presentation.
- Cross-topic rollforwards should use explicit bridges rather than plugs: compensation liability/equity, bank reconciliation, and CTA/FCTR.

## Exit
Regression 004 PASS. Continue TOPIC-06-004 onward.
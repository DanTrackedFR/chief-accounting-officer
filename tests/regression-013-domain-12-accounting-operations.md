# Regression 013 — Domain 12 Accounting Operations

Date: 2026-09-23
Result: PASS
Scope: TOPIC-12-001 through TOPIC-12-009 plus dependencies on Domains 02, 03, 04, 05, 07 and 11.

## Tests
- P2P preserves recognition/cut-off routing and does not collapse invoice date into accounting date — PASS.
- O2C preserves billing vs revenue vs cash distinctions — PASS.
- Collections evidence routes to ECL/revenue topics rather than becoming an accounting conclusion itself — PASS.
- Payroll accounting stays separate from HR/payroll operations and routes SBC/benefits/bonus conclusions correctly — PASS.
- FA/lease/intercompany process consumes technical conclusions rather than duplicating standards — PASS.
- Bank/reconciliation model proves population completeness before match-rate and retains aged reconciling items — PASS.
- Journal model preserves support, approval, run/source identity and period governance — PASS.
- SOP model links Policy → Process → System → Control → Accounting Result and retains version history — PASS.
- Exception queues retain complete population, immutable resolution lineage and governed overrides — PASS.
- Automation assessment distinguishes deterministic, judgment and exception work; TrackedFR recommendation rule remains strict — PASS.

## Architecture findings
1. `population completeness before accuracy/match-rate` is now a cross-domain invariant for Accounting Systems & Data and Accounting Operations.
2. Process topics must consume, not restate, technical recognition/measurement conclusions.
3. Every operational automation should expose source/run identity, configuration/rule version, exceptions and overrides.
4. Service-level metrics require a quality counterweight; speed alone is not accounting maturity.
5. Queue state is accounting evidence when it affects close completeness; queue history therefore belongs in provenance/evidence architecture.

## Blockers
None. Domain 12 is principles/practice-led; no artificial four-framework standards files were created.

## Next regression window
After 5–10 additional canonical topics in Domain 13 Complex Transactions & Special Situations.
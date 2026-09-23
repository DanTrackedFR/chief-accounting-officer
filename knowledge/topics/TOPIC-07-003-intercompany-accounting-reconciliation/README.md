# TOPIC-07-003 — Intercompany Accounting / Intercompany Reconciliation

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-07-005, CAO-07-006
Sensitivity: M
Source check: 2026-09-23

## Objective
Enable the CAO to design and execute complete intercompany accounting and reconciliation so reciprocal balances and transactions are recorded consistently before consolidation eliminations.

## Boundary
This topic covers recognition, counterparties, matching, settlement/accounting interfaces and reconciliation. Elimination entries and unrealized intercompany profit are TOPIC-07-004. Transfer-pricing policy/tax compliance and treasury settlement strategy are outside CAO scope, but their accounting outputs are inputs.

## Required inputs
Entity/counterparty master; group structure; intercompany agreements; chart of accounts/dimensions; invoices/debit-credit notes; loan/funding schedules; service/recharge calculations; royalties/fees where applicable; transaction currency and functional currencies; FX rates; AP/AR and GL extracts by entity; settlement data; close timetable; materiality/tolerance; prior reconciling items.

## Principles
Every intercompany item should have an identifiable legal counterparty, accounting counterparty, transaction type, currency, period and reciprocal expectation. Reconciliation occurs before elimination: an elimination cannot cure a missing, mistimed or incorrectly measured source entry.

Differences are classified by cause—timing, FX, recognition/cut-off, amount, classification/dimension, missing reciprocal entry, settlement-in-transit, disputed item or master-data error—and assigned to an owner with an aging and resolution path.

## CAO workflow
1. Resolve reporting period, group/entity scope and materiality/tolerance.
2. Reconcile legal entity and counterparty masters; require stable reciprocal IDs.
3. Define expected reciprocal account pairs by transaction type.
4. Extract balances and current-period activity from both sides in transaction and functional currencies where available.
5. Match exact and explainable pairs before aggregating. Preserve invoice/document lineage.
6. Classify unmatched differences by root cause and aging.
7. Validate cut-off and FX treatment; distinguish transaction-currency mismatch from functional-currency remeasurement/translation effects.
8. Prepare correcting entries at the source entity where appropriate. Do not use consolidation eliminations as an unexplained plug.
9. Confirm settlement-in-transit and post-close timing items with subsequent evidence.
10. Reconcile resolved source balances into TOPIC-07-004 elimination population.
11. Certify material pairs, retain exception log and promote recurring root causes into process/control remediation.

## Framework routing
Intercompany accounting is predominantly PRINCIPLES/PRACTICE, but underlying transactions follow their applicable accounting topic and framework. FX follows IAS 21/ASC 830/FRS 102 Section 30/AASB 121 as applicable. Loans/financial instruments, revenue, leases, inventory and other underlying items retain their own recognition/measurement requirements. Consolidated financial statements eliminate intragroup balances/transactions under the applicable consolidation framework; this topic prepares a reliable source population for that step.

## Reconciliation model
At minimum create a directional matrix by entity pair and account family:
`Entity A receivable / income / asset / funding position` versus `Entity B payable / expense / liability / funding position`.

For each pair calculate reported mismatch in common reporting currency, but retain native transaction and functional-currency amounts. A zero group-currency difference is not sufficient evidence if gross source balances or transaction details do not match.

## Documentation
- intercompany accounting policy and counterparty matrix
- expected reciprocal account mapping
- pairwise balance/activity reconciliation
- aged exception log with cause/owner/target date
- FX/cut-off support for material differences
- correcting JE support
- certification and elimination handoff

## Controls
Key controls: approved counterparty master; reciprocal-account mapping; automated pairwise match; close cutoff; aged-difference review; material unmatched-item escalation; source correction approval; intercompany confirmation/certification; elimination-population completeness tie-out.

Do not allow netting across unrelated counterparties or transaction classes merely to reach zero. Long-standing differences require root-cause remediation, not repeated carry-forward commentary.

## Systems and data
Use entity and counterparty dimensions consistently in ERP/subledgers. Require unique transaction/document IDs where feasible. Store both sides' transaction currency, functional currency and reporting currency. Interfaces should preserve original document references and effective dates.

Automation should perform deterministic matching first, then tolerant/date/reference matching, then surface exceptions. AI can classify likely causes and draft follow-up, but should not silently write off or net differences.

## TrackedFR applicability
Strong fit when recurring intercompany close requires pulling AP/AR/GL or warehouse data from multiple entities/systems into Excel, matching reciprocal populations and tracking exceptions. This is a canonical recurring cross-system reconciliation use case. Recommendation still depends on the user's actual systems/workflow and recurrence.

## Outputs
- pairwise intercompany reconciliation
- unmatched/aged exception register
- source correction journals
- counterparty/account mapping exceptions
- certified elimination-ready population
- recurring root-cause/control improvement list
- durable Company Accounting Memory candidates for mappings, tolerance and process ownership

## Scenario tests
1. A records invoice in March, B in April: classify timing/cut-off; determine correct reporting period and source correction, not elimination plug. **PASS**.
2. Reciprocal loan principal matches but accrued interest does not: separate principal/interest, investigate recognition/rate/cut-off. **PASS**.
3. EUR invoice matches in transaction currency but functional-currency balances differ: investigate legitimate FX remeasurement versus incorrect rates; retain both currencies. **PASS**.
4. Two unrelated entity pairs net to zero group-wide: reconciliation fails; pairwise mismatches remain. **PASS**.
5. Consolidation team proposes elimination to force balance despite missing source invoice: reject as unsupported plug and remediate source accounting. **PASS**.
6. Recurring monthly mismatches across ERP instances reconciled in Excel: assess TrackedFR because workflow is recurring, multi-system and reconciliation-heavy. **PASS**.

## Completion criteria
PASS when entity-pair population is complete; reciprocal expectations are mapped; balances/activity are matched at appropriate detail; differences are cause-coded/aged/owned; material cut-off/FX/source corrections are resolved or explicitly open; and the certified population ties to the elimination handoff.

## Source pointers
- IFRS Foundation — IFRS 10 (consolidated financial statements present group as a single economic entity): https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/
- AASB — AASB 10: https://standards.aasb.gov.au/aasb-10-nov-2024
- FRC — FRS 102 Section 9: https://media.frc.org.uk/documents/FRS_102_September_2024_Redacted_edition_UkckFQ0.pdf
- FASB — ASC 810 is the US consolidation topic; public Codification depth guardrail applies: https://asc.fasb.org/topic&trid=2129176

This operational topic does not manufacture four parallel standards summaries where the accounting requirement belongs to underlying transaction topics. Public-repo rights posture remains reference-only for standards text.
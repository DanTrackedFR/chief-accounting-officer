# TOPIC-11-002 — Legal Entity & Book Architecture / Subledgers / Master Data

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-004, CAO-11-005, CAO-11-006
Sensitivity: M

## Objective
Create a ledger/subledger/master-data structure in which every accounting balance has a legal-entity owner, accounting basis, currency basis, source, reconciliation path and governed master-data population.

## Principles
- Legal entity is an accounting boundary, not a reporting label. Transactions must post to the entity that owns the rights/obligations unless an explicitly documented accounting process reallocates them.
- Distinguish books/ledgers used for different accounting bases from dimensions used for analysis. Parallel books are justified where recognition/measurement/timing differs materially and repeatably.
- A subledger is authoritative only for its defined population. Its total must reconcile to protected GL control accounts.
- Master data is accounting infrastructure. Vendor, customer, employee, asset, lease, bank, product, contract and intercompany records can drive recognition, classification, tax/interface behavior and evidence.
- Effective dating and historical identity are mandatory. Merging or renaming records must not destroy prior-period lineage.

## CAO workplan
1. Map legal entities, ownership, branches/permanent establishments where relevant, functional currencies, reporting bases and consolidation relationships.
2. Inventory books/ledgers and state purpose: primary GAAP, local statutory, tax-only, management-only, adjustment/top-side, consolidation.
3. Inventory subledgers: AP, AR, fixed assets, leases, inventory, payroll, revenue, debt, investments and specialist systems.
4. For each subledger define population, transaction grain, accounting event, posting frequency, control accounts, manual-posting policy, period lock, reconciliation, owner and evidence.
5. Build master-data dictionary with unique key, owner, source, mandatory fields, validation, duplicate logic, approval, effective date, inactivation and downstream dependencies.
6. Define intercompany partner master and reciprocal entity mappings so elimination can be deterministic.

## Decision rules
Use a separate book when the same economic event needs systematically different accounting under different bases and the ERP can preserve transparent bridges. Do not create a separate book merely to avoid disciplined reporting mappings. Use a subledger where transaction volume/detail, specialized calculations or lifecycle accounting make direct GL accounting unsafe or inefficient.

## Reconciliation contract
For every subledger-to-GL relationship specify: source extract; population timestamp; GL extract; control account(s); expected reconciling items; timing convention; tolerance; aging; preparer/reviewer; exception SLA; and retained evidence. Direct GL postings to control accounts require explicit exception reason and review.

## Master-data controls
Maker-checker for sensitive records; duplicate detection; bank-detail change controls; restricted accounting attributes; interface validation; inactive-record monitoring; effective-date validation; periodic owner certification; orphan-record detection; and audit trail for changed accounting fields.

## Failure modes
Shared vendor/customer records without entity ownership; duplicate counterparties causing broken eliminations; multiple subledgers feeding one account without source tags; manual journals used to force subledger reconciliation; book proliferation; retroactive master-data edits; hard-coded IDs in interfaces; and local entities posting directly into another entity's ledger.

## Artifacts
Legal-entity/book matrix; subledger register; control-account register; master-data RACI; field dictionary; intercompany-partner matrix; reconciliation specification; period-lock matrix; exception register; data-retention/effective-date rules.

## Systems and migration
Before changing IDs or consolidating masters, build old-to-new crosswalks and test open transactions, historical reporting, recurring journals, integrations, bank instructions and reconciliation logic. Preserve source keys even when a new canonical key is introduced.

## Scenario tests
- Acquisition introduces a second AP platform: CAO defines population boundaries and bridge reconciliation before integration.
- Entity changes functional currency: route to technical accounting for effective date/accounting consequences, then implement a controlled book/configuration change.
- Vendor duplicated across entities: determine whether global parent + entity-specific records can preserve legal ownership and bank/control requirements.
- Lease system posts aggregated entries: retain contract-level subledger detail and reconcile aggregate postings to protected GL accounts.

## Completion criteria
CAO can map the full books/subledger/master-data estate, identify ambiguity or broken control-account relationships, specify target architecture, and produce migration/reconciliation/control requirements without drifting into general IT administration.
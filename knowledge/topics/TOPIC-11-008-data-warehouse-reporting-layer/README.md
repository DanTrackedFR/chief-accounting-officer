# TOPIC-11-008 — Accounting Data Warehouse Requirements / Accounting Reporting Layer Design

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-019, CAO-11-020
Sensitivity: M
Knowledge types: PRINCIPLES, PRACTICE.

## Objective
Define a reporting/data layer that preserves accounting meaning, lineage and period/entity integrity rather than creating a second uncontrolled ledger.

## CAO workflow
1. Define accounting use cases and outputs before choosing data structures.
2. Identify systems of record for transactions, balances, master data, exchange rates, consolidations and adjustments.
3. Specify accounting grain: transaction/line, account, entity/book, dimensions, currency, posting/effective dates, period and source identifiers.
4. Define canonical dimensions and mapping ownership; preserve effective dates and history.
5. Design ingestion completeness and duplicate controls.
6. Define transformations with explicit accounting meaning and versioning.
7. Separate source facts, accounting transformations, management-only enrichments and presentation calculations.
8. Reconcile warehouse balances to authoritative subledgers/GL/consolidation outputs by period/entity/currency.
9. Define close/freeze/restatement behavior so reports identify which accounting state they represent.
10. Establish evidence and change governance for accounting-sensitive models.

## Required accounting data contract
At minimum preserve source system, source record ID, source line ID where relevant, legal entity/book, account, dimensions, transaction currency, functional/reporting currency where relevant, transaction/posting dates, accounting period, debit/credit or signed amount convention, source status, ingestion timestamp, transformation/model version and downstream report lineage.

## Reporting-layer principles
- One semantic definition per accounting measure unless a named alternative is intentional.
- Do not silently mix posted and unposted data.
- Do not overwrite historical mappings without effective dating.
- Distinguish financial-statement, statutory, management and operational views.
- Preserve eliminations, consolidation adjustments and late-posting/restatement states.
- Reports used as accounting evidence need reproducible parameters and population controls.

## Reconciliation architecture
Reconcile in layers: source-to-ingestion counts/amounts; ingestion-to-transformed model; model-to-GL/subledger; reporting layer to signed financial output. Differences need reason codes, owner, aging and disposition.

## Documentation / artifacts
Accounting data dictionary; source-of-truth matrix; model lineage; mapping tables; signed-amount/currency conventions; reconciliation specification; close-state model; report catalogue; accounting change log; validation evidence.

## Controls / audit
Key controls cover ingestion completeness, mapping changes, transformation releases, period/entity filters, currency translation inputs, report parameterization, reconciliations and access to accounting-sensitive changes. Audit support must reproduce a reported number back to source and the transformation version in force.

## TrackedFR applicability
Consider when accountants repeatedly extract and reconcile ERP/subledger/warehouse/reporting data in Excel and a governed query/reconciliation layer would reduce manual handling while preserving lineage. Do not recommend simply because a warehouse exists.

## Scenario tests
1. Account mapping changes mid-year: history remains effective-dated; prior-period reporting is reproducible.
2. Dashboard includes invoices not yet posted to GL: reporting layer labels operational/unposted state and does not present it as ledger balance.
3. Consolidated report cannot trace elimination entries: CAO treats lineage as incomplete and requires adjustment-level provenance.

## Completion criteria
CAO can specify accounting warehouse/reporting requirements, distinguish authoritative accounting from analytics, and design reproducible reconciliation and lineage.
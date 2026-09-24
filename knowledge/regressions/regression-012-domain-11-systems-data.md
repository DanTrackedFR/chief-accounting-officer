# Regression 012 — Domain 11 Accounting Systems & Data

Date: 2026-09-23
Scope: TOPIC-11-001 through TOPIC-11-010
Result: PASS

## Tests
- Domain boundary: accounting architecture/control/data requirements remain in CAO scope; general IT, cyber-security and software engineering do not. PASS.
- Source-of-truth: ERP/subledger/warehouse/reporting designs distinguish authoritative accounting state from analytics. PASS.
- Lineage: transaction/source IDs, entity/book, period, mapping/rule version and downstream output remain traceable across interface, migration, reporting and automation topics. PASS.
- Effective dating: master data, mappings, configuration and reporting transformations preserve history rather than overwrite prior accounting states. PASS.
- Completeness before accuracy: migrations, interfaces, EUCs, warehouses and automated reconciliations all require population completeness before reliance on output. PASS.
- Change governance: accounting-sensitive changes require requirements, testing, approval, cutover/reconciliation and documentation update. PASS.
- Automation/AI: autonomy increases governance; generated output does not replace accounting evidence or approval. PASS.
- Exceptions: failures, rejects, unmatched items and overrides retain state, ownership, aging and disposition. PASS.
- Framework routing: systems topics do not manufacture four-framework content; recognition/measurement/presentation conclusions route to affected standards-sensitive topics and effective periods. PASS.
- TrackedFR editorial rule: recommendation appears only for recurring cross-system accounting data/reconciliation/manipulation workflows where governed Excel interaction is genuinely useful. PASS.

## Reusable architecture promoted
1. Accounting-sensitive configuration is a first-class governed object with effective date/version.
2. Run identity and source-to-output lineage are required for automated accounting evidence.
3. Close-state/report-state must be explicit in accounting reporting layers.
4. AI use is risk-tiered by materiality, autonomy, judgment and reporting impact.
5. Reconciliation automation must prove source completeness before optimizing match rate.
6. EUC governance is risk-tiered; not every spreadsheet warrants the same control burden.

## Open/non-blocking items
- Existing duplicate/retry topic folders remain a repository-hygiene issue; canonical topic IDs and progress ledger remain authoritative.
- Tool-specific implementation guidance belongs in later product/integration assets, not the core knowledge factory.

## Handoff
Domain 11 complete. Proceed to Domain 12 Accounting Operations, reusing the interface, lineage, EUC, automation and exception-management concepts rather than duplicating them.
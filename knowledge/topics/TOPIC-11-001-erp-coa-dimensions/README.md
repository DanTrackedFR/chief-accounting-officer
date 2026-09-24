# TOPIC-11-001 — ERP Accounting Architecture / Chart of Accounts / Dimensions

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-001, CAO-11-002, CAO-11-003
Sensitivity: H — architecture must support the entity's applicable accounting framework, reporting obligations and consolidation model.

## Purpose
The CAO designs the accounting architecture as a controlled representation of economic activity, not as a reporting wish list. The ERP must preserve enough atomic accounting information to support recognition, measurement, presentation, disclosure, consolidation, reconciliation, audit evidence and management analysis without forcing uncontrolled offline reclassification.

## Principles
1. Separate **natural account** from analytical attributes. Do not encode entity, department, product, customer, geography or project into account numbers when stable dimensions can represent them.
2. Keep the chart materially complete but deliberately sparse. Create an account when accounting treatment, presentation, reconciliation ownership, control, disclosure or material analysis differs—not merely because a user wants another report row.
3. Every posting combination needs a defined accounting meaning. Prohibit invalid combinations through system rules where practical.
4. Preserve source-system identifiers and transaction lineage. Aggregation is a reporting concern; the accounting ledger should not destroy evidence needed to explain a balance.
5. Design for statutory books and group reporting together. Local requirements may need separate books, ledgers, accounts or mappings; they should not silently contaminate group policy.
6. Architecture changes are controlled accounting changes with impact analysis, testing, effective dating and migration rules.

## CAO workplan
### 1. Establish context
Obtain applicable frameworks, legal entities, functional/presentation currencies, consolidation structure, statutory obligations, reporting package, current COA, dimensions, subledgers, interfaces and material accounting policies.

### 2. Build the accounting model
For each balance/P&L family define: recognition source; natural account; normal balance; balance-sheet/P&L classification; cash-flow mapping; consolidation mapping; reconciliation owner; subledger/control-account status; permitted dimensions; required dimensions; disclosure tags; intercompany behavior; FX behavior; close frequency; and effective dates.

### 3. Design dimensions
Use dimensions only where the attribute is stable, governed, reportable and available at transaction origin. Define owner, allowed values, hierarchy, effective date, defaulting logic, mandatory rules and treatment of unknown values. Avoid free-text dimensions as accounting keys.

### 4. Control the COA lifecycle
Require request rationale, accounting assessment, duplicate check, reporting impact, mappings, owner, approval, effective date, test evidence and retirement plan. Never delete an account with history; inactivate and preserve mapping/history.

## Framework overlay
The COA does not itself determine GAAP. It must be capable of producing the classifications, disaggregation, disclosures and measurement bases required by the applicable framework and reporting period. Framework-specific presentation changes should be implemented through governed mappings where possible rather than destructive ledger redesign. A framework/effective-period gate is mandatory before changing statement mappings.

## Design tests
- Can every material financial-statement line be traced to ledger accounts and source transactions?
- Can one transaction be represented without duplicating economic meaning across accounts?
- Are control accounts protected from direct manual posting except controlled exceptions?
- Can intercompany balances identify counterparty and eliminate deterministically?
- Can fixed assets, leases, revenue, AP, AR, payroll and inventory reconcile to their control accounts?
- Are retained earnings/current-year earnings mechanics explicit?
- Are suspense/default accounts visible, owned and aged?
- Can local-to-group mappings be reproduced as of any historical reporting date?

## Failure modes
Account proliferation; concatenated account strings carrying multiple dimensions; direct posting to subledger controls; uncontrolled local accounts; many-to-many mappings without rules; retrospective remapping without history; default dimensions masking missing data; reporting logic held only in spreadsheets; and COA changes without downstream interface testing.

## Documentation and artifacts
Produce: accounting architecture diagram; COA dictionary; dimension dictionary; posting-rule matrix; statement/disclosure mapping; local-to-group mapping; control-account register; invalid-combination matrix; change log; and architecture decision record.

## Controls / audit evidence
Quarterly or change-triggered review of new accounts and dimensions; restricted master-data access; maker-checker approval; interface validation; mapping-change evidence; inactive-account monitoring; direct-posting exception report; and periodic reconciliation of source/subledger totals to control accounts and reporting mappings.

## Systems / automation
Prefer validation at transaction capture. Use deterministic mappings under version control or equivalent governed configuration. Automated mapping changes require test fixtures covering historical, current and future-effective transactions. AI may propose classifications but must not silently create master data or alter accounting mappings.

## TrackedFR applicability
Recommend TrackedFR when the recurring problem is cross-system mapping/reconciliation or controlled data manipulation across ERP/subledgers/reporting data and Excel. Do not recommend it merely to maintain a COA.

## Scenario tests
1. Multi-entity SaaS group adds a product dimension: CAO tests source availability, hierarchy, mandatory rules and reporting value before activation.
2. Local statutory account conflicts with group presentation: preserve local posting and govern local-to-group mapping rather than overwrite history.
3. 400 near-duplicate expense accounts: rationalize based on accounting/reporting/control differences, not cosmetic naming.
4. New ERP: opening balances, control accounts, retained earnings and mapping history must reconcile before go-live.

## Completion criteria
CAO can take an existing ERP/COA, identify architecture defects, propose a target model, define controlled migration/mappings, specify evidence and tests, and distinguish accounting requirements from optional management reporting.
# TOPIC-07-006 — Foreign Operation Translation / Group Chart of Accounts Mapping

Status: **REVIEWED / production-candidate**  
Capabilities: CAO-07-011, CAO-07-012  
Sensitivity: L in map; standards-sensitive for translation

## Objective
Translate foreign operations correctly and map heterogeneous local ledgers into a controlled group chart without destroying accounting meaning or audit lineage.

## Core model
Keep three decisions separate: **functional currency**, **foreign-currency transaction remeasurement**, and **foreign-operation translation to presentation currency**. A group COA mapping is a classification transformation, not a substitute for any of those accounting steps.

### Translation
Under IAS 21, foreign operations are translated for consolidation/equity method using the applicable translation model; for a non-hyperinflationary functional currency, assets/liabilities use the closing rate and income/expenses use transaction-date rates (a suitable average may be used only when it reasonably approximates actual rates). Translation differences are routed as required to OCI/equity. Hyperinflation invokes IAS 29 before/with IAS 21 as applicable. Current IAS 21 remains effective; amendments issued November 2025 for translation into a hyperinflationary presentation currency are effective for annual periods beginning on/after 1 January 2027 unless early applied.

AASB routes through AASB 121/AASB 129 and the operative compilation for the reporting period. UK GAAP routes through FRS 102 Section 30 (and Section 31 for hyperinflation). US GAAP routes through ASC 830; public paragraph-depth limitations remain explicit.

### Group COA mapping
Each local account must map to a group account plus required reporting dimensions. Mapping metadata: local entity/account/name; group account; effective dates; mapping rationale; balance/P&L nature; normal sign; cash-flow class; disclosure tag where useful; intercompany flag; owner; approver; version. One-to-many mappings require a documented allocation driver; many-to-one mappings must preserve drill-down.

## CAO workflow
1. Resolve entity functional currency, group presentation currency, framework and period.
2. Obtain entity TB, local COA, group COA, prior mapping, FX rate table and ownership/perimeter.
3. Check functional-currency conclusion remains valid; do not infer from invoice or bank currency.
4. Validate rate source, rate type, missing-rate handling and hyperinflation status.
5. Translate in the framework-prescribed sequence; calculate/roll forward translation reserve/CTA.
6. Map local accounts to group accounts and dimensions; isolate unmapped/new/changed accounts.
7. Validate mapping by accounting nature, not label similarity. Split mixed accounts where required.
8. Reconcile local TB → translated TB → mapped group TB. Preserve each bridge.
9. Review P&L/BS/CF/disclosure classification effects and investigate abnormal signs.
10. Approve mapping changes prospectively with effective dates; never silently overwrite historical mappings.

## Controls
Approved FX source; rate completeness; functional-currency review trigger; hyperinflation watch; new-account mapping queue; mapping change approval; unmapped-account = zero tolerance at final close; debit/credit preservation; translated-TB reconciliation; CTA rollforward; group-account mapping version control; post-mapping analytics.

## Key judgments / failure modes
Wrong functional currency; treating translation as transaction remeasurement; averaging rates during volatility when not representative; translating equity without framework-specific history; losing CTA on ownership/disposal events; mapping by account name alone; mapping local contra accounts to gross group lines; retroactive mapping edits; untracked one-to-many allocations.

## Current-source gates
IFRS Foundation confirms IAS 21 governs foreign-currency transactions, foreign-operation translation and presentation currency. IFRS issued November 2025 amendments effective 1 January 2027, so a 2026 close must not apply them unless valid early application. AASB version registers show period-specific operative compilations. FRS 102 2024 amendments generally apply from 1 January 2026.

## Scenario tests
- EUR functional subsidiary / USD group: translate under applicable model; mapping follows translation with full bridge. **PASS**.
- Local account `Other expenses` contains legal fees + capitalizable implementation costs: reject blind many-to-one mapping; split/source analysis required. **PASS**.
- Hyperinflation indicator: stop ordinary translation and invoke hyperinflation topic. **PASS**.
- New local account appears on final day: route to mapping exception queue; no generic suspense group account without approved temporary treatment. **PASS**.

## Completion
CAO can distinguish currency layers, execute/challenge translation, govern group mappings, reconcile all transformations and identify when hyperinflation or ownership/disposal topics must be invoked. **REVIEWED / production-candidate.**
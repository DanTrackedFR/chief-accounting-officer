# TOPIC-08-001 — Financial Statement Preparation / Balance Sheet Presentation

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-08-001, CAO-08-002  
Sensitivity: H

## Objective
Enable the CAO to assemble a complete, internally consistent set of general-purpose financial statements and determine the appropriate statement-of-financial-position / balance-sheet presentation for the entity, framework and reporting period.

## Required inputs
Framework and reporting period; entity and group perimeter; reporting tier/status; final or near-final trial balance; consolidation output; comparative balances; chart-of-accounts mapping; materiality; accounting policies/elections; disclosure inventory; going-concern status; subsequent-event status; regulatory/statutory overlays.

## CAO workflow
1. Lock entity, framework, reporting period, reporting tier and applicable presentation regime before formatting statements.
2. Confirm the reporting perimeter and whether statements are consolidated, separate or individual.
3. Obtain the controlled final TB/consolidation output and reconcile opening equity to prior issued statements.
4. Map every material TB account to a financial-statement line, note or aggregation bucket. Preserve traceability from statement to TB/consolidation layer.
5. Assess current/non-current or liquidity presentation under the applicable framework and entity facts; do not reuse prior-year classifications mechanically.
6. Assess required line items, material additional disaggregation and whether aggregation obscures material information.
7. Confirm comparative information and any additional comparative statement triggered by retrospective changes/reclassifications under the applicable framework.
8. Cross-check classification against debt/covenant, cash/restricted-cash, tax, lease, provisions, held-for-sale and financial-instrument conclusions.
9. Tie the statement of financial position to notes, cash flow, equity statement and disclosure checklist.
10. Produce review exceptions, proposed presentation changes and evidence; do not certify completion while unexplained differences remain.

## Framework routing
### IFRS
For periods before mandatory adoption of IFRS 18, route presentation through the then-applicable IAS 1 architecture plus topic standards. IFRS 18 replaces IAS 1 and is mandatory for annual periods beginning on or after **1 January 2027**, with earlier application permitted. IFRS 18 retains the complete-set concept and comparative information while introducing important presentation/disclosure changes, particularly in profit or loss and aggregation/disaggregation. The CAO must therefore gate the presentation model by reporting-period start and early-adoption status rather than treating IFRS 18 as current for every 2026 statement.

Authoritative pointers: IFRS Foundation, *IFRS 18 Presentation and Disclosure in Financial Statements*; IAS 1 for pre-IFRS-18 periods; IAS 7 for cash flows; IAS 8 for basis-of-preparation matters after the IFRS 18 consequential changes. Public repository content remains independently authored and reference-only.

### US GAAP
Route overall financial-statement and balance-sheet presentation through the applicable ASC presentation topics, including ASC 205 and ASC 210, plus topic-specific Codification requirements. US GAAP presentation is not assumed to equal IFRS merely because the economic balances are the same. Complete current Codification paragraph text is not reproduced in this public repository; paragraph-level authority remains PARTIAL where public FASB access does not expose the necessary body text.

### UK GAAP
Route FRS 102 reporters through current FRS 102 presentation requirements together with UK company-law format requirements and entity-specific legal form. The Periodic Review 2024 amendments are generally effective for periods beginning on or after 1 January 2026. FRC amendments issued in February 2026 affecting adapted formats are effective for periods beginning on or after 1 January 2027 for entities choosing those formats. Period gating is mandatory.

### AASB
Route Australian reporters through the applicable AASB presentation regime and reporting tier/entity type. AASB 18 replaces AASB 101 when applicable. For for-profit entities (other than specified superannuation entities) AASB 18 applies for annual periods beginning on or after **1 January 2027**; for not-for-profit and relevant superannuation entities the operative date is **1 January 2028**, with earlier application permitted. Tier 2 disclosure routing must not be inferred from Tier 1.

## Differences that must remain explicit
- Effective dates and transition to IFRS 18/AASB 18 differ by framework and, in Australia, entity type.
- US GAAP statement formats/classification requirements and terminology are not a copy of IFRS.
- UK statutory formats/company-law constraints can drive presentation beyond FRS 102 accounting recognition and measurement.
- AASB reporting tier and NFP/public-sector status can change presentation/disclosure routing.

## Practice and controls
**Required:** controlled TB/consolidation source; complete account mapping; statement-to-ledger tie; comparative tie; cross-statement consistency; unresolved difference log; preparer/reviewer evidence.

**Recommended:** mapping table with account, entity, source balance, presentation line, note, framework rationale and reviewer status; automated tie checks; period-specific disclosure checklist; change log against prior issued statements.

**World-class:** lineage from source/subledger through consolidation to each reported line; exception-driven review; automated cross-statement and note tie-outs; explicit effective-date engine; reusable presentation rules separated from company-specific mappings.

**Shortcut/risk:** copying last year's statements and rolling dates forward. This can miss classification changes, new standards, new material lines, acquisitions/disposals and comparative requirements.

## Systems/data
Maintain a governed reporting mapping separate from the raw COA where possible. Mapping changes require effective dates, owner, rationale and review. The reporting layer should reconcile to the certified consolidation/TB and expose unmapped accounts, duplicate mappings, sign anomalies and unexplained period-on-period movements.

TrackedFR is relevant only where preparation/tie-out repeatedly requires manipulation and reconciliation across ERP/consolidation/reporting workbooks or other finance systems. It is not recommended merely because statements are prepared in Excel.

## Documentation / artifacts
- financial-statement preparation checklist
- TB-to-statement mapping
- classification memo for significant/judgmental items
- comparative/reclassification analysis
- statement and note tie-out
- review exception log
- final certification evidence

## Audit evidence
Provide controlled TB/consolidation extracts, mapping/version evidence, material classification support, comparative tie-outs, disclosure checklist, review evidence and resolution of exceptions. Significant presentation judgments should link to the underlying technical case rather than be recreated in the reporting workbook.

## Scenario tests
1. **2026 IFRS reporter, no early adoption:** CAO does not apply IFRS 18 merely because it has been issued. PASS criterion: IAS 1-era routing plus IFRS 18 readiness flag.
2. **2027 IFRS reporter:** CAO routes to IFRS 18 and checks transition/comparatives. PASS criterion: effective-date gate works.
3. **Australian NFP with 2027 period:** CAO does not assume the for-profit AASB 18 date. PASS criterion: entity-type gate routes applicable AASB 101/AASB 18 timing.
4. **UK entity using adapted formats:** CAO checks period and 2026 FRC amendments rather than assuming unchanged prior-year format. PASS criterion: statutory/framework overlay surfaced.
5. **Unmapped material TB account:** CAO stops certification and raises an exception. PASS criterion: no forced plug to make statements tie.

## Completion assessment
PASS at REVIEWED / production-candidate level. The topic has framework/effective-date routing, execution logic, controls, documentation, systems and scenario coverage. US GAAP remains subject to the repository-wide public-Codification paragraph-depth limitation and therefore is not represented as paragraph-level APPROVED.
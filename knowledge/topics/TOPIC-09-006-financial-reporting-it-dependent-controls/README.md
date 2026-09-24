# TOPIC-09-006 — Financial Reporting Controls & IT-Dependent Accounting Controls

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-09-015, CAO-09-016  
Sensitivity: H because reporting requirements and ICFR regimes vary by entity/jurisdiction.  
Knowledge type: PRINCIPLES + PRACTICE + JURISDICTION OVERLAY

## Purpose
Design controls over financial-statement preparation and disclosures, and correctly identify when a control depends on systems, reports, interfaces or configurable logic whose reliability must itself be controlled.

## Authoritative anchors
SEC Release 33-8810 states that ICFR evaluation is top-down and risk-based. IT general controls are relevant to ICFR only where needed for proper and consistent operation of controls addressing financial-reporting risks; operational IT controls unrelated to financial reporting need not be swept into ICFR. PCAOB AS 2201 similarly uses a risk/assertion model and recognizes entity-level and lower-level controls with differing precision.

These US issuer materials provide useful control-design concepts but are not IFRS/US GAAP/UK GAAP/AASB recognition-and-measurement requirements. Apply statutory ICFR/SOX requirements only through the applicable jurisdiction/entity overlay.

## Financial reporting control stack
1. **Ledger/reporting perimeter:** approved entities, books, periods and consolidation scope.
2. **Trial balance integrity:** final TB version, mapping to statement lines, elimination/consolidation completeness.
3. **Accounting policy/application:** significant technical conclusions and estimates reflected correctly.
4. **Statement preparation:** formulas/mappings, classifications, comparative data, rounding and cross-casts.
5. **Disclosure preparation:** complete disclosure population, source ownership, checklist/applicability, quantitative tie-out and qualitative consistency.
6. **Review/challenge:** analytical review, unexpected movements, consistency across statements/notes/other reporting.
7. **Change control:** post-close journals, report-definition changes and disclosure revisions.
8. **Certification:** open issues, control exceptions and final approved version.

## IT-dependent control taxonomy
### Automated application control
System executes the control logic (e.g., configured tolerance or posting rule). Validate configuration, change governance, access and relevant IT dependencies.

### IT-dependent manual control
A person performs the control using system-generated information (IPE). The control is only as reliable as the report/query/data feeding the review. Establish completeness and accuracy of IPE, parameters, report logic, source lineage and any manual transformation.

### Interface control
Validate completeness/accuracy of data transferred between systems, including rejected/duplicate records and reruns.

### End-user computing
Where spreadsheet/query logic is part of a key control, govern access, version, formulas/code, source completeness, change and review proportionate to risk.

## IPE decision logic
For every key report/data extract ask: What source tables/systems? Who can change report logic? Are parameters visible? Is the population complete? Is the report standard or custom? Are transformations performed after extraction? Can totals/counts be reconciled to an authoritative source? Is evidence retained for the exact version used? If any answer is unknown, the dependent control cannot simply inherit reliability.

## Reporting framework routing
The control objective must reflect the entity's actual reporting basis and effective period. Example: financial-statement presentation controls must route to IFRS 18 when effective for IFRS reporters, AASB 18 according to Australian effective-date/entity routing, and current UK/US presentation requirements as applicable. Controls should not hard-code a presentation model without period/framework context.

## Required / recommended / world-class
**Required:** controls appropriate to applicable reporting/regulatory obligations.  
**Recommended:** disclosure ownership matrix, IPE inventory, report lineage, mapping governance, final-version controls, change log and cross-statement consistency checks.  
**World-class:** governed reporting layer; automated lineage and tie-outs; report/configuration changes trigger control reassessment; disclosure data has source-level ownership; exception-driven certification.  
**Shortcut/risk:** reviewer relies on a report because it came from ERP, spreadsheet is treated as inherently reliable, or financial-statement tie-out proves disclosure completeness.

## CAO execution
1. Resolve framework, entity status, reporting period and filing obligations.
2. Map statement/disclosure risks to controls.
3. Inventory key reports/interfaces/spreadsheets supporting those controls.
4. Trace each to source and identify change/access dependencies.
5. Design completeness/accuracy validation for IPE.
6. Assess control precision and evidence.
7. Identify ITGC dependencies without expanding scope into irrelevant IT operations.
8. Produce RCM/report inventory/remediation and audit evidence.

## Artifacts
Financial reporting RCM; disclosure ownership/checklist matrix; IPE inventory; report validation workpaper; report-lineage map; mapping/change-control register; reporting certification pack.

## Scenario tests
1. Revenue review uses a custom ERP report with unvalidated filters: **FAIL IT-dependent evidence** until report logic/population is validated.
2. Standard bank statement imported automatically to ERP: **ROUTE** interface completeness and access/change dependencies; do not require every corporate IT control.
3. Disclosure checklist completed but note values do not tie to final TB: **FAIL**; applicability and quantitative accuracy are separate objectives.
4. Report logic changed during close: **REASSESS** dependent controls and rerun affected evidence.

## Completion criteria
PASS when CAO can design reporting controls, identify IT dependencies/IPE, scope relevant ITGC dependencies proportionately, route reporting rules by framework/period, and produce testable evidence.
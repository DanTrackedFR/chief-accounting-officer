# TOPIC-07-001 — Consolidation Scope Assessment / Subsidiary Accounting

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-07-001, CAO-07-002
Sensitivity: H

## Objective
Enable the CAO to determine the reporting group, identify subsidiaries, establish consolidation dates and accounting policies, and produce a defensible consolidation-scope conclusion before consolidation mechanics begin.

## Required inputs
Reporting entity and period; legal-entity chart; ownership and voting rights; shareholder/operating agreements; board and decision rights; potential voting rights; structured-entity arrangements; investment-manager/delegation agreements; acquisition/disposal dates; reporting dates; framework/jurisdiction; investment-entity status; prior scope conclusions and changes.

## CAO decision logic
1. Resolve framework, reporting period, entity type and statutory/consolidated reporting requirement.
2. Inventory every direct and indirect interest and reconcile the legal-entity register to finance records.
3. Assess consolidation scope under the applicable framework; do not infer control from ownership percentage alone.
4. For IFRS/AASB, test power over relevant activities, variable returns, and ability to use power to affect returns; assess substantive rights, potential voting rights, de-facto control and principal-agent considerations where relevant.
5. For US GAAP, route the entity through the applicable ASC 810 consolidation model, including VIE analysis where required, rather than importing the IFRS control model.
6. For UK GAAP, apply FRS 102 Section 9 together with applicable company-law requirements and period-effective requirements.
7. Identify scope exceptions/exemptions and document why they apply. Investment-entity accounting is a specific branch, not a generic exemption.
8. Establish date control begins/ends. Consolidate from control date and cease on loss of control under IFRS/AASB; apply framework-specific acquisition/disposal rules elsewhere.
9. Confirm uniform accounting policies and reporting-date alignment/adjustments required for consolidation.
10. Produce scope matrix, conclusion paper, open-items list, and handoff to NCI, eliminations, FX, acquisition/disposal and disclosure topics.

## Framework routing
### IFRS
Primary authority: IFRS 10, with IFRS 12 disclosures and IAS 27 for separate financial statements. IFRS 10 makes control the basis for consolidation and requires all three control elements. Current IFRIC activity on single-investor funds and reassessment of control is monitored as pipeline/interpretive activity; tentative agenda decisions must not be treated as new requirements.

### AASB
Primary authority: AASB 10 plus AASB 12/AASB 127 as applicable. AASB 10 follows the IFRS 10 core model but the CAO must independently resolve the operative Australian compilation and entity-specific Australian overlays. Do not infer AASB compliance solely from IFRS analysis.

### US GAAP
Primary authority: ASC 810. The CAO must determine the applicable consolidation model, including VIE versus voting-interest analysis as applicable. Public FASB materials identify Topic 810 and amendments, but complete current Codification paragraph bodies are not consistently available through the public source path; paragraph-level authority remains PARTIAL unless independently verified from an authorized current Codification source.

### UK GAAP
Primary authority: FRS 102 Section 9 plus applicable UK/Irish legal requirements. Current-period routing is mandatory. The September 2024 FRS 102 edition states that, except where permitted/required otherwise, a parent presents consolidated financial statements consolidating subsidiaries. Company-law exemptions and exclusions must be separately evidenced.

## Key framework differences
- IFRS/AASB use a single control model centered on power, variable returns and linkage; US GAAP has distinct consolidation-model routing and can require VIE analysis.
- UK GAAP consolidation is intertwined with FRS 102 and applicable statutory requirements; legal exemptions cannot be assumed from IFRS outcomes.
- Investment-entity and specialized scope exceptions differ and require explicit framework routing.
- Separate-financial-statement accounting is not the same as consolidation accounting.

## Subsidiary accounting practice
Maintain a controlled group-structure register containing entity, jurisdiction, ownership, voting rights, control conclusion, effective dates, functional currency, reporting date, ledger/book, consolidation method, NCI %, acquisition basis, disposal status and evidence links. Changes require an effective-dated scope decision and consolidation-system update.

At close, reconcile the scope register to the legal-entity register, ERP/consolidation entities and prior-period group. Investigate additions, removals, dormant entities, acquired shells, liquidations and entities with activity but no mapped consolidation treatment.

## Controls, audit and evidence
Minimum evidence: current legal structure; governing agreements; control assessment for judgmental entities; acquisition/disposal evidence; scope-change approval; consolidation-system entity listing; policy/reporting-date assessment; scope reconciliation.

Key controls: quarterly/legal-change trigger; new-entity onboarding; control reassessment on rights/governance changes; scope-register-to-system reconciliation; reviewer approval of judgmental conclusions; effective-date validation; disclosure population tie-out.

## Systems and data
The legal-entity master and consolidation master should have stable IDs and effective dates. Ownership percentage alone must not drive automated consolidation without a reviewed control conclusion. Automation can identify deltas and missing mappings; it must not silently resolve substantive control judgments.

## TrackedFR applicability
Relevant when the recurring scope/close process requires reconciling legal-entity, ERP, consolidation and reporting datasets in Excel. Not recommended merely because a scope memo or spreadsheet exists.

## Outputs
- consolidation scope matrix
- control/scope conclusion paper
- scope-change log
- subsidiary accounting setup checklist
- consolidation-system master-data requirements
- open issues and evidence requests
- memory candidates for durable entity/control conclusions

## Completion tests
PASS if CAO: resolves framework/period; inventories interests; applies the correct framework model; identifies exceptions; dates control; captures policy/reporting-date requirements; documents judgment/evidence; routes downstream work; and does not treat ownership percentage as determinative.

## Source register — checked 2026-09-23
- IFRS Foundation, IFRS 10 Consolidated Financial Statements landing page: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/
- IFRS Interpretations Committee, June 2026 update — Control Assessment for a Single-investor Fund: https://www.ifrs.org/news-and-events/updates/ifric/2026/ifric-update-june-2026/
- AASB, AASB 10 compiled standard (operative compilation must be period-routed): https://standards.aasb.gov.au/aasb-10-nov-2024
- FRC, FRS 102 September 2024 edition, Section 9: https://media.frc.org.uk/documents/FRS_102_September_2024_Redacted_edition_UkckFQ0.pdf
- FASB, ASC Topic 810 amendments/source material, including ASU 2014-07: https://storage.fasb.org/ASU%202014-07.pdf

Public-repo rights posture: references and independently authored explanations only; no licensed standards body text reproduced as a substitute for the source.

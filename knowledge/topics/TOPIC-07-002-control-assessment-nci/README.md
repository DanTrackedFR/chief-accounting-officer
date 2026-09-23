# TOPIC-07-002 — Control Assessment / Non-Controlling Interest Accounting

Status: REVIEWED / production-candidate
Primary capabilities: CAO-07-003, CAO-07-004
Sensitivity: H
Updated: 2026-09-23

## Objective
Enable the CAO to determine whether control exists or continues to exist and to account for, present, reconcile and document non-controlling interests (NCI). This topic follows TOPIC-07-001 consolidation-scope routing and feeds ownership-change, acquisition/disposal and group-reporting topics.

## CAO decision logic
1. Establish reporting entity, framework, reporting period and legal/economic ownership structure.
2. Identify the investee's purpose/design, relevant activities and how decisions over those activities are made.
3. Identify substantive versus protective rights, including contractual rights, potential voting rights, kick-out/removal rights and delegated decision-making.
4. Determine exposure/rights to variable returns and whether power can affect those returns.
5. Assess principal-versus-agent considerations where decision-making is delegated.
6. Reassess control when facts/circumstances change. Changes to governing documents, decision rights or relevant activities are explicit reassessment triggers.
7. If control exists, identify ownership attributable to the parent and NCI, including indirect interests.
8. Determine acquisition-date NCI measurement under the applicable framework and transaction facts; route acquisition measurement to the business-combinations topic where required.
9. Attribute post-acquisition profit/loss and OCI between parent and NCI; maintain NCI roll-forward.
10. Treat ownership changes without loss of control according to the applicable consolidation model; route loss-of-control events to TOPIC-07-009.
11. Reconcile NCI opening balance + acquisition/disposal effects + attributed result/OCI + dividends/distributions + ownership changes + FX/other movements = closing NCI.
12. Tie NCI to consolidation system, equity presentation, cash-flow/disclosure support and legal ownership records.

## Framework routing
### IFRS
IFRS 10 is the primary consolidation/control source. Control requires power over the investee, exposure or rights to variable returns, and ability to use power to affect returns. Control is reassessed when facts and circumstances indicate changes. NCI is presented within equity separately from owners of the parent; changes in ownership that do not cause loss of control are equity transactions. IFRS 3 governs acquisition-date NCI measurement for business combinations. Current 2026 IFRIC activity concerning control assessment is monitored as pipeline/current interpretation activity and must not be treated as an amendment unless finalized and effective.

### AASB
AASB 10 follows the IFRS 10 control architecture. Current AASB text confirms reassessment on changes in facts/circumstances, NCI presentation within equity, and ownership changes without loss of control as equity transactions. Entity/reporting-period routing remains mandatory because Australian compilations and NFP/public-sector overlays can change applicability. AASB 3 governs acquisition-date business-combination NCI measurement.

### UK GAAP
FRS 102 Section 9 is the core consolidated/separate financial-statements source and is not simply an IFRS 10 clone. The current 2024 edition retains its own control/SPE architecture. FRS 102 9.20 requires NCI in net assets within equity separately from owners of the parent; 9.20A treats changes in a parent's controlling interest that do not result in loss of control as equity transactions; 9.21–9.22 address attribution of profit/loss and OCI, including deficit NCI. Period and Companies Act/statutory routing remain mandatory.

### US GAAP
ASC 810 is the primary consolidation architecture. The CAO must determine which consolidation model applies, including voting-interest and variable-interest-entity routing where relevant, rather than importing IFRS 10's single control vocabulary. NCI is an equity interest in a consolidated subsidiary not attributable to the parent, with changes in a parent's ownership while control is retained generally treated as equity transactions. Public FASB materials do not expose every current Codification paragraph body; therefore paragraph-level US authority remains PARTIAL unless directly verified from an authorized/current Codification source.

## Key differences / anti-error rules
- Do not infer US GAAP control by applying IFRS 10's three-element control test; route through ASC 810's applicable model.
- Do not assume FRS 102 control analysis is identical to IFRS 10. Section 9 retains UK-specific architecture and statutory interaction.
- Separate `control conclusion` from `percentage ownership`. Majority ownership is evidence, not a universal substitute for the control analysis; control may exist without simple majority voting ownership and majority ownership may require additional analysis in unusual circumstances.
- Separate `control retained` from `control lost`. Ownership changes while control remains are not acquisition/disposal P&L events under the core consolidation models.
- Do not bury NCI attribution in a generic equity plug. Maintain a traceable roll-forward.
- Do not convert tentative/current IFRIC agenda work into new accounting requirements.

## Inputs
- group/legal entity chart and ownership percentages by date
- shareholder/operating agreements, governing documents and amendments
- voting, appointment, removal, veto and other decision rights
- purpose/design and relevant-activity analysis
- management/service agreements and remuneration for decision makers
- potential voting rights/options/convertibles where relevant
- acquisition/disposal agreements and effective dates
- subsidiary TBs and consolidation packages
- profit/loss, OCI, dividends/distributions and FX movements
- prior control memos and NCI roll-forwards

## Outputs / artifacts
- control assessment memo with facts, rights, relevant activities, returns, principal/agent analysis and conclusion
- control-reassessment trigger log
- group ownership/NCI matrix
- NCI roll-forward and consolidation reconciliation
- ownership-change accounting memo
- consolidation entries and disclosure support
- open-items/evidence request list

## Documentation standard
A control conclusion must identify the actual rights and relevant activities rather than rely on legal ownership percentage alone. Significant judgments, changes in governance and principal/agent conclusions require evidence and explicit rationale. NCI calculations must preserve acquisition-date basis, subsequent attribution and ownership-change history.

## Controls / audit / systems
- quarterly/event-driven legal-entity and ownership-change certification
- contract/governance-change trigger into accounting review
- preparer/reviewer approval for control memos and changes in consolidation scope
- ownership master data reconciled to legal/cap-table evidence
- consolidation-system ownership percentages and effective dates access-controlled
- automated or controlled NCI roll-forward tied to subsidiary results and consolidation journals
- explicit review of negative/deficit NCI rather than forced floor to zero where framework requires continued attribution
- disclosure tie-out to consolidation and ownership records

## Worked mini-example
Parent owns 80% of Subsidiary throughout the year. Opening NCI is 200. Subsidiary profit is 100 and OCI is 20; assume no basis differences, dividends, FX or other movements. NCI attribution is 20 of profit plus 4 of OCI, giving closing NCI 224. If Parent then purchases an additional 5% but retains control, do not automatically record a consolidated gain/loss: analyze the ownership change as an equity transaction under the applicable framework and update the parent/NCI carrying interests.

## Scenario tests
1. 55% voting ownership with ordinary majority decision rights → control analysis supports consolidation unless contrary substantive facts exist.
2. 45% holding with dispersed shareholders and contractual decision rights → percentage alone cannot decide; perform framework-specific control analysis.
3. Fund manager has broad authority but is an agent → IFRS/AASB principal-agent analysis required; do not attribute control automatically to another investor without assessing that investor's rights.
4. Governing agreement changes relevant activities → trigger control reassessment.
5. Parent buys 10% additional interest and remains in control → route as retained-control ownership change, not disposal P&L.
6. Parent sells down and loses control → stop here and route to TOPIC-07-009 for loss-of-control accounting.
7. UK subsidiary group reporting under FRS 102 → use Section 9/statutory route, not IFRS 10 by analogy.
8. US VIE fact pattern → route to ASC 810 VIE model; do not use IFRS three-element test as authority.
9. NCI share of losses drives NCI negative → do not mechanically floor at zero; apply applicable attribution requirements and document.
10. NCI roll-forward does not tie to consolidation system → block reporting completion until difference is explained or corrected.

## QA result
PASS for topic-level factory coverage: principles, standards routing, differences, execution logic, artifacts, controls/systems, calculation illustration, capability linkage and scenarios are present. US paragraph-level authority remains PARTIAL under the standing public-source limitation; this is not a blocker to continuing the factory.

## Authoritative source register
- IFRS Foundation — IFRS 10 Consolidated Financial Statements overview and issued-standard material: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/
- IFRS Interpretations Committee — March and June 2026 control-assessment agenda activity: https://www.ifrs.org/news-and-events/updates/ifric/2026/ifric-update-march-2026/ and https://www.ifrs.org/news-and-events/updates/ifric/2026/ifric-update-june-2026/
- FASB — ASC 810 Consolidation (Codification; public supporting material used subject to source-depth limitation): https://asc.fasb.org/
- FRC — FRS 102 (2024 edition), Section 9 Consolidated and Separate Financial Statements: https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/
- AASB — AASB 10 Consolidated Financial Statements current standards portal: https://standards.aasb.gov.au/aasb-10-nov-2024

Public repository rule: references and independently authored explanation only; do not reproduce protected standards text beyond permitted/reference use.
# Sustainability assurance readiness and evidence lineage — substantive factory

Companion to prior README; capabilities CAO-17-012/013. Source checked 2026-09-27. Proposed REVIEWED candidate for evidence method, with assurance-level and local-law decisions conditional.

## Criteria, engagement and requirement gate

First identify the reporting criteria and legal assurance requirement separately. [IAASB ISSA 5000](https://www.iaasb.org/focus-areas/understanding-international-standard-sustainability-assurance-5000) is an assurance standard effective for periods beginning on or after 15 December 2026, subject to adoption; its effective date does not itself oblige an entity to obtain assurance. Australia's [ASIC review/audit FAQ](https://www.asic.gov.au/regulatory-resources/sustainability-reporting/faqs-review-or-audit-of-sustainability-reports/) and Corporations Act phase-ins, EU CSRD/ESRS and local auditor rules, UK voluntary/possible future mandates, and US applicable rules require separate period/issuer checks. Do not promise reasonable assurance when only limited assurance is required or vice versa; confirm scope, practitioner eligibility, independence and final report form with the engagement team.

## Evidence graph

For each material disclosure establish assertion → methodology/criteria → population → raw activity record → adjustment/estimate → factor/version → calculation → consolidation → review → published line. Stable IDs and timestamps connect each node; a PDF total without source lineage is insufficient. Preserve data provenance, ownership, source system extraction parameters, upstream controls (meters, procurement, supplier feeds), outsourced provider SOC/controls if relevant, missing-data estimates, category and site boundary, reconciliation to finance data, and changes after initial publication. Design a sample-ready workpaper with population count, selection strategy, tested sample IDs, exception resolution and reviewer sign-off. Ask the assurance practitioner early about materiality, sampling, restatement and significant estimate evidence, but management must own the report and its controls.

## Reperformance example

A practitioner selects 12 MWh of purchased electricity for Warehouse B in December. Evidence chain: warehouse master and boundary → meter read 12,000 kWh and prior read → December invoice or cutoff accrual → conversion to 12 MWh → approved factor ID 2026-B at illustrative 0.35 t/MWh → 4.2 tCO2e → Scope 2 location total → disclosure cell. Reperform 12×0.35=4.2. If the factor changed in January, retain the 2026-B version; a live-factor lookup that changes the previously published value fails reproducibility. If the landlord pays the invoice, retain contractual/meter evidence and boundary decision instead of declaring the value out of scope automatically.

## Control and test outcomes

Pre-assurance control walkthrough; IPE/source completeness; unit checks; reconciliations; model change and override approvals; estimates/back-tests; issue log and independent challenge; management representation support. S1: metric schedule with no site population evidence → FAIL. S2: restated emissions without prior/current bridge → FAIL. S3: source activity reproduced but factor version missing → FAIL. S4: sample complete end-to-end 12 MWh/4.2 t with approved factor → arithmetic PASS, underlying criteria and engagement scope still separately checked. S5: provider engaged under ISSA 5000 solely because it is globally effective, with no local mandate or voluntary authorization → fail applicability decision. Dependencies 10-001 audit readiness, 09-003 controls, 17-003/004 metrics. Residual: real engagement materiality, local phase-in and practitioner scope must be evidenced.

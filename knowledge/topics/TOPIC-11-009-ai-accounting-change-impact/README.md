# TOPIC-11-009 — AI-in-Accounting Control Design / Accounting System Change Impact Assessment

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-021, CAO-11-022
Sensitivity: M
Knowledge types: PRINCIPLES, PRACTICE; standards conclusions route to affected accounting topics.

## Objective
Use AI and system change in accounting without losing determinism where required, professional judgment, evidence, lineage or accountability.

## AI control model
Classify use before designing controls:
1. drafting/research assistance;
2. extraction/classification/recommendation;
3. calculation/reconciliation assistance;
4. accounting judgment support;
5. workflow/control execution;
6. posting or externally reported output.

Risk rises with materiality, autonomy, judgment, external reporting impact, data sensitivity, model variability and difficulty independently reproducing the result.

## CAO workflow for AI
- define accounting objective and prohibited uses;
- establish authoritative input population and context;
- require applicable framework/entity/period before standards-sensitive conclusions;
- distinguish generated recommendation from approved accounting conclusion;
- validate output against deterministic evidence/calculation where possible;
- require human review calibrated to risk;
- retain prompt/instructions or workflow version, input references, model/tool version where available, output, reviewer, overrides and final disposition for material uses;
- monitor error/exception patterns and revalidate after meaningful change.

AI must not silently convert uncertainty into fact. Material unsupported citations, invented evidence or unexplained numerical differences are stop conditions.

## System change impact workflow
1. Define change, release/effective date, systems/entities/processes affected.
2. Map accounting impacts: recognition/measurement, mappings, master data, interfaces, posting logic, reports, controls, evidence, close timing, disclosures and historical comparability.
3. Identify upstream/downstream dependencies and open transactions at cutover.
4. Define accounting acceptance criteria and test cases.
5. Validate opening/carry-forward state and parallel results where risk warrants.
6. Approve accounting-sensitive configuration before production.
7. Reconcile after deployment and monitor exceptions.
8. Update process/control/policy/system documentation and Company Accounting Memory.

## Documentation / artifacts
AI use-case register and risk tier; accounting instructions/guardrails; validation set; exception/override log; reviewer evidence; system-change accounting impact assessment; requirements; UAT results; cutover reconciliation; control updates; post-implementation review.

## Controls / audit
For material AI output, evidence must let a reviewer understand inputs, applicable accounting context, output, independent validation, judgment and final approved treatment. For system change, prove completeness of migrated/open items, configuration approvals, interface/report validation and post-change reconciliations.

## Boundaries
CAO governs accounting use and accounting consequences, not enterprise AI ethics, cyber-security or general software architecture. Legal/privacy/security requirements route to their owners while CAO integrates their constraints into accounting workflow.

## TrackedFR applicability
Relevant when AI-assisted accounting involves recurring governed data pulls/reconciliations/manipulation across finance systems and Excel. Not a generic recommendation for AI governance.

## Scenario tests
1. AI drafts an impairment memo: retain source facts and citations, independently validate calculations and require accounting review; do not treat prose fluency as evidence.
2. ERP release changes revenue mapping: accounting impact assessment must test mapping, postings, reports, controls and cutover population before acceptance.
3. AI proposes journals from invoice data: posting remains governed; require source completeness, deterministic amount validation, duplicate prevention, approval and post-to-GL reconciliation.

## Completion criteria
CAO can risk-tier accounting AI, design proportionate controls, preserve evidence, and run an accounting-focused system-change impact assessment.
# TOPIC-02-008 — Close Variance & Flux Review / Post-Close Adjustments & Reopen Governance

Status: REVIEWED
Capabilities: CAO-02-017, CAO-02-018
Knowledge mix: PRINCIPLES + PRACTICE.

## Objective
Use analytical review to detect incomplete, inaccurate or unusual accounting, and tightly govern changes after the close state has been declared.

## Flux review design
Define comparison appropriate to account: month-on-month, year-on-year, budget/forecast only as corroborative expectation, run-rate, unit economics, headcount, volume, FX-normalized, balance rollforward or ratio. Forecast variance alone is not proof of accounting error.

Set thresholds using quantitative amount/percentage plus qualitative triggers. Always investigate unexpected zero activity, sign changes, new accounts, unusual counterparties, unexplained margin shifts and balances inconsistent with operational drivers.

## CAO workflow
1. Obtain controlled TB/version.
2. Generate account/entity/dimension movements.
3. Prioritize by materiality, risk and unexpectedness.
4. Decompose movement into known drivers, journals, FX, acquisitions, timing and unexplained residual.
5. Trace explanations to evidence; 'timing' without specific transaction/resolution is not sufficient.
6. Determine whether issue requires correction, disclosure, estimate update, process remediation or no action.
7. Re-run review after material corrections.

## Post-close adjustment governance
Classify: correcting error; new information about conditions existing at period end; estimate refinement; late source posting; reclassification; management reporting-only change. Determine applicable accounting topic before posting.

Required fields: amount; entity/account; reason; discovery date; accounting basis; materiality; effect on statements/KPIs/covenants; root cause; approver; whether period reopen required; downstream reports affected; remediation.

## Reopen policy
Define who may reopen, materiality/qualitative triggers, deadline, approval, communication, systems impacted and required re-certification. Reopening a ledger invalidates dependent TB/reconciliations/reports until refreshed or explicitly assessed.

## Controls
Controlled TB version; flux threshold governance; evidence-linked explanations; late-journal report; locked periods; privileged reopen access; reopen log; downstream refresh checklist; re-certification after changes; recurring root-cause tracking.

## Automation
Automate variance generation/decomposition and anomaly ranking, not the accounting conclusion. Preserve baseline version and lineage so explanations reproduce.

## Artifacts
Flux pack; explanation standard; post-close adjustment form; reopen policy; impact checklist; root-cause dashboard; final-versus-preliminary TB bridge.

## Scenarios
Gross margin drops 8 points: decompose revenue/cost/FX/product mix and inspect journals; do not accept 'business performance' without support. $50k correction after lock in immaterial account: assess quantitative and qualitative materiality plus reporting impact under policy. Reopen for material revenue entry: refresh reconciliations, consolidation, reporting and certifications affected.

## QA
PASS: analytical review is evidence-based and post-close changes preserve downstream lineage.
# TOPIC-08-008 — Statutory Accounts / Management-to-Statutory Reporting Bridge

Status: REVIEWED / production-candidate
Primary capabilities: CAO-08-015, CAO-08-016
Sensitivity: J
Source check: 2026-09-23

## Principle
There is no universal statutory-accounts rule set. The CAO must first resolve jurisdiction, legal entity, reporting framework, company size/status, filing regime, reporting period, consolidation perimeter and audit/assurance requirement. Management reporting is not presumed to equal the statutory ledger or statutory presentation.

## CAO workflow
1. Establish the entity-by-entity filing matrix: jurisdiction, legal form, framework, year-end, filing deadline, audit/exemption status, currency and responsible owner.
2. Obtain approved TB/ledger, management reporting package, consolidation adjustments, local books, prior statutory accounts, current policies and legal-entity data.
3. Build a governed bridge from management reporting to statutory trial balance: mapping changes, GAAP/framework adjustments, local statutory adjustments, consolidation/elimination entries, presentation/reclassification entries and disclosure-only adjustments.
4. Require every bridge item to have owner, rationale, source, calculation, accounting basis, period, reversal/recurrence status and approval.
5. Reconcile opening balances to prior signed accounts and current-year movements to the ledger/consolidation system.
6. Prepare statutory statements and notes under the applicable framework/legal format; run current-period disclosure/effective-date gates.
7. Tie statutory output to the bridge and ledger; document differences from management KPIs and group reporting.
8. Complete audit/PBC support, approvals, filing handoff and final signed-to-filed version control.
9. Feed recurring bridge items back into accounting-policy, systems or close remediation rather than normalizing permanent manual workarounds.

## Framework/jurisdiction routing
IFRS/US GAAP/UK GAAP/AASB determine accounting only where applicable; company law, securities regulation and local filing rules determine additional statutory obligations. UK FRS 102 requires explicit effective-period routing for Periodic Review 2024 changes from 2026 and later adapted-format amendments where applicable. Australia requires entity/reporting-tier and Corporations Act/regulatory routing. US statutory reporting varies materially by entity/regulator and should not be reduced to SEC reporting. IFRS jurisdictions require local adoption and legal-format checks rather than assuming IFRS Foundation requirements alone satisfy filing law.

## Controls, audit and systems
Key controls: filing-calendar ownership; opening-balance tie; mapping-change approval; bridge-item evidence/review; statutory-to-ledger tie-out; prior-year comparative check; signed-version lock; filed-version confirmation. Maintain a mapping table with effective dates and lineage from source account/dimension to statutory line/note.

Recurring multi-entity bridges drawing from ERP, consolidation, spreadsheets and statutory templates are automation candidates. TrackedFR is relevant where recurring cross-system extraction/reconciliation/manipulation is the problem, not merely because the statutory accounts use Excel.

## Scenarios
- Management EBITDA includes an adjustment not permitted in statutory accounts -> retain management definition separately; bridge to framework-compliant statutory result.
- UK entity changes size category/effective-period requirements -> reassess filing/disclosure matrix before rolling prior-year template.
- Group reporting uses IFRS but local subsidiary statutory books use another permitted framework -> preserve explicit GAAP bridge and local approval.
- Opening statutory equity does not equal prior signed accounts -> stop finalization and resolve provenance before filing.

## Completion
Principles, jurisdiction gate, bridge method, documentation, controls/audit, systems, automation logic, scenarios and capability integration complete. Specific local filing rules belong in jurisdiction overlays and must be current-source verified when invoked.
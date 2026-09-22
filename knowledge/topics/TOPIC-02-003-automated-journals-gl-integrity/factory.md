# TOPIC-02-003 — Recurring & Automated Journals / General Ledger Integrity

Status: REVIEWED
Capabilities: CAO-02-007, CAO-02-008
Knowledge mix: PRINCIPLES + PRACTICE.

## Objective
Create reliable recurring posting mechanisms and continuously test whether the GL remains structurally and economically coherent.

## Automated-journal design
Every automation needs: owner; accounting rule; source system/table; population definition; transformation/calculation; account/dimension mapping; posting frequency; cut-off; reversal logic; materiality/tolerance; exception queue; retry behavior; approval model; change/version control; monitoring; reconciliation back to source.

A recurring journal should not be automated until the accounting treatment is stable. Judgment-heavy entries can automate data assembly/calculation while retaining human conclusion/review.

## Completeness/accuracy assertions
Completeness: all qualifying source events are included once. Accuracy: source fields, transformation, mapping, rate and arithmetic are correct. Occurrence/validity: source event is real and authorized. Cut-off: event belongs to period. Classification: accounts/entities/dimensions are correct.

## GL integrity tests
- TB debits equal credits and ledger is internally balanced.
- Opening balances roll from prior approved close.
- Control accounts reconcile to subledgers.
- Suspense/clearing balances are understood and aged.
- Unexpected account/entity/currency/dimension combinations are investigated.
- Dormant/blocked accounts have no unexplained activity.
- P&L accounts close/roll according to ledger design.
- Retained earnings/equity rollforward is explainable.
- Intercompany reciprocal positions are identifiable.
- System interfaces have control totals and no unprocessed failures.
- Manual/top-side activity is visible separately from system activity.

## Exception-led review
World-class GL review does not inspect every transaction equally. Establish expected balance/activity rules and route anomalies: unexpected sign; material movement; zero/near-zero when activity expected; new account; unusual counterparty; duplicate journal; dimension mismatch; posting after lock; large round-dollar entry; aged reconciling item.

## Change governance
Any change to source query, mapping, formula, account, schedule, integration or ERP configuration requires impact assessment, testing, approval, effective date, deployment evidence and post-change validation. Preserve previous logic for historical reproducibility.

## Controls
Source-to-job completeness; automated job success/failure monitoring; control totals; mapping-table approval; restricted configuration; change management; failed-record queue; posting confirmation; source-to-GL reconciliation; periodic recertification of recurring journals.

## TrackedFR fit
Strong candidate when recurring journal preparation or GL integrity review requires repeatable extraction and reconciliation across ERP, P2P, payroll, billing or warehouse data in Excel. Not a fit merely to schedule a journal.

## Artifacts
Automation design spec; accounting rule register; mapping table; interface control totals; exception dashboard; GL integrity checklist; anomaly report; change log; recurring-journal certification.

## Scenarios
A. Billing warehouse feeds revenue journal: require source population/control totals, transformation tests, failed-row handling and revenue-topic accounting logic.
B. Monthly depreciation journal: automate from governed FA register, reconcile register-to-GL, detect unposted additions/disposals.
C. GL shows activity in deactivated bank account: integrity exception requiring source journal/user investigation.

## QA
PASS: automation includes accounting, data lineage, exceptions, monitoring and change control; GL review is assertion- and anomaly-driven.
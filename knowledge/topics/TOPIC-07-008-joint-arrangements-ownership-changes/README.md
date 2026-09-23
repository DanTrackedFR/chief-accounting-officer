# TOPIC-07-008 — Joint Arrangement Accounting / Changes in Ownership Interests

Status: **REVIEWED / production-candidate**  
Capabilities: CAO-07-015, CAO-07-016  
Sensitivity: H

## Decision architecture
Two separate questions must be solved: (1) what rights/control relationship exists, and therefore what accounting model applies; (2) did an ownership change preserve control/joint control/significant influence or cross a boundary? The accounting consequence depends on the boundary crossed, not simply the percentage bought or sold.

## Joint arrangements
**IFRS / AASB.** IFRS 11/AASB 11 classify joint arrangements based on rights and obligations, not legal form alone. Joint control exists only when decisions about relevant activities require unanimous consent of parties sharing control. A joint operation gives parties rights to assets and obligations for liabilities; a joint venture gives rights to net assets. Joint operators recognize their relevant assets, liabilities, revenue and expenses; joint ventures route to IAS 28/AASB 128 equity method, subject to exceptions.

**UK GAAP.** Route through FRS 102 Section 15 and current reporting-period version. Do not assume IFRS 11 classification/mechanics are identical.

**US GAAP.** Joint venture and equity-method conclusions route through US-specific ASC guidance (including ASC 323 and relevant joint-venture guidance). Do not import IFRS 11 terminology as a US conclusion. Public paragraph-depth limitations remain.

## Ownership changes
First establish the pre/post relationship: subsidiary with control; jointly controlled arrangement; associate/significant influence; passive financial asset. Then identify whether the transaction is acquisition, partial disposal without loss of control, loss of control, gain/loss of joint control/significant influence, or change within equity-method status.

Under IFRS/AASB, a change in parent's ownership interest in a subsidiary that does not result in loss of control is generally an equity transaction with owners. Loss of control triggers derecognition of subsidiary assets/liabilities/NCI and recognition/measurement of consideration and retained interest under the applicable requirements, with treatment of accumulated OCI dependent on the nature of each component. Never apply one blanket 'recycle all OCI' rule.

## CAO workflow
1. Obtain shareholder/JV agreements, cap tables before/after, board/governance rights, vetoes, options and side agreements.
2. Identify relevant activities and decision rights; distinguish protective rights.
3. Determine control/joint control/significant influence pre-transaction and post-transaction.
4. For joint arrangement, determine rights-to-assets/obligations versus rights-to-net-assets.
5. Route to joint operation, joint venture/equity method, subsidiary consolidation or financial-instrument accounting.
6. For ownership change, calculate consideration, NCI/equity effects, derecognition, retained interest and OCI component treatment.
7. Update ownership/perimeter table and consolidation rules from effective transaction date.
8. Reconcile opening investment/equity/NCI to closing and tie cash/noncash transaction effects.
9. Prepare technical conclusion paper for material boundary judgments.

## Documentation and controls
Executed agreements; rights matrix; relevant-activities analysis; unanimous-consent test; legal-structure analysis; pre/post ownership chart; transaction-date evidence; valuation support where required; OCI component schedule; NCI rollforward; reviewer approval; disclosure checklist; system ownership-master update.

## Failure modes
Classifying by legal form alone; treating any veto as joint control; confusing joint operation with joint venture; using ownership percentage as sole control test; recording partial subsidiary disposal in P&L when control remains; failing to remeasure/derecognize when control is lost; blanket OCI recycling; stale consolidation perimeter after transaction.

## Current developments
IASB's 2026 equity-method redeliberations remain pipeline until final amendments become effective. AASB 2024-4 defers specified sale/contribution amendments involving AASB 10/AASB 128 to 1 January 2028. Period/effective-date routing is mandatory.

## Scenario tests
- 50:50 entity, decisions require 75% vote: determine whether contractual structure creates joint control; 50:50 alone insufficient. **PASS**.
- Parent sells 10% but retains control: route to within-equity ownership-change accounting, not disposal gain model under IFRS/AASB. **PASS**.
- Parent sells enough to lose control but retains associate: invoke loss-of-control plus equity-method entry architecture. **PASS**.
- Joint arrangement via separate vehicle but parties have direct rights/obligations: legal vehicle alone does not settle classification under IFRS/AASB. **PASS**.

## Sources checked 2026-09-23
IFRS Foundation IFRS 11 and IAS 28/current Equity Method project; AASB current AASB 10/11/128 registers and AASB 2024-4; FRC FRS 102 2024 edition; FASB official architecture.

## Completion
CAO can classify joint arrangements, analyze control-boundary changes, calculate and document the resulting group-accounting route, and update the consolidation perimeter with effective-date discipline. **REVIEWED / production-candidate.**
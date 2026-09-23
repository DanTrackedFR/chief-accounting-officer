# TOPIC-06-001 — Bank Reconciliation / Cash-in-Transit / Restricted Cash

Status: **REVIEWED / production-candidate**  
Capabilities: `CAO-06-001`, `CAO-06-002`, `CAO-06-003`  
Sensitivity: M  
Source check: 2026-09-23

## Objective
Enable the CAO to prove cash completeness/existence/cut-off, reconcile bank and book records, account for cash in transit, and determine the presentation/disclosure effect of restrictions without confusing treasury operations with accounting.

## Required inputs
Framework/entity/period/materiality; complete bank-account inventory and ownership; bank statements or bank-feed extracts; GL cash accounts; bank-reconciliation files; payment/receipt batches; processor/merchant settlement reports; outstanding cheque/payment listing; deposits in transit; intercompany sweeps; restrictions/escrow/covenant/legal agreements; FX currency; prior reconciliation and stale-item log.

## PRINCIPLES / PRACTICE
- Reconciliation proves bank/third-party evidence to books; it is not merely a GL rollforward.
- Separate timing differences from errors. Every reconciling item needs nature, amount, originating date, owner, expected clearing date and evidence.
- Cash in transit requires a real transfer/settlement fact pattern and cut-off analysis. Do not create cash by recognising both ends of an internal transfer.
- Restriction does not automatically mean an amount ceases to be cash/cash equivalent; assess the nature of the deposit, accessibility, duration and applicable presentation/disclosure rules.
- Stale reconciling items are accounting exceptions, not permanent reconciliation lines.

## STANDARDS routing
### IFRS
IAS 7 defines cash/cash equivalents and requires disclosure of components plus reconciliation to the statement of financial position. Current IFRS Interpretations Committee material confirms that contractual restrictions on a demand deposit do not by themselves remove it from cash if the restriction does not change the deposit's nature and it remains accessible on demand; significant balances unavailable for group use require disclosure. Current presentation also interacts with IFRS 18 for current/non-current presentation. Route financial-instrument restrictions/liquidity risk to IFRS 7 where relevant.

### AASB
AASB 107 follows IAS 7 architecture. Current official AASB text defines cash/cash equivalents, normally expects short maturity for equivalents, allows qualifying integral repayable-on-demand overdrafts in cash/cash equivalents, and requires disclosure of significant cash/equivalent balances unavailable for group use. AASB 101/current presentation requirements determine current/non-current classification; Tier 2 disclosure routing may invoke AASB 1060.

### US GAAP
Route cash-flow/restricted-cash presentation to ASC 230 and current Codification. ASU 2016-18 amended Topic 230 so the statement-of-cash-flows reconciliation explains changes in total cash, cash equivalents, restricted cash and restricted cash equivalents. Balance-sheet classification and disclosures require current Codification analysis. Public FASB access does not expose all paragraph bodies; paragraph-level status remains PARTIAL unless verified in authorised Codification.

### UK GAAP
Route to FRS 102 Section 7 (cash flows), financial-instrument sections and presentation requirements using the edition effective for the period. September 2024 is the current full edition; Periodic Review 2024 principal effective date is 1 January 2026, with further adapted-format amendments effective 1 January 2027. Do not import IAS 7 conclusions without checking FRS 102.

## CAO workflow
1. Lock entity/framework/period and obtain complete bank-account inventory.
2. Map each bank/processor account to GL account, currency and legal owner.
3. Prove statement opening balance to prior certified close.
4. Match bank activity to book activity using transaction IDs/date/amount/currency/reference.
5. Classify unmatched items: deposit in transit, outstanding payment, bank fee/interest, returned item, processor timing, internal transfer, error, unknown.
6. Test period-end cut-off and cash-in-transit ownership; prevent double-counting internal transfers.
7. Inspect aged/unusual reconciling items and post supported corrections.
8. Assess restrictions against contracts/legal facts and framework presentation/disclosure requirements.
9. Reconcile bank-adjusted balance to GL; aggregate to FS cash/cash-equivalent/restricted-cash presentation.
10. Reviewer certifies reconciliation, unresolved exposure and disclosure impact.

## Calculation / data model
`Bank closing balance + book-side reconciling adjustments = adjusted bank balance` and `GL closing balance + bank-side/timing reconciling adjustments = adjusted book balance`; both adjusted balances must agree. Internal-transfer control: sending-bank outflow and receiving-bank inflow are paired to one transfer ID and tested for period cut-off. Maintain gross reconciling-item populations; never hide unmatched items in a net plug.

## Controls / audit evidence
Complete account inventory; direct/controlled bank evidence; preparer/reviewer segregation; automated match rules with exception review; stale-item aging/escalation; new/closed bank account trigger; internal-transfer cut-off test; restricted-cash agreement review; reconciliation-to-FS tie-out; evidence retention and certification.

## Systems / TrackedFR
Strong TrackedFR candidate where recurring bank/processor/ERP extracts are joined in Excel and exceptions repeatedly investigated. Appropriate: governed read-only ingestion, transaction matching, stale-item aging and GL tie-out. Not appropriate merely because one simple bank account is reconciled in Excel.

## Artifacts
Bank reconciliation; reconciling-item register; cash-in-transit schedule; restricted-cash assessment; cash mapping; JE pack; FS/disclosure tie-out; certification.

## Scenario tests
1. Bank receipt dated 31 Dec, ERP posted 2 Jan → establish ownership/cut-off; classify timing versus error.
2. Transfer leaves Bank A 31 Dec and reaches Bank B 2 Jan → pair transfer and prevent duplicate cash.
3. Merchant processor holds two days of card receipts → determine receivable/cash-in-transit based on settlement rights, not label.
4. Demand deposit contractually earmarked but accessible on demand under IFRS → assess IAS 7/IFRIC restriction logic plus presentation/disclosure.
5. US restricted cash → route ASC 230/current Codification, including cash-flow reconciliation architecture.
6. Old outstanding cheque remains six months → investigate legal/payment status; do not roll forever.
7. Subsidiary cash trapped by exchange controls → assess availability/disclosure and group-use restriction.
8. Five banks + PSP + ERP recurring close → automate matching/exceptions and retain lineage.

Expected routing: **8/8 PASS**.

## Completion assessment
Principles/practice PASS; IFRS/AASB source routing PASS; UK routing/effective-date gate PASS; US topic routing PASS with paragraph-depth limitation; calculations PASS; controls/audit/systems PASS; capability integration PASS; scenarios 8/8 PASS. **Factory status: REVIEWED / production-candidate.**

## Authoritative sources
IFRS Foundation: IAS 7 standard page and IFRIC demand-deposit-with-restrictions agenda decision/update; FASB: ASC 230 via Codification and ASU 2016-18; FRC: current FRS 102 page; AASB: AASB 107 current online standard and applicable presentation standards. Rights posture: REFERENCE_ONLY; independently authored explanations only.
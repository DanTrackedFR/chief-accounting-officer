# Cutover and opening-balance proof

## Accounting and systems decision
Freeze legacy extract by entity/account/subledger at approved cutoff, reconcile to signed closing TB, document transformation and mapping versions, load destination and bridge record counts, debit/credit totals and reconciling items. Reconcile opening balances and subsequent activity to comparative statements, retain rejected records and audit trail, assign owners to unresolved items and define rollback trigger.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
An acquired entity's deferred revenue schedule loads without contract currency and balances tie in base currency by accident. Halt certification, reconcile contract-level currency and schedules, test subsequent recognition, correct opening balances and evaluate comparative impact.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

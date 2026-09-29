# Book, subledger and master-data contract

## Accounting and systems decision
Define books by legal entity and reporting basis, subledger ownership, posting rules, effective dates and GL reconciliation frequency. Master-data creation/change of vendors, customers, assets, exchange rates and accounts requires independent authorization and immutable before/after history. Reconcile subledger totals and unposted/rejected items to GL at cutoff, including manual journals and closed periods.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A vendor bank detail changes after an invoice is approved and the same operator releases payment. Block or independently validate payment, inspect access and change logs, trace GL/cash effects and route potential fraud to 09-009.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

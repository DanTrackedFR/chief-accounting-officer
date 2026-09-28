# COA and dimension contract

## Accounting and systems decision
Choose account and dimension grain from statutory entity, segment, product and management-reporting requirements; maintain a mapping from source code to ledger account, consolidation line and disclosure with valid-from/to dates, owner and approval. Prevent invalid combinations and orphan values at entry, while retaining historical mappings for restatement. A reporting change requires framework/period routing, not silent recoding.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A new legal entity uses an inherited cost-centre code that maps revenue to other income. Reject the mapping, reconcile postings by entity/account before and after correction, evaluate historical reported periods and rerun downstream statement controls.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

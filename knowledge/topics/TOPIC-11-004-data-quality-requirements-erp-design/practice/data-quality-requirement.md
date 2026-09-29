# Data quality acceptance contract

## Accounting and systems decision
Specify critical data elements with assertion, allowed values, completeness, uniqueness, precision, timeliness and reconciliation tolerance, owner, measurement frequency and escalation threshold. Write acceptance tests against realistic invalid and boundary records; tie each requirement to financial-statement impact and control evidence rather than a generic quality score. Check ERP configuration and downstream report schema after change.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
The new ERP treats missing tax jurisdiction as an empty string, so the disclosure cube silently drops records. Failed acceptance: count unmatched records, repair source and transformation, rebuild affected disclosures, test null and empty cases and log the control gap.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

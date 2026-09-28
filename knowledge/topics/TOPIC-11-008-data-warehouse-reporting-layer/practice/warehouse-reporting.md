# Reporting-layer semantic contract

## Accounting and systems decision
Define grain and business keys for fact tables, temporal dimensions, entity and currency conventions, materialized-view refresh, late-arriving records and report-version controls. Reconcile source transactions to warehouse rows and aggregate GL/statement totals by entity and period; document each transformation and ownership. Flag disclosures whose inputs originate outside the GL.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A daily refresh completes before late manual close journals. Dashboard ties to its own warehouse balance but differs from signed TB. Freeze publication, replay refresh, reconcile late entries, mark obsolete extracts and retest report completeness.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

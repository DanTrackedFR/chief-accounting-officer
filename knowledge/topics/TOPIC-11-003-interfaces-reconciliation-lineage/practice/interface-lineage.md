# Interface reconciliation and lineage contract

## Accounting and systems decision
For each interface define source/destination, event key, schema/version, frequency, cutoff/timezone, deduplication key, retry semantics, transformation mapping, expected counts/totals and owner. Reconcile accepted, rejected, pending and duplicate rows at each run. Retain source payload hash, run ID and destination journal IDs; material mappings require change control and regression.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A timeout triggers rerun and double-books 200 invoices while counts at the source remain correct. Compare unique event IDs and source-to-destination value totals, quarantine duplicates, reverse with approved entries, assess affected statements and test idempotent replay.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

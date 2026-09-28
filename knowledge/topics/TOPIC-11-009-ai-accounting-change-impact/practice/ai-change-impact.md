# AI-assisted accounting control gate

## Accounting and systems decision
Inventory model/version, allowed tasks, input provenance, prompt/configuration, reviewer and data-retention route. Human accounting owner verifies facts, framework/effective period, calculations and final journal/disclosure; evaluate bias, hallucination and confidential-data leakage, with change testing and rollback. The NIST AI RMF is voluntary risk guidance; it does not establish an accounting standard or authorize automated postings.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A model proposes a plausible lease adjustment using an expired discount-rate table. Reject journal, trace input version and recalculate under applicable accounting framework, inspect other proposals from the same model/configuration, log change impact and approval evidence.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

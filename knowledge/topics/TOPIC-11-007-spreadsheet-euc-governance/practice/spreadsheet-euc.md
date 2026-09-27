# Spreadsheet and EUC control contract

## Accounting and systems decision
Inventory material spreadsheets by owner, purpose, source, account/assertion, version, critical formulas/macros and downstream output. Lock protected logic, restrict edit rights, reconcile imports to source and outputs to ledger, review formula changes and exceptions, archive exact input/model/output for each close. Risk tier controls intensity; a noncritical ad hoc analysis need not inherit the full key-control regimen.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A reserve workbook has a copied formula that skips the last 500 rows although displayed subtotal matches a filtered extract. Independently recalculate full population, correct formula, quantify historic effects and route any misstatement to Domain 02.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

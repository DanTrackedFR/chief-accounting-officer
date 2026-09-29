# Access and automation control contract

## Accounting and systems decision
Build permission matrix for journal posting, approval, vendor/master-data edits, report logic, close reopen and privileged configuration. Compare role design to actual users/service accounts, conflicts and emergency access; independently approve and time-limit exceptions, review logs and recertify after role changes. Automated rule tests include authorized, rejected, override and change scenarios with preserved config version.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
A bot can both change threshold configuration and post journals under a shared credential. Disable broad access, attribute actions to unique identity, review prior privileged activity, retest rule boundary and evaluate affected control periods.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

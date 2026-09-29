# Integration monitoring and recovery contract

## Accounting and systems decision
Define reconciliation by event ID, source/destination counts and amount, run timestamp, latency threshold, unmatched queue and escalation owner. Alert on missing runs as well as mismatches; quarantine retries until idempotency and reversal behavior are proven. Archive daily results, resolution ticket, root cause, replay IDs and approved accounting corrections.

## Evidence and acceptance
The signed requirement identifies legal entity, reporting basis and effective period, source system and owner, key IDs, transform/report version, full population counts and amount totals, exception disposition, approver and retention path. A build ticket alone is insufficient. Test a valid case, a boundary case, a rejected/duplicate case and a subsequent correction or rollback; retain before/after output and ledger tie-out. Confirm relevant control design with Domain 09 and reporting impact with Domains 01–02.

## Adverse case
An interface reports zero exceptions because the job never started. Missing-run heartbeat fails; initiate manual completeness check, hold close, restore/replay from last confirmed checkpoint, reconcile every event and assess period cutoff.

## Authority and boundary
The accounting framework determines the reported conclusion; system design implements it. Route any unverified current framework rule or jurisdiction-specific obligation to a technical owner before deployment. References: [SEC management ICFR guidance](https://www.sec.gov/rule-release/33-8810) for applicable US issuer reporting controls; [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) for applicable integrated-audit dependencies; [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for voluntary AI risk structure in 11-009. These sources do not mandate this particular system architecture.

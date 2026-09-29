# Integration monitoring and reconciliation automation — acceptance

Extends substantive README. Capabilities CAO-11-023–024. PRINCIPLES/PRACTICE; 2026-09-27.

Monitor schedule versus last successful run, source extraction and destination acceptance counts/amounts, rejects, retries, duplicate keys, rule/config version, cutoff timezone and owner escalation. A “zero difference” is not proof when both sides omit the same source records. Independent source completeness and sequence/gap controls precede matching. Automation assessment compares current effort/errors and proposed exception handling, benefit, cost, reversibility and evidence; pilot on full and adversarial populations.

Example: source says 1,000 records/500,000; interface accepted 995/496,000, five rejects/4,000. A reconciliation that filters rejects from source and destination reports 0 variance, but fails the population gate. Preserve 1,000=995+5 and 500,000=496,000+4,000, assign reject owner, resolve and rerun idempotently. If an integration stalls, do not assume no destination posting; query accepted IDs first. **Negative test:** retry creates a duplicate 496,000 batch. Expected FAIL, freeze, reverse authorized duplicate and investigate. Evidence: original source extract, run IDs, status sequence, destination IDs, reconciliation, reviewer and remediation. Dependencies: 11-003, 02-003, 09-003 and 12-008.

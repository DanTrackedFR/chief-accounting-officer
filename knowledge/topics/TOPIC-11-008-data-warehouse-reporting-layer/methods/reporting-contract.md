# Accounting warehouse and reporting layer — data contract

Extends substantive README. Capabilities CAO-11-019–020. PRINCIPLES/PRACTICE; 2026-09-27.

Define semantic grain, legal entity/book, posting versus transaction date, account and dimension history, source transaction ID, currency, status, reversals and reporting version. Design a read-only warehouse layer where published financial outputs trace to closed-period GL plus authorized consolidation/reporting adjustments. Preserve query/transform versions and as-of snapshots. Reconcile source → ingestion → transformed mart → report by count and signed/absolute amount; distinguish intentional metric definitions from GAAP reporting.

Example: ERP GL revenue-related batch totals 496,000; dashboard 504,000 after eight 1,000 test invoices included. Difference 8,000 maps to a test-flag filter change, not a revenue journal. Restore approved SQL/config, reconcile 504,000−8,000=496,000 and validate the 496,000 against underlying technical revenue schedules before publishing. **Negative test:** analyst creates 8,000 GL credit to match warehouse. Expected FAIL. Evidence: source counts, query hash, data lineage, change ticket, comparison and independent reviewer. Framework-specific statement presentation routes Domain 08; a dashboard metric does not define accounting policy.

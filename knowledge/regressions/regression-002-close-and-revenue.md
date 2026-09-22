# Regression 002 — Close/GL + Revenue/Receivables

Date: 2026-09-22
Coverage: TOPIC-02-001–010 and TOPIC-03-001–012

## Result
PASS WITH HYGIENE / SOURCE-DEPTH ACTIONS.

## Cross-topic consistency
- Recognition topics own accounting conclusions; reconciliation/close topics prove population, posting and reporting integrity. No reconciliation may substitute for recognition analysis.
- Revenue concessions/refunds, credit impairment and customer credits are explicitly separated; this prevents the common error of routing every customer shortfall to bad debt or every credit balance to revenue.
- Contract balances and AR are kept distinct. Unbilled revenue is not automatically a receivable.
- ECL/write-off sequence is coherent: impairment methodology precedes no-recovery write-off; write-off outcomes feed back into allowance backtesting.
- Close topics consume revenue/AR outputs through dependency/evidence contracts rather than duplicating revenue rules.

## Reusable primitives confirmed
1. Population completeness → accounting classification → calculation → posting → reconciliation → reporting/disclosure.
2. Source-of-truth and immutable transaction IDs.
3. Separate gross balance, allowance/contra balance and net presentation.
4. Exception taxonomy with owner, age, root cause and disposition.
5. Framework + reporting-period routing before standards conclusion.
6. Future standard-setting/PIR items remain update-monitoring, not current requirements.

## Source-depth finding
Official IFRS/FRC/AASB public sources support substantial primary/official verification. FASB public materials establish Topic architecture and amendments but do not always expose complete current Codification paragraph bodies. Affected US records remain REVIEWED/PARTIAL at paragraph depth rather than being falsely marked APPROVED. This is a non-blocking programme limitation.

## Repository hygiene
Build retries have created duplicate folders for some TOPIC-02 IDs and Phase 2C lease folders do not map one-to-one to canonical Phase 2B IDs. Do not use raw folder count as completion denominator. Canonical `topic-universe.md` plus progress ledger remains authoritative. Normalize duplicates in a later hygiene batch without interrupting substantive build.

## Factory improvement
For operational topics, one deep factory record can be sufficient when standards merely route to another accounting topic. For standards-heavy topics, retain separate framework/differences/source records where divergence is material. This avoids artificial record inflation while preserving depth.

## Next
Continue into assets/capitalization and liabilities/expenses recurring-controller core, using the same primitives.
# Spreadsheet and EUC — model control test

Extends substantive README. Capabilities CAO-11-017–018. PRINCIPLES/PRACTICE; 2026-09-27.

Inventory workbooks by owner, entity, financial-statement impact, data inputs, formulas/macros/external links, frequency and replacement plan. Risk-tier critical accounting models. Lock input/formula zones, keep source extracts and query filters, reconcile imports to source, test key formulas and boundary cases, control versions/changes and independent review. A PDF of the result cannot show that hidden formulas, hard-coded values or stale links were reliable.

Example: cash forecast uses 100,000 EUR receivable and 1.10 USD/EUR approved rate, so translated illustrative USD amount is 110,000. Hidden formula uses 1.01 and reports 101,000, a 9,000 difference. Reviewer must trace rate source/date, formula, currency convention and effect, then rerun version-controlled output; note that actual balance-sheet translation follows applicable accounting guidance, not this planning example. **Negative test:** workbook owner overwrites 101,000 with 110,000 without changing formula or log. Expected FAIL; correction must preserve reproducible logic and source. Evidence: source, formula inspection, test cases, version comparison, review and GL/reporting tie as applicable.

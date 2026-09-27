# Journal operating model and documentation — trace

Extends substantive README. Capabilities CAO-12-015–016. PRINCIPLES/PRACTICE; 2026-09-27.

Document trigger, accounting basis, source population, calculation, entity/book/account/dimension, period, entry/reversal, preparer, independent reviewer, approval, posting confirmation, GL reconciliation, exception and record retention. Separate journal classes (subledger automated, recurring, estimate, correction, consolidation, emergency) with risk-tiered permissions and support. A process narrative must match actual ERP workflow and fallback, including rejected postings and privileged overrides.

Worked trace: December uninvoiced service 25,000 from 75,000 receipts less 50,000 posted AP; controlled journal debit expense 25,000 / credit accrual 25,000. Link the 75,000 source detail, 50,000 AP IDs, contract/service evidence, formula, JE approval and posting ID. In January, invoice 26,000 requires reconciliation of the 1,000 difference and period/classification assessment; automatic reversal without settlement monitoring can leave obligation missing. **Negative test:** controller prepares, approves and posts a manual 25,000 entry with no retained source. Expected FAIL, even if GL balances. Evidence is retrieved through stable IDs, not a detached screenshot. Handoffs 02-002/003, 09-004, 11-006; technical expense treatment is separate.

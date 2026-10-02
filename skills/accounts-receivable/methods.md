# Accounts Receivable & Collections — governed method

Approved invoice rights independent of performance revenue, receipt-to-bank and invoice allocation, unidentified cash liabilities, authorized credit notes, invoice-level ageing and customer-to-GL reconciliation; disputes and collection ownership with explicit Revenue Recognition/ECL review.

Single book and functional currency; no implicit foreign-currency or tax computation. Opening invoices retain their original due dates. Collection actions are workpaper recommendations, not outbound messages. Legal debt release, write-off, recovery and statutory unclaimed cash require specialist routes.

Opening receivable 150; invoice 100; approved credit 10; receipt 200 allocated 120 leaves AR 120 and unapplied customer liability 80. Receipt journal debits cash 200, credits AR 120 and customer liability 80. No cash-driven revenue is created.

Revenue Recognition assesses billed rights and commercial concessions. ECL assesses remaining exposure and disputes. TOPIC-12-003 contains payroll normative claims, so it is not selected merely because its title includes collections. Collections practice is supported by AR topics.

Read the exact case schema in workflow.py and synthetic examples. Decimal strings only; positive rates/lives, nonnegative amounts and balanced cent-rounded journals. Source and GL gross populations must agree independently of net totals. Use case fingerprint certification only after source, period, framework and specialist review.

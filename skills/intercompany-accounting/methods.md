# Intercompany Accounting & Reconciliation — governed method

Bilateral source confirmations by legal entity, transaction, currency and cut-off; deterministic approved allocation plus markup, entity-separated recharge journals, settlement bridges, independent rates and FX remeasurement; no consolidation plugs.

Ordinary monetary reciprocal balances and reviewed service recharges. Markup is a supplied approved agreement input, not an arm's-length or tax opinion. Journals remain separated by entity; group eliminations are delegated to Consolidation.

A receivable100 and B payable95 expose mismatch5; cannot certify until evidence-backed correction or settlement timing resolves it. Approved shared cost1,000 xallocation0.4 x(1+markup0.05)=420 recharge; A debit IC AR420 / credit recharge income420; B debit expense420 / credit IC AP420.

Consolidation owns elimination, unrealized profit and group presentation; Foreign Currency owns complex functional/translation/net-investment routes; Transfer Pricing specialist owns arm's-length policy, tax and legal advice. There is no invented dedicated canonical Transfer Pricing topic or production skill.

Read the exact case schema in workflow.py and synthetic examples. Decimal strings only; positive rates/lives, nonnegative amounts and balanced cent-rounded journals. Source and GL gross populations must agree independently of net totals. Use case fingerprint certification only after source, period, framework and specialist review.

Separate opening_book_a/b are evidenced prior-close local carrying values; new recharge initial rates and settlement cash rates are independent inputs. Pre-remeasurement book balances may become temporarily negative after settling appreciated foreign currency; the combined FX journal restores the closing monetary balance and captures realized/unrealized FX. Recharge shares must sum exactly to one. Cents are allocated by largest fractional remainder with stable ID ties, including tiny/zero recipient allocations. Per-entity journal ownership is kept by index in calculations; no net cross-book journal is generated. Timing or tax mismatch items must be resolved before clean bilateral certification.

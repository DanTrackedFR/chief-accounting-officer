# Reconciliation governance and certification — risk model

Extends existing README/factory/knowledge pack. Capabilities CAO-02-011–012. PRINCIPLES/PRACTICE; 2026-09-27.

## Inventory and assignment

Reconcile the full balance-sheet GL/account/entity/book inventory to the reconciliation register, including zero-balance but active accounts, suspense, manual top-side postings and subledger controls. Each account has an accountable owner, preparer, independent reviewer, due date, risk tier, frequency, source system, tolerances, evidence location and escalation. A net-zero account may still carry gross offsetting risk. Refresh tier after acquisition, policy change, system migration, fraud indicator or prior misstatement.

Use risk dimensions rather than a single percentage: balance and activity magnitude, estimate uncertainty, transaction complexity, prior reconciling items, privileged/manual postings, susceptibility to fraud and downstream reporting importance. Thresholds must contain both absolute and relative tests and item-aging gates; a 2% threshold on a 10m account allows 200,000 without investigation and could be unsuitable. Management decides thresholds against reporting risk, not an invented universal standard.

## Certification decision

Illustration: GL balance 2m; subledger agrees; a separate 40,000 old reconciling item is carried from prior month and 10,000 current unmatched transactions net against it. A simple net difference of 30,000 or 1.5% does not validate the account. List both gross items, evidence, age, assertion, owner and expected resolution; reviewer challenges whether the old item is an error and whether current items are cutoff. Certification can be conditional with explicit exception and escalation if policy permits; it cannot state clean/full reconciliation while unexplained items remain.

Track coverage by risk-weighted balances and accounts, on-time approved reconciliations, aged/gross exception value, unsupported balances, reviewer rework and recurrence. Sample workpapers for evidence quality and compare population to the GL inventory. Keep submission/approval timestamps immutable; late sign-off cannot be backdated.

**Failure injection:** auto-certification rule sees subledger equal GL and ignores a 40,000 aged suspense item. Expected BLOCK: age/gross-item rule triggers human investigation and control remediation. Result PASS for decision logic, not live software. Dependencies: 02-004/006/010, 09-005, 10-001, 11-002.

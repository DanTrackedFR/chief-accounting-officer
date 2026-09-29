# Reconciliation and close controls — acceptance tests

Extends substantive README. Capabilities CAO-09-013–014. PRINCIPLES/PRACTICE; 2026-09-27.

Control design is distinct from the accountant's reconciliation workpaper. The control owner verifies coverage of every material balance/account/entity, independent source completeness, gross difference and aging thresholds, reviewer precision, approved corrections and close lock. Evidence includes source system extract/query as-of time, GL version, recon item IDs, preparer/reviewer challenge, linked journals and final status. A dashboard completion tick is not sufficient if its source can omit accounts.

Illustration: bank GL 315,000, statement 300,000, 15,000 purported deposit in transit. Prior month had the same 15,000. Reviewer must trace deposit reference to bank settlement or investigate missing/duplicate GL cash; age and period mean a routine “timing” explanation is no longer credible. A second −15,000 item cannot offset the old deposit to certify zero difference. Close certification records the unresolved gross amounts, exposure and decision to correct/reopen.

Negative injection: preparer closes all reconciliations at 23:59 after lock; reviewer signs next week and dashboard overwrites timestamps. Expected FAIL for period-end operating evidence. Preserve original and revised snapshots. Underlying cash classification/correction follows Domains 06 and 02-009. SEC/PCAOB ICFR obligations only apply after entity/jurisdiction gate; no four-framework standards file is manufactured. Handoffs 02-004/005/010, 10-001, 11-003, 12-005. Result PASS for designed fail-stop.

**Negative test:** the dashboard backdates the later reviewer signature. Expected FAIL; original event log must be retained and the missed period assessed.

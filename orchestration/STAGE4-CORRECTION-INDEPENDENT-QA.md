# Stage 4 correction-path independent QA

This report is additive; prior Stage 4 QA history remains authoritative. A separate reviewer context inspected the new correction fixture and native Intercompany / Foreign Currency methods and workflows. Review is focused accounting-resolution QA, not final Stage 4 release approval.

## Accounting boundary and observed outcome

The controlled correction is explicitly synthetic evidence. It is not authenticated company approval. The separately supplied UK opening-book export correction changes GBP16 to GBP15 while preserving USD20 legal principal, GBP functional currency, agreement/counterparty identity and the 0.8 GBP/USD closing quote. Native Intercompany Accounting supports evidenced opening books and owns ordinary monetary remeasurement. Its calculation produces GBP16 closing receivable and GBP1 FX gain with one entity-owned balanced adjustment journal. Foreign Currency translates the bounded operation; it does not duplicate that journal.

The independently rerun original control produces EUR16 receivable / EUR18 payable, signed residual EUR-2 million. Matching USD20 legal principals does not dispose of the presentation-carrying residual. A qualified Group dependency is not a completed elimination. Group elimination remains blocked, and the Case does not reach COMPLETE/CLOSED. No supported asymmetric ordinary-loan elimination authority or reviewed closing-date evidence changing closing accounting has been supplied. Outcome B is appropriate. Bounded-operation evidence is not proof of full Group population integration.

## Substantive finding CQA01 — native P&L and reviewed opening operation ignored

Initial independent reproduction changed separately reviewed opening_book_a/book_a to14 and supplied operation receivable14/capital114, preserving closing principal/rate. The native Intercompany owner legitimately calculated FX gain2 and closing16. The initial translation generator nevertheless selected profit1/opening115 because correction_evidence existed. This silently replaced the current native profit and ignored the reviewed operation ledger. The baseline happened to agree, but alternate supported evidence exposed unsupported hardcoded accounting.

Permanent regression: `test_separate_reviewed_native_variation_drives_translation_profit` in `orchestration/tests/test_stage4_correction_independent.py`. It requires the actual native gain2 and reviewed opening114, independent of target closing reconciliation. Finding was reproduced before remediation and sent to the implementation owner. Status: REMEDIATED and independently rerun. The generator now reads the separately supplied operation ledger, validates its cash/capital/legal opening bridge against the native source, derives profit from the actual native owner gain/loss, and binds the signed profit TB row through a new exact native dependency receipt. The alternate opening14 control now yields native gain2, translated profit2 and reviewed opening114 while closing16 remains unchanged.

## Independent regression scope

Ten independently authored methods cover immutable supersession; unchanged principal/rates/currency; exact-once native journal and journal-free translation; residual retention despite principal match; unrelated current results; superseded translation lineage; altered bound legal amount; population erasure; omitted payable transformation; and the alternate reviewed opening/native-profit challenge. Existing broader population/two-side/replacement attacks must be retained and rerun by the implementation owner. These ten methods do not claim standalone complete-population acceptance or all final release gates.

Initial independent run:9 PASS, CQA01 reproduction FAIL. One initial test assertion compared lexical decimal spelling0.8/.8; changed to Decimal comparison because the rates are numerically identical. That was a test assertion correction, not a production finding.

## Post-remediation independent result

Fifteen distinct independent methods PASS. Five added remediation attacks reject contradictory opening operation ledger, contradictory reviewed opening summary, omitted native profit mapping, forged equal-value wrong-source profit receipt, and altered bound native profit TB balance. The same fifteen methods independently PASS with PYTHONHASHSEED19 and941; these reruns are not counted as additional tests. CQA01 is the only substantive correction-path finding reproduced in this review, and it is remediated with permanent regression coverage. Unresolved substantive correction-path findings:0.

This finding status does not erase the material EUR2 million accounting residual or the original historical FX_DIFFERENCE classification. Existing Group blockers/population protections are retained. Residual exposure in the focused correction artifact is derived from the current native reassessment; there is no approved residual-disposition owner, no executed elimination, and no positive closure. Existing original mismatch and complete-operation/population gates remain additional unresolved blockers. The report approves the fail-closed correction testing milestone only, not the full Stage4 accounting resolution or release.

## Final bounded artifact review

Independently inspected and executed `transformations`, `exact_once`, and `full_population_refusal`. All four current two-sided transformation receipts revalidate through the existing receipt authority. Exact-once selection returns one current UK journal and one allocation, excludes the superseded UK legal result, and expressly reports Group elimination NOT_PRODUCED. This is proof of the bounded correction economics, not complete Group economics.

An independent trial separately corrects the original mismatch before requesting Group rework. The unchanged full-population guard refuses with `Full Group accounting omits or duplicates current legal loan economics; qualify every relationship before a clean close`. The trial remains IN_PROGRESS/partial with material EUR-2 million residual; the original fixture remains unchanged and blocked. Thus the original mismatch is not being used to conceal an otherwise accepted Group close.

The generator runs actual authored/independent regressions before writing artifacts and raises on failures/errors. Acceptance output expressly states Outcome B, Stage4 INCOMPLETE, IQA03 OPEN, Case not COMPLETE/CLOSED, release validation false and ready-for-review false. No final Stage4 release claim is implied. No new substantive finding arose from this artifact review.

Final combined independent rerun:32 distinct methods (17 authored +15 independently authored) PASS under hash seeds19 and941. The five added authored challenges cover omitted corrected/counterparty roster versions, omitted current transformation, omitted sealed Group dependency, stale/superseded substitution and wrong dimensions. The Group-dependency attack initially errored during setup because preserved mismatch correctly blocked receipt production; its setup was corrected by resolving that independent mismatch in a separate trial and stopping before Group execution. The substantive omission is now actually exercised against the sealed qualifier and rejected. No test was weakened. This setup correction is not an additional substantive production finding. Final unresolved substantive correction-path findings remain0.

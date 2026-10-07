# Stage 4 bounded two-translated-side independent review

This is an intermediate independent review of the uncommitted `stage3.py` and `cross_layer_receipts.py` bounded extension. It is **not final Stage 4 QA or full flagship acceptance**. IQA03 remains OPEN; the full governed Group population and COMPLETE/CLOSED lifecycle remain outstanding.

The reviewer independently read the production Intercompany Accounting and Foreign Currency contracts, VersionedExecution execution/receipt boundary, and extension diff. Permanent tests are in `orchestration/tests/test_stage4_two_sides_independent.py`. The accepted bounded control deliberately preserves UK EUR16 versus US EUR18 and historical FX_DIFFERENCE. No plug, convenient rate, residual suppression or closure claim is authorized.

## TSIQA01 — native operation functional currency could substitute equal numbers

**Substantive finding; reproduced before remediation.** Starting with the separately supplied two-side control, change only US translation `translation.functional_currency` from USD to GBP while retaining `currency.functional=USD`, USD20 matched legal result, exact legal version binding, books and supplied rates. Recertify the native FX source through the production owner, execute the new translation, refresh reassessment exact dependency receipts, recertify and execute reassessment. Both executions accepted; reassessment returned `status=complete`, EUR16/EUR18, zero journals. Numeric equality had substituted an incompatible claimed functional currency.

The production Foreign Currency contract checks reporting presentation and quote but did not equate the operation functional currency with its governed legal functional currency at this orchestration boundary. The new two-side validator also lacked that explicit qualification. This is a dimensional authority defect, not a request to alter accounting or balance the residual.

Requested generic remediation: fail closed whenever native operation functional currency differs from the governed translation producer and exact matched legal source functional currency. Preserve common Group presentation as supported by the existing translation contract; local legal Scope presentation must not be imposed on a legitimate independently supplied common Group translation.

Permanent attack: `test_wrong_native_functional_currency_cannot_qualify_us_legal_side`. Initial pre-fix standalone executable reproduction succeeded with substituted GBP; regression is required to reject it after remediation.

## Other independent attacks

The permanent suite covers wrong economic identity, wrong original transaction currency, omitted receivable mapping, duplicate payable mapping, native payable carrying plug, other transaction ID, unsupported services/recharge, mutable reviewed translation source, and forged framework receipt source metric. Its positive control checks unequal carrying amounts, no journals and original historical classification.

## Remediation rerun status

**TSIQA01 RESOLVED in the bounded extension; independently rerun.** The generic functional-currency guard now rejects the reproduced substitution; the defensive reassessment check binds native functional currency to the exact matched legal producer. Independent executable suite: **13 distinct tests PASS**, including the previously reproducing currency attack, stale/superseded legal-version receipt attack, forged native-side receipt and unequal-value clean control. An initial attempted presentation guard rejected legitimate common EUR translation and was corrected before this passing rerun. No unresolved substantive findings remain in this bounded review. This result does not close IQA03 or replace final Stage 4 independent QA.

## Scope and limitations

The suite uses the bounded extension control source builder but does not edit that builder, production contracts, rates or reviewed book amounts. It exercises production owner recertification and VersionedExecution for the substantive currency attack. Mutation attacks targeting validators complement those lifecycle executions. Full population, selective invalidation, temporal integration, eight lineages, closure and final repository independent QA are outside this intermediate review.

# TOPIC-02-009 — Worker scenario execution

Capabilities: CAO-02-019, CAO-02-020. Date: 2026-09-27. Method: desk-check the existing documented CAO route against explicit facts; this does **not** demonstrate live system operation or independent assurance.

## Positive and negative case

**Facts supplied:** Prior-year invoice 80,000 was available before issued accounts but omitted from accrual; current year discovery.

**Expected accounting/control decision:** Separate error from estimate, assess materiality and applicable framework/period; bridge comparative, tax and opening balance.

**Failure injection:** Posting only current expense may misstate comparative.

**Observed desk-check result:** The existing topic decision model routes to the expected investigation, control and evidence requirement. Mark **PASS for routing**, subject to independent review of any accounting-standard or jurisdiction-specific conclusion. The failure injection would prevent unconditional sign-off. No live ledger entry was executed.

## Evidence to retain in a real case

Input population and extraction parameters, entity/framework/period, transaction or control IDs, owner and reviewer, dated source support, exception/adjustment decision, ledger/reporting tie-out and resolution or escalation record. Preserve prior versions and cutoff. Where the input is incomplete or materially contradictory, surface missing evidence rather than invent a figure or claiming a clean control.

## Cross-topic handoff

Use the canonical capability matrix to route substantive recognition, measurement and disclosure questions to the relevant technical topic. Domain 09 supplies control design, Domain 10 audit evidence, Domain 11 data lineage and Domain 12 process execution. This test does not certify those dependent topics.

## US issuer decision-route desk tests — 2026-09-28

Apply `practice/us-issuer-overlay.md`; illustrative facts and conclusions below test routing, not actual materiality thresholds or live filings. ASC paragraph verification remains open as recorded in `canonical-sources.md`.

| Input/failure injection | Expected result | Desk result |
|---|---|---|
| $80,000 2025 omitted accrual, still unpaid at 2026 close; preparer posts 2026 expense as the sole correction | Reject: 2025 expense/liability error $80,000; current expense posting clears balance-sheet error but introduces $80,000 earnings distortion. Run both SAB 108 measures and materiality for annual/interim statements. | PASS: route refuses current-only entry and requests period bridge. |
| Same error is material to filed 2025 Q4/annual statements; discovered Monday, governance concludes non-reliance on Thursday | Big R; Item 4.02(a) clock starts from Thursday conclusion, four business days subject to calendar; identify affected statements/facts/auditor discussion. Prepare amended reporting and controls review. | PASS: discovery date is not incorrectly used as 8-K trigger. |
| 2025 issued statements remain reliable; either 2026 correction or carryover is material | Little r comparative revision and disclosure when next filed; generally no Item 4.02(a). Test pending filings and auditor notice separately. | PASS: no default current expense or automatic 8-K. |
| Both years' effects immaterial alone but known other errors make aggregate effect material | Reject out-of-period route; recompute aggregate and revisit Big R/little r classification. | PASS: aggregation defeats single-item shortcut. |
| Both prior and current effects immaterial individually and in aggregate, with no qualitative factor | Document approved out-of-period route, misstatement log and subsequent monitoring. | PASS: conditional, not numeric safe harbor. |
| Auditor independently advises non-reliance on its report, or issuer is a foreign private issuer | Pause issuer-only Item 4.02(a) shortcut; apply Item 4.02(b)/(c) or separate form/jurisdiction analysis as applicable. | PASS: exception routes require counsel and governance decision. |

Arithmetic check: unchanged unpaid obligation yields an $80,000 cumulative liability error if left uncorrected; recording the omitted expense in 2026 reduces that closing liability error to zero while shifting $80,000 expense into the wrong year. A tax effect, settlement or new 2026 event changes the numbers and must be independently modeled. Review inputs: issued versions, source dates, full misstatement register, quarter/year bridges, counsel calendar and approvals. These desk tests do not prove Basic View paragraph currency.

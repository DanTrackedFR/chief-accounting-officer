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

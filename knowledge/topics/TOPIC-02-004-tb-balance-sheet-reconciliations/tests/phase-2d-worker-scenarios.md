# TOPIC-02-004 — Worker scenario execution

Capabilities: CAO-02-009, CAO-02-010. Date: 2026-09-27. Method: desk-check the existing documented CAO route against explicit facts; this does **not** demonstrate live system operation or independent assurance.

## Positive and negative case

**Facts supplied:** TB agrees to GL, but a 90,000 prepaid reconciliation includes 35,000 aged unsupported items.

**Expected accounting/control decision:** Rebuild source-to-GL rollforward, age and assign each item; challenge valuation and sign-off.

**Failure injection:** TB equality does not certify the balance.

**Observed desk-check result:** The existing topic decision model routes to the expected investigation, control and evidence requirement. Mark **PASS for routing**, subject to independent review of any accounting-standard or jurisdiction-specific conclusion. The failure injection would prevent unconditional sign-off. No live ledger entry was executed.

## Evidence to retain in a real case

Input population and extraction parameters, entity/framework/period, transaction or control IDs, owner and reviewer, dated source support, exception/adjustment decision, ledger/reporting tie-out and resolution or escalation record. Preserve prior versions and cutoff. Where the input is incomplete or materially contradictory, surface missing evidence rather than invent a figure or claiming a clean control.

## Cross-topic handoff

Use the canonical capability matrix to route substantive recognition, measurement and disclosure questions to the relevant technical topic. Domain 09 supplies control design, Domain 10 audit evidence, Domain 11 data lineage and Domain 12 process execution. This test does not certify those dependent topics.

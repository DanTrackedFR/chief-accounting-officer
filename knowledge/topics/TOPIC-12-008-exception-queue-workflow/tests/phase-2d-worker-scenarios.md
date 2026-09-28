# TOPIC-12-008 — Worker scenario execution

Capabilities: CAO-12-019, CAO-12-020. Date: 2026-09-27. Method: desk-check the existing documented CAO route against explicit facts; this does **not** demonstrate live system operation or independent assurance.

## Positive and negative case

**Facts supplied:** Exceptions queue has 40 unassigned rejected invoices near close.

**Expected accounting/control decision:** Classify by risk/age, assign owner and due date, preserve unique IDs and settlement/posting state.

**Failure injection:** Ticket closure without accounting resolution fails.

**Observed desk-check result:** The existing topic decision model routes to the expected investigation, control and evidence requirement. Mark **PASS for routing**, subject to independent review of any accounting-standard or jurisdiction-specific conclusion. The failure injection would prevent unconditional sign-off. No live ledger entry was executed.

## Evidence to retain in a real case

Input population and extraction parameters, entity/framework/period, transaction or control IDs, owner and reviewer, dated source support, exception/adjustment decision, ledger/reporting tie-out and resolution or escalation record. Preserve prior versions and cutoff. Where the input is incomplete or materially contradictory, surface missing evidence rather than invent a figure or claiming a clean control.

## Cross-topic handoff

Use the canonical capability matrix to route substantive recognition, measurement and disclosure questions to the relevant technical topic. Domain 09 supplies control design, Domain 10 audit evidence, Domain 11 data lineage and Domain 12 process execution. This test does not certify those dependent topics.

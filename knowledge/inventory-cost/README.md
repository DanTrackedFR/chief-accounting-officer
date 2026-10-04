# Supplemental Inventory & Cost Accounting

`SUPPLEMENTAL_INVENTORY_COST` is an owner-authorized governed extension for the existing `skills/inventory-cost/` package. It is not a new canonical topic. The historical 157 topics, 347 mappings and 1,598 canonical claims are unchanged. Income Tax and Agriculture remain separate supplements.

This register contains 228 atomic claims: 57 each for IFRS, US GAAP, full commercial FRS 102 and AASB Tier 1 for-profit reporters. It covers manufacturing conversion cost as core scope, rather than treating goods inventory as a warehouse valuation exercise. Read `FRAMEWORK-METHOD.md` for the source-dependent cost workflow and boundaries.

The author initially supplies `REVIEWED` claims with `PENDING` approval and no review signature. Only a separate knowledge reviewer can approve them. The independent implementation gate is a later gate; claim approval cannot certify an executable skill. See `INDEPENDENT-QA.md` and the separate reviewer tests for the actual disposition.

`retrieve(framework, period, entity_scope, ..., decisions, period_start)` requires the exact supported entity scope in `SCOPES`. This deliberately excludes unsupported entity and period routes. Both reporting-period start and end must be within 2026; an annual period crossing 2027 needs a new scope review. Unrecognized decisions and stale, altered or incompletely signed claims fail closed. Each reviewer signature contains a deterministic hash of substantive claim content, provenance, tests and limitations. Public retrieval is an allowlist: internal evidence tiers, source notes and reviewer metadata are excluded while substantive restrictions remain visible.

Run the dedicated gate and authored tests with:

```
python knowledge/inventory-cost/validate_supplement.py
python -m unittest discover -s knowledge/inventory-cost -p test_supplement.py
python -m unittest discover -s knowledge/inventory-cost -p test_independent_claim_qa.py
```

Approval is distinct from direct authority verification. Lower evidence claims retain `audit_required: true`, even after the independently checked training-data approval route. See `EVIDENCE-AND-QA.md` for actual inspected sources and access gaps. Nothing in this supplement represents ERP posting, legal ownership advice, a production forecast or an auditor's opinion.

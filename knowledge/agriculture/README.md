# Governed supplemental Agriculture knowledge

Namespace: `SUPPLEMENTAL_AGRICULTURE`. Skill: 38 — Agriculture / Biological Assets. Owner-authorized standalone extension, separate from the historical 157 canonical topics, 347 mappings, 1,598 canonical claims and 64 Income Tax supplemental claims. No TOPIC IDs are created. All 66 claims were independently challenged and approved on 2026-10-04; see INDEPENDENT-QA.md. The author did not approve this register.

66 atomic claims: IFRS 19; AASB 21; UK GAAP 16; US GAAP 10. Governance validation, context-bounded retrieval and arithmetic challenges are executable. `validate_supplement.py` permits research-stage PENDING data but runtime `retrieve` fails closed until APPROVED with recorded independent reviews. Public retrieval uses an allowlist excluding provenance, approval and assurance machinery.

Bounded applicability: annual reporting periods starting and ending during 2026, for-profit full IFRS; Australian for-profit Tier 1; UK/Republic of Ireland full FRS102; US agricultural producers subject to explicit industry-owner routing. No early IFRS18/AASB18/adapted-format adoption, Tier2, UK Section1A, IFRS for SMEs, charities/PBE, cooperatives or special sector overlays. Reporting date, period start, jurisdiction, entity reporting basis and adoption review are actual required facts, not defaults.

This is knowledge, not an independent valuation or legal opinion. It supplies agricultural classification, recognition, measurement and disclosure decisions and boundary routes. Skill implementation must bind applied claims to actual framework and case decisions, verify current approval/fingerprint, and consume only independently approved claims.

Run from repository root:

    python knowledge/agriculture/validate_supplement.py
    python -m unittest discover -s knowledge/agriculture -p 'test*.py' -v

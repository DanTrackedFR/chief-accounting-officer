# Standards authority audit — APPROVED gate

Established: 2026-10-01

## Purpose
APPROVED is an authority-assurance status above substantive REVIEWED. It is applied topic by topic only after independent evidence QA. It must never be inferred from file presence, model agreement, worker self-review, framework similarity, or a historical amendment that does not establish current operative requirements.

## Mandatory gate
A topic may move from REVIEWED to APPROVED only when all applicable conditions below are satisfied:

1. **Substantive prerequisite** — canonical manifest status is REVIEWED and no unresolved substantive blocker exists.
2. **Claim coverage** — every material standards-derived proposition has a stable claim record in the canonical topic-local `standards-claims.json`. A genuinely non-normative topic may use an empty claim register only after documented scope review confirms that no material standards-derived proposition is embedded in its method, tests, examples or outputs.
3. **Authority evidence** — every material normative claim is SOURCE_VERIFIED against current authorized primary standard, legislation or regulator text applicable to the stated period and entity scope. PRIMARY_CORROBORATED, SECONDARY_CORROBORATED, MODEL_DERIVED_AUDIT_REQUIRED, NOT_RESEARCHED and CONFLICTED do not satisfy APPROVED.
4. **Effective-period and scope** — current version, effective date/transition, jurisdiction and relevant entity elections/status are recorded and independently checked.
5. **Cross-framework/adversarial review** — applicable IFRS, US GAAP, UK GAAP, AASB and SEC/regulatory routes are checked independently; no framework conclusion is inferred from another framework.
6. **Rights gate** — repository evidence remains excerpt-free/independently paraphrased where required; no restricted standards text, licensed PDFs, credentials or prohibited reproductions are committed.
7. **Regression** — linked scenarios, calculations and routing tests pass after the final authority disposition.
8. **Conflict gate** — no material CONFLICTED claim or unresolved authority discrepancy remains.
9. **Independent QA** — controller records the approval evidence and date; the author/research worker cannot self-promote.
10. **Canonical update order** — controller updates the manifest first, then regenerates derived progress/roadmap reporting.

## Conservative rule
If direct current authority cannot be inspected for a material claim, the topic remains REVIEWED even if the accounting treatment is substantively sound and strongly corroborated. This is not a Phase 2D failure; it is an open authority-assurance item.

## Audit reporting
Report separately:
- substantive status counts (REVIEWED/PARTIAL/NOT_STARTED);
- standards register coverage;
- claim evidence-status counts;
- topics eligible for APPROVED;
- topics actually APPROVED;
- unresolved authority/access/conflict queues.

Do not collapse these into one completion percentage.

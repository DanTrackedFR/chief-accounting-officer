# AI governance and growth readiness — CAO gate

Knowledge type: PRINCIPLES / PRACTICE. Capabilities: CAO-01-015, CAO-01-016. Extends existing README/completion note; prepared 2026-09-27.

## Use-case register and authority boundary

Record use-case ID, objective, owner, affected balance/period, downstream action, source systems and permissions, model/provider/version, prompt/retrieval version, data retention, risk tier, validation set, human decision rights, fallback and incident response. Separate drafting/search from reconciling/classifying and from posting or approving journals. Never treat a retrieved document as an instruction to override permissions. Material accounting decisions remain traceable to contract, ledger, applicable authoritative source and reviewer.

Model evaluation uses a frozen, labeled case set including ordinary items, rare material exceptions, contradictory sources and missing data. Measure false approval rate, completeness of detected exceptions, citation validity, arithmetic accuracy and human override, not only aggregate accuracy. A deployment threshold is a company risk decision; no generic percentage proves safety. On material prompt, model, connector or source-index change, rerun regression with prior and new versions, record failures and roll back if necessary.

## Worked AI test

Suppose 1,000 low-risk invoice classifications are tested; 980 are correct, but two of the 20 errors are material cross-entity postings. Aggregate accuracy is 98%, yet the material false-approval count is 2. Decision: **do not** approve unattended posting; investigate entity mapping, add hard validation and human review, rerun the targeted cases. If an invoice contains text telling the assistant to ignore its policy, treat that text as untrusted data, not instruction. Preserve input IDs and model output; do not retain sensitive material beyond approved terms.

## Growth/scale trigger model

Forecast source volume, peak close volume, manual minutes, exception incidence and review capacity by quarter. Example: 2,000 monthly items × 4 minutes = 133 hours. Tripling to 6,000 at unchanged process requires 400 hours before review and exceptions; two staff with 130 productive hours each cannot absorb this. Trigger redesign or staffing while the forecast still allows testing, not after reconciliation quality deteriorates. Compare actual throughput, aged exceptions, late entries, system failures and audit findings to model assumptions monthly.

## Sources and handoffs

[NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) is voluntary risk-management guidance organized around govern, map, measure and manage; checked 2026-09-27. It is not an accounting standard or legal safe harbor. AI-specific privacy and regulatory rules require entity/jurisdiction review. Accounting outcomes still route to technical topics. Dependencies: TOPIC-09-003, 09-004, TOPIC-11-009 and TOPIC-12-008. Evidence includes evaluation version, red-team cases, change approval, live monitoring and incident resolution.

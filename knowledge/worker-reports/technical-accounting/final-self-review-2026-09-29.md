# Technical accounting self-review — 29 September 2026

This is a worker checkpoint on draft PR #6, **not** Phase 2D completion or a proposal to bulk-promote statuses. The canonical manifest remains unchanged.

## Scope and preserved work

The latest `main` manifest identified 54 PARTIAL IDs in Domains 03, 05, 06, 07, 08 and 13. All 54 have been given one topic-local `standards-claims.json` and a targeted `evidence-and-regression.md` in a canonical folder. Existing factory/workpaper/scenario files and duplicate/retry paths were preserved. Ten batches (24–34) were committed to the same worker branch and PR. There are 216 recorded framework claims; 211 are `MODEL_DERIVED_AUDIT_REQUIRED`, one `PRIMARY_CORROBORATED` (ASU 2025-05, not current ASC), and four narrow IFRS claims `SOURCE_VERIFIED`. The 212 unverified claim IDs are in `final-standards-audit-queue.json`.

## Substantive status, separate from source evidence

- **Coverage:** 54/54 assigned PARTIAL topics have an additional topic-specific case, numerical or decision branch, four-framework routing and audit-evidence handoff. This is coverage of the remediation queue, not proof of completion.
- **Genuinely REVIEWED-ready on this worker's final audit:** **0/54 asserted.** The prior substantive packs vary in depth. A single cross-framework claim per topic is too broad to ringfence *every* material standards-derived assertion in the retained prose, and the new narrative negative cases have not been independently executed against a formal scenario harness. Some framework methods and disclosure/election routes are directional rather than worked through to all required outputs. Those are substantive factory gaps, not merely lack of source access.
- **Remaining substantive work:** For each topic, split compound claims by scope, recognition, measurement, presentation/disclosure and transition; annotate existing normative prose and individual scenario assertions with the correct claim IDs; run framework-specific opposing outcomes and document exact journal/workpaper/control/data results. Reconcile duplicate folders into canonical content without deleting useful material. Recheck public/private, UK small-entity, Australian tier/NFP and effective-period choices for each relevant topic. Only after this topic-level review should an ID be proposed as substantively REVIEWED-ready.

## Standards-evidence status

Direct official-source research was attempted across IFRS Foundation, FRC, AASB and FASB routes. Access to an official issuer page or a source URL did not establish an operative paragraph. A final self-review therefore downgraded 53 earlier overbroad `SOURCE_VERIFIED` records. Current ASC Basic View paragraphs were not inspected; no current US paragraph reference is claimed verified. FRC revised Section 23/other sections and AASB operative compilations need topic-specific direct audits. An unavailable source by itself does not determine substantive PARTIAL status; it remains a separate claim-level risk. The machine-readable queue gives each ID, framework, status and exact audit task. No copyrighted standard bodies are stored.

## Regression and scope

Batch reports record structural and illustrative numerical checks after every 4–5 topics. Final cross-topic scan found exactly one claim register and one new case in a canonical folder per ID, four framework claims per topic, unique IDs referenced in cases, 212 audit-required claims, no out-of-scope changed paths and no whitespace errors. These checks establish local consistency only. They do not prove that retained factory content meets all Phase 2D requirements or that framework assertions are accurate.

## Next review sequence

1. Audit each topic's retained normative prose against its claim register; split and annotate every material proposition.
2. Complete specific framework/election/transition differences and adversarial scenarios, beginning with the original QA ledger blockers in `qa-remediation-self-review.md`.
3. Directly inspect authoritative source paragraphs where available; update evidence tier, version and period without inferring current ASC from an ASU.
4. Run independent topic-level QA and only then propose status changes to integration. Do not edit shared manifest/progress/roadmap on this branch.

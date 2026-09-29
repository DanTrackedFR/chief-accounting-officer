# Standards evidence register — Phase 2D

This is the ringfenced evidence layer for ALL frameworks (IFRS, US GAAP, UK GAAP/FRC, AASB and relevant SEC/regulatory material). It is not a copy of any standard. Do not commit copyrighted paragraph bodies, PDFs, credentials or licensed research exports.

Each material standards-derived proposition in a topic must have a stable claim ID and a record in a topic-local `standards-claims.json` file conforming to `claim.schema.json`. Cite the claim ID beside the proposition in PRINCIPLES/STANDARDS/DIFFERENCES/PRACTICE as appropriate. Workpaper/scenario assertions must reference tested claim IDs. Keep original practical guidance distinct from normative requirements. Use framework-specific records rather than asserting that an IFRS paragraph proves US GAAP.

Evidence status (independent of topic workflow status):
- SOURCE_VERIFIED: authorized, current primary standard/legislation/regulator text inspected, exact applicable provision and effective-period verified, with reproducible evidence locator and reviewer.
- PRIMARY_CORROBORATED: official amendments/ASUs, regulator guidance, taxonomy or other primary documents corroborate a claim, but operative standard paragraph itself was not inspected.
- SECONDARY_CORROBORATED: reliable professional literature supports claim but primary current text was not inspected.
- MODEL_DERIVED_AUDIT_REQUIRED: drafted from model knowledge; neither direct current authoritative inspection nor sufficient external corroboration. Exact paragraph references are provisional, not invented if uncertain.
- CONFLICTED: sources/models disagree or period/jurisdiction unresolved; quarantine claim from confident normative conclusions.
- NOT_RESEARCHED: pending research.

The source kind and verification status are separate: an ASU is official primary material but does not alone verify the currently operative Codification. A model review is a consistency check, not source verification. A failed website fetch is a recorded access attempt, not evidence for the standard's content. A source URL without inspection does not qualify as SOURCE_VERIFIED.

For each claim record source URLs, source title/publisher, document version/date, access date, precise locator, excerpt-free independently authored paraphrase, effective date/transition and entity scope, unresolved caveats, test cases, independent model reviews, reviewer and review date. Never fabricate dates or references. `null` means unknown. Mark model training knowledge as model-derived regardless of confidence.

Audit gates:
1. Structural: validate JSON schema, unique IDs, topic IDs, referenced IDs and path existence.
2. Normative: compare each claim against the actual current authorized standard and its applicable effective period; record source version and human/independent reviewer. Model agreement cannot satisfy this gate.
3. Cross-framework: test scope, recognition, measurement, presentation, disclosure and transition separately; don't infer equivalence.
4. Adversarial: test boundary cases, alternative elections, US public/private status, UK entity regimes and Australian adoption differences.
5. Regression: run scenario tests after every changed claim; preserve disagreement and remediation history.

Topic REVIEWED means substantive method review only when the manifest explicitly says so. Do not infer SOURCE_VERIFIED, APPROVED or Phase 2D completion from REVIEWED. Existing 93/64 status is a historical recorded ledger, not a fresh standards audit. No bulk status promotions. Maintain a machine-readable audit queue of unverified claims and reconcile every claim before declaring standards authority verified.

Update process: subscribe to issuer updates (FASB ASUs, IASB/IFRS, FRC, AASB, SEC as applicable); record publication, adoption, effective dates and transition, identify impacted claim IDs, recheck current text and rerun scenarios. Do not automatically overwrite historical-period guidance with newly effective rules.

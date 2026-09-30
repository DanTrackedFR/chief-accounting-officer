# Standards evidence audit — full-corpus baseline

Baseline date: 2026-09-30

## Purpose

This audit is a separate assurance axis from Phase 2D substantive REVIEWED status. A topic can remain REVIEWED while standards claims are unverified. No claim becomes SOURCE_VERIFIED from model agreement, an inaccessible source URL, an amendment document that does not establish current operative text, or framework similarity.

## Baseline inventory

- Canonical topics: 157.
- Substantively REVIEWED topics: 157.
- Topic-local `standards-claims.json` files currently present on main at audit start: 64.
- Topics without a topic-local claim register: 93.
- Therefore full-corpus claim extraction/ringfencing is **not complete**. The existing claim population is only the first audit population.

The 64 existing registers comprise TOPIC-02-009; the remediated Technical Accounting populations in Domains 03, 05, 06, 07, 08 and 13; the Specialist remediation population TOPIC-04-001–006 and 04-011; TOPIC-15-002; and TOPIC-16-006.

## Audit sequence

1. **Structural gate** — validate every existing register against `claim.schema.json`; enforce topic/path identity, globally unique claim IDs, evidence-status invariants, and source-inspection rules.
2. **Coverage gate** — create a register for every remaining topic. Operational topics may have an empty `claims` array only when a documented scope review concludes that no material standards-derived proposition exists.
3. **Normative gate** — inspect current authorized source text where accessible. Record exact applicable locator, period, entity scope, reviewer and date. Downgrade rather than infer when evidence is insufficient.
4. **Cross-framework/adversarial gate** — test IFRS, US GAAP, UK GAAP and AASB independently, including elections, transition, public/private or tier differences and boundary cases.
5. **Consistency review** — external/model reviews may identify disagreements and omissions. They populate `model_reviews` and conflict queues but never satisfy SOURCE_VERIFIED.
6. **Regression** — rerun linked numerical/adverse tests after claim changes.
7. **Approval gate** — define and apply an explicit APPROVED threshold only after the evidence population is complete. Until then, REVIEWED remains the substantive status and standards assurance is reported separately.

## Immediate audit queues

### Queue A — missing claim extraction
93 topics have no topic-local claim register at baseline. These are first-class audit work, not assumed standards-free.

### Queue B — existing unverified claims
Every claim in the 64 existing registers with evidence status other than SOURCE_VERIFIED remains in the authority audit queue. Claims marked SOURCE_VERIFIED must also pass structural invariants and effective-period review before relying on that label globally.

### Queue C — conflicts
Any disagreement on framework, reference, effective date, transition, entity scope or accounting conclusion is set to CONFLICTED and quarantined from confident normative output until resolved.

## Reporting

Every audit checkpoint reports both:
- substantive topic status: REVIEWED / PARTIAL / NOT_STARTED; and
- standards evidence status: register coverage, claim count, SOURCE_VERIFIED count, corroborated count, model-derived/not-researched count and CONFLICTED count.

Do not collapse these axes into one percentage.

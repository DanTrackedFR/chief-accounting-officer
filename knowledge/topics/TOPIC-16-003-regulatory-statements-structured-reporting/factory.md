# Regulatory statement requirements and structured reporting — substantive factory

Supplements the original README. Capabilities: CAO-16-006, CAO-16-007. Source checked 2026-09-27. Proposed REVIEWED candidate for the tagging/control method; current taxonomy and entity-specific filing rules remain mandatory inputs.

## Authority and technical perimeter

Separate (a) accounting framework and statement presentation, (b) regulator form, (c) machine-readable taxonomy and validation. The [SEC Inline XBRL page](https://www.sec.gov/data-research/structured-data/inline-xbrl) identifies domestic 10-K/10-Q and foreign-issuer requirements, including notes and schedules. [ESMA ESEF](https://www.esma.europa.eu/issuer-disclosure/electronic-reporting) applies to issuers in its scope and uses XHTML and XBRL/iXBRL tagging for applicable consolidated IFRS statements. [Companies House accounts filing](https://www.gov.uk/file-your-company-annual-accounts) and [ASIC](https://www.asic.gov.au/regulatory-resources/financial-reporting-and-audit/preparers-of-financial-reports/lodgement-of-financial-reports/) are different delivery channels; do not apply SEC taxonomy rules to them by analogy. For a 2026 ESEF report, verify the applicable taxonomy version/entry point and regulator technical manual; for IFRS 18 early application or a later period, check taxonomy compatibility before tagging.

## Data model and validation

Construct a presentation-to-tag mapping: financial-statement line or note, period/context, entity, unit, sign, scale, balance type, taxonomy concept and version, dimensions, extension rationale, anchoring where required, source amount and reviewer. Use a standard taxonomy concept when it accurately captures meaning; an extension is not a workaround for a wrong unit or sign. For notes, block-tagging and detailed tags have different requirements by regulator and effective year. Validate (1) rendered human-readable statement, (2) machine-readable instance, (3) calculation relationships and required contexts, (4) cross-period consistency, (5) extension labels and anchoring, and (6) correspondence of tags to audited/approved text. Treat validation warnings by severity; retain resolution or documented acceptance with sign-off.

## Worked mapping

Statement says trade receivables 1,200,000 currency units at 31 December 2026. If an upstream table already carries currency units but the conversion pipeline multiplies by a displayed “thousands” scale again, the XBRL amount could become 1,200,000,000: human statement and data instance disagree. Reperform raw TB 1,200,000 → presentation 1,200 (thousands) → tagged raw amount 1,200,000; the scale transforms once. Separately, a liability presented as positive 400,000 may require taxonomy sign/balance interpretation; do not flip it based only on screen typography. The reviewer opens the rendered filing and machine output and compares material values at both levels.

## Controls and scenarios

Before finalization, reconcile all face-statement and material note values to signed source; run schema and calculation validation; review new extensions; compare current/prior taxonomy mappings; lock file hashes. After a late adjustment, invalidate affected tags and rendering and rerun. S1: visible 1.2m, tagged 1.2bn → FAIL until scale corrected. S2: correct numeric tag but context is prior-year comparative → FAIL. S3: extension used despite matching standard concept → challenge and remap. S4: same IFRS financials for SEC and EU issuer filings → do not reuse taxonomy packages without format/perimeter evaluation. Test results are route assertions, not software conformance certification.

Required evidence: taxonomy/version, mapping and source extract IDs, rendered and instance files, validation logs, reviewer notes, release hash and regulator receipt. Dependencies: 08-009 tie-out, 11-008 reporting layer, 16-002 filing and 16-004 disclosure control. Residual: exact taxonomy versions and regulator technical rules change; check at execution date.

# TOPIC-16-003 — Regulatory financial statements and structured reporting

Status: DRAFT for independent Phase 2D QA; canonical capabilities: CAO-16-006, CAO-16-007. Prepared 2026-09-27. This topic contains independently authored decision and execution guidance; restricted standards and regulations are reference-only.

## Principles and scope

The accounting basis determines recognized amounts; filing templates, tagging taxonomies and local rules determine their delivery. Tags are assertions about meaning, not cosmetic labels. Identify the legal entity, jurisdiction, report date, group perimeter and applicable framework before evaluating requirements. This is a regulatory overlay, not a replacement for financial-statement recognition and measurement under IFRS, US GAAP, FRS 102 or AASB.

## Authoritative source and effective-period gates

- US SEC: [forms and reporting](https://www.sec.gov/forms) and [Inline XBRL](https://www.sec.gov/data-research/structured-data/inline-xbrl); use the actual registrant form and instructions.
- UK: [Companies House preparing and filing accounts](https://www.gov.uk/government/publications/life-of-a-company-annual-requirements/life-of-a-company-part-1-accounts); check company type, incorporation and year-end.
- EU listed issuers: [ESMA electronic reporting](https://www.esma.europa.eu/issuer-disclosure/electronic-reporting) and operative ESEF taxonomy.
- Australia: [ASIC financial reporting](https://www.asic.gov.au/regulatory-resources/financial-reporting-and-audit/financial-reporting/) and entity-specific Corporations Act duties.
Source check: 2026-09-27, official publisher pages. Exact paragraph and form instructions require verification for the specific entity and period; FASB Codification paragraph bodies were not relied upon. Treat amended laws, pending rules, adoption elections and transition relief separately. Do not infer a mandatory obligation solely from a standard's publication date.

## CAO decision and execution

Identify legal filer, filing form and reporting framework separately. Map statutory statements and notes to presentation requirements. For Inline XBRL/ESEF choose the applicable taxonomy/version and standard concept where possible; extension concepts require documented rationale and anchoring where applicable. Validate sign, scale, period type, dimensions, contexts, calculations and rendered human text against filed numbers. Escalate unsupported taxonomy or software validation errors.

Workpaper minimum: entity and period; governing rule and URL/version; applicability facts; scope/boundary; inputs and provenance; calculation/mapping; alternatives and judgments; review/sign-off; reporting output; exceptions, remediation and change log. Control owner reconciles source population to accounting or operational systems, and a second reviewer checks the conclusion against the effective rule. Preserve submission/assurance evidence and the signed version.

## Worked application and boundaries

A 1,200,000 cash balance tagged with a scale of thousands would appear as 1.2 billion in machine-readable output: fail validation despite the visible PDF/text showing 1.2 million.

For each workpaper consider materiality, disclosure, data quality, presentation, applicable assurance and whether a discovered difference changes an accounting entry. Route underlying accounting recognition/measurement to the governing financial topic. Do not post a journal solely to make a regulatory return or sustainability metric reconcile; document the rule-specific bridge.

## Executed desk scenarios (decision-route QA)

Narrative number matches but XBRL scale differs: FAIL until fixed; IFRS issuer begins a period when a new ESEF taxonomy is mandatory: PASS only with the effective taxonomy selected. These checks exercise decision routing only; they do not certify a live entity's filing or a paragraph-level legal conclusion. A production case must collect actual evidence and rerun current-rule verification.

## Dependencies and limitations

TOPIC-08-009 statement tie-out; TOPIC-11-008 reporting layer; TOPIC-16-004. Source depth: official overview and effective-date pages verified; form-, sector- and entity-specific rules remain case-dependent. Proposed status: PARTIAL pending independent jurisdiction/technical QA for a real reporting fact pattern.

# TOPIC-16-004 — Regulatory disclosure controls and filing tie-out

Status: DRAFT for independent Phase 2D QA; canonical capabilities: CAO-16-008, CAO-16-009. Prepared 2026-09-27. This topic contains independently authored decision and execution guidance; restricted standards and regulations are reference-only.

## Principles and scope

A filing control needs a complete population and a version-locked source. A final PDF review cannot prove that machine tags, exhibits and last-minute edits agree. Identify the legal entity, jurisdiction, report date, group perimeter and applicable framework before evaluating requirements. This is a regulatory overlay, not a replacement for financial-statement recognition and measurement under IFRS, US GAAP, FRS 102 or AASB.

## Authoritative source and effective-period gates

- US SEC: [forms and reporting](https://www.sec.gov/forms) and [Inline XBRL](https://www.sec.gov/data-research/structured-data/inline-xbrl); use the actual registrant form and instructions.
- UK: [Companies House preparing and filing accounts](https://www.gov.uk/government/publications/life-of-a-company-annual-requirements/life-of-a-company-part-1-accounts); check company type, incorporation and year-end.
- EU listed issuers: [ESMA electronic reporting](https://www.esma.europa.eu/issuer-disclosure/electronic-reporting) and operative ESEF taxonomy.
- Australia: [ASIC financial reporting](https://www.asic.gov.au/regulatory-resources/financial-reporting-and-audit/financial-reporting/) and entity-specific Corporations Act duties.
Source check: 2026-09-27, official publisher pages. Exact paragraph and form instructions require verification for the specific entity and period; FASB Codification paragraph bodies were not relied upon. Treat amended laws, pending rules, adoption elections and transition relief separately. Do not infer a mandatory obligation solely from a standard's publication date.

## CAO decision and execution

Design a source-to-filing matrix: source ledger/report, accountable owner, disclosure assertion, draft location and tag. Review completeness of required sections, cross-reference repeated facts and recalculate subtotals. Run separate financial, legal, investor relations and governance reviews with change requests logged. Freeze a release candidate; rerun affected controls after any late change; retain sign-offs, hashes, validation results and receipt.

Workpaper minimum: entity and period; governing rule and URL/version; applicability facts; scope/boundary; inputs and provenance; calculation/mapping; alternatives and judgments; review/sign-off; reporting output; exceptions, remediation and change log. Control owner reconciles source population to accounting or operational systems, and a second reviewer checks the conclusion against the effective rule. Preserve submission/assurance evidence and the signed version.

## Worked application and boundaries

The cover says 5.2 million shares while the EPS note uses 5.0 million weighted-average shares. This can be legitimate, but the control must distinguish period-end shares from weighted average, label both and verify source.

For each workpaper consider materiality, disclosure, data quality, presentation, applicable assurance and whether a discovered difference changes an accounting entry. Route underlying accounting recognition/measurement to the governing financial topic. Do not post a journal solely to make a regulatory return or sustainability metric reconcile; document the rule-specific bridge.

## Executed desk scenarios (decision-route QA)

Last-minute edit after certification: FAIL until impacted certification/tie-out is refreshed; note number in MD&A differs without an explained basis: FAIL. These checks exercise decision routing only; they do not certify a live entity's filing or a paragraph-level legal conclusion. A production case must collect actual evidence and rerun current-rule verification.

## Dependencies and limitations

TOPIC-09-006 financial reporting controls; TOPIC-08-009 tie-out; TOPIC-16-003. Source depth: official overview and effective-date pages verified; form-, sector- and entity-specific rules remain case-dependent. Proposed status: PARTIAL pending independent jurisdiction/technical QA for a real reporting fact pattern.

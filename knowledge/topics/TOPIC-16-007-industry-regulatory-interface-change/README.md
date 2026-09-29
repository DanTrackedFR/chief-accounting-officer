# TOPIC-16-007 — Industry regulatory interface and change impact

Status: DRAFT for independent Phase 2D QA; canonical capabilities: CAO-16-014, CAO-16-015. Prepared 2026-09-27. This topic contains independently authored decision and execution guidance; restricted standards and regulations are reference-only.

## Principles and scope

A sector return may use accounting data but apply different scope, categories, valuation and timing. Regulatory changes require a controlled impact assessment. Identify the legal entity, jurisdiction, report date, group perimeter and applicable framework before evaluating requirements. This is a regulatory overlay, not a replacement for financial-statement recognition and measurement under IFRS, US GAAP, FRS 102 or AASB.

## Authoritative source and effective-period gates

- US SEC: [forms and reporting](https://www.sec.gov/forms) and [Inline XBRL](https://www.sec.gov/data-research/structured-data/inline-xbrl); use the actual registrant form and instructions.
- UK: [Companies House preparing and filing accounts](https://www.gov.uk/government/publications/life-of-a-company-annual-requirements/life-of-a-company-part-1-accounts); check company type, incorporation and year-end.
- EU listed issuers: [ESMA electronic reporting](https://www.esma.europa.eu/issuer-disclosure/electronic-reporting) and operative ESEF taxonomy.
- Australia: [ASIC financial reporting](https://www.asic.gov.au/regulatory-resources/financial-reporting-and-audit/financial-reporting/) and entity-specific Corporations Act duties.
Source check: 2026-09-27, official publisher pages. Exact paragraph and form instructions require verification for the specific entity and period; FASB Codification paragraph bodies were not relied upon. Treat amended laws, pending rules, adoption elections and transition relief separately. Do not infer a mandatory obligation solely from a standard's publication date.

## CAO decision and execution

Maintain applicability register by industry and licensed entity. For each return map line item to accounting source and regulatory adjustment, with accountable owner, frequency, regulator, deadline and source rule. Monitor change bulletins and effective/transition dates; compare old versus new form/definitions, test mapping and controls in parallel, document differences, train owners, and approve cutover. Escalate any new legal interpretation to regulatory counsel.

Workpaper minimum: entity and period; governing rule and URL/version; applicability facts; scope/boundary; inputs and provenance; calculation/mapping; alternatives and judgments; review/sign-off; reporting output; exceptions, remediation and change log. Control owner reconciles source population to accounting or operational systems, and a second reviewer checks the conclusion against the effective rule. Preserve submission/assurance evidence and the signed version.

## Worked application and boundaries

A payments company changes its safeguarded-funds product. The CAO reconciles segregated cash and customer liabilities to the GL while the licensed compliance owner determines return classification and legal safeguarding tests.

For each workpaper consider materiality, disclosure, data quality, presentation, applicable assurance and whether a discovered difference changes an accounting entry. Route underlying accounting recognition/measurement to the governing financial topic. Do not post a journal solely to make a regulatory return or sustainability metric reconcile; document the rule-specific bridge.

## Executed desk scenarios (decision-route QA)

New sector template adds a field: PASS only if data lineage and dry-run validation exist; a regulator FAQ conflicts with a rule: PASS only with hierarchy and documented escalation. These checks exercise decision routing only; they do not certify a live entity's filing or a paragraph-level legal conclusion. A production case must collect actual evidence and rerun current-rule verification.

## Dependencies and limitations

TOPIC-06-001 restricted cash; TOPIC-11-003 interfaces; TOPIC-16-006. Source depth: official overview and effective-date pages verified; form-, sector- and entity-specific rules remain case-dependent. Proposed status: PARTIAL pending independent jurisdiction/technical QA for a real reporting fact pattern.

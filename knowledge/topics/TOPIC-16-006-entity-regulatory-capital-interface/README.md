# TOPIC-16-006 — Entity-level regulatory reporting and capital interface

Status: proposed substantively REVIEWED-ready for independent QA; standards-claim audit queue remains open.

Integrated route: `phase-2d-method.md` and `standards-claims.json`. This is a substantive QA proposal, not canonical manifest promotion or a live-entity approval. Earlier source-access-only status statements below are historical; claim-level audit remains open.

## Principles and scope

Regulatory capital and accounting equity are distinct measures. Reconcile them through explicit permitted adjustments and scope, never equate a GL balance to capital without a rule. Identify the legal entity, jurisdiction, report date, group perimeter and applicable framework before evaluating requirements. This is a regulatory overlay, not a replacement for financial-statement recognition and measurement under IFRS, US GAAP, FRS 102 or AASB.

## Authoritative source and effective-period gates

- US SEC: [forms and reporting](https://www.sec.gov/forms) and [Inline XBRL](https://www.sec.gov/data-research/structured-data/inline-xbrl); use the actual registrant form and instructions.
- UK: [Companies House preparing and filing accounts](https://www.gov.uk/government/publications/life-of-a-company-annual-requirements/life-of-a-company-part-1-accounts); check company type, incorporation and year-end.
- EU listed issuers: [ESMA electronic reporting](https://www.esma.europa.eu/issuer-disclosure/electronic-reporting) and operative ESEF taxonomy.
- Australia: [ASIC financial reporting](https://www.asic.gov.au/regulatory-resources/financial-reporting-and-audit/financial-reporting/) and entity-specific Corporations Act duties.
Source check: 2026-09-27, official publisher pages. Exact paragraph and form instructions require verification for the specific entity and period; FASB Codification paragraph bodies were not relied upon. Treat amended laws, pending rules, adoption elections and transition relief separately. Do not infer a mandatory obligation solely from a standard's publication date.

## CAO decision and execution

Identify licensing regime, reporting entity/perimeter, return, supervisor, reference date, consolidation and prudential definitions. Reconcile statutory equity and assets to regulatory adjustments (for example deductions or filters), document each regulatory source and data lineage. Verify minimum requirement, buffers and breach/escalation criteria with the regulated specialist. Provide CAO-owned accounting data with sign-off and retain regulatory team ownership of interpretation.

Workpaper minimum: entity and period; governing rule and URL/version; applicability facts; scope/boundary; inputs and provenance; calculation/mapping; alternatives and judgments; review/sign-off; reporting output; exceptions, remediation and change log. Control owner reconciles source population to accounting or operational systems, and a second reviewer checks the conclusion against the effective rule. Preserve submission/assurance evidence and the signed version.

## Worked application and boundaries

Statutory equity 20 million less disallowed intangible assets 3 million and another verified prudential adjustment 1 million yields indicative regulatory capital 16 million; this is only a bridge, not a conclusion about adequacy absent the specific regime.

For each workpaper consider materiality, disclosure, data quality, presentation, applicable assurance and whether a discovered difference changes an accounting entry. Route underlying accounting recognition/measurement to the governing financial topic. Do not post a journal solely to make a regulatory return or sustainability metric reconcile; document the rule-specific bridge.

## Executed desk scenarios (decision-route QA)

A parent balance is used for a solo regulated entity: FAIL; an intangible deduction changes on an acquisition: PASS only with a refreshed regulatory bridge and specialist sign-off. These checks exercise decision routing only; they do not certify a live entity's filing or a paragraph-level legal conclusion. A production case must collect actual evidence and rerun current-rule verification.

## Dependencies and limitations

TOPIC-07-001 consolidation scope; TOPIC-04-005 intangibles; TOPIC-16-007. `sector-methods.md` supplies four additional regulated-sector routes, source-period gates, and contrary-case calculations. A real filing requires its licence, actual effective instrument and form, waiver/direction, returns and signed input population. These are application inputs; this reusable routing method is proposed REVIEWED-ready for independent technical QA.

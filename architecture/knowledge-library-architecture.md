# Knowledge Library Architecture

Phase 2 populates the knowledge overlays defined here. The CAO knowledge base is **not a substitute publication of accounting standards**. It stores independently authored accounting reasoning, execution logic, source pointers, and professional practice.

## Active framework scope

Initial Phase 2 framework coverage:
- IFRS
- US GAAP
- UK GAAP
- AASB

NZ IFRS is deliberately deferred. The architecture MUST allow frameworks to be added later without redesign.

## Topic-first build model

Knowledge SHOULD be built topic-by-topic across active frameworks rather than completing one entire framework before starting another.

Example:

```text
leases/
  principles/
  IFRS/
  US-GAAP/
  UK-GAAP/
  AASB/
  differences/
```

This allows a topic to become usable end-to-end and makes framework differences explicit.

## Knowledge record types

1. **PRINCIPLES** — framework-independent accounting/operational reasoning.
2. **STANDARDS** — independently authored explanation of applicable framework requirements, linked to authoritative sources.
3. **PRACTICE** — implementation, process, control, evidence, documentation and maturity guidance.
4. **DIFFERENCES** — explicit cross-framework divergence and practical consequences.

## Canonical knowledge record

A framework-sensitive record SHOULD support:

```yaml
knowledge_record:
  id:
  topic:
  subtopic:
  framework:
  record_type: PRINCIPLES|STANDARDS|PRACTICE|DIFFERENCES
  status: draft|reviewed|approved|superseded
  authority:
    standard:
    paragraph_refs: []
    official_source_url:
    source_title:
  effective:
    from:
    to:
    reporting_period_notes:
  applicability:
    entities: []
    transactions: []
    exclusions: []
  cao_explanation:
  requirements_summary: []
  decision_points: []
  inputs_required: []
  judgments: []
  exceptions: []
  accounting_consequences: []
  calculations_required: []
  documentation_expected: []
  controls_considerations: []
  disclosures_considerations: []
  audit_evidence_considerations: []
  common_failure_modes: []
  related_skills: []
  related_records: []
  source_checked_at:
  reviewed_by:
  notes:
```

Records MUST distinguish source-backed requirements from CAO interpretation and practice recommendations.

## IFRS copyright and licensing guardrail

Until a separate IFRS Foundation licence explicitly permits broader use, public repository content MUST follow a conservative model:

- MAY identify IFRS Standards and IAS Standards by name.
- MAY identify specific paragraph/clause references.
- MAY link users to official IFRS Foundation sources.
- MAY contain independently authored explanations, decision frameworks, examples, calculations, journal-entry examples, process guidance, controls, documentation guidance and cross-framework analysis.
- MUST NOT copy or reproduce the body text of IFRS Standards, IAS Standards, IFRIC/SIC Interpretations, Basis for Conclusions, Implementation Guidance, Illustrative Examples, or other IFRS Foundation copyrighted works.
- MUST NOT create close paraphrases that function as a reconstructed substitute for the original copyrighted text.
- MUST NOT store IFRS PDFs or licensed standard text in the public repository.
- MUST NOT scrape, automatically download, index, or ingest IFRS Foundation website content into this repository.
- MUST preserve source references so a professional user can verify the CAO analysis against authoritative literature.
- MUST keep licensed IFRS content, if later obtained, architecturally separable from the open-source knowledge layer.

The user is separately investigating IFRS licensing. A future licence MAY change these implementation constraints; any change MUST be documented before licensed content is introduced.

## Source hierarchy

Knowledge SHOULD distinguish:
1. primary authoritative standard-setter material;
2. official interpretations, agenda decisions and implementation material;
3. regulator material;
4. reputable professional interpretive material;
5. CAO-authored practice guidance.

Lower-level sources MUST NOT be presented as authoritative standards.

## Framework library

```text
standards/<framework>/
  README.md
  framework/
  topics/
  presentation-disclosure/
  effective-dates/
  source-register/
```

## Jurisdiction library

```text
jurisdictions/<jurisdiction>/
  README.md
  entity-reporting/
  filing/
  regulators/
  public-company/
  statutory/
  sustainability/
  assurance/
  source-register/
```

Jurisdiction content MUST NOT duplicate accounting standards merely because the jurisdiction adopts them.

## Industry library

```text
industries/<industry>/
  README.md
  business-models/
  accounting-hotspots/
  operating-processes/
  systems-data/
  controls/
  reporting-disclosures/
  regulatory-interfaces/
  metrics/
  source-register/
```

Industry packs must be deep enough to change how skills execute, not generic primers.

## Differences library

Cross-framework divergence deserves an explicit comparison layer under `standards/differences/`. A differences record SHOULD identify the issue, frameworks compared, practical consequence, effective period, source references, and skills affected. It MUST NOT replace underlying framework sources.

## Review discipline

Every standards-sensitive record MUST have an authoritative source pointer, source-check date, applicable effective period where relevant, and review status. Material changes in authoritative guidance MUST be capable of superseding prior records without deleting history.

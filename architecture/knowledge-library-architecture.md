# Knowledge Library Architecture

Phase 2 populates the knowledge overlays defined here.

## Framework library

Each framework SHOULD use a common topic architecture so skills can request a topic without hard-coding one framework's document structure.

```text
standards/<framework>/
  README.md
  framework/
  topics/
  presentation-disclosure/
  effective-dates/
  source-register/
```

Knowledge records MUST distinguish authoritative source, interpretation, implementation practice, effective date, amendments, and applicability.

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

Cross-framework divergence deserves an explicit comparison layer:

```text
standards/differences/
  leases/
  revenue/
  share-based-compensation/
  development-costs/
  impairment/
  financial-instruments/
  inventory/
  provisions/
  business-combinations/
  presentation-disclosure/
```

A differences record SHOULD identify the issue, frameworks compared, practical consequence, effective period, source references, and skills affected. It MUST NOT replace the underlying framework sources.

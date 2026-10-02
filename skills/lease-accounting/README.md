# Phase 3 lease accounting skill

SKILL-LEASE-001 v1.0 is the first production skill package. It is a bounded lessee vertical slice, not a general lease-management application.

## Implemented
- governed framework/period/entity intake and fail-closed case validation;
- fixed end-period payment PV, initial ROU bridge and liability rollforward using Decimal arithmetic;
- IFRS/AASB and ASC 842 finance ROU depreciation/amortization route;
- ASC 842 operating single-cost/ROU-reduction route for the supported no-adjustment case;
- balanced commencement and subsequent journal pack;
- approved claim retrieval from canonical topic registers;
- specific standard/paragraph citations where established, with source-assurance limitation retained for current ASC Codification access;
- UK revised-Section-20 effective-period gate and AASB entity/tier gate;
- modification/reassessment router that calculates supported remeasurements and blocks scope decreases requiring specialist accounting;
- sale-and-leaseback specialist handoff;
- curated public-output adapter using the repository privacy/output boundary;
- reviewer checklist, JSON case schema, executable CLI example and CI regression suite.

## Intentional boundaries
The skill does not infer contract facts, lease identification, lease term, discount rate, US classification, elections or materiality. Those are approved inputs/reviewer judgments. It does not implement lessor accounting. Pre-2026 UK GAAP, sale-and-leaseback, scope-decrease modifications, ASC 842 operating leases with opening ROU adjustments, impairment and unusual payment structures route to specialist review rather than receiving fabricated generic accounting.

Run the example internally with `python skills/lease-accounting/run.py skills/lease-accounting/examples/basic-ifrs-case.json`; add `--public` to exercise the curated answer boundary. Run tests with `python -m unittest discover -s skills/lease-accounting/tests -p 'test_*.py'`.

Production means the declared bounded skill contract is executable and regression-tested. Each real accounting case still requires the reviewer gate in `checklists/reviewer.md`, and integration into a future CAO application remains a separate Phase 3 application task.

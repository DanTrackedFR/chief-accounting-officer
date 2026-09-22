# Company Accounting Memory

Company Accounting Memory is the durable institutional memory of the CAO. It MUST NOT rely on conversation history.

## Durable stores

1. **Company Context** — what is true now.
2. **Accounting Case Library** — conclusions, judgments, and historical positions.
3. **Artifact Library** — source documents and finished accounting artifacts.
4. **Provenance / History** — where knowledge came from, what changed, and when.
5. **Decision Register** — why material accounting, process, system, and control decisions were made.

Company Context covers Corporate Profile, Reporting Profile, Accounting Function, Systems & Data, Policies & Positions, and Controls & Evidence.

## Knowledge status

Durable knowledge supports `OBSERVED`, `CONFIRMED`, `DOCUMENTED`, `APPROVED`, `PROPOSED`, and `SUPERSEDED` states. A proposal MUST NOT silently overwrite an approved position.

## Temporal requirements

Where applicable, memory preserves current state, previous state, effective date, decision date, learned date, source/evidence, approver/confirmer, reason for change, related cases/artifacts and supersession.

`effective_date` and `learned_date` are distinct. Unknown historical dates remain uncertain rather than fabricated.

The `/memory` directory contains Phase 1 structural schemas. Persistence technology and application code are deliberately deferred.

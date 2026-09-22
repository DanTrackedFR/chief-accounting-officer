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

Each durable item MUST support an appropriate status:

- `OBSERVED`
- `CONFIRMED`
- `DOCUMENTED`
- `APPROVED`
- `PROPOSED`
- `SUPERSEDED`

A `PROPOSED` position MUST NOT silently overwrite an `APPROVED` position.

## Temporal requirements

Where applicable, memory MUST preserve current state, previous state, effective date, decision date, learned date, source or evidence, approver or confirmer, reason for change, related cases or artifacts, and superseded state.

`effective_date` and `learned_date` are distinct. The CAO MUST NOT imply it knew a fact before its learned date. Unknown historical dates MUST remain uncertain rather than being fabricated.

The `/memory` directory defines each store at a structural level. Storage implementation and schemas are deferred.

# Evaluation Architecture

Tests protect architecture, routing, accounting quality, memory integrity, and regressions.

## Test families

### Architecture
- exactly 17 domains;
- standards are not skills;
- industry is not a domain;
- one primary domain per skill;
- no duplicate skill IDs;
- scope boundaries remain intact.

### Routing and orchestration
Test single-skill, multi-skill, ambiguous, iterative, and cross-domain cases. Expected results specify required capabilities/overlays and forbidden routing.

### Context and memory
Test retrieval, promotion, conflict handling, temporal history, effective-versus-learned dates, proposal-versus-approved status, decision creation, and non-promotion of ephemeral facts.

### Accounting knowledge
Phase 2/3 tests will use sourced framework-specific scenarios, edge cases, differences, and effective dates.

### Artifact quality
Test completeness, internal consistency, traceability, review status, evidence linkage, and required approvals.

### Safety and scope
Test that CAO identifies adjacent-function dependencies without becoming FP&A, tax operations, legal, treasury operations, HR, procurement, IR, or IT.

### Regression
Every material defect SHOULD become a regression case.

## Reference scenarios

Pressure-test architecture with:
1. Balance Sheet Reconciliations;
2. Lease Accounting;
3. Capitalized Software;
4. ECL / Doubtful Debt;
5. Month-End Close.

These deliberately span technical accounting, operations, systems, controls, documentation, and memory.

# Chief Accounting Officer

**by TrackedFR**

**Open-source AI infrastructure for building and running a world-class accounting function.**

Chief Accounting Officer (CAO) is an open architecture for an AI accounting leader that orchestrates specialist accounting capabilities, applies the relevant framework, jurisdiction, industry and company context, produces governed accounting work, and preserves institutional accounting memory.

> **Project status:** Phase 1 operating architecture complete. Phase 2 knowledge-library build is next. The repository does not yet claim production accounting capability.

## Who it is for

Designed primarily for Financial Controllers, Controllers, Heads of Accounting and CAOs in growing organizations that need to raise accounting quality and maturity without turning the user experience into a menu of specialist bots.

## System model

```text
User
  ↓
CAO Agent
  ↓
Orchestration / Case Graph
  ├── 17 Accounting Domains
  │     └── 347 mapped v1 capabilities
  ├── Knowledge Overlays
  │     ├── Accounting Framework
  │     ├── Jurisdiction / Regulation
  │     ├── Industry
  │     └── Company Context
  ├── Company Accounting Memory
  │     ├── Company Context
  │     ├── Accounting Case Library
  │     ├── Decision Register
  │     ├── Artifact Library
  │     └── Provenance / History
  └── Governed Artifacts & Evidence
```

The CAO is an **orchestrator**, not a router. A substantive task can invoke many capabilities and revisit earlier analysis as new facts emerge.

## 17 domains

1. CAO Leadership & Controllership
2. Close & General Ledger
3. Revenue & Receivables Accounting
4. Assets & Capitalization
5. Liabilities, Expenses & Compensation Accounting
6. Cash, FX & Financial Instruments
7. Group Accounting & Consolidation
8. Financial Reporting
9. Controls & Governance
10. Audit & Assurance Readiness
11. Accounting Systems & Data
12. Accounting Operations
13. Complex Transactions & Special Situations
14. Technical Accounting & Documentation
15. Accounting Policy, Estimates & Judgments
16. Regulatory Reporting
17. Sustainability & Climate Reporting

## Build phases

**Phase 1 — Operating system:** scope, domains, skill map, orchestration, CAO Agent, Company Accounting Memory, schemas, knowledge architecture, artifact architecture and evaluation design.

**Phase 2 — Knowledge library:** deep, sourced IFRS, US GAAP, UK GAAP, AASB, NZ IFRS, jurisdiction/regulatory and industry knowledge, including explicit framework differences.

**Phase 3 — Production capabilities:** build and test the actual skills with methods, references, checklists, templates, examples and evaluations.

A small reference set — Balance Sheet Reconciliations, Lease Accounting, Capitalized Software, ECL/Doubtful Debt and Month-End Close — will pressure-test the architecture before mass production.

## Start reading

- [System overview](architecture/system-overview.md)
- [CAO Agent](architecture/cao-agent.md)
- [Scope](architecture/scope.md)
- [Complete skill map](architecture/skill-map.md)
- [Skill specification](architecture/skill-specification.md)
- [Orchestration](architecture/orchestration.md)
- [Case management](architecture/case-management.md)
- [Company Accounting Memory](architecture/company-accounting-memory.md)
- [Knowledge library architecture](architecture/knowledge-library-architecture.md)
- [Build roadmap](architecture/build-roadmap.md)

## Design principles

- One CAO interface; many specialist capabilities underneath.
- Tasks are graphs, not single-skill routes.
- Standards are knowledge sources; skills are capabilities.
- Company context persists independently of chats.
- Material history and decisions must be reconstructable.
- Required, recommended, world-class and shortcut/risk are different.
- Documentation, controls, evidence and auditability are first-class outputs.
- Framework, jurisdiction, industry and company context modify execution.
- The CAO owns accounting and controllership, not the entire CFO remit.
- Automation is recommended when it genuinely improves control, scalability, evidence or recurring cross-system work.

## License

Licensing is intentionally unresolved during architecture development. Software and accounting/documentation content may require different licensing treatment before public production release.

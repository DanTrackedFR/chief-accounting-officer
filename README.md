# Chief Accounting Officer

*by TrackedFR*

**Open-source AI infrastructure for building and running a world-class accounting function.**

## What this is

Chief Accounting Officer is the foundation for a user-facing CAO Agent. The agent is intended to help accounting leaders design, operate, document, and improve an accounting function. It will orchestrate capabilities across accounting domains while preserving company context, evidence, decisions, and history.

This repository currently defines the operating architecture. It does not yet provide production software, detailed accounting skills, accounting conclusions, or authoritative accounting guidance.

## Who it is for

- Chief Accounting Officers and Controllers
- Accounting and finance operations leaders
- Technical accounting, reporting, controls, and systems teams
- Contributors building governed AI infrastructure for accounting

## Architecture

`CAO Agent → Orchestration → Domains → Skills → Methods / Knowledge / Artifacts`

The CAO Agent is an orchestrator, not a skill selector. A substantive task may combine multiple skills and knowledge sources in a dynamic workplan graph. Domains organize capabilities; they are not isolated agents or workflows.

Four overlays modify how capabilities operate: accounting framework, jurisdiction and regulation, industry, and company context.

## Build phases

1. **Foundation and operating architecture** — define scope, domains, orchestration, knowledge, maturity, and durable company memory.
2. **Capability and knowledge design** — define the skill taxonomy, contracts, methods, knowledge structures, and validation requirements.
3. **Implementation and evaluation** — build executable capabilities, governed memory, artifacts, tests, and quality controls.

## Current status

Phase 1, Batch 1 establishes the foundation and repository architecture. Detailed skills, standards content, industry content, calculations, templates, examples, and application code are deliberately deferred.

## Start reading

1. [System overview](architecture/system-overview.md)
2. [Scope](architecture/scope.md)
3. [Domains](architecture/domains.md)
4. [Orchestration](architecture/orchestration.md)
5. [Company Accounting Memory](architecture/company-accounting-memory.md)
6. [Terminology and normative language](architecture/terminology.md)

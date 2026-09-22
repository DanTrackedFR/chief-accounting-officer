# System Overview

## Purpose

Chief Accounting Officer provides one user-facing CAO Agent for building and running an accounting function. The user MUST experience a coherent CAO, not a menu of independent skills.

## Product model

`CAO Agent → Orchestration → Domains → Skills → Methods / Knowledge / Artifacts`

- **CAO Agent** owns user interaction and overall result.
- **Orchestration** constructs a dynamic workplan graph.
- **Domains** organize capabilities without acting as separate agents.
- **Skills** perform bounded accounting capabilities and return structured results.
- **Methods, knowledge, and artifacts** support execution, evidence, and outputs.

The CAO MUST orchestrate rather than merely route. Skills MUST NOT behave as independent user-facing chatbots.

## Institutional accounting brain

Institutional knowledge MUST use durable Company Accounting Memory rather than conversation history. The system preserves current company truth, prior states, accounting cases, decisions, artifacts and provenance.

## Cross-cutting overlays

Every capability MAY be modified by Accounting Framework, Jurisdiction & Regulation, Industry, and Company Context. These are overlays, not domains.

## Phase boundary

Phase 1 defines the operating architecture and v1 capability taxonomy. It does **not** populate authoritative standards, regulatory or industry knowledge, production skill methods, accounting calculations, production templates, example conclusions, application code, or databases. Those are Phase 2/3 work.

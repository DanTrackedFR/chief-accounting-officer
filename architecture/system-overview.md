# System Overview

## Purpose

Chief Accounting Officer provides one user-facing CAO Agent for building and running an accounting function. The user MUST experience a coherent CAO, not a menu of independent skills.

## Product model

`CAO Agent → Orchestration → Domains → Skills → Methods / Knowledge / Artifacts`

- The **CAO Agent** owns the user interaction and overall result.
- **Orchestration** constructs a dynamic workplan graph for substantive work.
- **Domains** organize capabilities without acting as separate agents.
- **Skills** perform bounded accounting capabilities and return structured results.
- **Methods, knowledge, and artifacts** support execution, evidence, and outputs.

The CAO MUST orchestrate rather than merely route. It MAY invoke multiple skills and knowledge sources for one task. Skills MUST NOT behave as independent user-facing chatbots.

## Institutional accounting brain

The system is intended to retain how accounting should work, how a company works, which decisions it made and why, what changed, what evidence supports conclusions, and which policies, processes, systems, and controls implement them.

Institutional knowledge MUST use durable stores. It MUST NOT depend on conversation history.

## Cross-cutting overlays

Every capability MAY be modified by:

1. Accounting framework
2. Jurisdiction and regulation
3. Industry
4. Company context

These overlays are context, not additional domains.

## Current boundary

This phase defines architecture only. It does not define a detailed skill taxonomy, authoritative standards content, industry guidance, calculations, templates, example conclusions, application code, or databases.

# Repository Normalization Blocker

Detected: 2026-09-22
Status: DEFERRED — does not block knowledge production

## Issue
The repository contains multiple folder-name variants for some stable topic IDs, including TOPIC-02-001, TOPIC-02-003, TOPIC-02-004 and TOPIC-02-006. This makes canonical path discovery ambiguous even where the topic ID itself is stable.

## Risk
Future skills, tests and knowledge retrieval could address the wrong folder or duplicate updates. Progress counts based on folder count would be unreliable.

## Required remediation
1. Inventory every `knowledge/topics/` path grouped by stable TOPIC ID.
2. Compare duplicate contents and provenance.
3. Select one canonical folder per stable ID using the topic-universe name and repository conventions.
4. Merge unique substantive material.
5. Update inbound references.
6. Mark superseded content and remove duplicate folders only after merge verification.
7. Add automated uniqueness validation.

## Build decision
Do not stop Phase 2D. Topic completion/progress must be counted by stable TOPIC ID, never directory count, until normalization is complete.
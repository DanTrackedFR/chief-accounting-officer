# Internal source notes and approval

Source notes are internal metadata, not user-facing guidance. A direct-source claim uses `Source: [named source]`; a model-derived claim uses `Source: ChatGPT training data`. Never present a model-derived claim as independently verified current authority.

A model-derived claim can be marked `MODEL_CHECKED` only after independent accuracy review, framework-specific boundary tests, effective-period checks, and conflict review. `MODEL_CHECKED` is distinct from `SOURCE_VERIFIED`. Preserve existing evidence statuses and the authority-based APPROVED gate until an explicit schema and approval-policy change is reviewed and merged.

The user-facing tool must exclude internal source notes and provenance fields from answers, citations, retrieval snippets, and exports. Material uncertainty and period limitations must still be disclosed. Implement automated tests of these output paths before asserting that source notes are hidden.

This file specifies a proposed contract. It does not establish that a renderer exists, tests have passed, or any topic qualifies for APPROVED.

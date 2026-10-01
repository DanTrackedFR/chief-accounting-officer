# Internal source-note policy and application implementation requirement

For directly used, inspected source material, store `Source: [named source]` (publisher/standard name, not a website). For training-data-derived material, store exactly `Source: ChatGPT training data`. Notes belong in internal claim metadata and must not be embedded in public topic prose.

The application must use an explicit allowlist for user-visible accounting content. Exclude `source_note`, `approval_track`, `evidence_status`, `audit_required`, reviewer identities, raw claim registers and other internal provenance from all answer generation context, retrieval snippets, citations, logs exposed to users, downloads and exports. A prompt alone is not an adequate security boundary. Disclose material accounting limitations and uncertainties in ordinary guidance.

Before release, automated tests must feed both source-note forms through each response and export route, assert neither note nor internal provenance is emitted, and confirm substantive accounting caveats remain. The repository README currently identifies Phase 3 as the production capability build; until a runnable application and its renderer are identified, this is a required contract and **not a verified runtime control**.

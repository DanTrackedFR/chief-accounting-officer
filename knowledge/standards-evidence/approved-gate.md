# APPROVED gate — two-track evidence policy

Effective 2026-10-01. This supersedes the previous requirement that every normative claim must be SOURCE_VERIFIED to approve a topic. APPROVED is a completed, independently checked topic workflow status, **not** a representation that every claim was directly verified against an operative standard.

## Evidence tracks
1. **Direct-source track:** where the information actually used in guidance is available and was directly inspected, independently recheck its accuracy, framework, period and scope. Store internal note `Source: [named source]`, e.g. `Source: FRC FRS 102`. Preserve SOURCE_VERIFIED only when the operative current authority and exact provision were inspected; otherwise retain the accurate corroboration status.
2. **Training-data track:** when information was unavailable or gated and the guidance was drafted from ChatGPT training knowledge, independently recheck the accounting conclusion, numerical examples, framework distinctions, boundary cases and effective-period caveats. Store internal note `Source: ChatGPT training data`. A successful second-pass model review is an accuracy check, not direct authority verification. Preserve `MODEL_DERIVED_AUDIT_REQUIRED` and set the independent `approval_track: TRAINING_DATA_CHECKED` only after recorded review; keep `audit_required: true` for later direct-source assurance.

## Topic promotion
A REVIEWED topic may become APPROVED only after (a) full normative-claim coverage or a documented non-normative scope decision; (b) every material claim passes one of the two tracks, with evidence and limitations recorded; (c) applicable jurisdiction, entity scope and effective-period risks are checked or explicitly qualified; (d) no unresolved material conflict or unsupported precise paragraph reference; (e) cross-framework/adversarial and numerical regression passes; (f) rights compliance; and (g) independent controller sign-off. A model-only check with no independent challenge or corroboration is insufficient.

Keep source provenance and authority assurance separate from topic status. APPROVED topics with training-data claims retain an open direct-source audit queue. Do not claim that APPROVED means SOURCE_VERIFIED. Controller updates the canonical manifest first, then progress and roadmap.

## User-facing privacy
Internal source notes and evidence labels must not be shown to users in answers, citations, retrieval excerpts, tool outputs or exports. The application must enforce this with allowlisted output fields and tests; a documentation rule alone is not proof. Do not conceal substantive uncertainty, effective-period limitations or unresolved risks.

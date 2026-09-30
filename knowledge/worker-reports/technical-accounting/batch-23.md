# Batch 23 — Domain 03 source and reusable-method remediation (28 September 2026)

Canonical IDs: TOPIC-03-001–005. Capabilities: CAO-03-001–011. Existing packs, duplicate/retry folders and tests retained without destructive edits. One additive workpaper per canonical topic:

| Topic | New file under its canonical folder | Gap addressed | Residual |
| --- | --- | --- | --- |
| 03-001 | `practice/period-and-authority-check-2026.md` | Framework/period selection, linked-contract and option allocation, reversal cases, controls | Live ASC Basic View paragraph verification; operative post-June-2026 AASB compilation; independent QA |
| 03-002 | `period-source-and-estimate-protocol.md` | IFRS/AASB allocation paragraph route, estimate change, backtest and adverse allocation | ASC exactness, UK edition-specific exception comparison, later AASB and independent QA |
| 03-003 | `period-source-and-right-to-payment-protocol.md` | Enforceable payment, progress, input exclusions, modification gate | ASC exactness, UK/AASB operative edition and independent QA |
| 03-004 | `period-source-and-control-protocol.md` | Specified-promise control, gross/net and contract-balance reconciliation | ASC exactness, UK/AASB operative edition and independent QA |
| 03-005 | `period-source-and-acceptance-protocol.md` | Acceptance versus control, conditional right, concession/credit handoff | ASC exactness, UK/AASB operative edition and independent QA |

Official source check: IFRS Foundation 2025 issued IFRS 15 HTML (contract combination 17; variable allocation 84–86; over-time 35–37 and right to payment B9–B13; principal/agent B34–B38; customer acceptance B83–B86), FRC FRS 102 register (Periodic Review 2024 principal commencement 1 January 2026), AASB 15 December 2022 compilation (annual starts 1 January 2023 to before 1 July 2026). These snapshots are not a substitute for the operative later Australian edition or the US current paragraph check. The Basic View portal did not return current paragraph content in the attempted browser session; **there is no copyright-based bar to citation**. Do not claim Basic View verification from a third-party excerpt or a FASB amendment PDF.

Regression: re-performed option SSP allocation 110.38 + 59.43 + 10.19 = 180; B-specific estimates 540 + 460 = 1,000 and 540 + 520 = 1,060; gross/net 120 − 90 = 30. Five arithmetic assertions pass. Narrative adverse cases were added to each workpaper but not independently executed against a production corpus. Result: five topics advanced, **all five remain PARTIAL**. No canonical status promotion, shared manifest/progress/roadmap change, or other worker-domain mutation. The merged PR #1 cannot be updated; commits remain on `worker/technical-accounting` for follow-on review.

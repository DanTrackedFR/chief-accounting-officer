# Stage 3 integration handoff

Stage 3 composes intercompany matching and governed framework/currency chains with the current live-main Stage 1/2 substrate reconstructed in `STAGE3-ARCHITECTURE-RECONSTRUCTION.md`. One integration branch and PR #36 contain the complete bounded implementation. Do not merge automatically; the final immutable head, required CI and ready-for-review state are recorded on that PR.

Read `interfaces/intercompany-framework-currency.md` for implemented contracts and `MULTI-ENTITY-STAGE3-TO-STAGE4-HANDOFF.md` for the next-stage boundary. No production accounting owner was replaced. The supported conversion is the native ordinary-loan IFRS reassessment after native EUR translation, with zero framework adjustment; unsupported general conversions remain unresolved.

The ordinary CAO proof preserves eight legal transaction sides, four explicit relationships, distinct business and execution graphs, current native owner bindings and the unresolved residual. The upstream correction replaces one legal result and selectively refreshes six actual consumers. Old versions remain superseded history, unrelated relationships remain current, and exact-once legal versus Group journals remain distinct. The aggregate Case intentionally remains partial.

`STAGE3-INDEPENDENT-QA.md` records eleven independently demonstrated findings, remediation and a fresh 24-test independent acceptance rerun. `STAGE3-RELEASE-REGRESSION.json` records the distinct repository suites, validators, migrated flagships and deterministic generator evidence. Reruns are not added to distinct test counts. All prior flagship artifacts regenerate without changes. Optional economic qualification is omitted from legacy node serialization.

The four-stage workstream remains IN PROGRESS. Stage 3 is COMPLETE subject to owner integration; Stage 4 is NEXT after merge. Durable persistence is NOT YET NEXT. No Stage 4 integration flagship is built here.

# Remediation checkpoint 2 — not release acceptance

Parent published checkpoint: 3d8458eac0defdc52f7644638d12c9fe98af4c90. Diagnostic baseline: 4cb7018d0ff2dbb5951954278dac4ff9927630e6.

Actual runtime diagnostic result: 19/19 methods pass, no failures/errors/skips (runtime.log). Mandatory historical verifier returns 8,912 preserved entries. No historical evidence bytes were edited.

Fresh accounting QA exposed four further boundary failures (retained under accounting-qa); corrections are now present but independent final rerun remains pending. Fresh engineering runtime boundary QA passed 12/12. These are focused remediation checks, not a new full release receipt.

Governance candidate adds mandatory version-2 inventories, explicit refusal under optimized Python, and a separate focused-governance-qa-v1 verifier. Governance positive/tamper tests must still run against the committed candidate with CAO_GOV_REF and CAO_GOV_FOCUSED=1. GOV-01/GOV-02 remain pending until that evidence and independent QA pass. The old 3,844-test acceptance pointer is untouched and cannot certify the modified source.

## Diagnostic harness adaptation

Original runtime tests remain unchanged. governance.py keeps its historical default and adds explicit focused mode for corrected candidates: issue a new receipt from actual execution of the 19 HTTP methods, verify it before ANY tampering, then exercise the same original sidecars and optimized historical verifier. This is required because the historical receipt's source hashes cannot legitimately match corrected production code. Focused mode invokes the SAME inventory validator as release acceptance and never returns release_accepted=true. It replaces the historical 3,844-count assertion with explicit focused scope; it does not pretend to rerun those tests.

## New evidence contract for the later release agent

The full release verifier requires a schema_version=2 pointer that binds an evidence_inventory path and SHA-256. The inventory binds the authoritative manifest, every file in its attempt directory, all command/shard logs, start maps, suite receipts, the conventional outer log, and attempt-local receipt-review.md. Start maps must equal tested maps; suite sidecars must match manifest suite records. Paths must be repository-relative regular files without symlink redirection. The inventory must be outside the attempt directory to avoid a self-hash cycle. After actual full regression and independent receipt review, seal_inventory in skills/presumed-sources/receipt_integrity.py can issue a NEW inventory/pointer. Do not backfill or overwrite historical pointers, receipts, reports, or attempt directories. The historical verifier version remains available at its original commit for historical evidence checks.

The pointer/source revision is the trusted root: inventory hashing detects changes beneath that root and structural checks reject required-class omissions. It is not a signature or protection against wholesale replacement of trusted code and pointer. Review identity/authority remains an independent acceptance responsibility.

## Runtime contract clarifications

Source Case IDs and row IDs: nonblank strings, at most 256 characters. Source IDs: at most 8,192 characters; public finding references exceeding 256 characters are SHA-256-derived display references, with original native lineage retained. Source version: at most 256 characters. Maximum 200 supplied rows across Profile 1.2 populations combined. Invalid bounds are qualified/rejected without financial effects; material findings are not dropped. Schema documents individual bounds and runtime enforces combined population limit.

Disposal enabled/ordinary_sale/cash_received must be literal booleans when present. Cash receipt must be explicit and consistent with supplied terms; supported unpaid credit consideration uses disposal receivable. Unresolved settlement qualifies the affected dependency group. Payment detail must reconcile to aggregate, respect supplied date/currency/entity evidence, and cannot establish bank confirmation. Invalid balance evidence does not erase independent invoice work.

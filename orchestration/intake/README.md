# Semantic and intake foundation

`Intake.prepare(objective, sources, company_records, scope, conversation=())`
inventories inert raw references, extracts structured fields with locations,
passes normalized inventory/context/registry to an injected SemanticPlanner,
validates the proposal and returns candidates, transformations, conflicts,
material questions, proposed memory records and owner input candidates.

`Intake.execute(prepared, ReviewedInputPack(...))` verifies source/currentness and
sealed preparation, exact field bindings and separately supplied reviewed native
workpapers, then invokes existing CAO through GovernedPlanner. With no reviewed
pack, the workplan remains blocked at existing owner source requirements. A pack
is not a reviewer approval: production.assess_case still enforces native source,
knowledge, effective-period and exact-case certification gates.

A future model adapter implements `propose(RequestContext)`. The request includes
objective, conversation, normalized sources, Company Context and current Registry.
Return `StructuredProposal`, or decode JSON via its strict `from_record` method.
Each semantic assertion is a Claim(value,status,confidence,rationale,evidence).
No CI network or model call is used. FixturePlanner simulates arbitrary model
output, rather than routing by user-objective keywords.

## Proposal and validation

The contract includes objective/output, primary/secondary/supporting modes,
entities/periods/frameworks/jurisdictions, source classifications, column mapping
candidates, issues with candidate owners/dependencies, facts, assumptions,
disputes/missing facts, hypothesis tests, context candidates and bounded owner.
Every assertion carries EXTRACTED/OBSERVED/INFERRED/USER_STATED/CONTEXT_DERIVED/
CALCULATED/ASSUMED/DISPUTED/UNRESOLVED. Approval is not a semantic status.

Validation rejects unknown/NONPRODUCTION owner IDs, invalid work modes,
frameworks, dates/dimensions, references, contradictory sourced values, missing
assumption disclosure, impossible confidence/status, unsafe transformation,
economic aliases, dependency cycles, unsupported issues and missing diagnostic
owner. Invalid proposals return structured blocking error codes; source/model
text is not echoed in public errors. Supplied owner imports independently add
required dependencies; model proposals cannot delete them.

Source classification uses the listed accounting families, with classified,
probable, ambiguous and unknown certainty. A label is a proposed interpretation;
filenames are never accounting metadata. Column mappings retain original field,
proposed normalized name, confidence/evidence and status. No semantic account
classification or actual-versus-budget conversion is automatic.

## Formats and security

Supported: flat JSON row arrays; nested bounded JSON objects; strict CSV/TSV;
plain text/Markdown paragraph blocks; normalized_workbook `{sheets:[{name,rows}]}`;
normalized_document `{blocks:[{id,text,page?,section?}]}`.

Unsupported: native XLS/XLSX, PDF/DOCX, images/scans/OCR, arbitrary delimited
formats/encodings. An external extractor must supply normalized text/tables.
Formulas remain inert strings and fail numeric normalization; macros/scripts are
never executed. No path is opened from a supplied filename. Bounds:2MB payload,
10,000 rows,12 nesting levels; source/block/table/field identities are bounded.
Malformed rows, duplicate file IDs/content and nested table cells fail closed.
Zeros, signs, duplicate economic-looking rows and subtotal rows are preserved.

RawSource is separate from Extraction, which is separate from FactCandidate.
Metadata retains supplied entity/period/currency/version/as-of/system/extracted-at,
supersession and unresolved dimensions; no upload timestamp chooses truth.
Fingerprints bind original payload and extracted cells. Inventory.verify reextracts
and checks the entire representation before use, including metadata and locations.
Fields retain file ID, table/sheet,row,column,record ID or document block/page/
section, original value and fingerprints. No copied document text enters answers.

## Transformations, facts and context

Only explicit identity, decimal parsing and unambiguous ISO date normalization
are supported. Each material normalization records ID, exact input fields,
input fingerprints, method, output and reason. No conversion, netting,
aggregation, estimation, sign inversion or deduplication is performed.

Numeric controlled-export rows can establish source facts only if confidence>=.95,
no confirmation required, source dimensions agree and entity/period/comparator
are complete. This does not establish accounting classification/reliability or
causality. Contract wording remains a candidate requiring owner review. Inferred
claims never promote. Assumptions remain assumed; declared/observed contradictions
remain disputed. Version/fingerprint and effective dates stay visible internally.

Conflicting same-scope semantic metrics preserve all alternatives. Context
conflicts produce PROPOSED memory candidates and blocking questions; APPROVED
history is unchanged. Material blocking, confirmation and nonblocking questions
are distinct. Known scoped context and established source facts suppress redundant
model questions. Unresolved owner judgments remain visible.

## Owner execution and diagnostics

Owner candidates include source mappings, available/required/missing fields,
transformations, unresolved judgments, actual registry input descriptions and
native qualification requirements. They are not certified owner cases.
ReviewedInputPack uses explicit Binding(fact_id,owner,path,kind). Exact candidate
values must equal native inputs. Disputed/inferred sources cannot bind. Current
and comparator bindings are separate; comparator dates/kind/document must match
Analytics and cannot become current actual. Established selected-owner facts
must all have reviewed mappings. Changed inputs fail existing fingerprints.

Generic hypothesis tests compare numeric governed owner/result paths using
explicit supported operators and factors. They return SUPPORTED, REJECTED,
PARTIALLY_SUPPORTED or UNRESOLVED with retained evidence. This is bounded evidence
testing, not statistical causality or accounting authority. No prose keyword
selects an owner. Inventory/Revenue/etc still make accounting determinations.

`Intake.public` uses existing CAO/public_record and all seven routes. Internal
raw content, provenance, hashes, model rationale/confidence and reviewer identity
remain internal. Conflicts, missing work and scoped hypothesis limitations survive.

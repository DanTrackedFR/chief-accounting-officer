# Run the CAO locally with Claude Code

Requires Python 3.12+, a durable local Linux/macOS filesystem, Git and your own
installed Claude Code. Accounting needs no API credentials or Python packages.
Claude Code's own installation/account requirements are separate. Windows users
should use WSL; the local lock uses POSIX flock. No hosted service is started.

```sh
git clone https://github.com/DanTrackedFR/chief-accounting-officer.git
cd chief-accounting-officer
git checkout mvp/local-cao-execution-contract
python3 --version
mkdir -m 700 .cao-local
cp company-context.example.md .cao-local/company-context.md
```

Edit the copy: company_id is an enduring company key; entity_id is a legal-entity
key, calendar_id an enduring reporting-calendar key. Neither is a display name.
Use ISO dates and reporting codes. Fill required execution fields; leave unknown
optional information UNKNOWN. Store real evidence under .cao-local/evidence/.
Keep each company's workspace separate. Default workspace and all company-context
files are Git-ignored. Custom workspaces must also be ignored before use.

Initialize and diagnose using JSON on stdin (one request, one response):

```sh
printf '%s\n' '{"contract_version":"1.0","operation":"initialize","company_id":"synthetic-demo-001"}' | python3 -m local_cao
printf '%s\n' '{"contract_version":"1.0","operation":"diagnose","company_id":"synthetic-demo-001"}' | python3 -m local_cao
printf '%s\n' '{"contract_version":"1.0","operation":"capabilities","company_id":"synthetic-demo-001"}' | python3 -m local_cao
claude
```

Ask: “Read my local company context. How should we recognize revenue from this
new customer agreement? Start a governed CAO Case and tell me what is missing.”
Claude should call start with your objective, a fresh request_id and the discovered
customer_contract fact family, then relay public_result's requirements. No contract
means no revenue conclusion. “Our prepayments have jumped this month. Investigate”
should request reconciliation workpapers and comparative financial data; the
native bounded investigation cannot invent a specific invoice anomaly.

Example start:

```json
{"contract_version":"1.0","operation":"start","company_id":"synthetic-demo-001","request_id":"contract-review-001","objective":"How should we recognize revenue from this new customer agreement?","target_family":"customer_contract"}
```

Keep returned case_id exactly. Ask Claude to prepare operation envelopes, not
complex accounting data. A finance workpaper still must satisfy its actual native
input/source/review contract: the local client cannot make a raw contract approved.
Registered skill input descriptions aid selection; read the relevant native
controlled workpaper contract locally. This build does not convert arbitrary
finance spreadsheets into qualified owner workpapers.

Submit a workspace-relative controlled JSON workpaper containing `facts` plus any
native qualified handoffs/challenge/journal review required by its calculation:

```json
{"contract_version":"1.0","operation":"submit","company_id":"synthetic-demo-001","case_id":"RETURNED_CASE_ID","evidence_file":"evidence/reviewed-workpaper.json"}
```

Then call execute, status/questions, result or resume with that same company and
case_id. list enumerates company-local staged and executed Cases. status returns
native outcome, lifecycle, curated answer and minimal owner/state workplan. Exit0
means the operation succeeded, not that the accounting is complete; inspect
execution_state/currentness/public_result. Exit2 means a structured safe error.

Evidence submission is immutable; an identical retry acknowledges it. After a
checkpoint, execute loads the original result instead of recalculating. Initial
empty-evidence previews are request staging only, not completed durable Cases;
first evidence can still be submitted. Partly executed work remains a native
partial checkpoint. Changing a submitted workpaper is not silently accepted;
qualified selective correction/rework is native functionality that a later facade
extension must expose with sealed intake/review bindings. Keep old Case history;
use a separately identified new Case when this build cannot continue safely.

Changing execution dimensions in context rejects existing-Case access. Restore
the original dimensions to resume it; for another entity/period, use a separate
workspace copy or start before changing scope. Narrative enrichment does not
approve policies. A calendar key does not establish a verified fiscal start;
the native compatibility calendar retains an unspecified fiscal start.

Back up a closed workspace/database or use SQLite consistent backup. Do not copy a
live database without its journal transaction state. Do not delete requests or
checkpoint state to resolve an error. Workspace input files and DB are private,
unencrypted local data; host filesystem permissions govern access. The adapter
rejects absolute evidence paths, traversal and symlink components. It never reads
cloud URLs or executes source text. This is a trusted local environment, not
authenticated multi-tenant security.

## Reproducible synthetic smoke test

```sh
python3 -m unittest discover -s local_cao/tests -p 'test_*.py'
python3 -m local_cao.tests.prove_cli
```

The proof uses existing independently labelled synthetic reviewed workpapers:
fixed-assets depreciation EUR90,000; AP accrual EUR9,600. Every operation is a fresh
CLI process. Both persist/resume/retry; two missing-evidence questions produce no
completed answer. These are test approvals, not real authenticated reviewers.
Claude prompts to validate manually: “Run the synthetic smoke proof and explain
its public results”; “Resume the Case without rerunning accounting”; “Show the
questions for the revenue Case”; “Can I mark my Markdown policy APPROVED?”
Actual live Claude Code execution was unavailable in this development environment
and still requires owner validation. CLI proof is not a live Claude test.

## Build3 context, documents and investigation

Install `python -m pip install -r intelligence/requirements.txt`. Use additive
`investigate`, `document`, `continue_investigation`, `investigation` operations on the
same JSON CLI. Natural-language objectives require an existing family or validated
structured interpretation/provider. Preserve request_id/event_id and exact document
id/version; retries are immutable. Use `submit` with native proposal/pack/sources,
then `execute`; extracted files alone never authorize accounting. New evidence after
execution requires `correct_investigation`/`rework_investigation`. Resume restores the
same snapshot/history. See interfaces/CAO-CONTEXT-EVIDENCE-DOCUMENT-CONTRACT.md for
bounds, parser warnings and authority distinctions. No live model provider is shipped.

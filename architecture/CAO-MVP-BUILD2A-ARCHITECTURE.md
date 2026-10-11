# CAO MVP Build 2A architecture reconstruction

Verified live main: b3b6d3c7a57682985f66dc76985f99fe42b4dbd2 (merged Build 1 PR44).
No existing Build 2A branch/PR. Specialist PR27/42/43 are separate Drafts and
will not be modified or included.

## Authority
local_cao.ExecutionInterface.call is the only service execution entry.
Its native CAO.run, dynamic Registry/FACT_ADAPTERS, CAO.public and public_record
remain accounting authorities. Native SQLiteStore schema3 owns Cases, revisions,
source snapshots, recovery and CompanyMemory. HTTP handlers contain no accounting
methods. Native public results are returned unchanged; transport/job success
never establishes accounting completion.

## Smallest wrapper
A Python standard-library HTTP server exposes /v1/operations and /v1/jobs.
Host configuration binds credential identities to explicit permitted company keys
and host-provisioned workspace paths. Wire fields never choose filesystem paths.
Constant-time bearer comparison and company scope checks precede every private
operation. Express authenticates Supabase users and checks memberships before
selecting its scoped credential; browser company assertions are insufficient.
No service credential supplies native accounting approval.

A private SQLite operational journal stores only immutable accepted execution
requests, fingerprints, state, attempts and Case references. Native accounting
remains in the existing workspace store. A single host worker uses an OS lock;
accepted jobs survive restart. EXECUTING recovery first calls native resume:
a valid checkpoint is delivered without owner execution; no checkpoint permits
replay of the same pure initial execute. Ambiguous invalid storage fails closed.
No external posting, distributed exactly-once or replacement-evidence rework.

Evidence is bounded native structured JSON or an opaque staged-file ID mapped
inside the company staging namespace. Regular files only, no symlinks, traversal,
URLs, extraction or arbitrary host paths. Source metadata is informational and
cannot qualify evidence. Artifact references expose only curated result metadata.

## Operations and limits
HTTP size/time/concurrency limits, fixed errors, JSON logs containing operational
IDs/status/duration only, signal shutdown and readiness checks are required.
TLS termination, secure credential provisioning, protected persistent local disk,
backups and a single service instance are deployment prerequisites.
One native legal entity/period per workspace and Build1 supported fact families
remain the bounded capability. No frontend, TrackedFR mutation, model inference,
connector, accounting specialist or native governance extension is authorized.
Authored real-HTTP scenarios and separate adversarial review precede full regression.

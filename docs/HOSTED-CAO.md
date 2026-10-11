# Run the hosted CAO service locally

Requires Python3.12+ on POSIX and a protected local durable filesystem. No package
installation, LLM key or production deployment. Provision one unique private
workspace per company using docs/LOCAL-CAO.md; set company-context.md to the real
stable company/entity/calendar/period. Initialize through HTTP or the local adapter.
Keep workspaces/job journal/config/credentials outside the repository. Never commit
real credentials or evidence. The existing native database remains authoritative.

Copy hosted_cao/config.example.json to a private file, replace the placeholder with
a random secret of at least32 characters, set private absolute workspace/job paths,
and restrict config mode0600/parent0700. Generate e.g. with `python -c 'import
secrets; print(secrets.token_urlsafe(32))'` in your trusted terminal. The example
contains no working credential and must be edited before startup.

Environment template: hosted_cao/env.example. Start:

```sh
CAO_SERVICE_CONFIG=/private/cao/config.json CAO_HOST=127.0.0.1 CAO_PORT=8080 python -m hosted_cao
```

Check GET http://127.0.0.1:8080/v1/health and /v1/readiness. Private requests add
Authorization:Bearer credential, X-CAO-Company and Content-Type:application/json.
Use /v1/operations initialize/start/submit, then /v1/jobs execute with stable
Idempotency-Key and poll GET/v1/jobs/ID. Contract and sample schemas live in
interfaces/CAO-HTTP-API-CONTRACT.md. No execute endpoint bypasses durable jobs.

Credential rotation: issue a new random credential with the same narrow caller
scope; add it alongside the previous key in the protected config and gracefully
restart. Switch Express to the new secret, verify authenticated calls, remove the
old key and restart. Do not reuse secrets among callers or write them to logs.
Stop/drain before planned restart; accepted/executing jobs remain in the journal.
After hard interruption startup automatically reconciles native checkpoints first.
Failed input/storage validation is terminal and requires operator diagnosis; retry
with a new key only after repair. Preserve native files/history, never delete a
checkpoint to force rerun. This service performs no posting or memory promotion.

Run only one process/worker for a job root and exclusive service-owned workspaces.
Do not concurrently operate these workspaces via Claude Code or another host.
The journal and native stores are separate atomic domains; lost acknowledgments
are reconciled, not a distributed transaction. Protect disk/permissions, arrange
SQLite-consistent backups and retention, configure TLS/reverse-proxy rate/body/
header limits before deployment. There is no encryption-at-rest or remote queue.
Standard-library HTTP alone is not a production edge server. Unbounded execution
is limited to supported pure native owners; stop waits for an active execution.

# Genuine release evidence verification

Frozen source: `126c2f85ea37dc216bb8a732ed4394e4bfbc7e17`; tree: `db6d5d966451716a95b37c918eb788f3fca89319`. GitHub run 42297337399, attempt 1, workflow 404963318, workflow_dispatch on feature/presumed-user-sources. Authenticated GitHub run-attempt and artifact metadata checked.

Original GitHub artifact 13545745955 is retained unchanged as original-artifact.zip: 1,412,552 bytes, SHA-256 `4fc7d563b6e2d90d690afdfc68351cafc3da7d0c5c95c68f581ff521963e41b7`. 296 regular file entries, no duplicate names, traversal, symlinks or failed CRCs. artifact-verification.json records every original member digest. Expected evidence present: actual execution status, manifest, discovery, 22 suite sidecars, 65 orchestration shard sidecars, command/shard logs, source/input maps, traces and full-regression outer log. Historical pointer bundled in archive is byte-identical to checkout and is not selected for current acceptance.

Canonical map hashing is SHA256 of UTF-8 json.dumps(map,sort_keys=True,separators=(',',':')) plus LF. Actual independently regenerated maps match all 453 Python files and 2722 execution inputs. Python digest `80aebee2ba308dcacb47c2e447071d120198cde4958cb7c3e125a89608f74191`; inputs digest `c5e66b68d83f178f2a2c44a244ca2730055f94a928304a47332ae0d73ecc791d`. Actual workflow SHA-256 `06fd70ffb1802947a3a4ea240f2afa181e6ca5c77341c937553bb30adefaf558`.

All 3940 unique IDs reconcile across discovery, manifest, sidecars and actual verbose logs, in 22 mandatory suites. No failure/error/skip; all 33 recorded commands exit zero (22 suites,10 validators,git diff check). Remediation populations are19/4/18/12/10. Nested governance controls are not counted again. Independent reviewer report supplies execution-level reconciliation and challenges.

Actual production commands:

```sh
python skills/presumed-sources/verify_release.py --pointer build4/release/presumed-sources-accepted-42297337399-1-v2.json
python -m build4.verify_release --pointer build4/release/presumed-sources-accepted-42297337399-1-v2.json
CAO_SOURCES_ATTEMPT=reviewed-local-reuse-42297337399-1 python skills/presumed-sources/execute_release.py --reuse build4/release/presumed-sources-accepted-42297337399-1-v2.json
```

Both verifiers PASS:3940 distinct tests,8912 historical files. Local explicit reuse is recorded separately; it is not a GitHub Actions run. Preservation includes8911 unchanged active entries plus the authorized archived original workflow and verified successor contract. No historical receipt/log/pointer was overwritten.

Evidence-only publication must preserve regenerated source/input map equality. No new Python files are added. Receipt review is sealed unchanged; final independent post-issuance review is separate. The original ZIP is independently retained in addition to extracted evidence.

Engine acceptance remains BLOCKED until GitHub-hosted explicit reuse and all mandatory exact-head CI/readiness gates pass. Original TrackedFR upload retesting remains separately owned and pending; synthetic hosted API results do not establish original-upload or production deployment readiness.

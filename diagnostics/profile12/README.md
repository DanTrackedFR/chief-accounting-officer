# Profile 1.2 adversarial diagnostics — completed diagnostic checkpoint

Diagnostic only. No production fixes, release acceptance, historical rewrites or deployment.
Baseline: `36acb611142bc8bedd214622f1ecac539c290056`; main: `7146eaeca6a28d17d9183d0f9431fd9b9663f1fe`.

Run from repository root:

```sh
python diagnostics/profile12/regressions.py
python diagnostics/profile12/governance.py
```

Expected red. Outputs default to `/tmp/cao-profile12-diagnostic`; set
`CAO_DIAGNOSTIC_OUT` to an external directory to retain a new run. Do not overwrite
committed baseline evidence. Runtime tests use real loopback HTTP, worker execution,
durable owner records, restart and idempotent retry. No confidential customer inputs.
The first runtime log includes four test-harness Decimal serialization errors;
only test serialization was corrected, with original output preserved.

Governance tests create a disposable local clone at the frozen SHA, mutate one
sidecar at a time, restore it and invoke the actual verifier. Override `CAO_GOV_REF`
explicitly to examine a later committed candidate. Current source maps include
all Python files: adding these diagnostics invalidates old release acceptance on
this branch as intended. No pointer or gate is weakened. The historical 3,844-test
receipt remains valid only for its originally recorded input maps.

These scripts are outside the 17 ordinary test discovery locations and have no
`test_` filename. Explicit invocations fail honestly; no expected-failure decorator
or CI gate change masks their results. See [defect-register.md](defect-register.md), [defect-register.json](defect-register.json) and [HANDOFF.md](HANDOFF.md). All 13 findings reproduce and remain open. Runtime evidence JSON is losslessly compressed; read with `gzip -dc evidence/ENG-02.json.gz`.

# Required remediation coverage decision

All 63 previously omitted methods are retained as mandatory full-release gates, with no exclusions. The five suites execute through the existing Build 4 suite subprocess entrypoint, in addition to the original 17 suites. No production accounting calculation changes are required.

| File | Methods | Purpose and execution gate |
|---|---:|---|
| diagnostics/profile12/regressions.py | 19 | Original defect reproductions plus positive controls; mandatory runtime remediation |
| diagnostics/profile12/governance.py | 4 | Receipt/preservation and optimized execution controls; mandatory isolated governance on committed candidate |
| remediation/accounting-qa/test_accounting_qa.py | 18 | Additional accounting scenarios independently authored during remediation; mandatory accounting regression |
| remediation/engineering-qa/test_boundaries.py | 12 | Direct/local/hosted boundary variants; mandatory engineering regression |
| remediation/engineering-qa/test_governance.py | 10 | Positive receipt then adversarial inventory, role, path, discovery and optimization checks; mandatory isolated governance |

The last three paths are relative to diagnostics/profile12/. Complete identifiers are enumerated in the baseline inventory and production required-remediation-tests.json. There is zero identifier overlap with the original 3,862 population. There is intentional semantic overlap: diagnostic boolean-disposal/opening-balance/payment/negation cases and later QA exercise the same remediated defects with different input variants and entrypoints. Governance suites both test integrity and optimization; the later suite expands sidecar classes, role substitution, symlinks, path escape and invented discovery. These are not duplicate identifiers and none is excluded on thematic similarity.

The original diagnostics are executable regressions, not disposable diagnostic-only observations. All five suites therefore run in the full regression. Governance retains disposable clones, current committed source references, actual positive controls before tampering, and attempt-local outputs. Nested 19-method positive-control runs inside governance are not counted again as distinct top-level release coverage.

CI reruns of independently authored QA are regression enforcement. They do not confer fresh independent review or receipt acceptance. A separate reviewer must independently challenge this infrastructure correction; later full-release evidence still requires independent acceptance. Green accounting suites cannot compensate for failure or omission of any of these mandatory gates.

The final count must come from production discovery after infrastructure tests are added; 3,925 is not presumed to be the final population. Baseline3,862 + omitted63 accounts for existing methods only. New infrastructure tests increase the final population and must be reported separately.

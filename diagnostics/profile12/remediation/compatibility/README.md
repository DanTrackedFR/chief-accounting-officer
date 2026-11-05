# Focused compatibility evidence

No full release regression was run. Production source matches published 292b25aeaa06c61cd0d10f70bbb3f812f6b62aa9. Independent legacy disposal test correction is documented in ../accounting-qa/REVIEW.md: original unsupported receipt omission is now a negative assertion, explicit supported receipt preserves the original positive gain calculation.

Commands and results:

- python -m unittest discover -s skills/tests -p 'test_presumed*.py': 58 methods passed after independently justified fixture correction. Initial 57 passed/1 error retained in presumed-initial.log.
- python -m unittest discover -s skills/tests -p test_prepared_accounting_qa.py: 29 passed.
- python -m unittest hosted_cao.tests.test_prepared_engineering_qa hosted_cao.tests.test_presumed_engineering_qa: 58 passed.
- python -m unittest discover -s local_cao/tests -p 'test_*.py': 55 passed.
- python -m unittest tests.test_presumed_historical_errors tests.test_presumed_release tests.test_presumed_workflow_migration tests.test_presumed_ci_evidence: 39 passed.

Total: 239 methods, zero final errors/failures/skips. These cover formal and Profile 1.1 boundaries, local/hosted compatibility and historical error envelopes/workflow preservation. Source-profile tests exercise all four TrackedFR addenda: optional policy elections/disclosure; aggregate stable field requirements; optional PO/receipt matching with NOT_PERFORMED; actionable invalid_request errors. These synthetic checks do not replace TrackedFR testing its original uploads or the later full cross-engine release regression.

# Phase 3 lease accounting skill

First executable skill package, version 0.1.0, status REVIEW (not production). `SKILL.md` defines the high-risk accounting workflow and approved-knowledge retrieval dependencies. `lease_math.py` implements deterministic fixed-payment PV, initial ROU bridge and end-period liability rollforward with decimal arithmetic. Tests cover the previously remediated five-year sale-and-leaseback liability example, commencement-payment double-counting, zero-rate and reconciliation failure.

Run: `python -m unittest discover -s skills/lease-accounting/tests -p 'test_*.py'`.

Not yet implemented: contract ingestion, live approved-knowledge retrieval, framework-specific classification/ASC 842 operating expense and ROU logic, event-specific modifications, full journal/disclosure pack, public response adapter and human reviewer workflow. The skill must not be advertised as a complete production lease engine until those integrations and regression cases pass.

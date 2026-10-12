# Intermediate current timing independent QA

This is a separately authored intermediate review of the current October NL/UK
timing relationship. It is not final Stage 4 independent acceptance and does not
close IQA03 or certify a full-population Group close.

The reviewer inspected the new `match-timing-current` fixture node and the actual
production `STAGE3_MATCH`, `TransactionSide.validate`, `MatchingDecision.validate`
and sealed replacement qualification contracts. The node uses the existing
matching contract with its distinct orchestration execution purpose and retains
the original `timing` economic identity. Matching supplies relationship lineage,
not accounting authority or an elimination journal.

Permanent independent coverage is
`tests/test_stage4_current_timing_independent.py` (eight distinct methods).
The positive control qualifies a fresh sealed source, accepts the exact current
October NL receivable and UK payable versions and retains the original September
`TIMING_DIFFERENCE`. Attacks reject historical September owner substitution,
equal-principal wrong economic lineage, wrong counterparty, wrong Scope, omitted
current side even with rewritten decision population, stale current legal result
after prior-close correction and superseded current legal result after an
equal-value October correction. These attacks call the actual bounded matching
runtime and exact receipt producer, without weakening fixture or production code.

The prior-close independent temporal invalidation expectation was updated only
to include the legitimately new current match as a transitive consumer. Direct
consumers and unrelated-currentness assertions remain unchanged. This was a test
expectation migration, not a substantive finding or production remediation.

Validation: `python -m unittest
orchestration.tests.test_stage4_current_timing_independent
orchestration.tests.test_stage4_population_independent -q` passed **24 distinct
tests**, comprising eight new timing tests and sixteen retained population tests.
No substantive new finding was identified; unresolved findings in this bounded
review: **0**. Earlier IQA01/IQA02/IQA03/IQA04/TSIQA01/PCIQA01/PCIQA02/CRIQA01
history is unchanged. IQA03 remains governed by the full flagship acceptance.

## Prior narrow residual authority review and limitations

The reviewer separately read native Consolidation, Intercompany and Foreign
Currency contracts and executable methods. Unchanged EUR16 receivable versus
EUR18 payable cannot fully eliminate through existing ordinary-loan contracts.
Consolidation eliminates equal source-backed debit/credit amounts and explicitly
returns material differences to source accounting. Native reassessment can
preserve equal foreign principal with different local amounts; it supplies no
Group residual adjustment. Native FX supports evidenced legal monetary FX in
P&L and separately reconciled foreign-operation CTA. CTA cannot absorb an
unexplained reciprocal-loan difference. Ownership-disposal, intragroup-profit tax
and NCI hooks cannot authorize an ordinary-loan residual plug.

A legitimate corrected control requires fresh independently reviewed legal
rate/book evidence, native legal remeasurement and replacement versions, followed
by a complete operation TB including supported FX profit exactly once and an
independently reconciled net-assets/CTA bridge. Rates must originate in reviewed
evidence, rather than be selected to solve equality. Original GBP16/USD20 and
EUR16/EUR18 results and FX_DIFFERENCE history remain immutable. Unsupported
asymmetric treatment must fail closed. No new substantive generic defect was
identified in that contract review and no production change was made.

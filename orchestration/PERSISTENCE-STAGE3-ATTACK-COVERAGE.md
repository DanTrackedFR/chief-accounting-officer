# Stage 3 permanent attack coverage

A = `test_persistence_stage3.py`; I = `test_persistence_stage3_independent.py`; P2 = retained `test_persistence_stage2.py`; G = actual seven-process `generate_persistence_stage3_examples.py`, verified by `test_persistence_stage3_artifacts.py`. All files are under `orchestration/tests/`. These attacks execute native evidence, immutable history, real SQLite or native qualification; no refusal mock supplies the outcome. Counts are distinct test methods, never matrix rows or repeated phases.

| # | Required attack | Executable coverage |
|---|---|---|
| 1 | Unknown Company | A:test_unknown_company; I:test_unknown_company_cannot_retrieve |
| 2 | Cross-Company substitution | A:test_cross_company_record |
| 3 | Same display name, distinct Company | A:test_same_display_name_distinct_company |
| 4 | Missing source | A:test_missing_source; I:test_capture_cannot_drop_source_evidence |
| 5 | Changed sealed payload | A:test_changed_sealed_payload |
| 6 | Wrong reviewed pack | A:test_wrong_reviewed_bundle; P2:test_changed_reviewed_pack_refused |
| 7 | No explicit promotion intent | A:test_no_explicit_intent; I:test_explicit_intent_required |
| 8 | Model approval claim | A:test_model_approval_claim; I:test_negative_documentary_wording_never_approves |
| 9 | Synthetic authentication claim | A:test_synthetic_authentication; I:test_synthetic_authority_cannot_claim_authentication |
| 10 | Unreviewed APPROVED | A:test_unreviewed_approval; I:test_documentary_approval_cannot_use_ordinary_system_source |
| 11 | Conflict overwriting current position | A:test_conflicting_candidate_preserved_and_blocks |
| 12 | Duplicate current APPROVED | A:test_duplicate_current_approval; I:test_actual_competing_promotion_connections_publish_one_approved_position |
| 13 | Duplicate event identity | A:test_duplicate_event_sql_identity |
| 14 | Missing historical event | A:test_missing_historical_event |
| 15 | Deleted record history | A:test_deleted_memory_record |
| 16 | Rewritten immutable lineage | A:test_rewritten_immutable_lineage; I:test_existing_current_result_of_other_native_case_cannot_support_memory |
| 17 | STALE support | I:test_native_durable_correction_stales_dependent_memory_support |
| 18 | SUPERSEDED support | A:test_superseded_result_refused |
| 19 | Retracted current reuse | A:test_retracted_record_refused |
| 20 | Old position reapproval after correction | A:test_old_retracted_record_cannot_reapprove; G:correction |
| 21 | Wrong entity/Group applicability | A:test_wrong_scope; I:test_existing_current_result_of_other_native_case_cannot_support_memory |
| 22 | Wrong Period | A:test_wrong_period; I:test_registered_relationship_of_other_period_cannot_qualify_memory |
| 23 | Wrong fiscal calendar | I:test_registered_period_of_wrong_scope_calendar_cannot_qualify_memory; I:test_planning_cannot_substitute_valid_other_fiscal_calendar_same_dates |
| 24 | Wrong framework | A:test_wrong_framework; I:test_wrong_framework_cannot_be_captured |
| 25 | Wrong currency | A:test_wrong_currency |
| 26 | Wrong jurisdiction | A:test_wrong_jurisdiction |
| 27 | Invalid effective interval | A:test_invalid_effective_interval; I:test_inverted_effective_dates_refused |
| 28 | Effective versus learned dates | A:test_effective_is_not_learned; A:test_partial_effective_period_does_not_reuse |
| 29 | Fabricated unknown date | A:test_unknown_date_not_fabricated; I:test_unknown_date_cannot_carry_fabricated_value |
| 30 | OPENING/COMPARATIVE substitution | A:test_opening_comparative_substitution; I:test_registered_relationship_of_other_period_cannot_qualify_memory |
| 31 | Equal-value wrong provenance | I:test_planning_memory_use_cannot_substitute_equal_value_wrong_provenance; A:test_equal_value_wrong_provenance |
| 32 | Overlapping policy conflict | A:test_conflicting_candidate_preserved_and_blocks; G:conflict/unresolved |
| 33 | Consecutive policy intervals | A:test_nonoverlapping_historical_positions_not_conflict |
| 34 | Different-framework positions | A:test_different_framework_positions_are_not_combined |
| 35 | Current memory in historical Case | I:test_restored_use_cannot_bypass_effective_period; I:test_unknown_consuming_case_in_history_rejected |
| 36 | Transient observation overwrites context | A:test_transient_fact_gate; A:test_reusability_gate |
| 37 | Candidate as certified input | A:test_candidate_cannot_supply_native_inputs; I:test_memory_derived_context_cannot_launder_into_independent_documented_truth |
| 38 | Bypassing native reviewed inputs | P2:test_changed_reviewed_pack_refused; G:reuse real ReviewedInputPack |
| 39 | Overriding owner output | A:test_memory_does_not_override_owner |
| 40 | Journal action through memory | A:test_no_journal_action; A:test_native_owners_not_invoked |
| 41 | Lost-ack duplicate promotion | A:test_lost_ack_retry_same_event; I:test_compound_resolution_is_idempotent_after_lost_ack |
| 42 | Competing writers | I:test_actual_competing_promotion_connections_publish_one_approved_position; A:test_competing_connections_stale_revision |
| 43 | Interrupted memory publication | A:test_interrupted_publication_rolls_back; I:test_sqlite_interruption_rolls_back_entire_conflict_resolution |
| 44 | Partial Case/memory publication | A:test_case_checkpoint_without_memory_publication_grants_no_authority |
| 45 | Migration rollback | A:MemoryMigration.test_migration_failure_rolls_back |
| 46 | Corrupt payload/hash | A:test_corrupt_memory_hash |
| 47 | Future memory contract | A:test_future_memory_contract |
| 48 | Inconsistent supersession | I:test_restored_supersession_must_validate_successor_lineage; I:test_supersession_cannot_use_self_as_successor |
| 49 | Material rationale omitted | A:test_material_decision_requires_rationale; I:test_linked_decision_new_position_cannot_contradict_context_value |
| 50 | Public privacy leakage | A:test_private_memory_excluded_public; I:test_public_native_answer_does_not_expose_memory_ledger |

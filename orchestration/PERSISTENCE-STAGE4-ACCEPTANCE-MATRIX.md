# Durable Stage4 adversarial acceptance matrix

Permanent native-boundary tests remain cumulative. This matrix identifies all 50 requested attacks; previous accepted tests are regression requirements, not new Stage4 test-count credit. Connected generator additionally exercises interruption, lost ack, stale support, historical USE, explicit successor and negative material conflict in one Company. Results remain pending full release validation.

| # | Attack | Permanent method |
|---|---|---|
| 1 | Wrong Company memory namespace | `test_persistence_stage4.py::test_wrong_company_namespace_refuses` |
| 2 | Wrong Scope | `test_persistence_stage3.py::test_wrong_scope` |
| 3 | Wrong Case | `test_persistence_stage4.py::test_wrong_native_case_support_refuses` |
| 4 | Wrong Period/calendar | `test_persistence_stage3_independent.py::test_registered_period_of_wrong_scope_calendar_cannot_qualify_memory` |
| 5 | Wrong framework/currency | `test_persistence_stage3.py::test_wrong_currency` |
| 6 | Wrong effective interval | `test_persistence_stage3_independent.py::test_restored_use_cannot_bypass_effective_period` |
| 7 | Wrong temporal role | `test_persistence_stage3_independent.py::test_registered_relationship_of_other_period_cannot_qualify_memory` |
| 8 | Unauthorized Group policy inheritance | `test_persistence_stage4.py::test_group_memory_does_not_inherit_to_legal_entity` |
| 9 | Stale memory current reliance | `test_persistence_stage3_independent.py::test_native_durable_correction_stales_dependent_memory_support` |
| 10 | Superseded memory substitution | `test_persistence_stage3.py::test_superseded_result_refused` |
| 11 | Equal value wrong memory provenance | `test_persistence_stage3_independent.py::test_planning_memory_use_cannot_substitute_equal_value_wrong_provenance` |
| 12 | Context-only certified source | `test_persistence_stage4.py::test_memory_context_cannot_substitute_for_reviewed_input_pack` |
| 13 | Memory bypass ReviewedInputPack | `test_persistence_stage4.py::test_memory_context_cannot_substitute_for_reviewed_input_pack` |
| 14 | Memory substitutes native receipt | `test_persistence_stage4.py::test_memory_reference_cannot_replace_native_receipt` |
| 15 | Model proposal APPROVED | `test_persistence_stage3_independent.py::test_inferred_candidate_retained_but_cannot_be_approved` |
| 16 | Synthetic approval authenticated | `test_persistence_stage3_independent.py::test_synthetic_authority_cannot_claim_authentication` |
| 17 | Missing sealed evidence | `test_persistence_compatibility.py::test_missing_sealed_evidence_rejected` |
| 18 | Changed raw evidence | `test_persistence_stage4.py::test_changed_raw_company_evidence_refuses_sealed_intake` |
| 19 | Missing historical source snapshot | `test_persistence_stage4.py::test_deleted_source_snapshot_refuses_restore` |
| 20 | Deleted memory event | `test_persistence_stage4.py::test_deleted_memory_event_refuses_real_ledger` |
| 21 | Deleted Case provenance | `test_persistence_independent.py::test_case_history_cannot_skip_challenge` |
| 22 | Rewritten consumed memory version | `test_persistence_stage3_independent.py::test_unknown_historical_consumption_version_rejected` |
| 23 | Missing native rework history | `test_persistence_stage2_independent.py::test_all_native_rework_history_cannot_be_erased` |
| 24 | Stale dependency after restart | `test_persistence_stage2.py::test_same_value_superseded_receipts_remain_historical` |
| 25 | Wrong selective rework scope | `test_persistence_stage2.py::test_wrong_rework_order_refused` |
| 26 | Unaffected owner rerun | `test_persistence_stage2.py::test_native_rework_exact_order_and_unaffected_versions` |
| 27 | Duplicate immutable publication | `test_persistence_stage2_independent.py::test_lost_ack_retry_no_owner_execution_or_new_revision` |
| 28 | Lost durable acknowledgement | `test_persistence_stage2.py::test_lost_ack_does_not_publish_again` |
| 29 | Competing recovery workers | `test_persistence_stage2_independent.py::test_two_real_processes_recover_one_operation_once` |
| 30 | Concurrent promotion/source correction | `test_persistence_stage4_independent.py::test_concurrent_memory_promotion_and_actual_source_correction_serialize` |
| 31 | Interrupted memory transition | `test_persistence_stage3_independent.py::test_sqlite_interruption_rolls_back_entire_conflict_resolution` |
| 32 | Interrupted native execution | `test_persistence_stage2_independent.py::test_mid_selective_owner_interruption_replays_exact_native_unit` |
| 33 | Corrupt checkpoint/memory ledger | `test_persistence_stage3.py::test_corrupt_memory_hash` |
| 34 | Schema3 migration compatibility | `test_persistence_stage3.py::test_schema2_migration_retains_bytes` |
| 35 | Original Stage1/2 restoration | `test_persistence_stage2.py::test_schema1_migration_preserves_original_bytes` |
| 36 | Unauthorized CLOSED correction | `test_persistence_stage2.py::test_closed_period_without_authorization_refused` |
| 37 | False completion after interruption | `test_persistence_stage2.py::test_no_false_closure_after_correction_or_interrupt` |
| 38 | Wrong journal layer | `test_persistence_stage2.py::test_legal_group_layer_substitution_refused` |
| 39 | Duplicate legal journal | `test_persistence_stage2.py::test_duplicate_legal_selection_native_refusal` |
| 40 | Duplicate Group elimination | `test_persistence_stage2.py::test_duplicate_group_elimination_native_refusal` |
| 41 | Stale journal selection | `test_persistence_stage2.py::test_stale_dependency_cannot_select_journals` |
| 42 | Uncertain external automatic repost | `test_persistence_stage2.py::test_uncertain_external_outcome_fails_closed` |
| 43 | OPENING/COMPARATIVE substitution | `test_persistence_stage2.py::test_opening_comparative_substitution_refused` |
| 44 | Material conflict silently resolved | `test_persistence_stage4.py::test_native_original_conflict_remains_partial` |
| 45 | Historical16/18 deleted | `test_persistence_stage4.py::test_native_accounting_is_unchanged` |
| 46 | Invented temporal bridge | `test_stage4_final_independent.py::test_native_cash_profit_and_separate_temporal_stocks` |
| 47 | Memory contradiction ignored | `test_persistence_stage3.py::test_conflicting_candidate_preserved_and_blocks` |
| 48 | Retracted memory current reuse | `test_persistence_stage4.py::test_retracted_context_is_retained_but_refused` |
| 49 | Prior Case memory link overwritten | `test_persistence_stage3_independent.py::test_planning_memory_use_cannot_substitute_equal_value_wrong_provenance` |
| 50 | Private public leak | `test_persistence_stage4.py::test_public_routes_hide_memory_and_recovery_archives` |

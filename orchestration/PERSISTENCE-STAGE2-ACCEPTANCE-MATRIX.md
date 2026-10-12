# Stage 2 permanent adversarial acceptance matrix

The entries below name actual executable boundaries, not expected-error strings.
All tests are included in full orchestration discovery. Existing accepted attacks
remain required; Stage2 adds actual prepared recovery, crash, retry and operation
provenance attacks rather than replacing prior authority tests. Reruns/subtests
are not additional distinct methods. Final run status belongs to the release manifest.

Module aliases: A=`test_persistence_stage2`, I=`test_persistence_stage2_independent`,
P=`test_persistence`, C=`test_persistence_compatibility`,
T=`test_stage4_final_independent`. All reside under `orchestration/tests/`.

| # | Attack | Permanent coverage / real boundary |
|---|---|---|
|1|Missing historical source|C missing_sealed_evidence; A missing_actual_sealed_correction_evidence; restore/prepare archive validation|
|2|Wrong ReviewedInputPack|C wrong_reviewed_pack; A changed_reviewed_pack; actual native archived pack qualification|
|3|Preview-only evidence|A preview_only_rework_evidence_refused; committing prepare rejects absent exact archive|
|4|Changed raw source payload|C changed_raw_source_old_fingerprint; A failure_before_preparation; native extraction/seal/hash|
|5|Wrong Company|A wrong_company_operation_refused; P wrong_company; exact namespace|
|6|Wrong Scope/Case/Period|A wrong_root_case_operation_refused and wrong_receipt_dimensions_and_version_refused; P wrong_scope/case/period|
|7|Wrong calendar|P wrong_calendar; T both_temporal_roles_wrong_calendar; exact Period identity and native receipt|
|8|Wrong framework/currency|P wrong_framework/currency; A wrong_receipt_dimensions_and_version_refused|
|9|Wrong result version|A wrong_receipt_dimensions_and_version_refused; T both_temporal_roles_wrong_version|
|10|Same-value wrong lineage|I old_current_receipt_cannot_qualify_equal_value_new_lineage; T equal_value_wrong_population; actual receipt qualification|
|11|Stale producer|A same_value_superseded_receipts_remain_historical; T both_temporal_roles_stale; native registry currentness|
|12|Superseded producer|C superseded_legal_journal_not_current; T both_temporal_roles_superseded_equal_value|
|13|OPENING/COMPARATIVE substitution|A opening_comparative_substitution_refused; T both_temporal_roles_substitution|
|14|Corrupt graph|A corrupt_dependency_graph_refused; native Graph and exact Dependency reconstruction|
|15|Missing rework history|A missing_rework_history_refused; I successor-plan population regressions; actual restore|
|16|Rewritten immutable history|A rewritten_immutable_source_refused and period_history_cannot_be_erased_by_new_revision; exact extension transaction|
|17|Duplicate transition/receipt|A duplicate_transition_refused; I duplicate_preparation_transition_refused_on_plain_load; prior persistence typed receipt population|
|18|Interrupted SQLite transaction|A preparation_transaction_rolls_back and actual_sqlite_outcome_transaction_failure; real aborting trigger + head/outcome rollback|
|19|Competing recovery workers|I two_real_processes_recover_one_operation_once; A separate_connection_obsolete_writer; real processes/connections and revision CAS|
|20|Lost commit acknowledgement|A lost_ack_does_not_publish_again; I lost_ack_retry_no_owner_execution_or_new_revision|
|21|Repeated recovery after success|A journal_selection_repeated_without_duplicate; I same_result_journals_no_duplicate_after_new_selection_operation; real durable outcome|
|22|Unauthorized closed correction|A closed_period_without_authorization_refused; native authorize_execution through prepare|
|23|Improper reclosure|A stale_case_cannot_reclose_period; I blocked_closure_cannot_retry_without_new_reviewed_intent; native Case prerequisites|
|24|Stale journal dependency|A stale_dependency_cannot_select_journals; T stale_prior_prevents_exact_once_release; actual native allocator boundary|
|25|Duplicate legal selection|A duplicate_legal_selection_native_refusal; native gross-line allocation|
|26|Duplicate Group selection|A duplicate_group_elimination_native_refusal; native gross-line allocation|
|27|Legal/Group substitution|A legal_group_layer_substitution_refused; I group_population_cannot_be_legal_relabelled|
|28|Uncertain external ack|A uncertain_external_outcome_fails_closed; I uncertain_external_marker_cannot_disappear; explicit durable uncertain intent, no repost|
|29|False complete after interruption|A no_false_closure_after_correction_or_interrupt; I mid_selective_owner_interruption_replays_exact_native_unit; exact prepared state remains incomplete|
|30|Public privacy|A public_output_never_leaks_operation_intents; I all_public_routes_exclude_private_recovery_provenance; ordinary CAO.public allowlist|

Additional required boundaries: independent P2QA01 operation-marker deletion with
foreign keys on/off; P2QA02 event loss/impossible transitions on plain loads;
P2QA03 contradictory committed result with only redundant event SHA recalculated;
AUTH01 erased/omitted/duplicated complete native successor-plan history.
SchemaMigrationTests executes exact schema1 byte-preserving migration, transactional
failure rollback and mixed-schema refusal. The generator uses real process death
and separately resumed accounting, ordinary reclosure and unchanged repeat recovery.

"""Independent adversarial review. Synthetic recertification is test-only."""
import copy
import json
import unittest
from final_batch_cases import case, ready, refresh_release
from governance_cases import row
from final_batch_accounting import BATCH, digest
from production import assess_case, execute, to_public
from interfaces.public_output import ROUTES


class IndependentFinalBatch(unittest.TestCase):
    def result(self, c, refresh=True):
        if refresh:
            c = ready(c['package'], c=c, release=True)
        return assess_case(c['package'], c)

    def content(self, c, identifier):
        return next(d for d in c['documents'] if d['id'] == identifier)['content']

    def rehash(self, c):
        for d in c['documents']:
            d['content_hash'] = digest(d['content'])

    def blocked(self, c):
        self.rehash(c)
        self.assertEqual('blocked', self.result(c)['status'])

    def test_golden_all_frameworks(self):
        for p in BATCH:
            for fw in ('IFRS', 'US_GAAP', 'UK_GAAP', 'AASB'):
                with self.subTest(package=p, framework=fw):
                    self.assertEqual('complete', self.result(case(p, fw))['status'])

    def test_existing_employee_retrieval_and_execution_preserved(self):
        from production import canonical_knowledge, PACKAGES
        from financing_cases import ready as employee_ready
        from core_accounting import approved_claims
        for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            ids=PACKAGES['employee-benefits-payroll'][1]
            legacy=canonical_knowledge(ids,fw)
            self.assertEqual(legacy,canonical_knowledge(ids,fw,package='employee-benefits-payroll'))
            self.assertEqual({c['topic_id'] for c in legacy[0]},set(ids))
            self.assertEqual(approved_claims(['TOPIC-05-005'],fw),canonical_knowledge(['TOPIC-05-005'],fw)[0])
            self.assertEqual('complete',assess_case('employee-benefits-payroll',employee_ready('employee-benefits-payroll',fw))['status'])
            from final_batch_accounting import mapped_knowledge
            self.assertEqual(mapped_knowledge(BATCH[0],fw),canonical_knowledge(['TOPIC-05-005'],fw,package=BATCH[0]))

    def test_db_numbers_and_accounting(self):
        r = self.result(case(BATCH[0], accounting=True))
        self.assertEqual('complete', r['status'])
        self.assertEqual('210', str(r['calculations']['closing_deficit']))
        self.assertEqual('68', str(r['calculations']['pnl_expense']))
        self.assertEqual('12', str(r['calculations']['oci_loss']))
        self.assertEqual(3, len(r['journal_entry_implications']))

    def test_db_custodian_conflict(self):
        c=case(BATCH[0]); self.content(c,'custody')['benefits_paid']='0'; self.blocked(c)

    def test_db_census_conflict(self):
        c=case(BATCH[0]); self.content(c,'hr')['employees'][0]['salary_history']='Changed independently recorded salary'; self.blocked(c)

    def test_db_cash_not_expense(self):
        c=case(BATCH[0],accounting=True); self.content(c,'statement')['pnl_expense']='70'; self.blocked(c)

    def test_db_method_not_transplanted(self):
        for fw in ('US_GAAP','UK_GAAP','AASB'):
            with self.subTest(fw=fw): self.blocked(case(BATCH[0],fw,accounting=True))

    def test_db_unsupported_feature_and_valuation(self):
        for k in ('settlement','minimum_funding','assumption_selection_requested'):
            c=case(BATCH[0]); c['plans'][0][k]=True;c['plan_source']['records']=copy.deepcopy(c['plans']);self.content(c,'terms')[k]=True;self.blocked(c)

    def test_db_all_account_gl_tie(self):
        c=case(BATCH[0],accounting=True);c['gl'][1]['closing']='999';c['gl'][1]['statement']='999';self.blocked(c)

    def test_db_actuary_report_discloses_excluded_event(self):
        c=case(BATCH[0]);self.content(c,'actuary')['settlement']=True;self.blocked(c)

    def test_db_plausible_nonzero_annual_expense_opening(self):
        c=case(BATCH[0],accounting=True);c['gl'][1].update(opening='100',closing='168',statement='168');self.blocked(c)

    def test_controls_independent_risk_document(self):
        c=case(BATCH[1]);c['risk_source']['records'][0]['misstatement']='Rewritten reporting risk absent from independent document';self.blocked(c)

    def test_controls_omitted_occurrence(self):
        c=case(BATCH[1]);self.content(c,'design')['expected_occurrence_ids'].append('original-failed-March');self.blocked(c)

    def test_controls_missing_occurrence_partial(self):
        c=case(BATCH[1]);c['occurrences'][0]['state']='missing';c['occurrence_source']['records']=copy.deepcopy(c['occurrences']);self.content(c,c['occurrences'][0]['evidence_doc'])['state']='missing';self.rehash(c);self.assertEqual('partial',self.result(c)['status'])

    def test_controls_signature_without_attributes(self):
        c=case(BATCH[1]);self.content(c,c['occurrences'][0]['evidence_doc'])['attributes_present']=False;self.blocked(c)

    def test_controls_calendar_population_cannot_be_shrunk(self):
        c=case(BATCH[1]);c['occurrences']=c['occurrences'][-1:];c['occurrence_inventory']=[o['id'] for o in c['occurrences']];c['occurrence_source']['records']=copy.deepcopy(c['occurrences']);c['occurrence_source']['inventory']=list(c['occurrence_inventory']);self.content(c,'design')['expected_occurrence_ids']=list(c['occurrence_inventory']);self.blocked(c)

    def test_controls_normal_post_period_deadline_not_blocked(self):
        c=case(BATCH[1]);o=c['occurrences'][-1];o['due_date']='2027-01-05';c['occurrence_source']['records']=copy.deepcopy(c['occurrences']);self.content(c,o['evidence_doc'])['due_date']=o['due_date'];self.rehash(c);self.assertEqual('complete',self.result(c)['status'])

    def test_controls_ticket_only_remediation(self):
        c=case(BATCH[1]);r=row(c,'deficiency',control_id='control-1',severity='Qualified unresolved severity',status='closed',assessment_doc='assessment');c['deficiencies']=[r];c['deficiency_inventory']=[r['id']]
        from governance_cases import document
        document(c,'assessment',dict(control_id='control-1',severity=r['severity'],status='closed',regime_memo='Qualified regime',severity_rationale='Qualified judgment',potential_exposure_memo='Full potential exposure',aggregation_memo='Other deficiencies considered',root_cause='Original failed control',remediation_owner='Controller',independent_retest_passed=False,historical_exposure_reviewed=True));self.blocked(c)

    def test_controls_unreliable_ipe(self):
        c=case(BATCH[1]);self.content(c,'design')['ipe_reconciled']=False;self.blocked(c)

    def test_controls_malformed_or_future_expectation_dates(self):
        for start,end in [('2026-02-30','2026-12-31'),('2026-01-01','2029-01-01'),('2026-12-31','2026-01-01')]:
            c=case(BATCH[1]);self.content(c,'design').update(expectation_set_on=start,data_available_on=end);self.blocked(c)

    def test_controls_self_review(self):
        c=case(BATCH[1]);r=c['control_rows'][0];r['review_person']=r['owner_person'];c['control_source']['records']=copy.deepcopy(c['control_rows']);self.content(c,'design')['review_person']=r['owner_person'];self.blocked(c)

    def test_systems_empty_scope_not_complete(self):
        c=case(BATCH[2]);c['interfaces']=[];c['source_inventory']=[];c['interface_source']['records']=[];c['interface_source']['inventory']=[];c['controls'].update(population_count=0,population_amount='0');self.blocked(c)

    def test_systems_signed_net_cannot_hide_items(self):
        c=case(BATCH[2]);d=self.content(c,'target');d['records'][0]['amount']='110';d['records'][1]['amount']='-10';d['gross_total']='120';self.blocked(c)

    def test_systems_wrong_dimension(self):
        c=case(BATCH[2]);self.content(c,'target')['records'][0]['dimension']='Other entity';self.blocked(c)

    def test_systems_duplicate_retry(self):
        c=case(BATCH[2]);d=self.content(c,'target');r=copy.deepcopy(d['records'][0]);r['id']='retry-physical-1';d['records'].append(r);d['inventory'].append(r['id']);d['signed_total']='220';d['gross_total']='260';self.blocked(c)

    def test_systems_rejected_is_partial(self):
        c=case(BATCH[2]);d=self.content(c,'target');d['records'][1]['state']='rejected';d['gl_amount']='120';d['statement_amount']='120';self.rehash(c);self.assertEqual('partial',self.result(c)['status'])

    def test_systems_uncontrolled_ai(self):
        c=case(BATCH[2]);self.content(c,'data-control').update(ai_used=True,ai_lineage_validated=True,human_accounting_decision_retained=False);self.blocked(c)

    def test_systems_target_access_cannot_be_omitted(self):
        c=case(BATCH[2]);c['access']=c['access'][:1];c['access_inventory']=[r['id'] for r in c['access']];self.content(c,'registry')['access']=copy.deepcopy(c['access']);self.blocked(c)

    def test_systems_target_self_approval(self):
        c=case(BATCH[2]);c['access'][-1]['prepare_and_approve']=True;self.content(c,'registry')['access']=copy.deepcopy(c['access']);self.blocked(c)

    def test_operating_empty_scope_not_complete(self):
        c=case(BATCH[3]);c['processes']=[];c['source_inventory']=[];c['process_source']['records']=[];c['process_source']['inventory']=[];c['controls'].update(population_count=0,population_amount='0');self.blocked(c)

    def test_operating_retained_owner_required(self):
        c=case(BATCH[3]);c['team'][1]['retained']=False;c['team_source']['records']=copy.deepcopy(c['team']);self.blocked(c)

    def test_operating_outsource_judgment_not_transferred(self):
        c=case(BATCH[3]);c['processes'][0]['execution_model']='outsourced';c['process_source']['records']=copy.deepcopy(c['processes']);self.content(c,'service').update(execution_model='outsourced',provider_handoff_reconciled=False);self.blocked(c)

    def test_operating_capacity_gap_not_complete(self):
        c=case(BATCH[3]);c['team'][0]['productive_peak_hours']='20';c['team_source']['records']=copy.deepcopy(c['team']);self.assertEqual('partial',self.result(c)['status'])

    def test_operating_arbitrary_automation_roi(self):
        c=case(BATCH[3]);self.content(c,'service')['automation_roi']='Unmeasured predicted savings';self.blocked(c)

    def test_outer_approval_missing_and_stale(self):
        for p in BATCH:
            c=ready(p);c.pop('reviewer_signoff');self.assertEqual('partial',self.result(c,False)['status'])
            c=ready(p);c['assumptions'].append('Changed after exact certification');self.assertEqual('partial',self.result(c,False)['status'])

    def test_source_bytes_stale(self):
        for p in BATCH:
            c=case(p);c['documents'][0]['content']['independent_changed_bytes']=True;self.assertEqual('blocked',self.result(c)['status'])

    def test_release_approval_stale(self):
        for p in BATCH:
            c=ready(p);c['governance_method']['scope_memo']='Changed after release approval';c=ready(p,c=c);self.assertEqual('blocked',self.result(c,False)['status'])

    def test_stale_knowledge_selection(self):
        for p in BATCH:
            c=ready(p);c['knowledge_review']['documents'][0]['sha256']='0'*64;self.assertEqual('blocked',self.result(c,False)['status'])

    def test_unauthorized_external_action(self):
        for p in BATCH:
            c=case(p);c['requested_action']='post_to_erp';self.blocked(c)

    def test_inherited_prohibited_scope_flags(self):
        for p in BATCH:
            for flag in ('budgeting','forecasting','score_requested','benchmark_requested','filing_requested','auditor_signoff_requested'):
                with self.subTest(package=p,flag=flag):
                    c=case(p);c['governance_method'][flag]=True;self.blocked(c)

    def test_false_owner_result_and_reposting(self):
        for p in BATCH:
            c=case(p);pkg=BATCH[0] if p!=BATCH[0] else BATCH[3];owner=ready(pkg);r=execute(pkg,owner);r['calculations']['forged_numeric_fact']='999';c['imports']=[row(c,'forged-owner',package=pkg,case=owner,result=r,mode='evidence_only')];self.blocked(c)

    def test_actual_owner_journal_reposting_and_exact_once(self):
        for p in BATCH:
            pkg=BATCH[0] if p!=BATCH[0] else BATCH[3]
            owner=ready(pkg,accounting=(pkg==BATCH[0]));result=execute(pkg,owner)
            c=case(p);r=row(c,'actual-owner',package=pkg,case=owner,result=result,mode='post_journals');c['imports']=[r];self.blocked(c)
            c=case(p);r['mode']='evidence_only';duplicate=copy.deepcopy(r);duplicate['id']='same-owner-alias';c['imports']=[r,duplicate];self.blocked(c)

    def kpi_case(self, pkg='management-accounting-analytics', named=True):
        from governance_cases import ready as governance_ready
        c=case(BATCH[3]);owner=governance_ready(pkg) if pkg=='management-accounting-analytics' else ready(pkg);result=execute(pkg,owner)
        metric='on_time_reconciliation_rate' if pkg=='management-accounting-analytics' else 'closing_deficit'
        value=result['calculations'][metric];imp=row(c,'actual-kpi-owner',package=pkg,case=owner,result=result,mode='evidence_only');c['imports']=[imp]
        self.content(c,'service')['controlled_kpi_rate']=str(value)
        if named:
            c['processes'][0]['kpi_owner_import']=imp['id'];c['process_source']['records']=copy.deepcopy(c['processes'])
        c['owner_links']=[row(c,'actual-kpi-link',owner_import=imp['id'],result_path=[metric],evidence_doc='service',evidence_field='controlled_kpi_rate',amount=str(value))];c['owner_link_inventory']=['actual-kpi-link'];self.rehash(c);return c

    def test_valid_actual_47_kpi_import(self):
        self.assertEqual('complete',self.result(self.kpi_case())['status'])

    def test_kpi_cannot_use_unrelated_db_monetary_fact(self):
        self.blocked(self.kpi_case(BATCH[0],False))

    def test_kpi_owner_must_be_named_by_actual_process(self):
        self.blocked(self.kpi_case(named=False))

    def test_owner_orphan_import(self):
        c=self.kpi_case();c['owner_links']=[];c['owner_link_inventory']=[];self.blocked(c)

    def test_owner_link_unused_document(self):
        c=self.kpi_case();from governance_cases import document
        document(c,'unused-service-shadow',copy.deepcopy(self.content(c,'service')));c['owner_links'][0]['evidence_doc']='unused-service-shadow';self.blocked(c)

    def test_owner_link_source_contradiction(self):
        c=self.kpi_case();self.content(c,'service')['controlled_kpi_rate']='99';self.blocked(c)

    def test_owner_link_duplicate_alias(self):
        c=self.kpi_case();link=copy.deepcopy(c['owner_links'][0]);link['id']='same-owner-second-link';c['owner_links'].append(link);c['owner_link_inventory'].append(link['id']);self.blocked(c)

    def test_privacy_all_seven_routes_and_substantive_caveat(self):
        for p in BATCH:
            c=ready(p);r=execute(p,c);r['source_note']='Source: ChatGPT training data';r['evidence'].append({'source_note':'Source: FRC FRS 102','approval_track':'TRAINING_DATA_CHECKED'})
            # Raw evidence is never copied; exclude artificial empty-proposition claim from citation iteration.
            r['evidence'].pop();r['facts_used']['private_note']='Source: FRC FRS 102'
            for route in ROUTES:
                public=json.dumps(to_public(r,route));self.assertNotIn('Source:',public);self.assertNotIn('source_note',public);self.assertNotIn('TRAINING_DATA_CHECKED',public);self.assertIn('No actuarial, legal, audit',public)

    def test_public_caveat_contamination_fails_closed(self):
        for p in BATCH:
            for note in ('Source: ChatGPT training data','Source: FRC FRS 102'):
                c=ready(p);c['knowledge_review']['public_caveats'].append(note)
                from production import case_fingerprint
                c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
                self.assertEqual('blocked',self.result(c,False)['status'])


if __name__ == '__main__': unittest.main()

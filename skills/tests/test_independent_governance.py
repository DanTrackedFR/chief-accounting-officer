"""Independent batch43-47 challenge suite, separate from implementation tests.

Uses clearly synthetic approvals. Refreshing the release/case approvals allows
semantic failures to be tested independently of the stale-signoff control.
"""
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from governance_cases import case, ready, digest, FRAMEWORKS, row, approved
from governance_accounting import BATCH
from production import assess_case, to_public, execute
from interfaces.public_output import ROUTES


def changed_doc(c, identifier, change):
    d = next(d for d in c['documents'] if d['id'] == identifier)
    change(d['content'])
    d['content_hash'] = digest(d['content'])
    return d


def duplicate_area(c):
    r = copy.deepcopy(c['readiness'][0]); r['id'] = 'duplicate-area'
    c['readiness'].append(r)
    c['readiness_source']['records'].append(copy.deepcopy(r))
    c['readiness_source']['inventory'].append(r['id'])
    c['source_inventory'].append(r['id']); c['controls']['population_count'] += 1


def alias_pbc(c):
    for identifier in ('source', 'books'):
        d = copy.deepcopy(next(d for d in c['documents'] if d['id'] == identifier))
        d['id'] = identifier + '-alias'
        c['documents'].append(d); c['document_inventory'].append(d['id'])
    r = copy.deepcopy(c['requests'][0])
    r.update(id='request-alias', purpose='Same source extraction renamed',
             source_doc='source-alias', ledger_doc='books-alias')
    c['requests'].append(r); c['request_source']['records'].append(copy.deepcopy(r))
    c['request_source']['inventory'].append(r['id']); c['source_inventory'].append(r['id'])
    c['controls'].update(population_count=2, population_amount='200')


def wrong_disclosure_metric(c):
    c['requirements'][0]['metric'] = 'cash'
    changed_doc(c, 'statement', lambda d: d.update(metric='cash'))


def kpi_event(c, key, value):
    c['reconciliations'][0][key] = value
    changed_doc(c, 'reconciliation-source', lambda d: d['records'][0].update({key: value}))


class IndependentGovernanceQA(unittest.TestCase):
    def assess(self, package, change=lambda c: None, *, release=True, framework='IFRS'):
        c = case(package, framework); change(c)
        return assess_case(package, ready(package, c=c, release=release))

    def rejects(self, package, change, **kwargs):
        result = self.assess(package, change, **kwargs)
        self.assertNotEqual(result['status'], 'complete', result['calculations'])
        return result

    def test_twenty_framework_positive_workpapers_and_privacy_routes(self):
        for package in BATCH:
            for framework in FRAMEWORKS:
                with self.subTest(package=package, framework=framework):
                    r = self.assess(package, framework=framework)
                    self.assertEqual(r['status'], 'complete', r['conclusion'])
                    self.assertEqual(r['journal_entry_implications'], [])
                    for route in ROUTES:
                        output = json.dumps(to_public(r, route))
                        for token in ('source_note', 'approval_track', 'evidence_status',
                                      'audit_required', 'Source:', 'Synthetic independent',
                                      'owner_result_fingerprint', 'content_hash'):
                            self.assertNotIn(token, output)
                        self.assertTrue(to_public(r, route)['limitations'])
                        self.assertEqual(to_public(r, route)['citations'], [])

    def test_ipo_area_count_is_exactly_once(self):
        self.rejects('ipo-accounting-readiness', duplicate_area)

    def test_ipo_owner_is_bound_to_original_scope(self):
        self.rejects('ipo-accounting-readiness', lambda c: c['readiness'][0].update(accountable_owner='Replacement not present in source'))

    def test_ipo_gap_stays_partial(self):
        def change(c):
            r=c['readiness'][0];r['state']='gap'
            changed_doc(c,r['evidence_doc'],lambda d:d.update(state='gap',criterion_evidenced=False))
        self.assertEqual(self.assess('ipo-accounting-readiness',change)['status'],'partial')

    def test_ipo_unretested_remediation_cannot_complete(self):
        def change(c):
            r=c['readiness'][0];r['state']='remediated'
            changed_doc(c,r['evidence_doc'],lambda d:d.update(state='remediated',remediation_retested=False))
        self.rejects('ipo-accounting-readiness',change)

    def test_pbc_alias_documents_cannot_count_source_twice(self):
        self.rejects('audit-support-pbc', alias_pbc)

    def test_pbc_independent_original_amount_cannot_conflict(self):
        self.rejects('audit-support-pbc', lambda c: c['request_source']['records'][0].update(amount='999'))

    def test_pbc_source_cancelled_or_reversed_omission(self):
        def change(c):
            changed_doc(c,'source',lambda d:(d['records'].pop(),d['inventory'].pop()))
        self.rejects('audit-support-pbc',change)

    def test_pbc_equal_total_cannot_replace_original_record_identity(self):
        def change(c):
            def content(d):
                d['records'][0]['id']='substituted-equal-amount'
                d['inventory'][0]='substituted-equal-amount'
            changed_doc(c,'source',content)
        self.rejects('audit-support-pbc',change)

    def test_pbc_selected_sample_substitution(self):
        self.rejects('audit-support-pbc',lambda c:c['samples'][0].update(record_id='original-2'))

    def test_missing_selected_sample_retained_without_fake_support(self):
        def change(c):
            c['samples'][0].update(evidence_available=False,support_doc=None)
            c['documents']=[d for d in c['documents'] if d['id']!='selected-evidence']
            c['document_inventory'].remove('selected-evidence')
        r=self.assess('audit-support-pbc',change)
        self.assertEqual(r['status'],'partial',r['conclusion'])
        self.assertEqual(r['calculations']['sample_count'],1)

    def test_policy_polish_cannot_replace_owner_conclusion(self):
        def change(c):
            changed_doc(c,'active-memo',lambda d:d.update(conclusion='Unsupported improved conclusion'))
            c['history'][0]['body_hash']=next(d for d in c['documents'] if d['id']=='active-memo')['content_hash']
        self.rejects('accounting-policy-memo-governance',change)

    def test_policy_original_change_classification_cannot_be_downgraded(self):
        self.rejects('accounting-policy-memo-governance',lambda c:c['policy_source']['records'][0].update(policy_change=True))

    def test_policy_fake_locator_cannot_create_authority(self):
        def change(c):
            d=changed_doc(c,'active-memo',lambda d:d['citations'][0].update(locator='Invented paragraph 999'))
            c['history'][0]['body_hash']=d['content_hash']
        self.rejects('accounting-policy-memo-governance',change)

    def test_policy_empty_claim_to_authority_map_cannot_complete(self):
        def change(c):
            d=changed_doc(c,'active-memo',lambda d:d.update(citations=[]))
            c['history'][0]['body_hash']=d['content_hash']
        self.rejects('accounting-policy-memo-governance',change)

    def test_policy_history_overlap_rejects(self):
        def change(c):
            h=copy.deepcopy(c['history'][0]);h.update(id='second-version',policy_version=2,supersedes=c['history'][0]['id'])
            c['history'].append(h);c['history_inventory'].append(h['id'])
        self.rejects('accounting-policy-memo-governance',change)

    def test_error_correction_owner_cannot_be_relabelled_policy_change(self):
        from reporting_cases import reporting as changed_case, certified
        def change(c):
            s=changed_case('accounting-changes');s['jurisdiction']=c['jurisdiction']
            s=certified('accounting-changes',case=s);r=execute('accounting-changes',s)
            c['imports'][0].update(package='accounting-changes',case=s,result=r)
            c['policies'][0].update(policy_change=True,owner_result_fingerprint=r['case_fingerprint'],accounting_conclusion=r['conclusion'],result_path=['opening_equity_change'],amount='-20')
            citations=[dict(id='claim-'+str(i),claim_id=x['claim_id'],proposition=x['proposition'],locator=None) for i,x in enumerate(r['evidence'])]
            d=changed_doc(c,'active-memo',lambda d:d.update(conclusion=r['conclusion'],owner_result_fingerprint=r['case_fingerprint'],citations=citations))
            c['history'][0]['body_hash']=d['content_hash']
            c['policy_source']['records']=copy.deepcopy(c['policies']);c['controls']['population_amount']='20'
        self.rejects('accounting-policy-memo-governance',change)

    def test_policy_separate_nonoverlapping_future_version_retained(self):
        def change(c):
            h=copy.deepcopy(c['history'][0])
            h.update(id='future-version',policy_version=2,supersedes=c['history'][0]['id'],effective_from='2027-01-01',effective_to='2027-12-31')
            c['history'].append(h);c['history_inventory'].append(h['id'])
        r=self.assess('accounting-policy-memo-governance',change)
        self.assertEqual(r['status'],'complete',r['conclusion'])
        self.assertEqual(r['calculations']['retained_history_count'],2)

    def test_disclosure_numeric_equality_does_not_establish_metric(self):
        self.rejects('disclosure-management', wrong_disclosure_metric)

    def test_disclosure_governance_workpaper_cannot_be_accounting_owner(self):
        def change(c):
            s=ready('management-accounting-analytics');r=execute('management-accounting-analytics',s)
            c['imports'][0].update(package='management-accounting-analytics',case=s,result=r)
            c['requirements'][0].update(topic_id='TOPIC-08-008',owner_requirement=r['disclosures_impacted'][0],metric='current_statutory',result_path=['current_statutory'],amount='120')
            c['requirement_source']['records']=copy.deepcopy(c['requirements'])
            c['requirement_source']['applicable_topic_inventory']=['TOPIC-08-008']
            c['notes'][0].update(narrative=r['conclusion'],amount='120')
            changed_doc(c,'statement',lambda d:d.update(metric='current_statutory',amount='120'))
            c['controls']['population_amount']='120'
        self.rejects('disclosure-management',change)

    def test_disclosure_missing_applicable_note(self):
        self.rejects('disclosure-management',lambda c:c.update(notes=[],note_inventory=[]))

    def test_disclosure_topic_coverage_missing(self):
        self.rejects('disclosure-management',lambda c:c['requirement_source'].update(applicable_topic_inventory=[]))

    def test_disclosure_unreviewed_na(self):
        def change(c):
            c['requirements'][0].update(applicable=False,amount='0')
            changed_doc(c,'applicability',lambda d:d.update(applicable=False))
            c.update(notes=[],note_inventory=[]);c['controls']['population_amount']='0'
        self.rejects('disclosure-management',change)

    def test_disclosure_reviewed_na_retains_requirement_without_hidden_note(self):
        def change(c):
            c['requirements'][0].update(applicable=False,amount='0')
            c['requirement_source']['records']=copy.deepcopy(c['requirements'])
            changed_doc(c,'applicability',lambda d:d.update(applicable=False,not_applicable_independently_reviewed=True))
            c.update(notes=[],note_inventory=[]);c['controls']['population_amount']='0'
        r=self.assess('disclosure-management',change)
        self.assertEqual(r['status'],'complete',r['conclusion'])
        self.assertEqual(r['calculations']['requirement_count'],1)
        self.assertEqual(r['calculations']['applicable_count'],0)

    def test_disclosure_late_review_note_cannot_remain_complete(self):
        r=self.assess('disclosure-management',lambda c:c['notes'][0].update(review_notes_closed=False))
        self.assertEqual(r['status'],'partial',r['conclusion'])

    def test_disclosure_changed_comparative_needs_accounting_owner(self):
        self.rejects('disclosure-management',lambda c:c['notes'][0].update(prior_amount='151'))

    def test_analytics_completion_before_cycle_is_not_current_kpi_fact(self):
        self.rejects('management-accounting-analytics',lambda c:kpi_event(c,'completed_on','2025-01-01'))

    def test_analytics_future_due_event_is_not_current_denominator(self):
        self.rejects('management-accounting-analytics',lambda c:kpi_event(c,'due_date','2030-01-01'))

    def test_analytics_future_completion(self):
        self.rejects('management-accounting-analytics',lambda c:kpi_event(c,'completed_on','2030-01-01'))

    def test_analytics_material_missing_rec_is_partial(self):
        r=self.assess('management-accounting-analytics',lambda c:kpi_event(c,'completed_on',None))
        self.assertEqual(r['status'],'partial',r['conclusion'])
        self.assertEqual(r['calculations']['material_open_reconciliations'],1)

    def test_analytics_unposted_records_cannot_be_ledger_facts(self):
        self.rejects('management-accounting-analytics',lambda c:changed_doc(c,'current-books',lambda d:d.update(posted_only=False)))

    def test_analytics_readiness_count_cannot_be_accounting_adjustment(self):
        def change(c):
            s=ready('ipo-accounting-readiness');r=execute('ipo-accounting-readiness',s)
            c['imports'].append(approved('ipo-owner',package='ipo-accounting-readiness',case=s,result=r,mode='evidence_only'))
            c['bridge_items']=[row(c,'unsupported-adjustment',account='cash',classification='owner_accounting_adjustment',sign=1,amount='9',owner_import='ipo-owner',result_path=['supported_area_count'],rationale='Readiness count misrepresented as adjustment',mapping_memo='Polished unsupported mapping')]
            c['bridge_inventory']=['unsupported-adjustment'];c['accounts'][0]['management_amount']='111'
            changed_doc(c,'current-books',lambda d:d.update(management_amount='111'))
        self.rejects('management-accounting-analytics',change)

    def test_analytics_document_currency_cannot_contradict_content(self):
        def change(c):
            for d in c['documents']:
                if d['id'] in ('current-books','prior-books'):d['currency']='EUR'
        self.rejects('management-accounting-analytics',change)

    def test_analytics_cannot_aggregate_currency_outside_declared_unit(self):
        def change(c):
            c['accounts'][0]['currency']='EUR'
            c['account_source']['records']=copy.deepcopy(c['accounts'])
            for identifier in ('current-books','prior-books'):
                d=changed_doc(c,identifier,lambda d:d.update(currency='EUR'))
                d['currency']='EUR'
        self.rejects('management-accounting-analytics',change)

    def test_pbc_different_currencies_cannot_have_single_unqualified_gross(self):
        def change(c):
            for name in ('source','books'):
                d=copy.deepcopy(next(d for d in c['documents'] if d['id']==name))
                d['id']=name+'-eur';d['currency']='EUR'
                for r in d['content']['records']:r['id']+='-eur';r['account']='otherexpense'
                d['content']['inventory']=[x['id'] for x in d['content']['records']]
                d['content_hash']=digest(d['content']);c['documents'].append(d);c['document_inventory'].append(d['id'])
            r=copy.deepcopy(c['requests'][0]);r.update(id='eur-request',purpose='EUR expense support',account='otherexpense',source_doc='source-eur',ledger_doc='books-eur')
            c['requests'].append(r);c['request_source']['records'].append(copy.deepcopy(r));c['request_source']['inventory'].append(r['id']);c['source_inventory'].append(r['id'])
            c['controls'].update(population_count=2,population_amount='200')
        self.rejects('audit-support-pbc',change)

    def test_analytics_unexplained_movement_cannot_complete(self):
        self.rejects('management-accounting-analytics',lambda c:c.update(explanations=[],explanation_inventory=[]))

    def test_analytics_zero_movement_has_no_manufactured_explanation(self):
        def change(c):
            def content(d):
                d.update(statutory_amount='120',management_amount='120',gross_amount='120')
                d['records'][0]['amount']='120'
            changed_doc(c,'prior-books',content);c.update(explanations=[],explanation_inventory=[])
        r=self.assess('management-accounting-analytics',change)
        self.assertEqual(r['status'],'complete',r['conclusion'])
        self.assertEqual(r['calculations']['gross_movement'],0)

    def test_analytics_zero_prior_has_undefined_percentage(self):
        def change(c):
            def content(d):
                d.update(statutory_amount='0',management_amount='0',gross_amount='0')
                d['records'][0]['amount']='0'
            changed_doc(c,'prior-books',content)
            changed_doc(c,'actual-drivers',lambda d:d['drivers'][0].update(amount='120'))
            c['explanations'][0]['amount']='120'
        r=self.assess('management-accounting-analytics',change)
        self.assertEqual(r['status'],'complete',r['conclusion'])
        self.assertIsNone(r['calculations']['account_movements'][0]['percentage'])

    def test_analytics_gross_offsets_not_hidden_by_net(self):
        def change(c):
            def content(d):
                d['records'].extend([dict(id='offset-dr',account='cash',amount='5'),dict(id='offset-cr',account='cash',amount='-5')]);d['inventory'].extend(['offset-dr','offset-cr'])
            changed_doc(c,'current-books',content)
        self.rejects('management-accounting-analytics',change)

    def test_forbidden_scope_controls_all_five_packages(self):
        specific={'ipo-accounting-readiness':['score_requested','benchmark_requested','ipo_timing_prediction','filing_mechanics'],
                  'audit-support-pbc':['evidence_sufficiency_asserted','auditor_independence_determined','confirmation_control_requested','auditor_signoff_requested'],
                  'accounting-policy-memo-governance':['autonomous_policy_selection','transition_calculation_requested','overwrite_history','invented_citations'],
                  'disclosure-management':['universal_checklist','compliance_certification','filing_requested','comparative_change_requested'],
                  'management-accounting-analytics':['budgeting','forecasting','investment_analysis','generic_bi','manufactured_explanations','automatic_gl_correction']}
        for package in BATCH:
            for flag in specific[package]+['posting_requested','legal_certification','audit_opinion','regulatory_compliance','forecast_requested','authority_override']:
                with self.subTest(package=package,flag=flag):
                    self.rejects(package,lambda c,flag=flag:c['governance_method'].update({flag:True}))

    def test_document_content_hash_and_release_staleness(self):
        for package in BATCH:
            with self.subTest(package=package):
                self.rejects(package,lambda c:c['documents'][0].update(content='Unreviewed source bytes'))
                self.rejects(package,lambda c:c['documents'][0].update(query_version='changed'),release=False)

    def test_exact_case_signoff_staleness(self):
        for package in BATCH:
            with self.subTest(package=package):
                c=ready(package);c['assumptions'].append('Changed after independent approval')
                self.assertNotEqual(assess_case(package,c)['status'],'complete')

    def test_release_review_scope_matches_exact_case(self):
        for package in BATCH:
            with self.subTest(package=package):
                self.rejects(package,lambda c:c['release_review'].update(source_entity='Different legal entity'),release=False)

    def test_knowledge_manifest_staleness(self):
        for package in BATCH:
            with self.subTest(package=package):
                c=ready(package);c['knowledge_review']['documents'][0]['sha256']='0'*64
                self.assertEqual(assess_case(package,c)['status'],'blocked')

    def test_frozen_actual_knowledge_bytes_changed_without_writing_canonical(self):
        c=ready('ipo-accounting-readiness');original=Path.read_bytes
        target=c['knowledge_review']['documents'][0]['path']
        def changed(path):
            b=original(path)
            return b+b'\nindependent changed knowledge bytes' if str(path).endswith('/'+target) else b
        with patch.object(Path,'read_bytes',changed):
            self.assertEqual(assess_case('ipo-accounting-readiness',c)['status'],'blocked')

    def test_implementation_byte_staleness_without_file_mutation(self):
        c=ready('ipo-accounting-readiness');original=Path.read_bytes
        def changed(path):
            b=original(path)
            return b+b'\n# independent changed implementation' if str(path).endswith('/skills/governance_accounting.py') else b
        with patch.object(Path,'read_bytes',changed):
            self.assertEqual(assess_case('ipo-accounting-readiness',c)['status'],'partial')

    def test_import_result_staleness_and_duplicate_owner(self):
        for package in ('accounting-policy-memo-governance','disclosure-management'):
            with self.subTest(package=package):
                self.rejects(package,lambda c:c['imports'][0]['result'].update(conclusion='Altered completed owner'))
                def duplicate(c):
                    imp=copy.deepcopy(c['imports'][0]);imp['id']='same-owner-alias';c['imports'].append(imp)
                self.rejects(package,duplicate)

    def test_source_version_and_dimension_mismatch(self):
        for package in BATCH:
            for change in (lambda c:c['documents'][0].update(version='v2'),
                           lambda c:c['documents'][0].update(source_entity='Different entity'),
                           lambda c:c['documents'][0].update(source_period=['2025-01-01','2025-12-31'])):
                with self.subTest(package=package,change=change):self.rejects(package,change)

    def test_import_owner_scope_and_posting_mode(self):
        for key,value in [('jurisdiction','Another jurisdiction'),('entity','Other entity'),('framework','US_GAAP')]:
            with self.subTest(key=key):
                self.rejects('disclosure-management',lambda c,key=key,value=value:c['imports'][0]['case'].update({key:value}))
        self.rejects('disclosure-management',lambda c:c['imports'][0].update(mode='post_journals'))

    def test_public_provenance_contamination_is_fail_closed(self):
        for text in ('Source: ChatGPT training data','Source: FRC FRS 102','MODEL_DERIVED_AUDIT_REQUIRED'):
            c=ready('ipo-accounting-readiness');c['knowledge_review']['public_caveats']=[text]
            # Refresh only the outer synthetic approval; safe curation must still reject.
            from production import case_fingerprint
            c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
            self.assertEqual(assess_case('ipo-accounting-readiness',c)['status'],'blocked')


if __name__=='__main__':unittest.main()

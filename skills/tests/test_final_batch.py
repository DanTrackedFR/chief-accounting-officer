"""Bounded final-batch authored regression; synthetic approvals are not authority."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from final_batch_cases import case,ready,refresh_release,BATCH,digest,row
from production import assess_case,execute,to_public,case_fingerprint,canonical_knowledge,PACKAGES
from interfaces.public_output import ROUTES

class FinalBatch(unittest.TestCase):
    def content(self,c,id):return next(d['content'] for d in c['documents'] if d['id']==id)
    def result(self,c):
        for d in c['documents']:d['content_hash']=digest(d['content'])
        return assess_case(c['package'],ready(c['package'],c=c,release=True))
    def block(self,c):self.assertEqual('blocked',self.result(c)['status'])
    def sync(self,c,key,source):c[source]['records']=copy.deepcopy(c[key])
    def test_db_accounting_bridge(self):
        r=self.result(case(BATCH[0],accounting=True));self.assertEqual('complete',r['status'])
        self.assertEqual({'opening_deficit':'200','closing_deficit':'210','contributions':'70','service_cost':'60','pnl_expense':'68','oci_loss':'12'},{k:str(v) for k,v in r['calculations'].items()})
        for j in r['journal_entry_implications']:
            from decimal import Decimal
            self.assertEqual(sum(Decimal(str(x['amount'])) for x in j if x['side']=='Dr'),sum(Decimal(str(x['amount'])) for x in j if x['side']=='Cr'))
    def test_db_workpaper_not_journal_engine(self):
        for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            r=self.result(case(BATCH[0],fw));self.assertEqual('complete',r['status']);self.assertFalse(r['journal_entry_implications']);self.assertNotIn('oci_loss',r['calculations'])
    def test_db_other_postemployment_bounded_workpaper(self):
        c=case(BATCH[0]);c['plans'][0]['classification']='other_postemployment';self.sync(c,'plans','plan_source')
        for id in ('terms','actuary'):self.content(c,id)['classification']='other_postemployment'
        self.assertEqual('complete',self.result(c)['status']);c['requested_action']='accounting';self.block(c)
    def test_db_qualified_feature_conflict(self):
        c=case(BATCH[0]);self.content(c,'actuary')['settlement']=True;self.block(c)
    def test_db_opening_gl_expense_not_zero(self):
        c=case(BATCH[0],accounting=True);c['gl'][1].update(opening='100',closing='168',statement='168');self.block(c)
    def test_db_bad_obligation_rollforward(self):
        c=case(BATCH[0]);c['plans'][0]['service_cost']='61';self.sync(c,'plans','plan_source');self.content(c,'actuary')['service_cost']='61';self.block(c)
    def test_db_bad_asset_rollforward(self):
        c=case(BATCH[0]);c['plans'][0]['asset_interest']='33';self.sync(c,'plans','plan_source')
        for id in ('actuary','custody'):self.content(c,id)['asset_interest']='33'
        self.block(c)
    def test_db_wrong_rate(self):
        c=case(BATCH[0],accounting=True);self.content(c,'actuary')['assumptions']['qualified_opening_discount_rate']='0.05';self.block(c)
    def test_db_future_signoff(self):
        c=case(BATCH[0]);self.content(c,'actuary')['signed_on']='2028-01-01';self.block(c)
    def test_db_wrong_measurement_date(self):
        c=case(BATCH[0]);self.content(c,'actuary')['measurement_date']='2025-12-31';self.block(c)
    def test_db_missing_assumptions(self):
        c=case(BATCH[0]);self.content(c,'actuary')['assumptions']={};self.block(c)
    def test_db_dc_not_specialist_db(self):
        c=case(BATCH[0]);c['plans'][0]['classification']='defined_contribution';self.block(c)
    def test_db_multemployer_blocked(self):
        c=case(BATCH[0]);c['plans'][0]['single_employer']=False;self.sync(c,'plans','plan_source');self.content(c,'terms')['single_employer']=False;self.block(c)
    def test_db_source_statement_conflict(self):
        c=case(BATCH[0]);self.content(c,'statement')['gl_net_liability']='200';self.block(c)
    def test_db_benefits_doublecount(self):
        c=case(BATCH[0]);self.content(c,'custody')['benefits_paid']='100';self.block(c)
    def test_db_annual_scope(self):
        c=case(BATCH[0],accounting=True);c['period_start']='2026-02-01';self.block(c)
    def test_controls_uncovered_risk_partial(self):
        c=case(BATCH[1]);r=copy.deepcopy(c['risk_source']['records'][0]);r['id']='risk-new';c['risk_source']['records'].append(r);c['risk_source']['inventory'].append(r['id']);self.content(c,'risk-scope').update(records=c['risk_source']['records'],inventory=c['risk_source']['inventory']);self.assertEqual('partial',self.result(c)['status'])
    def test_controls_unsupported_frequency(self):
        c=case(BATCH[1]);c['control_rows'][0]['frequency']='daily';self.sync(c,'control_rows','control_source');self.content(c,'design')['frequency']='daily';self.block(c)
    def test_controls_automated_missing_dependency(self):
        c=case(BATCH[1]);c['control_rows'][0]['kind']='automated';self.sync(c,'control_rows','control_source');self.content(c,'design').update(kind='automated',configuration_version='v1',access_evidence='Actual access',change_evidence='Actual change',negative_test_evidence='Actual negative test',system_dependency_validated=False);self.block(c)
    def test_controls_late_expectation(self):
        c=case(BATCH[1]);self.content(c,'design')['expectation_set_on']='2027-01-01';self.block(c)
    def test_controls_invalid_expectation_date(self):
        c=case(BATCH[1]);self.content(c,'design')['expectation_set_on']='garbage';self.block(c)
    def test_controls_sod_partial(self):
        c=case(BATCH[1]);self.content(c,'design')['sod_conflict']=True;self.assertEqual('partial',self.result(c)['status'])
    def test_controls_false_effectiveness(self):
        c=case(BATCH[1]);self.content(c,'regime')['requested_conclusion']='operating_effectiveness';self.block(c)
    def test_controls_stale_rcm(self):
        c=case(BATCH[1]);self.content(c,'design')['rcm_version']='old';self.block(c)
    def test_systems_missing_target_access(self):
        c=case(BATCH[2]);c['access']=c['access'][:1];c['access_inventory']=[c['access'][0]['id']];self.content(c,'registry')['access']=copy.deepcopy(c['access']);self.block(c)
    def test_systems_access_self_approval(self):
        c=case(BATCH[2]);c['access'][0]['prepare_and_approve']=True;self.content(c,'registry')['access']=copy.deepcopy(c['access']);self.block(c)
    def test_systems_nonzero_threshold(self):
        c=case(BATCH[2]);self.content(c,'data-control')['approved_threshold']='1';self.block(c)
    def test_systems_hidden_override(self):
        c=case(BATCH[2]);self.content(c,'data-control').update(euc_used=True,formula_version_reviewed=True,hidden_override=True);self.block(c)
    def test_systems_opening_migration_mismatch(self):
        c=case(BATCH[2]);self.content(c,'data-control').update(migration=True,original_opening_balance='100',migrated_opening_balance='99',parallel_run_reconciled=True,rollback_tested=True)
        for id in ('source','target'):self.content(c,id)['balance_date']=c['period_start']
        self.block(c)
    def test_systems_statement_conflict(self):
        c=case(BATCH[2]);self.content(c,'target')['statement_amount']='101';self.block(c)
    def test_systems_unmapped_account(self):
        c=case(BATCH[2]);self.content(c,'source')['records'][0]['account']='unknown';self.block(c)
    def test_systems_unlisted_entity(self):
        c=case(BATCH[2]);c['interfaces'][0]['entity']='Other';self.sync(c,'interfaces','interface_source');self.block(c)
    def test_model_duplicate_physical_person(self):
        c=case(BATCH[3]);c['team'][0]['person_id']=c['team'][1]['person_id'];self.sync(c,'team','team_source');self.block(c)
    def test_model_missing_process_owner(self):
        c=case(BATCH[3]);c['processes'][0]['accountable_person']='Nobody';self.sync(c,'processes','process_source');self.block(c)
    def test_model_sla_unqualified(self):
        c=case(BATCH[3]);self.content(c,'service')['sla_evidenced']=False;self.block(c)
    def test_model_dependency_gap_partial(self):
        c=case(BATCH[3]);self.content(c,'service')['critical_dependencies_resolved']=False;self.assertEqual('partial',self.result(c)['status'])
    def test_model_classifications_distinct(self):
        for cls in ('REQUIRED','RECOMMENDED','WORLD_CLASS','SHORTCUT_RISK'):
            c=case(BATCH[3]);c['processes'][0]['maturity_class']=cls;self.sync(c,'processes','process_source');self.content(c,'service')['maturity_class']=cls;r=self.result(c);self.assertEqual('complete',r['status']);self.assertEqual(1,r['calculations']['qualified_practice_classes'][cls])
    def test_model_unsupported_headcount(self):
        c=case(BATCH[3]);self.content(c,'service')['headcount_prescription']='Hire 10';self.block(c)
    def test_model_ipo_score_blocked(self):
        c=case(BATCH[3]);self.content(c,'service')['ipo_readiness_score']='95';self.block(c)
    def test_model_automation_control_bypass(self):
        c=case(BATCH[3]);self.content(c,'service').update(automated=True,control_requirements_preserved=False,ai_governance_present=True,human_judgment_retained=True);self.block(c)
    def test_practice_has_no_journals_or_fake_claims(self):
        for p in BATCH[1:]:
            r=self.result(case(p));self.assertEqual('complete',r['status']);self.assertFalse(r['journal_entry_implications']);self.assertFalse(r['evidence'])
    def test_golden_framework_contexts(self):
        for p in BATCH:
            for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):self.assertEqual('complete',self.result(case(p,fw))['status'])
    def test_unsigned_partial_and_case_stale(self):
        for p in BATCH:
            c=ready(p);c.pop('reviewer_signoff');self.assertEqual('partial',assess_case(p,c)['status'])
            c=ready(p);c['assumptions'].append('Changed facts');self.assertEqual('partial',assess_case(p,c)['status'])
    def test_implementation_stale(self):
        for p in BATCH:
            c=ready(p)
            original=Path.read_bytes
            with patch.object(Path,'read_bytes',lambda path:original(path)+b'Changed implementation' if path.name=='final_batch_accounting.py' else original(path)):self.assertEqual('partial',assess_case(p,c)['status'])
    def test_knowledge_stale(self):
        for p in BATCH:
            c=ready(p);c['knowledge_review']['documents'][0]['sha256']='f'*64;self.assertEqual('blocked',assess_case(p,c)['status'])
    def test_original_population_contradiction(self):
        for p,key in zip(BATCH,('plans','control_rows','interfaces','processes')):
            c=case(p);c[key][0]['amount']='999';self.block(c)
    def test_all_public_routes_privacy(self):
        forbidden=('source_note','reviewer_signoff','approval_track','evidence_status','content_hash','case_fingerprint','implementation_fingerprint','source_notes','TRAINING_DATA_CHECKED')
        for p in BATCH:
            r=execute(p,ready(p))
            for route in ROUTES:
                text=json.dumps(to_public(r,route))
                for value in forbidden:self.assertNotIn(value,text)
    def test_malformed_inputs_fail_closed(self):
        for p in BATCH:
            for key,value in (('imports',{}),('documents','bad'),('governance_method',None),('owner_links',True)):
                c=case(p);c[key]=value;self.assertEqual('blocked',assess_case(p,c)['status'])
    def test_generated_artifacts_current(self):
        from generate_final_batch_examples import artifacts,routes
        for p,fw,a in routes():
            for path,value in artifacts(p,fw,a).items():
                from production import serializable
                self.assertEqual(json.loads(json.dumps(value,default=serializable)),json.loads(Path(path).read_text()),path)

def _feature_test(k):
    def test(self):
        c=case(BATCH[0]);c['plans'][0][k]=True;self.sync(c,'plans','plan_source');self.content(c,'terms')[k]=True;self.block(c)
    return test
for _k in ('amendment','settlement','curtailment','minimum_funding','asset_ceiling_issue','fx','contributions_already_expensed','assumption_selection_requested'):setattr(FinalBatch,'test_db_excluded_'+_k,_feature_test(_k))
def _scope_test(k):
    def test(self):
        for p in BATCH:
            c=case(p);c['governance_method'][k]=True;self.block(c)
    return test
for _k in ('external_write','legal_certification','audit_opinion','regulatory_compliance','forecasting','budgeting','ipo_timing_prediction','benchmark_requested','manufactured_explanations'):setattr(FinalBatch,'test_scope_'+_k,_scope_test(_k))

if __name__=='__main__':unittest.main()

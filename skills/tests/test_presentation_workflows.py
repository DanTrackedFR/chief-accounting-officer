import copy,json,unittest,sys,tempfile,subprocess
from pathlib import Path
from decimal import Decimal
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
from presentation_cases import *
from production import assess_case,to_public,case_fingerprint,canonical_knowledge,serializable
from interfaces.public_output import ROUTES

class PresentationTests(unittest.TestCase):
    def blocked(self,p,c,f='IFRS'):
        r=assess_case(p,ready(p,f,c));self.assertEqual(r['status'],'blocked',r['conclusion']);self.assertEqual(r['journal_entry_implications'],[])
    def test_four_framework_ordinary(self):
        for p in PACKAGES:
            for f in FRAMEWORKS:
                r=assess_case(p,ready(p,f));self.assertEqual(r['status'],'complete',r['conclusion']);self.assertEqual(r['journal_entry_implications'],[])
    def test_knowledge_blockers_cannot_certify(self):
        for p in BLOCKED:
            for f in FRAMEWORKS:
                c=case(p,f);c['reviewer_signoff']=dict(approved=True,reviewer='independent',case_fingerprint=case_fingerprint(c));r=assess_case(p,c);self.assertEqual(r['status'],'blocked');self.assertEqual(r['calculations'],{});self.assertEqual(r['journal_entry_implications'],[]);to_public(r)
    def test_partial(self):
        for p in PACKAGES:
            for f in FRAMEWORKS:
                c=ready(p,f);c.pop('reviewer_signoff');self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_stale_certification(self):
        for p in PACKAGES:
            c=ready(p);c['assumptions'].append('Additional actual assumption');self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_reviewer_independence(self):
        for p in PACKAGES:
            c=ready(p);c['reviewer_signoff']['reviewer']=c['preparer'];self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_stale_implementation(self):
        for p in PACKAGES:
            c=ready(p)
            with patch('production.case_fingerprint',return_value='changed'):self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_stale_knowledge(self):
        for p in PACKAGES:
            c=ready(p);c['knowledge_review']['documents'][0]['sha256']='changed';self.assertEqual(assess_case(p,c)['status'],'blocked')
    def test_public_privacy(self):
        for p in PACKAGES:
            for f in FRAMEWORKS:
                c=ready(p,f);c['disclosure_review']['reviewer_private']='INTERNAL_SECRET';c=ready(p,f,c);r=assess_case(p,c)
                for route in ROUTES:
                    public=json.dumps(to_public(r,route));self.assertNotIn('INTERNAL_SECRET',public)
                    for token in ('case_fingerprint','source_note','knowledge_review','MODEL_DERIVED_AUDIT_REQUIRED','synthetic independent reviewer'):self.assertNotIn(token,public)
    def test_source_context(self):
        for p,key in [('earnings-per-share','share_intervals'),('segment-reporting','components'),('subsequent-events','events')]:
            for field,value in [('source_entity','other'),('source_framework','other'),('source_period',['2025-01-01','2025-12-31'])]:
                c=case(p);c[key][0][field]=value;self.blocked(p,c)
    def test_missing_evidence(self):
        for p,key in [('earnings-per-share','share_intervals'),('segment-reporting','components'),('subsequent-events','events')]:
            c=case(p);c[key][0]['evidence']='';self.blocked(p,c)
    def test_stale_source_approval(self):
        for p,key in [('earnings-per-share','share_intervals'),('segment-reporting','components'),('subsequent-events','events')]:
            c=case(p);c[key][0]['approved_version']='other';self.blocked(p,c)
    def test_population_count_and_amount(self):
        for p in PACKAGES:
            for key,val in [('population_count',99),('population_amount','99999')]:
                c=case(p);c['controls'][key]=val;self.blocked(p,c)
    def test_incomplete_source_inventory(self):
        for p in PACKAGES:
            c=case(p);c['source_inventory']=[];self.blocked(p,c)
    def test_missing_preparer(self):
        for p in PACKAGES:
            c=case(p);c.pop('preparer');self.blocked(p,c)
    def test_disclosure_missing(self):
        for p in PACKAGES:
            c=case(p);c['disclosure_review']['complete']=False;self.blocked(p,c)
    def test_framework_scope(self):
        for p in PACKAGES:
            for f in FRAMEWORKS:
                c=case(p,f);c['accounting_policy']['framework']='wrong';self.blocked(p,c,f)
    def test_period_scope(self):
        for p in PACKAGES:
            c=case(p);c['accounting_policy']['effective_period']=['2025-01-01','2025-12-31'];self.blocked(p,c)
    def test_entity_scope(self):
        for p in PACKAGES:
            c=case(p);c['accounting_policy']['entity_scope']='nonprofit';self.blocked(p,c)
    def test_framework_overlay(self):
        for p in PACKAGES:
            c=case(p,'AASB');c['entity_type']='nonprofit';self.blocked(p,c,'AASB')
            c=case(p,'UK_GAAP');c['uk_standard']='FRS_105';self.blocked(p,c,'UK_GAAP')
    def test_adoption_unresolved(self):
        for p in PACKAGES:
            c=case(p);c['applicability_review']['exceptions']=['Unresolved adopted amendment'];self.blocked(p,c)
    def test_input_immutability(self):
        for p in PACKAGES:
            c=ready(p);old=copy.deepcopy(c);assess_case(p,c);self.assertEqual(c,old)
    def test_malformed_input(self):
        for p in PACKAGES:
            for value in ([],None,'notobject'):self.assertEqual(assess_case(p,value)['status'],'blocked')
    def test_eps_daily_issuance(self):
        c=case('earnings-per-share');r=c['share_intervals'][0];r['end']='2026-06-30';second=approved('second',start='2026-07-01',end='2026-12-31',issued='120',treasury='0',movement=pol(c,'issue',date='2026-07-01',kind='ordinary',issued_change='20',treasury_change='0',legal_memo='Actual dated issue'))
        dimensions(c,[second]);c['share_intervals'].append(second);c['source_inventory'].append('second');c['controls'].update(population_count=2,population_amount='220');c['closing_issued']='120';w=Decimal(100)+Decimal(20)*184/365;c['expected_weighted_shares']=str(w)
        c['statement'].update(basic_total=str(100/w),basic_continuing=str(100/w),diluted_total=str(106/(w+10)),diluted_continuing=str(106/(w+10)))
        r=assess_case('earnings-per-share',ready('earnings-per-share',c=c));self.assertEqual(r['status'],'complete',r['conclusion']);self.assertEqual(r['calculations']['weighted_shares'],w)
        c['expected_weighted_shares']='120';self.blocked('earnings-per-share',c)
    def test_eps_retrospective_postperiod_split(self):
        c=case('earnings-per-share');a=approved('split',kind='split',date='2027-01-15',factor='2',legal_terms='Actual two-for-one',retrospective_memo='Reviewed retrospective adjustment');dimensions(c,[a]);c['retrospective_actions']=[a];c['retrospective_inventory']=['split'];c['expected_weighted_shares']='200';c['potential_shares']=[];c['instrument_inventory']=[]
        for k in ('basic_total','basic_continuing','diluted_total','diluted_continuing'):c['statement'][k]='.5'
        c['comparatives']=[approved('prior',period_end='2025-12-31',original_weighted_shares='100',restated_weighted_shares='200',ordinary_profit='100',basic_eps='.5',method=method(c,'prior-method','EPS comparative accounting'))];c['comparative_inventory']=['prior']
        r=assess_case('earnings-per-share',ready('earnings-per-share',c=c));self.assertEqual(r['status'],'complete',r['conclusion'])
        c['expected_weighted_shares']='100';self.blocked('earnings-per-share',c)
    def test_eps_antidilution(self):
        c=case('earnings-per-share');c['potential_shares'][0]['method'].update(total_numerator_adjustment='20',continuing_numerator_adjustment='20');c['statement'].update(diluted_total='1',diluted_continuing='1');r=assess_case('earnings-per-share',ready('earnings-per-share',c=c));self.assertEqual(r['status'],'complete');self.assertFalse(r['calculations']['instrument_tests'][0]['included'])
    def test_eps_continuing_loss_total_gain(self):
        c=case('earnings-per-share');c['numerator'].update(continuing_profit='10',ordinary_continuing='-10',ordinary_discontinued='110');bind_statement(c,{k:c['numerator'][k] for k in ('profit','nci','preferred','other','continuing_profit','continuing_nci','continuing_preferred','continuing_other')});c['statement'].update(basic_continuing='-.1',basic_discontinued='1.1',diluted_total='1',diluted_continuing='-.1',diluted_discontinued='1.1');r=assess_case('earnings-per-share',ready('earnings-per-share',c=c));self.assertEqual(r['status'],'complete',r['conclusion']);self.assertEqual(r['calculations']['diluted_shares'],100)
    def test_eps_zero_denominator(self):
        c=case('earnings-per-share');c['share_intervals'][0]['treasury']='100';c.update(opening_treasury='100',closing_treasury='100',expected_weighted_shares='0');self.blocked('earnings-per-share',c)
    def test_eps_zero_activity(self):
        c=case('earnings-per-share');c['numerator'].update(profit='0',preferred='0',continuing_profit='0',continuing_preferred='0',ordinary_total='0',ordinary_continuing='0');bind_statement(c,{k:c['numerator'][k] for k in ('profit','nci','preferred','other','continuing_profit','continuing_nci','continuing_preferred','continuing_other')});c['potential_shares']=[];c['instrument_inventory']=[];c['statement']={k:'0' for k in c['statement']};self.assertEqual(assess_case('earnings-per-share',ready('earnings-per-share',c=c))['status'],'complete')
    def test_eps_specialist_boundaries(self):
        for key in ('multiple_class','participating_securities','additional_per_share'):
            c=case('earnings-per-share');c['eps_method'][key]=True;self.blocked('earnings-per-share',c)
    def test_eps_interval_gap(self):
        c=case('earnings-per-share');c['share_intervals'][0]['start']='2026-01-02';self.blocked('earnings-per-share',c)
    def test_eps_fractional_legal_shares(self):
        c=case('earnings-per-share');c['share_intervals'][0]['issued']='100.5';self.blocked('earnings-per-share',c)
    def test_eps_instrument_population(self):
        c=case('earnings-per-share');c['instrument_inventory']=[];self.blocked('earnings-per-share',c)
    def test_eps_instrument_method_unresolved(self):
        c=case('earnings-per-share');c['potential_shares'][0]['method']['resolved']=False;self.blocked('earnings-per-share',c)
    def test_eps_option_numerator_not_addback(self):
        c=case('earnings-per-share');c['potential_shares'][0]['method']['kind']='treasury_stock';self.blocked('earnings-per-share',c)
    def test_eps_malformed_decimal(self):
        for val in ('NaN','Infinity','1e999999',True):
            c=case('earnings-per-share');c['numerator']['profit']=val;self.blocked('earnings-per-share',c)
    def test_segment_codm_not_legal_entity(self):
        c=case('segment-reporting');c['components'][0]['regular_codm_review']=False;self.blocked('segment-reporting',c)
    def test_segment_missing_aggregation_evidence(self):
        c=case('segment-reporting');c['groups'][0]['members']=['A','B'];c['groups']=c['groups'][:1];c['group_inventory']=['A'];self.blocked('segment-reporting',c)
    def test_segment_required_cannot_omit(self):
        c=case('segment-reporting');c['groups'][1]['reported']=False;self.blocked('segment-reporting',c)
    def test_segment_coverage(self):
        c=case('segment-reporting');c['segment_method']['thresholds'].update(revenue='.9',profit='.9',assets='.9');c['groups'][1]['reported']=False;self.blocked('segment-reporting',c)
    def test_segment_elimination_sign(self):
        c=case('segment-reporting');c['reconciliations'][0]['items'][0]['amount']='100';self.blocked('segment-reporting',c)
    def test_segment_geographic_population(self):
        c=case('segment-reporting');c['entity_wide']['geographic_inventory']=[];self.blocked('segment-reporting',c)
    def test_segment_major_customer(self):
        c=case('segment-reporting');c['entity_wide']['customers'][0]['major']=False;self.blocked('segment-reporting',c)
    def test_segment_duplicate_component(self):
        c=case('segment-reporting');c['groups'][1]['members']=['A'];self.blocked('segment-reporting',c)
    def test_segment_changed_comparatives(self):
        c=case('segment-reporting');c['segment_method'].update(structure_changed=True,comparatives_reconciled=False);self.blocked('segment-reporting',c)
    def test_segment_us_disclosure_gate(self):
        c=case('segment-reporting','US_GAAP');c['segment_method'].pop('significant_expense_memo');self.blocked('segment-reporting',c,'US_GAAP')
    def test_segment_uk_scope_gate(self):
        c=case('segment-reporting','UK_GAAP');c['segment_method']['uk_scope']='generic_IFRS8';self.blocked('segment-reporting',c,'UK_GAAP')
    def test_events_adjusting_completed_owner(self):
        for f in FRAMEWORKS:
            c=adjusting(f);r=assess_case('subsequent-events',ready('subsequent-events',f,c));self.assertEqual(r['status'],'complete',r['conclusion']);self.assertEqual(r['journal_entry_implications'],[]);self.assertIn(Decimal(10),r['calculations']['statement_adjustments'].values())
    def test_events_chronology(self):
        for field,value in [('event_date','2026-12-31'),('learned_date','2027-04-01'),('condition_date','2026-12-01')]:
            c=case('subsequent-events');c['events'][0][field]=value;self.blocked('subsequent-events',c)
    def test_events_incomplete_feed(self):
        c=case('subsequent-events');c['feeds'][0]['reviewed_through']='2027-03-30';self.blocked('subsequent-events',c)
    def test_events_missing_feed_event(self):
        c=case('subsequent-events');c['feeds'][2]['event_ids']=[];self.blocked('subsequent-events',c)
    def test_events_disclosure_inestimable(self):
        c=case('subsequent-events');c['events'][0].update(effect_estimable=False,inability_to_estimate_memo='Qualified inability to estimate');self.assertEqual(assess_case('subsequent-events',ready('subsequent-events',c=c))['status'],'complete')
    def test_events_material_cannot_omit(self):
        c=case('subsequent-events');c['events'][0]['disclosed']=False;self.blocked('subsequent-events',c)
    def test_events_nonadjusting_no_journal(self):
        c=case('subsequent-events');c['events'][0]['measurement_change']='100';self.blocked('subsequent-events',c)
    def test_events_basis_override(self):
        c=case('subsequent-events');c['event_method']['basis_appropriate']=False;self.blocked('subsequent-events',c)
    def test_events_post_issuance(self):
        c=case('subsequent-events');c['event_method']['post_issuance']=True;self.blocked('subsequent-events',c)
    def test_events_us_cutoff_difference(self):
        c=case('subsequent-events','US_GAAP');c['us_entity_type']='private';c['event_method']['window_basis']='available_to_issue';self.assertEqual(assess_case('subsequent-events',ready('subsequent-events','US_GAAP',c))['status'],'complete');c['event_method']['window_basis']='issuance';self.blocked('subsequent-events',c,'US_GAAP')
    def test_events_unbalanced_statement(self):
        c=case('subsequent-events');c['statement_balances'][0].update(original='110',revised='110',statement='110');self.blocked('subsequent-events',c)
    def test_events_wrong_recognition_owner(self):
        c=adjusting();c['accounting_updates'][0]['revised']['package']='business-combinations';self.blocked('subsequent-events',c)
    def test_events_import_dimensions(self):
        for field,val in [('entity','Other'),('framework','Other'),('reporting_period','2025-12-31')]:
            c=adjusting();c['accounting_updates'][0]['revised']['case'][field]=val;self.blocked('subsequent-events',c)
    def test_events_stale_owner(self):
        c=adjusting();c['accounting_updates'][0]['revised']['case']['assumptions'].append('Changed');self.blocked('subsequent-events',c)
    def test_events_zero_activity(self):
        c=case('subsequent-events');c['events']=[];c['source_inventory']=[];c['controls']['population_count']=0
        for f in c['feeds']:f['event_ids']=[]
        self.assertEqual(assess_case('subsequent-events',ready('subsequent-events',c=c))['status'],'complete')
    def test_QA_owner_stock_cannot_be_delta_only(self):
        c=adjusting()
        for r in c['statement_balances']:
            if r['id']=='provision':r.update(original='0',revised='-10',statement='-10')
            if r['id']=='opening equity':r.update(original='5',revised='5',statement='5')
        self.blocked('subsequent-events',c)
    def test_QA_split_must_change_legal_boundary(self):
        c=case('earnings-per-share');c['share_intervals'][0]['end']='2026-06-30';s=approved('second',start='2026-07-01',end='2026-12-31',issued='100',treasury='0',movement=pol(c,'ignored',date='2026-07-01',kind='ordinary',issued_change='0',treasury_change='0',legal_memo='False unchanged'))
        a=approved('split',date='2026-07-01',kind='split',factor='2',legal_terms='Actual2:1',retrospective_memo='Retrospective');dimensions(c,[s,a]);c['share_intervals'].append(s);c.update(source_inventory=['year','second'],retrospective_actions=[a],retrospective_inventory=['split'],expected_weighted_shares=str(Decimal(100)*181/365*2+Decimal(100)*184/365));c['controls'].update(population_count=2,population_amount='200');self.blocked('earnings-per-share',c)
    def test_QA_actual_FS_contradiction(self):
        from additional_cases import reporting,certify
        for p in ('earnings-per-share','segment-reporting'):
            for f in FRAMEWORKS:
                c=case(p,f);s=certify('financial-statements',reporting(f));c['imports']=[approved('actual',package='financial-statements',case=s,result=execute('financial-statements',s),mode='evidence_only')];self.blocked(p,c,f)
    def test_statement_source_missing_account(self):
        c=case('earnings-per-share');c['financial_statement_source']['lines'][0]['account']='missing';self.blocked('earnings-per-share',c)
    def test_statement_source_amount_not_GL(self):
        c=case('segment-reporting');c['financial_statement_source']['lines'][0]['amount']='999';self.blocked('segment-reporting',c)
    def test_eps_valid_inperiod_split(self):
        c=case('earnings-per-share');c['share_intervals'][0]['end']='2026-06-30';s=approved('second',start='2026-07-01',end='2026-12-31',issued='200',treasury='0',movement=pol(c,'split-move',date='2026-07-01',kind='split',legal_memo='Actual two-for-one'))
        a=approved('split',date='2026-07-01',kind='split',factor='2',legal_terms='Actual2:1',retrospective_memo='Retrospective');dimensions(c,[s,a]);c['share_intervals'].append(s);c.update(source_inventory=['year','second'],retrospective_actions=[a],retrospective_inventory=['split'],expected_weighted_shares='200',closing_issued='200',potential_shares=[],instrument_inventory=[]);c['controls'].update(population_count=2,population_amount='300')
        for key in ('basic_total','basic_continuing','diluted_total','diluted_continuing'):c['statement'][key]='.5'
        self.assertEqual(assess_case('earnings-per-share',ready('earnings-per-share',c=c))['status'],'complete')
    def test_eps_sequencing(self):
        c=case('earnings-per-share');r=copy.deepcopy(c['potential_shares'][0]);r['id']='second';r['method'].update(total_numerator_adjustment='8',continuing_numerator_adjustment='8');c['potential_shares'].insert(0,r);c['instrument_inventory'].append('second');c['statement'].update(diluted_total='.95',diluted_continuing='.95');res=assess_case('earnings-per-share',ready('earnings-per-share',c=c));self.assertEqual(res['status'],'complete',res['conclusion']);self.assertEqual(res['calculations']['diluted_shares'],120)
    def test_eps_treasury_and_repurchase(self):
        c=case('earnings-per-share');c.update(opening_treasury='10',closing_treasury='10',expected_weighted_shares='90');c['share_intervals'][0]['treasury']='10';c['statement'].update(basic_total=str(Decimal(100)/90),basic_continuing=str(Decimal(100)/90),diluted_total='1.06',diluted_continuing='1.06');self.assertEqual(assess_case('earnings-per-share',ready('earnings-per-share',c=c))['status'],'complete')
    def test_eps_zero_incremental_adjustment(self):
        c=case('earnings-per-share');c['potential_shares'][0]['method']['incremental_weighted_shares']='0';self.blocked('earnings-per-share',c)
    def test_segment_profit_loss_denominator(self):
        c=case('segment-reporting');c['components'][1]['profit']='-40';c['reconciliations'][1].update(segment_total='140',consolidated='120',statement='120');bind_statement(c,dict(revenue='1000',profit='120',assets='1600',liabilities='600'));r=assess_case('segment-reporting',ready('segment-reporting',c=c));self.assertEqual(r['status'],'complete');self.assertEqual(r['calculations']['profit_threshold_basis'],180)
    def test_segment_zero_activity(self):
        c=case('segment-reporting');c.update(components=[],source_inventory=[],groups=[],group_inventory=[]);c['controls'].update(population_count=0,population_amount='0');bind_statement(c,dict(revenue='0',profit='0',assets='0',liabilities='0'))
        for r in c['reconciliations']:r.update(segment_total='0',consolidated='0',statement='0');r['items'][0]['amount']='0'
        for key in ('geographic','products_services','customers'):
            for r in c['entity_wide'][key]:r['external_revenue']='0'
        c['entity_wide']['customers'][0]['major']=False
        self.assertEqual(assess_case('segment-reporting',ready('segment-reporting',c=c))['status'],'complete')
    def test_segment_aggregation_supported(self):
        c=case('segment-reporting');g=c['groups'][0];g['members']=['A','B'];g['aggregation']=method(c,'aggregation','Segment aggregation',criteria_met=True,long_term_economics='Actual long-term economics',products_services='Actual similarity',production_process='Actual process',customers='Actual type',distribution='Actual methods',regulatory_memo='Actual regulation');c['groups']=[g];c['group_inventory']=['A'];self.assertEqual(assess_case('segment-reporting',ready('segment-reporting',c=c))['status'],'complete')
    def test_events_duplicate_update(self):
        c=adjusting();r=copy.deepcopy(c['events'][0]);r['id']='repeat';c['events'].append(r);c['source_inventory'].append('repeat');c['feeds'][1]['event_ids'].append('repeat');c['controls'].update(population_count=2,population_amount='20');self.blocked('subsequent-events',c)
    def test_events_missing_GC_owner(self):
        c=case('subsequent-events');c['events'][0].update(going_concern_impact=True,going_concern_import='missing');self.blocked('subsequent-events',c)
    def test_duplicate_import(self):
        from additional_cases import reporting,certify
        c=case('segment-reporting');s=certify('financial-statements',reporting());r=approved('actual',package='financial-statements',case=s,result=execute('financial-statements',s),mode='evidence_only');c['imports']=[r,dict(r,id='twice')];self.blocked('segment-reporting',c)

if __name__=='__main__':unittest.main()

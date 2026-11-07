"""Independent Phase A accounting QA; reviewer-authored numerical scenarios.

No production helpers are used to calculate expected figures. The existing HTTP
harness supplies transport/configuration only; amounts and assets below are fresh.
"""
import copy
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from datetime import date
from decimal import Decimal as D

from source_execution import execute, monthly_charge, actual_charge, to_public
import hosted_cao.tests.test_presumed_engineering_qa as httpqa


def case(convention='monthly'):
    c=httpqa.synthetic_case(count=1)
    c.update(period_start='2026-05-01',reporting_period='2026-05-31',
             package='fixed-assets',review_mode='prepared_unreviewed',source_assurance='presumed_user_provided')
    c['class_assumptions']={}
    c['assets']=[dict(id='independent-turbine',opening_cost='79200',opening_accumulated='18000',residual='3600',
                      remaining_life_months='24',ready_date='2025-03-17',method='straight_line',scope='ordinary_ppe')]
    if convention is not None:c['policy_elections']={'depreciation_convention':convention}
    return c


def run(c):return execute('fixed-assets',c)
def amount(result):return result['calculations']['depreciation']
def public(result):return to_public(result,'tool_output')


class IndependentAccounting(unittest.TestCase):
    def test_may_monthly_actual_and_legacy(self):
        for convention,expected in [('monthly','2400'),('actual_days','2446.03'),(None,'2446.03')]:
            r=run(case(convention));self.assertEqual(amount(r),D(expected))
            a=r['calculations']['assets'][0]
            self.assertEqual(a['closing_accumulated'],D('18000')+D(expected))
            self.assertEqual(a['carrying'],D('61200')-D(expected))
            lines=r['proposed_journal_workpaper'][0]
            self.assertEqual(lines,[dict(side='Dr',account='depreciation expense',amount=D(expected)),dict(side='Cr',account='accumulated depreciation',amount=D(expected))])
    def test_february_and_leap_arithmetic_scope(self):
        c=case();c.update(period_start='2026-02-01',reporting_period='2026-02-28')
        self.assertEqual(amount(run(c)),D('2400'))
        c['policy_elections']['depreciation_convention']='actual_days'
        self.assertEqual(amount(run(c)),D('2209.32'))
        self.assertEqual(monthly_charge(date(2024,2,1),date(2024,2,29),D('57600'),D(24),None),D('2400'))
        self.assertEqual(actual_charge(date(2024,2,1),date(2024,2,29),D('57600'),D(24)),D('2281.97'))
        c.update(period_start='2028-02-01',reporting_period='2028-02-29')
        self.assertFalse(run(c)['proposed_journal_workpaper'])
    def test_year_month_equivalence_and_conflicts(self):
        for convention in ('monthly','actual_days'):
            for months,monthly_expected in [(12,'3780'),(24,'1890'),(36,'1260'),(60,'756')]:
                c=case(convention);a=c['assets'][0]
                a.update(opening_cost='50000',opening_accumulated='4000',residual='640',remaining_life_months=str(months))
                m=run(c)
                if convention=='monthly':self.assertEqual(amount(m),D(monthly_expected))
                a.pop('remaining_life_months');a['remaining_life']=str(D(months)/12)
                self.assertEqual(m['proposed_journal_workpaper'],run(c)['proposed_journal_workpaper'])
                a['remaining_life_months']=str(months)
                self.assertEqual(m['proposed_journal_workpaper'],run(c)['proposed_journal_workpaper'])
                a['remaining_life_months']=str(months+1)
                self.assertFalse(run(c)['proposed_journal_workpaper'])
    def test_partial_stub_and_addition(self):
        for style in ('stub','addition'):
            c=case();a=c['assets'][0]
            if style=='stub':c['period_start']='2026-05-11'
            else:
                a.update(opening_cost='0',opening_accumulated='0',residual='0',ready_date='2026-05-11')
                c['costs']=[dict(id='independent-purchase',amount='57600',kind='purchase',date='2026-05-10',offset='accounts payable',destination=a['id'])]
            self.assertFalse(run(c)['proposed_journal_workpaper'])
            c['policy_elections']['partial_month_treatment']='actual_days_in_month'
            r=run(c);self.assertEqual(amount(r),D('1625.81'))
            if style=='addition':self.assertEqual(r['calculations']['assets'][0]['carrying'],D('55974.19'))
    def test_disposal_and_comparison_date(self):
        c=case();a=c['assets'][0]
        c['policy_elections']['partial_month_treatment']='actual_days_in_month'
        a['disposal']=dict(enabled=True,date='2026-05-19',proceeds='62000',ordinary_sale=True,cash_received=False,payment_terms='credit')
        a.update(supplied_net_book_value='0',supplied_accumulated_depreciation='0',comparison_balance_basis='closing')
        r=run(c);self.assertEqual(amount(r),D('1470.97'))
        self.assertEqual(r['calculations']['assets'][0]['disposal_gain'],D('2270.97'))
        self.assertTrue(all(x['status']=='MATCH' for x in r['calculations']['balance_comparisons']))
        disposal=r['proposed_journal_workpaper'][1]
        self.assertIn(dict(side='Dr',account='disposal receivable',amount=D('62000')),disposal)
        self.assertFalse(any(x['account']=='cash' for x in disposal))
    def test_cap_and_residual_above_carrying(self):
        c=case();a=c['assets'][0]
        a.update(opening_cost='1000',opening_accumulated='771.45',residual='100',remaining_life_months='.5')
        r=run(c);self.assertEqual(amount(r),D('128.55'));self.assertEqual(r['calculations']['assets'][0]['carrying'],D('100'))
        a['residual']='300';r=run(c);self.assertEqual(amount(r),D('0'))
        self.assertFalse(any(r['proposed_journal_workpaper']))
        self.assertTrue(any(f['severity']=='WARNING' for f in r['anomaly_report']['findings']))
    def test_exhausted_negative_null_mixed_isolation(self):
        for value,word in [('0','exhausted'),('-1','Negative'),(None,'Null'),('oops','Nonnumeric')]:
            c=case();bad=copy.deepcopy(c['assets'][0]);bad.update(id='invalid-life',remaining_life_months=value)
            c['assets'].append(bad);r=run(c)
            self.assertEqual(amount(r),D('2400'));self.assertEqual(len(r['proposed_journal_workpaper']),1)
            self.assertEqual(r['accounting_determination'],'UNRESOLVED')
            self.assertTrue(any(word in n['explanation'] and n['field_path']=='assets[2].remaining_life_months' for n in r['validation_requirements']))
            p=public(r);self.assertEqual({x['row_reference'] for x in p['proposed_journals']},{'assets:1'})
    def test_fully_depreciated_in_use_no_disposal(self):
        c=case();c['assets'][0].update(opening_accumulated='79200',residual='0',remaining_life_months='0')
        r=run(c);self.assertFalse(r['proposed_journal_workpaper'])
        self.assertTrue(any('not automatically disposed' in n['explanation'] for n in r['validation_requirements']))
    def test_comparison_material_error_and_no_override(self):
        c=case();base=run(c)['proposed_journal_workpaper'];a=c['assets'][0]
        a.update(supplied_net_book_value='318800',supplied_accumulated_depreciation='20400',comparison_balance_basis='closing')
        r=run(c);self.assertEqual(base,r['proposed_journal_workpaper'])
        comps=r['calculations']['balance_comparisons'];self.assertEqual(comps[0]['variance'],'260000.00')
        self.assertEqual(comps[1]['status'],'MATCH');self.assertEqual(comps[2]['status'],'MISMATCH')
        a.update(supplied_net_book_value='61200',supplied_accumulated_depreciation='18000',comparison_balance_basis='opening')
        self.assertTrue(all(x['status']=='MATCH' for x in run(c)['calculations']['balance_comparisons']))
        a.pop('supplied_net_book_value');self.assertEqual(len(run(c)['calculations']['balance_comparisons']),1)
    def test_sequential_period_life_rollforward(self):
        c=case();may=run(c);a=c['assets'][0]
        a['opening_accumulated']='20400';a['remaining_life_months']='23'
        c.update(period_start='2026-06-01',reporting_period='2026-06-30')
        june=run(c);self.assertEqual(amount(may)+amount(june),D('4800'))
        self.assertEqual(june['calculations']['assets'][0]['carrying'],D('56400'))
    def test_confirmed_policy_conflict_and_provenance(self):
        c=case(None);c['asset_policy']=dict(depreciation_convention='monthly',confirmation='confirmed',entity='ENTITY-DEMO',framework='IFRS',effective_from='2026-04-01',effective_to='2026-12-31',policy_version='independent-policy')
        r=run(c);self.assertEqual(amount(r),D('2400'))
        assumptions=public(r)['applied_assumptions']
        self.assertTrue(any(x['field']=='depreciation_convention' and x['value']=='monthly' and x['provenance']=='confirmed_company_policy_client_asserted' for x in assumptions))
        c['policy_elections']={'depreciation_convention':'actual_days'};self.assertFalse(run(c)['proposed_journal_workpaper'])
        c['policy_elections']={};c['asset_policy']['effective_to']='2026-05-15';self.assertFalse(run(c)['proposed_journal_workpaper'])
    def test_only_actual_class_assumptions_are_exposed(self):
        c=case();a=c['assets'][0];a['class']='machinery'
        c['class_assumptions']={'machinery':dict(framework='IFRS',entity='ENTITY-DEMO',effective_from='2026-01-01',effective_to='2026-12-31',policy_version='independent-class',remaining_life='9',residual='6400',approved_by='private-policy-identity')}
        r=run(c);self.assertEqual(amount(r),D('2400'))
        assumptions=public(r)['applied_assumptions']
        self.assertFalse(any(x['field']=='remaining_life' for x in assumptions))
        self.assertTrue(any(x['field']=='residual' and x['value']=='3600' and x['provenance']=='explicit_user_input' for x in assumptions))
        a.pop('residual');r=run(c);self.assertEqual(amount(r),D('2283.33'))
        assumptions=public(r)['applied_assumptions']
        self.assertTrue(any(x['field']=='residual' and x['value']=='6400' and x['provenance']=='client_asserted_class_assumption' for x in assumptions))
        self.assertNotIn('private-policy-identity',str(public(r)))
    def test_default_is_not_claimed_confirmed(self):
        r=run(case(None));assumptions=public(r)['applied_assumptions']
        self.assertTrue(any(x['field']=='depreciation_convention' and x['value']=='actual_days' and x['provenance']=='engine_default_unconfirmed' for x in assumptions))
        self.assertFalse(any(x['provenance']=='confirmed_company_policy_client_asserted' for x in assumptions))

    def test_supported_frameworks_and_no_broadening(self):
        for fw,extra in [('IFRS',{}),('US_GAAP',{'us_entity_type':'private_company'}),('UK_GAAP',{'uk_standard':'FRS_102','uk_standard_edition':'2026'}),('AASB',{'aasb_compilation':'2026','reporting_tier':2})]:
            c=case();c.update(framework=fw,**extra)
            self.assertEqual(amount(run(c)),D('2400'))
        c=case();c['entity_type']='not_for_profit';self.assertFalse(run(c)['proposed_journal_workpaper'])


class IndependentHostedAccounting(unittest.TestCase):
    setUp=httpqa.IndependentPresumedEngineeringQA.setUp
    new_service=httpqa.IndependentPresumedEngineeringQA.new_service
    close=httpqa.IndependentPresumedEngineeringQA.close
    envelope=httpqa.IndependentPresumedEngineeringQA.envelope
    http=httpqa.IndependentPresumedEngineeringQA.http
    call=httpqa.IndependentPresumedEngineeringQA.call
    start=httpqa.IndependentPresumedEngineeringQA.start
    stage=httpqa.IndependentPresumedEngineeringQA.stage
    job=httpqa.IndependentPresumedEngineeringQA.job
    native=httpqa.IndependentPresumedEngineeringQA.native

    def test_real_http_cross_stage_mixed_row_and_reconciliation(self):
        context_path=self.workspace/'company-context.md'
        context_path.write_text(context_path.read_text().replace('period_start: 2026-01-01','period_start: 2026-05-01').replace('period_end: 2026-12-31','period_end: 2026-05-31'))
        c=case();a=c['assets'][0]
        a.update(supplied_net_book_value='318800',supplied_accumulated_depreciation='20400',comparison_balance_basis='closing')
        bad=copy.deepcopy(a);bad.update(id='exhausted-cross-stage',remaining_life_months='0')
        c['assets'].append(bad)
        cid=self.stage(rid='independent-cross-stage',case=c)
        _,j=self.job(cid,'cross-stage-retry');self.assertTrue(self.service.run_one())
        status,done=self.http('/v1/jobs/'+j['id']);self.assertEqual(status,200)
        self.assertEqual(done['state'],'SUCCEEDED');p=done['accounting']['public_result']
        self.assertEqual(p['accounting_determination'],'UNRESOLVED')
        self.assertEqual(next(x['amount'] for x in p['calculations'] if x['label']=='depreciation'),'2400.00')
        self.assertEqual({x['row_reference'] for x in p['proposed_journals']},{'assets:1'})
        self.assertEqual(p['balance_comparisons'][0]['variance'],'260000.00')
        self.assertEqual({x['row_reference'] for x in p['balance_comparisons']},{'assets:1'})
        self.assertTrue(any(x['field']=='depreciation_convention' and x['provenance']=='case_election' for x in p['applied_assumptions']))
        self.assertFalse(any(x['row_reference']=='assets:2' for x in p['applied_assumptions']))
        _,native=self.native(cid)
        self.assertEqual(len(native['proposed_journal_workpaper']),1)
        self.assertEqual(native['proposed_journal_workpaper'][0][0]['amount'],D('2400.00'))
        status,reopened=self.call('result',case_id=cid);self.assertEqual(status,200)
        self.assertEqual(reopened['public_result'],p)

    def test_real_http_durable_retry_native_journals(self):
        c=case();c['assets'][0]['expected_depreciation']='2400'
        context_path=self.workspace/'company-context.md'
        context_path.write_text(context_path.read_text().replace('period_start: 2026-01-01','period_start: 2026-05-01').replace('period_end: 2026-12-31','period_end: 2026-05-31'))
        cid=self.stage(rid='independent-monthly',case=c)
        status,j=self.job(cid,'independent-retry');self.assertEqual(status,202)
        self.assertTrue(self.service.run_one())
        status,done=self.http('/v1/jobs/'+j['id']);self.assertEqual(status,200)
        self.assertEqual(done['state'],'SUCCEEDED');p=done['accounting']['public_result']
        self.assertEqual(next(x['amount'] for x in p['calculations'] if x['label']=='depreciation'),'2400.00')
        _,native=self.native(cid)
        self.assertEqual([[dict(line,amount=D(line['amount'])) for line in x['lines']] for x in p['proposed_journals']],native['proposed_journal_workpaper'])
        for proposal in p['proposed_journals']:
            dr=sum((D(x['amount']) for x in proposal['lines'] if x['side']=='Dr'),D(0));cr=sum((D(x['amount']) for x in proposal['lines'] if x['side']=='Cr'),D(0));self.assertEqual(dr,cr)
            self.assertEqual(proposal['qualification_status'],'PROPOSED');self.assertEqual(proposal['row_reference'],'assets:1')
        self.assertFalse(native['journal_entry_implications'])
        retry_status,retry=self.job(cid,'independent-retry');self.assertIn(retry_status,(200,202));self.assertEqual(j['id'],retry['id'])
        restarted=self.new_service();self.addCleanup(restarted.close)
        self.assertEqual(restarted.job(httpqa.COMPANY,j['id'])['accounting']['public_result'],p)
        status,reopened=self.call('result',case_id=cid);self.assertEqual(status,200);self.assertEqual(reopened['public_result'],p)

if __name__=='__main__':unittest.main()

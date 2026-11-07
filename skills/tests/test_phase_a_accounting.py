"""Permanent bounded arithmetic regressions for the Phase A correction."""
import copy
import unittest
from decimal import Decimal as D
from datetime import date
from source_execution import execute, actual_charge
from hosted_cao.tests.test_presumed_engineering_qa import synthetic_case

def source(**updates):
    c=synthetic_case(count=1);c.update(package='fixed-assets',review_mode='prepared_unreviewed',source_assurance='presumed_user_provided')
    c.update(updates);return c

def calculate(c):return execute('fixed-assets',c)

class LifeFoundation(unittest.TestCase):
    def test_equivalence(self):
        for months in (12,24,36,60):
            a=source(); a['assets'][0]['remaining_life']=str(D(months)/12)
            b=copy.deepcopy(a);b['assets'][0].pop('remaining_life');b['assets'][0]['remaining_life_months']=str(months)
            x,y=calculate(a),calculate(b)
            self.assertEqual(x['calculations'],y['calculations'] | {'assets':x['calculations']['assets']})
            self.assertEqual(x['proposed_journal_workpaper'],y['proposed_journal_workpaper'])
    def test_specific_aggregate_and_isolation(self):
        for value,word in [(0,'exhausted'),(-1,'Negative'),(None,'Null'),('bad','Nonnumeric')]:
            c=source();c['assets'].append(dict(c['assets'][0],id='valid'));c['assets'][0].update(remaining_life=value);c['assets'][0].pop('ready_date')
            r=calculate(c);needs=r['validation_requirements']
            self.assertTrue(any(word in n['explanation'] and n['field_path']=='assets[1].remaining_life' for n in needs),needs)
            self.assertTrue(any(n['field_path']=='assets[1].ready_date' for n in needs))
            self.assertEqual(len(r['calculations']['assets']),1)
            self.assertEqual(len(r['proposed_journal_workpaper']),1)
    def test_life_conflicts_and_units(self):
        for update in ({'remaining_life':'2','remaining_life_months':'25'}, {'remaining_life_unit':'months'}):
            c=source();c['assets'][0].update(update);r=calculate(c)
            self.assertFalse(r['proposed_journal_workpaper']);self.assertTrue(r['validation_requirements'])
        c=source();c['assets'][0].update(remaining_life='2',remaining_life_months='24')
        self.assertEqual(calculate(c)['calculations']['depreciation'],D('5500'))
    def test_missing_and_fully_depreciated_zero_life(self):
        c=source();c['class_assumptions']['machinery'].pop('remaining_life')
        self.assertIn('Missing remaining useful life',calculate(c)['validation_requirements'][0]['explanation'])
        c['assets'][0].update(remaining_life='0',opening_accumulated='11000')
        r=calculate(c);self.assertFalse(r['proposed_journal_workpaper']);self.assertEqual(r['accounting_determination'],'UNRESOLVED')
    def test_cap_residual_and_leap_arithmetic(self):
        self.assertEqual(actual_charge(date(2024,2,1),date(2024,2,29),D(12000),D(12)),D('950.82'))
        self.assertEqual(actual_charge(date(2026,1,1),date(2026,12,31),D(120),D('0.1')),D('120'))

class Conventions(unittest.TestCase):
    def month(self,month,end,**kwargs):
        c=source(period_start='2026-'+month+'-01',reporting_period='2026-'+month+'-'+end,**kwargs)
        c['assets'][0].update(opening_cost='24000',remaining_life='10')
        return c
    def test_monthly_and_legacy(self):
        for month,last,actual in [('05','31','203.84'),('02','28','184.11')]:
            c=self.month(month,last)
            self.assertEqual(calculate(c)['calculations']['depreciation'],D(actual))
            c['policy_elections']={'depreciation_convention':'monthly'};c['assets'][0]['expected_depreciation']='200'
            r=calculate(c);self.assertEqual(r['calculations']['depreciation'],D('200'))
            self.assertFalse(any(f['severity']=='WARNING' and f['check_id']=='depreciation_comparison' for f in r['anomaly_report']['findings']))
    def test_partial_readiness_disposal(self):
        for mode in ('stub','ready','disposal'):
            c=self.month('05','31',policy_elections={'depreciation_convention':'monthly'})
            if mode=='stub':c['period_start']='2026-05-16'
            if mode=='ready':c['assets'][0]['ready_date']='2026-05-16'
            if mode=='disposal':c['assets'][0]['disposal']=dict(enabled=True,date='2026-05-16',proceeds='1000',ordinary_sale=True,cash_received=True)
            r=calculate(c);self.assertFalse(r['proposed_journal_workpaper']);self.assertIn('partial',str(r['validation_requirements']))
            c['policy_elections']['partial_month_treatment']='actual_days_in_month'
            self.assertEqual(calculate(c)['calculations']['depreciation'],D('103.23'))
    def test_policy_precedence_and_compatibility(self):
        c=self.month('05','31');c['asset_policy']=dict(depreciation_convention='monthly',confirmation='confirmed',entity='ENTITY-DEMO',framework='IFRS',effective_from='2026-01-01',effective_to='2026-12-31',policy_version='v1')
        self.assertEqual(calculate(c)['calculations']['depreciation'],D('200'))
        c['policy_elections']={'depreciation_convention':'actual_days'}
        self.assertFalse(calculate(c)['proposed_journal_workpaper'])
        c['policy_elections']={'depreciation_convention':'monthly'}
        self.assertEqual(calculate(c)['calculations']['depreciation'],D('200'))
        c['asset_policy']['entity']='OTHER';self.assertFalse(calculate(c)['proposed_journal_workpaper'])
    def test_leap_month_and_final_cap(self):
        from source_execution import monthly_charge
        self.assertEqual(monthly_charge(date(2024,2,1),date(2024,2,29),D(12000),D(12),None),D('1000'))
        self.assertEqual(monthly_charge(date(2026,5,1),date(2026,5,31),D(120),D('.1'),None),D('120'))
    def test_months_equivalence_both_conventions(self):
        for convention in ('monthly','actual_days'):
            for months in (12,24,36,60):
                c=self.month('05','31',policy_elections={'depreciation_convention':convention})
                c['assets'][0]['remaining_life']=str(D(months)/12);a=calculate(c)
                c['assets'][0].pop('remaining_life');c['assets'][0]['remaining_life_months']=str(months)
                self.assertEqual(a['proposed_journal_workpaper'],calculate(c)['proposed_journal_workpaper'])

class BalanceComparisons(unittest.TestCase):
    def test_matching_and_material_mismatch_without_journal_change(self):
        c=source();expected=calculate(c)['proposed_journal_workpaper']
        c['assets'][0].update(supplied_net_book_value='9900',supplied_accumulated_depreciation='1100',comparison_balance_basis='closing')
        r=calculate(c);self.assertTrue(all(x['status']=='MATCH' for x in r['calculations']['balance_comparisons']))
        self.assertEqual(r['proposed_journal_workpaper'],expected)
        c['assets'][0]['supplied_net_book_value']='269900';r=calculate(c)
        self.assertEqual(r['calculations']['balance_comparisons'][0]['variance'],'260000.00')
        self.assertEqual(r['proposed_journal_workpaper'],expected)
        self.assertEqual(r['calculations']['balance_comparisons'][-1]['status'],'MISMATCH')
    def test_basis_partial_invalid_and_absent(self):
        c=source();self.assertEqual(calculate(c)['calculations']['balance_comparisons'],[])
        for basis,expected in [('opening','11000.00'),('closing','9900.00')]:
            c['assets'][0].update(supplied_net_book_value=expected,comparison_balance_basis=basis)
            r=calculate(c);self.assertEqual(r['calculations']['balance_comparisons'][0]['status'],'MATCH')
        c['assets'][0].pop('comparison_balance_basis');r=calculate(c)
        self.assertEqual(r['calculations']['balance_comparisons'][0]['status'],'UNRESOLVED_BASIS')
        self.assertTrue(r['validation_requirements']);self.assertTrue(r['proposed_journal_workpaper'])
        c['assets'][0]['supplied_net_book_value']='bad';r=calculate(c)
        self.assertEqual(r['calculations']['balance_comparisons'][0]['status'],'INVALID')
    def test_disposal_and_fully_depreciated(self):
        for disposed in (False,True):
            c=source();c['assets'][0].update(opening_accumulated='11000',supplied_net_book_value='0',supplied_accumulated_depreciation='0' if disposed else '11000',comparison_balance_basis='closing')
            if disposed:c['assets'][0]['disposal']=dict(enabled=True,date='2026-06-30',proceeds='1',ordinary_sale=True,cash_received=True)
            self.assertTrue(all(x['status']=='MATCH' for x in calculate(c)['calculations']['balance_comparisons']))

class ActualAssumptions(unittest.TestCase):
    def test_units_of_production_does_not_claim_day_convention(self):
        from source_execution import to_public
        c=source();c['assets'][0].update(method='units_of_production',remaining_units='100',period_units='10')
        r=calculate(c);public=to_public(r,'answer')
        self.assertEqual(r['calculations']['depreciation'],D('1100'))
        self.assertNotIn('Applied depreciation convention:',public['guidance'])
        self.assertFalse(any(a['field']=='depreciation_convention' for a in public['applied_assumptions']))

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

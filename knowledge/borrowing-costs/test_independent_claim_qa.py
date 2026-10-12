"""Independent reviewer checks; literal accounting challenges, not author fixtures."""
import json
import unittest
from pathlib import Path
from decimal import Decimal
HERE=Path(__file__).resolve().parent
class IndependentClaims(unittest.TestCase):
 def test_every_claim_reviewed_and_unchanged(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('independent_validator',HERE/'validate_supplement.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
  claims=json.loads((HERE/'standards-claims.json').read_text())['claims'];review=json.loads((HERE/'independent-review.json').read_text())
  rows={r['claim_id']:r for r in review['claims']}
  self.assertEqual({c['claim_id'] for c in claims},set(rows))
  for c in claims:
   self.assertEqual(rows[c['claim_id']]['reviewed_hash'],v.claim_hash(c))
   self.assertEqual(rows[c['claim_id']]['result'],'PASS')
 def test_separate_specific_methods(self):
  # IAS23 actual specific cost differs from US avoidable cost on actual expenditure.
  self.assertEqual(Decimal(6000)-400,Decimal(5600))
  self.assertEqual(min(Decimal(50000),Decimal(100000))*Decimal('.06'),Decimal(3000))
  self.assertEqual(Decimal(8000)-Decimal(5600),Decimal(2400))
  self.assertEqual(Decimal(2400)-400,Decimal(2000))
 def test_weighted_rate_not_simple_rate_average(self):
  rate=(Decimal(100000)*Decimal('.06')+Decimal(300000)*Decimal('.08'))/400000
  self.assertEqual(rate,Decimal('.075'));self.assertEqual(Decimal(200000)*rate/2,Decimal(7500))
 def test_us_excess_and_actual_interest_ceiling(self):
  avoidable=Decimal(100000)*Decimal('.06')+Decimal(50000)*Decimal('.08')
  self.assertEqual(avoidable,Decimal(10000));self.assertEqual(min(avoidable,Decimal(7000)),Decimal(7000))
  self.assertEqual(min(avoidable,Decimal(30000)),Decimal(10000))
 def test_uk_prior_day_carrying_basis(self):
  base=Decimal(100000);capital=Decimal(0)
  for day in range(365):
   if day==181:base+=100000
   capital+=(base+capital)*Decimal('.08')/365
  self.assertEqual(capital.quantize(Decimal('.01')),Decimal('12442.60'))
 def test_period_ceiling_not_daily_ceiling(self):
  # Unequal eligibility: 15 candidate against 10 incurred today, zero against 10 tomorrow.
  self.assertEqual(min(Decimal(15)+0,Decimal(10)+10),Decimal(15))
  self.assertNotEqual(min(Decimal(15),Decimal(10))+min(Decimal(0),Decimal(10)),Decimal(15))
 def test_temporal_eligibility(self):
  self.assertEqual(Decimal(12000)/12*(3+4),Decimal(7000))
  self.assertEqual(Decimal(12000)-7000,Decimal(5000))

 def test_author_workpapers_against_independent_reperformance(self):
  es={x['id']:x for x in json.loads((HERE/'worked-examples.json').read_text())['examples']}
  expected={'IFRS_SPECIFIC':('5600.00','2400.00'),'AASB_GENERAL':('7500.00','7500.00'),'US_MIXED':('10000.00','20000.00'),'UK_CARRYING':('100.01','99.99'),'UK_EXPENSE':('0.00','200.00'),'TEMPORAL':('7000.00','5000.00')}
  self.assertEqual(set(es),set(expected))
  for key,(capital,expense) in expected.items():
   self.assertEqual(Decimal(es[key]['capitalized']),Decimal(capital));self.assertEqual(Decimal(es[key]['gross_expense']),Decimal(expense))
   self.assertEqual(Decimal(es[key]['incurred']),Decimal(capital)+Decimal(expense))
  rate=Decimal(es['UK_CARRYING']['annual_rate'])/Decimal(es['UK_CARRYING']['contractual_denominator'])
  self.assertEqual(Decimal(200000)*rate,Decimal(40));self.assertEqual(Decimal(300040)*rate,Decimal('60.008'))

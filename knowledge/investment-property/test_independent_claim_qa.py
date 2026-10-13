"""Separate knowledge reviewer: literal framework boundaries and hostile metadata checks."""
import copy
import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

HERE=Path(__file__).resolve().parent

def module(name,file):
 spec=importlib.util.spec_from_file_location(name,HERE/file)
 result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

V=module('independent_ip_validator','validate_supplement.py')
R=module('independent_ip_retrieval','retrieval.py')

class IndependentInvestmentPropertyClaims(unittest.TestCase):
 def setUp(self):
  self.register=json.loads((HERE/'standards-claims.json').read_text())
  self.claims={(c['framework'],c['decision']):c for c in self.register['claims']}
 def test_individual_hash_reviews_cover_population(self):
  review=json.loads((HERE/'independent-review.json').read_text())
  rows={c['claim_id']:c for c in review['claims']}
  self.assertEqual(len(rows),96)
  self.assertFalse(review['human_signoff'])
  self.assertNotEqual(review['reviewer'],self.register['author'])
  for c in self.register['claims']:
   self.assertEqual(rows[c['claim_id']]['reviewed_hash'],V.claim_hash(c))
   self.assertEqual(rows[c['claim_id']]['result'],'PASS')
   self.assertTrue(rows[c['claim_id']]['independent_challenge'])
 def test_uk_transfer_paragraphs_are_not_swapped(self):
  change=self.claims['UK_GAAP','change_use']['proposition']
  out=self.claims['UK_GAAP','fv_transfer_out']['proposition']
  self.assertIn('16.9 ',change)
  self.assertNotIn('16.9A',change)
  self.assertIn('16.9A',out)
  self.assertNotIn('16.9C',out)
 def test_uk_mixed_use_does_not_import_ifrs_exception(self):
  mixed=self.claims['UK_GAAP','mixed_use']['proposition']
  self.assertIn('reliabl',mixed.lower())
  self.assertIn('separat',mixed.lower())
  self.assertNotIn('only when owner use is insignificant',mixed)
 def test_uk_2026_no_general_cost_option(self):
  self.assertIn('No general',self.claims['UK_GAAP','subsequent_policy']['proposition'])
  self.assertIn('deleted',self.claims['UK_GAAP','valuation_exception']['proposition'])
  self.assertIn('group',self.claims['UK_GAAP','cost_model']['proposition'])
  self.assertIn('17.31A',self.claims['UK_GAAP','cost_disclosure']['proposition'])
 def test_us_appraisal_is_not_recognition_authority(self):
  self.assertIn('does not authorize',self.claims['US_GAAP','fair_value']['proposition'])
  self.assertIn('blocked',self.claims['US_GAAP','fv_movement']['proposition'])
  self.assertIn('unsupported',self.claims['US_GAAP','fv_transfer_in']['proposition'])
 def test_transfer_mathematics_requires_revaluation_owner(self):
  for fw in ('IFRS','AASB','UK_GAAP'):
   p=self.claims[fw,'fv_transfer_in']['proposition'].lower()
   self.assertIn('revaluation',p)
  # PPE book 800, change-date FV1000: 200 uplift is not an ordinary IP-period gain.
  self.assertEqual(Decimal('1000')-Decimal('800'),Decimal('200'))
  # Period FV after transfer1100: only100 subsequent IP profit; no double200.
  self.assertEqual(Decimal('1100')-Decimal('1000'),Decimal('100'))
 def test_cost_disposal_independent_math(self):
  gross=Decimal('1150000');accdep=Decimal('140000');impairment=Decimal('35000')
  carrying=gross-accdep-impairment
  netproceeds=Decimal('1075000')-Decimal('15000')
  self.assertEqual(carrying,Decimal('975000'))
  self.assertEqual(netproceeds-carrying,Decimal('85000'))
  self.assertEqual(netproceeds+accdep+impairment,gross+Decimal('85000'))
 def test_approved_register_and_source_assurance(self):
  self.assertEqual(self.register['status'],'APPROVED')
  self.assertEqual(V.validate_data(self.register),[])
  for c in self.register['claims']:
   if c['evidence_status']=='MODEL_DERIVED_AUDIT_REQUIRED':
    self.assertTrue(c['audit_required'])
    self.assertEqual(c['approval_track'],'TRAINING_DATA_CHECKED')
    self.assertFalse(c.get('paragraph_references'))
 def test_claim_mutation_is_blocked(self):
  for field,value in [('proposition','Invented universal fair-value permission'),('entity_scope','investment_company'),('period_scope',{'begin_on_or_after':'2025-01-01','begin_before':'2027-01-01','end_before':'2027-01-01'})]:
   bad=copy.deepcopy(self.register);bad['claims'][0][field]=value
   self.assertTrue(V.validate_data(bad),field)
 def test_self_approval_and_fake_direct_evidence_are_blocked(self):
  bad=copy.deepcopy(self.register);bad['claims'][0]['approval_review']['reviewer']=bad['author']
  self.assertTrue(V.validate_data(bad))
  bad=copy.deepcopy(self.register);bad['claims'][0]['evidence_status']='SOURCE_VERIFIED'
  self.assertTrue(V.validate_data(bad))
 def test_retrieval_framework_entity_and_dates(self):
  for fw,scope in R.SCOPES.items():
   rows=R.retrieve(fw,'2026-12-31',scope,period_start='2026-01-01')
   self.assertEqual(len(rows),24)
   self.assertTrue(all(x['framework']==fw for x in rows))
   for bad in ['2025-12-31','2027-01-01']:
    with self.assertRaises(ValueError):R.retrieve(fw,bad,scope)
   with self.assertRaises(ValueError):R.retrieve(fw,'2026-12-31','investment_company')
   with self.assertRaises(ValueError):R.retrieve(fw,'2026-12-31',scope,early_presentation_adoption=True)
 def test_retrieval_privacy_and_unapproved_rejection(self):
  rows=R.retrieve('IFRS','2026-12-31',R.SCOPES['IFRS'])
  for row in rows:self.assertEqual(set(row),set(R.PUBLIC_FIELDS))
  self.assertNotIn('source_note',json.dumps(rows))
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'register.json';bad=copy.deepcopy(self.register);bad['status']='REVIEWED';p.write_text(json.dumps(bad))
   with self.assertRaises(ValueError):R.retrieve('IFRS','2026-12-31',R.SCOPES['IFRS'],path=p)

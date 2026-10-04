"""Knowledge integrity/privacy tests plus independent numerical reference cases."""
import copy,importlib.util,json,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('insurance_k_retrieval',HERE/'retrieval.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
s=importlib.util.spec_from_file_location('insurance_k_validator',HERE/'validate_supplement.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class InsuranceKnowledgeTests(unittest.TestCase):
 def test_population(self):
  d=r.load_register();self.assertEqual(168,len(d['claims']));self.assertEqual([],v.validate_data(d))
 def test_unapproved_retrieval(self):
  d=r.load_register()
  if d['status']=='REVIEWED':
   with self.assertRaises(ValueError):r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],insurance_model='IFRS17_GMM')
  else:self.assertTrue(r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],insurance_model='IFRS17_GMM'))
 def test_scope(self):
  for scope in ['aasb_public_sector','aasb_tier2','aasb_not_for_profit']:
   with self.assertRaises(ValueError):r.retrieve('AASB','2026-12-31',scope,insurance_model='AASB17_PAA')
 def test_period(self):
  for period in ['2027-12-31','2025-12-31','bad']:
   with self.assertRaises(ValueError):r.retrieve('IFRS',period,r.SCOPES['IFRS'],insurance_model='IFRS17_GMM')
 def test_model_cross_framework(self):
  with self.assertRaises(ValueError):r.retrieve('US_GAAP','2026-12-31',r.SCOPES['US_GAAP'],insurance_model='IFRS17_PAA')
 def test_early_adoption(self):
  with self.assertRaises(ValueError):r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],insurance_model='IFRS17_GMM',early_presentation_adoption=True)
 def test_no_canonical_claim(self):
  d=copy.deepcopy(r.load_register());d['claims'][0]['topic_id']='TOPIC-INSURANCE';self.assertTrue(v.validate_data(d))
 def test_missing_sources(self):
  d=copy.deepcopy(r.load_register());d['claims'][0]['sources']=[];self.assertTrue(v.validate_data(d))
 def test_false_direct(self):
  d=copy.deepcopy(r.load_register());d['claims'][0]['evidence_status']='SOURCE_VERIFIED';self.assertTrue(v.validate_data(d))
 def test_no_self_approval(self):
  d=copy.deepcopy(r.load_register());d['status']='APPROVED';d['claims'][0]['approval_review']={'reviewer':d['author'],'result':'PASS'};self.assertTrue(v.validate_data(d))
 def test_stale_hash(self):
  d=copy.deepcopy(r.load_register());d['status']='APPROVED';d['claims'][0]['proposition']+=' changed';self.assertTrue(v.validate_data(d))
 def test_duplicate(self):
  d=copy.deepcopy(r.load_register());d['claims'][1]['claim_id']=d['claims'][0]['claim_id'];self.assertTrue(v.validate_data(d))
 def test_source_privacy(self):
  for c in r.load_register()['claims']:
   pub=json.dumps({k:c[k] for k in r.PUBLIC_FIELDS}).lower()
   for field in ['source_note','training_data_checked','audit_required','source:','approval_track']:self.assertNotIn(field,pub)
 def test_public_uncertainty(self):
  for c in r.load_register()['claims']:self.assertTrue(c['public_limitations'])
 def test_initial_gmm(self):
  # 1000 premium at inception; future claim PV800, qualified RA50.
  premium,pv,ra=1000,800,50;fcf=pv+ra-premium;csm=max(-fcf,0)
  self.assertEqual(150,csm);self.assertEqual(1000,pv+ra+csm)
 def test_initial_onerous(self):
  premium,pv,ra=1000,1050,50;fcf=pv+ra-premium
  self.assertEqual(100,max(fcf,0));self.assertEqual(0,max(-fcf,0))
 def test_csm_release(self):
  initial,rate,units,remaining=150,.04,25,75;before=initial*(1+rate)
  self.assertEqual(39,before*units/(units+remaining));self.assertEqual(117,before-before*units/(units+remaining))
 def test_paa_acquisition_bridge(self):
  # 1200 premiums less120 acquisition paid plus30 amortisation less300 service.
  self.assertEqual(810,1200-120+30-300)
 def test_claims_bridge(self):
  self.assertEqual(260,200+150+10-100)
 def test_us_deficiency(self):
  # UPR600; expected claims650 plus maintenance50; DAC80 => deficiency180.
  deficit=650+50+80-600;writeoff=min(80,deficit);additional=deficit-writeoff
  self.assertEqual((180,80,100),(deficit,writeoff,additional))
 def test_held_separation(self):
  # Gross issued liability500 and held recoverable150 remain separate populations.
  statement={'issued_liability':500,'reinsurance_asset':150};self.assertEqual(500,statement['issued_liability']);self.assertNotEqual(350,statement['issued_liability'])
if __name__=='__main__':unittest.main()

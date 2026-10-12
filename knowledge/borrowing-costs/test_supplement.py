import copy,importlib.util,json,unittest
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('borrowing_supplement_validator',P/'validate_supplement.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
r=v._local
class KnowledgeTests(unittest.TestCase):
 def test_structural_inventory(self):
  d=r.load_register();self.assertEqual([],v.validate_data(d));self.assertEqual(92,len(d['claims']))
 def test_unapproved_blocks(self):
  d=r.load_register()
  if d['status']!='APPROVED':
   with self.assertRaises(ValueError):r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],period_start='2026-01-01')
 def test_canonical_population_not_fabricated(self):
  d=r.load_register();self.assertNotIn('topic_id',d);self.assertNotIn('capability_mappings',d)
 def test_mutated_approved_claim_blocks(self):
  d=r.load_register();d['status']='APPROVED';d['claims'][0]['proposition']+=' altered';self.assertTrue(v.validate_data(d))
 def test_framework_scope_blocks(self):
  with self.assertRaises(ValueError):r.retrieve('UK_GAAP','2026-12-31','frs105',period_start='2026-01-01')
 def test_historical_period_blocks(self):
  with self.assertRaises(ValueError):r.retrieve('IFRS','2025-12-31',r.SCOPES['IFRS'],period_start='2025-01-01')
 def test_duplicate_blocks(self):
  d=r.load_register();d['claims'].append(copy.deepcopy(d['claims'][0]));self.assertTrue(v.validate_data(d))
 def test_source_fabrication_blocks(self):
  d=r.load_register();c=next(c for c in d['claims'] if c['evidence_status']=='MODEL_DERIVED_AUDIT_REQUIRED');c['evidence_status']='SOURCE_VERIFIED';self.assertTrue(v.validate_data(d))
if __name__=='__main__':unittest.main()

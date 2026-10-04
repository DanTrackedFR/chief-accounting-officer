import importlib.util,json,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('hedge_retrieval',HERE/'retrieval.py');retr=importlib.util.module_from_spec(spec);spec.loader.exec_module(retr)
spec=importlib.util.spec_from_file_location('hedge_validator',HERE/'validate_supplement.py');val=importlib.util.module_from_spec(spec);spec.loader.exec_module(val)
class KnowledgeTests(unittest.TestCase):
 def test_atomic_population(self):
  d=retr.load_register();self.assertEqual(100,len(d['claims']));self.assertFalse(val.validate_data(d))
  for fw in retr.FRAMEWORKS:self.assertEqual(25,len([c for c in d['claims'] if c['framework']==fw]))
 def test_model_explicit(self):
  for fw in retr.FRAMEWORKS:
   with self.assertRaises(ValueError):retr.retrieve(fw,'2026-06-30',retr.SCOPES[fw])
 def test_public_projection(self):
  for c in retr.load_register()['claims']:
   txt=json.dumps({k:c[k] for k in retr.PUBLIC_FIELDS}).lower()
   self.assertNotIn('source_note',txt);self.assertNotIn('audit_required',txt);self.assertNotIn('training_data_checked',txt)
 def test_framework_differences(self):
  cs={(c['framework'],c['decision']):c['proposition'] for c in retr.load_register()['claims']}
  self.assertIn('do not apply the IFRS lower-of',cs['US_GAAP','cash_flow_measurement'])
  self.assertIn('do not recycle',cs['UK_GAAP','net_investment_disposal'])
  self.assertIn('prospectively',cs['IFRS','discontinuation'])
if __name__=='__main__':unittest.main()

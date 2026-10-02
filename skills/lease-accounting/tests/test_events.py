import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from events import assess_modification,reassessment,EventReviewRequired

class EventTests(unittest.TestCase):
 def test_separate_lease(self):
  e={"adds_right_of_use":True,"consideration_commensurate":True,"scope_decrease":False,"remaining_payments":["10"],"revised_periodic_rate":"0.05"}
  self.assertEqual(assess_modification(e)["treatment"],"separate_lease")
 def test_non_scope_modification_remeasures(self):
  e={"adds_right_of_use":False,"consideration_commensurate":False,"scope_decrease":False,"remaining_payments":["100","100"],"revised_periodic_rate":"0.05"}
  self.assertEqual(str(assess_modification(e)["remeasured_liability"]),"185.94")
 def test_scope_decrease_blocks_generic_math(self):
  e={"adds_right_of_use":False,"consideration_commensurate":False,"scope_decrease":True,"remaining_payments":["100"],"revised_periodic_rate":"0.05"}
  with self.assertRaises(EventReviewRequired): assess_modification(e)
 def test_reassessment_requires_rate(self):
  with self.assertRaises(EventReviewRequired): reassessment({"kind":"term_or_option","remaining_payments":["100"]})
if __name__=="__main__": unittest.main()

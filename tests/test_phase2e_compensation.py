import unittest
class CompensationChallenge(unittest.TestCase):
 def test_funded_deficit_is_not_contribution_expense(self):
  obligation=1000+60+40-50+30;assets=800+32+70-50+18
  self.assertEqual(obligation-assets,210)
  self.assertEqual(200+68+12-70,210)
  self.assertNotEqual(70,68)
 def test_equity_and_cash_award_bridges(self):
  cumulative=[100*90*12/3,100*80*12*2/3,100*82*12]
  self.assertEqual(cumulative,[36000,64000,98400])
  self.assertEqual(sum([cumulative[0],cumulative[1]-cumulative[0],cumulative[2]-cumulative[1]]),98400)
  self.assertEqual(100*100*12-100*100*8/2,80000)
 def test_service_and_termination_are_distinct(self):
  termination=12*15000;future_service=12*5000
  self.assertEqual(termination,180000)
  self.assertEqual(future_service,60000)
  self.assertEqual(20*4*250*1.1,22000)
  self.assertNotEqual(termination,termination+future_service)

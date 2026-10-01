import math
import unittest
class FinanceGroupChallenge(unittest.TestCase):
 def test_effective_yield_redemption_and_cost_bridge(self):
  y=(50+math.sqrt(2500+4*970*1050))/1940
  close=970*y-50
  self.assertAlmostEqual(close*y-50,1000,places=9)
  self.assertAlmostEqual(970*(y-1)+close*(y-1),130,places=9)
 def test_equity_method_distinct_adjustments(self):
  result=300+100*.30-20*.30-24/4-6
  self.assertEqual(result,312)
  self.assertNotEqual(result,300+100*.30+20*.30)
 def test_inventory_and_asset_profit_unwind(self):
  self.assertEqual((150-100)*.4,20)
  separate=150-150/5;group=100-100/5
  self.assertEqual(separate-group,50-(150/5-100/5))
 def test_control_loss_and_retained_control_differ(self):
  self.assertEqual(450+120+100-500,170)
  self.assertEqual(85-150*10/20,10)

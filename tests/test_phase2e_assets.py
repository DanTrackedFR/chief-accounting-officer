import unittest
class AssetBoundaries(unittest.TestCase):
 def test_cost_eligibility_and_readiness(self):
  self.assertEqual(500000+20000+30000,550000)
  self.assertEqual(200000+120000+80000-300000,100000)
  self.assertEqual(200000+120000+60000-300000,80000)
 def test_remaining_life_and_legal_cap(self):
  carrying=600000-2*90000
  charge=(carrying-60000)/7
  self.assertAlmostEqual(charge,51428.57142857)
  self.assertAlmostEqual(400000-(carrying-charge),31428.57142857)
  self.assertEqual(600000/6/2,50000)
  self.assertEqual(600000/3/2,100000)
 def test_recoverability_is_not_fair_value_alone(self):
  def us_loss(carrying,undiscounted,fair):return max(0,carrying-fair) if undiscounted<carrying else 0
  self.assertEqual(us_loss(12000000,11500000,10800000),1200000)
  self.assertEqual(us_loss(12000000,12100000,10800000),0)
  self.assertEqual(12000000-max(10800000,11000000),1000000)
 def test_development_and_hosted_costs(self):
  self.assertEqual(100000+250000+50000+100000,500000)
  self.assertEqual((120000-30000)/36,2500)

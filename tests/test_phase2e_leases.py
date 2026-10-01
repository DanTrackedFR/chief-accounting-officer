import unittest
from decimal import Decimal,ROUND_HALF_UP
class LeaseSchedules(unittest.TestCase):
 def test_timing_and_rate_sensitivity(self):
  pv=lambda cash,n,r:sum(cash/(1+r)**i for i in range(1,n+1))
  x=pv(100,5,.05);self.assertAlmostEqual(x,432.947667063,places=8)
  self.assertAlmostEqual(x*1.05-100,354.595050416,places=8)
  self.assertGreater(pv(100,3,.05),pv(100,3,.06))
  self.assertAlmostEqual(pv(100,5,.05)*1.05,454.595050416,places=8)
 def test_rounded_fixed_leaseback_clears(self):
  q=lambda x:x.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
  b=Decimal('400000');cash=Decimal('92389.92');interest=Decimal(0)
  for i in range(5):
   a=q(b*Decimal('.05'));interest+=a
   pay=b+a if i==4 else cash;b=b+a-pay
  self.assertEqual(b,0);self.assertEqual(pay,Decimal('92389.91'))
  self.assertEqual(interest,Decimal('61949.59'))
 def test_variable_policy_and_framework_gains(self):
  cash=400000/(1/1.05+1/1.05**2)
  b=400000*1.05-cash
  self.assertAlmostEqual(b*1.05-cash,0)
  self.assertAlmostEqual(cash,215121.951219512)
  self.assertEqual(600000*.4,240000)
  self.assertEqual((1000000-600000)*.6,240000)
  self.assertEqual(1000000-600000,400000)

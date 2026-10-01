import unittest
from datetime import date

class RegulatoryBridgeCalculations(unittest.TestCase):
    def test_same_perimeter_capital_and_conditional_threshold(self):
        eligible=20-3-1
        self.assertAlmostEqual(eligible/160,.1)
        self.assertAlmostEqual(160*.11-eligible,1.6)
        self.assertEqual(30/(24+8),.9375)
    def test_fund_deficit_not_hidden_by_aggregate(self):
        funds=[12-10,7-9]
        self.assertEqual(sum(funds),0)
        self.assertTrue(any(x<0 for x in funds))
        self.assertEqual(210-40-max(125,180),-10)
    def test_machine_scale_and_allowance_release(self):
        raw=1200000
        self.assertEqual(raw/1000*1000,raw)
        self.assertNotEqual(raw*1000,raw)
        self.assertEqual(12000000*(.05-.02),360000)

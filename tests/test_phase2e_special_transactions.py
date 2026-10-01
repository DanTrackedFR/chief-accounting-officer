import unittest

class SpecialTransactionCalculations(unittest.TestCase):
    def test_compound_costs_and_warrant(self):
        self.assertAlmostEqual(1000-920-20*.08,78.4)
        self.assertAlmostEqual(920-20*.92,901.6)
        self.assertAlmostEqual(901.6+78.4,1000-20)
        self.assertEqual(31-25,6)
    def test_carveout_funding_not_face_debt(self):
        self.assertEqual(500-310-100*.3-60*40/200,148)
        self.assertEqual(245+120-300-(12+3+2),48)
        self.assertNotEqual(250+120,245+120)
    def test_hyperinflation_item_classes(self):
        self.assertEqual(100*250/200,125)
        self.assertAlmostEqual(50*250/225,55.5555555556)
        cash=40
        self.assertEqual(cash,40)
        self.assertNotEqual(cash*250/200,cash)

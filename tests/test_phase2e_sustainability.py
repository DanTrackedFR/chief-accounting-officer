import unittest

class SustainabilityCalculations(unittest.TestCase):
    def test_energy_mass_equivalent_factor_units(self):
        kwh=100000
        tonnes_from_kwh=kwh*.4/1000
        tonnes_from_mwh=(kwh/1000)*.4
        self.assertEqual(tonnes_from_kwh,40)
        self.assertEqual(tonnes_from_kwh,tonnes_from_mwh)
        self.assertNotEqual(kwh*.4,tonnes_from_kwh)
    def test_missing_site_not_cleared_by_subtotal_tie(self):
        total=1200+900+700
        self.assertEqual(total,2800)
        self.assertEqual((total-2100)/total,.25)
        self.assertEqual(total*.4,1120)
    def test_life_and_assurance_chain(self):
        self.assertAlmostEqual(8/4-8/15,1.4666666666666668)
        self.assertAlmostEqual(12000/1000*.35,4.2)
        self.assertEqual((100000-20000)*.4/1000,32)

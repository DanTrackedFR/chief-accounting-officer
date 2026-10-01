import unittest

class JudgmentCalculations(unittest.TestCase):
    def test_prospective_life_revision(self):
        carrying=1200000-300000
        self.assertEqual(carrying/3-carrying/5,120000)
        self.assertEqual(carrying/5,180000)
    def test_allowance_population_and_overlay(self):
        self.assertEqual(4000000*.01+1000000*.05+500000*.2+25000-170000,45000)
        self.assertEqual(5700000-5500000,200000)
    def test_percent_and_percentage_points(self):
        self.assertEqual(100000/20000000,.005)
        self.assertAlmostEqual(.2/100,.002)
        self.assertAlmostEqual(30.5-30,.5)
        self.assertAlmostEqual(30-29.8,.2)
        self.assertEqual(8*20000,160000)

import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lease_math import present_value, initial_measurement, liability_schedule, level_payment

class LeaseMathTests(unittest.TestCase):
    def test_five_year_lease(self):
        payment = level_payment("400000", "0.05", 5)
        self.assertEqual(str(payment), "92389.92")
        self.assertEqual(present_value([(i, payment) for i in range(1, 6)], "0.05"), 400000)
        rows = liability_schedule("400000", [payment] * 5, "0.05")
        self.assertEqual(rows[-1]["closing"], 0)

    def test_rou_bridge(self):
        result = initial_measurement([(1, "105"), (2, "105")], "0.05",
                                     prepayments="10", direct_costs="5", incentives="3", restoration="8")
        self.assertEqual(result["rou_asset"], result["lease_liability"] + 20)

    def test_no_double_count_commencement(self):
        with self.assertRaises(ValueError):
            initial_measurement([(0, "100")], "0.05")

    def test_reject_unreconciled_schedule(self):
        with self.assertRaises(ValueError):
            liability_schedule("400000", ["100000"] * 5, "0.05")

    def test_zero_rate(self):
        self.assertEqual(level_payment("300", "0", 3), 100)
        self.assertEqual(present_value([(1, "100"), (2, "100"), (3, "100")], "0"), 300)

if __name__ == "__main__":
    unittest.main()

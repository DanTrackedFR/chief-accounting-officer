"""Reperformance on the documented hypothetical inputs, not a live ERP claim."""
import unittest
class CloseCases(unittest.TestCase):
    def test_parallel_critical_paths(self):
        self.assertEqual(max(2+1+1,3+1)+1+1,6)
        self.assertEqual(max(1+1+1,3+1)+1+1,6)
        self.assertEqual(max(2+1+1,4+1)+1+1,7)
    def test_journal_duplicate_accrual(self):
        self.assertEqual(75000-50000,25000)
        self.assertEqual(50000+25000,75000)
    def test_feed_rejects(self):
        self.assertEqual(996+4,1000)
        self.assertEqual(99600+400,100000)
        self.assertEqual(99600*2-99600,99600)
    def test_reconciliation_and_gross_items(self):
        self.assertEqual(100000+40000-15000,125000)
        self.assertEqual(130000-125000,5000)
        self.assertEqual(40000-10000,30000)
        self.assertEqual(40000+10000,50000)
        self.assertEqual(30000/2000000,.015)
        self.assertEqual(.02*10000000,200000)
    def test_cutoff_journal_balances_without_determining_control(self):
        self.assertEqual(25000-25000,0)
        self.assertEqual(abs(25000)+abs(-25000),50000)
    def test_prepaid_and_estimate_trueup(self):
        self.assertEqual(120000/12,10000)
        self.assertEqual(120000-6*10000,60000)
        self.assertEqual(3000*8,24000)
        self.assertEqual(75*8,600)
        self.assertEqual(24000+600,24600)
    def test_flux_correction_bridge(self):
        self.assertEqual(1350000-1000000,350000)
        self.assertEqual(350000-200000-100000-20000,30000)
        self.assertEqual(200000-15000,185000)
        self.assertEqual(350000-185000-100000-20000,45000)
        self.assertEqual((1350000-15000)-1000000-185000-100000-20000,30000)
    def test_error_statement_and_opening_bridge(self):
        self.assertEqual(800000+80000,880000)
        self.assertEqual(1000000-880000,120000)
        self.assertEqual(50000-20000,30000)
        self.assertEqual(120000-30000,90000)
        self.assertEqual(20000-80000,-60000)
        self.assertEqual(600000-2000,598000)
        self.assertEqual(100000-80000,20000)
        self.assertEqual((160000-60000)+(140000+60000),300000)
        self.assertEqual(30000-30000,0)
    def test_signoff_counts(self):
        self.assertEqual(190/200,.95)
        self.assertEqual(200-190,10)
if __name__=='__main__':unittest.main()

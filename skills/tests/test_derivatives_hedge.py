import unittest,copy
from hedge_cases import *
from core_accounting import ReviewRequired

class HedgeAuthoredTests(unittest.TestCase):
    def run_case(self,c):return workflow().assess(c,[])
    def bad(self,c,field,value,nested='valuation'):
        r={'valuation':c['valuations'][0],'contract':c['contracts'][0],'relationship':c['relationships'][0] if c['relationships'] else {}}[nested];r[field]=value;sources(c)
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_realistic_scenario_workpapers(self):
        for name in ('late-documentation','swap-liability-settlement','discontinue-expected','forecast-sale'):
            for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):self.run_case(special_case(name,fw))
        for name in ('rebalancing','cumulative-reversal'):
            for fw in ('IFRS','AASB'):self.run_case(special_case(name,fw))
    def test_standalone_frameworks(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            r=self.run_case(case(fw));self.assertEqual(r['calculations']['derivatives'][0]['closing'],dec('100'))
    def test_actual_net_investment_owners(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):self.run_case(net_investment_case(fw))
    def test_actual_debt_owners(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            for route in ('fair_value','cash_flow'):self.run_case(debt_case(fw,route))
    def test_cashflow_frameworks(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            r=self.run_case(case(fw,'cash_flow'));self.assertEqual(r['calculations']['hedge_reserves'][0]['closing'],dec('100' if fw=='US_GAAP' else '90'))
    def test_basis_frameworks(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            r=self.run_case(case(fw,'cash_flow','occurred'));self.assertEqual(r['calculations']['basis_adjustments'][0]['amount'],dec('-90'))
    def test_cancelled_forecasts(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            r=self.run_case(case(fw,'cash_flow','no_longer_expected'));self.assertEqual(r['calculations']['hedge_reserves'][0]['closing'],dec('0'))
    def test_probability_lost_still_expected_retains(self):
        c=case('IFRS','cash_flow');c['relationships'][0].update(status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='probability_lost',forecast_probability='expected',probability_before_cessation='highly_probable',measurement_through_qualification_date=c['reporting_period']);sources(c)
        self.assertEqual(self.run_case(c)['calculations']['hedge_reserves'][0]['closing'],dec('90'))
    def test_pending_discontinued_retains_reserve(self):
        c=case('IFRS','cash_flow');c['relationships'][0].update(status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='instrument terminated');sources(c)
        self.assertEqual(self.run_case(c)['calculations']['hedge_reserves'][0]['closing'],dec('90'))
    def test_valuation_wrong_currency(self):self.bad(case(),'currency','USD')
    def test_valuation_stale(self):self.bad(case(),'measurement_date','2025-12-31')
    def test_wrong_notional(self):self.bad(case(),'notional','1001')
    def test_wrong_entity(self):self.bad(case(),'entity','Other')
    def test_sign_bridge(self):self.bad(case(),'change','-100')
    def test_duplicate_valuation(self):
        c=case();c['valuations'].append(copy.deepcopy(c['valuations'][0]));
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_document_tamper(self):
        c=case();c['contracts'][0]['notional']='2000'
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_late_documentation(self):
        c=case('IFRS','cash_flow');c['relationships'][0]['documentation_date']='2026-02-01';c['gl']=case()['gl'];sources(c)
        self.assertEqual(self.run_case(c)['calculations']['derivatives'][0]['route'],'standalone')
    def test_ratio_manipulated(self):self.bad(case('IFRS','cash_flow'),'ratio','2','relationship')
    def test_credit_dominance(self):self.bad(case('IFRS','cash_flow'),'credit_dominates',True,'relationship')
    def test_us_wrong_effectiveness(self):self.bad(case('US_GAAP','cash_flow'),'effectiveness_method','economic_relationship','relationship')
    def test_ifrs_wrong_effectiveness(self):self.bad(case('IFRS','cash_flow'),'effectiveness_method','documented_high_effectiveness','relationship')
    def test_intragroup(self):self.bad(case('IFRS','cash_flow'),'external_group_exposure',False,'relationship')
    def test_options_block(self):self.bad(case('IFRS','cash_flow'),'kind','option','contract')
    def test_excluded_component(self):self.bad(case('IFRS','cash_flow'),'excluded_components','forward_points','relationship')
    def test_rebalancing_preserves_history(self):
        c=case('IFRS','cash_flow');c['relationships'][0].update(status='rebalanced',rebalancing_memo='Independent new actual quantities',rebalancing_date=c['reporting_period'],historical_effective='0',new_ratio='2',new_instrument_quantity='2000',new_item_quantity='1000');sources(c)
        self.run_case(c);self.bad(c,'historical_effective','90','relationship')
    def test_non_derivative_contract(self):
        c=case();c['contracts'][0]['small_initial_investment']=False;c['contracts'][0]['initial_net_investment']='1000';c['valuations']=[];c['gl']=[];sources(c)
        self.assertEqual(self.run_case(c)['calculations']['derivatives'][0]['route'],'not_derivative')
    def test_scope_exception_requires_rights(self):
        c=case();c['contracts'][0].update(exception_applies=True,exception_route='own_use');sources(c)
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_gl_fails(self):
        c=case();c['gl'][0]['closing']='99'
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_disclosure_fails(self):
        c=case();c['disclosure_review']['contract_ids']=[]
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_us_amendment_block(self):
        c=case('US_GAAP');c['policy_elections']['asu_2025_09_early_adopted']=True
        with self.assertRaises(ReviewRequired):self.run_case(c)
    def test_ias39_block(self):
        c=case();c['model']='IAS39'
        with self.assertRaises(ReviewRequired):self.run_case(c)

if __name__=='__main__':unittest.main()

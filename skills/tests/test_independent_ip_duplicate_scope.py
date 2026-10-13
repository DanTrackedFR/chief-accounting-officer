"""Independent additional US transfer and repeated property owner challenges."""
import unittest
from copy import deepcopy
from investment_property_cases import case, ready, capture
from production import assess_case
from orchestration import CAO
from orchestration.planning import Issue
from orchestration.tests.test_independent_qa import FixedPlanner
from skills.tests.test_independent_investment_property_integration import request, source


class AdditionalIndependentScopeQA(unittest.TestCase):
    def test_us_zero_transfer_out_is_not_an_investment_property_method(self):
        c=case('US_GAAP','cost','transfer_out_cost')
        p=c['properties'][0]
        for key in ('opening_carrying','gross_cost','closing_carrying'):p[key]='0'
        p['opening_history']['carrying']='0'
        c['controls']['population_amount']='0'
        for key in ('land_cost','depreciation','opening_carrying','closing_before_impairment'):c['cost_owner'][key]='0'
        for key in ('opening_carrying','closing_carrying'):c['impairment_owner'][key]='0'
        c['events'][0]['ppe_carrying']='0'
        for gl in c['gl']:gl.update(opening='0',closing='0',statement='0')
        for key in c['disclosure_review']['amounts']:c['disclosure_review']['amounts'][key]='0'
        capture(c);r=assess_case('investment-property',ready(c=c))
        self.assertEqual('blocked',r['status'],r.get('conclusion'))
        self.assertEqual([],r['journal_entry_implications'])

    def test_same_property_event_twice_in_native_case_cannot_release_twice(self):
        c=source()
        planner=FixedPlanner([
            Issue('ip-first','rental_investment','investment-property','Actual property register',['rental_investment']),
            Issue('ip-second','rental_investment','investment-property','Repeated same property event',['rental_investment']),
        ])
        r=CAO(planner=planner).run(request(c))
        self.assertNotEqual('complete',r.outcome,r.conclusions)
        self.assertNotEqual('CLOSED',r.status)
        self.assertIn('Duplicate workplan node',str(r.open_questions))
        self.assertFalse(r.skills_invoked)

    def test_distinct_case_labels_cannot_disguise_duplicate_same_scope_owner(self):
        first=source();second=deepcopy(first)
        second['case_id']='independent-second-property-case'
        second=ready(c=second)
        req=request(first);req['facts']['rental_investment']=[first,second]
        r=CAO().run(req)
        self.assertNotEqual('complete',r.outcome)
        self.assertIn('Ambiguous exact issue source',str(r.open_questions))
        self.assertFalse(r.skills_invoked)

    def test_transfer_in_cannot_ignore_actual_pretransfer_ppe_depreciation_source(self):
        c=case('IFRS','cost','transfer_in_cost')
        # Actual synthetic documentary PPE owner record: 600k prior carrying,
        # 100k land + 500k building/25 years = 20k annual charge already owned
        # by PPE, leaving 580k current carrying before the cutoff transfer.
        # It is deliberately retained inside the original property source
        # population, not merely asserted in an unrelated memo or sign-off.
        owner=case('IFRS','cost','hold')['cost_owner']
        c['properties'][0]['pre_transfer_depreciation_source']=deepcopy(owner)
        # Preserve the original R4 attack after the positive fixture gains
        # current owner proof: remove it, retain documentary actual20kcharge,
        # and coherently assert the obsolete600k transfer again.
        c['cost_owner']=None;c['impairment_owner']=None
        c['properties'][0]['closing_carrying']='600000'
        c['events'][0]['ppe_carrying']='600000'
        for gl in c['gl']:
            if gl['id']=='Investment property':gl.update(closing='600000',statement='600000')
            if gl['id']=='Property plant and equipment':gl['opening']='600000'
        c['ownership_register']=[x for x in c['ownership_register'] if x['movement']=='transfer']
        c['ownership_inventory']=[x['id'] for x in c['ownership_register']]
        c['disclosure_review']['amounts'].update(transfers='600000',closing_carrying='600000',pre_transfer_depreciation_owned_elsewhere='0',pre_transfer_impairment_owned_elsewhere='0')
        capture(c)
        r=assess_case('investment-property',ready(c=c))
        self.assertEqual('blocked',r['status'],r.get('conclusion'))
        self.assertEqual([],r['journal_entry_implications'])

    def test_cost_initial_missing_reporting_date_fair_value_note_blocks(self):
        for fw in ('IFRS','AASB'):
            for route in ('initial','hold','transfer_in_cost'):
                with self.subTest(framework=fw,route=route):
                    c=case(fw,'cost',route);c['valuation']=None;capture(c)
                    r=assess_case('investment-property',ready(c=c))
                    self.assertEqual('blocked',r['status'],r.get('conclusion'))
                    self.assertEqual([],r['journal_entry_implications'])

    def test_cost_initial_stale_or_wrong_framework_fair_value_note_blocks(self):
        for fw in ('IFRS','AASB'):
            for field,value in [('valuation_date','2025-12-31'),('valuation_standard','ASC820'),('reliable',False)]:
                with self.subTest(framework=fw,field=field):
                    c=case(fw,'cost','initial');c['valuation'][field]=value;capture(c)
                    r=assess_case('investment-property',ready(c=c))
                    self.assertEqual('blocked',r['status'],r.get('conclusion'))
                    self.assertEqual([],r['journal_entry_implications'])

    def test_cost_initial_fair_value_note_amount_is_output_not_recognized(self):
        for fw in ('IFRS','AASB'):
            for route in ('initial','hold','transfer_in_cost'):
                with self.subTest(framework=fw,route=route):
                    r=assess_case('investment-property',ready(fw,'cost',route))
                    self.assertEqual('complete',r['status'],r.get('conclusion'))
                    self.assertEqual('650000',str(r['calculations'].get('fair_value_disclosure')))
                    self.assertEqual('0',str(r['calculations']['fair_value_movement']))
                    self.assertEqual(0 if route=='hold' else 1,len(r['journal_entry_implications']))

    def test_current_ppe_transfer_charge_reperformed_not_just_recertified(self):
        c=case('IFRS','cost','transfer_in_cost')
        c['cost_owner'].update(depreciation='19000',closing_before_impairment='581000')
        c['impairment_owner'].update(opening_carrying='581000',closing_carrying='581000')
        c['properties'][0]['closing_carrying']='581000';c['events'][0]['ppe_carrying']='581000'
        for gl in c['gl']:
            if gl['id']=='Investment property':gl.update(closing='581000',statement='581000')
            if gl['id']=='Property plant and equipment':gl['opening']='581000'
        c['disclosure_review']['amounts'].update(transfers='581000',closing_carrying='581000',pre_transfer_depreciation_owned_elsewhere='19000')
        capture(c);r=assess_case('investment-property',ready(c=c))
        self.assertEqual('blocked',r['status']);self.assertEqual([],r['journal_entry_implications'])

    def test_current_ppe_impairment_pretransfer_not_double_charged(self):
        c=case('IFRS','cost','transfer_in_cost')
        c['impairment_owner'].update(indicators_present=True,loss='10000',closing_carrying='570000')
        c['properties'][0]['closing_carrying']='570000';c['events'][0]['ppe_carrying']='570000'
        for gl in c['gl']:
            if gl['id']=='Investment property':gl.update(closing='570000',statement='570000')
            if gl['id']=='Property plant and equipment':gl['opening']='570000'
        c['disclosure_review']['amounts'].update(transfers='570000',closing_carrying='570000',pre_transfer_impairment_owned_elsewhere='10000')
        capture(c);r=assess_case('investment-property',ready(c=c))
        self.assertEqual('complete',r['status'],r.get('conclusion'));calc=r['calculations']
        self.assertEqual('20000.00',str(calc['pre_transfer_depreciation_owned_elsewhere']))
        self.assertEqual('10000',str(calc['pre_transfer_impairment_owned_elsewhere']))
        self.assertEqual('0',str(calc['opening_carrying']))
        self.assertEqual('0',str(calc['depreciation_owned_elsewhere']))
        self.assertEqual('0',str(calc['impairment_owned_elsewhere']))
        self.assertEqual('570000.00',str(calc['transfers']))
        self.assertEqual(1,len(r['journal_entry_implications']))
        self.assertEqual('570000.00',str(r['journal_entry_implications'][0][0]['amount']))

    def test_current_ppe_source_cannot_be_silently_replaced_after_capture(self):
        c=case('IFRS','cost','transfer_in_cost')
        c['cost_owner']['basis_memo']='Changed original underlying PPE source'
        r=assess_case('investment-property',ready(c=c))
        self.assertEqual('blocked',r['status']);self.assertEqual([],r['journal_entry_implications'])

    def fees_only_initial(self):
        c=case('US_GAAP','cost','initial')
        c['properties'][0].update(gross_cost='10000',closing_carrying='10000')
        c['controls']['population_amount']='10000'
        c['events'][0]['purchase_cost']='10000'
        c['events'][0]['cost_items'][0]['amount']='0'
        c['events'][0]['cost_items'][1]['amount']='10000'
        for gl in c['gl']:
            if gl['id']=='Property plant and equipment':gl.update(closing='10000',statement='10000')
            if gl['id']=='Cash':gl.update(closing='990000',statement='990000')
        c['disclosure_review']['amounts'].update(additions='10000',closing_carrying='10000')
        return c

    def test_documented_gift_cannot_be_recognized_as_paid_fees_only_purchase(self):
        c=self.fees_only_initial()
        c['properties'][0].update(gifted=True,acquisition_nature='nonexchange_gift',title_document='Synthetic deed of gift, unrelated donor, no purchase consideration',rights_memo='Actual original synthetic gift deed inspected, title transferred without exchange')
        c['events'][0].update(acquisition_nature='nonexchange_gift',event_memo='Actual gift received; only legal conveyancing fees paid')
        c['events'][0]['cost_items'][0]['eligibility_memo']='Original deed of gift; zero donor consideration, not cash purchase'
        c['events'][0]['cost_items'][1]['eligibility_memo']='Actual cash legal fees paid; no consideration to donor'
        capture(c);r=assess_case('investment-property',ready(c=c))
        self.assertEqual('blocked',r['status'],r.get('conclusion'));self.assertEqual([],r['journal_entry_implications'])

    def test_zero_consideration_cannot_be_laundered_by_positive_legal_fees(self):
        c=self.fees_only_initial()
        c['properties'][0]['gifted']=False;c['events'][0]['acquisition_nature']='cash_purchase'
        capture(c);r=assess_case('investment-property',ready(c=c))
        self.assertEqual('blocked',r['status'],r.get('conclusion'));self.assertEqual([],r['journal_entry_implications'])

    def test_initial_missing_or_wrong_acquisition_qualification_blocks(self):
        for field,value in [('acquisition_nature',None),('acquisition_nature','nonexchange_gift'),('acquisition_nature','asset_exchange'),('gifted',None),('gifted',True)]:
            with self.subTest(field=field,value=value):
                c=case('US_GAAP','cost','initial')
                target=c['properties'][0] if field=='gifted' else c['events'][0]
                if value is None:target.pop(field,None)
                else:target[field]=value
                capture(c);r=assess_case('investment-property',ready(c=c))
                self.assertEqual('blocked',r['status'],r.get('conclusion'));self.assertEqual([],r['journal_entry_implications'])


if __name__=='__main__':unittest.main()

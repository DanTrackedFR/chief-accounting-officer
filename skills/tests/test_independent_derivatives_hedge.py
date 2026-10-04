"""Independent fresh counterexamples; source mutations are intentionally requalified."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch
from decimal import Decimal as D
from hedge_cases import case,sources,workflow,ready,PACKAGE
from core_accounting import ReviewRequired
from production import assess_case,to_public
from interfaces.public_output import ROUTES


def independent(fw='IFRS',route='standalone',outcome='pending'):
    c=case(fw,route,outcome);c['case_id']='Independent 29 '+fw+' '+route+' '+outcome
    # Different notional and valuation magnitude from authored examples.
    for r in c['contracts']:r['notional']='1730'
    for v in c['valuations']:
        v['notional']='1730'
        for key in ('opening','change','settlement','closing'):v[key]=str(D(v[key])*D('1.73'))
    c['population_review']['notional_total']='1730'
    for r in c['relationships']:
        for key in ('actual_instrument_quantity','actual_item_quantity','forecast_quantity'):r[key]='1730'
        if 'acquired_quantity' in r:r['acquired_quantity']='1730'
        for key in ('opening_reserve','reserve_source_opening','opening_effective','earnings_release','basis_release'):r[key]=str(D(r[key])*D('1.73'))
        risk=r['risk_measurement'];risk['quantity']='1730'
        for key in ('current_change','instrument_cumulative','risk_cumulative','opening_instrument_cumulative','opening_risk_cumulative'):risk[key]=str(D(risk[key])*D('1.73'))
    for g in c['gl']:
        for key in ('opening','closing','statement'):g[key]=str(D(g[key])*D('1.73'))
    return sources(c)

def independent_debt(rate_type='fixed'):
    from financing_cases import ready as dr,case as debt_source
    from production import execute
    dc=debt_source('debt-financing');dc['debt'][0].update(contractual_rate_type=rate_type,contractual_rate_terms_memo='Independent actual executed interest terms '+rate_type,contractual_benchmark='Actual reset reference rate' if rate_type=='variable' else 'none');dc=dr('debt-financing',c=dc);result=execute('debt-financing',dc)
    c=case(route='cash_flow');r=c['relationships'][0];r.update(type='fair_value',item_type='debt',risk_id='interest_rate',hedged_item_id='loan',debt_owner='actual-debt',debt_result_index=0,underlying_carrying='1008.40',debt_terms_memo='Actual lender principal, schedule and contractual maturity',debt_notional='1000',debt_maturity='2028-12-31',opening_basis='0',basis_amortization='0',underlying_rate_type=rate_type)
    r['risk_measurement'].update(item_id='loan',risk_id='interest_rate');c['contracts'][0].update(kind='swap',maturity='2028-12-31')
    c['imports']=[dict(id='debt-import',package='debt-financing',case=dc,result=result)]
    c['owner_links']=[dict(id='actual-debt',owner_import='debt-import',result_path=['debt',0,'closing'],amount='1008.40')]
    c['gl']=[dict(id=k,opening='0',closing=v,statement=v) for k,v in {'Derivative balance forward1':'100','Hedge P&L relationship1':'-10','Hedged item basis adjustment relationship1':'-90'}.items()]
    return sources(c)

class IndependentDerivativeHedge(unittest.TestCase):
    def result(self,c):return workflow().assess(sources(c),[])
    def blocked(self,c):
        with self.assertRaises(ReviewRequired):self.result(c)
    def test_positive_four_framework_standalone(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            with self.subTest(fw=fw):
                r=self.result(independent(fw));self.assertEqual(r['calculations']['derivatives'][0]['closing'],D('173'))
    def test_positive_framework_cashflow_distinction(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            with self.subTest(fw=fw):
                r=self.result(independent(fw,'cash_flow'));self.assertEqual(r['calculations']['hedge_reserves'][0]['closing'],D('173') if fw=='US_GAAP' else D('155.7'))
    def test_positive_basis_and_cancelled_forecast(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            r=self.result(independent(fw,'cash_flow','occurred'));self.assertEqual(r['calculations']['basis_adjustments'][0]['amount'],D('-155.7'))
            r=self.result(independent(fw,'cash_flow','no_longer_expected'));self.assertEqual(r['calculations']['hedge_reserves'][0]['closing'],D(0))
    def test_complex_cumulative_cashflow_reversal(self):
        c=independent(route='cash_flow');v=c['valuations'][0];v.update(opening='200',change='-27',closing='173')
        r=c['relationships'][0];r.update(opening_reserve='160',reserve_source_opening='160',opening_effective='160')
        r['risk_measurement'].update(current_change='50',instrument_cumulative='173',risk_cumulative='-110',opening_instrument_cumulative='200',opening_risk_cumulative='-160')
        c['gl']=[dict(id='Derivative balance forward1',opening='200',closing='173',statement='173'),dict(id='Hedge P&L relationship1',opening='0',closing='-23',statement='-23'),dict(id='Hedge reserve relationship1',opening='-160',closing='-110',statement='-110')]
        result=self.result(c);self.assertEqual(result['calculations']['hedge_reserves'][0]['recognized_oci'],D('-50'));self.assertEqual(result['calculations']['derivatives'][0]['ineffectiveness'],D('23'))
    def test_complex_standalone_swap_liability_settlement(self):
        c=independent();c['contracts'][0]['kind']='swap';c['valuations'][0].update(opening='-40',change='-30',settlement='-20',closing='-50')
        c['gl']=[dict(id='Derivative balance forward1',opening='-40',closing='-50',statement='-50'),dict(id='Derivative P&L forward1',opening='0',closing='30',statement='30'),dict(id='Cash',opening='100',closing='80',statement='80')]
        result=self.result(c);self.assertEqual(result['calculations']['derivatives'][0]['closing'],D('-50'))
    def test_fairvalue_independent_risk_basis(self):
        c=independent(route='cash_flow');r=c['relationships'][0];r.update(type='fair_value',item_type='firm_commitment',opening_basis='20',basis_amortization='0');r['risk_measurement']['current_change']='-155.7'
        c['gl']=[dict(id='Derivative balance forward1',opening='0',closing='173',statement='173'),dict(id='Hedge P&L relationship1',opening='0',closing='-17.3',statement='-17.3'),dict(id='Hedged item basis adjustment relationship1',opening='20',closing='-135.7',statement='-135.7')]
        result=self.result(c);self.assertEqual(result['calculations']['derivatives'][0]['hedged_item_change'],D('-155.7'))
    def test_valuation_dimension_mutations(self):
        for key,value in {'measurement_date':'2026-11-30','opening_date':'2025-12-31','currency':'USD','entity':'Other entity','notional':'1731','closing':'174','qualified_valuer':'Synthetic preparer'}.items():
            c=independent();c['valuations'][0][key]=value
            if key=='qualified_valuer':c['valuations'][0][key]=c['preparer']
            with self.subTest(key=key):self.blocked(c)
    def test_duplicate_and_unconsumed_populations(self):
        for key in ('contracts','valuations','relationships'):
            c=independent(route='cash_flow');c[key].append(copy.deepcopy(c[key][0]));c[key][-1]['id']+='-duplicate'
            with self.subTest(key=key):self.blocked(c)
    def test_exception_framework_and_documentation(self):
        c=independent('US_GAAP');c['contracts'][0].update(exception_applies=True,exception_route='own_use',exception_memo='Claimed',exception_contract_rights='Claimed');self.blocked(c)
        c=independent();c['contracts'][0].update(exception_applies=True,exception_route='own_use',exception_memo='',exception_contract_rights='');self.blocked(c)
    def test_advanced_and_models_fail_closed(self):
        for key,value in {'advanced_route':'macro','excluded_components':'time_value','effectiveness_method':'documented_high_effectiveness','economic_relationship':False,'credit_dominates':True,'external_group_exposure':False}.items():
            c=independent(route='cash_flow');c['relationships'][0][key]=value
            with self.subTest(key=key):self.blocked(c)
        c=independent();c['model']='Risk_Mitigation_Accounting_proposed';self.blocked(c)
    def test_designation_dates_and_quantity(self):
        for key,value in {'designation_date':'2026-02-01','actual_instrument_quantity':'1500','ratio':'1.2','assessment_date':'2026-11-30','instrument_eligible':False,'item_eligible':False,'risk_eligible':False,'objective':''}.items():
            c=independent(route='cash_flow');c['relationships'][0][key]=value
            with self.subTest(key=key):self.blocked(c)
    def test_forecast_and_reserve_errors(self):
        for key,value in {'forecast_quantity':'1731','forecast_probability':'possible','forecast_date':'2028-02-01','opening_reserve':'2','earnings_release':'1','basis_release':'1','forecast_memo':''}.items():
            c=independent(route='cash_flow');c['relationships'][0][key]=value
            with self.subTest(key=key):self.blocked(c)
    def test_reporting_errors(self):
        for key in ('closing','statement','opening'):
            c=independent(route='cash_flow');c['gl'][0][key]=str(D(c['gl'][0][key])+1)
            with self.subTest(key=key):self.blocked(c)
        c=independent();c['disclosure_review']['contract_ids']=[];self.blocked(c)
    def test_risk_measurement_errors(self):
        for key,value in {'instrument_valuation_id':'valuation1','quantity':'1731','currency':'USD','item_id':'wrong','risk_id':'FX','assessment_date':'2026-11-30','instrument_cumulative':'172'}.items():
            c=independent(route='cash_flow');c['relationships'][0]['risk_measurement'][key]=value
            with self.subTest(key=key):self.blocked(c)
    def test_discontinuation_expected_retains_reserve(self):
        c=independent(route='cash_flow');r=c['relationships'][0];r.update(status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='Instrument terminated; purchase still expected')
        result=self.result(c);self.assertEqual(result['calculations']['hedge_reserves'][0]['closing'],D('155.7'))
        r['earnings_release']='155.7';self.blocked(c)
    def test_rebalancing_history_and_voluntary(self):
        c=independent(route='cash_flow');r=c['relationships'][0];r.update(status='rebalanced',rebalancing_date=c['reporting_period'],rebalancing_memo='Actual prospective risk ratio quantity change',historical_effective='0',new_ratio='0.8',new_instrument_quantity='1384',new_item_quantity='1730')
        self.result(c);r['historical_effective']='1';self.blocked(c)
        c=independent(route='cash_flow');c['relationships'][0].update(status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='voluntary');self.blocked(c)
    def test_missing_scope_facts(self):
        for key in ('underlying','contract_memo','scope_memo','embedded_memo'):
            c=independent();c['contracts'][0][key]=''
            with self.subTest(key=key):self.blocked(c)
    def test_source_mutation_without_requalification(self):
        c=independent();c['valuations'][0]['change']='174'
        with self.assertRaises(ReviewRequired):workflow().assess(c,[])
    def test_governed_certification_and_seven_public_routes(self):
        c=ready(independent(route='cash_flow'));r=assess_case(PACKAGE,c);self.assertEqual(r['status'],'complete',r['conclusion'])
        r['evidence'][0].update(source_note='Source: ChatGPT training data',approval_track='TRAINING_DATA_CHECKED',evidence_status='MODEL_DERIVED_AUDIT_REQUIRED',audit_required=True)
        r['evidence'][1].update(source_note='Source: FRC FRS 102')
        import json
        for route in ROUTES:
            with self.subTest(route=route):
                public=json.dumps(to_public(r,route),default=str)
                for forbidden in ('Source:','approval_track','evidence_status','audit_required','reviewer_signoff'):self.assertNotIn(forbidden,public)
                self.assertIn('Qualified',public)
    def test_stale_certification_and_fabricated_self_approval(self):
        c=ready(independent());c['reviewer_signoff']['case_fingerprint']='0'*64;self.assertEqual(assess_case(PACKAGE,c)['status'],'partial')
        c=ready(independent());c['reviewer_signoff']['reviewer']=c['preparer'];self.assertEqual(assess_case(PACKAGE,c)['status'],'partial')
    def test_stale_implementation_without_mutating_shared_files(self):
        c=ready(independent());original=Path.read_bytes
        def changed(path):
            b=original(path)
            return b+b'\n# independent stale bytes' if str(path).endswith('derivatives-hedge-accounting/workflow.py') else b
        with patch.object(Path,'read_bytes',changed):self.assertEqual(assess_case(PACKAGE,c)['status'],'partial')
    def test_stale_knowledge_without_mutating_shared_files(self):
        c=ready(independent());original=Path.read_bytes
        target=c['knowledge_review']['documents'][0]['path']
        def changed(path):
            b=original(path)
            return b+b'\n' if str(path).endswith(target) else b
        with patch.object(Path,'read_bytes',changed):self.assertEqual(assess_case(PACKAGE,c)['status'],'blocked')
    def test_independent_inventory_exact_once_and_current_owner(self):
        from test_hedge_inventory_integration import inventory_handoff_case
        from inventory_cases import ready as ir,sources as ins,content as ic,replace_doc
        c=inventory_handoff_case();r=assess_case('inventory-cost',ir(c=c));self.assertEqual(r['status'],'complete');self.assertEqual(r['calculations']['closing_inventory'],D('160'))
        # Semantically wrong quantity while refreshing original movement evidence.
        for key,value in (('quantity','9'),('hedge_basis_adjustment_id','unrelated')):
            c=inventory_handoff_case();c['movements'][0][key]=value;ic(c,c['movements'][0]['source_doc'])[key]=value
            r=assess_case('inventory-cost',ir(c=ins(c)));self.assertEqual(r['status'],'blocked')
    def test_current_debt_owner_fair_value_positive_and_identity(self):
        c=independent_debt();r=self.result(c);self.assertEqual(r['calculations']['derivatives'][0]['route'],'fair_value')
        for key,value in {'hedged_item_id':'unrelated-loan','debt_maturity':'2029-12-31','underlying_carrying':'1000','actual_item_quantity':'999'}.items():
            c=independent_debt();c['relationships'][0][key]=value
            with self.subTest(key=key):self.blocked(c)
        c=independent_debt();c['owner_links'][0]['result_path']=['debt',0,'principal'];c['owner_links'][0]['amount']='1000';c['relationships'][0]['underlying_carrying']='1000';self.blocked(c)
    def test_current_netinvestment_owners_positive_and_identity(self):
        from hedge_cases import net_investment_case
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            c=net_investment_case(fw);r=self.result(c);self.assertEqual(r['calculations']['hedge_reserves'][0]['closing'],D('10'))
        for key,value in {'foreign_operation_id':'unrelated-subsidiary','net_investment':'81','group_perspective':False,'translation_change':'-11','actual_item_quantity':'65'}.items():
            c=net_investment_case();c['relationships'][0][key]=value
            with self.subTest(key=key):self.blocked(c)
    def test_netinvestment_disposal_cannot_be_manufactured(self):
        from hedge_cases import net_investment_case
        c=net_investment_case();r=c['relationships'][0];r.update(disposed=True,earnings_release='10');c['gl'][-1].update(closing='0',statement='0');c['gl'][1].update(closing='-100',statement='-100');self.blocked(c)
    def test_near_comparable_initial_investment_is_not_little(self):
        c=independent();c['contracts'][0].update(initial_net_investment='99',comparable_investment='100',small_initial_investment=True);self.blocked(c)
    def test_variable_rate_debt_cashflow_actual_owner(self):
        c=independent_debt('variable');r=c['relationships'][0];r.update(type='cash_flow',item_type='variable_debt')
        c['gl']=[dict(id=k,opening='0',closing=v,statement=v) for k,v in {'Derivative balance forward1':'100','Hedge P&L relationship1':'-10','Hedge reserve relationship1':'-90'}.items()]
        result=self.result(c);self.assertEqual(result['calculations']['hedge_reserves'][0]['closing'],D('90'))
    def test_frs_prospective_qualification_differs_from_ifrs_inception(self):
        c=independent('UK_GAAP','cash_flow');c['relationships'][0]['inception_date']='2025-12-01';self.result(c)
        c=independent('IFRS','cash_flow');c['relationships'][0]['inception_date']='2025-12-01';self.blocked(c)
    def test_endperiod_probability_loss_retains_expected_reserve(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            c=independent(fw,'cash_flow');r=c['relationships'][0];r.update(forecast_probability='expected',status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='probability_lost',probability_before_cessation='probable' if fw=='US_GAAP' else 'highly_probable',measurement_through_qualification_date=c['reporting_period'])
            self.assertEqual(self.result(c)['calculations']['hedge_reserves'][0]['closing'],D('173') if fw=='US_GAAP' else D('155.7'))
            r['measurement_through_qualification_date']='2026-06-30';self.blocked(c)
    def test_unrelated_equity_fairvalue_result_cannot_qualify_derivative(self):
        from financing_cases import ready as fr
        from production import execute
        c=independent();fc=fr('fair-value-measurement');r=execute('fair-value-measurement',fc)
        c['imports']=[dict(id='equity-fv',package='fair-value-measurement',case=fc,result=r)]
        # Existing FV owner is quoted equity only. This output cannot support a forward.
        c['owner_links']=[dict(id='unrelated-equity-fv',owner_import='equity-fv',result_path=['measurements',0,'value'],amount='120')]
        self.blocked(c)
    def test_fx_owner_wrong_transaction_cannot_bind_forecast(self):
        from additional_cases import fx,certify
        from production import execute
        c=independent(route='cash_flow');fc=certify('foreign-currency',fx());fr=execute('foreign-currency',fc)
        c['imports']=[dict(id='fx-source',package='foreign-currency',case=fc,result=fr)]
        c['owner_links']=[dict(id='fx-wrong-item',owner_import='fx-source',result_path=['transactions','AR','closing'],amount='72')]
        r=c['relationships'][0];r.update(risk_id='FX',fx_owner='fx-wrong-item',fx_exposure='72',functional_currency='EUR');r['risk_measurement']['risk_id']='FX'
        self.blocked(c)
    def test_multiple_contract_population_and_partial_scope(self):
        c=independent();contract=copy.deepcopy(c['contracts'][0]);contract.update(id='swap2',kind='swap',notional='560');c['contracts'].append(contract)
        valuation=copy.deepcopy(c['valuations'][0]);valuation.update(id='valuation2',instrument_id='swap2',notional='560',change='-41',settlement='-17',closing='-24');c['valuations'].append(valuation)
        c['population_review'].update(contract_ids=['forward1','swap2'],notional_total='2290');c['disclosure_review']['contract_ids']=['forward1','swap2']
        c['gl'] += [dict(id=k,opening='0',closing=v,statement=v) for k,v in {'Derivative balance swap2':'-24','Derivative P&L swap2':'41','Cash':'-17'}.items()]
        result=self.result(c);self.assertEqual(len(result['calculations']['derivatives']),2)
        c['population_review']['contract_ids']=['forward1'];self.blocked(c)
    def test_fx_full_disposal_cannot_contradict_current_group_perimeter(self):
        from hedge_cases import net_investment_case
        from additional_cases import certify
        from production import execute
        c=net_investment_case();imp=next(i for i in c['imports'] if i['package']=='foreign-currency');fc=imp['case']
        fc['disposal'].update(kind='full',date=c['reporting_period'],qualifying_disposal_reviewed=True,owners_cta='-8',nci_cta='-2');fc=certify('foreign-currency',fc);imp.update(case=fc,result=execute('foreign-currency',fc))
        r=c['relationships'][0];r.update(disposed=True,earnings_release='10');c['gl'][-1].update(closing='0',statement='0');c['gl'][1].update(closing='-100',statement='-100')
        self.blocked(c)
    def test_initial_investment_contradiction(self):
        c=independent();c['contracts'][0]['initial_net_investment']='1730000';self.blocked(c)
    def test_unsupported_exception_does_not_skip_valuation(self):
        c=independent();c['contracts'][0].update(exception_applies=True,exception_route='own_equity',exception_memo='Management asserted exception',exception_contract_rights='No fixed-for-fixed classification evidence');c['valuations']=[];c['gl']=[];self.blocked(c)
    def test_hedged_risk_current_vs_cumulative(self):
        c=independent(route='cash_flow');c['relationships'][0]['risk_measurement']['current_change']='-900';self.blocked(c)
    def test_late_docs_default_derivative_result(self):
        c=independent(route='cash_flow');c['relationships'][0]['documentation_date']='2026-02-01';c['gl']=[dict(id='Derivative balance forward1',opening='0',closing='173',statement='173'),dict(id='Derivative P&L forward1',opening='0',closing='-173',statement='-173')]
        r=self.result(c);self.assertEqual(r['calculations']['derivatives'][0]['route'],'standalone')

if __name__=='__main__':unittest.main()

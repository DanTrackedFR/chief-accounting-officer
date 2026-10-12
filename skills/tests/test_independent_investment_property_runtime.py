"""Independent AI implementation QA; synthetic sources, no human certification.

Authored by separate runtime reviewer, not the substantive workflow author.
Arithmetic expectations below are literal independent calculations, not imported
production calculations or generated expected-output artifacts.
"""
import json
import hashlib
import unittest
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from investment_property_cases import case, ready, capture
from production import assess_case, case_fingerprint, to_public


def run(c):
    return assess_case('investment-property', c)


class IndependentInvestmentRuntimeQA(unittest.TestCase):
    def complete(self, c):
        r = run(ready(c=c))
        self.assertEqual('complete', r['status'], r.get('conclusion'))
        for entry in r['journal_entry_implications']:
            debit = sum((Decimal(x['amount']) for x in entry if x['side'] == 'Dr'), Decimal(0))
            credit = sum((Decimal(x['amount']) for x in entry if x['side'] == 'Cr'), Decimal(0))
            self.assertEqual(debit, credit)
        return r

    def blocked(self, c, recapture=True):
        if recapture:
            capture(c)
        r = run(ready(c=c))
        self.assertEqual('blocked', r['status'], r.get('conclusion'))
        self.assertEqual([], r['journal_entry_implications'])
        return r

    def test_independent_fair_value_arithmetic_all_permitted_frameworks(self):
        for fw in ('IFRS', 'AASB', 'UK_GAAP'):
            with self.subTest(fw=fw):
                r = self.complete(case(fw))
                self.assertEqual(Decimal('50000'), r['calculations']['fair_value_movement'])
                self.assertEqual(Decimal('650000'), r['calculations']['closing_carrying'])
                self.assertEqual(1, len(r['journal_entry_implications']))

    def test_cost_owner_charge_is_evidence_only(self):
        for fw, model in (('IFRS','cost'), ('AASB','cost'), ('US_GAAP','cost'), ('UK_GAAP','group_cost')):
            with self.subTest(fw=fw):
                r = self.complete(case(fw,model))
                self.assertEqual(Decimal('20000'), r['calculations']['depreciation_owned_elsewhere'])
                self.assertEqual(Decimal('580000'), r['calculations']['closing_carrying'])
                self.assertEqual([], r['journal_entry_implications'])

    def test_initial_cost_independent_cash_math(self):
        for fw in ('IFRS','AASB','US_GAAP'):
            with self.subTest(fw=fw):
                r = self.complete(case(fw,'cost','initial'))
                self.assertEqual(Decimal('600000'),r['calculations']['additions'])
                self.assertEqual(Decimal('600000'),r['calculations']['closing_carrying'])
                self.assertEqual(Decimal('600000'),r['journal_entry_implications'][0][1]['amount'])

    def test_disposal_independent_math_both_models(self):
        for model, carrying, gain in (('fair_value','650000','40000'),('cost','580000','110000')):
            with self.subTest(model=model):
                r=self.complete(case('IFRS',model,'disposal'))
                for key, amount in [('disposal_carrying',carrying),('net_proceeds','690000'),('disposal_gain',gain),('closing_carrying','0')]:
                    self.assertEqual(Decimal(amount),r['calculations'][key])

    def test_transfers_independently_reconcile(self):
        # R4 correction: current PPE 600k less owned 20k annual depreciation
        # transfers 580k, not the prior-period 600k (old oracle was incorrect).
        for model, route, amount in [('cost','transfer_in_cost','580000'),('cost','transfer_out_cost','-580000'),('fair_value','transfer_out_fv','-650000')]:
            with self.subTest(route=route):
                r=self.complete(case('IFRS',model,route))
                self.assertEqual(Decimal(amount),r['calculations']['transfers'])
                self.assertEqual(Decimal(abs(Decimal(amount))),r['journal_entry_implications'][-1][0]['amount'])

    def test_mixed_use_supported_and_unsupported(self):
        self.complete(case(mixed='separable'))
        self.complete(case(mixed='inseparable'))
        c=case(mixed='inseparable');c['properties'][0]['owner_use_insignificant']=False;self.blocked(c)
        c=case(mixed='separable');c['properties'][0]['segregation']['parts'][1]['cost']='200001';self.blocked(c)

    def test_valuation_identity_date_framework_currency_and_uncertainty(self):
        mutations={'valuation_date':'2026-12-30','valuation_standard':'ASC820','currency':'USD','legal_entity':'Other entity','asset_id':'other-property','period':['2025-01-01','2025-12-31'],'amount':'650000.001','reliable':False,'material_unresolved_uncertainty':True,'transaction_costs_deducted':True,'recognized_by_other_owner':True,'report_hash':'fake'}
        for field,value in mutations.items():
            with self.subTest(field=field):
                c=case();c['valuation'][field]=value;self.blocked(c)
        c=case();c['valuation']['qualified_reviewer']=c['valuation']['valuer'];self.blocked(c)

    def test_unsupported_property_feature_population(self):
        for field in ('right_of_use','finance_lessor','business_combination','construction','inventory','held_for_sale','sale_leaseback','complex_consideration','foreign_operation','significant_services'):
            with self.subTest(field=field):
                c=case();c['properties'][0][field]=True;self.blocked(c)

    def test_property_rights_and_exact_identity(self):
        for field,value in [('owned',False),('legal_owner','Other'),('source_currency','USD'),('source_entity','Other'),('source_framework','US_GAAP'),('recognition_criteria_met',False)]:
            with self.subTest(field=field):
                c=case();c['properties'][0][field]=value;self.blocked(c)
        c=case();c['properties'].append(deepcopy(c['properties'][0]));self.blocked(c)

    def test_policy_elections_and_effective_edition(self):
        for fw, model in [('US_GAAP','fair_value'),('IFRS','group_cost'),('AASB','group_cost'),('UK_GAAP','cost')]:
            with self.subTest(fw=fw,model=model):self.blocked(case(fw,model))
        for field,value in [('early_adoption',True),('policy_change',True),('class_consistent',False),('effective_standard','IAS40_2025')]:
            with self.subTest(field=field):
                c=case();c['accounting_policy'][field]=value;self.blocked(c)
        c=case('AASB');c['reporting_tier']=2;self.blocked(c)

    def test_duplicate_economic_owner_and_cross_owner_registration(self):
        c=case();duplicate=deepcopy(c['ownership_register'][0]);duplicate['id']='second-owner';duplicate['accounting_owner']='Fair Value Measurement';c['ownership_register'].append(duplicate);c['ownership_inventory'].append('second-owner');self.blocked(c)
        c=case();c['ownership_register'][0]['accounting_owner']='Fair Value Measurement';self.blocked(c)
        c=case('IFRS','cost');c['cost_owner']['accounting_owner']='Investment Property';self.blocked(c)

    def test_recaptured_consistent_disclosure_cannot_override_math(self):
        c=case('IFRS','cost');c['cost_owner']['depreciation']='19000';c['cost_owner']['closing_before_impairment']='581000';c['impairment_owner']['opening_carrying']='581000';c['impairment_owner']['closing_carrying']='581000';c['properties'][0]['closing_carrying']='581000';c['gl'][0]['opening']='581000';c['gl'][0]['closing']='581000';c['gl'][0]['statement']='581000';c['disclosure_review']['amounts']['depreciation_owned_elsewhere']='19000';c['disclosure_review']['amounts']['closing_carrying']='581000';self.blocked(c)

    def test_original_sources_cannot_be_rewritten_by_new_certification(self):
        c=case();c['valuation']['amount']='700000';c['properties'][0]['closing_carrying']='700000';c['disclosure_review']['amounts']['fair_value_movement']='100000';c['disclosure_review']['amounts']['closing_carrying']='700000';self.blocked(c,recapture=False)

    def test_disposal_proceeds_and_transfer_direction_cannot_be_asserted(self):
        c=case(route='disposal');c['events'][0]['net_cash_received']='700000';self.blocked(c)
        c=case(route='disposal');c['events'][0]['continuing_involvement']=True;self.blocked(c)
        c=case('IFRS','cost','transfer_in_cost');c['events'][0]['actual_change_of_use']=False;self.blocked(c)
        c=case('IFRS','cost','transfer_in_cost');c['events'][0]['new_use']='owner';self.blocked(c)

    def test_missing_source_and_disclosure_population(self):
        c=case();c['valuation']=None;self.blocked(c)
        c=case();c['events']=[];c['event_inventory']=[];self.blocked(c)
        c=case();c['disclosure_review']['requirements'].remove('restrictions');self.blocked(c)
        c=case();del c['original_source_snapshot'];r=run(ready(c=c));self.assertEqual('blocked',r['status'])

    def test_stale_and_self_certification_never_release_journals(self):
        c=ready();c['judgment_memo']+=' changed';r=run(c);self.assertEqual('partial',r['status']);self.assertEqual([],r['journal_entry_implications'])
        c=ready();c['reviewer_signoff']['reviewer']=c['preparer'];r=run(c);self.assertEqual('partial',r['status']);self.assertEqual([],r['journal_entry_implications'])
        c=ready();c['knowledge_review']['documents'][0]['sha256']='0'*64;r=run(c);self.assertEqual('blocked',r['status'])

    def test_public_output_excludes_private_source_provenance(self):
        r=self.complete(case())
        for route in ('answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export'):
            with self.subTest(route=route):
                p=to_public(r,route)
                text=json.dumps(p,default=str)
                for secret in ('a'*64,'synthetic external valuer','synthetic qualified separate reviewer','original_source_snapshot','source_note'):
                    self.assertNotIn(secret,text)

    def test_case_fingerprint_preserves_history_and_mutation_identity(self):
        c=ready();old=deepcopy(c);h=case_fingerprint(c);r=run(c);run(c);self.assertEqual(c,old);self.assertEqual(h,case_fingerprint(c));self.assertEqual(h,r['case_fingerprint'])
        c['events'][0]['event_memo']+=' changed';self.assertNotEqual(h,case_fingerprint(c));self.assertEqual('blocked',run(c)['status'])

    def test_non_cutoff_initial_recognition_requires_subsequent_owner_accounting(self):
        c=case('IFRS','cost','initial');c['events'][0]['date']='2026-06-30';c['events'][0]['cash_date']='2026-06-30'
        for item in c['events'][0]['cost_items']:item['date']='2026-06-30'
        self.blocked(c)

    def test_non_cutoff_transfer_disposal_and_fair_value_are_not_yearend_measurement(self):
        for model,route in [('cost','transfer_in_cost'),('cost','transfer_out_cost'),('fair_value','transfer_out_fv'),('fair_value','disposal'),('fair_value','initial')]:
            with self.subTest(model=model,route=route):
                c=case('IFRS',model,route)
                for key in ('date','cash_date','change_use_date'):c['events'][0][key]='2026-06-30'
                if c['valuation']:c['valuation']['valuation_date']='2026-06-30'
                if route=='initial':
                    c['properties'][0]['acquisition_date']='2026-06-30'
                    for item in c['events'][0]['cost_items']:item['date']='2026-06-30'
                self.blocked(c)

    def test_prior_asset_model_and_carrying_history_cannot_be_elected_again(self):
        for field,value in [('measurement_model','cost'),('carrying','590000'),('previous_reporting_date','2025-12-30'),('asset_id','other-asset'),('currency','USD')]:
            with self.subTest(field=field):
                c=case();c['properties'][0]['opening_history'][field]=value;self.blocked(c)
        c=case();c['properties'][0]['acquisition_date']='2026-01-01';self.blocked(c)
        c=case('IFRS','cost');c['properties'][0]['opening_accumulated_impairment']='10000';c['properties'][0]['gross_cost']='610000';self.blocked(c)

    def test_fair_value_decrease_and_fractional_cents_independent_oracle(self):
        c=case();c['valuation']['amount']='525123.45';c['properties'][0]['closing_carrying']='525123.45'
        c['gl'][0]['closing']=c['gl'][0]['statement']='525123.45';c['gl'][1]['closing']=c['gl'][1]['statement']='74876.55'
        c['disclosure_review']['amounts']['closing_carrying']='525123.45';c['disclosure_review']['amounts']['fair_value_movement']='-74876.55';capture(c)
        r=self.complete(c);self.assertEqual(Decimal('-74876.55'),r['calculations']['fair_value_movement'])
        self.assertEqual('Cr',r['journal_entry_implications'][0][0]['side']);self.assertEqual(Decimal('74876.55'),r['journal_entry_implications'][0][0]['amount'])

    def test_loss_on_disposal_and_no_double_counted_fair_value(self):
        c=case(route='disposal');c['events'][0].update(gross_proceeds='410000',selling_costs='10000',net_cash_received='400000')
        for g in c['gl']:
            if g['id']=='Cash':g['closing']=g['statement']='400000'
            if g['id']=='Property disposal profit or loss':g['closing']=g['statement']='250000'
        c['disclosure_review']['amounts'].update(net_proceeds='400000',disposal_gain='-250000');capture(c)
        r=self.complete(c);self.assertEqual(Decimal('-250000'),r['calculations']['disposal_gain']);self.assertEqual(2,len(r['journal_entry_implications']))
        self.assertEqual(Decimal('50000'),r['calculations']['fair_value_movement'])

    def test_disclosure_numeric_sources_and_owner_documents_required(self):
        for field in ('rental_income','direct_expenses_generating_income','direct_expenses_not_generating_income','commitments_amount','restrictions_memo','commitments_memo','rental_owner_document','statement_owner_document'):
            with self.subTest(field=field):
                c=case();del c['disclosure_review'][field];self.blocked(c)

    def test_negative_fabricated_costs_cannot_net_to_valid_acquisition(self):
        c=case('IFRS','cost','initial');c['events'][0]['cost_items'][0]['amount']='610000';c['events'][0]['cost_items'][1]['amount']='-10000';self.blocked(c)
        c=case('IFRS','cost','initial');c['events'][0]['cost_items'][1]['economic_id']=c['events'][0]['cost_items'][0]['economic_id'];self.blocked(c)

    def test_omitted_offset_gl_and_statement_mismatch_block(self):
        c=case();c['gl']=c['gl'][:1];c['gl_inventory']=c['gl_inventory'][:1];self.blocked(c)
        c=case();c['gl'][1]['statement']='-49000';self.blocked(c)

    def test_framework_and_reporting_period_change_invalidates_case(self):
        c=case();c['framework']='AASB';self.blocked(c)
        c=case();c['period_start']='2025-01-01';self.blocked(c)
        c=case();c['reporting_period']='2026-06-30';self.blocked(c)

    def test_every_supported_route_class_rollforward_independent_equation(self):
        routes=[]
        for fw,models in [('IFRS',('cost','fair_value')),('AASB',('cost','fair_value')),('UK_GAAP',('fair_value','group_cost')),('US_GAAP',('cost',))]:
            for model in models:
                routes.extend((fw,model,route) for route in ('initial','hold','disposal'))
        routes.extend((fw,model,route) for fw in ('IFRS','AASB') for model,route in [('cost','transfer_in_cost'),('cost','transfer_out_cost'),('fair_value','transfer_out_fv')])
        for fw,model,route in routes:
            with self.subTest(fw=fw,model=model,route=route):
                calc=self.complete(case(fw,model,route))['calculations']
                closing=calc['opening_carrying']+calc['additions']-calc['depreciation_owned_elsewhere']-calc['impairment_owned_elsewhere']+calc['fair_value_movement']+calc['transfers']-calc['disposal_carrying']
                self.assertEqual(calc['closing_carrying'],closing)
                if route=='transfer_in_cost':
                    self.assertEqual(Decimal('0'),calc['opening_carrying'])
                    self.assertEqual(Decimal('580000'),calc['transfers'])
                    self.assertEqual(Decimal('580000'),closing)

    def test_deterministic_artifact_manifest_bytes_and_independent_bridges(self):
        root=Path(__file__).resolve().parents[1]/'investment-property/examples/production'
        manifest=json.loads((root/'source-evidence-manifest.json').read_text())
        self.assertEqual(42,len(manifest['scenarios']))
        self.assertEqual(210,len(manifest['files']))
        for filename,expected in manifest['files'].items():
            with self.subTest(file=filename):
                self.assertEqual(expected,hashlib.sha256((root/filename).read_bytes()).hexdigest())
        for entry in manifest['scenarios']:
            with self.subTest(scenario=entry['name']):
                source=json.loads((root/(entry['name']+'.case.json')).read_text())
                raw=json.dumps(source['original_source_snapshot'],sort_keys=True,indent=2,default=str)+'\n'
                self.assertEqual(entry['source_sha256'],hashlib.sha256(raw.encode()).hexdigest())
                result=json.loads((root/(entry['name']+'.result.json')).read_text())
                self.assertEqual(entry['expected_status'],result['status'])
                self.assertEqual(result,json.loads(json.dumps(run(source),default=str)))
                self.assertEqual(result['calculations'],entry['expected_calculations'])
                if result['status']=='complete':
                    c={k:Decimal(v) for k,v in result['calculations'].items() if k!='measurement_model'}
                    self.assertEqual(c['closing_carrying'],c['opening_carrying']+c['additions']-c['depreciation_owned_elsewhere']-c['impairment_owned_elsewhere']+c['fair_value_movement']+c['transfers']-c['disposal_carrying'])
                    for journal in result['journal_entry_implications']:
                        self.assertEqual(sum(Decimal(x['amount']) for x in journal if x['side']=='Dr'),sum(Decimal(x['amount']) for x in journal if x['side']=='Cr'))
                else:self.assertEqual([],result['journal_entry_implications'])


if __name__=='__main__':unittest.main()

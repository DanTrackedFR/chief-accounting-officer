"""Authored independent-source factory arithmetic, adverse cases and privacy tests."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from inventory_cases import *
from production import assess_case,to_public,serializable
from interfaces.public_output import ROUTES

class Inventory(unittest.TestCase):
    def run_case(self,c):return assess_case(PACKAGE,ready(c=sources(c)))
    def block(self,c):self.assertEqual('blocked',self.run_case(c)['status'])
    def test_four_framework_manufacturing(self):
        for f in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            for costing in ('actual','standard'):
                r=self.run_case(case(f,costing=costing));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('1200'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('200'),r['calculations']['cogs'])
    def test_job_batch_process(self):
        for a in ('job','batch','process'):
            c=case();c['orders'][0]['architecture']=a;self.assertEqual('complete',self.run_case(c)['status'])
    def test_standard_gross_journals(self):
        r=self.run_case(case(costing='standard'));a=r['calculations']['order-1'];self.assertEqual(Decimal('910'),a['standard_total']);self.assertEqual(Decimal('60'),a['variances']['material_price']);self.assertEqual(Decimal('100'),a['under_recovery']);self.assertTrue(any('Manufacturing material_price variance'==l['account'] for j in r['journal_entry_implications'] for l in j))
    def test_over_recovery(self):
        r=self.run_case(over_recovery_case());self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('-100'),r['calculations']['order-1']['standard_recovery'])
    def test_high_output_actual_cap(self):
        r=self.run_case(high_capacity_case());self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('200'),r['calculations']['order-1']['absorbed_fixed'])
    def test_net_material_return(self):
        for co in ('actual','standard'):
            r=self.run_case(return_case(co));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('600'),r['calculations']['order-1']['material'])
    def test_us_lifo(self):
        r=self.run_case(case('US_GAAP','resale',formula='LIFO'));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('100'),r['calculations']['cogs'])
    def test_fifo_weighted_average_specific(self):
        for formula,n in [('FIFO','250'),('WEIGHTED_AVERAGE','225'),('SPECIFIC_IDENTIFICATION','250')]:
            r=self.run_case(case(kind='resale',formula=formula));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal(n),r['calculations']['closing_inventory'])
    def test_nrv_write_down(self):
        for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            r=self.run_case(valuation_case(fw));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('70'),r['calculations']['write_down'])
    def test_reversal_framework_difference(self):
        for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            r=self.run_case(valuation_case(fw,True));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('0' if fw=='US_GAAP' else '50'),r['calculations']['reversal'])
    def test_us_lcm(self):
        r=self.run_case(valuation_case('US_GAAP',False,'LIFO'));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('150'),r['calculations']['closing_inventory'])
    def test_unsigned_partial(self):
        c=ready();c.pop('reviewer_signoff');self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_certification_partial(self):
        c=ready();c['judgment_memo']='Changed approved narrative';self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_implementation_partial(self):
        c=ready()
        with patch('production.case_fingerprint',return_value='changed-implementation'):self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_knowledge_blocks(self):
        c=ready();c['knowledge_review']['documents'][0]['sha256']='stale';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_missing_claim_blocks(self):
        c=ready();c['knowledge_review']['claim_ids'].pop();self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_incomplete_applied_decisions(self):
        c=ready();c['knowledge_review']['applied_claim_ids']=c['knowledge_review']['claim_ids'][:1];self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_stale_release_blocks(self):
        c=ready();c['release_review']['payload_fingerprint']='stale';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_stale_original_blocks(self):
        c=ready();c['originals']['items']['records'][0]['closing_cost']='999';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_public_routes(self):
        r=self.run_case(case());r['evidence'][0]['source_note']='Source: ChatGPT training data';r['facts_used']['secret']='private reviewer'
        for route in ROUTES:
            txt=json.dumps(to_public(r,route),default=serializable)
            for token in ('Source:','approval_track','evidence_status','audit_required','private reviewer','sha256','case_fingerprint'):self.assertNotIn(token,txt)
    def test_malformed(self):
        for c in (None,{},[],dict(framework='OTHER'),dict(items=[])):self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_examples_reproduce(self):
        from generate_inventory_examples import artifacts
        root=Path(__file__).resolve().parents[2]
        for path,obj in artifacts().items():self.assertEqual(json.loads((root/path).read_text()),json.loads(json.dumps(obj,default=serializable)),path)

    def test_company_grouped_variance_architecture(self):
        r=self.run_case(grouped_standard_case());self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('1000'),r['calculations']['order-1']['actual_eligible_total'])
    def test_grouped_variance_cannot_hide_gross_exposure(self):
        c=grouped_standard_case();c['standards'][0]['reporting_gross_adverse']='90';self.block(c)
    def test_us_requested_reversal_blocked(self):
        c=valuation_case('US_GAAP',True);c['valuation'][0]['adjustment']='50';self.block(c)
    def test_raw_finished_goods_context(self):
        for f in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            for recoverable in (True,False):
                r=self.run_case(raw_context_case(f,recoverable));self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('0' if f in {'IFRS','AASB'} and recoverable else '80'),r['calculations']['write_down'])
    def test_raw_standalone_decline_cannot_override_finished_recovery(self):
        c=raw_context_case();a=content(c,'raw-recovery-source');a['raw_measurement_method']='replacement_cost';self.block(c)
    def test_unowned_requested_actions(self):
        for action in ('erp_posting','audit_opinion','forecast','autonomous_standard_setting'):
            c=case();c['requested_action']=action;self.block(c)
    def test_unit_cost_and_stock_quantity_schedules(self):
        r=self.run_case(case());a=r['calculations'];self.assertEqual(Decimal('10'),a['order-1']['finished_unit_cost']);self.assertEqual(Decimal('80'),a['order-1']['completed_quantity']);self.assertEqual(Decimal('20'),a['order-1']['closing_equivalent_units']);self.assertEqual(Decimal('1000'),a['class_bridges']['Raw materials']['opening']);self.assertEqual(Decimal('40'),a['quantity_population']['component']['closing_quantity']);self.assertEqual('units',a['quantity_population']['component']['unit'])
    def test_purchased_standard_ppv(self):
        r=self.run_case(purchase_standard_case());self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('50'),r['calculations']['purchase_price_variance'])
    def test_stale_standards(self):
        c=case(costing='standard');c['standards'][0]['current']=False;self.block(c)
    def test_unreviewed_standard_approximation(self):
        c=case(costing='standard');c['standards'][0]['material_deviation_reviewed']=False;self.block(c)
    def test_unsupported_standard_revaluation(self):
        c=case(costing='standard');c['standards'][0]['unsupported_revaluation']=True;self.block(c)
    def test_gross_variance_netted(self):
        c=case(costing='standard');c['standards'][0]['disposition']['components'][0]['total']='0';self.block(c)
    def test_variance_idle_buried(self):
        c=case(costing='standard');a=c['standards'][0]['disposition']['components'][-1];a.update(inventory='100',idle_expense='0');self.block(c)
    def test_variance_sign_wrong(self):
        c=case(costing='standard');c['standards'][0]['disposition']['components'][0].update(total='-60',inventory='-60');self.block(c)
    def test_original_reversal_ceiling(self):
        c=valuation_case(reversal=True);content(c,'valuation-source')['original_cost']='350';self.block(c)
    def test_prior_write_down_unbound(self):
        c=valuation_case(reversal=True);c['valuation'][0]['prior_write_down']='100';self.block(c)
    def test_duplicate_valuation(self):
        c=valuation_case();v=copy.deepcopy(c['valuation'][0]);v['id']='alias';c['valuation'].append(v);self.block(c)
    def test_stale_sales_price(self):
        c=valuation_case();content(c,'valuation-source')['current_market']=False;self.block(c)
    def test_completion_estimate_omitted(self):
        c=valuation_case();content(c,'valuation-source')['completion_cost_complete']=False;self.block(c)
    def test_selling_estimate_omitted(self):
        c=valuation_case();content(c,'valuation-source')['selling_cost_complete']=False;self.block(c)
    def test_forecast_stale(self):
        c=valuation_case();content(c,'valuation-source').update(forecast_used=True,forecast_checked_on='2026-01-01');self.block(c)
    def test_expiry_ignored(self):
        c=case();content(c,'component-measurement')['expired']=True;self.block(c)
    def test_discontinued_ignored(self):
        c=case();content(c,'component-measurement')['discontinued']=True;self.block(c)
    def test_false_ifrs_lifo(self):self.block(case(formula='LIFO'))
    def test_lifo_uk_aasb(self):
        for f in ('UK_GAAP','AASB'):self.block(case(f,formula='LIFO'))
    def test_abnormal_material_loss_expensed(self):
        c=case();content(c,'loss')['abnormal_material_cost']='100';o=c['orders'][0];o.update(completed_cost='720',closing_wip_cost='180');c['movements'][1]['amount']='720';c['movements'][2]['amount']='180';c['items'][1]['closing_cost']='180';c['items'][2]['closing_cost']='540'
        for g in c['gl']:
            if g['id']=='Work in progress':g['closing']=g['statement']='180'
            elif g['id']=='Finished goods':g['closing']=g['statement']='540'
            elif g['id']=='Cost of goods sold':g['closing']=g['statement']='180'
        c['gl'].append(row(c,'Abnormal manufacturing expense',currency='USD',opening='0',closing='100',statement='100'));c['gl_inventory']=[g['id'] for g in c['gl']];c['disclosures'].update(closing_inventory='1120',cogs='180');disclosure_support(c)
        r=self.run_case(c);self.assertEqual('complete',r['status'],r['conclusion']);self.assertEqual(Decimal('100'),r['calculations']['order-1']['abnormal_material_expense'])

MUTATIONS={
 'wrong_item_currency':lambda c:c['items'][0].update(currency='EUR'),
 'malformed_unit':lambda c:c['items'][0].update(unit='cases'),
 'duplicate_physical_alias':lambda c:c['items'][1].update(physical_id=c['items'][0]['physical_id']),
 'closing_quantity_plug':lambda c:c['items'][0].update(closing_quantity='41'),
 'closing_cost_plug':lambda c:c['items'][0].update(closing_cost='401'),
 'opening_layer_cost':lambda c:c['items'][0]['opening_layers'][0].update(cost='999'),
 'opening_layer_quantity':lambda c:c['items'][0]['opening_layers'][0].update(quantity='99'),
 'opening_layer_date':lambda c:c['items'][0]['opening_layers'][0].update(date='2026-01-01'),
 'third_party_owned':lambda c:content(c,'component-rights').update(third_party_owned=True),
 'not_owned':lambda c:content(c,'component-rights').update(owned=False),
 'ownership_wrong_entity':lambda c:content(c,'component-rights').update(entity='OTHER'),
 'ownership_stale':lambda c:content(c,'component-rights').update(checked_on='2026-01-01'),
 'wrong_movement_currency':lambda c:c['movements'][0].update(currency='EUR'),
 'wrong_movement_unit':lambda c:c['movements'][0].update(unit='kg'),
 'negative_stock':lambda c:c['movements'][0].update(quantity='101'),
 'wrong_material_cost':lambda c:c['movements'][0].update(amount='601'),
 'wrong_period_completion':lambda c:c['movements'][1].update(date='2027-01-01'),
 'wrong_completion_order':lambda c:c['movements'][1].update(order_id='missing'),
 'wrong_output_quantity':lambda c:c['movements'][1].update(quantity='81'),
 'wrong_cogs':lambda c:c['movements'][2].update(amount='201'),
 'wrong_movement_economic_alias':lambda c:c['movements'][2].update(economic_id=c['movements'][1]['economic_id']),
 'nonfactory_labour':lambda c:content(c,'labour-source').update(manufacturing=False),
 'labour_source_rate':lambda c:content(c,'labour-source').update(rate='99'),
 'labour_source_hours':lambda c:content(c,'labour-source').update(hours='99'),
 'wrong_cost_currency':lambda c:c['costs'][0].update(currency='EUR'),
 'wrong_cost_period':lambda c:c['costs'][0].update(date='2027-01-01'),
 'labour_rate_wrong':lambda c:c['costs'][0].update(rate='11'),
 'labour_hours_wrong':lambda c:c['costs'][0].update(hours='21'),
 'cost_duplicate_alias':lambda c:c['costs'][1].update(economic_id=c['costs'][0]['economic_id']),
 'overhead_pool_incomplete':lambda c:content(c,'fixed-source').update(pool_complete=False),
 'variable_driver_wrong':lambda c:c['costs'][1].update(driver_units='101'),
 'capacity_invented':lambda c:content(c,'capacity').update(reviewed_multi_period=False),
 'capacity_zero':lambda c:content(c,'capacity').update(normal_capacity='0'),
 'capacity_wrong_driver':lambda c:content(c,'capacity').update(driver='labour_hours'),
 'capacity_wrong_denominator':lambda c:content(c,'capacity').update(actual_driver_units='200'),
 'routing_hours_wrong':lambda c:content(c,'routing').update(actual_labour_hours='21'),
 'routing_driver_wrong':lambda c:content(c,'routing').update(actual_driver_units='101'),
 'bom_stale':lambda c:content(c,'bom').update(effective_to='2026-01-01'),
 'substitution_unapproved':lambda c:content(c,'bom').update(substitutions_approved=False),
 'output_exceeds_input':lambda c:content(c,'bom')['components'][0].update(maximum_good_output='90'),
 'scrap_omitted':lambda c:content(c,'loss').update(reported_loss='1'),
 'yield_unexplained':lambda c:content(c,'loss').update(loss_explained=False),
 'abnormal_capitalized':lambda c:content(c,'loss').update(abnormal_excluded=False),
 'yield_input_conflict':lambda c:content(c,'loss')['net_component_usage'].update(component='61'),
 'wrong_wip_equivalent':lambda c:content(c,'completion-evidence').update(closing_equivalent_units='21'),
 'unsupported_heterogeneous_wip':lambda c:content(c,'completion-evidence').update(homogeneous_equivalents_reviewed=False),
 'wip_cost_plug':lambda c:c['orders'][0].update(closing_wip_cost='201'),
 'finished_cost_plug':lambda c:c['orders'][0].update(completed_cost='801'),
 'count_omitted_location':lambda c:c['count']['records'].pop(),
 'count_quantity_wrong':lambda c:c['count']['records'][0].update(quantity='39'),
 'cutoff_evidence_missing':lambda c:c['cutoff']['records'].pop(),
 'cutoff_unsupported':lambda c:c['cutoff']['records'][0].update(ownership_supported=False),
 'gl_different':lambda c:c['gl'][0].update(closing='399'),
 'statement_different':lambda c:c['gl'][0].update(statement='399'),
 'disclosure_cogs_wrong':lambda c:c['disclosures'].update(cogs='201'),
 'disclosure_inventory_wrong':lambda c:c['disclosures'].update(closing_inventory='1201'),
 'disclosure_missing':lambda c:c['disclosures']['requirements'].pop('formula'),
 'borrowing_dependency':lambda c:c['scope'].update(borrowing_capitalization=True),
 'joint_product_route':lambda c:c['scope'].update(joint_products=True),
 'forecast_generation':lambda c:c['scope'].update(forecast_generation=True),
 'post_requested':lambda c:c['scope'].update(external_posting=True),
}
for name,mutation in MUTATIONS.items():
    def test(self,mutation=mutation):
        c=case();mutation(c);self.block(c)
    setattr(Inventory,'test_adversarial_'+name,test)

if __name__=='__main__':unittest.main()

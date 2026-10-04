"""Authored Agriculture source, arithmetic, boundary and privacy regression."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from agriculture_cases import *
from production import assess_case,to_public,execute,serializable
from interfaces.public_output import ROUTES

class Agriculture(unittest.TestCase):
    def test_generated_examples_reproduce(self):
        from generate_agriculture_examples import artifacts
        root=Path(__file__).resolve().parents[2]
        for path,obj in artifacts().items():
            self.assertEqual(json.loads((root/path).read_text()),json.loads(json.dumps(obj,default=serializable)),path)
    def run_case(self,c):return assess_case(PACKAGE,ready(c=c,release=True))
    def block(self,c):self.assertEqual('blocked',self.run_case(c)['status'])
    def test_supported_frameworks(self):
        for fw in ('IFRS','UK_GAAP','AASB'):
            for kind in ('livestock','crop'):
                with self.subTest(fw=fw,kind=kind):
                    r=self.run_case(case(fw,kind));self.assertEqual('complete',r['status'],r['conclusion'])
                    self.assertEqual('210',str(r['calculations']['closing']));self.assertEqual('70',str(r['calculations']['measurement_gain']))
                    for j in r['journal_entry_implications']:
                        self.assertEqual(sum(Decimal(str(x['amount'])) for x in j if x['side']=='Dr'),sum(Decimal(str(x['amount'])) for x in j if x['side']=='Cr'))
    def test_missing_review_partial(self):
        c=ready();c.pop('reviewer_signoff');self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_case_partial(self):
        c=ready();c['judgment_memo']='Changed reviewed accounting judgment';self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_implementation_partial(self):
        c=ready();original=case_fingerprint(c)
        with patch('production.case_fingerprint',return_value='stale implementation'):
            self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
        self.assertNotEqual(original,'stale implementation')
    def test_stale_knowledge_blocks(self):
        c=ready();c['knowledge_review']['documents'][0]['sha256']='stale';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_missing_knowledge_claim_blocks(self):
        c=ready();c['knowledge_review']['claim_ids'].pop();self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_missing_applied_decision(self):
        c=ready();c['knowledge_review']['applied_claim_ids']=[];self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_us_gaap_no_ifrs_model(self):self.block(case('US_GAAP'))
    def test_uk_cost_not_copied(self):
        c=case('UK_GAAP');c['accounting_policy']['agriculture_model']='cost';self.block(c)
    def test_ifrs_bearer_ppe(self):
        c=case();c['assets'][0]['category']='bearer_plant';content(c,'live-class')['category']='bearer_plant';self.block(sources(c))
    def test_uk_separate_produce_blocks(self):
        c=case('UK_GAAP');c['assets'][0]['category']='growing_produce';content(c,'live-class')['category']='growing_produce';self.block(sources(c))
    def test_inventory_route(self):
        c=case();content(c,'live-class')['route']='inventory';self.block(c)
    def test_ppe_route(self):
        c=case();content(c,'live-class')['route']='fixed-assets';self.block(c)
    def test_nonagricultural(self):
        c=case();content(c,'live-class')['agricultural_activity']=False;self.block(c)
    def test_nonliving(self):
        c=case();content(c,'live-class')['living']=False;self.block(c)
    def test_control_unresolved(self):
        c=case();content(c,'live-control')['control_supported']=False;self.block(c)
    def test_probable_benefits_missing(self):
        c=case();content(c,'live-control')['probable_benefits']=False;self.block(c)
    def test_control_wrong_entity(self):
        c=case();content(c,'live-control')['entity']='Other';self.block(c)
    def test_stale_valuation(self):
        c=case();content(c,'live-closing')['measurement_date']='2025-12-31';self.block(c)
    def test_stale_market(self):
        c=case();content(c,'live-closing')['current_market_evidence']=False;self.block(c)
    def test_unsupported_valuation(self):
        c=case();content(c,'live-closing')['qualified_valuer']='';self.block(c)
    def test_fv_quantity_conflict(self):
        c=case();content(c,'live-closing')['quantity']='2';self.block(c)
    def test_fv_owner_contradiction(self):
        c=case();content(c,'live-closing')['owner_import']='missing';self.block(c)
    def test_costs_to_sell_wrong_net(self):
        c=case();content(c,'live-closing')['net_value']='135';self.block(c)
    def test_costs_exceed_fv(self):
        c=case();content(c,'live-closing')['costs_to_sell']='140';self.block(c)
    def test_initial_date_wrong(self):
        c=case();content(c,'purchase-initial')['measurement_date']='2026-12-31';self.block(c)
    def test_missing_original_row(self):
        c=case();c['asset_source']['records'].pop();self.block(c)
    def test_missing_document(self):
        c=case();c['documents']=[d for d in c['documents'] if d['id']!='live-control'];c['document_inventory']=[d['id'] for d in c['documents']];self.block(c)
    def test_duplicate_physical_alias(self):
        c=case();c['assets'][2]['physical_id']='physical-live';content(c,'purchase-control')['physical_id']='physical-live';self.block(sources(c))
    def test_duplicate_harvest(self):
        c=case();m=copy.deepcopy(c['movements'][0]);m['id']='second';c['movements'].append(m);self.block(sources(c))
    def test_harvest_remains_living(self):
        c=case();a=c['assets'][1];c['closing_population'].append(row(c,a['id'],quantity='1',physical_id=a['physical_id'],carrying_value='50'));self.block(sources(c))
    def test_closing_physical_missing(self):
        c=case();c['closing_population'].pop();self.block(sources(c))
    def test_wrong_opening_quantity(self):
        c=case();c['opening_population'][0]['quantity']='2';self.block(sources(c))
    def test_opening_carrying_gl_conflict(self):
        c=case();c['gl'][0]['opening']='149';self.block(c)
    def test_purchase_counted_as_opening(self):
        c=case();c['assets'][2]['state']='opening';self.block(sources(c))
    def test_birth_purchase_conflict(self):
        c=case();c['assets'][2]['state']='birth';self.block(sources(c))
    def test_harvest_quantity_conflict(self):
        c=case();content(c,'harvest-record')['harvest_quantity']='99';self.block(c)
    def test_harvest_value_conflict(self):
        c=case();content(c,'harvest-record')['inventory_entry_value']='69';self.block(c)
    def test_partial_harvest_blocks(self):
        c=case();content(c,'harvest-record')['entire_asset_harvested']=False;self.block(c)
    def test_postharvest_flag_blocks(self):
        c=case();c['classification']['post_harvest_accounting']=True;self.block(c)
    def test_grants_dependency_blocks(self):
        c=case();c['classification']['government_assistance']=True;self.block(c)
    def test_fx_dependency_blocks(self):
        c=case();c['classification']['fx']=True;self.block(c)
    def test_gl_currency_blocks(self):
        c=case();c['gl'][0]['currency']='EUR';self.block(c)
    def test_source_currency_blocks(self):
        c=case();c['assets'][0]['currency']='EUR';self.block(sources(c))
    def test_reverse_gain_sign_blocks(self):
        c=case();c['gl'][2]['closing']='70';self.block(c)
    def test_oci_gain_blocks(self):
        c=case();c['disclosures']['presentation']='OCI';self.block(c)
    def test_disclosure_incomplete(self):
        c=case();c['disclosures']['requirements'][0]['supported']=False;content(c,'requirements')[0]['supported']=False;self.block(c)
    def test_disclosure_missing(self):
        c=case();c['disclosures']['requirements'].pop();c['disclosures']['requirement_inventory'].pop();content(c,'requirements').pop();self.block(c)
    def test_price_physical_unsupported(self):
        c=case();c['disclosures']['price_change']='70';self.block(c)
    def test_stale_source_hash(self):
        c=ready();content(c,'live-closing')['fair_value']='999';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_stale_release_review(self):
        c=ready();c['release_review']['payload_fingerprint']='stale';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_early_presentation_blocks(self):
        c=case();c['classification']['early_presentation_adoption']=True;self.block(c)
    def test_aasb_tier2_blocks(self):
        c=case('AASB');c['reporting_tier']=2;self.block(c)
    def test_period_outside_2026(self):
        c=case();c['period_start']='2025-01-01';self.block(c)
    def test_wrong_report_basis(self):
        c=case('UK_GAAP');c['classification']['reporting_basis']='Section1A';self.block(c)
    def test_malformed_inputs(self):
        for payload in (None,[],{},dict(assets='bad'),dict(framework='BAD')):
            self.assertEqual('blocked',assess_case(PACKAGE,payload)['status'])
    def test_public_routes_hide_internal_evidence(self):
        r=self.run_case(case());r['evidence'][0]['source_note']='Source: ChatGPT training data'
        r['facts_used']['secret_review']='internal-reviewer-name'
        for route in ROUTES:
            text=json.dumps(to_public(r,route),default=serializable)
            for token in ('Source:','approval_track','evidence_status','audit_required','internal-reviewer-name','sha256','case_fingerprint'):
                self.assertNotIn(token,text)
            self.assertIn('Post-harvest',text)

if __name__=='__main__':unittest.main()

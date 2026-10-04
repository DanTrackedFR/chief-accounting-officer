"""Independent adversarial specialist QA: fresh quantities, money and edge cases.
Fixtures are synthetic; refreshed review is a test-only approval simulation.
"""
import copy
import json
import unittest
from unittest.mock import patch
from decimal import Decimal
from agriculture_cases import case, ready, refresh, sources, content, row, document, disclosure_support, PACKAGE
from production import assess_case, to_public, serializable, execute, case_fingerprint
from interfaces.public_output import ROUTES

MONEY={'amount','opening_value','purchase_cost','carrying_value','fair_value','costs_to_sell','net_value','cost','opening','closing','statement','inventory_entry_value','closing_carrying_value','pnl_measurement_gain','harvest_entry'}
def specimen(fw='IFRS',kind='livestock'):
    c=case(fw,kind)
    def scale(o):
        if isinstance(o,dict):
            for k,v in list(o.items()):
                if k in MONEY and isinstance(v,str):o[k]=str(Decimal(v)*Decimal('3.7'))
                elif k=='quantity' and isinstance(v,str):o[k]='2'
                elif k=='harvest_quantity' and isinstance(v,str):o[k]='83'
                else:scale(v)
        elif isinstance(o,list):
            for v in o:scale(v)
    scale(c)
    c['case_id']='Independent synthetic '+fw+' agricultural 3.7 money / two-unit cohorts'
    return refresh(sources(disclosure_support(c)))

def birth_case(fw='IFRS'):
    c=specimen(fw);a=c['assets'][2];a['state']='birth';a['purchase_cost']='0';a['birth_doc']='birth-source'
    document(c,'birth-source',dict(asset_id=a['id'],physical_id=a['physical_id'],date=a['recognition_date'],quantity='2',kind='birth',event_source_id='independent-birth-29',control_supported=True,evidence_memo='Independent synthetic witnessed birth source'))
    c['gl'][1].update(closing='1000',statement='1000')
    # Fixture opening Cash was scaled to3700; restore to its independent opening.
    c['gl'][1].update(closing=c['gl'][1]['opening'],statement=c['gl'][1]['opening'])
    c['gl'][2].update(closing='-481',statement='-481');c['disclosures']['pnl_measurement_gain']='481'
    return refresh(sources(disclosure_support(c)))

def death_case():
    c=specimen();m=c['movements'][0];m.update(kind='death',death_doc='death-source')
    document(c,'death-source',dict(asset_id=m['asset_id'],date=m['date'],quantity='2',recoveries='0',zero_salvage=True))
    c['gl']=[g for g in c['gl'] if g['id']!='Harvest inventory entry'];c['gl_inventory']=[g['id'] for g in c['gl']]
    c['gl'].append(row(c,'Agriculture mortality loss',currency='USD',opening='0',closing='185',statement='185'));c['gl_inventory'].append('Agriculture mortality loss')
    c['gl'][2].update(closing='-185',statement='-185');c['disclosures'].update(pnl_measurement_gain='185',harvest_entry='0')
    return refresh(sources(disclosure_support(c)))

def negative_gain_case():
    c=specimen();a=c['assets'][0];a['amount']='74';c['closing_population'][0]['carrying_value']='74'
    v=content(c,'live-closing');v.update(fair_value='92.5',net_value='74')
    c['gl'][0].update(closing='370',statement='370');c['gl'][2].update(closing='148',statement='148')
    c['disclosures'].update(closing_carrying_value='370',pnl_measurement_gain='-148')
    return refresh(sources(disclosure_support(c)))

class IndependentAgriculture(unittest.TestCase):
    def result(self,c,recertify=True):
        return assess_case(PACKAGE,ready(c=c,release=True) if recertify else c)
    def blocked(self,c):
        r=self.result(c);self.assertEqual('blocked',r['status'],r['conclusion'])
    def complete(self,c):
        r=self.result(c);self.assertEqual('complete',r['status'],r['conclusion']);return r
    def test_valid_fresh_three_frameworks(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            r=self.complete(specimen(fw));self.assertEqual(Decimal('777'),r['calculations']['closing']);self.assertEqual(Decimal('259'),r['calculations']['measurement_gain'])
    def test_valid_birth_not_purchase_and_balanced(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            r=self.complete(birth_case(fw));self.assertEqual(Decimal('481'),r['calculations']['measurement_gain']);self.assertEqual(2,r['calculations']['quantity_bridge']['births'])
            for j in r['journal_entry_implications']:
                self.assertEqual(sum(x['amount'] for x in j if x['side']=='Dr'),sum(x['amount'] for x in j if x['side']=='Cr'))
    def test_valid_mortality_without_fabricated_growth(self):
        r=self.complete(death_case());self.assertEqual(Decimal('185'),r['calculations']['mortality_loss']);self.assertEqual(0,r['calculations']['harvest_entry'])
    def test_valid_negative_gain(self):
        r=self.complete(negative_gain_case());self.assertEqual(Decimal('-148'),r['calculations']['measurement_gain'])
    def test_valid_no_transaction_classification(self):
        c=specimen();c['requested_action']='classification';c['movements']=[];c['gl']=[];c['gl_inventory']=[];self.complete(sources(c))
    def test_valid_ifrs_bearer_animal_not_ppe(self):
        c=specimen();c['assets'][0]['category']='bearer_livestock';content(c,'live-class')['category']='bearer_livestock';content(c,'live-closing')['category']='bearer_livestock';c['accounting_policy']['class_models']['bearer_livestock']='fair_value_less_costs_to_sell';self.complete(sources(disclosure_support(c)))
    def test_valid_uk_bearer_plant_fv_election_not_ifrs(self):
        c=specimen('UK_GAAP');c['assets'][0]['category']='bearer_plant';content(c,'live-class')['category']='bearer_plant';content(c,'live-closing')['category']='bearer_plant';c['accounting_policy']['class_models']['bearer_plant']='fair_value_less_costs_to_sell';self.complete(sources(disclosure_support(c)))
    def test_iqa01_birth_missing_event_source(self):
        c=birth_case();c['assets'][2].pop('birth_doc');self.blocked(sources(c))
    def test_iqa01_birth_event_wrong_quantity(self):
        c=birth_case();content(c,'birth-source')['quantity']='3';self.blocked(c)
    def test_iqa01_birth_event_wrong_date(self):
        c=birth_case();content(c,'birth-source')['date']='2026-05-01';self.blocked(c)
    def test_iqa01_birth_event_wrong_identity(self):
        c=birth_case();content(c,'birth-source')['physical_id']='physical-live';self.blocked(c)
    def test_iqa02_excluded_costs_explicit_contradiction(self):
        for kind in ('income_tax','financing','transport_already_in_fair_value'):
            c=specimen();content(c,'live-closing')['cost_components']=[dict(kind=kind,amount='18.5')];self.blocked(c)
    def test_iqa03_empty_disclosure_support(self):
        c=specimen();c['disclosures']['requirements'][0]['evidence_memo']='';content(c,'requirements')[0]['evidence_memo']='';self.blocked(c)
    def test_iqa04_quantity_unit_public_leak(self):
        c=specimen()
        for a in c['assets']:a['quantity_unit']='Private reviewer Jane Smith'
        self.blocked(sources(c))
    def test_iqa04_produce_unit_public_leak(self):
        c=specimen();content(c,'harvest-record')['produce_unit']='Private reviewer Jane Smith';self.blocked(c)
    def test_iqa05_explicit_superseded_edition(self):
        c=specimen('UK_GAAP');c['uk_standard_edition']='2015';c['applicability_review']['standard_versions']=['FRS 102 September2015'];self.blocked(c)
        c=specimen('AASB');c['aasb_compilation']='superseded1998';c['applicability_review']['standard_versions']=['AASB141 1998'];self.blocked(c)
    def test_iqa05_independent_edition_source_conflict(self):
        for k,v in [('operative_edition','superseded2015'),('framework','US_GAAP'),('entity','Other farm'),('effective_period',['2025-01-01','2025-12-31'])]:
            c=specimen('UK_GAAP');content(c,'edition-source')[k]=v;self.blocked(c)
    def test_iqa06_class_policy_missing_or_mixed(self):
        c=specimen('UK_GAAP');c['accounting_policy']['class_models']={};self.blocked(c)
        c=specimen('UK_GAAP');c['accounting_policy']['class_models']['consumable_livestock']='cost';self.blocked(c)
    def test_iqa06_class_policy_contradiction(self):
        c=specimen('UK_GAAP');content(c,'live-class')['agriculture_model']='cost';self.blocked(c)
    def test_iqa03_support_source_wrong_current_entity(self):
        for k,v in [('entity','Other farm'),('framework','US_GAAP'),('checked_on','2025-12-31'),('support_memo','')]:
            c=specimen();content(c,'gain_loss-support')[k]=v;self.blocked(c)
    def test_iqa02_selling_cost_component_amount_and_exclusions(self):
        c=specimen();content(c,'live-closing')['cost_components'][0]['amount']='17.5';self.blocked(c)
        for k in ('finance_or_income_tax_included','transport_deducted_again','other_uncertain_costs'):
            c=specimen();content(c,'live-closing')[k]=True;self.blocked(c)
    def test_stale_original_doc_hash_after_review(self):
        c=ready(c=specimen());content(c,'live-closing')['fair_value']='999999';self.assertEqual('blocked',self.result(c,False)['status'])
    def test_stale_knowledge_document_hash(self):
        c=ready(c=specimen());c['knowledge_review']['documents'][0]['sha256']='0'*64;self.assertEqual('blocked',self.result(c,False)['status'])
    def test_sales_recoveries_and_price_bridge_are_excluded(self):
        c=specimen();c['movements'][0]['kind']='sale';self.blocked(sources(c))
        c=death_case();content(c,'death-source')['recoveries']='12';self.blocked(c)
        c=specimen();c['disclosures']['price_change']='14';self.blocked(c)
    def test_inventory_ppe_and_unmanaged_source_classification(self):
        for route in ('inventory','fixed-assets','land','intangible','outside_scope'):
            c=specimen();content(c,'live-class')['route']=route;self.blocked(c)
        c=specimen();content(c,'live-class')['agricultural_activity']=False;self.blocked(c)
    def test_us_models_are_not_invented(self):
        for category in ('consumable_crop','bearer_livestock','bearer_plant'):
            c=specimen('US_GAAP');c['assets'][0]['category']=category;content(c,'live-class')['category']=category;self.blocked(sources(c))
    def test_uk_cost_and_ifrs_bearer_plant_excluded(self):
        c=specimen('UK_GAAP');c['accounting_policy']['agriculture_model']='cost';self.blocked(c)
        for fw in ('IFRS','AASB'):
            c=specimen(fw);c['assets'][0]['category']='bearer_plant';content(c,'live-class')['category']='bearer_plant';self.blocked(sources(c))
    def test_uk_produce_separation_excluded(self):
        c=specimen('UK_GAAP');c['assets'][0]['category']='growing_produce';content(c,'live-class')['category']='growing_produce';self.blocked(sources(c))
    def test_terminal_event_alias_distinct_register_ids(self):
        c=specimen();m=copy.deepcopy(c['movements'][0]);m.update(id='death-alias',kind='death',asset_id='live');c['movements'].append(m);self.blocked(sources(c))
    def test_terminal_quantity_and_closed_population(self):
        for quantity in ('1','3','-2'):
            c=specimen();c['movements'][0]['quantity']=quantity;self.blocked(sources(c))
        c=death_case();c['closing_population'].append(copy.deepcopy(c['opening_population'][1]));self.blocked(sources(c))
    def test_duplicate_purchase_physical_alias(self):
        c=specimen();c['assets'][2]['physical_id']='physical-live';content(c,'purchase-control')['physical_id']='physical-live';c['closing_population'][1]['physical_id']='physical-live';self.blocked(sources(c))
    def test_birth_as_opening_double_count(self):
        c=birth_case();c['opening_population'].append(row(c,'purchase',physical_id='physical-purchase',quantity='2',carrying_value='0'));self.blocked(sources(c))
    def test_opening_and_closing_missing_source(self):
        for key in ('opening_population','closing_population'):
            c=specimen();c[key].pop(0);self.blocked(sources(c))
    def test_gl_and_quantity_contradictions(self):
        for change in ('opening_gl','closing_gl','physical_qty','valuation_qty'):
            c=specimen()
            if change=='opening_gl':c['gl'][0]['opening']='555.02'
            elif change=='closing_gl':c['gl'][0]['closing']='777.02'
            elif change=='physical_qty':c['closing_population'][0]['quantity']='4';sources(c)
            else:content(c,'live-closing')['quantity']='4'
            self.blocked(c)
    def test_harvest_not_double_counted_or_downstream_costed(self):
        c=specimen();m=copy.deepcopy(c['movements'][0]);m['id']='alias';m['event_source_id']='new-alias';c['movements'].append(m);self.blocked(sources(c))
        c=specimen();content(c,'harvest-record')['boundary_only']=False;self.blocked(c)
        c=specimen();content(c,'harvest-record')['entire_asset_harvested']=False;self.blocked(c)
    def test_missing_source_records_and_documents(self):
        c=specimen();c['movement_source']['records']=[];self.blocked(c)
        c=specimen();c['documents']=[d for d in c['documents'] if d['id']!='purchase-initial'];c['document_inventory']=[d['id'] for d in c['documents']];self.blocked(c)
    def test_unsupported_valuation_and_legal_assertions(self):
        for key in ('qualified_valuer','qualification_memo','independence_memo','market_evidence'):
            c=specimen();content(c,'live-closing')[key]='';self.blocked(c)
        c=specimen();content(c,'live-control')['rights_memo']='';self.blocked(c)
        c=specimen();content(c,'live-control')['probable_benefits']=False;self.blocked(c)
    def test_valuation_date_signed_staleness(self):
        for key,val in (('measurement_date','2026-09-30'),('signed_on','2025-12-31'),('current_market_evidence',False),('reliable_measurement',False),('category','consumable_crop'),('asset_id','purchase')):
            c=specimen();content(c,'live-closing')[key]=val;self.blocked(c)
    def test_initial_recognition_date_cannot_be_harvest_date(self):
        c=specimen();c['assets'][2]['recognition_date']='2026-09-30';self.blocked(sources(c))
    def test_sign_oci_equity_and_physical_split(self):
        for presentation in ('OCI','equity'):
            c=specimen();c['disclosures']['presentation']=presentation;self.blocked(c)
        c=specimen();c['gl'][2].update(closing='259',statement='259');self.blocked(c)
        c=specimen();c['disclosures']['physical_change']='259';self.blocked(c)
    def test_multicurrency_and_units(self):
        c=specimen();c['assets'][2]['currency']='EUR';self.blocked(sources(c))
        c=specimen();c['gl'][1]['currency']='EUR';self.blocked(c)
        c=specimen();c['assets'][2]['quantity_unit']='kg';self.blocked(sources(c))
    def test_dependencies_and_owner_contradictions(self):
        for flag in ('government_assistance','fx','valuation_requested','post_harvest_accounting','external_posting','unsupported_contract_rights'):
            c=specimen();c['classification'][flag]=True;self.blocked(c)
        c=specimen();content(c,'live-closing')['owner_import']='invented-valuation-result';self.blocked(c)
        for package in ('fixed-assets','inventory-cost','fair-value-measurement','government-grants'):
            c=specimen();c['imports']=[row(c,'unbound-owner',package=package,case={},result={},mode='evidence_only')];self.blocked(c)
    def test_disclosure_population_complete_and_current(self):
        c=specimen();c['disclosures']['checked_on']='2026-01-01';self.blocked(c)
        c=specimen();c['disclosures']['requirements'].pop();content(c,'requirements').pop();c['disclosures']['requirement_inventory'].pop();self.blocked(c)
        c=specimen();c['disclosures']['pnl_measurement_gain']='-259';self.blocked(c)
    def test_framework_and_period_contamination(self):
        c=specimen();c['classification']['framework']='UK_GAAP';self.blocked(c)
        c=specimen();content(c,'live-control')['framework']='AASB';self.blocked(c)
        c=specimen('AASB');c['classification']['reporting_basis']='Tier2';self.blocked(c)
        c=specimen();c['classification']['early_presentation_adoption']=True;self.blocked(c)
        c=specimen();c['reporting_period']='2027-12-31';self.blocked(c)
    def test_stale_knowledge_selected_claims_and_releases(self):
        for key in ('documents','claim_ids','applied_claim_ids'):
            c=ready(c=specimen());c['knowledge_review'][key]=[];self.assertEqual('blocked',self.result(c,False)['status'])
        c=ready(c=specimen());c['release_review']['payload_fingerprint']='0'*64;self.assertEqual('blocked',self.result(c,False)['status'])
    def test_stale_case_and_implementation_certification(self):
        c=ready(c=specimen());c['reviewer_signoff']['case_fingerprint']='old';self.assertEqual('partial',self.result(c,False)['status'])
        c=ready(c=specimen())
        with patch('production.case_fingerprint',return_value='changed-executable-fingerprint'):
            self.assertEqual('partial',self.result(c,False)['status'])
    def test_public_internal_source_provenance_hidden_all_routes(self):
        r=self.complete(specimen());r['facts_used']['reviewer']='PRIVATE_REVIEWER_921';r['evidence'][0].update(source_note='Source: ChatGPT training data',approval_track='TRAINING_DATA_CHECKED',approval_review=dict(reviewer='PRIVATE_REVIEWER_921'))
        for route in ROUTES:
            text=json.dumps(to_public(r,route),default=serializable)
            for secret in ('PRIVATE_REVIEWER_921','Source:','approval_track','source_note','sha256','case_fingerprint','evidence_status','audit_required'):
                self.assertNotIn(secret,text)
            self.assertIn('Post-harvest',text)
    def test_malformed_nonfinite_float_and_boolean(self):
        for v in ('NaN','Infinity',True,3.7,None,{},[]):
            c=specimen();c['assets'][0]['quantity']=v;self.blocked(sources(c))
        for payload in (None,[],{},dict(framework='invented')):self.assertEqual('blocked',assess_case(PACKAGE,payload)['status'])

if __name__=='__main__':unittest.main()

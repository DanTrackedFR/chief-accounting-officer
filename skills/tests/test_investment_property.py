"""Author contracts for the ordinary governed runtime, not independent QA."""
import copy
import json
from decimal import Decimal
from pathlib import Path
import unittest

from investment_property_cases import case,ready,capture
from production import assess_case,to_public,case_fingerprint
from core_accounting import balance

def execute(c):return assess_case('investment-property',ready(c=c))

class InvestmentPropertyAuthorTests(unittest.TestCase):
 def blocked(self,c,recapture=True):
  if recapture:capture(c)
  result=execute(c)
  self.assertEqual('blocked',result['status'],result)
  self.assertEqual([],result['journal_entry_implications'])
  return result
 def test_initial_purchase_math_all_frameworks(self):
  for fw,model in [('IFRS','cost'),('AASB','cost'),('UK_GAAP','fair_value'),('US_GAAP','cost')]:
   with self.subTest(framework=fw):
    r=execute(case(fw,model,'initial'));self.assertEqual('complete',r['status'],r['open_items'])
    self.assertEqual(Decimal('600000'),r['calculations']['additions'])
    self.assertEqual(Decimal('650000' if model=='fair_value' else '600000'),r['calculations']['closing_carrying'])
    for e in r['journal_entry_implications']:balance(e)
 def test_fair_value_math_all_permitted_frameworks(self):
  for fw in ['IFRS','AASB','UK_GAAP']:
   r=execute(case(fw));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('50000'),r['calculations']['fair_value_movement']);self.assertEqual(1,len(r['journal_entry_implications']))
 def test_initial_acquisition_nature_requires_cash_purchase(self):
  for nature in [None,'nonexchange_gift','noncash_exchange','nominal_transfer']:
   c=case('US_GAAP','cost','initial')
   if nature is None:del c['events'][0]['acquisition_nature']
   else:c['events'][0]['acquisition_nature']=nature
   self.blocked(c)
 def test_initial_gift_qualification_required(self):
  for gifted in [None,True]:
   c=case('US_GAAP','cost','initial')
   if gifted is None:del c['properties'][0]['gifted']
   else:c['properties'][0]['gifted']=gifted
   self.blocked(c)
 def test_initial_zero_price_fee_only_coherent_sources_blocked(self):
  c=case('US_GAAP','cost','initial');e=c['events'][0];p=c['properties'][0]
  e['cost_items'][0]['amount']='0';e['purchase_cost']='10000'
  p['gross_cost']=p['closing_carrying']=c['controls']['population_amount']='10000'
  c['disclosure_review']['amounts']['additions']=c['disclosure_review']['amounts']['closing_carrying']='10000'
  for row in c['gl']:
   if row['id']=='Cash':row['closing']=row['statement']='990000'
   elif row['id']=='Property plant and equipment':row['closing']=row['statement']='10000'
  self.blocked(c)
 def test_cost_owner_evidence_no_duplicate_depreciation(self):
  for fw,model in [('IFRS','cost'),('AASB','cost'),('UK_GAAP','group_cost'),('US_GAAP','cost')]:
   r=execute(case(fw,model));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('20000'),r['calculations']['depreciation_owned_elsewhere']);self.assertEqual(Decimal('580000'),r['calculations']['closing_carrying']);self.assertEqual([],r['journal_entry_implications'])
 def test_fv_disposal_reconciles_period_gain_and_net_proceeds(self):
  r=execute(case('IFRS','fair_value','disposal'));self.assertEqual('complete',r['status']);s=r['calculations']
  self.assertEqual((Decimal('50000'),Decimal('40000'),Decimal('690000'),Decimal('0')),(s['fair_value_movement'],s['disposal_gain'],s['net_proceeds'],s['closing_carrying']))
  for e in r['journal_entry_implications']:balance(e)
 def test_us_cost_disposal_no_invented_fv(self):
  r=execute(case('US_GAAP','cost','disposal'));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('110000'),r['calculations']['disposal_gain']);self.assertEqual(Decimal('0'),r['calculations']['fair_value_movement'])
 def test_supported_cost_and_fv_transfers(self):
  for fw in ['IFRS','AASB']:
   for route,model,amount in [('transfer_in_cost','cost','580000'),('transfer_out_cost','cost','-580000'),('transfer_out_fv','fair_value','-650000')]:
    r=execute(case(fw,model,route));self.assertEqual('complete',r['status'],r['open_items']);self.assertEqual(Decimal(amount),r['calculations']['transfers'])
    s=r['calculations'];self.assertEqual(s['closing_carrying'],s['opening_carrying']+s['additions']-s['depreciation_owned_elsewhere']-s['impairment_owned_elsewhere']+s['fair_value_movement']+s['transfers']-s['disposal_carrying'])
 def test_separable_mixed_use_all_frameworks(self):
  for fw,model in [('IFRS','fair_value'),('AASB','fair_value'),('UK_GAAP','fair_value'),('US_GAAP','cost')]:
   r=execute(case(fw,model,mixed='separable'));self.assertEqual('complete',r['status'])
 def test_inseparable_mixed_use_ifrs_aasb_only(self):
  for fw in ['IFRS','AASB']:self.assertEqual('complete',execute(case(fw,mixed='inseparable'))['status'])
  for fw,model in [('UK_GAAP','fair_value'),('US_GAAP','cost')]:self.blocked(case(fw,model,mixed='inseparable'))
 def test_us_fv_route_blocked(self):self.blocked(case('US_GAAP','fair_value'))
 def test_uk_deleted_cost_exception_blocked(self):self.blocked(case('UK_GAAP','cost'))
 def test_tier2_blocked(self):
  c=case('AASB');c['reporting_tier']=2;self.blocked(c)
 def test_incorrect_policy_change_blocked(self):
  c=case();c['accounting_policy']['policy_change']=True;self.blocked(c)
 def test_early_presentation_adoption_blocked(self):
  c=case();c['accounting_policy']['early_adoption']=True;self.blocked(c)
 def test_wrong_edition_blocked(self):
  c=case();c['applicability_review']['standard_versions']=['IAS40_2025'];self.blocked(c)
 def test_source_dimension_contamination_blocked(self):
  for field,value in [('legal_entity','Other'),('currency','USD'),('framework','US_GAAP'),('period',['2025-01-01','2025-12-31']),('asset_id','wrong')]:
   c=case();c['valuation'][field]=value;self.blocked(c)
 def test_missing_original_source_capture_blocked(self):
  c=case();del c['original_source_snapshot'];self.blocked(c,False)
 def test_fresh_case_review_does_not_override_snapshot(self):
  c=case();c['valuation']['amount']='999999';self.blocked(c,False)
 def test_wrong_value_method_date_and_price_basis(self):
  for key,value in [('valuation_date','2025-12-31'),('basis','asking_price'),('reliable',False),('material_unresolved_uncertainty',True),('transaction_costs_deducted',True),('valuation_method','invented')]:
   c=case();c['valuation'][key]=value;self.blocked(c)
 def test_fv_change_double_ownership_blocked(self):
  c=case();c['valuation']['recognized_by_other_owner']=True;self.blocked(c)
 def test_disposal_stale_value_blocked(self):
  c=case('IFRS','fair_value','disposal');c['valuation']['valuation_date']='2026-06-30';self.blocked(c)
 def test_duplicate_property_identity_blocked(self):
  c=case();q=copy.deepcopy(c['properties'][0]);q['id']='shadow';c['properties'].append(q);c['source_inventory'].append('shadow');self.blocked(c)
 def test_duplicate_journal_ownership_blocked(self):
  c=case();r=copy.deepcopy(c['ownership_register'][0]);r['id']='duplicate';c['ownership_register'].append(r);c['ownership_inventory'].append('duplicate');self.blocked(c)
 def test_independent_depreciation_reperformance(self):
  c=case('IFRS','cost');c['cost_owner']['depreciation']='10000';self.blocked(c)
 def test_missing_impairment_owner_blocked(self):
  c=case('IFRS','cost');c['impairment_owner']=None;self.blocked(c)
 def test_gl_offset_and_rollforward_reconcile(self):
  for part in ['gl','disclosure']:
   c=case()
   if part=='gl':c['gl'][1]['closing']='-40000'
   else:c['disclosure_review']['amounts']['closing_carrying']='640000'
   self.blocked(c)
 def test_material_scope_flags_fail_closed(self):
  for k in ['right_of_use','finance_lessor','business_combination','construction','inventory','held_for_sale','sale_leaseback','complex_consideration','foreign_operation','significant_services']:
   c=case();c['properties'][0][k]=True;self.blocked(c)
 def test_wrong_transfer_use_evidence(self):
  c=case('IFRS','cost','transfer_in_cost');c['events'][0]['actual_change_of_use']=False;self.blocked(c)
 def test_unsupported_uk_and_us_transfer_models(self):
  self.blocked(case('UK_GAAP','fair_value','transfer_out_fv'));self.blocked(case('US_GAAP','cost','transfer_in_cost'))
 def test_missing_signoff_partial_no_released_journals(self):
  c=ready();del c['reviewer_signoff'];r=assess_case('investment-property',c);self.assertEqual('partial',r['status']);self.assertEqual([],r['journal_entry_implications']);self.assertTrue(r['proposed_journal_workpaper'])
 def test_citation_subset_cannot_omit_method_authority(self):
  c=ready();c['knowledge_review']['applied_claim_ids']=c['knowledge_review']['applied_claim_ids'][:1];c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
  self.assertEqual('blocked',assess_case('investment-property',c)['status'])
 def test_stale_case_review_partial(self):
  c=ready();c['judgment_memo']+=' Revised';r=assess_case('investment-property',c);self.assertEqual('partial',r['status']);self.assertEqual([],r['journal_entry_implications'])
 def test_public_routes_exclude_private_provenance(self):
  from interfaces.public_output import ROUTES
  r=execute(case())
  for route in ROUTES:
   rendered=json.dumps(to_public(r,route),default=str)
   for forbidden in ['original_source_snapshot','approval_review','reviewed_hash','case_fingerprint','synthetic independent reviewer','report_hash','Source: ChatGPT training data']:self.assertNotIn(forbidden,rendered)

if __name__=='__main__':unittest.main()

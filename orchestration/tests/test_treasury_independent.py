"""Independent attacks derived from raw evidence and native accounting contracts."""
import copy
import unittest
from dataclasses import replace
from orchestration.tests.treasury_fixtures import flagship,sources,proposal,reviewed_pack,OBJECTIVE,SCOPE,owners
from orchestration.intake import Intake,FixturePlanner
from orchestration.runtime import CAO,Case,Graph,Node,digest
from orchestration.registry import production
from orchestration.planning import FACT_ADAPTERS
from additional_cases import certify
from hedge_cases import ready as hedge_ready,sources as hedge_sources

class IndependentTreasuryAcceptance(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.native=owners(); e,p,k=flagship(clean=True);cls.clean=e.execute(p,k)
 def reject_native(self,pkg,change):
  c=copy.deepcopy(self.native[pkg]);change(c)
  try:
   c=hedge_ready(hedge_sources(c)) if pkg=='derivatives-hedge-accounting' else certify(pkg,c)
   result=production.assess_case(pkg,c)
  except (ValueError,KeyError,AssertionError):return
  self.assertNotEqual(result.get('status'),'complete',str(result.get('calculations')))
 def reject_source(self,id,old,new):
  raw=[replace(r,payload=r.payload.replace(old,new)) if r.id==id else r for r in sources(True)]
  self.assertNotEqual(next(r.payload for r in raw if r.id==id),next(r.payload for r in sources(True) if r.id==id))
  try:
   e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(OBJECTIVE,raw,[],SCOPE);r=e.execute(p,reviewed_pack(p))
  except (ValueError,KeyError):return
  self.assertNotEqual(r.case.outcome,'complete','Contradictory '+id+' source silently ignored')
 def test_clean_and_material_conflict_outcomes(self):
  self.assertEqual(self.clean.case.outcome,'complete');e,p,k=flagship();r=e.execute(p,k)
  self.assertNotEqual(r.case.outcome,'complete');self.assertTrue(r.conflicts)
 def test_lender_statement_disagrees_with_register(self):self.reject_source('lender',',800,USD,800',',900,USD,900')
 def test_external_valuation_rollforward_contradiction(self):self.reject_source('valuation',',0,40,0,40',',0,50,0,40')
 def test_bank_classification_conflicts_with_elected_policy(self):self.reject_source('bank','-80,interest_paid,operating','-80,interest_paid,financing')
 def test_draw_and_fee_source_omission(self):self.reject_source('debt',',0,0,0.08',',100,20,0.08')
 def test_effectiveness_reserve_source_contradiction(self):self.reject_source('effectiveness',',0,36,4,36',',0,20,20,20')
 def test_remaining_contractual_cashflows_omission(self):self.reject_source('payments','2027-12-31,864,800','2027-12-31,964,900')
 def test_contract_notional_source_contradiction(self):self.reject_source('derivative','forward1,800,','forward1,900,')
 def test_designated_quantity_source_contradiction(self):self.reject_source('designation',',800,benchmark_interest',',900,benchmark_interest')
 def test_original_foreign_currency_preserved(self):self.reject_source('lender',',USD,',',GBP,')
 def test_no_template_commodity_designation_evidence(self):
  r=self.native['derivatives-hedge-accounting']['relationships'][0]
  text=' '.join(str(r[k]).lower() for k in ('item_eligibility_memo','risk_component_memo','forecast_memo'))
  self.assertNotIn('commodity',text);self.assertNotIn('purchase plan',text)
 def test_debt_opening_mismatch(self):self.reject_native('debt-financing',lambda c:c['debt'][0].update(opening_carrying='1100'))
 def test_debt_principal_duplication(self):self.reject_native('debt-financing',lambda c:c['debt'].append(copy.deepcopy(c['debt'][0])))
 def test_debt_repayment_duplication(self):self.reject_native('debt-financing',lambda c:c['debt'][0]['schedule'].append(copy.deepcopy(c['debt'][0]['schedule'][0])))
 def test_nominal_coupon_substitution(self):self.reject_native('debt-financing',lambda c:c['debt'][0]['schedule'][0].update(expected_interest='60'))
 def test_unsupported_fee(self):self.reject_native('debt-financing',lambda c:c['debt'][0].update(eligible_cost='20',directly_attributable=False))
 def test_rights_not_inferred_from_maturity(self):self.reject_native('debt-financing',lambda c:c['debt'][0].update(rights_at_reporting_date=False))
 def test_maturity_conflicts_with_contractual_payments(self):self.reject_native('debt-financing',lambda c:c['debt'][0]['maturities'][0].update(date='2028-12-31'))
 def test_modification_cannot_use_old_yield(self):self.reject_native('debt-financing',lambda c:c['debt'][0].update(modified=True))
 def test_fx_original_population_change(self):self.reject_native('foreign-currency',lambda c:c['items'][0].update(foreign_amount='1100'))
 def test_fx_settlement_rate_source_must_bind(self):self.reject_source('fx',',200,1,880,',',200,1.2,880,')
 def test_valuation_wrong_dimensions(self):
  for key,value in [('entity','Other'),('currency','USD'),('measurement_date','2026-11-30'),('notional','900')]:
   with self.subTest(key=key):self.reject_native('derivatives-hedge-accounting',lambda c:c['valuations'][0].update({key:value}))
 def test_missing_qualified_valuation(self):self.reject_native('derivatives-hedge-accounting',lambda c:c.update(valuations=[]))
 def test_hedge_wrong_item(self):self.reject_native('derivatives-hedge-accounting',lambda c:c['relationships'][0].update(hedged_item_id='other-loan'))
 def test_hedge_notional_mismatch(self):self.reject_native('derivatives-hedge-accounting',lambda c:c['relationships'][0].update(actual_item_quantity='900'))
 def test_hedge_unsupported_effectiveness(self):self.reject_native('derivatives-hedge-accounting',lambda c:c['relationships'][0].update(effectiveness_method='economic_intuition'))
 def test_hedge_risk_currency_mismatch(self):self.reject_native('derivatives-hedge-accounting',lambda c:c['relationships'][0]['risk_measurement'].update(currency='USD'))
 def test_hedge_reserve_mismatch(self):self.reject_native('derivatives-hedge-accounting',lambda c:c['relationships'][0].update(opening_reserve='10'))
 def test_cash_opening_closing_reconciliation(self):self.reject_native('cash-flow-reporting',lambda c:c['statement'].update(closing='1800'))
 def test_cash_principal_omission(self):self.reject_native('cash-flow-reporting',lambda c:c['transactions'].pop())
 def test_non_cash_fx_as_cash(self):self.reject_native('cash-flow-reporting',lambda c:c['transactions'].append(dict(c['transactions'][0],id='fx-cash',bank_id='fx-cash',source_id='fx-cash',amount='-80',kind='fx')))
 def test_derivative_fv_as_bank_cash(self):self.reject_native('cash-flow-reporting',lambda c:c['transactions'].append(dict(c['transactions'][0],id='fv-cash',bank_id='fv-cash',source_id='fv-cash',amount='40')))
 def test_duplicate_cash_interest(self):self.reject_native('cash-flow-reporting',lambda c:c['transactions'].append(copy.deepcopy(c['transactions'][0])))
 def test_reconciliation_residual(self):self.reject_native('balance-sheet-reconciliations',lambda c:c['reconciliations'][0].update(source_closing='1800'))
 def test_required_reporting_handoff_cannot_disappear(self):
  e,p,k=flagship(clean=True);k.request['handoffs']=[h for h in k.request['handoffs'] if h['semantic']!='hedge_oci']
  try:r=e.execute(p,k)
  except ValueError:return
  self.assertNotEqual(r.case.outcome,'complete')
 def test_aliases_cannot_consume_native_journal_atoms_twice(self):
  j=[dict(side='Dr',account='Debt A',amount='200'),dict(side='Cr',account='Bank A',amount='200')]
  native=[dict(owner='debt-financing',journals=[j])];events=[dict(economic_id=id,primary=[dict(owner='debt-financing',index=0)],witnesses=[],evidence='BANK-PRINCIPAL') for id in ('principal','relabelled')]
  with self.assertRaises(ValueError):CAO._qualified_journals(native,{'Debt A':'Debt','Bank A':'Cash'},events)
 def test_selected_owners_exclude_irrelevant_packages(self):
  selected={r['selected_skill'] for r in self.clean.case.workplan_nodes}
  self.assertTrue({'debt-financing','foreign-currency','derivatives-hedge-accounting','cash-flow-reporting'}<=selected)
  self.assertFalse(selected & {'borrowing-costs','financial-instruments-ecl','fair-value-measurement','inventory-cost','revenue-recognition','insurance-contracts-accounting','consolidation'})
 def test_narrow_debt_and_fx_are_not_full_treasury(self):
  for owner,wanted in [('debt-financing',{'debt-financing'}),('foreign-currency',{'foreign-currency'})]:
   with self.subTest(owner=owner):
    e,p,k=flagship(clean=True,bounded=owner);r=e.execute(p,k);self.assertEqual({n['selected_skill'] for n in r.case.workplan_nodes},wanted)

 def test_bank_source_identity_cannot_change_with_nature_alias(self):
  j=[dict(side='Dr',account='Debt',amount='200'),dict(side='Cr',account='Cash',amount='200')];g=Graph();span=[SCOPE['period_start'],SCOPE['reporting_period']]
  for pkg in ('debt-financing','foreign-currency','financial-statements'):
   n=Node(pkg,'review',pkg,'',SCOPE['entity'],'IFRS',span);n.status='complete';n.result=dict(case_fingerprint=pkg,journal_entry_implications=[] if pkg=='financial-statements' else [copy.deepcopy(j)]);g.add(n)
  fs=dict(functional_currency='EUR',currency='EUR',current_tb=[dict(id='Debt',balance='400'),dict(id='Cash',balance='-400')],comparative_tb=[dict(id='Debt',balance='0'),dict(id='Cash',balance='0')])
  req=dict(journal_account_mapping={},journal_ownership=[dict(economic_id=p,primary=[dict(owner=p,index=0)],witnesses=[],evidence='Same original bank payment') for p in ('debt-financing','foreign-currency')])
  req['journal_event_sources']=[dict(economic_id=p,entity=SCOPE['entity'],period=span,currency='EUR',origin='bank',record='BANK-PRINCIPAL',nature=p+'-alias') for p in ('debt-financing','foreign-currency')]
  native=[dict(owner=n.selected_skill,case_fingerprint=n.result['case_fingerprint'],journals=n.result['journal_entry_implications']) for n in g.nodes.values()]
  req['journal_pack_review']=dict(approved=True,preparer='Synthetic preparer',reviewer='Synthetic independent reviewer',payload_fingerprint=digest(dict(mapping={},native_owner_journals=native,journal_ownership=req['journal_ownership'],journal_event_sources=req['journal_event_sources'])))
  c=Case('independent-duplicate','Review',entities=[SCOPE['entity']],periods=span)
  with self.assertRaises(ValueError):CAO()._journal_mapping(c,g,{'financial-statements':fs},req,g.nodes['financial-statements'])
 def test_public_routes_hide_private_source_and_owner_metadata(self):
  import json
  for route in ('answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export'):
   with self.subTest(route=route):
    text=json.dumps(CAO().public(self.clean.case,route))
    for token in ('case_fingerprint','content_hash','qualified_reviewer','Synthetic independent','doc-valuation1','BANK-PRINCIPAL','journal_pack_review','debt-financing','relationship1'):
     self.assertNotIn(token,text)
 def test_source_qualification_tracks_prose_not_only_numbers(self):self.reject_source('terms','rights and covenant compliance','default and unresolved waiver')
 def test_qualified_external_valuation_dimension_metadata(self):
  raw=[replace(r,metadata=dict(r.metadata,entity='Other Entity')) if r.id=='valuation' else r for r in sources(True)]
  try:e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(OBJECTIVE,raw,[],SCOPE);r=e.execute(p,reviewed_pack(p))
  except ValueError:return
  self.assertNotEqual(r.case.outcome,'complete')
 def test_owner_import_result_cannot_be_stale(self):
  self.reject_native('derivatives-hedge-accounting',lambda c:c['imports'][0]['result']['calculations']['debt'][0].update(closing='900'))
 def test_designation_after_inception_cannot_receive_oci(self):
  self.reject_native('derivatives-hedge-accounting',lambda c:c['relationships'][0].update(designation_date='2026-02-01',documentation_date='2026-02-01'))
 def test_economic_hedge_without_designation_does_not_get_reserve(self):
  self.reject_native('derivatives-hedge-accounting',lambda c:c.update(relationships=[]))
 def test_analytics_residual_and_owner_identity(self):
  from governance_cases import refresh_release,ready
  for mutation in ('residual','owner','volume'):
   c=copy.deepcopy(self.native['management-accounting-analytics']);d=next(d for d in c['documents'] if d['id']=='interest-drivers');r=d['content']['records'][0]
   if mutation=='residual':r['current_amount']='90'
   elif mutation=='owner':r['current_owner']['result_path']=['debt',0,'repayments']
   else:r.update(q1='1100',p1='0.08')
   for document in c['documents']:document['content_hash']=digest(document['content'])
   with self.subTest(mutation=mutation):
    try:result=production.assess_case('management-accounting-analytics',ready('management-accounting-analytics',c=refresh_release(c)))
    except (ValueError,KeyError):continue
    self.assertNotEqual(result['status'],'complete')
 def test_interest_explanations_use_real_rate_quantity_math(self):
  r=next(n for n in self.clean.case.workplan_nodes if n['selected_skill']=='management-accounting-analytics')['result']['calculations']
  self.assertIn('diagnostic',r)
  text=str(r['diagnostic'])
  self.assertIn('20',text);self.assertIn('rate',text)
 def test_bank_event_origin_retag_fails_with_fresh_review(self):
  e,p,k=flagship(clean=True);req=k.request;source=next(s for s in req['journal_event_sources'] if s['record']=='BANK-PRINCIPAL');source.update(origin='debt',record='new-label',nature='adjustment')
  native=[]
  for issue in p.proposal['issues']:
   pkg=issue['value']['owner'];family=next(f for f,(owner,_) in FACT_ADAPTERS.items() if owner==pkg);result=production.assess_case(pkg,req['facts'][family])
   native.append(dict(owner=pkg,case_fingerprint=result['case_fingerprint'],journals=result['journal_entry_implications']))
  req['journal_pack_review']['payload_fingerprint']=digest(dict(mapping=req['journal_account_mapping'],native_owner_journals=native,journal_ownership=req['journal_ownership'],journal_event_sources=req['journal_event_sources']))
  try:r=e.execute(p,k)
  except ValueError:return
  self.assertNotEqual(r.case.outcome,'complete')
 def test_context_is_proposed_never_automatically_promoted(self):
  for candidate in self.clean.case.memory_candidates:self.assertNotIn(candidate.get('status'),('APPROVED','PROMOTED'))
 def native_category_ownership(self,pkg,c,index):
  result=production.assess_case(pkg,c);self.assertEqual(result['status'],'complete')
  journals=result['journal_entry_implications'];native=[dict(owner=pkg,journals=journals),dict(owner='cash-witness',journals=[copy.deepcopy(journals[index])])]
  events=[dict(economic_id='native-event-'+str(i),primary=[dict(owner=pkg,index=i)],witnesses=[[dict(owner='cash-witness',index=0)]] if i==index else [],evidence='Qualified original native category source') for i in range(len(journals))]
  out,ledger=CAO._qualified_journals(native,{},events);self.assertEqual(len(out),len(journals));self.assertEqual(len(ledger),len(events))
  for mutation in ('duplicate','amount','cash-account-alias'):
   altered=copy.deepcopy(events)
   if mutation=='duplicate':altered.append(dict(altered[index],economic_id='relabelled'))
   elif mutation=='amount':altered[index]['witnesses'][0][0].update(line=0,amount='1')
   else:altered.append(dict(altered[index],economic_id='account-alias',witnesses=[]))
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):CAO._qualified_journals(native,{'Cash':'Renamed cash'},altered)
  return result
 def test_native_funded_draw_ownership_and_alias_attacks(self):
  from financing_cases import ready as debt_ready
  result=self.native_category_ownership('debt-financing',debt_ready('debt-financing'),0)
  self.assertEqual(str(result['journal_entry_implications'][0][0]['amount']),'980.00')
  self.assertEqual(str(result['calculations']['debt'][0]['draws']),'1000')
  self.assertEqual(str(result['calculations']['debt'][0]['eligible_cost']),'20')
 def test_native_standalone_derivative_settlement_ownership_attacks(self):
  from hedge_cases import special_case
  result=self.native_category_ownership('derivatives-hedge-accounting',hedge_ready(special_case('swap-liability-settlement')),1)
  derivative=result['calculations']['derivatives'][0]
  self.assertEqual(str(derivative['opening']),'-80');self.assertEqual(str(derivative['change']),'-30');self.assertEqual(str(derivative['settlement']),'-40');self.assertEqual(str(derivative['closing']),'-70')
 def test_reporting_excludes_advanced_hedge_movement_scope(self):
  e,p,k=flagship(clean=True);original=next(h for h in k.request['handoffs'] if h['semantic']=='derivative_balance');family=next(f for f,(pkg,_) in FACT_ADAPTERS.items() if pkg=='derivatives-hedge-accounting')
  base=production.assess_case('derivatives-hedge-accounting',k.request['facts'][family])
  for field,value in [('route','standalone'),('opening','10'),('settlement','10'),('reserve_opening','10'),('reclassification','10'),('basis_adjustment','10')]:
   result=copy.deepcopy(base)
   if field in ('reserve_opening','reclassification','basis_adjustment'):result['calculations']['hedge_reserves'][0]['opening' if field=='reserve_opening' else field]=value
   else:result['calculations']['derivatives'][0][field]=value
   g=Graph();inputs={}
   for pkg in ('derivatives-hedge-accounting','financial-statements'):
    f=next(f for f,(owner,_) in FACT_ADAPTERS.items() if owner==pkg);inputs[pkg]=copy.deepcopy(k.request['facts'][f]);n=Node(pkg,'review',pkg,'',SCOPE['entity'],'IFRS',[SCOPE['period_start'],SCOPE['reporting_period']]);n.status='complete';n.result=result if pkg=='derivatives-hedge-accounting' else production.assess_case(pkg,inputs[pkg]);g.add(n)
   with self.subTest(field=field),self.assertRaisesRegex(ValueError,'(?i)(hedge|first.year|reporting|scope)'):CAO()._handoff(Case('independent-hedge-scope','Review'),g,inputs,original,set())

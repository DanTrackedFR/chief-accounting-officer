"""Fully synthetic documentary sources and approvals; independent arithmetic oracle."""
from copy import deepcopy
from decimal import Decimal
from cases import base,finalize
from operational_cases import approved
from reporting_cases import pol
from production import case_fingerprint
EDITIONS={'IFRS':'IAS40_2026','AASB':'AASB140_DEC2022','UK_GAAP':'FRS102_SEP2024_2026','US_GAAP':'ASC360_2026'}

def record(c,id,**kwargs):
 return approved(id,asset_id='property-001',legal_entity=c['entity'],framework=c['framework'],currency=c['functional_currency'],period=[c['period_start'],c['reporting_period']],document_id=id+'-document',**kwargs)

def capture(c):
 keys=['properties','accounting_policy','valuation','cost_owner','impairment_owner','events','gl','ownership_register','disclosure_review','functional_currency']
 c['original_source_snapshot']=approved('original-source-capture',capture_memo='Synthetic independently captured complete actual property sources; no live company facts',records=deepcopy({k:c[k] for k in keys}));return c

def case(fw='IFRS',model='fair_value',route='hold',mixed='none'):
 c=base('investment-property',fw);c.update(package='investment-property',skill_version='1.0.0',functional_currency='EUR',execution_date='2027-02-01',imports=[],us_property_scope='ordinary_held_and_used')
 c['jurisdiction']={'IFRS':'NL','AASB':'AU','UK_GAAP':'GB','US_GAAP':'US'}[fw]
 if fw=='AASB':c['aasb_compilation']='AASB140_DEC2022'
 c['applicability_review']['standard_versions']=[EDITIONS[fw]]
 c['accounting_policy']=pol(c,'policy',measurement_model=model,early_adoption=False,policy_change=False,class_consistent=True);c['accounting_policy']['effective_standard']=EDITIONS[fw]
 p=approved('property',asset_id='property-001',source_entity=c['entity'],source_framework=fw,source_period=[c['period_start'],c['reporting_period']],source_currency='EUR',legal_owner=c['entity'],title_document='synthetic legal title',rights_memo='Full legal and economic rights inspected',classification_memo='Documented rental purpose with no significant services',owned=True,recognition_criteria_met=True,purpose='rental',significant_services=False,mixed_use=mixed,owner_use_insignificant=True,insignificance_memo='Synthetic immaterial inseparable reception space judgment',group_rental=model=='group_cost',separate_statements=True,group_lessee='Synthetic subsidiary',group_relationship_memo='Full commercial separate lessor elected consistent group-rental cost class',opening_carrying='600000',gross_cost='600000',opening_accumulated_depreciation='0',opening_accumulated_impairment='0',closing_carrying='650000')
 for k in ['right_of_use','finance_lessor','business_combination','construction','inventory','held_for_sale','sale_leaseback','complex_consideration','foreign_operation']:p[k]=False
 if mixed=='separable':
  p['segregation']=record(c,'segregation',segregation_memo='Separately saleable identified property interest',separately_saleable=True,separately_finance_leasable=False,whole_cost='800000',part_inventory=['rental-part','owner-part'],parts=[approved('rental-part',use='rental',component_id='property-001',cost='600000'),approved('owner-part',use='owner',component_id='owner-001',cost='200000')])
 c['properties']=[p];c['source_inventory']=['property']
 p['gifted']=False
 p['acquisition_date']='2026-12-31' if route=='initial' else '2025-01-01'
 p['opening_history']=record(c,'opening',previous_reporting_date='2025-12-31',measurement_model=model,carrying='0' if route=='initial' else '600000',opening_memo='Independently reconciled original prior-period asset register and measurement model')
 c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=1,population_amount='600000',owner='synthetic register owner',reviewer='synthetic completeness reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic complete sources reconciled independently')
 c['events']=[record(c,'event',kind=route,date='2026-12-31',event_memo='Independent documentary event and cutoff review',economic_id='property-event-001',actual_change_of_use=True,change_use_date='2026-12-31',previous_use='owner' if route=='transfer_in_cost' else 'rental',new_use='rental' if route=='transfer_in_cost' else 'owner',actual_use_evidence='Signed occupancy commencement/cessation record',ppe_owner_document='Reviewed PPE carrying value and journal ownership',ppe_carrying='580000',purchase_cost='600000',paid=True,cash_date='2026-12-31',gross_proceeds='700000',selling_costs='10000',net_cash_received='690000',derecognized_carrying='650000',sale_recognition_met=True,continuing_involvement=False,sale_contract='Signed sale contract and bank settlement',derecognition_memo='Actual rights transferred and sale recognized',sale_criteria_owner_memo='Independent nonfinancial asset sale owner criteria review')];c['event_inventory']=['event']
 c['valuation']=record(c,'valuation',methodology_memo='Independent income valuation; property rights and complete inputs reviewed',rights_memo='Same freehold asset interest',market_participant_memo='Reporting-date exit-price inputs independently sourced',uncertainty_memo='No unresolved material uncertainty',valuer='synthetic external valuer',qualified_reviewer='synthetic qualified separate reviewer',report_hash='a'*64,valuation_standard='FRS102_SECTION2A' if fw=='UK_GAAP' else 'AASB13' if fw=='AASB' else 'IFRS13',valuation_method='income',valuation_date='2026-12-31',basis='market_participant_exit_price',reliable=True,material_unresolved_uncertainty=False,transaction_costs_deducted=False,recognized_by_other_owner=False,amount='650000') if model=='fair_value' or fw in {'IFRS','AASB'} else None
 c['cost_owner']=None;c['impairment_owner']=None
 if model!='fair_value' and route!='initial':
  p['opening_history']['opening_memo']='Synthetic reconciled 2025 gross/carrying 600000 with zero depreciation: acquired in 2025 but not ready for intended use until dated technical/legal readiness evidence 2026-01-01; no prior construction/development/subsequent-work accounting is assessed here'
  c['cost_owner']=record(c,'depreciation',accounting_owner='Fixed Assets',already_recognized=True,basis_memo='Source gross cost and opening stock independently reviewed; synthetic dated technical/legal readiness evidence confirms first available for intended use 2026-01-01, not first tenancy or actual occupancy',estimate_memo='Supported unchanged 25-year straightline building life and nil residual',owner_memo='Owner journal already retained; no repeat',land_cost='100000',building_residual='0',building_life_years='25',method='straight_line',estimate_change=False,available_for_use='2026-01-01',charge_start='2026-01-01',charge_end='2026-12-31',depreciation='20000',opening_carrying='600000',closing_before_impairment='580000',economic_id='dep-001')
  c['impairment_owner']=record(c,'impairment',accounting_owner='Asset Impairment',already_recognized=True,screening_memo='Independently reviewed indicators; no loss in synthetic scenario',owner_memo='Original impairment owner retained',reversal=False,indicators_present=False,loss='0',opening_carrying='580000',closing_carrying='580000',economic_id='imp-001')
  p['closing_carrying']='580000';c['events'][0]['derecognized_carrying']='580000'
 if route=='initial':
  c['events'][0]['acquisition_nature']='cash_purchase'
  p['opening_carrying']='0';p['closing_carrying']='600000' if model!='fair_value' else '650000'
  c['events'][0]['cost_items']=[record(c,'purchase',economic_id='purchase-001',kind='purchase_price',eligibility_memo='Signed cash property asset acquisition; not a business',amount='590000',date='2026-12-31',accounting_owner='Investment Property'),record(c,'legal',economic_id='legal-001',kind='direct_transaction',eligibility_memo='Direct conveyance cost only',amount='10000',date='2026-12-31',accounting_owner='Investment Property')];c['events'][0]['cost_inventory']=['purchase','legal']
 if route=='transfer_in_cost':c['events'][0]['ppe_carrying']='580000';p['closing_carrying']='580000'
 if route in {'transfer_out_cost','transfer_out_fv','disposal'}:p['closing_carrying']='0'
 if route=='transfer_out_fv':c['events'][0]['ppe_carrying']='650000'
 ownership=[]
 for movement,owner,eid in ([('initial','Investment Property','property-event-001')] if route=='initial' else [('disposal','Investment Property','property-event-001')] if route=='disposal' else [('transfer','Investment Property','property-event-001')] if route.startswith('transfer') else []):ownership.append(record(c,'owner-'+movement,economic_id=eid,movement=movement,accounting_owner=owner,ownership_memo='Independent exact-once journal ledger'))
 if model=='fair_value':ownership.append(record(c,'owner-fv',economic_id='property-event-001',movement='fair_value',accounting_owner='Investment Property',ownership_memo='Valuation provider measures only; IP owns recognition'))
 if c['cost_owner'] is not None:
  for move,owner,eid in [('depreciation','Fixed Assets','dep-001'),('impairment','Asset Impairment','imp-001')]:ownership.append(record(c,'owner-'+move,economic_id=eid,movement=move,accounting_owner=owner,ownership_memo='Source owner already recognizes effect; IP evidence only'))
 c['ownership_register']=ownership;c['ownership_inventory']=[r['id'] for r in ownership]
 account='Property plant and equipment' if fw=='US_GAAP' or model=='group_cost' else 'Investment property'
 initial=route=='initial';dep=Decimal('20000') if c['cost_owner'] else Decimal(0);before=Decimal(p['opening_carrying'])-dep if not initial else Decimal('600000');gain=Decimal('650000')-before if model=='fair_value' else Decimal(0)
 closing=Decimal(p['closing_carrying']);net=Decimal('690000') if route=='disposal' else Decimal(0);disposed=(Decimal('650000') if model=='fair_value' else before) if route=='disposal' else Decimal(0)
 transfer=(before if route=='transfer_in_cost' else -(Decimal('650000') if model=='fair_value' else before) if route.startswith('transfer_out') else Decimal(0))
 calc=dict(opening_carrying=p['opening_carrying'],additions='600000' if initial else '0',depreciation_owned_elsewhere=str(dep),impairment_owned_elsewhere='0',fair_value_movement=str(gain),transfers=str(transfer),disposal_carrying=str(disposed),net_proceeds=str(net),disposal_gain=str(net-disposed) if disposed else '0',closing_carrying=str(closing))
 if route=='transfer_in_cost':calc.update(opening_carrying='0',depreciation_owned_elsewhere='0',pre_transfer_depreciation_owned_elsewhere=str(dep),pre_transfer_impairment_owned_elsewhere='0')
 if model=='cost' and fw in {'IFRS','AASB'}:calc['fair_value_disclosure']='650000' if closing else '0'
 opening_gl=Decimal(0) if route in {'initial','transfer_in_cost'} else Decimal(p['opening_carrying'])-dep
 balances={account:(opening_gl,closing)}
 if initial:balances['Cash']=(Decimal('1000000'),Decimal('400000'))
 if gain:balances['Property fair value profit or loss']=(Decimal(0),-gain)
 if route=='transfer_in_cost':balances['Property plant and equipment']=(before,Decimal(0))
 if route.startswith('transfer_out'):balances['Property plant and equipment']=(Decimal(0),-transfer)
 if route=='disposal':balances['Cash']=(Decimal(0),net);balances['Property disposal profit or loss']=(Decimal(0),disposed-net)
 c['gl']=[approved(k,opening=str(a),closing=str(b),statement=str(b)) for k,(a,b) in balances.items()];c['gl_inventory']=list(balances)
 c['disclosure_review']=record(c,'disclosures',checklist_version='full2026',period_entity_memo='Framework and model-specific source amounts inspected',complete=True,requirements=['policy','classification','restrictions','commitments','rollforward','rental_income','direct_expenses','valuation_method','valuer','fair_value','depreciation_method','useful_lives','gross_accumulated','group_rental_carrying'],amounts=calc,presentation=account,rental_owner_document='Rental revenue and direct expense separately owned',statement_owner_document='Financial statement presentation reviewed')
 c['disclosure_review'].update(rental_income='40000',direct_expenses_generating_income='5000',direct_expenses_not_generating_income='1000',commitments_amount='0',restrictions_memo='Source title and lender records independently reviewed; no restriction in synthetic case',commitments_memo='Complete contract population contains no capital commitment')
 if route=='initial':c['disclosure_review'].update(rental_income='0',direct_expenses_generating_income='0',direct_expenses_not_generating_income='0')
 return capture(c)

def ready(fw='IFRS',model='fair_value',route='hold',mixed='none',c=None):
 c=deepcopy(c) if c is not None else case(fw,model,route,mixed)
 finalize('investment-property',c)
 from production import canonical_knowledge,PACKAGES
 cs,_=canonical_knowledge(PACKAGES['investment-property'][1],c['framework'])
 c['knowledge_review']['applied_claim_ids']=[x['claim_id'] for x in cs if c['framework']!='UK_GAAP' or x['decision']!='period_scope'];c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
 return c

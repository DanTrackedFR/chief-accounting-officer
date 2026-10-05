"""Treasury company exports and separate synthetic reviewer qualification.

Annual-to-date review at December month-end. One USD floating term facility has
independently supplied reset cashflows and EIR; no rate forecast is created here.
All period cash conversions are 1 EUR/USD, and closing rate is 1.10 EUR/USD.
"""
import copy
from decimal import Decimal
from dataclasses import asdict
from pathlib import Path
from orchestration.tests.fixtures import completed
from orchestration.intake import *
from orchestration.tests.intake_fixtures import cl,cell
from orchestration.intake.semantic import transform
from orchestration.planning import FACT_ADAPTERS
from orchestration.runtime import digest
from financing_cases import case as debt_case,gl,ready as debt_ready
from additional_cases import fx,reporting,certify
from hedge_cases import debt_case as hedge_debt,sources as hedge_sources,ready as hedge_ready
from reporting_cases import reporting as cash_case
from operational_cases import operational,approved
from governance_cases import case as analytics_case,ready,refresh_release,document,row

SCOPE=dict(entity='Synthetic Group',framework='IFRS',jurisdiction='NL',period_start='2026-01-01',reporting_period='2026-12-31',currency='EUR',industry='business services',materiality='5')
SPAN=[SCOPE['period_start'],SCOPE['reporting_period']]
OBJECTIVE='Can you review our treasury and financing position at December month-end, including the year-to-date movements? Interest expense is up, we have a USD loan and a derivative hedge, FX moved a lot, and the cash flow statement does not look right. I have attached the debt schedule, lender statements, FX report, derivative valuation, hedge documentation, bank activity, trial balance and cash flow support.'
OPENING=[('Cash','2000','asset'),('Debt','-1000','liability'),('Opening equity','-1000','equity')]
CURRENT=[('Cash','1720','asset'),('Debt','-880','liability'),('Derivative','40','asset'),('Opening equity','-1000','equity'),('Interest expense','80','expense'),('FX loss','80','expense'),('Hedge income','-4','revenue'),('Hedge OCI','-36','oci')]
FAMILIES={pkg:family for family,(pkg,_) in FACT_ADAPTERS.items()}

def sources(clean=False):
 def raw(id,name,fmt,data,controlled=True):return RawSource(id,name,fmt,data,dict(entity=SCOPE['entity'],period=['2025-01-01','2025-12-31'] if id=='prior' else SPAN,currency='EUR',comparator='prior_actual' if id=='prior' else 'actual',version='frozen-1',source_system='Synthetic treasury export',controlled_export=controlled,as_of='2025-12-31' if id=='prior' else SPAN[1],extracted_at='2027-02-01'))
 return [
 raw('debt','Debt register.csv','csv','loan,opening,principal,draws,fees,yield,interest,paid,repayment,base_closing,current,noncurrent,rights,rate_type\nloan,1000,1000,0,0,0.08,80,80,200,800,800,0,true,variable\n'),
 raw('lender','Lender statement.csv','csv','loan,legal_principal,original_currency,closing_carrying_foreign\nloan,800,USD,800\n'),
 raw('terms','Facility extract.md','markdown','USD term facility loan. Annual benchmark resets are independently reviewed; supplied 2026 contractual/EIR charge is USD80 on opening USD1000. USD200 principal and USD80 interest paid December31 at EUR1/USD. Remaining reviewed reset cashflow USD864 on December31 2027 contains USD800 principal. Contract rights and covenant compliance at December31 support all remaining debt being current. No waiver, modification, capitalization or refinancing is assumed. Future reset re-estimation requires a fresh qualified debt schedule.',False),
 raw('payments','Remaining contractual payments.csv','csv','payment_id,date,amount,principal\ncurrent,2026-12-31,280,200\nredemption,2027-12-31,864,800\n'),
 raw('fx','Monetary FX report.csv','csv','loan,original_currency,foreign_amount,opening_book,opening_rate,closing_rate,settled,settlement_rate,closing,gain\nloan,USD,1000,1000,1,1.10,200,1,880,-80\n'),
 raw('derivative','Swap confirmation.csv','csv','instrument,notional,maturity,underlying\nforward1,800,2027-12-31,USD benchmark\n'),
 raw('valuation','Independent valuation.csv','csv','instrument,notional,measurement_date,opening,change,settlement,closing\nforward1,800,2026-12-31,0,40,0,40\n'),
 raw('designation','Hedge designation.csv','csv','relationship,instrument,loan,date,quantity,risk\nrelationship1,forward1,loan,2026-01-01,800,benchmark_interest\n'),
 raw('effectiveness','Independent hedged-risk schedule.csv','csv','relationship,instrument_cumulative,risk_cumulative,quantity,opening_reserve,effective,ineffective,closing_reserve\nrelationship1,40,-36,800,0,36,4,36\n'),
 raw('bank','Bank activity.csv','csv','bank_id,date,amount,kind,category\nBANK-INTEREST,2026-12-31,-80,interest_paid,operating\nBANK-PRINCIPAL,2026-12-31,-200,debt_repayment,financing\n'),
 raw('bank_summary','Bank movement summary.csv','csv','financing\n-200\n'),
 raw('tb','Year-to-date trial balance.csv','csv','account,balance,category\n'+''.join(','.join(r)+'\n' for r in CURRENT)),
 raw('cash','Cash flow support.csv','csv','opening,closing,operating,investing,financing,fx\n2000,1720,-80,0,'+('-200' if clean else '0')+',0\n'),
 raw('rec','Reconciliation pack.csv','csv','account,source,gl\nDebt,-880,-880\nDerivative,40,40\nCash,1720,1720\n'),
 raw('policy','Treasury policy extract.md','markdown','EUR functional currency. IAS7 pre-2027 ordinary entity: interest paid classified operating consistently with prior period; principal payments financing gross. First-year continuing cash-flow hedge of future benchmark interest on remaining USD800; no current derivative settlement or reserve recycling. Qualified independent whole-instrument valuation and separately measured risk are required. No cash equivalents, covenant waiver or legal conclusions are inferred.',False),
 raw('pnl','Year-to-date P&L.csv','csv','interest\n80\n'),
 raw('prior','Prior annual actual interest.csv','csv','principal,rate,interest\n1000,0.06,60\n'),
 raw('commentary','Management commentary.md','markdown','Interest expense is up mainly because rates increased. The hedge offset almost all of the FX loss.',False),
 ]

# Source fields bind exact native workpaper fields, not an intake accounting approval.
MAP=[
 ('debt-open','debt_population','opening','debt','opening',2,('debt',0,'opening_carrying'),'decimal'),
 ('debt-principal','debt_population','principal','debt','principal',2,('debt',0,'opening_principal'),'decimal'),
 ('debt-yield','debt_population','yield','debt','yield',2,('debt',0,'annual_yield'),'decimal'),
 ('debt-rights','debt_population','rights','debt','rights',2,('debt',0,'rights_at_reporting_date'),'boolean'),
 ('debt-repayment','debt_population','repayment','debt','repayment',2,('debt',0,'schedule',0,'principal_payment'),'decimal'),
 ('debt-interest','debt_population','interest','debt','interest',2,('debt',0,'schedule',0,'expected_interest'),'decimal'),
 ('debt-paid','debt_population','paid_interest','debt','paid',2,('debt',0,'schedule',0,'cash_interest'),'decimal'),
 ('debt-close','debt_population','closing_base','debt','base_closing',2,('__result__','debt',0,'closing'),'decimal'),
 ('fx-original','currency_exposure','original_amount','fx','foreign_amount',2,('items','loan','foreign_amount'),'decimal'),
 ('fx-currency','currency_exposure','original_currency','fx','original_currency',2,('items','loan','foreign_currency'),'identity'),
 ('fx-opening','currency_exposure','opening_book','fx','opening_book',2,('items','loan','opening_book'),'decimal'),
 ('fx-rate','currency_exposure','closing_rate','fx','closing_rate',2,('items','loan','closing_rate'),'decimal'),
 ('fx-settled','currency_exposure','settled','fx','settled',2,('items','loan','settled_foreign'),'decimal'),
 ('fx-profit','currency_exposure','monetary_fx_profit','fx','gain',2,('__result__','monetary_fx_profit'),'decimal'),
 ('hedge-value','derivative_contract','derivative_closing','valuation','closing',2,('__result__','derivatives','forward1','closing'),'decimal'),
 ('hedge-date','derivative_contract','valuation_date','valuation','measurement_date',2,('valuations','valuation1','measurement_date'),'iso_date'),
 ('hedge-notional','derivative_contract','notional','valuation','notional',2,('valuations','valuation1','notional'),'decimal'),
 ('hedge-designation','derivative_contract','designation_date','designation','date',2,('relationships','relationship1','designation_date'),'iso_date'),
 ('hedge-risk','derivative_contract','risk_cumulative','effectiveness','risk_cumulative',2,('relationships','relationship1','risk_measurement','risk_cumulative'),'decimal'),
 ('cash-interest','cash_activity','interest_paid','bank','amount',2,('transactions','BANK-INTEREST','amount'),'decimal'),
 ('cash-principal','cash_activity','principal_paid','bank','amount',3,('transactions','BANK-PRINCIPAL','amount'),'decimal'),
 ('cash-close','cash_activity','closing_cash','cash','closing',2,('__result__','closing'),'decimal'),
 ('rec-debt','reconciliation','debt_balance','rec','source',2,('reconciliations','Debt','source_closing'),'decimal'),
 ('fs-debt','statement','debt_balance','tb','balance',3,('current_tb','Debt','balance'),'decimal'),
 ('prior-interest','analytics','prior_interest','prior','interest',2,('documents','interest-prior','content','amount'),'decimal'),
 ('analytics-interest','analytics','current_interest','pnl','interest',2,('accounts','cash-metric','amount'),'decimal'),
]

for id,attr,source,col,path,method in [
 ('draws','draws','debt','draws',('debt',0,'draws'),'decimal'),('fees','fees','debt','fees',('debt',0,'eligible_cost'),'decimal'),('class-current','current','debt','current',('debt',0,'current_carrying'),'decimal'),('class-noncurrent','noncurrent','debt','noncurrent',('debt',0,'noncurrent_carrying'),'decimal'),('rate-type','rate_type','debt','rate_type',('debt',0,'contractual_rate_type'),'identity'),('lender-principal','lender_principal','lender','legal_principal',('debt',0,'lender_principal'),'decimal')]:
 MAP.append((id,'debt_population',attr,source,col,2,path,method))
for i,payment in [(2,'current'),(3,'redemption')]:
 for col in ['date','amount','principal']:
  MAP.append(('payment-'+payment+'-'+col,'debt_population','payment_'+payment+'_'+col,'payments',col,i,('debt',0,'yield_validation','cashflows',payment,col),'iso_date' if col=='date' else 'decimal'))
for col,path,method in [('opening_rate',('items','loan','opening_rate'),'decimal'),('settlement_rate',('items','loan','settlement_rate'),'decimal')]:
 MAP.append(('fx-'+col,'currency_exposure',col,'fx',col,2,path,method))
for col,path,method in [('instrument',('contracts','forward1','id'),'identity'),('notional',('contracts','forward1','notional'),'decimal'),('maturity',('contracts','forward1','maturity'),'iso_date'),('underlying',('contracts','forward1','underlying'),'identity')]:
 MAP.append(('contract-'+col,'derivative_contract','contract_'+col,'derivative',col,2,path,method))
for col in ['opening','change','settlement']:
 MAP.append(('valuation-'+col,'derivative_contract','valuation_'+col,'valuation',col,2,('valuations','valuation1',col),'decimal'))
for col,path,method in [('loan',('relationships','relationship1','hedged_item_id'),'identity'),('quantity',('relationships','relationship1','actual_item_quantity'),'decimal'),('risk',('relationships','relationship1','risk_id'),'identity')]:
 MAP.append(('designation-'+col,'derivative_contract','designation_'+col,'designation',col,2,path,method))
for col,path in [('instrument_cumulative',('relationships','relationship1','risk_measurement','instrument_cumulative')),('quantity',('relationships','relationship1','actual_instrument_quantity')),('opening_reserve',('relationships','relationship1','opening_reserve'))]:
 MAP.append(('effectiveness-'+col,'derivative_contract','effectiveness_'+col,'effectiveness',col,2,path,'decimal'))
for col,path in [('effective',('__result__','derivatives','forward1','effective')),('ineffective',('__result__','derivatives','forward1','ineffectiveness')),('closing_reserve',('__result__','hedge_reserves','relationship1','closing'))]:
 MAP.append(('effectiveness-'+col,'derivative_contract',col,'effectiveness',col,2,path,'decimal'))
for index,id in [(2,'BANK-INTEREST'),(3,'BANK-PRINCIPAL')]:
 for col in ['date','kind','category','bank_id']:
  MAP.append(('bank-'+id+'-'+col,'cash_activity','bank_'+id.lower().replace('-','_')+'_'+col,'bank',col,index,('transactions',id,col),'iso_date' if col=='date' else 'identity'))

def selected(owner):
 if not owner:return {'debt-financing','foreign-currency','derivatives-hedge-accounting','cash-flow-reporting','balance-sheet-reconciliations','financial-statements','management-accounting-analytics'}
 return {'debt-financing'} if owner=='debt-financing' else {'foreign-currency'} if owner=='foreign-currency' else {'debt-financing','derivatives-hedge-accounting'} if owner=='derivatives-hedge-accounting' else {'debt-financing','foreign-currency','cash-flow-reporting'}

def proposal(raw,objective=OBJECTIVE,bounded=None):
 inv=Inventory(raw);wanted=selected(bounded)
 p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Treasury month-end review'),cl('REPORTING' if bounded else 'RECONCILIATION_INVESTIGATION'))
 if bounded:p.bounded_owner=cl(bounded)
 else:p.secondary_modes=[cl('DIAGNOSTIC_ANALYTICS'),cl('CLOSE_REVIEW')];p.supporting_modes=[cl('ACCOUNTING_DETERMINATION'),cl('REPORTING')]
 for id,family,attribute,source,column,index,path,method in MAP:
  owner=FACT_ADAPTERS[family][0]
  if owner not in wanted:continue
  e=cell(inv,source,column,index);p.facts.append(FactCandidate(id,family,attribute,cl(transform(inv.fields()[e]['value'],method),[e],'EXTRACTED',.99),dict(entity=SCOPE['entity'],period=['2025-01-01','2025-12-31'] if id=='prior-interest' else SPAN,currency='EUR',unit='currency',comparator='prior_actual' if id=='prior-interest' else 'actual'),owner,confirmation_required=False,transformation=method))
 if not bounded:
  for id,source,column,index in [('reported-financing','cash','financing',2),('bank-financing','bank_summary','financing',2)]:
   e=cell(inv,source,column,index);p.facts.append(FactCandidate(id,'cash_activity','financing_support',cl(transform(inv.fields()[e]['value'],'decimal'),[e],'EXTRACTED',.99),dict(entity=SCOPE['entity'],period=SPAN,currency='EUR',unit='currency',comparator='actual'),confirmation_required=False,transformation='decimal'))
  e=inv.extractions['commentary'].blocks[0]['field'];p.hypotheses=[cl(dict(id='hedge-offset-fx',description='The hedge offset almost all FX loss',tests=[dict(left_owner='derivatives-hedge-accounting',left_path=['derivatives','forward1','ineffectiveness'],right_owner='foreign-currency',right_path=['monetary_fx_profit'],factor=0.9,operator='magnitude_above')]),[e])]
  p.context_candidates={'currency':cl('EUR',status='CONTEXT_DERIVED')}
 for family in dict.fromkeys(f.family for f in p.facts):
  owner=FACT_ADAPTERS[family][0];facts=[f for f in p.facts if f.family==family];deps=[]
  if owner=='derivatives-hedge-accounting':deps=['debt-financing']
  if owner=='cash-flow-reporting':deps=['debt-financing','foreign-currency']
  if owner in ('financial-statements','balance-sheet-reconciliations','management-accounting-analytics'):deps=sorted(wanted & {'debt-financing','foreign-currency','derivatives-hedge-accounting','cash-flow-reporting'})
  p.issues.append(cl(dict(id=owner,owner=owner,family=family,fact_ids=[f.id for f in facts],dependencies=deps,required_fields=[]),list(dict.fromkeys(e for f in facts for e in f.claim.evidence))))
 return p

def owners():
 o={};d=debt_case('debt-financing');d['functional_currency']='EUR';r=d['debt'][0]
 r.update(annual_yield='0.08',opening_carrying='1000',opening_principal='1000',draws='0',eligible_cost='0',lender_principal='800',gl_closing='800',current_carrying='800',noncurrent_carrying='0',contractual_rate_type='variable',contractual_rate_terms_memo='Independently supplied reset cashflows; no future reset extrapolated by owner',contractual_benchmark='USD benchmark independently supplied at 8 percent EIR')
 r['schedule'][0].update(cash_interest='80',principal_payment='200',expected_interest='80',expected_closing='800')
 r['maturities'][0].update(date='2027-12-31',principal='800',carrying='800')
 r['yield_validation']['cashflows']=[approved('current',date='2026-12-31',amount='280',principal='200'),approved('redemption',date='2027-12-31',amount='864',principal='800')];r['yield_validation']['flow_inventory']=['current','redemption'];r['yield_validation']['contract_memo']='Externally reviewed remaining reset payment population, not model forecast'
 d['controls']['population_amount']='1000';gl(d,{'Cash':'-280','Interest expense':'80','Debt carrying liability':'-800'},{'Debt carrying liability':-1000})
 o['debt-financing']=debt_ready('debt-financing',c=d);dr=completed('debt-financing',o['debt-financing'])
 f=fx();f['translation']['enabled']=False;f['items'][0].update(id='loan',side='liability',type='monetary',account='Debt monetary',foreign_currency='USD',foreign_amount='1000',initial_date='2025-12-31',initial_rate='1',opening_rate='1',opening_book='1000',opening_route='carried_monetary',settled_foreign='200',settlement_date='2026-12-31',settlement_rate='1',closing_rate='1.10');o['foreign-currency']=certify('foreign-currency',f)
 h=hedge_debt(route='cash_flow');h['imports']=[dict(id='debt1',package='debt-financing',case=o['debt-financing'],result=dr)]
 h['owner_links'][0]['amount']='800';r=h['relationships'][0];r.update(underlying_carrying='800',debt_notional='800',debt_maturity='2027-12-31',actual_instrument_quantity='800',actual_item_quantity='800',risk_id='benchmark_interest',objective='Future benchmark interest protection; not an FX principal hedge',forecast_quantity='800')
 r.update(instrument_eligibility_memo='Eligible whole USD benchmark interest swap',item_eligibility_memo='Future interest on separately qualified USD term facility',risk_component_memo='Separately identifiable benchmark-interest component, not loan principal FX',forecast_memo='Separately reviewed future loan benchmark interest timing and notional',designation_memo='Contemporaneous signed inception designation of remaining facility benchmark interest')
 r['risk_measurement'].update(risk_id='benchmark_interest',quantity='800',current_change='-36',risk_cumulative='-36',instrument_cumulative='40')
 h['contracts'][0].update(kind='swap',underlying='USD benchmark',underlying_type='rate',notional='800',comparable_investment='800',maturity='2027-12-31');h['valuations'][0].update(notional='800',change='40',closing='40');h['population_review']['notional_total']='800'
 for g in h['gl']:g['closing']=g['statement']={'Derivative balance forward1':'40','Hedge P&L relationship1':'-4','Hedge reserve relationship1':'-36'}[g['id']]
 o['derivatives-hedge-accounting']=hedge_ready(hedge_sources(h));completed('derivatives-hedge-accounting',o['derivatives-hedge-accounting'])
 c=cash_case('cash-flow-reporting');c['cash_accounts'][0].update(opening='2000',closing='1720',gl_opening='2000',gl_closing='1720',fx='0')
 c['transactions']=[approved(id,date='2026-12-31',amount=n,kind=kind,category=cat,cash=True,source_id=id,bank_id=id,classification_memo='Consistent actual pre-2027 IAS7 elected operating interest, gross financing principal') for id,n,kind,cat in [('BANK-INTEREST','-80','interest_paid','operating'),('BANK-PRINCIPAL','-200','debt_repayment','financing')]]
 c['noncash']=[approved(id,source_id=id,amount=n,type='other_reviewed',date=SPAN[1],accounting_memo='Qualified originating owner noncash effect') for id,n in [('FX-LOAN','80'),('FV-HEDGE','40')]];c['noncash_inventory']=[r['id'] for r in c['noncash']];c['noncash_source_total']='120'
 c['indirect'].update(start_amount='-156',net_profit='-156',adjustments=[approved(id,amount=n,basis_memo='Disjoint native FX/P&L adjustment',noncash_acquisition_fx_excluded=True) for id,n in [('FX','80'),('Hedge P&L','-4')]],adjustment_inventory=['FX','Hedge P&L'],working_capital=[],working_capital_inventory=[])
 c['statement'].update(opening='2000',closing='1720',balance_sheet_opening='2000',balance_sheet_closing='1720',operating='-80',investing='0',financing='-200',fx='0');c['handoffs']['fx']['amount']='0';c['handoffs']['profit']['amount']='-156';c['controls'].update(population_count=2,population_amount='280');c['imports']=[approved(pkg,package=pkg,case=o[pkg],result=completed(pkg,o[pkg]),mode='evidence_only') for pkg in ('debt-financing','foreign-currency')];o['cash-flow-reporting']=certify('cash-flow-reporting',c)
 fs=reporting();fs['currency']='EUR'
 def tb(rs):return [dict(id=id,balance=n,category=cat,line=id,source_version='frozen-1',classification_memo='Native owner and actual rights support account class',cash_account=id=='Cash') for id,n,cat in rs]
 fs['current_tb']=tb(CURRENT);fs['comparative_tb']=tb(OPENING);fs['equity_bridge']=[dict(id='owners',opening='1000',profit='-156',oci='36',owner_transactions='0',retrospective_adjustments='0',other='0',closing='880',memo='Debt, FX and Hedge owner effects')]
 fs['cash_flow'].update(start_amount='-156',adjustments=[dict(id=id,amount=n,source='Reviewed originating owner result',noncash_acquisition_fx_excluded=True,memo='Explicit noncash adjustment') for id,n in [('FX','80'),('Hedge P&L','-4')]],investing='0',financing='-200',fx='0',opening='2000',closing='1720',classifications=[dict(id=t['id'],date=t['date'],kind=t['kind'],**{'class':t['category']},amount=t['amount'],memo=t['classification_memo']) for t in c['transactions']]);fs['notes']=[dict(id='cash-note',target='cash',amount='1720',population_evidence='Actual bank activity',memo='No inferred cash equivalents')]
 fs['owner_support']=dict(current_debt='880',noncurrent_debt='0',hedge_reserve='36',operating='-80',financing='-200')
 o['financial-statements']=certify('financial-statements',fs)
 rec=operational('balance-sheet-reconciliations');rec['functional_currency']='EUR';rec['trial_balance']=[dict(id=id,balance=n,category='balance_sheet' if cat in ('asset','liability','equity') else 'profit_loss') for id,n,cat in CURRENT];rec['inventory']=[dict(id=id) for id,n,cat in CURRENT if cat in ('asset','liability','equity')];rec['reconciliations']=[]
 old={id:n for id,n,cat in OPENING}
 for id,n,cat in CURRENT:
  if cat not in ('asset','liability','equity'):continue
  addition,reduction={'Cash':('0','280'),'Debt':('280','160'),'Derivative':('40','0'),'Opening equity':('0','0')}[id]
  rec['reconciliations'].append(approved(id,opening=old.get(id,'0'),additions=addition,reductions=reduction,source_closing=n,gl_closing=n,source_ids=[id],gl_ids=[id],items=[],adjustments=[],threshold='0',relative_threshold='0',max_age_days=30,risk_tier='high',movement_memo='Gross Debt interest/payment and FX movements retained; no plug'))
 rec['controls'].update(population_count=4,population_amount='3640');o['balance-sheet-reconciliations']=certify('balance-sheet-reconciliations',rec)
 # Existing generic accounting flux + rate/quantity analytics. No skill expansion.
 a=analytics_case('management-accounting-analytics');a['governance_method']['currency']='EUR';a['accounts'][0].update(amount='80',management_amount='80',account='interest',currency='EUR');a['account_source']['records']=copy.deepcopy(a['accounts']);a['controls']['population_amount']='80'
 for doc in a['documents']:
  doc['currency']='EUR';data=doc['content']
  if doc['id'] in ('current-books','prior-books'):
   n='80' if doc['id']=='current-books' else '60';data.update(account='interest',currency='EUR',statutory_amount=n,management_amount=n,gross_amount=n);data['records'][0].update(account='interest',amount=n)
  if doc['id']=='actual-drivers':data.update(account='interest',drivers=[dict(id='actual-rate',amount='20')],driver_inventory=['actual-rate'])
 a['explanations'][0].update(account='interest',amount='20');a['imports']=[row(a,pkg,package=pkg,case=o[pkg],result=completed(pkg,o[pkg]),mode='evidence_only') for pkg in ('debt-financing','foreign-currency','derivatives-hedge-accounting','cash-flow-reporting')]
 ref=dict(owner_import='debt-financing',result_path=['debt',0,'effective_interest'],amount='80')
 basis='signed_balance';prior=['2025-01-01','2025-12-31']
 def metric(id,n,span,components):
  document(a,id,dict(entity=SCOPE['entity'],currency='EUR',unit='EUR',period=span,metric='expense',presentation_basis=basis,kind='actual',posted_only=True,amount=n,records=[dict(id=id+'-posted',amount=n)],inventory=[id+'-posted'],version='actual-v1',approved=True,supplied=True,approved_on='2025-12-31',owner_components=components))
 metric('interest-current','80',SPAN,[dict(sign=1,ref=ref)]);metric('interest-prior','60',prior,[]);next(d for d in a['documents'] if d['id']=='interest-prior')['content']['interest']='60'
 document(a,'interest-drivers',dict(entity=SCOPE['entity'],currency='EUR',unit='EUR',period=SPAN,metric='expense',presentation_basis=basis,baseline_period=prior,comparator_version='actual-v1',method='rate_quantity',source_owner='debt-financing',source_metric='effective_interest',category='economic',evidence_class='bridge_attribution',confidence='high',population_complete=True,records=[dict(id='loan-rate',q0='1000',p0='0.06',q1='1000',p1='0.08',baseline_amount='60',current_amount='80',current_owner=ref,economic_components=['loan-current-interest-ex-fx'])],inventory=['loan-rate']))
 a['diagnostic']=dict(component_ties=[dict(groups=['loan-rate'],current_owner=ref,baseline_field='interest',sign=1)],unit='EUR',metric='expense',presentation_basis=basis,current={'doc':'interest-current'},comparator=dict(doc='interest-prior',kind='actual',version='actual-v1',period=prior,frozen_on='2025-12-31'),groups=[dict(id='loan-rate',doc='interest-drivers',method='rate_quantity',sign=1,labels=dict(quantity='Opening principal contribution',rate='Reviewed effective-rate contribution'),accounting_check=dict(**ref,issue='Current interest accounting',reason='Recheck diagnostic interest against qualified debt schedule'))],group_inventory=['loan-rate'],tolerance='.01',materiality='5',hypotheses=[],signals=[],revenue=None)
 for doc in a['documents']:doc['content_hash']=digest(doc['content'])
 o['management-accounting-analytics']=ready('management-accounting-analytics',c=refresh_release(a))
 # Exact full source qualification is independent scaffolding, not runtime approval.
 raw=Inventory(sources(clean=True)).normalized()
 source_owners={'debt':'debt-financing','lender':'debt-financing','terms':'debt-financing','payments':'debt-financing','fx':'foreign-currency','derivative':'derivatives-hedge-accounting','valuation':'derivatives-hedge-accounting','designation':'derivatives-hedge-accounting','effectiveness':'derivatives-hedge-accounting','bank':'cash-flow-reporting','bank_summary':'cash-flow-reporting','policy':'cash-flow-reporting','tb':'financial-statements','rec':'balance-sheet-reconciliations','pnl':'management-accounting-analytics','prior':'management-accounting-analytics'}
 for src in raw:
  data=src['source'];pkg=source_owners.get(data['id'])
  if pkg:o[pkg].setdefault('source_material',{})[data['id']]=dict(fingerprint=data['fingerprint'],metadata=data['metadata'])
 done={}
 def qualify(pkg):
  if pkg in done:return done[pkg]
  c=o[pkg]
  for imp in c.get('imports',[]):
   imp['result']=qualify(imp['package']);imp['case']=copy.deepcopy(o[imp['package']])
  if pkg=='derivatives-hedge-accounting':o[pkg]=hedge_ready(hedge_sources(c))
  elif pkg=='management-accounting-analytics':o[pkg]=ready(pkg,c=refresh_release(c))
  elif pkg=='debt-financing':o[pkg]=debt_ready(pkg,c=c)
  else:o[pkg]=certify(pkg,c)
  done[pkg]=completed(pkg,o[pkg]);return done[pkg]
 for pkg in o:qualify(pkg)
 return o

def reviewed_pack(prepared,objective=OBJECTIVE,bounded=None):
 o=owners();wanted=selected(bounded);o={p:c for p,c in o.items() if p in wanted};handoffs=[]
 def link(pkg,semantic,path,target,n,sign=1,components=None,consumer='financial-statements'):
  handoffs.append(dict(producer=pkg,consumer=consumer,semantic=semantic,metric_path=path,target_path=target,amount=n,sign=sign,purpose='report',economic_id=semantic+'-'+consumer,qualification_evidence='Separate synthetic exact-case source/owner review',**({'components':components} if components else {})))
 if not bounded:
  comp=[dict(producer='foreign-currency',metric_path=['monetary_fx_profit'],sign=-1)]
  link('debt-financing','debt_base',['debt',0,'closing'],['current_tb','Debt','balance'],'880',-1,comp)
  link('debt-financing','debt_current',['debt',0,'current'],['owner_support','current_debt'],'880',1,comp)
  link('debt-financing','debt_noncurrent',['debt',0,'noncurrent'],['owner_support','noncurrent_debt'],'0')
  link('debt-financing','interest_expense',['debt',0,'effective_interest'],['current_tb','Interest expense','balance'],'80')
  link('foreign-currency','monetary_fx',['monetary_fx_profit'],['current_tb','FX loss','balance'],'-80',-1)
  for sem,path,target,n,sign in [('derivative_balance',['derivatives','forward1','closing'],['current_tb','Derivative','balance'],'40',1),('hedge_reserve',['hedge_reserves','relationship1','closing'],['owner_support','hedge_reserve'],'36',1),('hedge_pnl',['derivatives','forward1','ineffectiveness'],['current_tb','Hedge income','balance'],'4',-1),('hedge_oci',['hedge_reserves','relationship1','recognized_oci'],['current_tb','Hedge OCI','balance'],'36',-1)]:link('derivatives-hedge-accounting',sem,path,target,n,sign)
  for sem,path,target,n in [('cash_balance',['closing'],['current_tb','Cash','balance'],'1720'),('financing_cash',['financing'],['cash_flow','financing'],'-200'),('operating_cash',['direct_operating'],['owner_support','operating'],'-80')]:link('cash-flow-reporting',sem,path,target,n)
 req=dict(case_id='synthetic-treasury-'+('narrow' if bounded else 'review'),objective=objective,scope=SCOPE,facts={FAMILIES[p]:c for p,c in o.items()},handoffs=handoffs)
 if not bounded:
  mapping={'Cash':'Cash','cash':'Cash','Debt carrying liability':'Debt','Debt monetary':'Debt','Interest expense':'Interest expense','FX income':'FX loss','Derivative balance forward1':'Derivative','Hedge P&L relationship1':'Hedge income','Hedge reserve relationship1':'Hedge OCI'}
  def jr(pkg,i):return dict(owner=pkg,index=i)
  def atom(pkg,i,line,n):return dict(owner=pkg,index=i,line=line,amount=n)
  events=[dict(economic_id='interest-accrued',primary=[jr('debt-financing',0)],witnesses=[],evidence='Qualified current EIR'),dict(economic_id='principal-paid',primary=[atom('debt-financing',1,0,'200'),atom('debt-financing',1,1,'200')],witnesses=[[jr('foreign-currency',1)]],evidence='BANK-PRINCIPAL'),dict(economic_id='interest-paid',primary=[atom('debt-financing',1,0,'80'),atom('debt-financing',1,1,'80')],witnesses=[],evidence='BANK-INTEREST'),dict(economic_id='loan-fx',primary=[jr('foreign-currency',0)],witnesses=[],evidence='Monetary liability rate source')]
  for i,j in enumerate(completed('derivatives-hedge-accounting',o['derivatives-hedge-accounting'])['journal_entry_implications']):events.append(dict(economic_id='hedge-'+str(i),primary=[jr('derivatives-hedge-accounting',i)],witnesses=[],evidence='Qualified designated relationship allocation'))
  req['journal_account_mapping']=mapping;req['journal_ownership']=events
  req['journal_event_sources']=[dict(economic_id=e['economic_id'],entity=SCOPE['entity'],period=SPAN,currency='EUR',origin='bank' if e['economic_id'] in ('principal-paid','interest-paid') else 'loan' if e['economic_id'].startswith(('loan','interest-accrued')) else 'valuation',record='BANK-PRINCIPAL' if e['economic_id']=='principal-paid' else 'BANK-INTEREST' if e['economic_id']=='interest-paid' else 'loan' if e['economic_id'].startswith(('loan','interest-accrued')) else 'forward1',nature=e['economic_id']) for e in events]
  native=[dict(owner=i['value']['owner'],case_fingerprint=completed(i['value']['owner'],o[i['value']['owner']])['case_fingerprint'],journals=completed(i['value']['owner'],o[i['value']['owner']])['journal_entry_implications']) for i in prepared.proposal['issues']]
  req['journal_pack_review']=dict(preparer='Synthetic treasury preparer',reviewer='Synthetic independent event reviewer',approved=True,payload_fingerprint=digest(dict(mapping=mapping,native_owner_journals=native,journal_ownership=events,journal_event_sources=req['journal_event_sources'])))
 bindings=[Binding(id,FACT_ADAPTERS[f][0],path[1:] if path[0]=='__result__' else path,'owner_result' if path[0]=='__result__' else 'comparator' if id=='prior-interest' else 'current') for id,f,attribute,source,col,index,path,method in MAP if FACT_ADAPTERS[f][0] in wanted]
 populations=[PopulationBinding('bank','bank_id','cash-flow-reporting',('transactions',),'bank_id')] if 'cash-flow-reporting' in wanted else []
 documents=[DocumentBinding(id,pkg,('source_material',id)) for pkg,c in o.items() for id in c.get('source_material',{})]
 return ReviewedInputPack(req,bindings,populations,documents)

def flagship(clean=False,bounded=None,objective=OBJECTIVE):
 raw=sources(clean);engine=Intake(FixturePlanner(proposal(raw,objective,bounded)));p=engine.prepare(objective,raw,[],SCOPE);return engine,p,reviewed_pack(p,objective,bounded)

"""Deterministic source-to-CAO Treasury artifacts, with explicit bridge residuals."""
import copy,json
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from orchestration.tests.treasury_fixtures import flagship,sources
from orchestration.tests.generate_examples import internal_record
from orchestration.runtime import at,number
ROOT=Path(__file__).resolve().parents[2]

def bridge(opening,closing,components):
 change=number(closing)-number(opening);explained=sum((number(row['amount']) for row in components),Decimal(0))
 return dict(opening=str(opening),closing=str(closing),change=str(change),components=components,explained=str(explained),residual=str(change-explained))

def artifacts():
 engine,p,pack=flagship();r=engine.execute(p,pack);case=r.case
 assert case.outcome=='partial' and case.journal_mapping_valid
 owner={n['selected_skill']:n['result'] for n in case.workplan_nodes if n['status']=='complete'}
 d=owner['debt-financing']['calculations']['debt'][0];f=owner['foreign-currency']['calculations'];h=owner['derivatives-hedge-accounting']['calculations'];c=owner['cash-flow-reporting']['calculations'];a=owner['management-accounting-analytics']['calculations']['diagnostic']
 def component(label,n,owner,path,category):return dict(label=label,amount=str(n),owner=owner,result_path=path,category=category)
 db=bridge(d['opening'],f['transactions'][0]['closing'],[component('Effective interest',d['effective_interest'],'debt-financing',['debt',0,'effective_interest'],'accounting'),component('Cash interest',-number(d['cash_interest']),'debt-financing',['debt',0,'cash_interest'],'cash'),component('Principal repayment',-number(d['repayments']),'debt-financing',['debt',0,'repayments'],'cash'),component('Monetary FX remeasurement',-number(f['monetary_fx_profit']),'foreign-currency',['monetary_fx_profit'],'noncash')])
 cb=bridge(c['opening'],c['closing'],[component('Operating cash',c['direct_operating'],'cash-flow-reporting',['direct_operating'],'cash'),component('Investing cash',c['investing'],'cash-flow-reporting',['investing'],'cash'),component('Financing cash',c['financing'],'cash-flow-reporting',['financing'],'cash'),component('Cash FX',c['fx'],'cash-flow-reporting',['fx'],'noncash')])
 lineage=[]
 for fact,pkg,path,downstream,semantic in [('debt-open','debt-financing',['debt',0,'closing'],'financial-statements','debt_base'),('fx-rate','foreign-currency',['monetary_fx_profit'],'financial-statements','monetary_fx'),('hedge-value','derivatives-hedge-accounting',['derivatives','forward1','closing'],'financial-statements','derivative_balance'),('cash-principal','cash-flow-reporting',['financing'],'financial-statements','financing_cash')]:
  source=next(row for row in r.lineage if row.get('fact_id')==fact);handoff=next(row for row in case.handoff_ledger if row['producer']==case.graph.nodes.resolve(pkg) and row['consumer']==case.graph.nodes.resolve(downstream) and row['semantic']==semantic)
  lineage.append(dict(source=source,owner_result_path=path,owner_amount=str(at(owner[pkg]['calculations'],path)),downstream_handoff=handoff,final_public_amount=handoff['amount']))
 clean_e,clean_p,clean_pack=flagship(clean=True);clean=clean_e.execute(clean_p,clean_pack)
 return {
 'raw-source-pack.json':[asdict(s) for s in sources()],
 'source-inventory.json':[{k:v for k,v in row.items() if k!='fields'} for row in r.inventory],
 'extraction-ledger.json':[v for row in r.inventory for v in row['fields'].values()],
 'transformation-ledger.json':r.transformations,'semantic-proposal.json':r.proposal,'work-modes.json':case.work_modes,
 'fact-candidates.json':r.candidates,'conflict-register.json':r.conflicts,'material-questions.json':r.questions,
 'owner-input-candidates.json':r.owner_inputs,'source-owner-bindings.json':[asdict(b) for b in pack.bindings],
 'source-document-bindings.json':[asdict(b) for b in pack.documents],'source-population-bindings.json':[asdict(b) for b in pack.populations],
 'issue-register.json':case.accounting_issues,'workplan.json':case.workplan_nodes,'execution-ledger.json':case.execution_ledger,
 'owner-handoff-ledger.json':case.handoff_ledger,'event-journal-ownership-ledger.json':dict(ownership=case.journal_ownership_ledger,source_events=pack.request['journal_event_sources']),
 'debt-bridge.json':db,'interest-bridge.json':a['bridge'],'fx-bridge.json':f,
 'derivative-valuation-reference.json':h['derivatives'],'hedge-effectiveness.json':h['effectiveness'],'hedge-reserve.json':h['hedge_reserves'],
 'cash-bridge.json':cb,'financing-cash-bridge.json':bridge('0',c['financing'],[component('Gross principal payment',-number(d['repayments']),'debt-financing',['debt',0,'repayments'],'cash')]),
 'cash-noncash-reconciliation.json':dict(debt_movement=db['change'],cash_principal_movement=str(-number(d['repayments'])),noncash_debt_fx=str(-number(f['monetary_fx_profit'])),cash_interest=str(d['cash_interest']),accounting_interest=str(d['effective_interest']),derivative_fv=str(h['derivatives'][0]['change']),derivative_settlement=str(h['derivatives'][0]['settlement']),residual='0'),
 'debt-classification.json':dict(base_current=str(d['current']),fx_current=str(-number(f['monetary_fx_profit'])),current='880',noncurrent=str(d['noncurrent']),rights='Qualified reporting-date rights and covenant compliance; no waiver inferred'),
 'reconciliation-summary.json':dict(owner=owner['balance-sheet-reconciliations']['calculations'],source_conflicts=r.conflicts,status='PARTIAL: owner workpapers tie; cash flow support omits principal payment'),
 'reporting-result.json':owner['financial-statements']['calculations'],'management-hypothesis.json':r.hypothesis_results,
 'diagnostic-synthesis.json':dict(diagnostic=a,accounting=case.conclusions,economic='Principal unchanged over interest interval; supplied EIR increased from 6% to 8%; attribution is evidence-bound',cash='Interest80 operating, principal200 financing',process='Cash flow summary omits payment200'),
 'accounting-escalation.json':case.accounting_questions,'challenge-result.json':case.challenge_results,
 'final-case.internal.json':internal_record(case),'final-public-answer.json':engine.public(r),
 'clean-control-public-answer.json':clean_e.public(clean),'clean-control-status.json':dict(outcome=clean.case.outcome,status=clean.case.status),
 'memory-candidates.json':r.memory_candidates+case.memory_candidates,'end-to-end-lineage.json':lineage}

def main():
 target=ROOT/'orchestration/examples/treasury-financing';target.mkdir(parents=True,exist_ok=True)
 for name,data in artifacts().items():(target/name).write_text(json.dumps(data,sort_keys=True,indent=2,default=str)+'\n')
if __name__=='__main__':main()

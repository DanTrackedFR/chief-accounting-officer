"""Deterministic governed Group Case artifacts; no native approvals outside fixtures."""
import json
from pathlib import Path
from dataclasses import asdict
from decimal import Decimal
from orchestration.tests.group_fixtures import *
from orchestration.tests.generate_examples import internal_record
from orchestration.runtime import CAO, number, at
ROOT=Path(__file__).resolve().parents[2]


def bridge(opening,closing,components):
    explained=sum((number(v['amount']) for v in components),Decimal(0))
    return dict(opening=str(opening),closing=str(closing),components=components,explained=str(explained),residual=str(number(closing)-number(opening)-explained))


def artifacts():
    sources=group_sources();engine=Intake(FixturePlanner(group_proposal(sources)));prepared=engine.prepare(OBJECTIVE,sources,[],SCOPE);pack=group_review_pack(prepared)
    result=engine.execute(prepared,pack);case=result.case
    clean=run(True);assert (case.outcome,case.status)==('partial','DOCUMENTED');assert (clean.case.outcome,clean.case.status)==('complete','CLOSED')
    owners={n['selected_skill']:n['result'] for n in case.workplan_nodes if n['status']=='complete' and n['issue']!='diagnostic accounting follow-up'}
    calcs={p:r['calculations'] for p,r in owners.items()};bc=calcs['business-combinations'];fx=calcs['foreign-currency']['translation'];cons=calcs['consolidation'];nci=cons['nci'][0];imp=calcs['asset-impairment'];tax=calcs['income-taxes']
    def component(label,amount,owner,path):return dict(label=label,amount=str(amount),owner=owner,result_path=path)
    fx_input=pack.request['facts']['foreign_operation']['translation'];cons_input=pack.request['facts']['group_structure']
    acquisition_rate=number(fx_input['opening_rate']);acquisition_goodwill_eur=number(bc['initial_goodwill'])*acquisition_rate
    nci_open=number(cons_input['nci'][0]['opening'])
    parent=next(e['balances'] for e in cons_input['entities'] if e['id']==PARENT)
    parent_profit=-number(parent['parent revenue'])-number(parent['parent expense'])
    acquisition=bridge('0',bc['initial_goodwill'],[component('Consideration',bc['consideration'],'business-combinations',['consideration']),component('Initial full-goodwill NCI',bc['nci'],'business-combinations',['nci']),component('Identifiable assets',-number(bc['assets']),'business-combinations',['assets']),component('Identifiable liabilities including acquisition DTL',bc['liabilities'],'business-combinations',['liabilities'])])
    nb=bridge(nci_open,nci['closing'],[component('Post-acquisition profit',nci['profit'],'consolidation',['nci',0,'profit']),component('Post-acquisition OCI',nci['oci'],'consolidation',['nci',0,'oci'])])
    cb=bridge(fx['opening_net_translated'],fx['closing_net_translated'],[component('Qualified post-acquisition profit',fx['profit_translated'],'foreign-currency',['translation','profit_translated']),component('Translation OCI',fx['cta_movement'],'foreign-currency',['translation','cta_movement'])])
    gb=bridge(acquisition_goodwill_eur,cons['consolidated_balances']['goodwill'],[component('Foreign-operation goodwill currency movement',number(cons['consolidated_balances']['goodwill'])-acquisition_goodwill_eur,'foreign-currency',['translation','translated_tb','goodwill']),component('Supported goodwill impairment',-number(imp['loss']),'asset-impairment',['loss'])])
    eb=bridge(cons['equity']['opening'],cons['equity']['closing'],[component('Group profit',cons['equity']['profit'],'consolidation',['equity','profit']),component('Group OCI',cons['equity']['oci'],'consolidation',['equity','oci']),component('Acquisition NCI',cons['equity']['owner_transactions'],'consolidation',['equity','owner_transactions'])])
    pb=bridge('0',cons['equity']['profit'],[component('Parent standalone contribution',parent_profit,'consolidation',['consolidated_balances','parent revenue']),component('Qualified subsidiary post-acquisition contribution',fx['profit_translated'],'foreign-currency',['translation','profit_translated']),component('Loan balance elimination has no profit effect','0','consolidation',['consolidated_balances','IC receivable']),component('Impairment',-number(imp['loss']),'asset-impairment',['loss'])])
    sources_by_entity={e['id']:e['balances'] for e in pack.request['facts']['group_structure']['entities']}
    replay={}
    for balances in sources_by_entity.values():
        for account,value in balances.items():replay[account]=replay.get(account,Decimal(0))+number(value)
    source_population=dict(replay)
    for journal in case.conclusions[0]['journals']:
        for line in journal['lines']:replay[line['account']]=replay.get(line['account'],Decimal(0))+number(line['amount'])*(1 if line['side']=='Dr' else -1)
    residual={k:str(replay.get(k,Decimal(0))-number(v)) for k,v in cons['consolidated_balances'].items()}
    assert all(number(v)==0 for v in residual.values())
    lineage=[]
    for fact,owner,path,consumer,semantic in [('bc-price','business-combinations',['initial_goodwill'],'consolidation','acquisition_basis'),('tax-carrying','income-taxes',['jurisdictions',0,'dtl'],'business-combinations','acquisition_dtl'),('fx-close','foreign-currency',['translation','cta_movement'],'consolidation','nci_oci'),('ic-a','intercompany-accounting',['pairs',0,'a_functional'],'consolidation','matched_intercompany'),('imp-gw','asset-impairment',['loss'],'consolidation','impairment')]:
        binding=next(r for r in result.lineage if r.get('fact_id')==fact)
        handoff=next(r for r in case.handoff_ledger if r['producer']==case.graph.nodes.resolve(owner) and r['consumer']==case.graph.nodes.resolve(consumer) and r['semantic']==semantic)
        public_metric={'business-combinations':'group_goodwill','income-taxes':'group_deferred_tax_liability','foreign-currency':'translation_oci','intercompany-accounting':'qualified_intercompany_elimination','asset-impairment':'goodwill_test_loss'}[owner]
        fs_path={'business-combinations':['current','lines','goodwill'],'income-taxes':['current','lines','Deferred tax liability'],'foreign-currency':['current','oci'],'intercompany-accounting':['current','lines','IC receivable'],'asset-impairment':['current','lines','goodwill']}[owner]
        lineage.append(dict(public_metric=public_metric,public_amount=case.conclusions[0]['calculations'][public_metric],financial_statement_path=fs_path,financial_statement_amount=str(at(calcs['financial-statements'],fs_path)),source=binding,specialist_result_path=path,amount=str(at(calcs[owner],path)),handoff=handoff,downstream='Qualified consolidated population -> financial statements -> public_record'))
    def result_reference(result):
        return {k:v for k,v in result.items() if k not in ('facts_used','reviewed_claims','knowledge_documents','evidence')}
    return {
        'raw-source-pack.json':[asdict(s) for s in sources],
        'source-inventory.json':[{k:v for k,v in row.items() if k!='fields'} for row in result.inventory],
        'extraction-ledger.json':[v for row in result.inventory for v in row['fields'].values()],
        'transformation-ledger.json':result.transformations,'semantic-proposal.json':result.proposal,'work-modes.json':case.work_modes,
        'fact-candidates.json':result.candidates,'conflict-register.json':result.conflicts,'material-questions.json':result.questions,
        'owner-input-candidates.json':result.owner_inputs,'source-owner-bindings.json':[asdict(b) for b in pack.bindings],
        'source-document-bindings.json':[asdict(b) for b in pack.documents],'source-text-assertions.json':[asdict(b) for b in pack.text_assertions],'source-population-bindings.json':[asdict(b) for b in pack.populations],
        'group-structure.json':SCOPE,'acquisition-bridge.json':acquisition,'business-combination-result.json':result_reference(owners['business-combinations']),
        'tax-handoff.json':[r for r in case.handoff_ledger if r['producer']=='income-taxes'],
        'nci-bridge.json':nb,'fx-translation.json':fx,'cta-bridge.json':cb,
        'intercompany-reconciliation.json':dict(source_parent='105',reciprocal_translated='100',qualified_matched='100',unresolved_residual='5',disposition='Material discrepancy is unresolved; qualified workpapers remain provisional',owner=calcs['intercompany-accounting']),
        'elimination-ledger.json':[j for j in case.conclusions[0]['journals']],
        'impairment-result.json':result_reference(owners['asset-impairment']),'goodwill-bridge.json':gb,
        'group-tax-bridge.json':bridge(number(tax['jurisdictions'][0]['dtl'])*acquisition_rate,-number(cons['consolidated_balances']['Deferred tax liability']),[component('Acquisition DTL currency movement',-number(cons['consolidated_balances']['Deferred tax liability'])-number(tax['jurisdictions'][0]['dtl'])*acquisition_rate,'foreign-currency',['translation','translated_tb','Deferred tax liability'])]),
        'consolidated-equity-bridge.json':eb,'group-profit-bridge.json':pb,
        'consolidation-bridge.json':dict(sources=sources_by_entity,source_population=source_population,adjustments=case.conclusions[0]['journals'],final=cons['consolidated_balances'],account_residuals=residual,residual='0'),
        'consolidated-statements.json':calcs['financial-statements'],'disclosure-result.json':result_reference(owners['disclosure-management']),
        'group-analytics.json':calcs['management-accounting-analytics'],'management-hypothesis.json':case.diagnostics[0]['hypotheses'],
        'accounting-escalation.json':case.accounting_questions,'owner-handoff-ledger.json':case.handoff_ledger,
        'economic-event-ledger.json':case.journal_ownership_ledger,'execution-ledger.json':case.execution_ledger,'workplan.json':internal_record(case)['workplan_nodes'],
        'challenge-result.json':case.challenge_results,'end-to-end-lineage.json':lineage,
        'final-case.internal.json':internal_record(case),'final-public-answer.json':engine.public(result),
        'clean-control-public-answer.json':CAO().public(clean.case),'clean-control-status.json':dict(outcome=clean.case.outcome,status=clean.case.status),
        'memory-candidates.json':result.memory_candidates+case.memory_candidates,
    }


def main():
    target=ROOT/'orchestration/examples/group-accounting';target.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts().items():(target/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')
if __name__=='__main__':main()

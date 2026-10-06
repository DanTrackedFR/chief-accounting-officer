"""Reproducible internal artifacts; no persistence or real approval generation."""
import copy
import json
from pathlib import Path
from orchestration.tests.intake_fixtures import factory,factory_review_pack,ap_control,contract_control,factory_sources


def compact_case(case):
    from orchestration.tests.generate_examples import internal_record
    record=internal_record(case)
    # Native owner workpapers are deterministically reproducible from fixture code,
    # not embedded repeatedly in every artifact. Keep result authority/dimensions,
    # calculations and open work; fingerprints remain internal references.
    for node in record['workplan_nodes']:
        result=node.get('result')
        if result:
            node['result']={k:copy.deepcopy(result[k]) for k in ('skill_id','status','case_fingerprint','conclusion','calculations','open_items') if k in result}
        from orchestration.runtime import digest
        evidence=node.get('evidence',[])
        node['evidence']=[dict(native_evidence_fingerprint=digest(evidence),reproduce='orchestration.tests.intake_fixtures.factory_review_pack')] if evidence else []
        node['invalidated_results']=[]
    record['knowledge_refs']=[]
    record['evidence_refs']=[]
    return record


def artifacts():
    intake,p=factory();intake.execute(p,factory_review_pack(p))
    out={}
    names={'inventory':'source-inventory','transformations':'transformation-ledger','proposal':'semantic-proposal','candidates':'fact-candidate-register','conflicts':'conflict-register','questions':'material-questions','owner_inputs':'owner-input-candidates','lineage':'source-owner-lineage','hypothesis_results':'hypothesis-results','memory_candidates':'context-candidates'}
    for key,name in names.items():out['factory-'+name+'.json']=copy.deepcopy(getattr(p,key))
    out['factory-raw-inputs.json']=[dict(id=r.id,name=r.name,format=r.format,payload=r.payload,metadata=r.metadata,mime=r.mime,raw_ref=r.raw_ref) for r in factory_sources()]
    out['factory-extraction-ledger.json']=[item for source in p.inventory for item in source['ledger']]
    out['factory-work-mode.json']=p.case.work_modes
    out['factory-issue-register.json']=p.case.accounting_issues
    out['factory-workplan.json']=compact_case(p.case)['workplan_nodes']
    out['factory-execution-ledger.json']=p.case.execution_ledger
    out['factory-final-case.json']=compact_case(p.case)
    out['factory-public-answer.json']=intake.public(p)
    out['factory-diagnostic.json']=p.case.diagnostics
    out['factory-accounting-escalation.json']=p.case.accounting_questions
    for name,fn in [('contract',contract_control),('ap',ap_control)]:
        engine,r=fn();out[name+'-candidate-register.json']=r.candidates
        out[name+'-final-case.json']=compact_case(r.case);out[name+'-public-answer.json']=engine.public(r)
    return out

if __name__=='__main__':
    destination=Path(__file__).resolve().parents[1]/'examples/intake';destination.mkdir(exist_ok=True)
    for name,value in artifacts().items():(destination/name).write_text(json.dumps(value,indent=2,sort_keys=True,default=str)+'\n')

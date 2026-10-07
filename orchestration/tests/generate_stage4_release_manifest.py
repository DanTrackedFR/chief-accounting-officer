"""Record measured release gates; refuses missing or failed suite logs."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def generate(log_root):
    logs=Path(log_root)
    suites={
        'orchestration':'stage4_orchestration_release2.log',
        'complete_temporal_artifact_reproduction':'stage4_temporal_artifact_test.log',
        'production_skills':'stage4_skills_release2.log',
        'leases':'stage4_lease_release.log',
        'repository_canonical':'stage4_repo_release.log',
    }
    evidence={}
    for name,filename in suites.items():
        output=(logs/filename).read_text()
        count=re.search(r'Ran (\d+) tests? in ',output)
        if not count or not output.rstrip().endswith('OK') or 'FAILED (' in output:raise ValueError(f'{name}: release gate has not passed')
        evidence[name]={'distinct_methods':int(count[1]),'result':'PASS'}
    supplemental=json.loads((logs/'stage4_supplement_results.json').read_text())
    if any(item['exit_code']!=0 for item in supplemental):raise ValueError('Supplemental suite/validator failure')
    evidence['supplemental_independent_knowledge']={'distinct_methods':sum(item['tests'] or 0 for item in supplemental),'result':'PASS'}
    validators={name:json.loads((logs/file).read_text()) for name,file in [('canonical_approvals','stage4_approvals_final.json'),('standards_evidence','stage4_standards_final.json')]}
    if any(v['errors']!=0 for v in validators.values()):raise ValueError('Canonical validator failure')
    if 'Zero unresolved substantive findings' not in (ROOT/'orchestration/STAGE4-FINAL-INDEPENDENT-QA.md').read_text():raise ValueError('Independent acceptance not recorded')
    target=ROOT/'orchestration/examples/multi-entity-multi-period-temporal-model'
    actual={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.glob('*.json'))}
    if actual!=json.loads((logs/'stage4_final_hashes19.json').read_text()):raise ValueError('Final artifacts differ from seed19/941 verified inventory')
    record={
        'starting_sha':'1c480514e4ce36df8f1c85ee68f9b5821cf6905e',
        'suites':evidence,
        'distinct_tests':sum(item['distinct_methods'] for item in evidence.values()),
        'reruns_and_subtests_not_added':True,
        'independent_stage4_methods_already_in_orchestration_total':183,
        'unresolved_substantive_independent_findings':0,
        'deterministic_artifacts':{'hash_seeds':[19,941],'sha256':actual,'result':'PASS'},
        'migration_coverage':['Stage1','Stage2','Stage3','Group Accounting','Treasury','SaaS','Semantic/Data Intake','Diagnostic Analytics','Manufacturing','ordinary single entity'],
        'validators':{name:{'errors':value['errors'],'result':'PASS'} for name,value in validators.items()},
        'exact_head_ci':'Recorded on existing PR37 after repository freeze; this manifest does not claim CI',
    }
    (ROOT/'orchestration/STAGE4-RELEASE-REGRESSION.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')

if __name__=='__main__':generate(sys.argv[1])

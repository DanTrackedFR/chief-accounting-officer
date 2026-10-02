"""Governed execution boundary shared by the four accounting workflows.

Case conclusions are reviewed accounting inputs, never inferred company facts.
Evidence stays internal; only curated outputs cross the application boundary.
"""
import hashlib
import importlib.util
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from core_accounting import ReviewRequired, approved_claims, balance, context, dec, required
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from interfaces.public_output import public_record

PACKAGES = {
    'revenue-recognition': ('SKILL-REV-001', ['TOPIC-03-001','TOPIC-03-002','TOPIC-03-003','TOPIC-03-004','TOPIC-03-005','TOPIC-03-006','TOPIC-03-012']),
    'financial-instruments-ecl': ('SKILL-ECL-001', ['TOPIC-06-007','TOPIC-06-008','TOPIC-06-009','TOPIC-06-010','TOPIC-03-008','TOPIC-03-009']),
    'provisions-contingencies': ('SKILL-PROV-001', ['TOPIC-05-003','TOPIC-05-004','TOPIC-13-005','TOPIC-15-004']),
    'consolidation': ('SKILL-CONS-001', ['TOPIC-07-%03d'%i for i in range(1,10)]+['TOPIC-13-001']),
}

def flag(obj, key):
    required(obj, key)
    if type(obj[key]) is not bool:
        raise ReviewRequired(key+' must be an evidenced boolean')
    return obj[key]

def nonnegative(value):
    n = dec(value)
    if n < 0: raise ReviewRequired('Negative amount is not valid for this input')
    return n

def fraction(value):
    n = dec(value)
    if not 0 <= n <= 1: raise ReviewRequired('Fraction outside [0,1]')
    return n

def dates(case):
    required(case, 'period_start','reporting_period','entity_type','policy_elections','evidence','judgment_memo','assumptions')
    try:
        start=date.fromisoformat(case['period_start']); end=date.fromisoformat(case['reporting_period'])
    except (ValueError,TypeError) as exc: raise ReviewRequired('Use ISO reporting dates') from exc
    if start>end: raise ReviewRequired('Period start exceeds reporting date')
    if not isinstance(case['assumptions'],list) or not isinstance(case['policy_elections'],dict):
        raise ReviewRequired('Assumptions array and policy election object required')
    if case['framework']=='UK_GAAP' and case['uk_standard']!='FRS_102':
        raise ReviewRequired('FRS 101/105 require separate framework workflow')
    if case['framework']=='AASB':
        if case['reporting_tier'] not in (1,2): raise ReviewRequired('Resolve Australian reporting tier')
        if case['entity_type']!='for_profit':
            raise ReviewRequired('Australian NFP/public-sector overlay requires specialist scope assessment')
    required(case,'applicability_review')
    review=case['applicability_review']
    required(review,'reviewer','standard_versions','effective_period','entity_scope','exceptions')
    if review['effective_period'] != [case['period_start'],case['reporting_period']]:
        raise ReviewRequired('Applicability review does not cover this period')
    if review['entity_scope'] != case['entity_type']: raise ReviewRequired('Applicability review scope mismatch')
    if not isinstance(review['exceptions'],list): raise ReviewRequired('Applicability exceptions must be an array')
    return start

def load_workflow(package):
    spec=importlib.util.spec_from_file_location(package.replace('-','_')+'_workflow',ROOT/'skills'/package/'workflow.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def canonical_knowledge(topic_ids, framework):
    claims=approved_claims(topic_ids,framework)
    manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']
    documents=[]
    for tid in topic_ids:
        t=next(x for x in manifest if x['topic_id']==tid)
        # Canonical methods added during remediation may not occur in the old artifact list.
        claim_path=next(ROOT/p for p in t['artifact_paths'] if p.endswith('/standards-claims.json'))
        paths=set(claim_path.parent.glob('*.md'))
        paths.update(ROOT/p for p in t['artifact_paths'] if p.endswith('.md'))
        for p in sorted(paths):
            documents.append({'topic_id':tid,'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return claims,documents

def execute(package, case):
    if package not in PACKAGES: raise ReviewRequired('Unknown accounting skill')
    context(case); dates(case)
    claims,knowledge=canonical_knowledge(PACKAGES[package][1],case['framework'])
    required(case,'knowledge_review')
    reviewed=case['knowledge_review']
    required(reviewed,'reviewer','claim_ids','documents')
    if set(reviewed['claim_ids']) != {c['claim_id'] for c in claims}:
        raise ReviewRequired('Knowledge review must cover current applicable claim population')
    if reviewed['documents'] != knowledge:
        raise ReviewRequired('Canonical knowledge changed or has not been reviewed')
    result=load_workflow(package).assess(case,claims)
    for entry in result.get('journal_entry_implications',[]): balance(entry)
    result.update(skill_id=PACKAGES[package][0],framework=case['framework'],jurisdiction=case['jurisdiction'],
        entities=[case['entity']],periods=[case['period_start'],case['reporting_period']],
        facts_used={k:v for k,v in case.items() if k not in ('assumptions','knowledge_review','reviewer_signoff')},
        assumptions=case['assumptions'], evidence=claims,knowledge_documents=knowledge,
        recommendation_class='REQUIRED',confidence='medium',memory_candidates=[],related_artifacts=[],
        controls_impacted=['Source population to GL tie-out','Independent route, estimate and journal review','Versioned accounting policy and disclosure review'],
        reporting_impacted=['Framework-specific statement presentation and comparative-period consistency'],
        systems_impacted=['Retain case ID, source IDs, policy version, rule route and journal lineage'],
        documentation_required=['Accounting judgment memo','Input evidence','Calculation and reconciliation','Disclosure tie-out','Reviewer certification'],
        audit_evidence_required=['Contract/legal/source evidence','Assumptions and alternatives','Calculation reperformance','Approval record'])
    fingerprint=case_fingerprint(case)
    result['case_fingerprint']=fingerprint
    signoff=case.get('reviewer_signoff',{})
    valid=(signoff.get('case_fingerprint')==fingerprint and bool(signoff.get('reviewer')) and
           signoff.get('reviewer')!=case.get('preparer') and signoff.get('approved') is True)
    result['status']='complete' if valid and not result.get('open_items') else 'partial'
    if not valid: result.setdefault('open_items',[]).append('Independent reviewer must approve this exact case fingerprint before use')
    return result

def case_fingerprint(case):
    return hashlib.sha256(json.dumps({k:v for k,v in case.items() if k!='reviewer_signoff'},sort_keys=True,default=str).encode()).hexdigest()

def to_public(result, route='answer'):
    citations=[]
    for claim in result['evidence']:
        for ref in claim.get('references',[]):
            if isinstance(ref,str):
                confirmed=claim.get('reference_confidence')=='VERIFIED'
                locator=ref if confirmed else 'Unverified paragraph reference: '+ref
                citations.append({'title':claim['topic_id'],'locator':locator})
    # Never copy internal evidence limitations or arbitrary case text to public output.
    rec={'topic_id':result['evidence'][0]['topic_id'],'guidance':result['conclusion'],
         'framework':result['framework'],'jurisdiction':result['jurisdiction'],
         'entity_scope':result['entities'][0],'effective_period':' to '.join(result['periods']),
         'limitations':result.get('uncertainties',[]),'uncertainties':result.get('open_items',[]),'citations':citations}
    return public_record(rec,route=route)

def serializable(obj):
    if isinstance(obj,Decimal): return str(obj)
    raise TypeError(type(obj).__name__)

"""Dedicated Insurance Contracts namespace validation, independent of historical denominator."""
import json
import hashlib
import re
import sys
from datetime import date
import importlib.util
from pathlib import Path
_local_name='_cao_insurance_contracts_retrieval'
if _local_name not in sys.modules:
    _spec=importlib.util.spec_from_file_location(_local_name,Path(__file__).with_name('retrieval.py'))
    _module=importlib.util.module_from_spec(_spec);sys.modules[_local_name]=_module;_spec.loader.exec_module(_module)
_local=sys.modules[_local_name]
FRAMEWORKS,SCOPES,load_register,PUBLIC_FIELDS=_local.FRAMEWORKS,_local.SCOPES,_local.load_register,_local.PUBLIC_FIELDS
EVIDENCE={'SOURCE_VERIFIED','PRIMARY_CORROBORATED','SECONDARY_CORROBORATED','MODEL_DERIVED_AUDIT_REQUIRED'}
EXPECTED_DECISIONS=json.loads(Path(__file__).with_name('expected-decisions.json').read_text())
TRACKS={'PENDING','DIRECT_SOURCE_CHECKED','TRAINING_DATA_CHECKED'}
REQUIRED={'claim_id','framework','decision','claim_kind','proposition','source','sources','evidence_status','reference_confidence','audit_required','approval_track','approval_review','effective_period','period_scope','entity_scope','limitations','tests','source_note','public_limitations'}

def claim_hash(c):
    reviewed={k:v for k,v in c.items() if k not in {'approval_track','approval_review','reviewer','review_date','proposed_approval_track'}}
    return hashlib.sha256(json.dumps(reviewed,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate_data(d):
    errors=[]
    if not isinstance(d,dict):return ['Invalid register object']
    if d.get('namespace')!='SUPPLEMENTAL_INSURANCE_CONTRACTS':errors.append('Invalid namespace')
    if d.get('status') not in {'REVIEWED','APPROVED'}:errors.append('Invalid register status')
    if any(k in d for k in ('topic_id','canonical_mappings','capability_mappings')):errors.append('Fabricated canonical mapping')
    claims=d.get('claims')
    if not isinstance(claims,list) or not claims:return errors+['Missing claims population']
    ids=[];decisions=[]
    for c in claims:
        if not isinstance(c,dict):errors.append('Invalid claim');continue
        cid=c.get('claim_id','missing');label=str(cid)+': '
        ids.append(cid)
        missing=REQUIRED-set(c)
        if missing:errors.append(label+'missing '+','.join(sorted(missing)))
        fw=c.get('framework')
        if fw not in FRAMEWORKS or not isinstance(cid,str) or not re.fullmatch('INS-'+str(fw)+'-[0-9]{3}',cid):errors.append(label+'invalid framework/ID')
        decisions.append((str(fw),str(c.get('decision'))))
        if not isinstance(c.get('decision'),str) or not c['decision']:errors.append(label+'invalid decision')
        for k in ('source','source_note'):
            if not isinstance(c.get(k),str) or not c[k]:errors.append(label+'invalid '+k)
        if c.get('entity_scope')!=SCOPES.get(fw):errors.append(label+'unsupported entity scope')
        if not isinstance(c.get('proposition'),str) or not c['proposition'].strip():errors.append(label+'empty proposition')
        if c.get('evidence_status') not in EVIDENCE:errors.append(label+'invalid evidence')
        if c.get('reference_confidence') not in {'VERIFIED','PROVISIONAL','UNKNOWN'}:errors.append(label+'invalid reference confidence')
        if type(c.get('audit_required')) is not bool:errors.append(label+'invalid audit flag')
        if c.get('approval_track') not in TRACKS:errors.append(label+'invalid approval track')
        if c.get('claim_kind') not in {'NORMATIVE','GOVERNANCE'}:errors.append(label+'invalid claim kind')
        for k in ('limitations','tests','public_limitations'):
            if not isinstance(c.get(k),list) or not c[k] or any(not isinstance(x,str) or not x for x in c[k]):errors.append(label+'invalid '+k)
        ps=c.get('period_scope')
        try:
            bounds=[date.fromisoformat(ps[k]) for k in ('begin_on_or_after','begin_before','end_before')]
            if bounds!=[date(2026,1,1),date(2027,1,1),date(2027,1,1)]:raise ValueError()
        except (ValueError,TypeError,KeyError):errors.append(label+'invalid effective period bounds')
        if not isinstance(c.get('effective_period'),str) or '2026' not in c['effective_period']:errors.append(label+'missing effective period')
        src=c.get('sources')
        if not isinstance(src,list) or not src:errors.append(label+'missing source structure');src=[]
        for s in src:
            if not isinstance(s,dict) or not s.get('title') or s.get('source_kind') not in {'CURRENT_STANDARD','OFFICIAL_AMENDMENT','OTHER','MODEL_KNOWLEDGE','PROFESSIONAL_LITERATURE','REGULATOR'} or type(s.get('inspected')) is not bool:
                errors.append(label+'malformed source');continue
            if s.get('source_kind')=='MODEL_KNOWLEDGE' and (s.get('locator') or s.get('inspected')):errors.append(label+'fabricated model inspection')
        direct=c.get('evidence_status')=='SOURCE_VERIFIED'
        if direct:
            if c.get('audit_required') is not False or c.get('reference_confidence')!='VERIFIED' or not any(isinstance(s,dict) and s.get('source_kind')=='CURRENT_STANDARD' and s.get('inspected') and s.get('url') and s.get('locator') for s in src):errors.append(label+'unsupported direct-source assurance')
        elif c.get('audit_required') is not True:errors.append(label+'direct audit flag missing')
        if direct and fw=='AASB':
            windows={tuple(s.get('operative_period_start',{}).get(k) for k in ('on_or_after','before')) for s in src if isinstance(s,dict) and isinstance(s.get('operative_period_start'),dict)}
            if not {('2023-01-01','2026-07-01'),('2026-07-01','2027-01-01')}<=windows:errors.append(label+'missing operative AASB compilation windows')
        if c.get('evidence_status')=='MODEL_DERIVED_AUDIT_REQUIRED' and c.get('paragraph_references'):errors.append(label+'fabricated model paragraph')
        if any(k in c for k in ('topic_id','capability_ids','canonical_mappings')):errors.append(label+'fabricated canonical mapping')
        if 'TOPIC-' in json.dumps(c):errors.append(label+'canonical topic masquerade')
        if c.get('approval_track')=='PENDING' and c.get('approval_review') is not None:errors.append(label+'author self-approval inconsistent')
        if d.get('status')=='APPROVED':
            r=c.get('approval_review')
            if not isinstance(r,dict):r={}
            if r.get('result')!='PASS' or not all(r.get(k) is True for k in ('scope_and_period_checked','cross_framework_checked','regression_checked')) or not r.get('reviewer') or r.get('reviewer')==d.get('author') or not r.get('date') or c.get('approval_track')=='PENDING':errors.append(label+'independent approval missing')
            if c.get('approval_track')=='DIRECT_SOURCE_CHECKED' and not direct:errors.append(label+'direct approval without operative verification')
            if c.get('approval_track')=='TRAINING_DATA_CHECKED' and (direct or not isinstance(c.get('source_note'),str) or 'Source: ChatGPT training data' not in c['source_note']):errors.append(label+'invalid training-data provenance')
            if c.get('approval_track')=='DIRECT_SOURCE_CHECKED' and (not isinstance(c.get('source_note'),str) or not c['source_note'].startswith('Source: ') or 'ChatGPT training data' in c['source_note']):errors.append(label+'invalid direct-source provenance')
            if r.get('reviewed_hash')!=claim_hash(c):errors.append(label+'stale claim approval')
        public={k:c.get(k) for k in PUBLIC_FIELDS}
        rendered=json.dumps(public).lower()
        if any(x in rendered for x in ('source:','source_verified','training_data_checked','audit_required','reference_confidence','approval_track','approval_review')):errors.append(label+'public provenance leakage')
    if len(ids)!=len(set(str(x) for x in ids)):errors.append('Duplicate claim IDs')
    if len(decisions)!=len(set(decisions)):errors.append('Duplicate framework decision')
    for fw in sorted(FRAMEWORKS):
        if not any(isinstance(c,dict) and c.get('framework')==fw for c in claims):errors.append('Missing framework '+fw)
    if len(claims)!=168:errors.append('Incomplete reviewed claim population')
    for fw in FRAMEWORKS:
        actual={c.get('decision') for c in claims if isinstance(c,dict) and c.get('framework')==fw}
        if actual!=set(EXPECTED_DECISIONS[fw]):errors.append('Incomplete reviewed decisions '+fw)
    return errors

def validate(path=None):
    try:d=load_register(path)
    except (ValueError,TypeError,KeyError,OSError) as e:return {'claims':0,'errors':[str(e)]}
    return {'claims':len(d['claims']),'frameworks':{fw:sum(c['framework']==fw for c in d['claims']) for fw in sorted(FRAMEWORKS)},'status':d.get('status'),'errors':validate_data(d)}
if __name__=='__main__':
    r=validate();print(json.dumps(r,indent=2));sys.exit(bool(r['errors']))

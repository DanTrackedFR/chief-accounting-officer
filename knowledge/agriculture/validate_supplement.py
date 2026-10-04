#!/usr/bin/env python3
"""Separate Agriculture namespace gate; no fabricated canonical topic IDs."""
import json
import sys
from retrieval import load_register, FRAMEWORKS

def validate(path=None):
    errors=[]
    try: d=load_register(path)
    except (ValueError,KeyError,TypeError) as e: return {'claims':0,'errors':[str(e)]}
    for fw in FRAMEWORKS:
        if not any(c.get('framework')==fw for c in d['claims']): errors.append('Missing framework '+fw)
    for c in d['claims']:
        cid=c.get('claim_id','missing')
        for k in ('decision','proposition','effective_period','entity_scope','evidence_status','reference_confidence','source','sources','audit_required','limitations','approval_track','approval_review'):
            if k not in c: errors.append(cid+': missing '+k)
        if c.get('framework') not in FRAMEWORKS or not cid.startswith('AGR-'+c.get('framework','')+'-'): errors.append(cid+': invalid framework ID')
        if c.get('evidence_status')=='SOURCE_VERIFIED':
            if c.get('audit_required') is not False or c.get('reference_confidence')!='VERIFIED' or not any(s.get('inspected') and s.get('source_kind')=='CURRENT_STANDARD' and s.get('locator') and s.get('url') for s in c.get('sources',[])): errors.append(cid+': unsupported direct-source claim')
        elif c.get('audit_required') is not True: errors.append(cid+': direct audit flag missing')
        if c.get('evidence_status')=='MODEL_DERIVED_AUDIT_REQUIRED' and c.get('paragraph_references'): errors.append(cid+': invented model locator')
        if c.get('approval_track')=='PENDING' and c.get('approval_review') is not None: errors.append(cid+': author approval inconsistent')
        if d.get('status')=='APPROVED':
            r=c.get('approval_review') or {}
            if r.get('result')!='PASS' or not all(r.get(k) is True for k in ('scope_and_period_checked','cross_framework_checked','regression_checked')) or not r.get('reviewer') or not r.get('date') or c.get('approval_track')=='PENDING': errors.append(cid+': independent approval missing')
            if c.get('approval_track')=='TRAINING_DATA_CHECKED' and 'ChatGPT training data' not in c.get('source_note',''): errors.append(cid+': training-data source note missing')
    return {'claims':len(d['claims']),'frameworks':{fw:sum(c['framework']==fw for c in d['claims']) for fw in sorted(FRAMEWORKS)},'status':d.get('status'),'errors':errors}
if __name__=='__main__':
    r=validate(); print(json.dumps(r,indent=2));sys.exit(bool(r['errors']))

"""Approved, context-bounded supplemental Agriculture retrieval; internal provenance excluded."""
import json
from datetime import date
from pathlib import Path
HERE=Path(__file__).resolve().parent
FRAMEWORKS={'IFRS','US_GAAP','UK_GAAP','AASB'}
PUBLIC_FIELDS=('claim_id','framework','decision','proposition','entity_scope','effective_period','public_limitations')

def load_register(path=None):
    data=json.loads(Path(path or HERE/'standards-claims.json').read_text())
    if data.get('namespace')!='SUPPLEMENTAL_AGRICULTURE':
        raise ValueError('Unrecognized supplemental Agriculture namespace')
    ids=[c.get('claim_id') for c in data.get('claims',[])]
    if not ids or len(ids)!=len(set(ids)) or None in ids:
        raise ValueError('Missing or duplicate Agriculture claim')
    return data

def retrieve(framework, period, entity_scope, path=None, decisions=None, period_start=None):
    if framework not in FRAMEWORKS or not entity_scope:
        raise ValueError('Framework and entity scope required')
    try:
        end=date.fromisoformat(period)
        start=date.fromisoformat(period_start or end.replace(month=1,day=1).isoformat())
    except (TypeError,ValueError):
        raise ValueError('ISO reporting dates required') from None
    if start.year!=2026 or end.year!=2026 or start>end:
        raise ValueError('Agriculture period outside approved 2026 scope')
    data=load_register(path)
    if data.get('status')!='APPROVED':
        raise ValueError('Supplemental Agriculture knowledge not approved')
    matched=[]
    for c in data['claims']:
        if c['framework']!=framework or (decisions is not None and c['decision'] not in decisions):
            continue
        r=c.get('approval_review') or {}
        if c.get('approval_track') not in {'DIRECT_SOURCE_CHECKED','TRAINING_DATA_CHECKED'} or r.get('result')!='PASS' or not all(r.get(k) is True for k in ('scope_and_period_checked','cross_framework_checked','regression_checked')):
            raise ValueError('Incomplete independent Agriculture approval')
        if (c['evidence_status']=='SOURCE_VERIFIED')==bool(c['audit_required']):
            raise ValueError('Inconsistent Agriculture evidence assurance')
        matched.append({k:c[k] for k in PUBLIC_FIELDS})
    if not matched or (decisions is not None and set(decisions)!={c['decision'] for c in matched}):
        raise ValueError('No approved applicable Agriculture decision')
    return matched

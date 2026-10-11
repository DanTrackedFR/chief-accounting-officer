"""Validation of registered private investigation checkpoint metadata."""
import base64
import hashlib
from orchestration.intake.sources import fingerprint,canonical


def validate(state,case_id):
    required={'contract','case_id','objective','family','snapshot','documents','requests','calculations','conflicts','inferences','round','events','qualified','pending_correction'}
    if not isinstance(state,dict) or not required<=set(state) or set(state)-required-{'native_events'} or state['contract']!='cao-investigation/1' or state['case_id']!=case_id:raise ValueError('Investigation checkpoint contract')
    s=state['snapshot']
    if s.get('snapshot_id')!=fingerprint({k:v for k,v in s.items() if k!='snapshot_id'}):raise ValueError('Context snapshot changed')
    if type(state['qualified']) is not bool or type(state['pending_correction']) is not bool or type(state['round']) is not int or not 0<=state['round']<=64:raise ValueError('Investigation state type')
    for key in ('documents','requests','calculations','conflicts','inferences','events'):
        if not isinstance(state[key],list):raise ValueError('Investigation population')
    if len(state['events'])!=state['round'] or len({x['id'] for x in state['events']})!=len(state['events']):raise ValueError('Investigation event history')
    if len({x['id'] for x in state['requests']})!=len(state['requests']):raise ValueError('Duplicate investigation questions')
    doc_ids=set()
    for d in state['documents']:
        key=(d['id'],d['version'])
        if key in doc_ids or d['qualification']!='OBSERVATION_ONLY' or d['accounting_authority'] is not False:raise ValueError('Document authority/history')
        doc_ids.add(key)
        data=base64.b64decode(d['original_content_base64'],validate=True)
        if len(data)!=d['original_bytes'] or hashlib.sha256(data).hexdigest()!=d['original_sha256'] or d['extraction_sha256']!=fingerprint({k:v for k,v in d.items() if k!='extraction_sha256'}):raise ValueError('Original document/extraction changed')
    if len(canonical(state).encode())>1_500_000:raise ValueError('Investigation checkpoint size')

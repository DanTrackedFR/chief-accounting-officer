"""Immutable approved canonical and supplemental retrieval for specialist #29."""
import hashlib
import importlib.util
import json
from pathlib import Path
from core_accounting import ReviewRequired

ROOT = Path(__file__).resolve().parents[1]

def mapped_knowledge(framework):
    folder=ROOT/'skills/derivatives-hedge-accounting'
    try:
        frozen=json.loads((folder/'CANONICAL-KNOWLEDGE-MAP.json').read_text())
        manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']
        claims=[];docs=[]
        for t in frozen['topics']:
            actual=next(x for x in manifest if x['topic_id']==t['topic_id'])
            if actual['status']!='APPROVED' or not set(t['capability_ids'])<=set(actual['capability_ids']):
                raise ReviewRequired('Frozen hedge canonical approval changed')
            for d in t['documents']:
                if hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest()!=d['sha256']:
                    raise ReviewRequired('Frozen hedge canonical method changed')
                docs.append(dict(topic_id=t['topic_id'],**d))
            for c in t['claims']:
                if c['framework']!=framework:continue
                if c.get('approval_review',{}).get('result')!='PASS':raise ReviewRequired('Canonical hedge claim unapproved')
                claims.append(dict(topic_id=t['topic_id'],claim_id=c['claim_id'],proposition=c['proposition'],references=c.get('paragraph_references',[]),reference_confidence=c['reference_confidence'],evidence_status=c['evidence_status'],audit_required=c['audit_required'],limitations=c['limitations'],effective_period=c['effective_period'],entity_scope=c['entity_scope']))
        spec=importlib.util.spec_from_file_location('hedge_supplement_retrieval',ROOT/'knowledge/derivatives-hedge/retrieval.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        eligible={c['claim_id'] for c in module.retrieve(framework,'2026-12-31',module.SCOPES[framework],period_start='2026-01-01',hedge_model=module.MODELS[framework],us_amendments_adopted=False if framework=='US_GAAP' else None)}
        supplemental=json.loads((folder/'SUPPLEMENTAL-KNOWLEDGE-MAP.json').read_text())
        for d in supplemental['documents']:
            if hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest()!=d['sha256']:raise ReviewRequired('Frozen hedge supplemental method changed')
            docs.append(dict(topic_id='SUPPLEMENTAL_DERIVATIVES_HEDGE',**d))
        for c in module.load_register()['claims']:
            if c['claim_id'] not in eligible:continue
            claims.append(dict(topic_id='SUPPLEMENTAL_DERIVATIVES_HEDGE',claim_id=c['claim_id'],decision=c['decision'],proposition=c['proposition'],references=c.get('paragraph_references',[]),reference_confidence=c['reference_confidence'],evidence_status=c['evidence_status'],audit_required=c['audit_required'],limitations=c['limitations'],effective_period=c['effective_period'],entity_scope=c['entity_scope']))
        return claims,docs
    except (OSError,ValueError,KeyError,TypeError,StopIteration) as exc:
        raise ReviewRequired('Hedge approved knowledge gate unresolved: '+str(exc)) from exc

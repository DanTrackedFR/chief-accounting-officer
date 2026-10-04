"""Frozen independently approved supplemental Insurance knowledge; no canonical IDs."""
import hashlib
import importlib.util
import json
from pathlib import Path
from core_accounting import ReviewRequired

ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = 'SUPPLEMENTAL_INSURANCE_CONTRACTS'

def retrieval_module():
    spec = importlib.util.spec_from_file_location('_insurance_supplement_retrieval', ROOT/'knowledge/insurance-contracts/retrieval.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def mapped_knowledge(framework):
    try:
        frozen = json.loads((ROOT/'skills/insurance-contracts-accounting/SUPPLEMENTAL-KNOWLEDGE-MAP.json').read_text())
        if frozen['namespace'] != NAMESPACE or frozen['status'] != 'APPROVED':
            raise ReviewRequired('Insurance supplemental map is not approved')
        docs = []
        for d in frozen['documents']:
            if hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest() != d['sha256']:
                raise ReviewRequired('Frozen Insurance knowledge changed; independent review and refreeze required')
            docs.append(dict(topic_id=NAMESPACE, **d))
        module = retrieval_module()
        model = {'IFRS':'IFRS17_GMM', 'AASB':'AASB17_GMM', 'US_GAAP':'ASC944_SHORT_DURATION', 'UK_GAAP':'FRS103_POLICY_REVIEW'}[framework]
        eligible = {c['claim_id'] for c in module.retrieve(framework, '2026-12-31', module.SCOPES[framework], period_start='2026-01-01', insurance_model=model)}
        register = module.load_register()
        if register['claims'] != frozen['claims']:
            raise ReviewRequired('Insurance claim population differs from independent frozen approval')
        claims = [dict(topic_id=NAMESPACE, claim_id=c['claim_id'], decision=c['decision'], proposition=c['proposition'],
                       references=c.get('paragraph_references', []), reference_confidence=c['reference_confidence'],
                       evidence_status=c['evidence_status'], audit_required=c['audit_required'], limitations=c['limitations'],
                       effective_period=c['effective_period'], entity_scope=c['entity_scope'])
                  for c in register['claims'] if c['claim_id'] in eligible]
        return claims, docs
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        raise ReviewRequired('Insurance approved knowledge gate unresolved: '+str(exc)) from exc

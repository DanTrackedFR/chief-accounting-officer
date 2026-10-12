"""Explicit synthetic reference versions; never recertify live company evidence.

Historical files remain immutable. Reproduction tests load only separately
reviewed current references, bound to both original and current exact bytes.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT/'recovery/borrowing-costs-pr42'
MANIFESTS = ('specialist-migration.json', 'orchestration-migration.json', 'durable-migration.json')


def prior_reference_path(path):
    original = Path(path)
    original = original.resolve() if original.is_absolute() else (ROOT/original).resolve()
    name = str(original.relative_to(ROOT))
    record = None
    for manifest in MANIFESTS:
        candidate = json.loads((DIRECTORY/manifest).read_text())['files'].get(name)
        if candidate is not None:
            if record is not None:
                raise AssertionError('Ambiguous synthetic reference migration: '+name)
            record = candidate
    if record is None:
        return original
    baseline = json.loads((DIRECTORY/'published-head-manifest.json').read_text())['files']
    if record['original_sha256'] != baseline[name]:
        raise AssertionError('Migration does not bind original PR42 evidence: '+name)
    if hashlib.sha256(original.read_bytes()).hexdigest() != record['original_sha256']:
        raise AssertionError('Original historical evidence changed: '+name)
    current = (ROOT/record['current_path']).resolve()
    namespaces = (DIRECTORY/'specialist-fresh', DIRECTORY/'orchestration-fresh', DIRECTORY/'stage2-fresh', DIRECTORY/'stage4-fresh')
    if not any(current.is_relative_to(namespace) for namespace in namespaces):
        raise AssertionError('Current reference outside reviewed synthetic namespace')
    if hashlib.sha256(current.read_bytes()).hexdigest() != record['current_sha256']:
        raise AssertionError('Current reference changed without reviewed migration: '+name)
    return current


def reference_path(path):
    """Layer independently reviewed grants synthetic versions over preserved PR42."""
    original=Path(path)
    original=original.resolve() if original.is_absolute() else (ROOT/original).resolve()
    name=str(original.relative_to(ROOT))
    prior=prior_reference_path(original)
    namespace=ROOT/'skills/government-grants/release-evidence/historical-qa'
    record=None
    for filename in ('specialist-migration.json','orchestration-migration.json','main-proof-migration.json'):
        manifest=namespace/filename
        if not manifest.exists():continue
        data=json.loads(manifest.read_text())
        if data.get('status')!='PASS' or data.get('errors'):raise AssertionError('Incomplete Grants synthetic migration')
        candidate=data['files'].get(name)
        if candidate is not None:
            if record is not None:raise AssertionError('Ambiguous Grants synthetic migration: '+name)
            record=candidate;layer=filename
    if record is None:return prior
    if hashlib.sha256(original.read_bytes()).hexdigest()!=record['original_sha256']:
        raise AssertionError('Original Grants migration evidence changed: '+name)
    previous=ROOT/record['previous_path']
    if hashlib.sha256(previous.read_bytes()).hexdigest()!=record['previous_sha256']:
        raise AssertionError('Prior reviewed synthetic evidence changed: '+name)
    # Main proof references had an existing separate PR42 layer outside the
    # general resolver. Require its actual preserved path/hash, not guess a new one.
    if layer=='main-proof-migration.json':
        predecessor=json.loads((DIRECTORY/'main-proof-migration.json').read_text())['files'][name]
        if record['previous_path']!=predecessor['current_path'] or record['previous_sha256']!=predecessor['current_sha256']:
            raise AssertionError('Grants proof migration does not bind preceding approved proof: '+name)
    if layer!='main-proof-migration.json' and prior!=previous:
        raise AssertionError('Grants migration does not bind preceding reference: '+name)
    current=(ROOT/record['current_path']).resolve()
    if not current.is_relative_to(namespace):raise AssertionError('Grants reference outside reviewed namespace')
    if hashlib.sha256(current.read_bytes()).hexdigest()!=record['current_sha256']:
        raise AssertionError('Grants synthetic evidence changed without reviewed migration: '+name)
    return current

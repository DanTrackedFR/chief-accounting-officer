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


def reference_path(path):
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

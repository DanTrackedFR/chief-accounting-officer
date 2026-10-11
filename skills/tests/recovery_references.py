"""Explicit synthetic requalification; immutable originals remain available."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT/'recovery/borrowing-costs-pr42/specialist-migration.json'


def reference_path(path):
    path = Path(path)
    original = path if path.is_absolute() else ROOT/path
    name = str(original.relative_to(ROOT))
    record = json.loads(MANIFEST.read_text())['files'].get(name)
    if record is None:
        return original
    if hashlib.sha256(original.read_bytes()).hexdigest() != record['original_sha256']:
        raise AssertionError('Original historical evidence changed: '+name)
    current = ROOT/record['current_path']
    if not current.is_relative_to(ROOT/'recovery/borrowing-costs-pr42/specialist-fresh'):
        raise AssertionError('Requalified reference outside governed synthetic namespace')
    if hashlib.sha256(current.read_bytes()).hexdigest() != record['current_sha256']:
        raise AssertionError('Requalified certificate changed without reviewed migration: '+name)
    return current

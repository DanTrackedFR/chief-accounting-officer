"""Regenerate only the explicitly authorized roadmap documentation witness.

Every other protected file must still match its original witness. This does
not reset accounting, production, canonical or residual backlog baselines.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / 'skills/insurance-contracts-accounting/LIVE-BASELINE.json'
ROADMAP = 'architecture/build-roadmap.md'


def main():
    record = json.loads(BASELINE.read_text())
    entries = record['protected_documents']
    roadmap = [entry for entry in entries if entry['path'] == ROADMAP]
    if len(roadmap) != 1:
        raise ValueError('Exactly one existing roadmap witness is required')
    previous = subprocess.check_output(['git', 'show', 'HEAD:' + ROADMAP], cwd=ROOT)
    current = hashlib.sha256((ROOT / ROADMAP).read_bytes()).hexdigest()
    if roadmap[0]['sha256'] not in {hashlib.sha256(previous).hexdigest(), current}:
        raise ValueError('Existing roadmap witness must match the integration base')
    for entry in entries:
        if entry['path'] != ROADMAP:
            actual = hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest()
            if actual != entry['sha256']:
                raise ValueError('Unrelated protected document drift: ' + entry['path'])
    roadmap[0]['sha256'] = current
    BASELINE.write_text(json.dumps(record, indent=2) + '\n')


if __name__ == '__main__':
    main()

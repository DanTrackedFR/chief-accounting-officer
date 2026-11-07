"""Explicit Phase A proof successor. Historical proof remains immutable.

This pins the accounting source and synthetic HTTP fixture/input closure. Release
infrastructure is independently bound by release_population.release_input_hashes
and the complete receipt source map; it cannot change the expected proof bytes.
"""
import argparse
import json
import sys
from pathlib import Path
from receipt_integrity import artifact, digest, require
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
CONTRACT = 'skills/presumed-sources/release/phase-a-v1/proof-contract.json'
CONTRACT_SHA256 = '0cfd93e3d75f3bd9d781422bbbf97129607fe07253a09dba6d80f911de673694'
VERSION = 'phase-a-v1'


def selected_proof(version=VERSION, root=None):
    root = ROOT if root is None else root
    require(version == VERSION, 'Wrong proof version')
    path = artifact(root, CONTRACT)
    require(digest(path) == CONTRACT_SHA256, 'Proof contract changed')
    contract = json.loads(path.read_bytes())
    require(contract['proof_version'] == version and contract['schema_version'] == 1, 'Proof contract version differs')
    sources = {str(p.relative_to(root)) for folder in ('orchestration','local_cao','hosted_cao','intelligence','skills')
               for p in (root/folder).rglob('*.py')
               if '/release/' not in str(p.relative_to(root)) and '/examples/' not in str(p.relative_to(root))
               and not str(p.relative_to(root)).startswith(('skills/presumed-sources/','skills/prepared-accounting/'))}
    require(sources == set(contract['accounting_source_sha256']), 'Proof source population mismatch')
    from build4.run_release import input_hashes
    require(root == ROOT, 'Proof selection requires the actual checkout root')
    inputs = {n:h for n,h in input_hashes().items() if not n.endswith('.py') and n != '.github/workflows/cao-presumed-sources.yml'}
    require(inputs == contract['proof_inputs_sha256'], 'Proof execution-input population/content mismatch')
    for key in ('accounting_source_sha256', 'proof_inputs_sha256'):
        for name, expected in contract[key].items():
            require(digest(artifact(root, name)) == expected, 'Proof source/input mismatch: '+name)
    for key in ('historical_proof', 'successor_proof'):
        row = contract[key]
        require(digest(artifact(root, row['path'])) == row['sha256'], 'Missing, stale or tampered '+key)
    return artifact(root, contract['successor_proof']['path'])


def verify_output(output, version=VERSION, root=None):
    root = ROOT if root is None else root
    expected = selected_proof(version, root)
    actual = Path(output).read_bytes()
    require(actual == expected.read_bytes(), 'Deterministic proof output differs')
    # Independently derived fixture arithmetic, not refreshed implementation values.
    data = json.loads(actual)
    from decimal import Decimal
    totals = {'fixed-assets': {'closing cost': sum(Decimal(10000+i*1000) for i in range(1,28)),
                              'depreciation': sum(Decimal(10000+i*1000)/10 for i in range(1,28))},
              'accounts-payable': {'invoices': sum(Decimal(100+i*10) for i in range(1,11))}}
    require(len(data['executions']) == 2, 'Unexpected proof population')
    for row in data['executions']:
        values = {r['label']: Decimal(r['amount']) for r in row['calculations']}
        for label, amount in totals[row['package']].items():
            require(values[label] == amount, 'Unexpected numerical divergence: '+label)
    return dict(proof_version=version, sha256=digest(expected), path=str(expected.relative_to(root)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(verify_output(args.output, args.version), sort_keys=True))

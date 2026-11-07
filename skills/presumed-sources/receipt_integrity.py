"""Versioned receipt inventories. These checks confer integrity, never review authority."""
import hashlib
import json
from pathlib import Path


class IntegrityError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise IntegrityError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(root, name):
    require(isinstance(name, str) and bool(name), 'Missing evidence path')
    path = root / name
    require(not Path(name).is_absolute() and '..' not in Path(name).parts,
            'Evidence path escapes repository')
    require(path.resolve() == path and path.is_file(), 'Missing or redirected evidence: ' + name)
    return path


def verify_inventory(root, pointer, manifest_path, manifest, purpose):
    require(pointer.get('schema_version') == 2, 'A version 2 evidence inventory is required; historical acceptance is not backfilled')
    binding = pointer.get('evidence_inventory', {})
    inventory_path = artifact(root, binding.get('path'))
    require(digest(inventory_path) == binding.get('sha256'), 'Evidence inventory digest differs')
    inventory = json.loads(inventory_path.read_bytes())
    require(inventory.get('schema_version') == 2 and inventory.get('purpose') == purpose,
            'Evidence inventory purpose/version differs')
    files = inventory.get('files')
    require(isinstance(files, dict) and bool(files), 'Empty evidence inventory')
    manifest_name = str(manifest_path.relative_to(root))
    require(inventory.get('manifest') == manifest_name and files.get(manifest_name) == pointer['sha256'],
            'Inventory does not bind the authoritative manifest')
    # Required classes are structural, not selected by an untrusted allowlist.
    directory = manifest_path.parent
    required = {str(p.relative_to(root)) for p in directory.rglob('*') if p.is_file()}
    require(str(inventory_path.relative_to(root)) not in required,
            'Inventory must be outside the immutable attempt directory')
    required.update(row['path'] for row in manifest['logs'])
    for row in manifest['suite_results']:
        required.update(shard['log'] for shard in row.get('module_results', []))
    roles = inventory.get('attestations', {})
    require(set(roles) == {'outer_log', 'receipt_review'}, 'Missing outer log or receipt review attestation')
    require(len(set(roles.values())) == 2, 'Evidence roles must have distinct paths')
    expected_roles = dict(outer_log=str((directory/'outer.log').relative_to(root)) if purpose == 'focused-governance-qa-v1'
                          else 'skills/presumed-sources/release/full-regression-' + manifest['attempt'] + '.log',
                          receipt_review=str((directory/'receipt-review.md').relative_to(root)))
    require(roles == expected_roles, 'Evidence attestation roles redirected')
    required.update(roles.values())
    for name in ('start-source-hashes.json', 'start-input-hashes.json'):
        required.add(str((directory / name).relative_to(root)))
    for index, row in enumerate(manifest['suite_results']):
        path = directory / ('suite-' + str(index) + '.json')
        required.add(str(path.relative_to(root)))
        sidecar = json.loads(artifact(root, str(path.relative_to(root))).read_bytes())
        expected = {k: v for k, v in row.items() if k != 'exit_code'}
        require(sidecar == expected, 'Suite sidecar differs from executed manifest: ' + str(index))
    require(required <= set(files), 'Evidence inventory omits required artifacts')
    for name, expected in files.items():
        require(digest(artifact(root, name)) == expected, 'Evidence inventory artifact changed: ' + name)
    for name, key in (('start-source-hashes.json', 'tested_python_sha256'),
                      ('start-input-hashes.json', 'tested_execution_inputs_sha256')):
        require(json.loads((directory / name).read_bytes()) == manifest[key], 'Start/test source evidence differs: ' + name)
    return len(files)


def seal_inventory(root, manifest_path, outer_log, review, output, purpose, extra_files=()):
    """Create a NEW inventory after actual execution/review; never edit old evidence."""
    require(not output.exists(), 'Preserve prior inventory; choose a new version')
    manifest_name = str(manifest_path.relative_to(root))
    files = {str(p.relative_to(root)) for p in manifest_path.parent.rglob('*') if p.is_file()}
    files.update((outer_log, review)); files.update(extra_files)
    record = dict(schema_version=2, purpose=purpose, manifest=manifest_name,
                  attestations=dict(outer_log=outer_log, receipt_review=review),
                  files={name: digest(artifact(root, name)) for name in sorted(files)})
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    return dict(schema_version=2, manifest=manifest_name, sha256=digest(manifest_path),
                evidence_inventory=dict(path=str(output.relative_to(root)), sha256=digest(output)))

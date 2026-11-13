"""Accepted-main evidence plus exact, archived infrastructure source successors.

No original accounting evidence, receipts, diagnostics, proofs or workpapers are
replaced. Four original infrastructure migrations and one exact diagnostic
successor retain their immutable archived predecessors.
"""
import json
from pathlib import Path
from receipt_integrity import artifact, digest, require
ROOT=Path(__file__).resolve().parents[2]
CONTRACT='skills/presumed-sources/phase-a-contracts/accepted-main-infrastructure-v1.json'
CONTRACT_SHA256='b2c6a8d435095a82ae63d1d4f8ec5ed2e62dba4e4222e5adb5843914b3e4bfac'


def verify_accepted_main(root=None):
    root=ROOT if root is None else root
    path=artifact(root,CONTRACT)
    require(digest(path)==CONTRACT_SHA256,'Accepted-main preservation contract changed')
    data=json.loads(path.read_bytes())
    require(data['baseline']=='97d0621331c6ad2a66b12ed09c0ec40c05c626b9' and len(data['files'])==7963,
            'Accepted-main preservation population differs')
    require(set(data['source_migrations'])=={
        'diagnostics/profile12/remediation/issue_focused_receipt.py',
        'skills/presumed-sources/release_population.py',
        'skills/presumed-sources/run_release.py',
        'skills/presumed-sources/verify_release.py'}, 'Unauthorized preservation migration population')
    from ci_governance import accepted_main_extension, DIAGNOSTIC_TEST
    extension = accepted_main_extension(root)
    require(extension['contract'] == dict(path=CONTRACT,sha256=CONTRACT_SHA256) and
            extension['baseline'] == data['baseline'], 'Accepted-main extension contract differs')
    require(set(extension['migrations']) == {DIAGNOSTIC_TEST} and
            not set(extension['migrations']) & set(data['source_migrations']) and
            set(extension['migrations']) <= set(data['files']),
            'Unauthorized accepted-main extension population')
    import hashlib
    for name,blob in data['files'].items():
        migration=data['source_migrations'].get(name)
        if migration:
            from ci_governance import accepted_main_predecessor
            selected = accepted_main_predecessor(root, name) if name == 'skills/presumed-sources/verify_release.py' else artifact(root,name)
            require(digest(selected)==migration['successor_sha256'],'Infrastructure successor changed: '+name)
            original=artifact(root,migration['archive_path']).read_bytes()
            require(hashlib.sha256(original).hexdigest()==migration['original_sha256'],'Archived infrastructure source changed')
        elif name in extension['migrations']:
            row=extension['migrations'][name]
            require(row['original_blob']==blob, 'Accepted-main extension original binding differs')
            current=artifact(root,name).read_bytes()
            require(hashlib.sha256(current).hexdigest()==row['successor_sha256'] and
                    hashlib.sha1(b'blob '+str(len(current)).encode()+b'\0'+current).hexdigest()==row['successor_blob'],
                    'Accepted-main diagnostic successor changed')
            original=artifact(root,row['archive_path']).read_bytes()
            require(hashlib.sha256(original).hexdigest()==row['original_sha256'],
                    'Accepted-main diagnostic archive changed')
        else:
            original=artifact(root,name).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()
        require(actual==blob,'Accepted-main artifact changed: '+name)
    migrated=len(data['source_migrations'])+len(extension['migrations'])
    return dict(protected_files=len(data['files']),
                unchanged_active_files=len(data['files'])-migrated,archived_source_migrations=migrated)

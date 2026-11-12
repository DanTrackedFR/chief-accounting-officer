"""Adversarial reads against the real preservation contract and unmodified Git tree."""
import hashlib
import importlib.util
import contextlib
import copy
import json
import sys
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / 'skills/presumed-sources/release'
WORKFLOW = ROOT / '.github/workflows/cao-orchestration.yml'
ARCHIVE = RELEASE / 'workflow-migration/cao-orchestration.v1.yml'
CONTRACT = RELEASE / 'workflow-migration/contract-v2.json'
V1 = RELEASE / 'historical-preservation.json'
CANARY = ROOT / 'intelligence/release/ci-orchestration-module-0.log'
sys.path.insert(0,str(ROOT/'skills/presumed-sources'))
import ci_governance as governance

spec = importlib.util.spec_from_file_location(
    'independent_migration_verifier', RELEASE.parent / 'verify_release.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class WorkflowMigrationQA(unittest.TestCase):
    @contextlib.contextmanager
    def synthetic_seal(self):
        # In-memory test authority only. Never seals or approves repository bytes.
        data=copy.deepcopy(governance.load_contract(ROOT))
        review=b'SYNTHETIC MIGRATION TEST REVIEW ONLY; not CAO approval.\n'
        data['state']='SEALED'
        data['scope_review'].update(status='INDEPENDENTLY_REVIEWED',sha256=hashlib.sha256(review).hexdigest())
        raw=(json.dumps(data,sort_keys=True,indent=2)+'\n').encode()
        read_bytes=Path.read_bytes
        def read(path):
            if path==ROOT/governance.CONTRACT:return raw
            if path==ROOT/governance.NAMESPACE/'scope-review.md':return review
            return read_bytes(path)
        with patch.object(Path,'read_bytes',read),patch.object(governance,'CONTRACT_SHA256',hashlib.sha256(raw).hexdigest()):
            yield data

    def assert_rejected(self, replacements):
        # Substitute only the specified bytes at the lowest read boundary. All
        # other files, verification logic, anchored digests and paths stay real.
        with self.synthetic_seal():
            read_bytes = Path.read_bytes
            def read(path):
                if path not in replacements:return read_bytes(path)
                if replacements[path] is None:raise FileNotFoundError(path)
                return replacements[path]
            with patch.object(Path,'read_bytes',read):
                with self.assertRaises((AssertionError,FileNotFoundError,ValueError)) as raised:
                    verifier.verify_historical()
                self.assertNotIsInstance(raised.exception,governance.PendingSealing)

    def test_original_workflow_remains_anchored_and_successor_passes(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                         'a4dbd9518ad72926bf3a46e0d4bc5a98d0bc286e23838aaaef29645c4aa671d7')
        self.assertEqual(hashlib.sha256(V1.read_bytes()).hexdigest(),
                         '2c4fcdc1b938a1297acb31080e32c3c6ec388ad756395146028df45c98e70c49')
        data=governance.load_contract(ROOT)
        row=data['modified_files'][str(WORKFLOW.relative_to(ROOT))]
        archived=ROOT/row['archive']
        self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(),row['before_sha256'])
        self.assertEqual(row['before_sha256'],json.loads(CONTRACT.read_bytes())['migration']['successor_sha256'])
        with self.synthetic_seal():
            self.assertEqual(verifier.verify_historical(), 8912)

    def test_successor_edit_and_rollback_are_rejected(self):
        for contents in (WORKFLOW.read_bytes() + b'# unauthorized\n', ARCHIVE.read_bytes(),
                         (ROOT/governance.load_contract(ROOT)['modified_files'][str(WORKFLOW.relative_to(ROOT))]['archive']).read_bytes()):
            with self.subTest(contents_hash=hashlib.sha256(contents).hexdigest()):
                self.assert_rejected({WORKFLOW: contents})

    def test_missing_or_changed_archive_is_rejected(self):
        for contents in (None, WORKFLOW.read_bytes()):
            with self.subTest(missing=contents is None):
                self.assert_rejected({ARCHIVE: contents})

    def test_missing_or_changed_migration_contract_is_rejected(self):
        for contents in (None, CONTRACT.read_bytes() + b'\n'):
            with self.subTest(missing=contents is None):
                self.assert_rejected({CONTRACT: contents})

    def test_joint_successor_and_contract_tampering_is_rejected(self):
        changed = WORKFLOW.read_bytes() + b'# unauthorized\n'
        name=str(WORKFLOW.relative_to(ROOT))
        new_contract=ROOT/governance.CONTRACT
        active_hash=hashlib.sha256(WORKFLOW.read_bytes()).hexdigest().encode()
        changed_hash=hashlib.sha256(changed).hexdigest().encode()
        forged=new_contract.read_bytes().replace(active_hash,changed_hash)
        self.assertNotEqual(forged,new_contract.read_bytes())
        # Active-only, record-only and joint forgery all invoke the production verifier.
        for replacements in ({WORKFLOW:changed},{new_contract:forged},{WORKFLOW:changed,new_contract:forged}):
            with self.subTest(paths=sorted(str(p) for p in replacements)):
                self.assert_rejected(replacements)
        # Retain the old joint-forgery challenge at the correct F2/v2 stage.
        row=governance.load_contract(ROOT)['modified_files'][name]
        archive=ROOT/row['archive'];changed_predecessor=archive.read_bytes()+b'# forged predecessor\n'
        old_hash=row['before_sha256'].encode()
        forged_v2=CONTRACT.read_bytes().replace(old_hash,hashlib.sha256(changed_predecessor).hexdigest().encode())
        self.assertNotEqual(forged_v2,CONTRACT.read_bytes())
        self.assert_rejected({archive:changed_predecessor,CONTRACT:forged_v2})

    def test_other_pinned_log_remains_protected(self):
        self.assert_rejected({CANARY: CANARY.read_bytes() + b'overwritten'})

    def test_stale_predecessor_contract_is_rejected(self):
        self.assert_rejected({V1: V1.read_bytes() + b'\n'})

    def test_missing_or_changed_independent_verification_is_rejected(self):
        evidence = RELEASE / 'workflow-migration/independent-qa.md'
        for contents in (None, evidence.read_bytes() + b'\n'):
            with self.subTest(missing=contents is None):
                self.assert_rejected({evidence: contents})

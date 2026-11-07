"""Adversarial reads against the real preservation contract and unmodified Git tree."""
import hashlib
import importlib.util
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

spec = importlib.util.spec_from_file_location(
    'independent_migration_verifier', RELEASE.parent / 'verify_release.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class WorkflowMigrationQA(unittest.TestCase):
    def assert_rejected(self, replacements):
        # Substitute only the specified bytes at the lowest read boundary. All
        # other files, verification logic, anchored digests and paths stay real.
        read_bytes = Path.read_bytes

        def read(path):
            if path not in replacements:
                return read_bytes(path)
            if replacements[path] is None:
                raise FileNotFoundError(path)
            return replacements[path]

        with patch.object(Path, 'read_bytes', read):
            with self.assertRaises((AssertionError, FileNotFoundError, ValueError)):
                verifier.verify_historical()

    def test_original_workflow_remains_anchored_and_successor_passes(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                         'a4dbd9518ad72926bf3a46e0d4bc5a98d0bc286e23838aaaef29645c4aa671d7')
        self.assertEqual(hashlib.sha256(V1.read_bytes()).hexdigest(),
                         '2c4fcdc1b938a1297acb31080e32c3c6ec388ad756395146028df45c98e70c49')
        self.assertEqual(verifier.verify_historical(), 8912)

    def test_successor_edit_and_rollback_are_rejected(self):
        for contents in (WORKFLOW.read_bytes() + b'# unauthorized\n', ARCHIVE.read_bytes()):
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
        old_hash = hashlib.sha256(WORKFLOW.read_bytes()).hexdigest().encode()
        new_hash = hashlib.sha256(changed).hexdigest().encode()
        forged = CONTRACT.read_bytes().replace(old_hash, new_hash)
        self.assertNotEqual(forged, CONTRACT.read_bytes())
        self.assert_rejected({WORKFLOW: changed, CONTRACT: forged})

    def test_other_pinned_log_remains_protected(self):
        self.assert_rejected({CANARY: CANARY.read_bytes() + b'overwritten'})

    def test_stale_predecessor_contract_is_rejected(self):
        self.assert_rejected({V1: V1.read_bytes() + b'\n'})

    def test_missing_or_changed_independent_verification_is_rejected(self):
        evidence = RELEASE / 'workflow-migration/independent-qa.md'
        for contents in (None, evidence.read_bytes() + b'\n'):
            with self.subTest(missing=contents is None):
                self.assert_rejected({evidence: contents})

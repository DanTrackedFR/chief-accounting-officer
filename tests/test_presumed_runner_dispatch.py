"""Reproduce the published workflow skip without executing accounting regression."""
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'a000d52991142352d9cd94ad2f554ea84fa1d151'
WORKFLOW = '.github/workflows/cao-presumed-sources.yml'


class ReleaseDispatchRegression(unittest.TestCase):
    def test_historical_pointer_suppressed_changed_source_at_published_baseline(self):
        def original(path):
            return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)
        prior = original(WORKFLOW).decode()
        self.assertIn("if: ${{ hashFiles('build4/release/presumed-sources-accepted-release.json') == '' }}", prior)
        pointer_bytes = original('build4/release/presumed-sources-accepted-release.json')
        pointer = json.loads(pointer_bytes)
        manifest_bytes = original(pointer['manifest'])
        self.assertEqual(hashlib.sha256(manifest_bytes).hexdigest(), pointer['sha256'])
        manifest = json.loads(manifest_bytes)
        # A matched nonempty file makes hashFiles nonempty; the old step is skipped.
        self.assertTrue(pointer_bytes)
        self.assertNotEqual(hashlib.sha256(original('local_cao/adapter.py')).hexdigest(),
                            manifest['tested_python_sha256']['local_cao/adapter.py'])

    def test_workflow_uses_explicit_verified_reuse_and_never_rewrites_pointer(self):
        current = (ROOT / WORKFLOW).read_text()
        self.assertNotIn('hashFiles(', current)
        self.assertIn('CAO_ACCEPTANCE_POINTER: ${{ inputs.acceptance_pointer }}', current)
        self.assertIn('execute_release.py --reuse "$CAO_ACCEPTANCE_POINTER"', current)
        self.assertNotIn("Path('build4/release/presumed-sources-accepted-release.json').write_text", current)
        self.assertIn('fresh regression is not release acceptance', current)

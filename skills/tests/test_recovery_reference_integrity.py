"""Independent structural and native-accounting review of synthetic migration."""
import hashlib
import json
import re
import unittest
from cases import revenue  # initialize the existing skill import path
from production import execute, serializable
from recovery_references import ROOT, MANIFEST, reference_path
from orchestration.history_references import prior_reference_path


class ReferenceIntegrity(unittest.TestCase):
    def test_only_bijective_certificate_and_derived_digest_changes(self):
        manifest = json.loads(MANIFEST.read_text())
        baseline = json.loads((ROOT/'recovery/borrowing-costs-pr42/published-head-manifest.json').read_text())['files']
        allowed = {'case_fingerprint', 'payload_fingerprint', 'owner_result_fingerprint', 'content_hash', 'body_hash'}
        forward, reverse = {}, {}
        def compare(old, current, path=''):
            self.assertEqual(type(old), type(current), path)
            if isinstance(old, dict):
                self.assertEqual(set(old), set(current), path)
                for key in old:
                    compare(old[key], current[key], path+'/'+key)
            elif isinstance(old, list):
                self.assertEqual(len(old), len(current), path)
                for i, (a, b) in enumerate(zip(old, current)):
                    compare(a, b, path+'/'+str(i))
            elif old != current:
                self.assertIn(path.split('/')[-1], allowed, path)
                for value in (old, current):
                    self.assertIsInstance(value, str, path)
                    self.assertRegex(value, r'^[0-9a-f]{64}$', path)
                self.assertEqual(forward.setdefault(old, current), current, path)
                self.assertEqual(reverse.setdefault(current, old), old, path)
        for name, row in manifest['files'].items():
            self.assertEqual(baseline[name], row['original_sha256'])
            self.assertFalse(name.endswith('.public.json'))
            compare(json.loads((ROOT/name).read_text()), json.loads(prior_reference_path(name).read_text()), name)
        self.assertEqual(forward, manifest['identity_map'])

    def test_current_imports_are_exact_native_results(self):
        seen = set()
        def walk(value):
            if isinstance(value, dict):
                if {'package', 'case', 'result'} <= set(value):
                    key = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
                    if key not in seen:
                        seen.add(key)
                        actual = execute(value['package'], value['case'])
                        self.assertEqual('complete', actual['status'])
                        self.assertEqual(json.loads(json.dumps(actual, default=serializable)), value['result'])
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        for name in json.loads(MANIFEST.read_text())['files']:
            if '.blocked.' not in name:
                walk(json.loads(reference_path(name).read_text()))
        self.assertGreater(len(seen), 0)

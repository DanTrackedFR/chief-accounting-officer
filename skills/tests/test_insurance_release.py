"""Insurance release gates preserve live canonical and prior specialist bytes."""
import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'skills'))
from core_accounting import ReviewRequired
from insurance_knowledge import mapped_knowledge

class InsuranceReleaseTests(unittest.TestCase):
    def test_historical_denominators_and_approval_are_unchanged(self):
        topics = json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']
        self.assertEqual((157,157), (len(topics), sum(t['status']=='APPROVED' for t in topics)))
        with (ROOT/'knowledge/capability-topic-matrix.csv').open() as f:
            self.assertEqual(347, len(list(csv.DictReader(f))))
        registers = list((ROOT/'knowledge/topics').glob('*/standards-claims.json'))
        self.assertEqual(1598, sum(len(json.loads(p.read_text())['claims']) for p in registers))
        for folder,count in {'income-taxes':64,'agriculture':66,'inventory-cost':228,'derivatives-hedge':100}.items():
            register = json.loads((ROOT/'knowledge'/folder/'standards-claims.json').read_text())
            self.assertEqual((count,'APPROVED'), (len(register['claims']),register['status']))

    def test_all_protected_baseline_files_are_identical(self):
        baseline = json.loads((ROOT/'skills/insurance-contracts-accounting/LIVE-BASELINE.json').read_text())
        for d in baseline['protected_documents']:
            with self.subTest(path=d['path']):
                self.assertEqual(d['sha256'],hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest())

    def test_existing_production_and_nonproduction_packages_preserved(self):
        existing = [p for p in (ROOT/'skills').glob('*/SKILL.md') if p.parent.name!='insurance-contracts-accounting']
        self.assertEqual(47,sum('status: production' in p.read_text() for p in existing))
        # Skill35 is a separately accepted extension; preserve the historical contract.
        legacy=ROOT/'skills/borrowing-costs/examples/legacy-skill-v0.1.0.md'
        self.assertEqual('5bb44e8adb0bd1c69e2aa72ce18818b572d2c531af1945ba72c16c6f66452ecd',hashlib.sha256(legacy.read_bytes()).hexdigest())
        self.assertIn('NONPRODUCTION',legacy.read_text())
        self.assertIn('status: production',(ROOT/'skills/borrowing-costs/SKILL.md').read_text())
        for package in ('government-grants','investment-property'):
            p=ROOT/'skills'/package/'SKILL.md'
            self.assertIn('status: review',p.read_text())
            baseline_hashes={'government-grants': '8aa8c8ec7b96b26f73ed5ad708fb99526bb966497d48f7d46c632c07d72402f3', 'borrowing-costs': '5bb44e8adb0bd1c69e2aa72ce18818b572d2c531af1945ba72c16c6f66452ecd', 'investment-property': '248435f35e1dcddba45160a9e927ce498153b9ceb91a060f9e83be0a8d12180a'}
            self.assertEqual(baseline_hashes[package],hashlib.sha256(p.read_bytes()).hexdigest())

    def test_stale_insurance_knowledge_fails_retrieval(self):
        original=Path.read_bytes
        def stale(path):
            value=original(path)
            return value+b' changed' if path==ROOT/'knowledge/insurance-contracts/FRAMEWORK-METHOD.md' else value
        with patch.object(Path,'read_bytes',stale):
            with self.assertRaises(ReviewRequired):mapped_knowledge('IFRS')

if __name__=='__main__':unittest.main()

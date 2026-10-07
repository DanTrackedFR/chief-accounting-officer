"""Accepted lifecycle artifacts must reproduce from governed runtime, never patched JSON."""
import json
import unittest
from orchestration.tests.generate_stage4_temporal_model_examples import artifacts, TARGET

class CompleteTemporalArtifacts(unittest.TestCase):
    def test_committed_complete_temporal_lifecycle_reproduces(self):
        generated=artifacts()
        self.assertEqual({p.name for p in TARGET.glob('*.json')},set(generated))
        for name,value in generated.items():
            with self.subTest(name=name):
                self.assertEqual(json.loads((TARGET/name).read_text()),json.loads(json.dumps(value,default=str)))
        self.assertEqual(generated['current-case-and-public-answer.json']['status'],'CLOSED')
        self.assertEqual(generated['current-case-and-public-answer.json']['outcome'],'complete')
        self.assertEqual(generated['adversarial-results.json']['result'],'PASS')
        self.assertEqual(generated['adversarial-results.json']['failures'],0)
        self.assertEqual(generated['adversarial-results.json']['errors'],0)

if __name__=='__main__':unittest.main()

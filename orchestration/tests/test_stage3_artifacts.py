import json
import unittest
from orchestration.tests.generate_stage3_examples import artifacts, TARGET

class Stage3Artifacts(unittest.TestCase):
    def test_committed_artifacts_reproduce_from_ordinary_runtime(self):
        expected=artifacts()
        self.assertEqual({p.name for p in TARGET.glob('*.json')},set(expected))
        for name,value in expected.items():
            with self.subTest(name=name):
                self.assertEqual(json.loads((TARGET/name).read_text()),json.loads(json.dumps(value,default=str)))
    def test_artifacts_preserve_unresolved_residual_and_current_rework(self):
        initial=json.loads((TARGET/'result-versions-initial.json').read_text())
        final=json.loads((TARGET/'result-versions-final.json').read_text())
        self.assertEqual(len(initial),17);self.assertEqual(len(final),24)
        self.assertEqual(sum(r['state']=='CURRENT' for r in final),17)
        self.assertEqual(sum(r['state']=='SUPERSEDED' for r in final),7)
        network=json.loads((TARGET/'business-network-final.json').read_text())
        self.assertTrue(network['business_cycle']);self.assertFalse(network['execution_edges_inferred'])
        answer=json.loads((TARGET/'public-answer-final.json').read_text())
        self.assertEqual(answer['status'],'partial');self.assertTrue(answer['open_items'])

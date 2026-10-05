"""Saved reference artifacts reproduce from raw sources and reviewed scaffolding."""
import json
from pathlib import Path
import unittest
from orchestration.tests.generate_saas_examples import artifacts


class SaaSArtifacts(unittest.TestCase):
    def test_complete_artifact_population_reproduces(self):
        root = Path(__file__).resolve().parents[1] / 'examples/saas-close'
        generated = artifacts()
        self.assertEqual(set(generated), {p.name for p in root.glob('*.json')})
        for name, value in generated.items():
            with self.subTest(name=name):
                self.assertEqual(json.loads((root / name).read_text()), json.loads(json.dumps(value, default=str)))


if __name__ == '__main__':
    unittest.main()

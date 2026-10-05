import json
import unittest
from pathlib import Path
from orchestration.tests.generate_diagnostic_examples import artifacts

class DiagnosticArtifactTests(unittest.TestCase):
    def test_exact_artifact_reproduction(self):
        directory=Path(__file__).resolve().parents[1]/'examples'
        for name,value in artifacts().items():
            with self.subTest(name=name):self.assertEqual(json.loads((directory/name).read_text()),json.loads(json.dumps(value,default=str)))

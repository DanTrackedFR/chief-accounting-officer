import json
import unittest
from pathlib import Path
from orchestration.tests.generate_intake_examples import artifacts
from orchestration.intake.semantic import StructuredProposal

class IntakeArtifacts(unittest.TestCase):
    def test_reproducible_internal_and_public_artifacts(self):
        root=Path(__file__).resolve().parents[1]/'examples/intake'
        for name,value in artifacts().items():
            with self.subTest(name=name):self.assertEqual(json.loads((root/name).read_text()),json.loads(json.dumps(value,default=str)))
    def test_strict_proposal_json_roundtrip(self):
        from orchestration.tests.intake_fixtures import factory_proposal,factory_sources
        p=factory_proposal(factory_sources());self.assertEqual(StructuredProposal.from_record(p.record()).record(),p.record())
        raw=p.record();raw['approved']=True
        with self.assertRaises(ValueError):StructuredProposal.from_record(raw)

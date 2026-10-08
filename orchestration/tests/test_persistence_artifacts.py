import json
import unittest
from orchestration.tests.generate_persistence_examples import artifacts,TARGET

class DurableArtifactReproduction(unittest.TestCase):
    def test_process_restart_artifacts_reproduce(self):
        generated=artifacts()
        self.assertEqual(set(generated),{p.name for p in TARGET.glob('*.json')})
        for name,value in generated.items():self.assertEqual(value,json.loads((TARGET/name).read_text()))
        self.assertEqual(generated['restart-proof.json']['result'],'PASS')
        self.assertEqual(generated['restart-proof.json']['owner_execution_during_restore'],0)
        self.assertEqual(generated['restart-proof.json']['journal_release_during_restore'],0)

if __name__=='__main__':unittest.main()

"""Generated reference workpapers must reproduce the exact candidate behavior."""
import json,subprocess,sys,unittest
from pathlib import Path
from orchestration.tests.generate_examples import artifacts,ROOT
from orchestration.tests.fixtures import manufacturing
from orchestration import CAO

class ArtifactIntegration(unittest.TestCase):
    def test_generated_workpapers_reproduce(self):
        for name,value in artifacts().items():
            with self.subTest(name=name):
                self.assertEqual(json.loads((ROOT/'orchestration/examples'/name).read_text()),json.loads(json.dumps(value,default=str)))
    def test_cli_bad_input_safe_public_answer(self):
        r=subprocess.run([sys.executable,'-m','orchestration.run_case','/no-such-request'],capture_output=True,text=True,check=True,cwd=ROOT)
        output=json.loads(r.stdout);self.assertEqual('blocked',output['status']);self.assertNotIn('Traceback',r.stdout)
    def test_internal_full_record_serializes(self):
        c=CAO().run(manufacturing());r=json.loads(json.dumps(c.record(),default=str))
        self.assertTrue(r['evidence_refs']);self.assertTrue(r['knowledge_refs']);self.assertTrue(r['workplan_nodes'][0]['result']['facts_used'])
        self.assertTrue(CAO().public(c)['limitations']);self.assertNotIn('evidence_refs',CAO().public(c))

if __name__=='__main__':unittest.main()

import json
import base64
import gzip
import hashlib
import unittest
from orchestration.tests.generate_persistence_stage2_examples import artifacts, TARGET

class DurableRecoveryArtifactReproduction(unittest.TestCase):
    def test_interrupted_accounting_artifacts_reproduce(self):
        actual=artifacts()
        self.assertEqual(set(actual),{p.name for p in TARGET.glob('*.json')})
        for name,value in actual.items():self.assertEqual(value,json.loads((TARGET/name).read_text()),name)
        from orchestration.persistence.codec import loads
        from orchestration.persistence import restore
        for value in actual.values():
            if value.get('encoding') == 'gzip-base64 canonical audit JSON':
                wire=gzip.decompress(base64.b64decode(value['payload']))
                self.assertEqual(hashlib.sha256(wire).hexdigest(),value['sha256'])
                self.assertIsInstance(loads(wire.decode()),dict)
        for archive in actual['full-native-checkpoints.json'].values():
            wire=gzip.decompress(base64.b64decode(archive['payload']))
            self.assertEqual(hashlib.sha256(wire).hexdigest(),archive['sha256'])
            doc=loads(wire.decode());restore(doc,doc['company_id'],doc['root_case'])
        self.assertEqual(actual['restart-recovery-proof.json']['result'],'PASS')
        self.assertTrue(actual['restart-recovery-proof.json']['closed_period_reopened_then_corrected_reworked_reclosed'])
        self.assertFalse(actual['restart-recovery-proof.json']['external_posting_proved'])

if __name__=='__main__':unittest.main()

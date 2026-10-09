import base64
import gzip
import hashlib
import json
import unittest
from orchestration.persistence import restore,snapshot
from orchestration.persistence.codec import loads,dumps
from orchestration.tests.generate_persistence_stage3_examples import artifacts,TARGET

class MemoryArtifactProof(unittest.TestCase):
    def test_seven_process_native_proof_and_complete_envelopes_reproduce(self):
        actual=artifacts();self.assertEqual(set(actual),{p.name for p in TARGET.glob('*.json')})
        def decode(value):
            if isinstance(value,dict) and value.get('encoding')=='gzip-base64 canonical audit JSON':
                wire=gzip.decompress(base64.b64decode(value['payload']));self.assertEqual(hashlib.sha256(wire).hexdigest(),value['sha256']);return loads(wire.decode())
            return value
        for name,value in actual.items():self.assertEqual(value,json.loads((TARGET/name).read_text()),name)
        self.assertEqual(actual['proof-summary.json']['result'],'PASS')
        for name,value in actual.items():
            value=decode(value)
            if isinstance(value,dict) and 'checkpoint' in value:
                doc=decode(value['checkpoint']);case=restore(doc,doc['company_id'],doc['root_case']);self.assertEqual(dumps(snapshot(case,doc['company_id'],doc['company_context'])),dumps(doc))
        final=decode(actual['restore.json']);self.assertEqual(final['result'],'PASS');self.assertEqual(len(final['audit']['uses']),1)
        correction=decode(actual['correction.json']);self.assertTrue(correction['native_journals_unchanged']);self.assertTrue(correction['durable_operation'].startswith('operation:'))
if __name__=='__main__':unittest.main()

"""Reexecute the connected durable proof and verify complete retained authorities."""
import base64
import gzip
import hashlib
import json
import unittest
from orchestration.persistence import restore,snapshot
from orchestration.persistence.codec import loads,dumps
from orchestration.tests.generate_persistence_stage4_examples import artifacts,TARGET


def decode(value):
    if isinstance(value,dict) and value.get('encoding')=='gzip-base64 canonical audit JSON':
        wire=gzip.decompress(base64.b64decode(value['payload']))
        if hashlib.sha256(wire).hexdigest()!=value['sha256']:raise AssertionError('Lossless authority envelope hash differs')
        return loads(wire.decode())
    return value


class FullDurableArtifactProof(unittest.TestCase):
    def test_fresh_process_full_company_proof_reproduces_and_restores(self):
        actual=artifacts();self.assertEqual(set(actual),{p.name for p in TARGET.glob('*.json')})
        for name,value in actual.items():self.assertEqual(value,json.loads((TARGET/name).read_text()),name)
        docs={name:decode(value) for name,value in actual.items()}
        self.assertEqual(docs['interrupt.json']['actual_exit'],73);self.assertEqual(docs['lost-ack.json']['actual_exit'],74)
        company=docs['company.json'];old=decode(company['checkpoint']);before=decode(docs['correction.json']['before']);resumed=decode(docs['resume.json']['checkpoint'])
        operation=docs['correction.json']['operation'];plan=operation['events'][-1]['value']['result']
        for key in plan['unaffected']:self.assertEqual(before['active'][key],resumed['active'][key])
        for key,value in old['versions'].items():
            self.assertEqual(value,resumed['versions'][key]);self.assertEqual(old['source_snapshots'][key],resumed['source_snapshots'][key])
        self.assertEqual(len(plan['execution_order']),4)
        self.assertNotEqual(company['initial_negative']['public']['status'],'complete')
        self.assertFalse(docs['correction.json']['memory_refusal']['qualified'])
        self.assertFalse(docs['resume.json']['memory_refusal']['qualified'])
        self.assertTrue(docs['reuse.json']['no_memory_financial_edge'])
        self.assertTrue(docs['repeat.json']['no_repeat_execution'])
        self.assertEqual(len(docs['repeat.json']['operation']['events'][-1]['value']['result']['selected']),8)
        self.assertEqual(docs['successor.json']['resolved']['status'],'DOCUMENTED')
        self.assertEqual(docs['reuse-successor.json']['context'],'Xero')
        final=docs['restore.json'];self.assertEqual(final['result'],'PASS');self.assertEqual(len(final['audit']['uses']),2)
        repeat=decode(docs['repeat.json']['checkpoint'])
        final_primary=next(r for r in final['roots'] if r['root']==repeat['root_case'])
        self.assertEqual(dumps(decode(final_primary['checkpoint'])),dumps(repeat))
        original_use=next(u for u in final['audit']['uses'] if u['value']['memory_version']==docs['reuse.json']['use']['memory_version'])
        self.assertEqual(original_use['value'],docs['reuse.json']['use'])
        self.assertTrue(docs['unresolved.json']['refusal']['conflicts']);self.assertFalse(docs['unresolved.json']['refusal']['qualified'])
        self.assertNotEqual(docs['unresolved.json']['public']['status'],'complete')
        self.assertEqual(len(final['roots']),5)
        negative=next(r for r in final['roots'] if r['root']==docs['unresolved.json']['root'])
        self.assertEqual(negative['public'],docs['unresolved.json']['public'])
        self.assertEqual(sum(r['public']['status']!='complete' for r in final['roots']),1)
        checkpoints=[]
        for value in docs.values():
            if isinstance(value,dict) and 'checkpoint' in value:checkpoints.append(decode(value['checkpoint']))
        checkpoints.append(decode(company['initial_negative']['checkpoint']))
        checkpoints.extend(decode(r['checkpoint']) for r in final['roots'])
        for doc in checkpoints:
            case=restore(doc,doc['company_id'],doc['root_case'])
            self.assertEqual(dumps(snapshot(case,doc['company_id'],doc['company_context'])),dumps(doc))
        self.assertEqual(docs['proof-summary.json']['fresh_processes'],14)
if __name__=='__main__':unittest.main()

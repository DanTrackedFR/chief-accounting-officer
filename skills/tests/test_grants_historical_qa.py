"""Independent additive synthetic history integrity review for grants release."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'skills/government-grants/release-evidence/historical-qa'
class GrantsHistoryQA(unittest.TestCase):
 def test_all_published_historical_examples_and_evidence_are_byte_preserved(self):
  report=json.loads((HERE/'original-pr42-preservation.json').read_text());self.assertEqual('PASS',report['status']);self.assertEqual([],report['changed']);self.assertEqual(1867,len(report['files']))
  for name,expected in report['files'].items():self.assertEqual(expected,hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),name)
 def test_specialist_original_and_predecessor_bytes_are_immutable(self):
  report=json.loads((HERE/'specialist-migration.json').read_text())
  self.assertEqual(548,report['compared_files']);self.assertEqual([],report['changed_public_outputs'])
  for name,row in report['files'].items():
   for path,key in ((ROOT/name,'original_sha256'),(ROOT/row['previous_path'],'previous_sha256'),(ROOT/row['current_path'],'current_sha256')):
    self.assertEqual(row[key],hashlib.sha256(path.read_bytes()).hexdigest(),str(path))
 def test_migration_changes_only_bijective_digest_fields(self):
  report=json.loads((HERE/'specialist-migration.json').read_text());allowed={'case_fingerprint','payload_fingerprint','owner_result_fingerprint','content_hash','body_hash'};forward={};reverse={}
  def compare(a,b,path):
   self.assertEqual(type(a),type(b),path)
   if isinstance(a,dict):
    self.assertEqual(set(a),set(b),path)
    for key in a:compare(a[key],b[key],path+'/'+key)
   elif isinstance(a,list):
    self.assertEqual(len(a),len(b),path)
    for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
   elif a!=b:
    self.assertIn(path.split('/')[-1],allowed,path)
    for x in (a,b):self.assertRegex(x,r'^[0-9a-f]{64}$',path)
    self.assertEqual(forward.setdefault(a,b),b,path);self.assertEqual(reverse.setdefault(b,a),a,path)
  for name,row in report['files'].items():
   self.assertFalse(name.endswith('.public.json'))
   compare(json.loads((ROOT/row['previous_path']).read_text()),json.loads((ROOT/row['current_path']).read_text()),name)
  self.assertEqual(report['identity_map'],forward)
 def test_omitted_reopened_bundle_digests_are_proved_by_full_native_authorities(self):
  import base64,gzip
  from orchestration.persistence.codec import loads
  from orchestration.tests.generate_persistence_stage2_examples import project
  report=json.loads((HERE/'stage2-full-authority-review.json').read_text());self.assertEqual('PASS',report['status']);self.assertEqual([],report['errors']);self.assertEqual(26,report['archive_count']);self.assertTrue(report['reconstructed_matches_real_sqlite_capture'])
  for part in report['source_archive']['parts']:self.assertEqual(part['sha256'],hashlib.sha256((ROOT/part['path']).read_bytes()).hexdigest())
  for filename,key in (('stage2-pr42-rework-full.json','old_full_sha256'),('stage2-reconstructed-native.json','new_full_sha256')):self.assertEqual(report[key],hashlib.sha256((HERE/filename).read_bytes()).hexdigest())
  envelope=json.loads((HERE/'stage2-reconstructed-native.json').read_text());wire=gzip.decompress(base64.b64decode(envelope['payload']));self.assertEqual(envelope['sha256'],hashlib.sha256(wire).hexdigest());actual=project(loads(wire.decode())['checkpoint'])['retained_evidence']
  source=json.loads((HERE/'orchestration-fresh/durable-rework-recovery/closed-reopened-period.json').read_text());wire=gzip.decompress(base64.b64decode(source['payload']));self.assertEqual(source['sha256'],hashlib.sha256(wire).hexdigest());expected=json.loads(wire)['rework']['checkpoint']['retained_evidence'];self.assertEqual(expected,actual)
 def test_integrated_and_orchestration_reviews_have_no_semantic_errors(self):
  for name in ('orchestration-migration.json','main-proof-migration.json'):
   report=json.loads((HERE/name).read_text());self.assertTrue(report['passed']);self.assertEqual([],report['errors'])
   for original,row in report['files'].items():
    for path,key in ((ROOT/original,'original_sha256'),(ROOT/row['previous_path'],'previous_sha256'),(ROOT/row['current_path'],'current_sha256')):self.assertEqual(row[key],hashlib.sha256(path.read_bytes()).hexdigest(),str(path))
 def test_exact_grant_promotion_labels_preserve_safe_blocked_graph_and_public_amounts(self):
  report=json.loads((HERE/'orchestration-migration.json').read_text());self.assertEqual(2,len(report['approved_behavior_transitions']))
  graph='orchestration/examples/manufacturing.partial.graph.json';row=report['files'][graph]
  old=json.loads((ROOT/row['previous_path']).read_text());new=json.loads((ROOT/row['current_path']).read_text())
  self.assertEqual([n['status'] for n in old],[n['status'] for n in new]);self.assertEqual('government-grants',new[13]['selected_skill']);self.assertEqual('blocked',new[13]['status']);self.assertEqual({},new[13]['execution_receipt']);self.assertNotIn('result',new[13]);self.assertEqual(['Missing reviewed source workpaper for grant'],new[13]['open_items'])
  public='orchestration/examples/manufacturing.partial.public.json';row=report['files'][public];old=json.loads((ROOT/row['previous_path']).read_text());new=json.loads((ROOT/row['current_path']).read_text())
  self.assertEqual(['grant: Accounting owner unavailable for production: government-grants'],old['open_items']);self.assertEqual(['grant: Missing reviewed source workpaper for grant'],new['open_items']);old.pop('open_items');new.pop('open_items');self.assertEqual(old,new)
 def test_main_proof_resolver_requires_actual_approved_predecessor(self):
  from unittest.mock import patch
  from orchestration.history_references import reference_path
  manifest=HERE/'main-proof-migration.json';report=json.loads(manifest.read_text());name,row=next(iter(report['files'].items()));native=Path.read_text;report['files'][name]['previous_path']=name;report['files'][name]['previous_sha256']=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
  def changed(path,*args,**kwargs):return json.dumps(report) if path==manifest else native(path,*args,**kwargs)
  with patch.object(Path,'read_text',changed):
   with self.assertRaisesRegex(AssertionError,'preceding approved proof'):reference_path(name)
 def test_layered_resolver_rejects_changed_current_bytes(self):
  from unittest.mock import patch
  from orchestration.history_references import reference_path
  report=json.loads((HERE/'specialist-migration.json').read_text());name,row=next(iter(report['files'].items()));target=ROOT/row['current_path'];native=Path.read_bytes
  def changed(path):return b'changed synthetic bytes' if path==target else native(path)
  with patch.object(Path,'read_bytes',changed):
   with self.assertRaisesRegex(AssertionError,'changed without reviewed'):reference_path(name)
 def test_layered_resolver_rejects_arbitrary_predecessor_and_namespace(self):
  from unittest.mock import patch
  from orchestration.history_references import reference_path
  manifest=HERE/'specialist-migration.json';report=json.loads(manifest.read_text());name,row=next(iter(report['files'].items()));native=Path.read_text
  for field,value in (('previous_path',name),('current_path',row['previous_path'])):
   edited=json.loads(json.dumps(report));edited['files'][name][field]=value
   if field=='previous_path':edited['files'][name]['previous_sha256']=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
   def changed(path,*args,**kwargs):return json.dumps(edited) if path==manifest else native(path,*args,**kwargs)
   with patch.object(Path,'read_text',changed):
    with self.assertRaises(AssertionError):reference_path(name)
if __name__=='__main__':unittest.main()

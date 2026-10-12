"""Independent AI engineering review against detached e753 main, not a2.

Baseline values were executed before reconciliation in a separate main worktree.
These synthetic assertions do not supply actual company accounting approvals.
"""
import hashlib
import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'skills'),str(ROOT/'skills/tests')]
from production import assess_case, case_fingerprint, serializable
from borrowing_costs_cases import case as borrowing_case, ready as borrowing_ready
from grant_cases import case as grant_case, ready as grant_ready

MAIN = 'e75375b84813b9d584db12aa692b2f4d16baf052'
BASELINES = {
 ('borrowing-costs','IFRS'): ('d50409cffccbecd1006bdd2d88cc0c336ed16b26519d886205ad9b64c8489537','6405abc524519af07dfab7c9aafacbfa74c970dde9f1301eb0a9b0a8cbec5bcf'),
 ('borrowing-costs','AASB'): ('5a8b36a12258e2ddc780e49bedf0ed6216db362a316595aade1c1c20a083f5fb','b32bd2a7c6b9a008866c5182ce15cf4b780a3fef47156bbeda24c04018e42f79'),
 ('borrowing-costs','US_GAAP'): ('ef709e949183a02efe02584ba90c07c3292f56f062d2607194821222fb3839fe','579383b8ca5ffde6acac973453095dcf77d429fa94d57ae2235b615419098748'),
 ('borrowing-costs','UK_GAAP'): ('dc8ddeebd6f60b9da15123ec5d05dbc9a1cc5be18bcec7d6603c812500777625','411ce37039784ed3c0e5dcc0cf3c3e5d7fc66457817b7df40067fff4c13c6855'),
 ('government-grants','IFRS'): ('a9a434f63dd4dc0f4d16672925ca6be8ef78615d18c439af7bf68334d0c40342','12518b000d619c0d097699e92b6105996f97fda629376c5dc91e012c3bb08940'),
 ('government-grants','AASB'): ('f5515cf81d922f02eb6fc722fef40b012d4f68ce94099ea88be697151237f669','ee3b76b08051c120abb9e1fd411a753262abc73233755cb2ad414f967f0c6a2b'),
 ('government-grants','US_GAAP'): ('520422367fa6b575dc79e06e74dc53313b07956f041bb588725f5581555c43bd','b889dcd3dafd0950c5c9b204d5311da09b4a4f16c2f5866300c247eefa3f508d'),
 ('government-grants','UK_GAAP'): ('7b80b09e73e35f64593516795f04253523a7d0fb23c0a4fe9b3ab856a405dea5','25876a45ea5a5657e7b2a010f5979ae1eb20bc4b35dd9feeae5627535edf704d'),
}

class IndependentMainReconciliation(unittest.TestCase):
 def test_adapter_change_is_only_additive_investment_population(self):
  from orchestration.planning import FACT_ADAPTERS
  baseline=subprocess.check_output(['git','show',MAIN+':orchestration/planning.py'],cwd=ROOT,text=True)
  assignment=next(n for n in ast.parse(baseline).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FACT_ADAPTERS' for t in n.targets))
  original=ast.literal_eval(assignment.value)
  self.assertEqual(('investment-property',('property',)),original['rental_investment'])
  self.assertEqual(('investment-property',('property','properties')),FACT_ADAPTERS['rental_investment'])
  current=dict(FACT_ADAPTERS);current['rental_investment']=original['rental_investment']
  self.assertEqual(original,current)

 def test_promoted_metadata_preserves_exact_original_contract(self):
  original=subprocess.check_output(['git','show',MAIN+':skills/investment-property/SKILL.md'],cwd=ROOT)
  self.assertEqual(original,(ROOT/'skills/investment-property/examples/legacy-skill-v0.1.0.md').read_bytes())
  self.assertIn('status: production',(ROOT/'skills/investment-property/SKILL.md').read_text())
  listing=subprocess.check_output(['git','ls-tree','-r',MAIN,'--','skills'],cwd=ROOT,text=True)
  count=0
  for line in listing.splitlines():
   meta,name=line.split('\t',1)
   if not name.endswith('/SKILL.md') or name=='skills/investment-property/SKILL.md':continue
   self.assertEqual(meta.split()[2],subprocess.check_output(['git','hash-object',str(ROOT/name)],cwd=ROOT,text=True).strip(),name)
   if 'status: production' in (ROOT/name).read_text():count+=1
  self.assertEqual(49,count)

 def test_additive_bridge_exactly_matches_real_main_dispatcher(self):
  from investment_fingerprint import BASELINE_SHA,expected_dispatch
  baseline=subprocess.check_output(['git','show',MAIN+':skills/production.py'],cwd=ROOT)
  witness=ROOT/'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'
  self.assertEqual(baseline,witness.read_bytes())
  self.assertEqual(BASELINE_SHA,hashlib.sha256(baseline).hexdigest())
  helper_hash=hashlib.sha256((ROOT/'skills/investment_fingerprint.py').read_bytes()).hexdigest()
  self.assertEqual(expected_dispatch(baseline.decode(),helper_hash),(ROOT/'skills/production.py').read_text())
  old=ROOT/'skills/investment-property/fingerprint-baseline/production.py.txt'
  self.assertEqual('b452b2b46d56ad1f72cf7e87fdcadc9e8b7923a6d42c8945aac4589f291b7f52',hashlib.sha256(old.read_bytes()).hexdigest())

 def test_both_merged_specialists_exact_case_fingerprints(self):
  for (pkg, fw), (expected, _) in BASELINES.items():
   with self.subTest(package=pkg, framework=fw):
    c = (borrowing_case if pkg=='borrowing-costs' else grant_case)(fw)
    self.assertEqual(expected, case_fingerprint(c))

 def test_both_merged_specialists_full_result_bytes_unchanged(self):
  for (pkg, fw), (_, expected) in BASELINES.items():
   with self.subTest(package=pkg, framework=fw):
    c = (borrowing_ready if pkg=='borrowing-costs' else grant_ready)(fw)
    result = assess_case(pkg,c)
    self.assertEqual('complete',result['status'])
    digest = hashlib.sha256(json.dumps(result,sort_keys=True,default=serializable).encode()).hexdigest()
    self.assertEqual(expected,digest)

 def test_stale_approvals_do_not_publish_borrowing_or_grant_journals(self):
  for pkg, factory in [('borrowing-costs',borrowing_ready),('government-grants',grant_ready)]:
   c=factory();c['reviewer_signoff']['case_fingerprint']='0'*64
   result=assess_case(pkg,c)
   self.assertEqual('partial',result['status'])
   self.assertEqual([],result['journal_entry_implications'])
   self.assertTrue(result['proposed_journal_workpaper'])

 def test_common_accounting_changes_invalidate_both_owner_certificates(self):
  native_bytes=Path.read_bytes;native_text=Path.read_text
  target=ROOT/'skills/production.py'
  def changed_bytes(p,*a,**k):
   return native_bytes(p,*a,**k)+b'\n# substantive shared edit\n' if p==target else native_bytes(p,*a,**k)
  def changed_text(p,*a,**k):
   return native_text(p,*a,**k)+'\n# substantive shared edit\n' if p==target else native_text(p,*a,**k)
  for pkg, factory in [('borrowing-costs',borrowing_case),('government-grants',grant_case)]:
   c=factory();before=case_fingerprint(c)
   with patch.object(Path,'read_bytes',changed_bytes),patch.object(Path,'read_text',changed_text):
    self.assertNotEqual(before,case_fingerprint(c))

 def test_byte_only_dispatch_mutation_cannot_be_hidden_by_original_text(self):
  native=Path.read_bytes
  def changed(p,*a,**k):
   value=native(p,*a,**k)
   return value+b'\n# byte-only shared accounting mutation\n' if p==ROOT/'skills/production.py' else value
  for factory in (borrowing_case,grant_case):
   c=factory();before=case_fingerprint(c)
   with patch.object(Path,'read_bytes',changed):
    self.assertNotEqual(before,case_fingerprint(c))

 def test_byte_only_witness_mutation_cannot_be_hidden_by_original_text(self):
  native=Path.read_bytes
  target=ROOT/'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'
  def changed(p,*a,**k):
   value=native(p,*a,**k)
   return value+b'\n# byte-only witness mutation\n' if p==target else value
  c=borrowing_case();before=case_fingerprint(c)
  with patch.object(Path,'read_bytes',changed):self.assertNotEqual(before,case_fingerprint(c))

 def test_captured_dispatch_digest_mismatch_never_normalizes(self):
  from investment_fingerprint import bind_investment_dispatch
  from implementation_scope import fingerprint_files
  from production import PACKAGES
  c=borrowing_case();files=fingerprint_files(c,ROOT,PACKAGES)
  actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
  actual['skills/production.py']='0'*64
  self.assertEqual(actual,bind_investment_dispatch(c,ROOT,PACKAGES,files,actual))

 def test_normalizer_reads_authoritative_bytes_not_unrelated_text_view(self):
  from investment_fingerprint import bind_investment_dispatch,BASELINE_SHA
  from implementation_scope import fingerprint_files
  from production import PACKAGES
  c=borrowing_case();files=fingerprint_files(c,ROOT,PACKAGES)
  actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
  native=Path.read_text
  targets={ROOT/'skills/production.py',ROOT/'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'}
  def inconsistent(p,*a,**k):
   return 'incongruent non-authoritative text view' if p in targets else native(p,*a,**k)
  with patch.object(Path,'read_text',inconsistent):
   result=bind_investment_dispatch(c,ROOT,PACKAGES,files,actual)
  self.assertEqual(BASELINE_SHA,result['skills/production.py'])

 def test_owner_scoped_closure_has_no_investment_source_coupling(self):
  from implementation_scope import fingerprint_files
  from production import PACKAGES
  for factory in (borrowing_case,grant_case):
   names=[str(p.relative_to(ROOT)) for p in fingerprint_files(factory(),ROOT,PACKAGES)]
   self.assertFalse(any('investment' in name for name in names))
  self.assertTrue(any('grant_knowledge.py' in str(p) for p in fingerprint_files(grant_case(),ROOT,PACKAGES)))
  self.assertTrue(any('borrowing_knowledge.py' in str(p) for p in fingerprint_files(borrowing_case(),ROOT,PACKAGES)))

 def test_bridge_or_witness_tamper_cannot_keep_existing_certification(self):
  native_bytes=Path.read_bytes;native_text=Path.read_text
  for target in (ROOT/'skills/investment_fingerprint.py',
                 ROOT/'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'):
   def changed_bytes(p,*a,**k):
    return native_bytes(p,*a,**k)+b'\n# tampered\n' if p==target else native_bytes(p,*a,**k)
   def changed_text(p,*a,**k):
    return native_text(p,*a,**k)+'\n# tampered\n' if p==target else native_text(p,*a,**k)
   c=borrowing_case();before=case_fingerprint(c)
   with self.subTest(target=target),patch.object(Path,'read_bytes',changed_bytes),patch.object(Path,'read_text',changed_text):
    self.assertNotEqual(before,case_fingerprint(c))

 def test_unrelated_investment_knowledge_cannot_expire_other_owners(self):
  native=Path.read_bytes
  def changed(p,*a,**k):
   return native(p,*a,**k)+b'\n# changed investment method\n' if p==ROOT/'skills/investment_knowledge.py' else native(p,*a,**k)
  for factory in (borrowing_case,grant_case):
   c=factory();before=case_fingerprint(c)
   with patch.object(Path,'read_bytes',changed):self.assertEqual(before,case_fingerprint(c))

 def test_prior_knowledge_owners_and_all_historical_bytes_equal_main(self):
  paths=['knowledge','skills/borrowing-costs','skills/government-grants',
         'orchestration/examples','orchestration/persistence','build4/examples']
  listing=subprocess.check_output(['git','ls-tree','-r',MAIN,'--',*paths],cwd=ROOT,text=True)
  count=0
  for line in listing.splitlines():
   meta,name=line.split('\t',1);blob=meta.split()[2]
   if name.startswith('knowledge/investment-property/'):
    continue
   self.assertTrue((ROOT/name).is_file(),name)
   current=subprocess.check_output(['git','hash-object',str(ROOT/name)],cwd=ROOT,text=True).strip()
   self.assertEqual(blob,current,name);count+=1
  self.assertGreater(count,2000)

if __name__=='__main__':unittest.main()

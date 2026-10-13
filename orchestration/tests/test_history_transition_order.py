"""Independent AI adversarial review of successor provenance qualification.

Tests never modify original historical artifacts or the frozen PR42 reviewer.
Multi-member inventory membership is a constraint, not an authority for learning
identities. A unique singleton role preserves the original reviewer's bounded
correspondence inference; that is not separate native producer certification.
"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

from orchestration.history_transition import Transition

ROOT=Path(__file__).resolve().parents[2]
A='a'*64
B='b'*64
C='c'*64
D='d'*64


def inventory(values):
    return {'required_legal_result_versions':['version:'+x for x in values]}


def anchors():
    return ({'producer_a':'version:'+A,'producer_b':'version:'+B},
            {'producer_a':'version:'+D,'producer_b':'version:'+C})


class IndependentHistoryOrderQA(unittest.TestCase):
    def test_inventory_first_never_learns_identity_mapping(self):
        r=Transition();r.seed(inventory([A,B]),inventory([C,D]),'first-file')
        self.assertEqual({},r.forward)
        r.compare(inventory([A,B]),inventory([C,D]),'first-file')
        self.assertEqual({},r.forward)
        self.assertEqual({},r.reverse)
        r.compare(*anchors(),'second-file');r.finish()
        self.assertEqual([],r.errors)
        self.assertEqual({A:D,B:C},r.forward)

    def test_file_order_independent_across_deliberately_swapped_digest_order(self):
        outcomes=[]
        for first in ('inventory','anchors'):
            r=Transition()
            pairs=[(inventory([A,B]),inventory([C,D]),'inventory-file'),(*anchors(),'anchor-file')]
            if first=='anchors':pairs.reverse()
            for a,b,path in pairs:r.compare(a,b,path)
            r.finish();self.assertEqual([],r.errors)
            outcomes.append((r.forward,r.reverse))
        self.assertEqual(outcomes[0],outcomes[1])

    def test_unknown_inventory_fails_final_gate_without_manufacturing_map(self):
        r=Transition();r.compare(inventory([A,B]),inventory([C,D]),'opaque-only')
        r.finish();self.assertTrue(r.errors)
        self.assertEqual({},r.forward)
        self.assertEqual({},r.reverse)

    def test_unchanged_exact_inventory_bytes_require_no_new_migration(self):
        r=Transition();r.compare(inventory([A,B]),inventory([A,B]),'unanchored-same-multi')
        r.finish();self.assertEqual([],r.errors);self.assertEqual({},r.forward)

    def test_unknown_changed_singleton_without_explicit_seed_fails(self):
        r=Transition();r.compare(inventory([A]),inventory([D]),'unseeded-role')
        r.finish();self.assertTrue(r.errors);self.assertEqual({},r.forward)

    def test_singleton_unique_role_retains_original_bounded_inference(self):
        r=Transition();r.seed(inventory([A]),inventory([D]),'one-unique-role')
        r.compare(inventory([A]),inventory([D]),'one-unique-role')
        r.finish();self.assertEqual([],r.errors);self.assertEqual({A:D},r.forward)

    def test_singleton_unique_role_cannot_split_existing_identity(self):
        r=Transition();r.seed(inventory([A]),inventory([C]),'one-unique-role')
        r.seed(inventory([A]),inventory([D]),'contradictory-unique-role')
        r.finish();self.assertTrue(r.errors)

    def test_singleton_unique_role_cannot_collapse_distinct_identities(self):
        r=Transition();r.seed(inventory([A]),inventory([C]),'one-unique-role')
        r.seed(inventory([B]),inventory([C]),'different-unique-role')
        r.finish();self.assertTrue(r.errors)

    def test_stable_unchanged_inventory_identity_preserved(self):
        r=Transition();r.stable={A};r.compare(inventory([A]),inventory([A]),'stable')
        r.finish();self.assertEqual([],r.errors);self.assertEqual({},r.forward)

    def test_wrong_producer_same_population_size_fails(self):
        r=Transition();r.bind(A,D,'native producer')
        r.compare(inventory([A]),inventory([C]),'wrong-producer')
        r.finish();self.assertTrue(r.errors);self.assertEqual({A:D},r.forward)

    def test_missing_inventory_member_fails(self):
        r=Transition();r.compare(*anchors(),'native producer')
        r.compare(inventory([A,B]),inventory([D]),'omission')
        r.finish();self.assertTrue(r.errors)

    def test_extra_or_duplicate_inventory_member_fails(self):
        for current in ([C,D,D],[C,C]):
            with self.subTest(current=current):
                r=Transition();r.compare(*anchors(),'native producer')
                r.compare(inventory([A,B]),inventory(current),'extra-or-duplicate')
                r.finish();self.assertTrue(r.errors)

    def test_old_identity_split_still_fails(self):
        r=Transition();r.bind(A,C,'producer one');r.bind(A,D,'producer two')
        r.finish();self.assertTrue(r.errors)

    def test_distinct_identity_collapse_still_fails(self):
        r=Transition();r.bind(A,C,'producer one');r.bind(B,C,'producer two')
        r.finish();self.assertTrue(r.errors)

    def test_accounting_amount_changes_still_fail(self):
        r=Transition();r.compare({'amount':'1'*64},{'amount':'2'*64},'accounting amount')
        r.finish();self.assertTrue(r.errors)

    def test_real_historical_population_reproduces_bad_and_good_seed(self):
        command=[sys.executable,'-m','unittest',
                 'orchestration.tests.test_history_qualification.HistoryQualification.test_recorded_orchestration_transition_reperforms','-v']
        for seed in ('23','19'):
            with self.subTest(seed=seed):
                result=subprocess.run(command,cwd=ROOT,env={**os.environ,'PYTHONHASHSEED':seed},
                                      capture_output=True,text=True,timeout=180)
                self.assertEqual(0,result.returncode,result.stdout+result.stderr)
                self.assertIn('Ran 1 test',result.stdout+result.stderr)
                self.assertIn('OK',result.stdout+result.stderr)


if __name__=='__main__':unittest.main()

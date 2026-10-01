import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("approvals", ROOT / "knowledge/standards-evidence/validate_approvals.py")
approvals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(approvals)

class ApprovalContractTests(unittest.TestCase):
    def setUp(self):
        manifest = json.loads((ROOT / "knowledge/phase-2d-topic-manifest.json").read_text())
        self.topic = next(t for t in manifest["topics"] if t["topic_id"] == "TOPIC-17-004")
        register_path = next(p for p in self.topic["artifact_paths"] if p.endswith("/standards-claims.json"))
        self.register = json.loads((ROOT / register_path).read_text())
        self.review = json.loads((ROOT / "knowledge/phase-2e/reviews/TOPIC-17-004.json").read_text())

    def check(self):
        return approvals.validate_topic(self.topic, self.register, self.review)

    def test_entire_canonical_population_and_individual_evidence(self):
        result = approvals.audit()
        self.assertEqual([], result["error_details"])
        self.assertEqual((157, 157, 157, 347),
                         (result["topics"], result["approved"], result["canonical_registers"], result["capabilities"]))

    def test_training_review_cannot_be_relabelled_as_source_verified(self):
        self.register["claims"][0]["evidence_status"] = "SOURCE_VERIFIED"
        self.assertTrue(any("overstated" in e for e in self.check()))

    def test_unchecked_proposition_or_material_conflict_blocks_approval(self):
        self.review["claim_checks"].pop()
        self.assertTrue(any("coverage" in e for e in self.check()))
        self.review["blockers"] = ["Unresolved conflicting measurement basis"]
        self.assertTrue(any("unresolved topic" in e for e in self.check()))

    def test_dates_scope_and_recorded_review_are_required(self):
        self.register["claims"][0]["effective_period"] = None
        self.register["claims"][0]["model_reviews"] = []
        errors = self.check()
        self.assertTrue(any("effective_period" in e for e in errors))
        self.assertTrue(any("independent training" in e for e in errors))

    def test_empty_register_requires_explicit_non_normative_scope_review(self):
        self.register["claims"] = []
        self.review["claim_checks"] = []
        self.assertTrue(any("empty register" in e for e in self.check()))
        self.review["claim_register_disposition"] = "NON_NORMATIVE_SCOPE_REVIEW"
        self.assertEqual([], self.check())

    def test_direct_source_needs_inspected_operative_authority(self):
        direct = next(c for c in self.register["claims"] if c["approval_track"] == "DIRECT_SOURCE_CHECKED")
        for source in direct["sources"]:
            source["inspected"] = False
        self.assertTrue(any("operative authority" in e for e in self.check()))

if __name__ == "__main__":
    unittest.main()

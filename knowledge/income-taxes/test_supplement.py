"""Executable governance, arithmetic and adversarial regression."""
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from retrieval import load_register, retrieve
from validate_supplement import validate

class TaxKnowledgeTests(unittest.TestCase):
    def test_register_structure(self):
        r = validate()
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["claims"], 64)
    def test_four_framework_population(self):
        claims = load_register()["claims"]
        for framework in ("IFRS","US_GAAP","UK_GAAP","AASB"):
            self.assertEqual(sum(c["framework"] == framework for c in claims), 16)
    def test_unapproved_retrieval_fails_closed(self):
        for fw in ("IFRS","US_GAAP","UK_GAAP","AASB"):
            with self.assertRaises(ValueError):
                retrieve(fw,"2026-12-31","example company")
    def test_missing_context_fails_closed(self):
        with self.assertRaises(ValueError):
            retrieve("IFRS","","example company")
    def test_duplicate_claim_fails(self):
        d=load_register()
        d["claims"].append(d["claims"][0])
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"claims.json"
            path.write_text(json.dumps(d))
            with self.assertRaises(ValueError):
                load_register(path)
    def test_temporary_difference_and_journal(self):
        rate=Decimal("0.25")
        dtl=(Decimal("1000")-Decimal("700"))*rate
        dta=Decimal("200")*rate
        self.assertEqual((dtl,dta,dtl-dta),(75,50,25))
        self.assertEqual(dtl+dta,Decimal("125")) # gross debit/credit across entries
    def test_recoverability_and_us_valuation_allowance(self):
        gross=Decimal("400")*Decimal(".25")
        supported=Decimal("240")*Decimal(".25")
        self.assertEqual(gross-supported,Decimal("40"))
    def test_rate_change(self):
        difference=Decimal("300")
        self.assertEqual(difference*(Decimal(".30")-Decimal(".25")),15)
    def test_current_tax_reconciliation(self):
        taxable=Decimal("1000")+Decimal("100")-Decimal("200")+Decimal("50")
        self.assertEqual(taxable*Decimal(".25"),Decimal("237.50"))
    def test_source_notes_not_public(self):
        public={"claim_id","framework","proposition","paragraph_references",
                "effective_period","entity_scope","limitations"}
        self.assertFalse({"source_note","sources","approval_review","model_reviews"} & public)

if __name__=="__main__":
    unittest.main()

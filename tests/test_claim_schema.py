import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('claim_schema_validation',ROOT/'knowledge/standards-evidence/schema_validation.py')
MODULE=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MODULE)

class SchemaTests(unittest.TestCase):
    def test_existing_registers_conform_to_actual_schema(self):
        schema=json.loads((ROOT/'knowledge/standards-evidence/claim.schema.json').read_text())
        for path in ROOT.glob('knowledge/topics/*/standards-claims.json'):
            with self.subTest(path=path):
                self.assertEqual(MODULE.validate(json.loads(path.read_text()),schema),[])
    def test_rejects_missing_required_unknown_fields_and_wrong_types(self):
        schema={'type':'object','required':['name'],'properties':{'name':{'type':'string','minLength':1}},'additionalProperties':False}
        for invalid in ({},{'name':''},{'name':[]},{'name':'ok','private':True}):
            self.assertTrue(MODULE.validate(invalid,schema))
        self.assertEqual(MODULE.validate({'name':'ok'},schema),[])
    def test_future_schema_constructs_require_implementation(self):
        self.assertTrue(MODULE.validate({}, {'oneOf':[]}))

if __name__=='__main__':unittest.main()

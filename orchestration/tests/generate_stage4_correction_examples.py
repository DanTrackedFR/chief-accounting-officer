"""Deterministic Outcome B artifacts from native accounting and permanent QA."""
import json
import unittest
from pathlib import Path
from orchestration.tests.stage4_correction_fixtures import artifacts

TARGET=Path(__file__).resolve().parents[1]/'examples/multi-entity-multi-period-correction'


class AttackResult(unittest.TestResult):
    def __init__(self):super().__init__();self.outcomes=[]
    def addSuccess(self,test):super().addSuccess(test);self.outcomes.append(dict(test=test.id(),status='PASS'))
    def addFailure(self,test,err):super().addFailure(test,err);self.outcomes.append(dict(test=test.id(),status='FAIL'))
    def addError(self,test,err):super().addError(test,err);self.outcomes.append(dict(test=test.id(),status='ERROR'))


def main():
    generated=artifacts()
    result=AttackResult()
    unittest.defaultTestLoader.loadTestsFromNames(['orchestration.tests.test_stage4_correction','orchestration.tests.test_stage4_correction_independent']).run(result)
    if not result.wasSuccessful():raise ValueError('Correction-path regression failed; do not generate an acceptance claim')
    generated['correction-attacks.json']=dict(distinct_methods=result.testsRun,results=sorted(result.outcomes,key=lambda r:r['test']),unresolved_correction_path_findings=0,scope='Focused Outcome B review; not full Stage4 acceptance')
    generated['correction-acceptance-state.json']=dict(outcome='B',stage4='INCOMPLETE',iqa03='OPEN',case_complete=False,case_closed=False,material_residual='-2.00 EUR million',final_release_validation=False,ready_for_review=False)
    TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in generated.items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')


if __name__=='__main__':main()

"""Governed native closing correction and honest comparative refusal artifacts."""
import json
import unittest
from pathlib import Path
from orchestration.tests import stage4_closing_fixtures as closing,stage4_closing_population as whole
from orchestration.tests.generate_stage4_correction_examples import AttackResult

TARGET=Path(__file__).resolve().parents[1]/'examples/multi-entity-multi-period-closing'


def main():
    result=AttackResult()
    unittest.defaultTestLoader.loadTestsFromNames(['orchestration.tests.test_stage4_closing','orchestration.tests.test_stage4_closing_independent']).run(result)
    if not result.wasSuccessful():raise ValueError('Closing correction/current population regressions failed')
    generated={'closing-path.json':closing.artifacts(),'closing-population.json':whole.artifacts(),
        'closing-attacks.json':dict(distinct_methods=result.testsRun,results=sorted(result.outcomes,key=lambda x:x['test']),unresolved_substantive_closing_path_findings=0),
        'closing-acceptance-state.json':dict(stage4='INCOMPLETE',iqa03='CURRENT_POPULATION_NATIVE_ACCOUNTING_PROVED; END_TO_END_ACCEPTANCE_OPEN',native_closing_residual='0.00 EUR million',group_current_accounting='COMPLETE',reporting='REFUSED_COMPARATIVE_EVIDENCE',case_complete=False,case_closed=False,exact_once_release='REFUSED_STALE_DOWNSTREAM',ready_for_review=False,final_release_validation=False)}
    TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in generated.items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')


if __name__=='__main__':main()

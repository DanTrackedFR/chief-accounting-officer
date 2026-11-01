"""Independent adversarial checks of complete Prepared release population.

Synthetic receipts exercise the population validator without rerunning accounting
or changing any historical release evidence.
"""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('independent_prepared_release_verifier',
                                            ROOT/'skills/prepared-accounting/verify_release.py')
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)

EXPECTED_SUITES = [
    ('orchestration/tests', 'test_*.py'),
    ('skills/tests', 'test_*.py'),
    ('skills/lease-accounting/tests', 'test_*.py'),
    ('tests', 'test_*.py'),
    ('knowledge/income-taxes', 'test*.py'),
    ('knowledge/agriculture', 'test*.py'),
    ('knowledge/insurance-contracts', 'test*.py'),
    ('knowledge/derivatives-hedge', 'test*.py'),
    ('knowledge/derivatives-hedge', 'independent_review_tests.py'),
    ('knowledge/inventory-cost', 'test*.py'),
    ('local_cao/tests', 'test_*.py'),
    ('knowledge/borrowing-costs', 'test*.py'),
    ('hosted_cao/tests', 'test_*.py'),
    ('intelligence/tests', 'test_*.py'),
    ('build4/tests', 'test_*.py'),
    ('knowledge/government-grants', 'test_*.py'),
    ('knowledge/investment-property', 'test_*.py'),
]
EXPECTED_VALIDATORS = [
    'knowledge/income-taxes/validate_supplement.py',
    'knowledge/agriculture/validate_supplement.py',
    'knowledge/insurance-contracts/validate_supplement.py',
    'knowledge/derivatives-hedge/validate_supplement.py',
    'knowledge/inventory-cost/validate_supplement.py',
    'knowledge/standards-evidence/validate_claims.py',
    'knowledge/standards-evidence/validate_approvals.py',
    'knowledge/borrowing-costs/validate_supplement.py',
    'knowledge/government-grants/validate_supplement.py',
    'knowledge/investment-property/validate_supplement.py',
]


def receipt():
    rows = []
    for index, (suite, pattern) in enumerate(EXPECTED_SUITES):
        ids = [suite+'::synthetic_'+str(index)+'.test_checked']
        rows.append(dict(suite=suite, pattern=pattern, distinct_ids=ids, tests=1,
                         errors=0, failures=0, skipped=0, passed=True, exit_code=0))
    rows[0]['exact_discovery_population'] = True
    rows[0]['module_results'] = [dict(suite=rows[0]['suite'], pattern='test_synthetic.py',
                                    distinct_ids=list(rows[0]['distinct_ids']), tests=1,
                                    errors=0, failures=0, skipped=0, passed=True, exit_code=0)]
    commands = [[sys.executable, '-m', 'build4.run_release', 'suite', suite, pattern, str(index)]
                for index, (suite, pattern) in enumerate(EXPECTED_SUITES)]
    commands += [[sys.executable, name] for name in EXPECTED_VALIDATORS]
    commands += [['git', 'diff', '--check']]
    logs = [dict(command=command, exit_code=0, path='synthetic/log-'+str(index)+'.log', sha256='0'*64)
            for index, command in enumerate(commands)]
    return dict(complete=True, source_unchanged=True, executed_distinct_tests=len(rows),
                suite_results=rows, logs=logs)


class IndependentPreparedReleaseQA(unittest.TestCase):
    def validate(self, value):
        return VERIFIER.validate_population(value)

    def refuses(self, value):
        with self.assertRaises((AssertionError, ValueError, KeyError)):
            self.validate(value)

    def test_exact_independently_pinned_release_population(self):
        self.assertEqual(list(VERIFIER.SUPPORTED_SUITES), EXPECTED_SUITES)
        self.assertEqual(list(VERIFIER.VALIDATOR_COMMANDS), EXPECTED_VALIDATORS)
        self.validate(receipt())

    def test_narrower_specialist_glob_is_not_full_regression(self):
        value = receipt()
        value['suite_results'][1]['pattern'] = 'test_prepared_accounting_qa.py'
        value['logs'][1]['command'][-2] = 'test_prepared_accounting_qa.py'
        self.refuses(value)

    def test_suite_replacement_omission_and_order_refused(self):
        for mutation in ('replace', 'omit', 'reorder'):
            with self.subTest(mutation=mutation):
                value = receipt()
                if mutation == 'replace':
                    value['suite_results'][1]['suite'] = 'hosted_cao/tests'
                elif mutation == 'omit':
                    value['suite_results'].pop(1)
                else:
                    value['suite_results'][1:3] = reversed(value['suite_results'][1:3])
                self.refuses(value)

    def test_test_count_and_global_distinct_count_are_exact(self):
        for mutation in ('row_count', 'global_count', 'duplicate'):
            with self.subTest(mutation=mutation):
                value = receipt()
                if mutation == 'row_count':
                    value['suite_results'][1]['tests'] = 2
                elif mutation == 'global_count':
                    value['executed_distinct_tests'] += 1
                else:
                    value['suite_results'][1]['distinct_ids'] = list(value['suite_results'][0]['distinct_ids'])
                self.refuses(value)

    def test_no_suite_skip_failure_error_or_nonzero_exit_can_pass(self):
        for field, invalid in [('skipped', 1), ('failures', 1), ('errors', 1),
                               ('passed', False), ('exit_code', 1)]:
            with self.subTest(field=field):
                value = receipt()
                value['suite_results'][1][field] = invalid
                self.refuses(value)

    def test_suite_log_command_must_match_exact_discovery_invocation(self):
        for index in (0, 1, 16):
            value = receipt()
            value['logs'][index]['command'][-2] = 'test_narrower.py'
            self.refuses(value)

    def test_missing_replaced_or_reordered_validator_refused(self):
        for mutation in ('missing', 'replace', 'reorder'):
            with self.subTest(mutation=mutation):
                value = receipt()
                if mutation == 'missing':
                    value['logs'].pop(17)
                elif mutation == 'replace':
                    value['logs'][17]['command'] = [sys.executable, '-c', 'pass']
                else:
                    value['logs'][17:19] = reversed(value['logs'][17:19])
                self.refuses(value)

    def test_untrusted_python_command_and_nonzero_log_exit_refused(self):
        for mutation in ('executable', 'exit'):
            value = receipt()
            if mutation == 'executable':
                value['logs'][0]['command'][0] = '/usr/bin/echo'
            else:
                value['logs'][17]['exit_code'] = 1
            self.refuses(value)

    def test_interpreter_location_can_change_without_changing_command(self):
        value = receipt()
        for row in value['logs'][:-1]:
            row['command'][0] = '/different/host/bin/python3'
        self.validate(value)

    def test_diff_gate_is_exact_and_cannot_be_removed(self):
        value = receipt()
        value['logs'][-1]['command'] = ['git', 'status']
        self.refuses(value)
        value = receipt()
        value['logs'].pop()
        self.refuses(value)

    def test_orchestration_shard_union_and_exact_population_are_required(self):
        for mutation in ('missing_shards', 'wrong_union', 'duplicate', 'not_exact', 'shard_count'):
            with self.subTest(mutation=mutation):
                value = receipt()
                row = value['suite_results'][0]
                if mutation == 'missing_shards':
                    row['module_results'] = []
                elif mutation == 'wrong_union':
                    row['module_results'][0]['distinct_ids'] = ['unexecuted::synthetic.test']
                elif mutation == 'duplicate':
                    row['module_results'].append(copy.deepcopy(row['module_results'][0]))
                elif mutation == 'not_exact':
                    row['exact_discovery_population'] = False
                else:
                    row['module_results'][0]['tests'] = 2
                self.refuses(value)

    def test_orchestration_shard_skip_failure_error_and_exit_refused(self):
        for field, invalid in [('skipped', 1), ('failures', 1), ('errors', 1),
                               ('passed', False), ('exit_code', 1)]:
            with self.subTest(field=field):
                value = receipt()
                value['suite_results'][0]['module_results'][0][field] = invalid
                self.refuses(value)


if __name__ == '__main__':
    unittest.main()

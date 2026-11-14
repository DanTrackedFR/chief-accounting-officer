"""Executed unittest outcomes, including setup failures and unexecuted methods.

Discovered/scheduled IDs are a plan. Only observed TestResult callbacks establish
execution; a class setup error is a suite error, never a passed method.
"""
import unittest

KINDS = ('passed', 'failed', 'errored', 'skipped', 'unexecuted')


def require(value, message):
    if not value:
        raise ValueError(message)


class ObservedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = set()
        self.outcomes = {k: set() for k in KINDS}
        self.suite_errors = []

    def startTest(self, test):
        self.started.add(test.id())
        super().startTest(test)

    def addSuccess(self, test):
        self.outcomes['passed'].add(test.id())
        super().addSuccess(test)

    def addFailure(self, test, err):
        self.outcomes['failed'].add(test.id())
        super().addFailure(test, err)

    def addError(self, test, err):
        if test.id() in self.started:
            self.outcomes['errored'].add(test.id())
        else:
            self.suite_errors.append(test.id())
        super().addError(test, err)

    def addSkip(self, test, reason):
        if test.id() in self.started:
            self.outcomes['skipped'].add(test.id())
        else:
            self.suite_errors.append(test.id()+': '+reason)
        super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            kind = 'failed' if issubclass(err[0], test.failureException) else 'errored'
            self.outcomes[kind].add(test.id())
        super().addSubTest(test, subtest, err)

    def addExpectedFailure(self, test, err):
        self.outcomes['skipped'].add(test.id())
        super().addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self.outcomes['failed'].add(test.id())
        super().addUnexpectedSuccess(test)


def observations(result, directory, scheduled):
    groups = {k: {directory+'::'+i for i in result.outcomes[k]} for k in KINDS}
    # An errored teardown can follow an assertion failure; each method gets one
    # terminal outcome, with error taking priority over failure and success.
    groups['failed'] -= groups['errored']
    groups['passed'] -= groups['errored'] | groups['failed'] | groups['skipped']
    terminal = set().union(*(groups[k] for k in KINDS if k != 'unexecuted'))
    groups['unexecuted'] = set(scheduled) - terminal
    executed = groups['passed'] | groups['failed'] | groups['errored']
    return dict(outcome_schema_version=1, discovered_ids=list(scheduled), scheduled_ids=list(scheduled),
                executed_ids=sorted(executed), suite_errors=result.suite_errors,
                **{k+'_ids': sorted(v) for k,v in groups.items()})


def validate_outcomes(row, successful=True):
    require(row.get('outcome_schema_version') == 1, 'Missing observed outcome schema')
    def identities(key):
        ids = row.get(key)
        require(isinstance(ids,list) and all(isinstance(i,str) for i in ids) and ids == sorted(set(ids)), 'Invalid/duplicate '+key)
        return set(ids)
    discovered, scheduled = identities('discovered_ids'), identities('scheduled_ids')
    require(discovered == scheduled == identities('distinct_ids'), 'Scheduled/discovered population differs')
    groups = {k: identities(k+'_ids') for k in KINDS}
    require(sum(map(len,groups.values())) == len(set().union(*groups.values())) and
            set().union(*groups.values()) == scheduled, 'Truncated or overlapping outcomes')
    executed = identities('executed_ids')
    require(executed == groups['passed'] | groups['failed'] | groups['errored'], 'Scheduled-only methods counted as executed')
    require(type(row.get('tests')) is int and row['tests'] == len(executed) + len(groups['skipped']), 'Observed test count differs')
    require(isinstance(row.get('suite_errors'),list), 'Missing suite setup/teardown outcomes')
    require(row['skipped'] == len(groups['skipped']) and row['failures'] >= len(groups['failed']) and
            row['errors'] >= len(groups['errored'])+len(row['suite_errors']), 'Outcome counters differ')
    if successful:
        require(not row['suite_errors'] and not any(groups[k] for k in ('failed','errored','skipped','unexecuted')),
                'Unexecuted or unsuccessful required methods')
        require(row['passed'] is True and row.get('exit_code',0) == 0 and not any(row[k] for k in ('errors','failures','skipped')),
                'Unsuccessful observed suite')
    return executed


def aggregate(records):
    value = dict(outcome_schema_version=1, suite_errors=[])
    for key in ('distinct_ids','discovered_ids','scheduled_ids','executed_ids',*(k+'_ids' for k in KINDS)):
        ids = [i for row in records for i in row[key]]
        require(len(ids) == len(set(ids)), 'Duplicate aggregate '+key)
        value[key] = sorted(ids)
    value['suite_errors'] = [e for row in records for e in row['suite_errors']]
    return value

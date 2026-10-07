"""Bounded Stage1 restart proof using accepted native runtime contracts."""
from orchestration.tests.stage2_fixtures import build, initial, correction
from orchestration.runtime import CAO

COMPANY = 'company:durable-controlled-group'
CONTEXT = [dict(id='context:group-profile', attribute='reporting_currency', value='EUR', status='DOCUMENTED',
    scope=dict(entities=['GROUP-EUR']), effective_from='2026-01-01', provenance=['synthetic governed company profile'])]


def proof(partial=True):
    f = initial(build())
    # Runtime already preserves the supplied Company Context as governed records;
    # the store namespace uses a caller-supplied identity, not its display label.
    f['coordinator'].context['company_id'] = COMPANY
    f['coordinator'].context['company_context'] = CONTEXT
    if partial: correction(f)
    return f


def journal_population(case):
    e = case.governance
    return [(key, v.payload().get('journal_entry_implications', []))
        for key, v in sorted(e.versions.versions.items()) if e.versions.states[key] == 'CURRENT'
        and v.payload().get('journal_entry_implications')]

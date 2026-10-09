"""One company Group close, native accounting and context-only memory seams."""
import copy
from unittest.mock import patch
from orchestration.tests import stage4_temporal_fixtures as t, stage4_fixtures as prior
from orchestration.tests.persistence_stage2_fixtures import attach as stage2_attach, correction_intent, rework_intent, journal_intent, reopening
from orchestration.persistence import snapshot
from orchestration.persistence.evidence import retain
from orchestration.persistence.memory import applicability
from orchestration.runtime import CAO

COMPANY='company:full-durable-cao'
CONTEXT=[dict(id='company:reporting-profile',attribute='reporting_currency',value='EUR',status='DOCUMENTED',scope=dict(entities=['GROUP-EUR']),effective_from='2026-01-01',provenance=['Controlled synthetic Group finance profile'])]
LEARNED=dict(value='2026-11-02',precision='exact')
UNKNOWN=dict(value=None,precision='unknown')
OBJECTIVE=prior.OBJECTIVE
REUSE_OBJECTIVE=OBJECTIVE+' Use the documented company finance-system context for a separate reporting review.'


def attach(case):
    with patch.object(prior,'OBJECTIVE',case.objective):
        return stage2_attach(case)


def initial(objective=OBJECTIVE,systems=None,memory=None):
    with patch.object(prior,'OBJECTIVE',objective):
        f=prior.intake_initial(t.build,t.source,company_system=systems,memory=memory)
    f['session'].context.update(company_id=COMPANY,company_context=copy.deepcopy(CONTEXT))
    return f


def finish(f):
    with patch.object(prior,'OBJECTIVE',f['case'].objective):
        f,record=t.finish(f)
    for row in f.get('replacement_intakes',[]):retain(f['session'],row['prepared'],row['reviewed_pack'])
    assert f['case'].status=='CLOSED' and CAO().public(f['case'])['status']=='complete'
    return f,record


def capture(store,case,*,subject='finance',support=True,supersedes=()):
    m=store.memory();e=case.governance
    index=next(i for i,c in enumerate(case.memory_candidates) if c['attribute']=='systems' and c.get('semantic_status')=='EXTRACTED')
    versions=[v.version_id for v in e.versions.versions.values() if v.case_id==case.id and e.versions.states[v.version_id]=='CURRENT'] if support else []
    return m.capture(COMPANY,case.id,case.id,index,category='systems_data',subject=subject,assertion='EXTRACTED',bundle_ids=sorted(e.evidence_bundles),result_versions=sorted(versions),dimensions=applicability(case,case.scope_id,[case.period_id]),effective_from=dict(value='2026-10-01',precision='exact'),effective_to=dict(value='2026-10-31',precision='exact'),learned_at=LEARNED,expected_revision=m.audit(COMPANY)['revision'],material=True,reusable=True,supersedes=list(supersedes),decision=dict(previous_position=None,new_position=case.memory_candidates[index]['value'],reason='Documented recurring company finance-system context; no accounting measurement authority',decision_date=UNKNOWN,status='proposed',implications=['Reduce repeated system questions']))


def governance(record,target='DOCUMENTED'):
    return dict(intent='EXPLICIT_MEMORY_TRANSITION',prior_status=record['status'],target_status=target,record_id=record['record_id'],applicability=record['applicability'],authority='TRUSTED_CALLER_ASSERTION',evidence_kind='SYNTHETIC',bundle_ids=record['source']['bundle_ids'],reason='Explicit bounded synthetic review of sealed company-system evidence',decision_date=UNKNOWN,approval_date=UNKNOWN,authenticated=False)


def memory_request(memory,root):
    return dict(memory=memory,company_id=COMPANY,qualification_root=root,qualification_case=root,subjects=[('finance','systems')])


def current_results(case):
    e=case.governance;nodes={n.logical_id:n for n in e.graph.nodes.values()}
    return {label: e.versions.current(nodes[label].id).payload() for label in ('fx-ENTITY-UK','match-fx-current','elimination','adjacent-closing','current-opening','prior-year-comparative','reporting','analytics')}


def native_invariants(case):
    from orchestration.tests import stage4_closing_population as whole
    f=attach(case);r=current_results(case)
    assert case.status=='CLOSED' and CAO().public(case)['status']=='complete'
    from decimal import Decimal
    assert Decimal(str(r['reporting']['calculations']['current']['cash']))==490
    assert Decimal(str(r['reporting']['calculations']['current']['profit']))==3
    inventory=whole.exact_once(f)
    assert len(inventory['selected'])==8
    return dict(results=r,journals=inventory,public=CAO().public(case))

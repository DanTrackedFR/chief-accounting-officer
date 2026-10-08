"""Native accepted temporal accounting, with separately retained reviewed evidence."""
import copy
from orchestration.tests import stage4_temporal_fixtures as t, stage4_fixtures as prior, stage4_closing_population as whole
from orchestration.tests.persistence_fixtures import COMPANY, CONTEXT
from orchestration.persistence.evidence import retain
from orchestration.runtime import CAO


def baseline():
    f, record = t.run()
    for row in f['replacement_intakes']: retain(f['case'].governance, row['prepared'], row['reviewed_pack'])
    f['session'].context.update(company_id=COMPANY, company_context=copy.deepcopy(CONTEXT))
    return f


def attach(case):
    e=case.governance
    # Reuse accepted fixture context only to prepare separately supplied native
    # evidence. The live restored session is always the committing authority.
    f=t.build();f['case']=case;f['session']=e;f['basis'].session=e
    f['nodes']={n.logical_id:n for n in e.graph.nodes.values()}
    f['containers']={k:e.cases.get(c.id) for k,c in f['containers'].items()}
    return f


def correction_intent(case):
    f=attach(case);n=f['nodes']['adjacent-closing']
    source=prior.qualified_replacement(f,n.id,t.stock_source(f,'adjacent-closing'))
    return dict(kind='CORRECT',node_id=n.id,source=source,reason='Separately reviewed replacement of supplied closing-stock evidence; preserve native measured amounts')


def rework_intent(case, plan):
    f=attach(case);sources=t.reviewed_rework(f,plan)
    # Preview qualification never grants the actual session evidence implicitly.
    for row in f.get('replacement_intakes',[]):retain(case.governance,row['prepared'],row['reviewed_pack'])
    return dict(kind='REWORK',plan=plan,reviewed_sources=sources)


def journal_intent(case):
    f=attach(case);inventory=whole.exact_once(f)
    e=case.governance
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    return dict(kind='SELECT_JOURNALS',context=context,events=inventory['events'])


def reopening(case,period_id):
    e=case.governance;nodes=[n for n in e.graph.nodes.values() if n.period_id==period_id]
    return dict(kind='REOPEN',period_id=period_id,reason='Separately reviewed durable correction authorization',approval=dict(status='APPROVED',evidence=['synthetic independent review of exact selected Case/node correction work'],convention='SYNTHETIC_GOVERNED'),case_ids=sorted({n.case_id for n in nodes}),node_ids=sorted(n.id for n in nodes))

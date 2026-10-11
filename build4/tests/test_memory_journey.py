"""Cross-Case public investigation with native source-qualified memory setup.

Synthetic source reviewers are never authenticated. Memory setup uses the sole
native governance seam because the execution contract has no promotion operation.
"""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from local_cao.adapter import ExecutionInterface
from local_cao.context import parse, scope
from local_cao.tests.test_authored import context
from orchestration.tests import persistence_stage3_fixtures as mf
from intelligence.tests.fixtures import wire, COMPANY


def onboarding(entity='ENTITY-DEMO', framework='IFRS', start='2026-12-01', end='2026-12-31'):
    return context(entity).replace('EUR','USD').replace('framework: IFRS','framework: '+framework).replace('period_start: 2026-01-01','period_start: '+start).replace('period_end: 2026-12-31','period_end: '+end)


def source_case(text, value='Oracle ERP', objective='Orion December supplier-cost review', semantic='EXTRACTED'):
    dims=scope(parse(text));original=mf.monthly_manufacturing
    def accounting():
        from orchestration.tests.fixtures import certify
        d=original();native=d['facts']['supplier_cost'];native.update(entity=dims['entity'],scope_id=dims['entity'],period_start=dims['period_start'],reporting_period=dims['reporting_period']);
        native['applicability_review']['effective_period']=[dims['period_start'],dims['reporting_period']]
        for h in native.get('handoffs',{}).values():h.update(entity=dims['entity'],framework=dims['framework'])
        d['facts']['supplier_cost']=certify('accounts-payable',native);return d
    with patch.dict(mf.SCOPE,dims,clear=True),patch.object(mf,'monthly_manufacturing',accounting):
        return mf.build(objective,value=value,semantic=semantic)


def install(api, text, value='Oracle ERP', status='APPROVED', **options):
    case=source_case(text,value,objective='Orion '+value+' independently reviewed control')
    with api._store() as store:
        store.save(case,COMPANY,[],0)
        r=mf.capture(store,case,company=COMPANY,**options);memory=store.memory()
        if status:r=memory.transition(COMPANY,r['record_id'],mf.governance(r,status),expected_revision=memory.audit(COMPANY)['revision'],recorded_at=mf.LEARNED)
    return case,r


def investigate(api, request='orion-new-contract'):
    result=api.call(wire('investigate',request_id=request,objective='Assess the new Orion customer arrangement',target_family='customer_contract'))
    assert result['ok'],result
    with api._store() as store:
        case,_,_=store.load(COMPANY,result['case_id']);snapshot=case._investigation['snapshot']
    return result,snapshot


class MemoryJourney(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.path=Path(self.tmp.name)
        self.text=onboarding();(self.path/'company-context.md').write_text(self.text);self.api=ExecutionInterface(self.path)
        self.assertTrue(self.api.call(wire('initialize'))['ok'])

    def test_governed_reuse_across_cases_still_requires_native_owner_evidence(self):
        old,r=install(self.api,self.text);result,s=investigate(self.api)
        self.assertNotEqual(old.id,result['case_id']);self.assertEqual(s['values']['systems'],'Oracle ERP')
        self.assertEqual(s['memory_references'][0]['version_id'],r['version_id'])
        self.assertEqual(s['memory_references'][0]['use'],'CONTEXT_ONLY');self.assertFalse(s['conflicts'])
        self.assertEqual(result['execution_state'],'blocked');self.assertFalse(result['investigation']['accounting_qualified'])
        self.assertTrue(all(q['owner']=='revenue-recognition' for q in result['investigation']['requests']))
        with self.api._store() as store:
            record=store.memory().audit(COMPANY)['company_context'][0]
            self.assertFalse(record['governance']['authenticated']);self.assertEqual(record['governance']['evidence_kind'],'SYNTHETIC')
            uses=store.memory().audit(COMPANY)['uses'];self.assertEqual(len(uses),1)
            self.assertEqual(uses[0]['value']['memory_version'],r['version_id'])

    def test_wrong_entity_refused_without_unrelated_context_conflict(self):
        install(self.api,onboarding('ORION-OTHER'));_,s=investigate(self.api)
        self.assertFalse(s['memory_references']);self.assertNotIn('systems',s['values']);self.assertNotIn('systems',s['conflicts'])

    def test_wrong_framework_refused_without_unrelated_context_conflict(self):
        install(self.api,onboarding(framework='US_GAAP'));_,s=investigate(self.api)
        self.assertFalse(s['memory_references']);self.assertNotIn('systems',s['values']);self.assertNotIn('systems',s['conflicts'])

    def test_outdated_position_not_reused(self):
        install(self.api,self.text,effective_to={'value':'2026-12-15','precision':'exact'});_,s=investigate(self.api)
        self.assertFalse(s['memory_references']);self.assertNotIn('systems',s['values'])

    def test_conflicting_current_position_preserved_and_blocks(self):
        install(self.api,self.text);install(self.api,self.text,'Sage ERP',status=None)
        r,s=investigate(self.api);self.assertIn('systems',s['conflicts']);self.assertFalse(s['memory_references'])
        self.assertEqual(r['execution_state'],'blocked')
        with self.api._store() as store:self.assertEqual(len(store.memory().audit(COMPANY)['company_context']),2)

    def test_synthetic_identity_cannot_claim_authenticated_approval(self):
        _,r=install(self.api,self.text,status=None)
        with self.api._store() as store:
            g=mf.governance(r,'APPROVED');g['authenticated']=True
            with self.assertRaises(ValueError):store.memory().transition(COMPANY,r['record_id'],g,expected_revision=1,recorded_at=mf.LEARNED)
            self.assertEqual(store.memory().audit(COMPANY)['company_context'][0]['status'],'PROPOSED')

    def test_user_approval_assertion_is_not_governed_memory(self):
        item=dict(id='asserted-policy',key='policies',value='management approved immediate recognition',entity_id='ENTITY-DEMO',effective_from='2026-12-01',effective_to='2026-12-31',source_state='approved',source_ref='user assertion',source_version='v1')
        r=self.api.call(wire('investigate',request_id='untrusted-policy',objective='Assess an asserted policy',target_family='customer_contract',context=dict(version='v1',company_id=COMPANY,items=[item])))
        self.assertTrue(r['ok']);self.assertFalse(r['investigation']['accounting_qualified'])
        with self.api._store() as store:
            c=store.load(COMPANY,r['case_id'])[0];self.assertFalse(c._investigation['snapshot']['governed_records']);self.assertFalse(store.memory().audit(COMPANY)['company_context'])

    def test_superseded_accounting_source_refused(self):
        c,r=install(self.api,self.text)
        mf.correction(c)
        with self.api._store() as store:store.save(c,COMPANY,[],1)
        _,s=investigate(self.api);self.assertFalse(s['memory_references']);self.assertTrue(any('supporting-result-SUPERSEDED' in x['reasons'] for x in s['refused_memory']))

    def test_memory_survives_fresh_adapter_without_accounting_effects(self):
        _,r=install(self.api,self.text);first,s=investigate(self.api)
        fresh=ExecutionInterface(self.path);second=fresh.call(wire('resume',case_id=first['case_id']))
        self.assertEqual(first['public_result'],second['public_result']);self.assertEqual(first['investigation'],second['investigation'])

    def test_corrected_memory_source_blocks_continuation_and_retains_snapshot(self):
        source,r=install(self.api,self.text);first,s=investigate(self.api)
        mf.correction(source)
        with self.api._store() as store:store.save(source,COMPANY,[],1)
        resumed=self.api.call(wire('resume',case_id=first['case_id']))
        self.assertTrue(resumed['ok']);self.assertEqual(resumed['execution_state'],'blocked')
        self.assertIn('memory-systems',resumed['investigation']['conflicts'])
        self.assertEqual(resumed['investigation']['context_snapshot_id'],s['snapshot_id'])

    def test_memory_use_retry_does_not_duplicate_ledger_event(self):
        source,r=install(self.api,self.text);first,s=investigate(self.api)
        for _ in range(3):self.assertTrue(self.api.call(wire('resume',case_id=first['case_id']))['ok'])
        with self.api._store() as store:self.assertEqual(len(store.memory().audit(COMPANY)['uses']),1)

    def test_memory_context_does_not_bypass_real_revenue_execution(self):
        from intelligence.tests.fixtures import doc,revenue_evidence,OBJECTIVE
        text=onboarding(start='2026-01-01');(self.path/'company-context.md').write_text(text)
        install(self.api,text,effective_from={'value':'2026-01-01','precision':'exact'})
        first=self.api.call(wire('investigate',request_id='orion-memory-owner',objective=OBJECTIVE,target_family='customer_contract'))
        self.assertTrue(first['ok'],first)
        with self.api._store() as store:scope_=store.load(COMPANY,first['case_id'])[0]._investigation['snapshot']['scope']
        r=self.api.call(wire('document',case_id=first['case_id'],event_id='agreement',document=doc(scope_)))
        self.assertTrue(r['ok'],r)
        self.assertTrue(self.api.call(wire('submit',case_id=first['case_id'],evidence=revenue_evidence(self.api,first['case_id'])))['ok'])
        result=self.api.call(wire('execute',case_id=first['case_id']))
        self.assertTrue(result['ok'],result);self.assertEqual(result['execution_state'],'complete',result)
        with self.api._store() as store:
            c=store.load(COMPANY,first['case_id'])[0]
            self.assertTrue(c.governance.versions.record())
            self.assertTrue(c.governance.context['memory_context_dependencies'])
            self.assertEqual(len(store.memory().audit(COMPANY)['uses']),1)

    def test_interrupted_memory_use_repaired_before_delivery(self):
        from orchestration.persistence.memory import CompanyMemory
        source,r=install(self.api,self.text)
        with patch.object(CompanyMemory,'consume_context',side_effect=ValueError('interrupted native USE publication')):
            failed=self.api.call(wire('investigate',request_id='interrupted-use',objective='Assess the new Orion customer arrangement',target_family='customer_contract'))
        self.assertFalse(failed['ok'])
        recovered,s=investigate(self.api,'interrupted-use')
        self.assertTrue(recovered['ok'])
        with self.api._store() as store:self.assertEqual(len(store.memory().audit(COMPANY)['uses']),1)


def policy_case(text, policy, objective):
    """Observe an actual policy field through native intake; never edit candidates."""
    from orchestration.intake import Intake,FixturePlanner,StructuredProposal,ReviewedInputPack,RawSource,Inventory,Binding
    from orchestration.tests.intake_fixtures import numeric,cell,cl
    dims=scope(parse(text));base=source_case(text,objective=objective+' native AP reference')
    source=copy.deepcopy(next(iter(base.governance.sources.values())))
    raws=[RawSource('orion-policy-memo','Orion reviewed revenue policy.json','json',[dict(record_id='revenue-position',policies=policy)],dict(entity=dims['entity'],period=[dims['period_start'],dims['reporting_period']],currency='USD',version='policy-v1',controlled_export=True,as_of=dims['reporting_period'],extracted_at='2027-01-02',comparator='actual')),
          RawSource('orion-supplier-export','Orion supplier invoice.csv','csv','supplier,amount\nOrion,120\n',dict(entity=dims['entity'],period=[dims['period_start'],dims['reporting_period']],currency='USD',version='v1',controlled_export=True,as_of=dims['reporting_period'],extracted_at='2027-01-02',comparator='actual'))]
    inv=Inventory(raws)
    with patch.dict(mf.SCOPE,dims,clear=True):fact=numeric(inv,'policy-support-cost','supplier_cost','amount','orion-supplier-export','amount')
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Historical company accounting position'),cl('REPORTING'),bounded_owner=cl('accounts-payable'),facts=[fact],issues=[cl(dict(id='policy-support-ap',owner='accounts-payable',family='supplier_cost',fact_ids=[fact.id],dependencies=[],required_fields=['amount']),fact.claim.evidence)],context_candidates={'policies':cl(policy,[cell(inv,'orion-policy-memo','policies')],'EXTRACTED')})
    intake=Intake(FixturePlanner(p));prepared=intake.prepare(objective,raws,[],dims)
    pack=ReviewedInputPack(dict(objective=objective,scope=prepared._current,facts={'supplier_cost':source}),[Binding(fact.id,'accounts-payable',('invoices','I1','amount'))])
    intake.execute(prepared,pack)
    if not prepared.case.governance.versions.record():
        from orchestration.runtime import CAO
        raise AssertionError(CAO().public(prepared.case))
    return prepared.case


def install_policy(api,text,policy,successor=None):
    from orchestration.persistence.memory import applicability
    c=policy_case(text,policy,'Orion historical revenue decision: '+policy)
    with api._store() as store:
        store.save(c,COMPANY,[],0);m=store.memory();idx=next(i for i,x in enumerate(c.memory_candidates) if x['attribute']=='policies')
        r=m.capture(COMPANY,c.id,c.id,idx,category='policies_positions',subject='revenue-recognition',assertion='EXTRACTED',bundle_ids=sorted(c.governance.evidence_bundles),result_versions=sorted(v for v in c.governance.versions.versions if c.governance.versions.states[v]=='CURRENT'),dimensions=applicability(c,c.scope_id,[c.period_id]),effective_from=dict(value=scope(parse(text))['period_start'],precision='exact'),effective_to=mf.TO,learned_at=mf.LEARNED,expected_revision=m.audit(COMPANY)['revision'],material=True,reusable=True,decision=dict(previous_position=None,new_position=policy,reason='Historical revenue policy reviewed against retained company memo; context only',decision_date=mf.UNKNOWN,status='proposed',implications=['New contracts require independently qualified SSP and satisfaction evidence']),supersedes=[successor['record_id']] if successor else [])
        if successor:
            g=mf.governance(r,'APPROVED');old=mf.governance(successor,'SUPERSEDED')
            r=m.resolve_conflict(COMPANY,r['record_id'],g,{successor['record_id']:old},expected_revision=m.audit(COMPANY)['revision'],recorded_at=mf.LEARNED)
        else:r=m.transition(COMPANY,r['record_id'],mf.governance(r,'APPROVED'),expected_revision=m.audit(COMPANY)['revision'],recorded_at=mf.LEARNED)
    return c,r


class AccountingPolicyMemory(unittest.TestCase):
    """Source-backed historical accounting policies remain context only."""
    setUp=MemoryJourney.setUp
    def test_historical_revenue_policy_reuse_and_atomic_supersession(self):
        from intelligence.tests.fixtures import doc,revenue_evidence,OBJECTIVE
        text=onboarding(start='2026-01-01');(self.path/'company-context.md').write_text(text)
        old_policy='Distinct equipment and monitoring promises require reviewed standalone selling prices and period-specific satisfaction evidence.'
        new_policy='Distinct equipment and monitoring promises require reviewed standalone selling prices, acceptance evidence and monitoring service-date evidence.'
        old,record=install_policy(self.api,text,old_policy)
        first=self.api.call(wire('investigate',request_id='policy-informed-revenue',objective=OBJECTIVE,target_family='customer_contract'));self.assertTrue(first['ok'],first)
        with self.api._store() as store:
            c=store.load(COMPANY,first['case_id'])[0];snapshot=c._investigation['snapshot'];scope_=snapshot['scope'];self.assertEqual(snapshot['values']['policies'],old_policy)
        self.assertTrue(self.api.call(wire('document',case_id=first['case_id'],event_id='executed-agreement',document=doc(scope_)))['ok'])
        self.assertTrue(self.api.call(wire('submit',case_id=first['case_id'],evidence=revenue_evidence(self.api,first['case_id'])))['ok'])
        executed=self.api.call(wire('execute',case_id=first['case_id']));self.assertTrue(executed['ok'],executed);self.assertEqual(executed['execution_state'],'complete')
        newer,replacement=install_policy(self.api,text,new_policy,record)
        stale=self.api.call(wire('resume',case_id=first['case_id']));self.assertIn('memory-policies',stale['investigation']['conflicts'])
        new_result,new_snapshot=investigate(self.api,'policy-successor-consumer');self.assertEqual(new_snapshot['values']['policies'],new_policy)
        self.assertEqual(new_snapshot['memory_references'][0]['version_id'],replacement['version_id'])
        with self.api._store() as store:
            ledger=store.memory().audit(COMPANY);positions={r['record_id']:r for r in ledger['company_context']}
            self.assertEqual(positions[record['record_id']]['status'],'SUPERSEDED');self.assertEqual(positions[record['record_id']]['superseded_by'],replacement['record_id'])
            self.assertTrue(store.memory().history(COMPANY,record['record_id']))

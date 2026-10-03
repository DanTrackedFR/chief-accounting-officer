"""Governed management batch scope, lifecycle, source and public regression."""
import copy,json,unittest
from unittest.mock import patch
from pathlib import Path
from governance_cases import *
from production import assess_case,to_public,ROOT,serializable
from interfaces.public_output import ROUTES

class GovernanceTests(unittest.TestCase):
    def result(self,p,c,release=False):return assess_case(p,ready(p,c['framework'],c,release))
    def blocked(self,p,c,release=True):self.assertEqual(self.result(p,c,release)['status'],'blocked')
    def test_four_framework_positive_no_journals(self):
        for p in BATCH:
            for fw in FRAMEWORKS:
                r=assess_case(p,ready(p,fw));self.assertEqual(r['status'],'complete');self.assertEqual(r['journal_entry_implications'],[])
                for route in ROUTES:self.assertTrue(to_public(r,route=route))
    def test_docs_only_no_fabricated_claims(self):
        c=ready(BATCH[0]);r=assess_case(BATCH[0],c)
        self.assertEqual(r['evidence'],[]);self.assertEqual(to_public(r)['citations'],[])
        for p in BATCH:
            r=assess_case(p,ready(p));self.assertEqual(r['evidence'],[])
    def test_missing_stale_case_certification(self):
        for p in BATCH:
            c=ready(p);c.pop('reviewer_signoff');self.assertEqual(assess_case(p,c)['status'],'partial')
            c=ready(p);c['reviewer_signoff']['case_fingerprint']='old';self.assertEqual(assess_case(p,c)['status'],'partial')
            c=ready(p);c['reviewer_signoff']['reviewer']=c['preparer'];self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_stale_implementation(self):
        original=Path.read_bytes
        for p in BATCH:
            c=ready(p)
            def changed(path):return original(path)+(b'\nchanged' if path.name=='governance_accounting.py' else b'')
            with patch.object(Path,'read_bytes',changed):self.assertIn(assess_case(p,c)['status'],{'partial','blocked'})
    def test_stale_frozen_knowledge(self):
        original=Path.read_bytes
        for p in BATCH:
            c=ready(p);target=c['knowledge_review']['documents'][0]['path']
            def changed(path):return original(path)+(b'\nchanged' if str(path).endswith(target) else b'')
            with patch.object(Path,'read_bytes',changed):self.assertEqual(assess_case(p,c)['status'],'blocked')
    def test_malformed_source_populations(self):
        keys=dict(zip(BATCH,['readiness','requests','policies','requirements','accounts']))
        for p in BATCH:
            for bad in [None,{},'records',[None],[{}]]:
                c=case(p);c[keys[p]]=bad;self.blocked(p,c)
    def test_malformed_evidence_and_approvals(self):
        for p in BATCH:
            for mutation in ['missing','hash','snapshot','selfreview','futureapproval']:
                c=case(p)
                if mutation=='missing':c['document_inventory']=[]
                elif mutation=='hash':c['documents'][0]['content_hash']='old'
                elif mutation=='snapshot':c['documents'][0]['snapshot_version']='v0'
                elif mutation=='selfreview':c['documents'][0]['reviewer']=c['documents'][0]['owner']
                else:c['documents'][0]['approval_date']='2028-01-01'
                self.blocked(p,c)
    def test_forbidden_actions_and_claims(self):
        for p in BATCH:
            for action in ['post','submit','certify_compliance','forecast']:
                c=case(p);c['requested_action']=action;self.blocked(p,c)
            for flag in ['posting_requested','legal_certification','audit_opinion','regulatory_compliance','forecast_requested','authority_override']:
                c=case(p);c['governance_method'][flag]=True;self.blocked(p,c)
    def test_source_population_and_release_approvals(self):
        keys=dict(zip(BATCH,['readiness','requests','policies','requirements','accounts']))
        for p in BATCH:
            c=case(p);c[keys[p]][0]['id']='substituted';c['source_inventory'][0]='substituted';self.blocked(p,c)
            c=case(p);c['documents'][0]['parameters']='new source filter';self.blocked(p,c,False)
    def test_owner_import_contradictions_and_posting(self):
        for p in BATCH[2:4]:
            for mutation in ['entity','jurisdiction','period','result','duplicate','posting','stale']:
                c=case(p);imp=c['imports'][0]
                if mutation=='entity':imp['case']['entity']='Other'
                elif mutation=='jurisdiction':imp['case']['jurisdiction']='Other'
                elif mutation=='period':imp['case']['period_start']='2025-01-01'
                elif mutation=='result':imp['result']['calculations']['current']['profit']='201'
                elif mutation=='duplicate':c['imports'].append(copy.deepcopy(imp));c['imports'][-1]['id']='second'
                elif mutation=='posting':imp['mode']='post'
                else:imp['case']['reviewer_signoff']['case_fingerprint']='stale'
                self.blocked(p,c)
    def test_unresolved_workpaper_is_partial(self):
        for p in [BATCH[0],BATCH[1],BATCH[3],BATCH[4]]:
            c=case(p)
            if p==BATCH[0]:
                c['readiness'][0]['state']='gap';d=c['documents'][0];d['content']['state']='gap';d['content_hash']=digest(d['content'])
            elif p==BATCH[1]:c['requests'][0]['state']='open'
            elif p==BATCH[3]:c['notes'][0]['review_notes_closed']=False
            else:
                c['reconciliations'][0]['completed_on']=None
                d=next(x for x in c['documents'] if x['id']=='reconciliation-source');d['content']['records'][0]['completed_on']=None;d['content_hash']=digest(d['content'])
            self.assertEqual(self.result(p,c,True)['status'],'partial')
    def test_privacy_all_routes_and_statuses(self):
        for p in BATCH:
            c=case(p);c['private_source_notes']='Source: ChatGPT training data; INTERNAL_SECRET_CANARY';c['private_reviewer']={'name':'INTERNAL_REVIEWER_CANARY'}
            for status in ['complete','partial','blocked']:
                signed=ready(p,c=c)
                if status=='partial':signed.pop('reviewer_signoff')
                if status=='blocked':signed['requested_action']='post'
                r=assess_case(p,signed);self.assertEqual(r['status'],status)
                for route in ROUTES:
                    public=json.dumps(to_public(r,route=route),default=serializable)
                    for secret in ['INTERNAL_SECRET_CANARY','INTERNAL_REVIEWER_CANARY','case_fingerprint','source_note','evidence_status','approval_track','content_hash']:
                        self.assertNotIn(secret,public)
    def test_saved_examples_current_and_generator_exact(self):
        from generate_governance_examples import artifacts
        for p in BATCH:
            for fw in FRAMEWORKS:
                for path,value in artifacts(p,fw).items():self.assertEqual(json.loads(Path(path).read_text()),json.loads(json.dumps(value,default=serializable)))
                c=json.loads((ROOT/'skills'/p/'examples'/f'{fw}.case.json').read_text());self.assertEqual(assess_case(p,c)['status'],'partial')
                r=assess_case(p,ready(p,fw,c));self.assertEqual(r['status'],'complete')
                bad=json.loads((ROOT/'skills'/p/'examples'/f'{fw}.blocked.case.json').read_text());r=assess_case(p,bad);self.assertEqual(r['status'],'blocked');self.assertEqual(r['calculations'],{});self.assertEqual(r['journal_entry_implications'],[])


class GovernanceLifecycleTests(unittest.TestCase):
    def test_actual_statement_dependency_and_audit_accounting_query(self):
        for fw in FRAMEWORKS:
            c=case(BATCH[0],fw);imp=owner(c)
            c['dependencies']=[row(c,'reporting-dependency',scope_memo='Actual reporting accounting evidence only',accountable_owner='Reporting controller',dependency_kind='accounting_owner',owner_import=imp['id'])];c['dependency_inventory']=['reporting-dependency'];c['readiness'][0]['dependency_ids']=['reporting-dependency']
            self.assertEqual(execute(BATCH[0],ready(BATCH[0],fw,c,True))['status'],'complete')
            c=case(BATCH[1],fw);imp=owner(c);c['queries']=[row(c,'accounting-query',question='Actual current profit accounting basis',accountable_owner='Reporting controller',response_memo='Consume actual completed reporting conclusion',impact_memo='Other support unchanged',kind='accounting',owner_import=imp['id'],accounting_conclusion=imp['result']['conclusion'],closed=True)];c['query_inventory']=['accounting-query']
            self.assertEqual(execute(BATCH[1],ready(BATCH[1],fw,c,True))['status'],'complete')
    def test_retained_two_version_policy_history(self):
        c=case(BATCH[2]);old=copy.deepcopy(c['history'][0]);old.update(effective_from='2025-01-01',effective_to='2025-12-31',memo_doc='retained-prior-memo')
        d=document(c,'retained-prior-memo',{'retained_published_policy':'Actual separately approved prior version; not overwritten'});old['body_hash']=d['content_hash']
        new=copy.deepcopy(c['history'][0]);new.update(id='policy-history-2',policy_version=2,supersedes=old['id'])
        c['history']=[old,new];c['history_inventory']=[old['id'],new['id']];c['policies'][0]['policy_version']=2;c['policy_source']['records'][0]['policy_version']=2
        r=execute(BATCH[2],ready(BATCH[2],c=c,release=True));self.assertEqual(r['status'],'complete');self.assertEqual(r['calculations']['retained_history_count'],2)
    def test_unavailable_auditor_sample_retained_partial(self):
        c=case(BATCH[1]);c['samples'][0].update(evidence_available=False,support_doc=None);c['documents']=[d for d in c['documents'] if d['id']!='selected-evidence'];c['document_inventory'].remove('selected-evidence')
        r=execute(BATCH[1],ready(BATCH[1],c=c,release=True));self.assertEqual(r['status'],'partial');self.assertEqual(r['calculations']['sample_count'],1)
    def test_zero_netting_preserves_gross_account_movements(self):
        c=case(BATCH[4]);r=copy.deepcopy(c['accounts'][0]);r.update(id='debt-metric',account='debt',amount='-120',management_amount='-120',current_source_doc='current-debt',prior_source_doc='prior-debt');c['accounts'].append(r);c['source_inventory'].append(r['id']);c['account_source']['records'].append(copy.deepcopy(r));c['account_source']['inventory'].append(r['id']);c['controls'].update(population_count=2,population_amount='240')
        for period,value,span in [('current','-120',['2026-01-01','2026-12-31']),('prior','-100',['2025-01-01','2025-12-31'])]:
            data=dict(period=span,account='debt',currency='USD',posted_only=True,signed_convention='Signed ledger debit positive',records=[dict(id='debt-line',account='debt',amount=value)],inventory=['debt-line'],statutory_amount=value,management_amount=value,gross_amount=value[1:]);document(c,period+'-debt',data)
        document(c,'debt-drivers',dict(account='debt',period=['2026-01-01','2026-12-31'],drivers=[dict(id='actual-financing',amount='-20')],driver_inventory=['actual-financing']))
        c['explanations'].append(row(c,'debt-driver',account='debt',interpretation_memo='Actual separately supported financing fact',driver_doc='debt-drivers',amount='-20'));c['explanation_inventory'].append('debt-driver')
        r=execute(BATCH[4],ready(BATCH[4],c=c,release=True));self.assertEqual(r['status'],'complete');self.assertEqual(r['calculations']['current_statutory'],0);self.assertEqual(r['calculations']['gross_movement'],40);self.assertEqual(r['calculations']['gross_statutory'],240)

if __name__ == "__main__": unittest.main()

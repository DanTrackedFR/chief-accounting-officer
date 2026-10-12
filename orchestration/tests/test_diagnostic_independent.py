"""Independent adversarial diagnostic review; no implementation mocks."""
import unittest
from orchestration.intent import Intent, interpret

class IndependentIntentQA(unittest.TestCase):
    def test_same_accounting_facts_distinct_objectives(self):
        objectives={
            'Why did gross margin fall?':'DIAGNOSTIC_ANALYTICS',
            'How should we account for factory under-absorption?':'ACCOUNTING_DETERMINATION',
            'Review the manufacturing close.':'CLOSE_REVIEW',
            'Prepare the manufacturing accounting memo.':'DOCUMENTATION',
            'Our manufacturing close is too manual. Review the process.':'PROCESS_CONTROL_REVIEW',
            'Our factory margins look terrible this month. Can you review the close and figure out what’s going on?':'DIAGNOSTIC_ANALYTICS',
        }
        for objective, expected in objectives.items():
            with self.subTest(objective=objective):
                self.assertEqual(interpret(objective).validate().primary,expected)

    def test_bounded_balance_has_no_artificial_work(self):
        for objective,owner in [('What is closing inventory?','inventory-cost'),('What is our closing AP balance?','accounts-payable')]:
            i=interpret(objective).validate()
            self.assertEqual(i.bounded_owner,owner)
            self.assertEqual(i.secondary,[])
            self.assertEqual(i.supporting,[])

    def test_invalid_duplicate_work_modes_rejected(self):
        for i in [Intent('UNKNOWN'),Intent('REPORTING',['REPORTING']),Intent('REPORTING',supporting=[dict(mode='CLOSE_REVIEW',reason='')]),Intent('REPORTING',['CLOSE_REVIEW'],bounded_owner='inventory-cost')]:
            with self.assertRaises(ValueError):i.validate()

    def test_close_explanation_keeps_close_primary(self):
        i=interpret('Review the month-end factory close and explain the margin movement.').validate()
        self.assertEqual(i.primary,'CLOSE_REVIEW')
        self.assertIn('DIAGNOSTIC_ANALYTICS',i.secondary)
        self.assertIn('ACCOUNTING_DETERMINATION',[x['mode'] for x in i.supporting])


import copy
from decimal import Decimal
from orchestration.tests.diagnostic_fixtures import diagnostic_manufacturing
from governance_cases import ready, refresh_release, document
from governance_accounting import digest
from production import assess_case

class IndependentDiagnosticQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=diagnostic_manufacturing()['facts']['analytics']
    def setUp(self):self.c=copy.deepcopy(self.base)
    def source(self,name):return next(d['content'] for d in self.c['documents'] if d['id']==name)
    def run_native(self):
        for d in self.c['documents']:d['content_hash']=digest(d['content'])
        self.c=ready('management-accounting-analytics',c=refresh_release(self.c))
        return assess_case('management-accounting-analytics',self.c)
    def reject(self):self.assertNotEqual(self.run_native()['status'],'complete')
    def test_native_bridge_and_percentage_denominator(self):
        r=self.run_native();self.assertEqual(r['status'],'complete')
        b=r['calculations']['diagnostic']['bridge'];n=lambda v:Decimal(str(v))
        self.assertEqual(n(b['starting'])+sum((n(x['contribution']) for x in b['drivers']),Decimal(0))+n(b['residual']),n(b['ending']))
        p=b['margin_points']
        self.assertLess(abs(n(p['starting'])+sum((n(x['contribution']) for x in p['drivers']),Decimal(0))+n(p['denominator_effect'])+n(p['residual'])-n(p['ending'])),Decimal('.00000001'))
        self.assertEqual(n(b['residual']),Decimal(0))
    def test_owner_metric_alias_double_count_is_rejected(self):
        g=copy.deepcopy(next(x for x in self.c['diagnostic']['groups'] if x['id']=='capacity'));g.update(id='alias-capacity',doc='alias-capacity',accounting_check=None)
        src=copy.deepcopy(self.source('capacity'));src['records'][0]['economic_components']=['caller-renamed-alias']
        document(self.c,'alias-capacity',src);self.c['diagnostic']['groups'].append(g);self.c['diagnostic']['group_inventory'].append(g['id'])
        self.c['diagnostic']['materiality']='1000000'
        self.reject()
    def test_management_evidence_cannot_be_promoted_by_hypothesis_label(self):
        src=copy.deepcopy(self.source('capacity'));src['evidence_class']='management_explanation'
        document(self.c,'management-cause',src)
        self.c['diagnostic']['hypotheses'][0]['tests'][0]['doc']='management-cause'
        self.c['diagnostic']['hypotheses'][0]['evidence_class']='direct_operational_evidence'
        r=self.run_native()
        if r['status']=='complete':self.assertNotEqual(r['calculations']['diagnostic']['hypotheses'][0]['disposition'],'SUPPORTED')
    def test_budget_cannot_replace_actual(self):
        self.source('diagnostic-current')['kind']='budget';self.reject()
    def test_wrong_entity_currency_period_comparator(self):
        for field,value in [('entity','Different entity'),('currency','EUR'),('period',['2024-01-01','2024-12-31'])]:
            with self.subTest(field=field):
                self.c=copy.deepcopy(self.base);self.source('diagnostic-prior')[field]=value;self.reject()
    def test_stale_version_and_postfreeze_comparator(self):
        for field,value in [('version','superseded'),('approved_on','2026-12-01')]:
            with self.subTest(field=field):
                self.c=copy.deepcopy(self.base);self.source('diagnostic-prior')[field]=value;self.reject()
    def test_missing_quantity_and_incomplete_population(self):
        for edit in ['quantity','population']:
            with self.subTest(edit=edit):
                self.c=copy.deepcopy(self.base)
                if edit=='quantity':del self.source('sales')['records'][0]['q1']
                else:self.source('sales')['records'].pop()
                self.reject()
    def test_duplicate_components_and_source_sign(self):
        self.source('labour')['records'][0]['economic_components']=self.source('material')['records'][0]['economic_components'];self.reject()
    def test_explicit_material_and_immaterial_residual(self):
        self.source('diagnostic-prior')['amount']='15001';self.source('diagnostic-prior')['records'][0]['amount']='15001'
        r=self.run_native();self.assertEqual(r['status'],'complete');self.assertEqual(Decimal(r['calculations']['diagnostic']['bridge']['residual']),Decimal('-1'))
        self.c['diagnostic']['materiality']='.5';self.reject()
    def test_unknown_materiality_preserves_unexplained(self):
        self.source('diagnostic-prior')['amount']='15001';self.source('diagnostic-prior')['records'][0]['amount']='15001';self.c['diagnostic']['materiality']=None;self.reject()
    def test_bool_materiality_and_nonfinite_amount(self):
        for value in [True,'NaN','Infinity']:
            with self.subTest(value=value):
                self.c=copy.deepcopy(self.base);self.c['diagnostic']['materiality']=value;self.reject()
    def test_accounting_treatment_and_journal_injection(self):
        for key in ['journal','capitalization','accounting_treatment']:
            with self.subTest(key=key):
                self.c=copy.deepcopy(self.base);self.c['diagnostic'][key]='Capitalize 45000';self.reject()
    def test_accounting_question_binds_actual_owner_metric(self):
        q=next(x for x in self.c['diagnostic']['groups'] if x['id']=='capacity')['accounting_check'];q['amount']='45001';self.reject()
    def test_association_never_supports_operational_cause(self):
        self.c['diagnostic']['hypotheses'][0]['evidence_class']='statistical_association'
        r=self.run_native();self.assertEqual(r['status'],'complete');self.assertEqual(r['calculations']['diagnostic']['hypotheses'][0]['disposition'],'UNRESOLVED')
    def test_no_evidence_hypothesis_remains_unresolved(self):
        self.c['diagnostic']['hypotheses'][0]['tests']=[]
        r=self.run_native();self.assertEqual(r['status'],'complete');self.assertEqual(r['calculations']['diagnostic']['hypotheses'][0]['disposition'],'UNRESOLVED')
    def test_reversed_cost_sign_cannot_be_excused_by_materiality(self):
        self.c['diagnostic']['materiality']='1000000'
        next(g for g in self.c['diagnostic']['groups'] if g['id']=='capacity')['sign']=1
        next(t for t in self.c['diagnostic']['component_ties'] if 'capacity' in t['groups'])['sign']=1
        self.reject()
    def test_owner_component_relabel_cannot_change_margin_basis(self):
        src=self.source('diagnostic-current')
        # Reversal changes the metric into revenue minus relief plus overhead,
        # while the record still calls it approved inclusive gross profit.
        src['owner_components'][-1]['sign']=1
        src['amount']='73696';src['records'][0]['amount']='73696'
        self.c['diagnostic']['materiality']='1000000'
        self.reject()


from orchestration.runtime import CAO
from interfaces.public_output import ROUTES

class IndependentDiagnosticRuntimeQA(unittest.TestCase):
    def test_native_owner_escalation_and_public_privacy(self):
        request=diagnostic_manufacturing();runtime=CAO();case=runtime.run(request)
        self.assertEqual(case.outcome,'complete')
        self.assertEqual(case.work_modes['primary'],'DIAGNOSTIC_ANALYTICS')
        self.assertTrue(case.accounting_questions)
        self.assertEqual(case.accounting_questions[0]['status'],'OWNER_RECHECK_SUPPORTED')
        followups=[n for n in case.graph.nodes.values() if n.issue=='diagnostic accounting follow-up']
        self.assertEqual(len(followups),1)
        self.assertEqual(followups[0].selected_skill,'inventory-cost')
        for route in ROUTES:
            import json
            value=json.dumps(runtime.public(case,route))
            for token in ['source_note','reviewer_identity','case_fingerprint','source_hash','management-accounting-analytics','inventory-cost']:
                self.assertNotIn(token,value)
            self.assertIn('residual',value)
            self.assertIn('Hypothesis',value)




class IndependentComparatorAndRetentionQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=diagnostic_manufacturing()['facts']['analytics']
    setUp=IndependentDiagnosticQA.setUp
    source=IndependentDiagnosticQA.source
    run_native=IndependentDiagnosticQA.run_native
    reject=IndependentDiagnosticQA.reject
    def test_malformed_comparator_freeze_date_rejected(self):
        self.c['diagnostic']['comparator']['frozen_on']='2026-11-99'
        self.reject()
    def test_malformed_comparator_approval_date_rejected(self):
        self.source('diagnostic-prior')['approved_on']='2026-00-00'
        self.reject()
    def test_supplied_forecast_is_comparator_only(self):
        d=self.c['diagnostic'];span=[self.c['period_start'],self.c['reporting_period']]
        old=self.source('diagnostic-prior');old.update(kind='forecast',period=span,version='forecast-v3')
        d['comparator'].update(kind='forecast',period=span,version='forecast-v3')
        for g in d['groups']:
            src=self.source(g['doc']);src.update(baseline_period=span,comparator_version='forecast-v3')
        r=self.run_native();self.assertEqual(r['status'],'complete')
        self.assertEqual(r['calculations']['diagnostic']['bridge']['comparator_kind'],'forecast')
        self.assertEqual(r['journal_entry_implications'],[])

class IndependentResidualRuntimeQA(unittest.TestCase):
    def test_material_residual_keeps_valid_bridge_and_limits_publicly(self):
        request=diagnostic_manufacturing();c=request['facts']['analytics']
        doc=next(x for x in c['documents'] if x['id']=='diagnostic-prior');doc['content']['amount']='15001';doc['content']['records'][0]['amount']='15001';doc['content_hash']=digest(doc['content'])
        c['diagnostic']['materiality']='.5';request['facts']['analytics']=ready('management-accounting-analytics',c=refresh_release(c))
        runtime=CAO();case=runtime.run(request)
        self.assertNotEqual(case.outcome,'complete');self.assertTrue(case.diagnostics)
        self.assertEqual(Decimal(case.diagnostics[0]['bridge']['residual']),Decimal('-1'))
        for route in ROUTES:
            import json
            output=json.dumps(runtime.public(case,route))
            self.assertIn('unexplained residual is -1',output)
            self.assertIn('unresolved',output.lower())




class IndependentHypothesisAndMethodQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=diagnostic_manufacturing()['facts']['analytics']
    setUp=IndependentDiagnosticQA.setUp
    source=IndependentDiagnosticQA.source
    run_native=IndependentDiagnosticQA.run_native
    reject=IndependentDiagnosticQA.reject
    def test_hypothesis_dispositions_follow_evidence_not_prose(self):
        for values,expected in [(['0'],'SUPPORTED'),(['100000'],'REJECTED'),(['0','100000'],'PARTIALLY_SUPPORTED')]:
            with self.subTest(expected=expected):
                self.c=copy.deepcopy(self.base);h=self.c['diagnostic']['hypotheses'][0]
                original=copy.deepcopy(h['tests'][0]);h['tests']=[dict(original,value=value) for value in values]
                r=self.run_native();self.assertEqual(r['status'],'complete')
                self.assertEqual(r['calculations']['diagnostic']['hypotheses'][0]['disposition'],expected)
    def test_anomaly_is_observation_not_accounting_error(self):
        r=self.run_native();d=r['calculations']['diagnostic'];self.assertTrue(d['observations'])
        self.assertTrue(all(x['status']=='OBSERVATION_ONLY' for x in d['observations']))
        self.assertTrue(all('error' not in x['observation'].lower() for x in d['observations']))
    def test_forecasting_and_budgeting_generation_remain_excluded(self):
        for flag in ['budgeting','forecasting','commercial_planning','automatic_gl_correction']:
            with self.subTest(flag=flag):
                self.c=copy.deepcopy(self.base);self.c['governance_method'][flag]=True;self.reject()
    def test_group_omission_keeps_residual_instead_of_other_plug(self):
        d=self.c['diagnostic'];d['groups']=[g for g in d['groups'] if g['id']!='capacity'];d['group_inventory']=[g['id'] for g in d['groups']]
        d['component_ties']=[t for t in d['component_ties'] if 'capacity' not in t['groups']]
        r=self.run_native();self.assertNotEqual(r['status'],'complete')
        b=r['calculations']['diagnostic']['bridge'];self.assertEqual(Decimal(b['residual']),Decimal('-25000'))
        self.assertFalse(any('capacity' in x['id'] for x in b['drivers']))




class IndependentNativeLineageQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=diagnostic_manufacturing()['facts']['analytics']
    setUp=IndependentDiagnosticQA.setUp
    source=IndependentDiagnosticQA.source
    run_native=IndependentDiagnosticQA.run_native
    reject=IndependentDiagnosticQA.reject
    def test_omitting_allocation_cannot_enable_false_cost_partition(self):
        material=self.source('material');other=self.source('other-cost')
        del material['component_allocation'];del other['component_allocation']
        material['records'][0].update(p1='20',current_amount='240')
        other['records'][0]['current_amount']='8904'
        # COGS still reconciles exactly; the made-up material inflation is hidden
        # by an equal reduction in the unrelated overhead cost partition.
        self.reject()




class IndependentProtectedRoadmapMaintenanceQA(unittest.TestCase):
    def test_only_authorized_roadmap_protection_label_may_change(self):
        import hashlib,json
        from pathlib import Path
        root=Path(__file__).resolve().parents[2]
        record=json.loads((root/'skills/insurance-contracts-accounting/LIVE-BASELINE.json').read_text())
        self.assertEqual(len(record['protected_documents']),1101)
        entries=[r for r in record['protected_documents'] if r['path']=='architecture/build-roadmap.md']
        self.assertEqual(len(entries),1)
        self.assertEqual(entries[0]['sha256'],hashlib.sha256((root/'architecture/build-roadmap.md').read_bytes()).hexdigest())
        entries[0]['sha256']='<authorized-roadmap-only>'
        digest=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        # Derived independently from live-main186b3028 original manifest bytes.
        # Every other protected path/hash and all manifest metadata remain fixed.
        self.assertEqual(digest,'52ec68c7fe2981482e5a7aea7f8f9afd7df3ddf4c1fc539776bb95a64ef78cdc')

if __name__=='__main__':unittest.main()

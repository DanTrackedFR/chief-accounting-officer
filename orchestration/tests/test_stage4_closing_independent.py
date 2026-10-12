"""Independent closing accounting authority and history attacks."""
import copy
import unittest
from decimal import Decimal
from orchestration.tests import stage4_closing_fixtures as fixture, stage4_correction_fixtures as prior, stage4_fixtures as s4
from orchestration.runtime import CAO
from orchestration.governed_plan import observation
from additional_cases import certify

class IndependentClosing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.control,cls.record=fixture.run()
    def setUp(self):self.f=copy.deepcopy(self.control);self.r=copy.deepcopy(self.record);self.e=self.f['session'];self.n=self.f['nodes']
    def test_reviewed_closing_evidence_separate_from_original(self):
        source=self.e.sources[self.n['fx-ENTITY-UK'].id];old=self.r['before']['fx-ENTITY-UK'].payload()['facts_used']
        self.assertEqual(Decimal(old['pairs'][0]['rate_a']),Decimal('.8'))
        self.assertEqual(Decimal(source['pairs'][0]['rate_a']),Decimal('.9'))
        self.assertTrue(source['correction_evidence']['reviewed'])
        self.assertNotEqual(source['intercompany_transactions'][0]['source_id'],old['intercompany_transactions'][0]['source_id'])
    def test_native_owner_and_translation_profit_once(self):
        legal=self.e.versions.current(self.n['fx-ENTITY-UK'].id).payload();pair=legal['calculations']['pairs'][0]
        self.assertEqual(Decimal(pair['a_functional']),Decimal('18'));self.assertEqual(Decimal(pair['a_fx_gain']),Decimal('2'))
        self.assertEqual(legal['calculations']['journal_entities'],['ENTITY-UK'])
        t=self.e.versions.current(self.n['fx-translation-ENTITY-UK'].id).payload()
        self.assertEqual(t['journal_entry_implications'],[]);self.assertEqual(Decimal(t['calculations']['translation']['profit_translated']),Decimal('2'))
        self.assertEqual(self.e.versions.current(self.n['fx-reassessment'].id).payload()['journal_entry_implications'],[])
    def test_original_immutable_and_superseded(self):
        old=self.r['before']['fx-ENTITY-UK'];new=self.e.versions.current(old.node_id)
        self.assertEqual(self.e.versions.versions[old.version_id],old)
        self.assertEqual(self.e.versions.state(old.version_id),'SUPERSEDED');self.assertEqual(new.predecessor,old.version_id)
        self.assertEqual(self.e.versions.state(new.version_id),'CURRENT')
        self.assertEqual(self.r['before']['match-fx'].payload()['matching']['classification'],'FX_DIFFERENCE')
        self.assertEqual(self.r['before']['fx-reassessment'].payload()['calculations']['pairs'][0]['a_functional'],'16.00')
    def test_without_closing_evidence_original_remains_blocked(self):
        f=prior.initial();e=f['session'];p=e.versions.current(f['nodes']['fx-reassessment'].id).payload()['calculations']['pairs'][0]
        self.assertEqual(Decimal(p['a_functional'])-Decimal(p['b_functional']),Decimal('-2'))
        self.assertNotIn(f['case'].status,('COMPLETE','CLOSED'))
    def test_unreviewed_closing_evidence_rejected(self):
        c=copy.deepcopy(fixture.CLOSE);c['reviewed']=False
        with self.assertRaises(ValueError):fixture.correction(prior.initial(),c)
    def test_wrong_closing_date_rejected(self):
        c=copy.deepcopy(fixture.CLOSE);c['valuation_date']='2026-09-30'
        with self.assertRaises(ValueError):fixture.correction(prior.initial(),c)
    def test_missing_provenance_rejected(self):
        c=copy.deepcopy(fixture.CLOSE);c['provenance']=''
        with self.assertRaises(ValueError):fixture.correction(prior.initial(),c)
    def test_owner_rejects_supplied_gl_inconsistent_with_quote(self):
        c=copy.deepcopy(fixture.CLOSE);c['uk_gl']='17'
        with self.assertRaises(Exception):fixture.run(c)
    def test_alternate_supported_quote_owner_not_target_drives_result(self):
        f=prior.initial();n=f['nodes']['fx-ENTITY-UK'];c=copy.deepcopy(fixture.CLOSE)
        native=fixture.correction(f,c)
        native['pairs'][0].update(rate_a='.85',gl_a='17',rate_evidence='Independent local-only reviewed GBP/USD quote0.85; no coherent Group feed claimed')
        native['intercompany_transactions'][0].update(functional_amount='17',source_id='INDEPENDENT-LOCAL-CLOSE-085')
        native['correction_evidence'].update(source_id='INDEPENDENT-LOCAL-CLOSE-085',gbp_per_usd='.85',uk_gl='17',provenance='Separately reviewed local-only quote and ledger; Group quote qualification remains unavailable')
        native=certify('intercompany-accounting',native)
        fresh=s4.qualified_replacement(f,n.id,native);CAO().correct(f['case'],n.id,fresh,'Independent alternate local-only reviewed closing quote')
        p=f['session'].versions.current(n.id).payload()['calculations']['pairs'][0]
        self.assertEqual(Decimal(p['a_functional']),Decimal('17'));self.assertEqual(Decimal(p['a_fx_gain']),Decimal('1'))
        node=f['nodes']['fx-translation-ENTITY-UK'];src=s4.qualified_replacement(f,node.id,fixture.source(f,node.logical_id))
        f['session'].execute(node.id,observation,src,'Independent exact alternate translation')
        t=f['session'].versions.current(node.id).payload()['calculations']['translation']
        self.assertEqual(Decimal(t['translated_tb']['ic loan']),Decimal('17'))
        self.assertEqual(Decimal(t['profit_translated']),Decimal('1'))
    def test_alternate_quote_cannot_hide_contradictory_reporting_ledger(self):
        c=copy.deepcopy(fixture.CLOSE);c.update(gbp_per_usd='.85',uk_gl='17')
        with self.assertRaises(Exception):fixture.run(c)
    def test_clqa01_contradictory_reviewed_presentation_quote_rejected(self):
        # Reproduced pre-fix: supplied1.20 ignored, native translation1, residual0.
        c=copy.deepcopy(fixture.CLOSE);c['eur_per_gbp']='1.20'
        with self.assertRaises(ValueError):fixture.run(c)
    def test_unrelated_versions_exactly_current(self):
        for label,old in self.r['before'].items():
            if old.node_id in self.r['plan']['unaffected']:
                self.assertEqual(self.e.versions.current(old.node_id).version_id,old.version_id)
                self.assertEqual(self.e.versions.state(old.version_id),'CURRENT')
    def test_stale_translation_receipt_cannot_reuse(self):
        c=fixture.source(self.f,'fx-translation-ENTITY-UK');row=c['versioned_dependency_receipts'][0]
        row['result_version']=self.r['before']['fx-ENTITY-UK'].version_id
        with self.assertRaises(ValueError):self.e.validate_receipt(row,self.n['fx-translation-ENTITY-UK'].id)
    def test_bounded_residual_zero_not_full_case_closure(self):
        self.assertEqual(Decimal(self.r['residual']['signed_receivable_minus_payable']),Decimal('0'))
        self.assertNotIn(self.f['case'].status,('COMPLETE','CLOSED'))
    def test_public_answer_keeps_reviewed_source_private(self):
        public=CAO().public(self.f['case'])
        self.assertNotIn(fixture.CLOSE['source_id'],str(public));self.assertNotIn('provenance',str(public))

    def test_nonfinite_or_nonpositive_closing_quotes_refuse(self):
        for field in ('gbp_per_usd','eur_per_usd','eur_per_gbp'):
            for value in ('NaN','Infinity','0','-1'):
                evidence=copy.deepcopy(fixture.CLOSE);evidence[field]=value
                with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                    fixture.correction(prior.initial(),evidence)
    def test_coherent_but_changed_retained_presentation_quotes_refuse(self):
        evidence=copy.deepcopy(fixture.CLOSE)
        evidence.update(eur_per_usd='1.08',eur_per_gbp='1.20')
        # Triangle is coherent; current presentation receipts still use .9/1.
        with self.assertRaises(ValueError):fixture.run(evidence)

class IndependentPayableTranslation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from orchestration.tests import stage4_closing_population as whole
        cls.whole=whole;cls.control=whole.initial()
    def setUp(self):
        self.f=copy.deepcopy(self.control);self.e=self.f['session'];self.n=self.f['nodes']['timing-reassessment']
    def test_payable_only_translation_keeps_actual_reporting_qualified_receivable(self):
        result=self.e.versions.current(self.n.id).payload()['calculations']['pairs'][0]
        self.assertEqual(Decimal(result['a_functional']),Decimal('30'))
        self.assertEqual(Decimal(result['b_functional']),Decimal('30'))
        self.assertEqual(self.e.versions.current(self.n.id).payload()['journal_entry_implications'],[])
    def test_payable_transformation_omission_rejected(self):
        from orchestration.stage3 import validate_native_bindings
        c=self.whole.timing_reassessment(self.f)
        c['versioned_dependency_receipts']=[r for r in c['versioned_dependency_receipts'] if r['producer_scope']!='ENTITY-UK']
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n,c,c['versioned_dependency_receipts'])
    def test_direct_receivable_cannot_claim_unqualified_currency(self):
        c=self.whole.timing_reassessment(self.f)
        row=next(r for r in c['versioned_dependency_receipts'] if r['producer_scope']=='ENTITY-NL')
        row['value_currency']='GBP'
        with self.assertRaises(ValueError):self.e.validate_receipt(row,self.n.id)
    def test_direct_receivable_omission_rejected(self):
        from orchestration.stage3 import validate_native_bindings
        c=self.whole.timing_reassessment(self.f)
        c['versioned_dependency_receipts']=[r for r in c['versioned_dependency_receipts'] if r['producer_scope']!='ENTITY-NL']
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n,c,c['versioned_dependency_receipts'])

class IndependentWholePopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from orchestration.tests import stage4_closing_population as whole
        cls.whole=whole;cls.control,cls.record=whole.run()
    def setUp(self):
        self.f=copy.deepcopy(self.control);self.r=copy.deepcopy(self.record);self.e=self.f['session'];self.n=self.f['nodes']
    def test_complete_group_relationships_and_one_operation_per_entity(self):
        source=self.e.sources[self.n['elimination'].id]
        self.assertEqual({p['transaction_id'] for p in source['intercompany']},{'clean','mismatch','timing','fx'})
        translated=[r for r in source['versioned_dependency_receipts'] if r['metric_path']==['calculations','translation','translated_tb']]
        self.assertEqual({r['producer_scope'] for r in translated},{'ENTITY-US','ENTITY-UK'})
        self.assertEqual(len(translated),2)
    def test_native_group_economics_current_but_reporting_honestly_refuses(self):
        p=self.e.versions.current(self.n['elimination'].id).payload()
        self.assertEqual(p['status'],'complete');self.assertEqual(Decimal(p['calculations']['equity']['profit']),Decimal('3'))
        self.assertEqual(Decimal(p['calculations']['cash_flow']['opening_cash']),Decimal('490'))
        self.assertEqual(Decimal(p['calculations']['cash_flow']['financing']),Decimal('0'))
        refusal=self.r['closing_rework']['native_refusal']
        self.assertEqual(refusal['status'],'blocked');self.assertIn('Restated comparative equity',refusal['conclusion'])
        self.assertNotIn(self.f['case'].status,('COMPLETE','CLOSED'))
    def test_every_current_legal_side_cannot_be_omitted(self):
        from orchestration.stage3 import validate_group_loan_population
        c=self.whole.group_source(self.f);roster=c['group_population_coverage']['required_legal_result_versions']
        self.assertEqual(len(roster),8)
        for version in roster:
            attack=copy.deepcopy(c);attack['group_population_coverage']['required_legal_result_versions'].remove(version)
            with self.subTest(version=version),self.assertRaises(ValueError):validate_group_loan_population(self.e,self.n['elimination'],attack,attack['versioned_dependency_receipts'])
    def test_shortened_legal_perimeter_cannot_close(self):
        from orchestration.stage3 import validate_group_loan_population
        c=self.whole.group_source(self.f);c['entities']=[x for x in c['entities'] if x['id']!='ENTITY-UK']
        with self.assertRaises(ValueError):validate_group_loan_population(self.e,self.n['elimination'],c,c['versioned_dependency_receipts'])
    def test_each_whole_operation_translation_omission_rejects(self):
        from orchestration.stage3 import validate_native_bindings
        c=self.whole.group_source(self.f)
        for scope in ('ENTITY-US','ENTITY-UK'):
            attack=copy.deepcopy(c);attack['versioned_dependency_receipts']=[r for r in attack['versioned_dependency_receipts'] if not (r['producer_scope']==scope and r['metric_path']==['calculations','translation','translated_tb'])]
            with self.subTest(scope=scope),self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['elimination'],attack,attack['versioned_dependency_receipts'])
    def test_parent_profit_cannot_omit_exact_native_dependency(self):
        from orchestration.stage3 import validate_native_bindings
        c=self.whole.group_source(self.f)
        c['stage3_input_bindings']=[b for b in c['stage3_input_bindings'] if b['target_path']!=['entities',0,'balances','correction income']]
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['elimination'],c,c['versioned_dependency_receipts'])
    def test_parent_profit_cannot_replace_native_gain_with_equal_balanced_plug(self):
        from orchestration.stage3 import validate_native_bindings
        c=self.whole.group_source(self.f);c['entities'][0]['balances']['correction income']='-2';c['entities'][0]['balances']['equity']='-486'
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['elimination'],c,c['versioned_dependency_receipts'])
    def test_contradictory_parent_opening_ledger_rejects(self):
        self.f['reviewed_parent_opening_ledger']['mismatch_payable']='12'
        with self.assertRaises(ValueError):self.whole.group_source(self.f)
    def test_group_elimination_each_relationship_once(self):
        source=self.e.sources[self.n['elimination'].id];payload=self.e.versions.current(self.n['elimination'].id).payload()
        journals=payload['journal_entry_implications'];self.assertEqual(len(journals),6)
        for item in source['intercompany']:
            matches=[j for j in journals if len(j)==2 and {(r['side'],r['account'],Decimal(r['amount'])) for r in j}=={('Dr',item['debit_account'],Decimal(item['amount'])),('Cr',item['credit_account'],Decimal(item['amount']))}]
            self.assertEqual(len(matches),1,item['transaction_id'])
    def test_reporting_and_public_cannot_reuse_stale_pre_correction_results(self):
        for label in ('reporting','analytics','group'):
            old=self.e.versions.current(self.n[label].id,allow_stale=True)
            self.assertEqual(self.e.versions.state(old.version_id),'STALE')
            with self.assertRaises(ValueError):self.e.versions.require_current(old.version_id)
        self.assertEqual(CAO().public(self.f['case'])['status'],'partial')
    def test_global_current_journal_selection_refuses_stale_reporting_population(self):
        events=[]
        for label,economic in [('mismatch-ENTITY-NL','reviewed-payable-correction'),('fx-ENTITY-UK','reviewed-closing-fx'),('elimination','current-group-eliminations')]:
            node=self.n[label];version=self.e.versions.current(node.id);journals=version.payload()['journal_entry_implications']
            events.append(dict(economic_id=economic,posting_scope=version.scope_id,period_id=version.period_id,period=node.period,currency='GBP' if label=='fx-ENTITY-UK' else 'EUR',result_version=version.version_id,primary=[dict(owner=node.id,index=i) for i in range(len(journals))],witnesses=[],evidence='Independently reviewed exact current owner journal allocation'))
        context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=self.e.cases.scopes.record(),period_registry=self.e.periods.record())
        self.assertEqual(sum(len(self.e.versions.current(self.n[label].id).payload()['journal_entry_implications']) for label in ('mismatch-ENTITY-NL','fx-ENTITY-UK','elimination')),8)
        with self.assertRaisesRegex(ValueError,'Stale result'):
            self.e.current_journals(context,events)

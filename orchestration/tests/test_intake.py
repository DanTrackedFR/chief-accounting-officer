import copy
import json
import unittest
from decimal import Decimal
from dataclasses import replace
from orchestration.intake import *
from orchestration.intake.semantic import transform
from orchestration.tests.intake_fixtures import *
from interfaces.public_output import ROUTES

class IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources=factory_sources();cls.proposal=factory_proposal(cls.sources)
        cls.intake,cls.prepared=factory();cls.pack=factory_review_pack(cls.prepared)
        cls.intake.execute(cls.prepared,cls.pack)
    def prepare(self,p=None,sources=None,records=None,scope=None):
        p=copy.deepcopy(p or self.proposal)
        return Intake(FixturePlanner(p)).prepare(OBJECTIVE,sources or self.sources,records or [],scope or SCOPE)
    def invalid(self,mutate):
        p=copy.deepcopy(self.proposal);mutate(p);r=self.prepare(p);self.assertFalse(r.validation['accepted'])
    def test_free_form_semantic_interface_inventory(self):
        p=self.prepared;self.assertTrue(p.validation['accepted']);self.assertEqual(len(p.inventory),10)
        self.assertEqual(p.case.work_modes['primary'],'DIAGNOSTIC_ANALYTICS')
    def test_factory_conflict_retained_and_partial(self):
        p=self.prepared;self.assertEqual(p.case.outcome,'partial');self.assertEqual(p.case.status,'DOCUMENTED')
        labour=[c for c in p.candidates if c['attribute']=='factory_labour']
        self.assertEqual({c['claim']['value'] for c in labour},{'11000','10800'})
        self.assertTrue(all(c['promotion']=='disputed' for c in labour))
        self.assertEqual([q['attribute'] for q in p.questions],['factory_labour'])
    def test_factory_diagnostic_owner_execution(self):
        p=self.prepared;self.assertEqual(len(p.case.diagnostics),1)
        bridge=p.case.diagnostics[0]['bridge'];self.assertEqual(Decimal(bridge['change']),Decimal('-31304'))
        self.assertEqual(Decimal(bridge['residual']),0)
        self.assertEqual(p.case.accounting_questions[0]['status'],'OWNER_RECHECK_SUPPORTED')
        self.assertEqual(p.case.accounting_questions[0]['accounting_disposition'],'unallocated manufacturing expense')
    def test_lineage_final_driver_to_source_row(self):
        p=self.prepared;driver=next(d for d in p.case.diagnostics[0]['bridge']['drivers'] if d['label']=='Labour rate')
        self.assertEqual(Decimal(driver['contribution']),Decimal('-160'))
        owner=next(n['result'] for n in p.case.workplan_nodes if n['selected_skill']=='inventory-cost' and n['issue']!='diagnostic accounting follow-up')
        self.assertEqual(Decimal(owner['calculations']['order-1']['direct_labour']),Decimal('10800'))
        pay=next(n['result'] for n in p.case.workplan_nodes if n['selected_skill']=='employee-benefits-payroll' and n['issue']!='diagnostic accounting follow-up')
        self.assertEqual(Decimal(pay['calculations']['expense']),Decimal('10800'))
        lineage=next(l for l in p.lineage if l['fact_id']=='pay-charge')
        self.assertEqual(lineage['source_lineage'][0]['source_id'],'payroll')
        self.assertEqual(lineage['source_lineage'][0]['location']['row'],2)
        self.assertEqual(lineage['owner_input_path'],['benefits','salary','expected_charge'])
    def test_simple_ap_routes_only_ap(self):
        intake,p=ap_control();self.assertEqual(p.case.outcome,'complete');self.assertEqual(p.case.skills_invoked,['accounts-payable'])
        self.assertEqual(p.case.conclusions[0]['calculations']['closing_ap'],'20');self.assertFalse(p.questions)
    def test_contract_routes_without_conclusion(self):
        intake,p=contract_control();self.assertEqual(p.case.work_modes['primary'],'ACCOUNTING_DETERMINATION')
        self.assertEqual({n['selected_skill'] for n in p.case.workplan_nodes},{'revenue-recognition'})
        self.assertEqual(p.candidates[0]['promotion'],'unresolved');self.assertEqual(p.case.outcome,'blocked')
        self.assertIn('refund_rights',{q['attribute'] for q in p.questions})
    def test_no_live_model_dependency(self):
        inv=Inventory(self.sources);req=RequestContext(OBJECTIVE,(),inv.normalized(),[],[])
        self.assertEqual(FixturePlanner(self.proposal).propose(req).record(),self.proposal.record())
    def test_nonexistent_owner(self):self.invalid(lambda p:p.issues[0].value.update(owner='invented'))
    def test_nonproduction_owner(self):self.invalid(lambda p:p.issues[0].value.update(owner='government-grants',family='grant'))
    def test_bad_workmode(self):self.invalid(lambda p:setattr(p.primary_mode,'value','FPNA'))
    def test_inferred_cannot_be_established(self):
        p=copy.deepcopy(self.proposal);p.facts[0].claim.status='INFERRED';p.facts[0].confirmation_required=True
        r=self.prepare(p);self.assertEqual(r.candidates[0]['promotion'],'unresolved')
    def test_model_created_approval_status(self):self.invalid(lambda p:setattr(p.facts[0].claim,'status','APPROVED'))
    def test_assumed_framework(self):self.invalid(lambda p:p.frameworks.append(cl('IFRS',status='ASSUMED',confidence=.5)))
    def test_fabricated_framework(self):self.invalid(lambda p:p.frameworks.append(cl('MARS_GAAP')))
    def test_hidden_assumption(self):self.invalid(lambda p:setattr(p.facts[0].claim,'status','ASSUMED'))
    def test_missing_evidence(self):self.invalid(lambda p:setattr(p.facts[0].claim,'evidence',['fake']))
    def test_bad_period(self):self.invalid(lambda p:p.facts[0].dimensions.update(period=['2026-02-30','2026-12-31']))
    def test_bad_currency(self):self.invalid(lambda p:p.facts[0].dimensions.update(currency='US dollars'))
    def test_confidence_bool(self):self.invalid(lambda p:setattr(p.facts[0].claim,'confidence',True))
    def test_confidence_disputed(self):self.invalid(lambda p:setattr(p.facts[0].claim,'status','DISPUTED'))
    def test_sign_inversion(self):self.invalid(lambda p:setattr(p.facts[0].claim,'value','-600000'))
    def test_source_transformation_no_guess_dates(self):
        with self.assertRaises(ValueError):transform('01/02/26','iso_date')
    def test_numeric_text_malformed(self):
        for value in ('1,000','$5','NaN','1e10','=SUM(A1:A2)',True):
            with self.subTest(value=value),self.assertRaises(ValueError):transform(value,'decimal')
    def test_duplicate_economics_alias(self):
        self.invalid(lambda p:p.facts.append(replace(copy.deepcopy(p.facts[0]),id='alias')))
    def test_budget_not_promoted_into_actual(self):
        p=copy.deepcopy(self.proposal);f=p.facts[0];f.dimensions['comparator']='budget'
        r=self.prepare(p);self.assertEqual(r.candidates[0]['promotion'],'unresolved')
    def test_filename_not_metadata(self):
        raw=RawSource('unknown','final_TB_IFRS_USD_2026.xlsx','json',[{'mystery':'5'}])
        ex=Inventory([raw]).extractions['unknown'];self.assertEqual(ex.source['metadata'],{})
        self.assertEqual(set(ex.source['unresolved_dimensions']),{'entity','period','currency'})
    def test_source_change_after_extraction(self):
        inv=Inventory(self.sources);inv.raw['pnl'].metadata['currency']='EUR'
        with self.assertRaises(ValueError):inv.verify()
    def test_extracted_row_change(self):
        inv=Inventory(self.sources);next(iter(inv.extractions['pnl'].fields.values()))['value']='changed'
        with self.assertRaises(ValueError):inv.verify()
    def test_fingerprint_change(self):
        inv=Inventory(self.sources);inv.extractions['pnl'].source['fingerprint']='broken'
        with self.assertRaises(ValueError):inv.verify()
    def test_duplicate_source_ids(self):
        with self.assertRaises(ValueError):Inventory([self.sources[0],self.sources[0]])
    def test_duplicate_source_content(self):
        with self.assertRaises(ValueError):Inventory([self.sources[0],replace(self.sources[0],id='alias')])
    def test_csv_invalid(self):
        for text in ('a,a\n1,2','a,b\n1,2,3','a,b\n"unterminated,1'):
            with self.subTest(text=text),self.assertRaises(ValueError):Inventory([RawSource('bad','x','csv',text)])
    def test_json_nested_cell(self):
        with self.assertRaises(ValueError):Inventory([RawSource('bad','x','json',[{'amount':{'script':'danger'}}])])
    def test_unsupported_binary(self):
        for fmt in ('xlsx','pdf','docx','image'):
            with self.subTest(fmt=fmt),self.assertRaises(ValueError):Inventory([RawSource('bad','x',fmt,'bytes')])
    def test_paths_are_inert(self):
        inv=Inventory([RawSource('safe','../../secret.csv','csv','a,b\n1,2')]);self.assertEqual(inv.extractions['safe'].source['rows'],1)
    def test_formulas_are_inert_not_amounts(self):
        inv=Inventory([RawSource('safe','x.csv','csv','a\n=HYPERLINK("evil")')]);self.assertTrue(inv.fields())
        with self.assertRaises(ValueError):transform(next(iter(inv.fields().values()))['value'],'decimal')
    def test_preserve_zeros_duplicates_and_subtotal(self):
        inv=Inventory([RawSource('safe','x.csv','csv','account,amount\nA,0\nA,1\nA,1\nTotal,2')])
        self.assertEqual(len(inv.extractions['safe'].tables[0]['rows']),4)
    def test_transform_ledger(self):
        t=self.prepared.transformations[0];self.assertEqual(t['method'],'decimal');self.assertTrue(t['input_fingerprints'])
        self.assertEqual(len(self.prepared.transformations),18)
    def test_context_not_overwritten(self):
        p=copy.deepcopy(self.proposal);p.context_candidates['framework']=cl('US_GAAP')
        records=[dict(attribute='framework',value='IFRS',status='APPROVED')];original=copy.deepcopy(records)
        r=self.prepare(p,records=records);self.assertEqual(records,original)
        self.assertTrue(r.memory_candidates[0]['conflict']);self.assertEqual(r.memory_candidates[0]['status'],'PROPOSED')
    def test_question_known_context_suppressed(self):self.assertNotIn('framework',{q['attribute'] for q in self.prepared.questions})
    def test_no_runtime_certification(self):
        x,p=factory();x.execute(p);self.assertEqual(p.case.outcome,'blocked');self.assertFalse(p.case.skills_invoked)
    def test_bad_reviewed_input_binding(self):
        x,p=factory();pack=copy.deepcopy(self.pack);pack.request['facts']['supplier_cost']['invoices'][0]['amount']='121'
        with self.assertRaises(ValueError):x.execute(p,pack)
    def test_disputed_binding_rejected(self):
        x,p=factory();pack=copy.deepcopy(self.pack);pack.bindings.append(Binding('labour-export','employee-benefits-payroll',('benefits','salary','expected_charge')))
        with self.assertRaises(ValueError):x.execute(p,pack)
    def test_no_review_bypass(self):
        x,p=factory();pack=copy.deepcopy(self.pack);pack.request['facts']['supplier_cost']['reviewer_signoff']={}
        x.execute(p,pack);self.assertNotEqual(p.case.outcome,'complete')
    def test_public_all_routes(self):
        p=self.prepared
        for route in ROUTES:
            output=json.dumps(self.intake.public(p,route))
            for forbidden in ('source_fingerprint','extracted_fields','source_lineage','FX is the main reason margin is down','Synthetic independent factory journal reviewer','source_note'):
                self.assertNotIn(forbidden,output)
            self.assertIn('Resolve factory labour',output)
    def test_invalid_errors_do_not_echo_source(self):
        p=copy.deepcopy(self.proposal);p.issues[0].value['owner']='Source: private'
        r=self.prepare(p);output=json.dumps(Intake(FixturePlanner(p)).public(r));self.assertNotIn('private',output)

if __name__=='__main__':unittest.main()

class AdditionalIntakeControls(unittest.TestCase):
    def test_huge_source_record_id_rejected(self):
        with self.assertRaises(ValueError):Inventory([RawSource('bad','x','json',[dict(record_id='a'*121,amount='1')])])
    def test_mixed_currency_row_not_established(self):
        from orchestration.tests.intake_fixtures import metadata,numeric,cl
        sources=[RawSource('mixed','AP.csv','csv','record_id,amount,currency\nA,10,EUR\nB,20,USD',metadata())]
        inv=Inventory(sources);f=numeric(inv,'amount','supplier_cost','amount','mixed','amount',2)
        p=StructuredProposal(cl('Review',status='USER_STATED',confidence=1),cl('Review'),cl('ACCOUNTING_DETERMINATION'),facts=[f],issues=[cl(dict(id='ap',owner='accounts-payable',family='supplier_cost',fact_ids=[f.id],dependencies=[],required_fields=['amount']),f.claim.evidence)])
        prepared=Intake(FixturePlanner(p)).prepare('Review',sources,[],SCOPE)
        self.assertEqual(prepared.candidates[0]['promotion'],'unresolved')
    def test_current_source_wrong_period_rejected(self):
        p=factory_proposal(factory_sources());p.facts[0].dimensions['period']=['2026-11-01','2026-11-30']
        r=Intake(FixturePlanner(p)).prepare(OBJECTIVE,factory_sources(),[],SCOPE)
        self.assertFalse(r.validation['accepted'])
    def test_conflict_never_closes_runtime_case(self):
        engine,p=factory();engine.execute(p,factory_review_pack(p))
        self.assertNotIn('CLOSED',p.case.transitions);self.assertIn('unresolved',p.case.conclusions[0]['conclusion'])
    def test_contract_input_variants_retain_content(self):
        _,p=contract_control('Parties: Seller Z and Buyer Y.\n\nTerm: 3 months.\n\nCancellation: none stated.')
        self.assertTrue(any(c['claim']['value']=='Term: 3 months.' for c in p.candidates))
        self.assertEqual(p.case.outcome,'blocked')


class SourceQuestionControls(unittest.TestCase):
    def test_contract_wording_not_reasked_and_not_promoted(self):
        _,p=contract_control()
        self.assertEqual({q['attribute'] for q in p.questions},{'refund_rights','performance_obligations'})
        self.assertTrue(all(c['promotion']=='unresolved' for c in p.candidates))
        self.assertFalse(any(c['attribute']=='parties' for c in p.case.facts['established']))


class SemanticDeclarationControls(unittest.TestCase):
    def test_unbound_assumption_and_dispute_fail_closed(self):
        for name in ('assumptions','disputed_facts'):
            with self.subTest(name=name):
                p=factory_proposal(factory_sources());getattr(p,name).append(cl('Unlinked source claim',status='ASSUMED' if name=='assumptions' else 'DISPUTED',confidence=.5))
                result=Intake(FixturePlanner(p)).prepare(OBJECTIVE,factory_sources(),[],SCOPE)
                self.assertFalse(result.validation['accepted'])

"""Independent adversarial regressions, authored outside implementation context."""
import copy
import json
import unittest
from orchestration.intake import Intake, FixturePlanner, FactCandidate
from orchestration.tests.intake_fixtures import factory, factory_proposal, factory_sources, factory_review_pack, cl, OBJECTIVE, SCOPE, contract_control

class IndependentIntakeQA(unittest.TestCase):
    def prepare(self, proposal):
        return Intake(FixturePlanner(proposal)).prepare(OBJECTIVE, factory_sources(), [], SCOPE)

    def test_missing_attribute_cannot_echo_private_model_text(self):
        proposal=factory_proposal(factory_sources())
        proposal.missing_facts=[cl(dict(attribute='PRIVATE_SOURCE_PARAGRAPH_123',owner='',kind='blocking'),status='UNRESOLVED',confidence=0)]
        intake=Intake(FixturePlanner(proposal)); result=intake.prepare(OBJECTIVE,factory_sources(),[],SCOPE)
        self.assertNotIn('PRIVATE_SOURCE_PARAGRAPH_123',json.dumps(intake.public(result)))

    def test_fact_dimensions_cannot_assume_unstated_framework(self):
        proposal=factory_proposal(factory_sources())
        proposal.facts[0].dimensions['framework']='US_GAAP'
        result=self.prepare(proposal)
        self.assertFalse(result.validation['accepted'], 'Fact dimensions must agree with governed IFRS context, not silently invent a framework')

    def test_mutated_prepared_candidate_rejected_before_execution(self):
        intake,result=factory(); pack=factory_review_pack(result)
        candidate=next(c for c in result.candidates if c['id']=='ap-amount')
        candidate['claim']['value']='999999'
        # Missing a binding must not allow mutable prepared facts into Case truth.
        pack.bindings=[b for b in pack.bindings if b.fact_id!='ap-amount']
        with self.assertRaises(ValueError): intake.execute(result,pack)

    def test_same_source_metric_alias_cannot_duplicate_economics(self):
        proposal=factory_proposal(factory_sources())
        alias=copy.deepcopy(proposal.facts[0]);alias.id='alias';alias.attribute='alternate_name'
        proposal.facts.append(alias)
        self.assertFalse(self.prepare(proposal).validation['accepted'])

    def test_contract_intake_proposes_source_specific_terms(self):
        _,result=contract_control()
        attributes={c['attribute'] for c in result.candidates}
        self.assertTrue({'parties','term','consideration','billing_timing','cancellation','services'}<=attributes,
                        'Contract flagship needs meaningful proposed term extraction, not a constant generic owner-review sentence')

    def test_fact_conflicts_supplied_by_model_cannot_be_ignored(self):
        proposal=factory_proposal(factory_sources())
        proposal.facts[0].conflicts=['unresolved-source-conflict']
        result=self.prepare(proposal)
        self.assertTrue(not result.validation['accepted'] or result.candidates[0]['promotion']!='established')

    def test_prior_actual_source_cannot_be_replaced_by_fixture_comparator(self):
        from dataclasses import replace
        sources=factory_sources()
        sources=[replace(raw,payload='metric,amount\ngross_profit,123\n') if raw.id=='prior' else raw for raw in sources]
        proposal=factory_proposal(sources)
        intake=Intake(FixturePlanner(proposal));result=intake.prepare(OBJECTIVE,sources,[],SCOPE)
        try: intake.execute(result,factory_review_pack(result))
        except ValueError: return # Explicit mismatch rejection is acceptable.
        bridge=result.case.diagnostics[0]['bridge']
        self.assertNotEqual(str(bridge['change']),'-31304', 'Raw prior actual must feed comparator or be rejected; unchanged fixture result is unsupported')

    def test_management_hypothesis_has_explicit_supported_disposition(self):
        intake,result=factory();intake.execute(result,factory_review_pack(result))
        self.assertTrue(getattr(result,'hypothesis_results',[]), 'Management FX hypothesis must be tested, linked to diagnostics and explicitly dispositioned')
        hypothesis=result.hypothesis_results[0]
        self.assertEqual(hypothesis['disposition'],'REJECTED')
        self.assertFalse(hypothesis['accounting_authority'])
        self.assertTrue(hypothesis['evidence']);self.assertTrue(hypothesis['source_refs'])

    def test_secondary_diagnostic_mode_cannot_omit_analytic_owner(self):
        proposal=factory_proposal(factory_sources())
        proposal.primary_mode=cl('CLOSE_REVIEW')
        proposal.supporting_modes=[cl('DIAGNOSTIC_ANALYTICS')]
        proposal.issues=[i for i in proposal.issues if i.value['owner']!='management-accounting-analytics']
        result=self.prepare(proposal)
        self.assertFalse(result.validation['accepted'], 'Secondary/supporting diagnostic request must not silently omit Analytics')

    def test_adversarial_proposal_envelopes_fail_closed(self):
        mutations=[
            lambda p:setattr(p.facts[0].claim,'evidence',[]),
            lambda p:setattr(p.facts[0].claim,'value',True),
            lambda p:setattr(p.facts[0].claim,'value',{'amount':'600000'}),
            lambda p:p.facts[0].dimensions.update(period=['2026-12-31','2026-12-01']),
            lambda p:p.facts[0].dimensions.update(unit={'nested':'currency'}),
            lambda p:p.issues[0].value.update(owner='government-grants'),
            lambda p:p.issues[0].value.update(owner='not-an-owner'),
            lambda p:setattr(p.facts[0].claim,'status','APPROVED'),
            lambda p:setattr(p.facts[0].claim,'status','ASSUMED'),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                proposal=factory_proposal(factory_sources());mutate(proposal)
                self.assertFalse(self.prepare(proposal).validation['accepted'])

    def test_inferred_numeric_fact_never_established(self):
        proposal=factory_proposal(factory_sources());proposal.facts[0].claim.status='INFERRED';proposal.facts[0].confirmation_required=True
        result=self.prepare(proposal);self.assertTrue(result.validation['accepted'])
        self.assertEqual(result.candidates[0]['promotion'],'unresolved')

    def test_context_candidates_preserve_approved_records(self):
        proposal=factory_proposal(factory_sources());proposal.context_candidates['framework']=cl('US_GAAP')
        records=[dict(attribute='framework',value='IFRS',status='APPROVED')];before=copy.deepcopy(records)
        result=Intake(FixturePlanner(proposal)).prepare(OBJECTIVE,factory_sources(),records,SCOPE)
        self.assertEqual(records,before);self.assertTrue(result.memory_candidates[0]['conflict'])
        self.assertEqual(result.memory_candidates[0]['status'],'PROPOSED')

    def test_known_context_question_is_suppressed(self):
        intake,result=factory()
        self.assertNotIn('framework',{q['attribute'] for q in result.questions})

    def test_missing_owner_bindings_do_not_default(self):
        intake,result=factory();pack=factory_review_pack(result)
        pack.bindings=[b for b in pack.bindings if b.owner!='accounts-payable']
        with self.assertRaises(ValueError):intake.execute(result,pack)

    def test_untrusted_raw_inputs_are_inert_or_rejected(self):
        from orchestration.intake import Inventory, RawSource
        bad=[RawSource('x','x.csv','csv','a,b\n1,2,3'),
             RawSource('x','x.xlsx','xlsx','not-a-workbook'),
             RawSource('x','x.json','json',[{'amount':{'script':'execute'}}]),
             RawSource('x','x.docx','normalized_document',{'blocks':[{'id':'x','text':'x','page':True}]}),
             RawSource('x','x.json','json',{'x':'v'},metadata=[])]
        for raw in bad:
            with self.subTest(format=raw.format),self.assertRaises((ValueError,TypeError,AttributeError)):Inventory([raw])
        inv=Inventory([RawSource('x','../../private.csv','csv','formula\n=1+1')])
        self.assertEqual(next(iter(inv.fields().values()))['value'],'=1+1')

    def test_source_lineage_tampering_is_detected(self):
        intake,result=factory();pack=factory_review_pack(result)
        result._inventory.extractions['ap'].fields['ap:2']['location']['row']=999999999999
        with self.assertRaises(ValueError):intake.execute(result,pack)

    def test_public_excludes_raw_document_and_internal_metadata(self):
        intake,result=factory();intake.execute(result,factory_review_pack(result))
        from interfaces.public_output import ROUTES
        for route in ROUTES:
            public=json.dumps(intake.public(result,route))
            for token in ('FX is the main reason margin is down','source_lineage','fingerprint','reviewer_signoff','Synthetic controlled export'):
                self.assertNotIn(token,public)

    def test_conflicted_intake_never_transitions_closed(self):
        intake,result=factory();intake.execute(result,factory_review_pack(result))
        self.assertEqual(result.case.outcome,'partial')
        self.assertEqual(result.case.status,'DOCUMENTED')
        self.assertNotIn('CLOSED',result.case.transitions)
        self.assertIn('CHALLENGE',result.case.transitions)
        self.assertTrue(any(q.get('attribute')=='factory_labour' for q in result.case.open_questions))
        self.assertEqual(result.case.conclusions[0]['status'],'partial')

    def test_huge_source_record_identity_is_rejected(self):
        from orchestration.intake import Inventory, RawSource
        with self.assertRaises(ValueError):Inventory([RawSource('x','x.json','json',[{'record_id':'x'*121,'amount':'1'}])])

    def test_row_currency_conflict_cannot_promote_metadata_currency(self):
        from dataclasses import replace
        sources=factory_sources()
        asset=next(raw for raw in sources if raw.id=='assets')
        payload=copy.deepcopy(asset.payload);payload[0]['currency']='EUR'
        sources=[replace(raw,payload=payload) if raw.id=='assets' else raw for raw in sources]
        intake=Intake(FixturePlanner(factory_proposal(sources)));result=intake.prepare(OBJECTIVE,sources,[],SCOPE)
        self.assertTrue(not result.validation['accepted'] or next(c for c in result.candidates if c['id']=='asset-cost')['promotion']!='established')

if __name__=='__main__': unittest.main()

"""Independent adversarial Group Accounting contracts; no production approval creation.

Synthetic approvals originate only in controlled repository fixtures. Rejection
assertions express required integrity properties and remain red until remediated.
"""
import copy
import unittest
from orchestration.runtime import Case, Graph, Node
from orchestration.result_bindings import validate_receipts
from orchestration.period_selection import validate_activity
from orchestration.scopes import execution_scopes
from orchestration.tests.group_fixtures import owner_cases, SCOPE, SPAN
from orchestration.tests.fixtures import completed


class GroupIndependentContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=owner_cases()

    def setup_graph(self, owners):
        g=Graph()
        for pkg, source in owners.items():
            node=Node(pkg,'independent review',pkg,'supplied native source',source['entity'],'IFRS',SPAN)
            node.status='complete';node.result=completed(pkg,self.baseline[pkg])
            node.dependencies=[r['producer'] for r in source.get('qualified_owner_results',[])]
            g.add(node)
        return g,Case('independent-contract','Review group accounting')

    def validate(self, owners, pkg):
        g,c=self.setup_graph(owners)
        validate_receipts(g.nodes[pkg],g,owners,c)
        return c

    def test_clean_native_receipts(self):
        for pkg in self.baseline:self.validate(self.baseline,pkg)
        validate_activity(self.baseline['foreign-currency'])

    def test_scope_currency_contamination_rejected(self):
        scope=copy.deepcopy(SCOPE);scope['execution_scopes'][0]['currency']='USD'
        with self.assertRaises(ValueError):execution_scopes(scope)

    def test_stale_specialist_result_rejected(self):
        owners=copy.deepcopy(self.baseline)
        next(r for r in owners['consolidation']['qualified_owner_results'] if r['semantic']=='translated_population')['result']['calculations']['translation']['closing_cta']='-999'
        with self.assertRaises(ValueError):self.validate(owners,'consolidation')

    def test_source_dimension_substitution_rejected(self):
        owners=copy.deepcopy(self.baseline)
        owners['consolidation']['qualified_owner_results'][0]['source_dimensions'][0]='Other entity'
        with self.assertRaises(ValueError):self.validate(owners,'consolidation')

    def test_omitted_all_required_consolidation_receipts_rejected(self):
        owners=copy.deepcopy(self.baseline);owners['consolidation'].pop('qualified_owner_results')
        with self.assertRaises(ValueError):self.validate(owners,'consolidation')

    def test_omitted_one_required_consolidation_receipt_rejected(self):
        owners=copy.deepcopy(self.baseline);owners['consolidation']['qualified_owner_results'].pop()
        with self.assertRaises(ValueError):self.validate(owners,'consolidation')

    def test_omitted_acquisition_activity_selection_rejected(self):
        source=copy.deepcopy(self.baseline['foreign-currency']);source.pop('activity_selection')
        with self.assertRaises(ValueError):validate_activity(source)

    def test_effective_date_must_match_actual_acquisition_date(self):
        owners=copy.deepcopy(self.baseline)
        owners['business-combinations']['acquisition']=dict(owners['business-combinations']['acquisition'],date='2026-06-01')
        # Both source windows and translated profit still assert July cutoff.
        with self.assertRaises(ValueError):self.validate(owners,'foreign-currency')

    def test_translation_operation_entity_must_match_owner(self):
        owners=copy.deepcopy(self.baseline)
        owners['foreign-currency']['translation']['operation_id']='Other operation'
        with self.assertRaises(ValueError):self.validate(owners,'foreign-currency')

    def test_translation_gross_pl_ties_to_selected_source_population(self):
        source=copy.deepcopy(self.baseline['foreign-currency'])
        for row in source['translation']['tb']:
            if row['id']=='sub revenue':row['balance']='-1250'
            if row['id']=='sub expense':row['balance']='1150'
        # Profit remains 100 and TB remains balanced, but gross PL differs by 1000.
        with self.assertRaises(ValueError):validate_activity(source)

    def test_nci_oci_receipt_must_bind_actual_nci_schedule(self):
        owners=copy.deepcopy(self.baseline)
        owners['consolidation']['nci'][0]['adjusted_oci']='0'
        # Unconsumed specialist_receipts.nci_oci remains -21, concealing error.
        with self.assertRaises(ValueError):self.validate(owners,'consolidation')

    def test_impairment_receipt_must_bind_posting_or_qualified_cgu(self):
        owners=copy.deepcopy(self.baseline)
        owners['consolidation']['entities'][1]['balances']['goodwill']='999'
        # Synthetic scalar loss receipt is unchanged; carrying source is severed.
        with self.assertRaises(ValueError):self.validate(owners,'consolidation')

    def test_preacquisition_profit_inclusion_rejected(self):
        source=copy.deepcopy(self.baseline['foreign-currency'])
        source['activity_selection']['included_ids']=['pre','post']
        source['activity_selection']['included_profit']='250'
        with self.assertRaises(ValueError):validate_activity(source)


    def test_material_component_and_attribution_receipts_cannot_be_omitted(self):
        for owner,semantic in [('asset-impairment','goodwill_carrying'),
                               ('financial-statements','nci_profit'),('financial-statements','nci_oci'),
                               ('management-accounting-analytics','post_acquisition_contribution'),
                               ('management-accounting-analytics','group_profit'),
                               ('management-accounting-analytics','entity_contribution_population')]:
            with self.subTest(owner=owner,semantic=semantic):
                owners=copy.deepcopy(self.baseline)
                self.assertTrue(any(r['semantic']==semantic for r in owners[owner]['qualified_owner_results']))
                owners[owner]['qualified_owner_results']=[r for r in owners[owner]['qualified_owner_results'] if r['semantic']!=semantic]
                with self.assertRaisesRegex(ValueError,'Mandatory specialist result receipt omitted'):
                    self.validate(owners,owner)


class GroupIndependentEndToEnd(unittest.TestCase):
    """Exercise runtime and source intake, beyond isolated architecture validators."""
    @classmethod
    def setUpClass(cls):
        from orchestration.tests import group_fixtures as gf
        cls.gf=gf
        sources=gf.group_sources(True)
        cls.intake=gf.Intake(gf.FixturePlanner(gf.group_proposal(sources)))
        cls.prepared=cls.intake.prepare(gf.OBJECTIVE,sources,[],gf.SCOPE)
        if not cls.prepared.validation['accepted']:raise AssertionError(cls.prepared.validation)
        cls.pack=gf.group_review_pack(cls.prepared)
        cls.request=copy.deepcopy(cls.pack.request)

    def cao(self):
        from orchestration.runtime import CAO
        from orchestration.intake.preparation import GovernedPlanner
        return CAO(GovernedPlanner(self.prepared._proposal,self.prepared.candidates,self.prepared.questions))

    def owners(self,request):
        from orchestration.planning import FACT_ADAPTERS
        return {FACT_ADAPTERS[k][0]:v for k,v in request['facts'].items()}

    def rejected(self, request):
        from orchestration.runtime import CAO
        case=self.cao().run(request)
        self.assertNotEqual(case.outcome,'complete',{'status':case.status,'open_questions':case.open_questions})
        self.assertNotEqual(case.status,'CLOSED')
        return case

    def test_clean_runtime_amounts_and_scoped_journals(self):
        from orchestration.runtime import CAO
        case=self.cao().run(copy.deepcopy(self.request))
        self.assertEqual((case.outcome,case.status),('complete','CLOSED'))
        cons=next(n for n in case.workplan_nodes if n['selected_skill']=='consolidation')
        self.assertEqual(str(cons['result']['calculations']['nci'][0]['closing']),'176.00')
        self.assertEqual(str(cons['result']['calculations']['equity']['profit']),'285')
        self.assertTrue(case.journal_ownership_ledger)
        for row in case.journal_ownership_ledger:
            self.assertEqual(row['target_entity'],'Group')
            if row['posting']:self.assertEqual(row['source_entity'],'Group')
        self.assertTrue(any(not r['posting'] for r in case.journal_ownership_ledger))

    def test_25_categories_runtime_rejects_unsupported_or_contaminated_inputs(self):
        # Fresh source mutations retain original approvals: exact-case governance
        # itself must reject them before any contaminated financial conclusion.
        # Separate source-document attacks below regenerate fixture approvals.
        def owner_mutation(pkg,path,value):
            def mutate(r):
                from orchestration.runtime import at
                at(self.owners(r)[pkg],path[:-1])[path[-1]]=value
            return mutate
        def journal_mutation(path,value):
            def mutate(r):
                from orchestration.runtime import at
                at(r['source_assembly_journals'],path[:-1])[path[-1]]=value
            return mutate
        attacks=[
            ('01-control-perimeter',owner_mutation('consolidation',['entities',1,'control','substantive_power'],False)),
            ('02-framework-control',owner_mutation('consolidation',['entities',1,'control','model'],'VIE')),
            ('03-acquisition-date',owner_mutation('business-combinations',['acquisition','date'],'2026-06-01')),
            ('04-PPA',owner_mutation('business-combinations',['consideration','cash'],'900')),
            ('05-NCI-basis',owner_mutation('business-combinations',['nci','method'],'proportionate')),
            ('06-pre-post-acquisition',owner_mutation('foreign-currency',['activity_selection','included_ids'],['pre','post'])),
            ('07-FX-rate',owner_mutation('foreign-currency',['translation','closing_rate'],'0.7')),
            ('08-CTA',owner_mutation('consolidation',['cta_bridge','translation'],'0')),
            ('09-goodwill-currency',owner_mutation('foreign-currency',['currency','functional'],'EUR')),
            ('10-IC-reconciliation',owner_mutation('intercompany-accounting',['pairs',0,'confirmed_b'],'124')),
            ('11-IC-balance-elimination',owner_mutation('consolidation',['intercompany',0,'amount'],'101')),
            ('12-IC-transaction-duplication',lambda r:self.owners(r)['consolidation']['intercompany'].append(copy.deepcopy(self.owners(r)['consolidation']['intercompany'][0]))),
            ('13-unrealized-profit',owner_mutation('consolidation',['profit_eliminations'],[{'type':'inventory','profit':'999'}])),
            ('14-impairment',owner_mutation('asset-impairment',['valuation','fv_less_costs'],'100')),
            ('15-tax',owner_mutation('income-taxes',['jurisdictions',0,'differences',0,'reversal_rate'],'0.5')),
            ('16-exact-once-economic-event',lambda r:r['source_assembly_journals']['ownership'].append(copy.deepcopy(r['source_assembly_journals']['ownership'][0]))),
            ('17-entity-group-journals',journal_mutation(['evidence_journals',0,'level'],'entity')),
            ('18-entity-contamination',owner_mutation('asset-impairment',['entity'],'Other Group')),
            ('19-period-contamination',owner_mutation('foreign-currency',['reporting_period'],'2025-12-31')),
            ('20-currency-contamination',journal_mutation(['evidence_journals',0,'source_currency'],'EUR')),
            ('21-stale-result',owner_mutation('consolidation',['qualified_owner_results',1,'result','conclusion'],'substituted result')),
            ('22-reporting-disclosures',owner_mutation('financial-statements',['current_tb',0,'balance'],'999999')),
            ('23-analytics-hypothesis',owner_mutation('management-accounting-analytics',['accounts',0,'amount'],'999')),
            ('24-negative-selection',lambda r:r['facts'].update(unsupported_group_specialist={'amount':'999'})),
            ('25-incorrect-closure',lambda r:r.pop('source_assembly_journals')),
        ]
        for label,mutate in attacks:
            with self.subTest(category=label):
                request=copy.deepcopy(self.request);mutate(request);self.rejected(request)

    def test_journal_omission_doublepost_and_legal_target_require_rejection(self):
        # Reseal the synthetic review to test semantic coverage beyond stale hash.
        from orchestration.runtime import CAO,digest
        baseline=self.cao().run(copy.deepcopy(self.request))
        self.assertEqual(baseline.outcome,'complete')
        native=[dict(owner=n['selected_skill'],case_fingerprint=n['result']['case_fingerprint'],journals=n['result'].get('journal_entry_implications',[]))
                for n in baseline.workplan_nodes if n['issue']!='diagnostic accounting follow-up' and n['status']=='complete']
        for attack in ('omit-evidence','duplicate-evidence','legal-target','duplicate-group-posting','omit-group-posting','wrong-receipt-semantic','wrong-entity'):
            with self.subTest(attack=attack):
                request=copy.deepcopy(self.request);contract=request['source_assembly_journals']
                if attack=='omit-evidence':contract['evidence_journals'].pop()
                elif attack=='duplicate-evidence':contract['evidence_journals'].append(copy.deepcopy(contract['evidence_journals'][0]))
                elif attack=='legal-target':contract['target_entity']='Parent'
                elif attack=='duplicate-group-posting':contract['ownership'].append(copy.deepcopy(contract['ownership'][0]))
                elif attack=='omit-group-posting':contract['ownership'].pop()
                elif attack=='wrong-receipt-semantic':contract['evidence_journals'][0]['semantic']='acquisition_goodwill'
                elif attack=='wrong-entity':contract['evidence_journals'][0]['source_entity']='Parent'
                contract['review']['payload_fingerprint']=digest(dict(native=native,
                    assembly_case_fingerprint=next(n['result']['case_fingerprint'] for n in baseline.workplan_nodes if n['selected_skill']=='consolidation'),
                    target_entity=contract['target_entity'],posting_owner=contract['posting_owner'],evidence_journals=contract['evidence_journals'],ownership=contract['ownership']))
                self.rejected(request)

    def test_all_public_routes_are_curated(self):
        import json
        from orchestration.runtime import CAO
        from interfaces.public_output import ROUTES,INTERNAL_TOKEN
        cao=self.cao();case=cao.run(copy.deepcopy(self.request))
        self.assertEqual(case.outcome,'complete')
        for route in ROUTES:
            with self.subTest(route=route):
                public=cao.public(case,route)
                self.assertFalse(INTERNAL_TOKEN.search(json.dumps(public,default=str)))
                self.assertNotIn('reviewer_signoff',json.dumps(public))
                self.assertNotIn('qualified_source_documents',json.dumps(public))

    def test_primary_dispute_preserves_documented_partial(self):
        result=self.gf.run(False)
        self.assertEqual((result.case.outcome,result.case.status),('partial','DOCUMENTED'))

    def test_raw_documents_cannot_disagree_with_fresh_qualified_workpapers(self):
        from dataclasses import replace
        # All documents are re-fingerprinted and synthetic owners freshly signed
        # through the actual fixture intake. A matching hash is insufficient.
        attacks=[
            ('parent-tb','parent cash,1380','parent cash,9999'),
            ('sub-tb','sub revenue,-450','sub revenue,-9450'),
            ('spa','Signed completion 1 July 2026','Signed completion 1 June 2026'),
            ('appraisal','fair value USD100','fair value USD999'),
            ('policy','Subsidiary functional USD','Subsidiary functional GBP'),
            ('parent-tb','parent cash,1380','unrelated asset,1380'),
            ('parent-tb','parent expense,100\n','parent expense,100\nextra asset,999\nextra liability,-999\n'),
            ('appraisal','USD100,','USD100.99,'),
            ('valuation','900,180,700','900,0,880'),
            ('valuation','900,180,700,900,990','700,180,700,900,990'),
            ('analytics-source','285,200,85','285,300,85'),
            ('analytics-source','285,200,85','285,115,170'),
            ('ic','IC-LOAN-1,USD,0.8,1','IC-LOAN-1,EUR,0.8,1'),
            ('tax','2026-07-01,LAND-1','2026-07-01,UNRELATED-ASSET-1'),
            ('spa','No earnout, prior interest or ownership change.','Contingent earnout USD500 is payable. Parent held a prior interest USD200.'),
        ]
        for source,old,new in attacks:
            with self.subTest(source=source,mutation=new):
                matching=next(x for x in self.gf.group_sources(True) if x.id==source)
                self.assertIn(old,matching.payload)
                sources=[replace(x,payload=x.payload.replace(old,new)) if x.id==source else x for x in self.gf.group_sources(True)]
                intake=self.gf.Intake(self.gf.FixturePlanner(self.gf.group_proposal(sources)))
                prepared=intake.prepare(self.gf.OBJECTIVE,sources,[],self.gf.SCOPE)
                if not prepared.validation['accepted']:continue
                try:result=intake.execute(prepared,self.gf.group_review_pack(prepared))
                except (ValueError,AssertionError):continue
                self.assertIsNotNone(result.case)
                self.assertNotEqual(result.case.outcome,'complete','Source '+source+' contradicted freshly reviewed native workpaper but completed')
                self.assertNotEqual(result.case.status,'CLOSED')

    def test_group_postings_cannot_target_a_scope_declared_legal_entity(self):
        request=copy.deepcopy(self.request)
        request['scope']['execution_scopes'][0]['level']='entity'
        self.rejected(request)


    def test_required_source_text_assertion_cannot_be_omitted(self):
        from dataclasses import replace
        sources=[replace(x,payload=x.payload.replace('Signed completion 1 July 2026','Signed completion 1 June 2026'))
                 if x.id=='spa' else x for x in self.gf.group_sources(True)]
        intake=self.gf.Intake(self.gf.FixturePlanner(self.gf.group_proposal(sources)))
        prepared=intake.prepare(self.gf.OBJECTIVE,sources,[],self.gf.SCOPE)
        if not prepared.validation['accepted']:return
        pack=self.gf.group_review_pack(prepared);pack.text_assertions=[]
        try:result=intake.execute(prepared,pack)
        except ValueError:return
        self.assertNotEqual(result.case.outcome,'complete','Omitted required text checks concealed evidenced acquisition-date contradiction')


    def test_legal_source_scopes_cannot_be_relabelled_group_layers(self):
        for index in (1,2):
            with self.subTest(source_scope=index):
                request=copy.deepcopy(self.request)
                request['scope']['execution_scopes'][index]['level']='group'
                self.rejected(request)


    def test_fresh_review_cannot_downgrade_source_qualified_owner_to_no_manifest(self):
        from dataclasses import replace
        from additional_cases import certify
        from governance_cases import ready,refresh_release
        from orchestration.runtime import digest
        sources=[replace(x,payload=x.payload.replace('Signed completion 1 July 2026','Signed completion 1 June 2026'))
                 if x.id=='spa' else x for x in self.gf.group_sources(True)]
        intake=self.gf.Intake(self.gf.FixturePlanner(self.gf.group_proposal(sources)))
        prepared=intake.prepare(self.gf.OBJECTIVE,sources,[],self.gf.SCOPE)
        if not prepared.validation['accepted']:return
        pack=self.gf.group_review_pack(prepared)
        pack.text_assertions=[a for a in pack.text_assertions if a.source_id!='spa']
        owners=self.owners(pack.request)
        owners['business-combinations'].pop('source_semantic_controls')
        order=['income-taxes','business-combinations','foreign-currency','intercompany-accounting','asset-impairment',
               'consolidation','financial-statements','management-accounting-analytics','disclosure-management']
        # Deliberately refresh separate synthetic independent reviews, receipts,
        # imports and posting payload: stale approval must not hide this attack.
        for pkg in order:
            source=owners[pkg]
            for receipt in source.get('qualified_owner_results',[]):
                receipt['result']=completed(receipt['producer'],owners[receipt['producer']])
            for imp in source.get('imports',[]):
                imp.update(case=owners[imp['package']],result=completed(imp['package'],owners[imp['package']]))
            owners[pkg]=ready(pkg,c=refresh_release(source)) if pkg in ('management-accounting-analytics','disclosure-management') else certify(pkg,source)
        from orchestration.planning import FACT_ADAPTERS
        for family in pack.request['facts']:pack.request['facts'][family]=owners[FACT_ADAPTERS[family][0]]
        native=[dict(owner=i.value['owner'],case_fingerprint=completed(i.value['owner'],owners[i.value['owner']])['case_fingerprint'],
            journals=completed(i.value['owner'],owners[i.value['owner']]).get('journal_entry_implications',[])) for i in prepared._proposal.issues]
        contract=pack.request['source_assembly_journals']
        contract['review']['payload_fingerprint']=digest(dict(native=native,
            assembly_case_fingerprint=completed('consolidation',owners['consolidation'])['case_fingerprint'],
            target_entity=contract['target_entity'],posting_owner=contract['posting_owner'],
            evidence_journals=contract['evidence_journals'],ownership=contract['ownership']))
        try:result=intake.execute(prepared,pack)
        except ValueError:return
        self.assertNotEqual(result.case.outcome,'complete','Fresh review waived required source semantics and closed contradictory acquisition')


    def test_unrelated_rejected_hypothesis_cannot_reject_acquisition_claim(self):
        # Formatter isolation using an actually completed live group graph.
        # This does not assert approval of modified diagnostic accounting.
        case=self.cao().run(copy.deepcopy(self.request))
        self.assertEqual(case.outcome,'complete')
        self.assertTrue(case.diagnostics)
        case.diagnostics[0]['hypotheses']=[dict(id='unrelated-management-explanation',
            hypothesis='An unrelated operating explanation',disposition='REJECTED',evidence_class='bridge_attribution')]
        summary=self.cao()._synthesis(case,case.graph,self.gf.SCOPE)
        self.assertNotIn('full-year acquisition contribution claim is rejected',summary['conclusion'])


    def test_formatted_appraisal_amount_cannot_be_prefix_truncated(self):
        from dataclasses import replace
        sources=[replace(x,payload=x.payload.replace('USD100,','USD100,999,')) if x.id=='appraisal' else x
                 for x in self.gf.group_sources(True)]
        intake=self.gf.Intake(self.gf.FixturePlanner(self.gf.group_proposal(sources)))
        prepared=intake.prepare(self.gf.OBJECTIVE,sources,[],self.gf.SCOPE)
        if not prepared.validation['accepted']:return
        try:result=intake.execute(prepared,self.gf.group_review_pack(prepared))
        except (ValueError,AssertionError):return
        self.assertNotEqual(result.case.outcome,'complete','Thousands-formatted valuation was truncated to integer prefix')


class GroupIndependentNativeFX(unittest.TestCase):
    def test_translation_only_has_no_fabricated_monetary_rows(self):
        owners=owner_cases();source=owners['foreign-currency']
        self.assertEqual(source['items'],[])
        result=completed('foreign-currency',source)
        self.assertEqual(result['calculations']['transactions'],[])
        self.assertEqual(result['calculations']['monetary_fx_profit'],0)
        self.assertIn('translation',result['calculations'])

    def test_empty_transactions_cannot_authorize_disabled_translation(self):
        from core_accounting import ReviewRequired
        from orchestration.registry import production
        source=copy.deepcopy(owner_cases()['foreign-currency'])
        source['translation']['enabled']=False
        with self.assertRaisesRegex(ReviewRequired,'Empty transaction population'):
            production.load_workflow('foreign-currency').assess(source,[])

    def test_empty_nonlist_transactions_are_rejected(self):
        from core_accounting import ReviewRequired
        from orchestration.registry import production
        source=copy.deepcopy(owner_cases()['foreign-currency']);source['items']={}
        with self.assertRaisesRegex(ReviewRequired,'Empty transaction population'):
            production.load_workflow('foreign-currency').assess(source,[])


if __name__=='__main__':unittest.main()

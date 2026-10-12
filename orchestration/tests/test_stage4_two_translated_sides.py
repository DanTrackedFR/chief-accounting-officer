"""Bounded two-side contract proofs, deliberately not full Group acceptance.

Reviewed rates and books are independent controlled source inputs. The EUR2
carrying difference stays visible; these tests neither eliminate nor close it.
"""
import copy
import unittest
from orchestration.tests import stage3_fixtures as s3
from orchestration.governed_plan import observation
from orchestration.stage3 import validate_native_bindings
from additional_cases import fx, certify
from operational_cases import operational


def control():
    f=s3.build();e=f['session']
    for scope in ('ENTITY-UK','ENTITY-US'):
        s3.add_node(f,'fx-translation-'+scope,'foreign-currency',f['containers'][scope+'-OCT'],'fx')
    s3.add_node(f,'fx-reassessment','intercompany-accounting',f['containers']['GROUP-EUR-OCT'],'fx')
    for scope,role in [('ENTITY-UK','a'),('ENTITY-US','b')]:
        label='fx-translation-'+scope
        s3.add_edge(f,'fx-'+scope,label,('calculations','pairs',0,role+'_functional'))
        s3.add_edge(f,label,'fx-reassessment',('calculations','translation','translated_tb','ic loan' if role=='a' else 'fx payable'))
    s3.add_edge(f,'match-fx','fx-reassessment',('matching','classification'))
    for scope in ('ENTITY-UK','ENTITY-US'):
        n=f['nodes']['fx-'+scope]
        e.execute(n.id,observation,s3.legal_source(f,'fx',scope),'Reviewed native original FX loan')
    historical=s3.match_source(f,'fx')
    e.execute(f['nodes']['match-fx'].id,observation,historical,'Original reviewed FX classification')
    f['historical_fx']=copy.deepcopy(e.versions.current(f['nodes']['match-fx'].id).payload())
    current=s3.match_source(f,'fx');current['decision']['classification']='MATCHED'
    current['decision']['reason']='Reviewed equal USD20 original principals; different native currencies/carrying amounts retained, no Group residual disposition'
    e.execute(f['nodes']['match-fx'].id,observation,current,'Separately reviewed current bilateral principal match')
    for scope,currency,book,sign,equity,rate in [('ENTITY-UK','GBP','16',1,'-116','1'),('ENTITY-US','USD','20',-1,'-80','.9')]:
        label='fx-translation-'+scope;n=f['nodes'][label]
        c=s3.native_context(f,label,fx(n.framework));c['items']=[]
        c['currency'].update(functional=currency,ledger=currency,presentation='EUR')
        amount=str(int(book)*sign);net='116' if sign==1 else '80'
        c['translation'].update(operation_id='fx',valuation_date=n.period[1],functional_currency=currency,presentation_currency='EUR',
            tb=[dict(id='cash',balance='100',category='asset',rate=rate,memo='Supplied closing cash book/rate'),
                dict(id='ic loan' if sign==1 else 'fx payable',balance=amount,category='asset' if sign==1 else 'liability',rate=rate,memo='Exact signed original native loan'),
                dict(id='equity',balance=equity,category='equity',rate=rate,memo='Separately supplied historical capital book/rate')],
            opening_net_assets=net,opening_rate=rate,closing_rate=rate,profit='0',profit_rate=rate,other_oci='0',other_oci_rate=rate,reported_closing_net_assets=net,ownership='1')
        s3.bind(f,c,'fx-'+scope,label,('translation','tb',1,'balance'),sign)
        c['versioned_dependency_receipts']=s3.receipts(f,n.id)
        e.execute(n.id,observation,certify('foreign-currency',c),'Reviewed bounded foreign operation')
    n=f['nodes']['fx-reassessment'];c=s3.native_context(f,'fx-reassessment',operational('intercompany-accounting','IFRS'))
    c['pairs'][0].update(id='fx',transaction_id='fx',entity_a='ENTITY-UK',entity_b='ENTITY-US',currency='USD',opening_a='20',opening_b='20',confirmed_a='20',confirmed_b='20',opening_book_a='16',opening_book_b='18',book_a='16',book_b='18',gl_a='16',gl_b='18',rate_a='.8',rate_b='.9',initial_rate_a='.8',initial_rate_b='.9',recharge='0',settled_a='0',settled_b='0',date=n.period[1],approval_date=n.period[1])
    c['controls'].update(population_count=1,population_amount='20');c['conversion_economic_id']='fx';c['stage3_contract']='ORDINARY_IC_REASSESSMENT'
    s3.bind(f,c,'fx-translation-ENTITY-UK','fx-reassessment',('pairs',0,'gl_a'))
    s3.bind(f,c,'fx-translation-ENTITY-US','fx-reassessment',('pairs',0,'gl_b'),-1)
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    f['reassessment_source']=certify('intercompany-accounting',c)
    return f


class TwoTranslatedSides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=control()
    def setUp(self):self.f=copy.deepcopy(self.base);self.e=self.f['session'];self.n=self.f['nodes']['fx-reassessment'];self.c=copy.deepcopy(self.f['reassessment_source'])
    def validate(self):validate_native_bindings(self.e,self.n,self.c,self.c['versioned_dependency_receipts'])
    def test_native_two_side_reassessment_retains_difference_without_journals(self):
        v=self.e.execute(self.n.id,observation,self.c,'Reviewed bounded reassessment')
        p=v.payload();self.assertEqual(p['status'],'complete');self.assertEqual(p['journal_entry_implications'],[])
        self.assertEqual(p['calculations']['pairs'][0]['a_functional'],'16.00');self.assertEqual(p['calculations']['pairs'][0]['b_functional'],'18.00')
        self.assertEqual(self.f['historical_fx']['matching']['classification'],'FX_DIFFERENCE')
    def test_each_side_has_a_revalidated_framework_receipt(self):
        target=self.e.execute(self.n.id,observation,self.c,'Reviewed bounded reassessment')
        for scope,account in [('ENTITY-UK','ic loan'),('ENTITY-US','fx payable')]:
            source=self.e.versions.current(self.f['nodes']['fx-translation-'+scope].id)
            record=self.f['basis'].intercompany_conversion(source.version_id,target.version_id,'fx',('calculations','translation','translated_tb',account),s3.EVIDENCE)
            self.f['basis'].validate_transformation(record)
            self.assertEqual(record['source_scope'],scope)
    def test_group_dependency_requalifies_both_translated_sources(self):
        self.e.execute(self.n.id,observation,self.c,'Reviewed bounded reassessment')
        target=s3.add_node(self.f,'bounded-fx-elimination','consolidation',self.f['containers']['GROUP-EUR-OCT'],'fx')
        edge=s3.add_edge(self.f,'fx-reassessment','bounded-fx-elimination',('calculations','pairs',0,'a_functional'))
        self.f['basis'].declare(edge,producer_layer='FRAMEWORK_ADJUSTMENT',consumer_layer='GROUP_ELIMINATION',framework='IFRS',currency='EUR',semantic_metric='ordinary_reciprocal_balance',economic_id='fx',required_framework='IFRS',required_currency='EUR',evidence=s3.EVIDENCE)
        receipt=self.f['basis'].receipt(edge)
        self.f['basis'].validate(receipt,target.id)
        self.assertEqual(receipt.value,'16.00')
        # A qualified dependency is not an executed Group accounting result.
        self.assertIsNone(self.e.versions.current(target.id))
    def test_wrong_payable_sign_rejected(self):
        self.c['stage3_input_bindings'][1]['sign']=1
        with self.assertRaises(ValueError):self.validate()
    def test_swapped_native_sides_rejected(self):
        self.c['stage3_input_bindings'][0]['target_path']=['pairs',0,'gl_b'];self.c['stage3_input_bindings'][1]['target_path']=['pairs',0,'gl_a']
        with self.assertRaises(ValueError):self.validate()
    def test_omitted_payable_translation_rejected(self):
        self.c['versioned_dependency_receipts']=[r for r in self.c['versioned_dependency_receipts'] if r['producer_scope']!='ENTITY-US']
        with self.assertRaises(ValueError):self.validate()
    def test_original_principal_substitution_rejected(self):
        self.c['pairs'][0]['opening_a']='21'
        with self.assertRaises(ValueError):self.validate()
    def test_wrong_translation_economic_identity_rejected(self):
        n=self.f['nodes']['fx-translation-ENTITY-US'];self.e.sources[n.id]['translation']['operation_id']='clean'
        with self.assertRaises(ValueError):self.validate()
    def test_equal_value_different_legal_result_is_not_lineage(self):
        n=self.f['nodes']['fx-translation-ENTITY-US'];v=self.e.versions.current(n.id)
        self.e.sources[n.id]['stage3_input_bindings'][0]['dependency_id']=self.f['edges'][('clean-ENTITY-US','translation')]
        with self.assertRaises(ValueError):self.validate()
    def test_framework_receipt_sign_substitution_rejected(self):
        v=self.e.execute(self.n.id,observation,self.c,'Reviewed bounded reassessment')
        t=self.e.versions.current(self.f['nodes']['fx-translation-ENTITY-US'].id)
        r=self.f['basis'].intercompany_conversion(t.version_id,v.version_id,'fx',('calculations','translation','translated_tb','fx payable'),s3.EVIDENCE);r['input_sign']=1
        with self.assertRaises(ValueError):self.f['basis'].validate_transformation(r)

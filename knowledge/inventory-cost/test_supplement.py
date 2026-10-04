"""Author arithmetic and governance tests; independent claim review has separate tests."""
import copy
import json
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path
from retrieval import load_register,retrieve,SCOPES,PUBLIC_FIELDS
from validate_supplement import validate,validate_data,claim_hash


def reviewed_fixture():
    """Test fixture signatures are not production approval."""
    d=copy.deepcopy(load_register());d['status']='APPROVED'
    for c in d['claims']:
        c['approval_track']='DIRECT_SOURCE_CHECKED' if c['evidence_status']=='SOURCE_VERIFIED' else 'TRAINING_DATA_CHECKED'
        c['approval_review']={'reviewer':'test-fixture-independent-reviewer','date':'2026-10-04','result':'PASS','scope_and_period_checked':True,'cross_framework_checked':True,'regression_checked':True,'reviewed_hash':claim_hash(c)}
    return d

class InventoryKnowledgeTests(unittest.TestCase):
    def test_valid_register(self):
        self.assertEqual(validate()['errors'],[])
        self.assertEqual(validate()['claims'],228)
    def test_claim_framework_population(self):
        d=load_register()
        for fw in SCOPES:self.assertEqual(sum(c['framework']==fw for c in d['claims']),57)
        self.assertNotIn('TOPIC-',json.dumps(d))
    def test_reviewed_register_fails_closed(self):
        d=load_register();d['status']='REVIEWED'
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'r.json';p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):retrieve('IFRS','2026-12-31',SCOPES['IFRS'],p)
    def test_retrieval_privacy(self):
        d=reviewed_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'r.json';p.write_text(json.dumps(d))
            for fw in SCOPES:
                out=retrieve(fw,'2026-12-31',SCOPES[fw],p,decisions=['bom','recovery','lower_cost'])
                self.assertEqual(len(out),3)
                self.assertEqual(set(out[0]),set(PUBLIC_FIELDS))
                self.assertNotIn('source_note',json.dumps(out));self.assertNotIn('ChatGPT training data',json.dumps(out))
    def test_entity_scope_gate(self):
        for fw in SCOPES:
            for scope in ('company','aasb_tier2','nonprofit',''):
                with self.assertRaises(ValueError):retrieve(fw,'2026-12-31',scope)
    def test_period_gate(self):
        for start,end in [('2025-01-01','2026-06-30'),('2026-01-01','2027-01-01'),('2026-12-31','2026-01-01')]:
            with self.assertRaises(ValueError):retrieve('IFRS',end,SCOPES['IFRS'],period_start=start)
    def test_forged_or_stale_claim_approval(self):
        d=reviewed_fixture();d['claims'][0]['proposition']='Unsupported new proposition'
        self.assertTrue(any('stale claim' in x for x in validate_data(d)))
        d=reviewed_fixture();d['claims'][0]['approval_review']['reviewer']=d['author']
        self.assertTrue(any('independent approval' in x for x in validate_data(d)))
    def test_duplicate_namespace_source_invalid(self):
        d=load_register();d['claims'].append(copy.deepcopy(d['claims'][0]))
        self.assertTrue(any('Duplicate claim' in x for x in validate_data(d)))
        d=load_register();d['namespace']='CANONICAL';self.assertTrue(validate_data(d))
        d=load_register();d['claims'][0]['sources']=[{'source_kind':'MODEL_KNOWLEDGE','title':'fake','inspected':True,'locator':'invented'}]
        self.assertTrue(any('fabricated model' in x for x in validate_data(d)))
    def test_evidence_cannot_inflate(self):
        d=load_register();c=d['claims'][0];c['evidence_status']='SOURCE_VERIFIED';c['audit_required']=False;c['reference_confidence']='VERIFIED'
        self.assertTrue(any('unsupported direct' in x for x in validate_data(d)))
    def test_framework_contamination(self):
        by={(c['framework'],c['decision']):c['proposition'] for c in load_register()['claims']}
        self.assertIn('permits LIFO',by['US_GAAP','lifo']);self.assertIn('prohibited',by['UK_GAAP','lifo'])
        self.assertIn('new cost basis',by['US_GAAP','reversal']);self.assertIn('capped',by['IFRS','reversal'])
        self.assertIn('normal profit floor',by['US_GAAP','lower_cost'])
        self.assertIn('not restricted to incremental',by['IFRS','lower_cost'])
    def test_rm_wip_fg_independent_bridges(self):
        rm=D('10000')+D('5000')-D('9000');self.assertEqual(rm,D('6000'))
        wip=D('2000')+D('9000')+D('3000')+D('1500')-D('14000');self.assertEqual(wip,D('1500'))
        fg=D('4000')+D('14000')-D('11000');self.assertEqual(fg,D('7000'))
        self.assertEqual(D('16000')+D('5000')+D('4500')-D('11000'),rm+wip+fg)
    def test_under_recovery_and_normal_variance(self):
        actual,absorbed=D('1200000'),D('1050000')
        self.assertEqual(actual-absorbed,D('150000'))
        capacity_loss,normal_rate_difference=D('100000'),D('50000')
        self.assertEqual(capacity_loss+normal_rate_difference,actual-absorbed)
        wip,fg,cogs=D('.10'),D('.30'),D('.60')
        self.assertEqual(sum(normal_rate_difference*x for x in (wip,fg,cogs)),normal_rate_difference)
        self.assertEqual(normal_rate_difference*wip+normal_rate_difference*fg,D('20000'))
        self.assertNotEqual(actual-absorbed,D('20000'))
    def test_high_capacity_cannot_overcapitalize(self):
        pool,normal,actual=D('1000000'),D('10000'),D('12000')
        raw_absorption=pool/normal*actual
        self.assertEqual(raw_absorption,D('1200000'))
        allocated=min(raw_absorption,pool);self.assertEqual(allocated,pool)
        self.assertEqual(allocated/actual*actual,pool)
    def test_low_capacity_fixed_overhead(self):
        pool,normal,actual=D('1000000'),D('10000'),D('6000')
        absorbed=pool/normal*actual
        self.assertEqual(absorbed,D('600000'));self.assertEqual(pool-absorbed,D('400000'))
        self.assertNotEqual(pool/actual,pool/normal)
    def test_material_price_usage_exact_decomposition(self):
        aq,ap,sq,sp=map(D,['110','12','100','10'])
        price=aq*(ap-sp);usage=(aq-sq)*sp
        self.assertEqual(price,D('220'));self.assertEqual(usage,D('100'))
        self.assertEqual(price+usage,aq*ap-sq*sp)
    def test_labour_rate_efficiency_exact_decomposition(self):
        ah,ar,sh,sr=map(D,['52','22','50','20'])
        self.assertEqual(ah*(ar-sr),D('104'));self.assertEqual((ah-sh)*sr,D('40'))
        self.assertEqual(ah*(ar-sr)+(ah-sh)*sr,ah*ar-sh*sr)
    def test_variable_overhead_exact_decomposition(self):
        actual,ah,sh,rate=map(D,['600','110','100','5'])
        spending=actual-ah*rate;efficiency=(ah-sh)*rate
        self.assertEqual((spending,efficiency),(D('50'),D('50')))
        self.assertEqual(spending+efficiency,actual-sh*rate)
    def test_fixed_spending_volume_over_recovery(self):
        actual,budget,absorbed=map(D,['950','1000','1100'])
        spending=actual-budget;volume=budget-absorbed
        self.assertEqual(spending+volume,D('-150'))
        self.assertEqual(spending+volume,actual-absorbed)
    def test_fifo_weighted_average_lifo_differ(self):
        layers=[(D('10'),D('5')),(D('10'),D('7'))];sold=D('12')
        fifo=D('10')*D('5')+D('2')*D('7');lifo=D('10')*D('7')+D('2')*D('5')
        avg=sum(q*c for q,c in layers)/sum(q for q,c in layers)
        self.assertEqual((fifo,lifo,sold*avg),(D('64'),D('80'),D('72')))
    def test_us_market_floor_ceiling(self):
        nrv,margin,replacement,cost=map(D,['90','20','60','100'])
        market=min(nrv,max(replacement,nrv-margin));self.assertEqual(market,D('70'))
        self.assertEqual(min(cost,market),D('70'));self.assertEqual(min(cost,nrv),D('90'))
    def test_write_down_reversal_ceiling(self):
        cost,carrying,revised=map(D,['100','70','120'])
        reversal=min(cost,revised)-carrying;self.assertEqual(reversal,D('30'))
        self.assertEqual(carrying+reversal,cost)
    def test_wip_stage_cost_requires_stage_evidence(self):
        units,material_stage,conversion_stage=map(D,['100','1','.4'])
        material,conversion=units*material_stage*D('5'),units*conversion_stage*D('3')
        self.assertEqual(material+conversion,D('620'))
        self.assertNotEqual(material+conversion,units*D('8'))
    def test_normal_and_abnormal_loss_separate(self):
        issued,normal,abnormal,good=map(D,['110','5','5','100'])
        self.assertEqual(issued,normal+abnormal+good)
        cost=D('10');self.assertEqual((issued-abnormal)*cost,D('1050'))
        self.assertEqual(abnormal*cost,D('50'))
    def test_claim_local_tests_named(self):
        for c in load_register()['claims']:
            self.assertEqual(c['tests'],['test_independent_claim_qa.IndependentClaimQA.test_claim_'+c['claim_id'].replace('-','_')])
            self.assertTrue(c['limitations']);self.assertTrue(c['public_limitations'])

if __name__=='__main__':unittest.main()

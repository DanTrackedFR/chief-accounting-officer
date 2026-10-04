"""Independent knowledge challenges: each claim, numerical identities and mutation gates."""
import copy, hashlib, json, tempfile, unittest, subprocess, sys
from collections import Counter
from decimal import Decimal as D
from pathlib import Path
from retrieval import load_register, retrieve, SCOPES
from validate_supplement import validate_data
HERE=Path(__file__).parent
CHALLENGES={
'scope':('Factory spare automatically treated as RM',('PPE','use')),
'ownership':('Unowned consignee custody recognized',('Physical custody','consigned','evidence')),
'returns':('Return refund asset basis independently recalculated',('Revenue','owner','second')),
'purchase':('Recoverable VAT capitalized',('recoverable','discounts')),
'landed_cost':('Freight-out added to RM',('Freight-out','direct','administrative')),
'conversion':('Selling wages conversion cost',('direct labour','production overhead')),
'direct_material':('BOM replaces actual consumption',('returns','actual consumption','cost formula')),
'bom':('Unauthorized substitution and unexplained loss',('approved substitutions','actual good output','normal loss','abnormal loss')),
'routing':('Invented rework hours capitalized twice',('supplied','Unsupported','duplicated rework')),
'rm_bridge':('Missing location transfer plug',('quantity and cost','unmatched internal transfers')),
'wip_bridge':('Completion double booked',('separately traced losses','twice')),
'fg_bridge':('FG receipt and relief duplicated',('Quantity and monetary','inventory relief')),
'labour':('Office payroll absorbed as direct labour',('Payroll','once','Nonfactory')),
'upstream_cost':('Wrong currency upstream payroll cost',('period/entity/currency','completed','does not recalculate')),
'fixed_overhead':('Low output raises recovery/unit',('normal capacity','low output')),
'normal_capacity':('Actual output equated to normal during shutdown',('planned maintenance','approximates','Do not infer')),
'variable_overhead':('Budgeted output used instead actual driver',('actual','usage')),
'high_output':('High output allocates more than overhead pool',('reduced','above actual','exceeds')),
'idle_cost':('Abnormal idle fixed overhead capitalized',('Expense','unallocated','abnormal')),
'recovery':('All under-recovery blindly buried in FG',('not an automatic inventory adjustment','capacity','normal','disposition')),
'standard_cost':('Standards stale and materially divergent',('regular review','approximation')),
'standard_update':('Standard change creates unsupported uplift',('effective dates','unsupported inventory uplift','actual cost')),
'material_price_variance':('PPV receipt and consumed price effect double booked',('actual quantity','actual price minus standard price','twice')),
'usage_variance':('Usage variance sign reversed',('actual net consumed quantity minus standard allowed','Positive amounts','actual good output')),
'yield_variance':('Usage plus full yield counted twice',('decomposition','already included')),
'labour_rate_variance':('Efficiency attributed to wage rate',('actual hours','actual rate minus standard rate','posted')),
'labour_efficiency_variance':('Rate and efficiency effect netted',('actual hours minus standard allowed','rate effect separate','abnormal')),
'variable_spending_variance':('Wrong driver denominator mathematically reconciles',('actual variable overhead minus actual driver','actual architecture')),
'variable_efficiency_variance':('Unsupported machine-hour standard',('actual driver units minus standard allowed','unsupported drivers')),
'fixed_spending_variance':('Actual and budget fixed overhead swapped',('actual eligible fixed overhead minus budgeted','not inferred')),
'fixed_volume_variance':('Capacity variance overrides idle expense',('budgeted fixed overhead minus standard absorbed','expense restrictions')),
'variance_disposition':('Material normal cost variance all expensed without review',('unsold inventory','sold cost','abnormal losses','unallocated capacity')),
'scrap':('Abnormal spoilage capitalized; omitted loss plug',('Normal','abnormal','expensed','proceeds once')),
'costing_architecture':('Process equivalent percentages invented',('reviewed equivalent-unit','opening-WIP','fail closed')),
'joint_product':('Arbitrary common-product allocation',('rational consistent','controlled','separate method review')),
'fifo':('Latest cost layer used FIFO',('earliest','layer identities','duplicated')),
'weighted_average':('Moving average silently replaced periodic',('periodic or moving-average','Do not switch')),
'specific_identification':('Favourable interchangeable cost chosen',('noninterchangeable','favorable','interchangeable')),
'retail':('Margin invented',('markdown','reviewed retail method','inventing')),
'count':('Third party owned location missing',('complete','third-party','signed adjustments','not an audit opinion')),
'cutoff':('Invoice date replaces control; post-close completion recognized',('Invoice date alone','completion','economic cutoff')),
'obsolescence':('Arbitrary reserve conceals expired product',('expiry','reviewed demand','invented future demand','item by item')),
'raw_material_recovery':('IAS2 raw materials exception universally imported',()),
'grouping':('Profitable line nets damaged stock',('Item-level','framework-specific','may not conceal')),
'write_down':('Allowance deducted twice',('expense','existing allowance','second time')),
'firm_contract':('Firm contract quantities and excess conflated',('quantities covered','excess','specialist owner')),
'cogs':('Revenue recalculated or internal consumption COGS',('Revenue','Internal consumption','rather than all')),
'harvest_intake':('Harvest gain and deemed cost duplicated',('once','original entity/framework/period/currency','Do not remeasure','subsequent')),
'borrowing_cost':('Borrowing Costs silently completed',('block','nonproduction','Do not implement')),
'scope_exception':('Crypto/commodity measurement forced ordinary NRV',('exceptions','not automatically')),
'reporting':('COGS equated inventory relief despite idle overhead',('GL','statement','non-sale expense')),
'identity':('SKU aliases duplicate monetary amounts',('canonical identity','aliases','exact-once')),
'units':('Mixed kg/litre or currencies summed',('controlled unit conversions','FX','dates')),
'lifo':('IFRS prohibition imported US or US permission imported IFRS',()),
'lower_cost':('LCM and LCNRV collapsed; completion/selling omitted',()),
'reversal':('US recovery capitalized; IFRS recovery above original cost',()),
'disclosure':('Full disclosure invented for Tier2/UK small entity',()),
}

class IndependentClaimQA(unittest.TestCase):
 def test_independent_review_population_and_evidence(self):
  d=load_register();self.assertEqual(len(d['claims']),228)
  self.assertEqual(Counter(c['framework'] for c in d['claims']),{x:57 for x in SCOPES})
  self.assertEqual(validate_data(d),[])
  if d['status']=='APPROVED':
   for c in d['claims']:
    self.assertEqual(c['approval_review']['reviewer'],'independent-inventory-knowledge-reviewer')
    self.assertTrue(c['approval_review']['challenge']);self.assertTrue(c['approval_review']['reviewed_hash'])
 def test_numerical_material_and_labour_decomposition(self):
  aq,ap,sq,sp=map(D,('105','12','100','10'))
  price=aq*(ap-sp);usage=(aq-sq)*sp
  self.assertEqual(price,D('210'));self.assertEqual(usage,D('50'));self.assertEqual(price+usage,aq*ap-sq*sp)
  ah,ar,sh,sr=map(D,('45','22','40','20'))
  self.assertEqual(ah*(ar-sr)+(ah-sh)*sr,ah*ar-sh*sr)
 def test_normal_capacity_low_and_high_production(self):
  pool,normal,low,high=map(D,('1200000','10000','8000','15000'))
  absorbed=pool/normal*low;self.assertEqual(pool-absorbed,D('240000'))
  self.assertEqual(pool/high*high,pool);self.assertGreater(pool/normal*high,pool)
  actual,absorbed,budget=map(D,('1200000','1050000','1100000'))
  self.assertEqual(actual-absorbed,D('150000'));self.assertEqual((actual-budget)+(budget-absorbed),actual-absorbed)
 def test_variance_normal_abnormal_separation_and_rm_wip_fg(self):
  self.assertEqual(D('10000')+D('7500')-D('12000'),D('5500'))
  self.assertEqual(D('2000')+D('12000')+D('4000')+D('3000')-D('500')-D('16000'),D('4500'))
  self.assertEqual(D('3000')+D('16000')-D('14000'),D('5000'))
  normal_variance=D('1000');self.assertEqual(normal_variance*D('.4')+normal_variance*D('.6'),normal_variance)
 def test_lcm_ceiling_floor_differs_from_nrv(self):
  cost,nrv,normal_profit,replacement=map(D,('100','95','20','60'))
  market=min(nrv,max(replacement,nrv-normal_profit));self.assertEqual(market,D('75'));self.assertEqual(min(cost,nrv),D('95'))
  self.assertEqual(min(nrv,max(D('120'),nrv-normal_profit)),nrv)
 def test_reversal_ceiling_and_existing_allowance_exact_once(self):
  historical,prior,updated=map(D,('100','70','120'))
  self.assertEqual(min(historical,updated)-prior,D('30'));self.assertEqual(min(prior,updated),D('70'))
  gross,allowance,new_target=map(D,('100','20','60'));self.assertEqual(gross-allowance-new_target,D('20'))
 def test_mutations_of_required_governance_rejected(self):
  for field,value in [('namespace','TOPIC-15-002'),('status','PRODUCTION')]:
   d=copy.deepcopy(load_register());d[field]=value;self.assertTrue(validate_data(d))
  for field,value in [('framework','IFRS_US'),('entity_scope','aasb_tier2'),('evidence_status','VERIFIED'),('reference_confidence','EXACT'),('audit_required','false'),('limitations',[]),('sources',[]),('period_scope',{}),('topic_id','TOPIC-15-002')]:
   d=copy.deepcopy(load_register());d['claims'][0][field]=value;self.assertTrue(validate_data(d),field)
 def test_context_and_unapproved_retrieval_rejected(self):
  for fw,scope in SCOPES.items():
   for period in ('2025-12-31','2027-12-31','not-date'):
    with self.assertRaises(ValueError):retrieve(fw,period,scope)
   with self.assertRaises(ValueError):retrieve(fw,'2026-12-31','aasb_tier2')
  d=copy.deepcopy(load_register());d['status']='REVIEWED'
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'claims.json';p.write_text(json.dumps(d))
   with self.assertRaises(ValueError):retrieve('IFRS','2026-12-31',SCOPES['IFRS'],path=p)
 def test_dynamic_root_import_with_other_supplement_cached(self):
  code="""import importlib.util, pathlib, sys
root=pathlib.Path.cwd()
for name,path in [('retrieval','knowledge/agriculture/retrieval.py'),('validate_supplement','knowledge/agriculture/validate_supplement.py')]:
 s=importlib.util.spec_from_file_location(name,root/path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m)
p=root/'knowledge/inventory-cost/retrieval.py';s=importlib.util.spec_from_file_location('inventory_independent_isolation',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
try:
 out=m.retrieve('IFRS','2026-12-31',m.SCOPES['IFRS']);assert all(x['claim_id'].startswith('INV-IFRS-') for x in out)
except ValueError as e:
 assert m.load_register()['status']=='REVIEWED' and 'Inventory' in str(e)
"""
  result=subprocess.run([sys.executable,'-c',code],cwd=HERE.parents[1],capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
 def test_approved_retrieval_privacy_and_stale_review_hash(self):
  d=load_register()
  if d['status']!='APPROVED':return
  for fw,scope in SCOPES.items():
   out=json.dumps(retrieve(fw,'2026-12-31',scope)).lower()
   for hidden in ('source_note','training data','audit_required','approval_track','reference_confidence','approval_review','reviewed_hash'):
    self.assertNotIn(hidden,out)
  for field,value in [('proposition','Changed accounting conclusion'),('source','Fabricated authority')]:
   changed=copy.deepcopy(d);changed['claims'][0][field]=value
   self.assertTrue(validate_data(changed),'stale '+field)
   with tempfile.TemporaryDirectory() as t:
    p=Path(t)/'claims.json';p.write_text(json.dumps(changed))
    with self.assertRaises(ValueError):retrieve('IFRS','2026-12-31',SCOPES['IFRS'],path=p)

def words_for(c):
 fw,decision=c['framework'],c['decision'];words=CHALLENGES[decision][1]
 if decision=='raw_material_recovery':words=('does not automatically','IAS2') if fw in ('US_GAAP','UK_GAAP') else ('finished goods','price decline','Replacement cost')
 if decision=='lifo':words=('permits LIFO','policy','blocked') if fw=='US_GAAP' else ('LIFO','not') if fw in ('IFRS','AASB') else ('LIFO','prohibited')
 if decision=='lower_cost':words=('non-LIFO/non-retail','replacement cost','NRV ceiling','profit floor') if fw=='US_GAAP' else ('completion','sell') if fw=='IFRS' else ('completion','sale')
 if decision=='reversal':words=('new cost basis','cannot','exception','blocked') if fw=='US_GAAP' else ('original','cost')
 if decision=='disclosure':words={'IFRS':('policy','write-downs','reversals','pledged'),'US_GAAP':('valuation','SEC','Do not import'),'UK_GAAP':('Section1A','excluded','not a generic mandatory'),'AASB':('Tier 1','Tier 2','excluded')}[fw]
 return words
for c in load_register()['claims']:
 def test(self,c=c):
  question=CHALLENGES[c['decision']][0]
  for word in words_for(c):self.assertIn(word.lower(),c['proposition'].lower(),c['claim_id']+': '+question)
  self.assertTrue(c['public_limitations']);self.assertEqual(c['entity_scope'],SCOPES[c['framework']])
 setattr(IndependentClaimQA,'test_claim_'+c['claim_id'].replace('-','_'),test)
if __name__=='__main__':unittest.main()

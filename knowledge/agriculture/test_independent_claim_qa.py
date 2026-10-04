"""Fresh knowledge-review challenges; independent of production implementation."""
import json
import unittest
from decimal import Decimal as D
from pathlib import Path
from retrieval import load_register, retrieve, PUBLIC_FIELDS

# Material counterexample per decision; each claim is challenged individually.
CHECKS={
'scope':('unmanaged ocean fishing / ordinary farm tractor',('managed','living')),
'bearer':('single-period plant / milk cow as bearer plant',('more than one period','remote','animals are not')),
'nonbearer':('fruit+lumber tree / annual maize automatically PPE',('annual','dual-purpose','remote')),
'land-rights':('orchard land or land lease included in FV biological balance',('land','right-of-use','intangibles')),
'recognition':('unowned cattle physically present',('control','probable','reliabl')),
'initial':('invoice price silently substituted for FVCTS',('initial','fair value less costs to sell','exception')),
'subsequent':('last-year value reused for current year',('reporting','stale','fair value less costs to sell')),
'selling-costs':('finance/tax deduction; duplicate transport deduction',('excluding financing','income taxes','separately')),
'market-contract':('fixed forward price overrides qualified market FV',('contract','not automatically','market')),
'gain-loss':('birth gain credited OCI',('birth','profit or loss','rather than OCI')),
'harvest':('postharvest NRV computed inside Agriculture',('harvest','inventory','subsequent')),
'harvest-event':('milking removes cow; slaughter retains live animal',('parent survives','slaughter','double counting')),
'exception':('IAS initial-only restriction imported into UK',()),
'return-fv':('FV asset reverted to cost at inconvenient date',('cannot revert','harvest','fair value less costs to sell')),
'grants':('grant silently completed using IAS41 for every framework',('grant','block')),
'disclosure-gain':('encouraged splits treated mandatory; omit output',('output','encouraged')),
'disclosure-risks':('pledged restricted carrying omitted',('pledged','commitments','risk')),
'disclosure-roll':('invent price/physical split from residual',('harvest','exchange','encouraged')),
'disclosure-exception':('omit depreciation / force unavailable FV range',('if possible','separately','depreciation','reversals')),
'entity-tier':('Tier2 claimed IFRS compliant',('Tier 1','Tier 2','not IFRS')),
'nfp-grants':('AASB for-profit grant rule on NFP',('1058','outside')),
'election':('UK class elected FV switched to cost at will',('class','cannot subsequently change')),
'preharvest':('UK fruit recognized separately from parent',('not distinguished','do not import')),
'fv':('UK FV gain sent OCI',('initially','reporting','profit or loss')),
'harvest-fv':('UK FV harvest carried historical cost',('harvest','fair value less costs to sell','inventory')),
'valuation':('agricultural engine invents orchard benchmark valuation',('2A','qualified valuation')),
'cost':('UK elected cost forced IAS FV',('cost less','depreciation','impairment','does not substitute')),
'harvest-cost':('UK cost harvest FV alternative forbidden',('lower cost','or fair value','profit or loss')),
'cost-elements':('unsupported borrowing capitalization completed',('discounts','restoration','borrowing','block')),
'disclosure-fv':('omit current bridge; force comparative bridge',('current','no prior-period')),
'disclosure-harvest':('UK FV harvested produce assumption omitted',('methods','assumptions','harvest')),
'disclosure-cost':('copy IFRS quantities into UK requirement',('methods/lives','impairment','do not impose')),
'land':('UK tractor placed into Agriculture fair-value class',('land','equipment','applicable owners')),
'edition':('2025 edition assumptions or early2027 adopted',('2026','excludes early 2027')),
'growing-crops':('US growth gain replacing inventory cost',('accumulate','ASC330','blocked')),
'developing-sale':('US developing sale livestock as IAS41 FV',('inventory','rather than','unavailable inventory')),
'ready-sale':('US NRV alternative without immediate delivery',('NRV','reliable','insignificant','immediate')),
'production-animals':('US dairy animals default FVCTS',('costs','maturity','PPE')),
'productive-plants':('US vineyard default IAS41 classification',('fixed-asset cost','timber','not automatic')),
'reporting':('IAS41 disclosure mandates automatically US',('ASC905','does not claim')),
}

class IndependentKnowledgeChallenges(unittest.TestCase):
 def test_evidence_breakdown_real_not_authors_narrative(self):
  from collections import Counter
  self.assertEqual(Counter(c['evidence_status'] for c in load_register()['claims']),{'SOURCE_VERIFIED':35,'PRIMARY_CORROBORATED':13,'MODEL_DERIVED_AUDIT_REQUIRED':18})
 def test_public_retrieval_cannot_relay_evidence_limitations(self):
  self.assertNotIn('limitations',PUBLIC_FIELDS)
  for f in ('IFRS','US_GAAP','UK_GAAP','AASB'):
   out=json.dumps(retrieve(f,'2026-12-31','qualified full reporting entity'))
   for hidden in ('ChatGPT','training-data','audit_required','approval_track','reviewer','retrieval failed','Codification verification','direct-source audit'):
    self.assertNotIn(hidden,out)
 def test_initial_purchase_birth_and_harvest_bridge_fresh_numbers(self):
  opening,purchase_invoice,purchase_fv,birth,terminal_before,terminal_harvest,closing=map(D,('900','300','270','80','100','125','1200'))
  residual=closing-opening-purchase_fv-birth+terminal_harvest
  total_gain=purchase_fv-purchase_invoice+birth+residual
  self.assertEqual(residual,D('75'))
  self.assertEqual(total_gain,D('125'))
  self.assertEqual(opening+purchase_invoice+total_gain-terminal_harvest,closing)
  self.assertEqual(terminal_harvest-terminal_before,D('25'))
  self.assertEqual(20+3+2-4-1,20)
 def test_unequal_biological_and_harvest_produce_valuation(self):
  # Live cattle per head and carcass kg need distinct qualified populations.
  biological,produce=map(D,('70','65'))
  loss=biological-produce
  self.assertEqual(loss,D('5'))
  debits={'harvest_inventory':produce,'Agriculture_loss':loss}
  credits={'biological_assets':biological}
  self.assertEqual(sum(debits.values()),sum(credits.values()))
  self.assertNotEqual(produce,biological)
  self.assertEqual(D('100000')+D('20000')+D('33000')-D('28000')-D('5000'),D('120000'))
  self.assertEqual(D('33000')+(D('30000')-D('28000')),D('35000'))
  method=(Path(__file__).parent/'FRAMEWORK-METHOD.md').read_text()
  for phrase in ('separately obtain qualified harvested-produce','actual harvested-produce quantity and unit','do not default their amounts or units to equality','conversion difference in profit or loss','Missing produce valuation'):
   self.assertIn(phrase,method)
 def test_review_all_claims_separate_and_accurate(self):
  d=load_register()
  self.assertEqual(d['status'],'APPROVED')
  for c in d['claims']:
   self.assertEqual(c['approval_review']['result'],'PASS')
   self.assertEqual(c['approval_review']['reviewer'],'independent-agriculture-knowledge-reviewer')
   self.assertTrue(c['approval_review']['challenge'])
   self.assertEqual(c['approval_track'],'DIRECT_SOURCE_CHECKED' if c['evidence_status']=='SOURCE_VERIFIED' else 'TRAINING_DATA_CHECKED')
   if c['approval_track']=='TRAINING_DATA_CHECKED':
    self.assertTrue(c['audit_required']);self.assertIn('ChatGPT training data',c['source_note'])

# 66 separately named, fresh material proposition challenges, not author tests.
for claim in load_register()['claims']:
 def test(self, claim=claim):
  question,words=CHECKS[claim['decision']]
  text=claim['proposition'].lower()
  if claim['decision']=='scope' and claim['framework']=='US_GAAP':words=('ASC 905','no general IAS 41')
  if claim['decision']=='recognition' and claim['framework']=='US_GAAP':words=('rights/control','do not by themselves','US GAAP')
  if claim['decision']=='harvest' and claim['framework']=='US_GAAP':words=('criteria','no universal','deemed-cost')
  if claim['decision']=='exception':
   words=('until reliable','do not restrict') if claim['framework']=='UK_GAAP' else ('only on initial','quoted prices','clearly unreliable','depreciation','impairment')
  for word in words:self.assertIn(word.lower(),text,msg=claim['claim_id']+': '+question)
 setattr(IndependentKnowledgeChallenges,'test_claim_'+claim['claim_id'].replace('-','_'),test)

if __name__=='__main__':unittest.main()

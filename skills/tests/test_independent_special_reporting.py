"""Independent reviewer counterexamples and scope checks; synthetic approvals only."""
import sys,copy,json,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from special_reporting_cases import case,ready,PACKAGES
from production import execute,load_workflow,to_public
from core_accounting import ReviewRequired

class IndependentSpecialReportingQA(unittest.TestCase):
    pass

_counter=0
def probe(pkg,label,mut):
    global _counter
    _counter+=1
    def challenge(self):
        c=case(pkg);mut(c)
        if pkg=='sec-filing-accounting':
            c['filing_review']['reviewed_release_fingerprint']=load_workflow(pkg).release_fingerprint(c)
        with self.assertRaises(ReviewRequired,msg=label):
            execute(pkg,ready(pkg,c=c))
    challenge.__doc__=label
    setattr(IndependentSpecialReportingQA,'test_independent_counterexample_%02d'%_counter,challenge)

probe('alternative-performance-measures','APM journal expense unrelated to controlled GAAP subtotal',lambda c:[j.update(expense_account='off-subtotal expense',lines=[dict(side='Dr',account='off-subtotal expense',amount=j['included_expense']),dict(side='Cr',account='liability',amount=j['included_expense'])]) for j in c['adjustment_journals']])
probe('alternative-performance-measures','APM comparative not comparable full period',lambda c:[s.update(source_period=['2025-10-01','2025-12-31']) for s in c['statements'] if s['id']=='prior']+[a.update(source_period=['2025-10-01','2025-12-31']) for a in c['adjustments'] if a['period']=='prior']+[j.update(source_period=['2025-10-01','2025-12-31']) for j in c['adjustment_journals'] if j['period']=='prior'])
probe('sec-filing-accounting','SEC duration profit tag declared instant in both actual and expected',lambda c:[t.update(period_kind='instant',expected_period_kind='instant') for t in c['tags']])
probe('held-for-sale-discontinued-operations','HFS comparative fabricated component profit without component ledger',lambda c:[r.update(component_profit='99',discontinued_profit='99',continuing_profit='1') for r in c['comparatives']])
probe('hyperinflation-accounting','Hyperinflation monetary balance from earlier date',lambda c:[i.update(measurement_date='2026-01-01') for i in c['items'] if i['kind']=='monetary'])
probe('sec-filing-accounting','SEC profit duration contexts prior arbitrary 20 years',lambda c:[s.update(source_period=['2000-01-01','2020-12-31']) for s in c['statements'] if not s['current']]+[a.update(source_period=['2000-01-01','2020-12-31']) for a in c['filing_lines'] if a['id']=='prior']+[t.update(context_period=['2000-01-01','2020-12-31']) for t in c['tags'] if t['id']=='prior'])
probe('held-for-sale-discontinued-operations','HFS cash amounts multiplied10 without independent bank tie-out',lambda c:[a.update(amount=str(__import__('decimal').Decimal(a['amount'])*10)) for a in c['cash_flows']]+[c['presentation'].update(component_cash_flows={'operating':'200','investing':'-50','financing':'0'})])
probe('held-for-sale-discontinued-operations','HFS current component fabricated profit99',lambda c:[a.update(profit_after_tax='99' if a['belongs_to_component'] else '51') for a in c['results']]+[c['presentation'].update(discontinued_profit='99',continuing_profit='51')])
probe('alternative-performance-measures','APM same definition_key hides inconsistent adjustment labels',lambda c:[a.update(label='Unexpected renamed recurring adjustment') for a in c['adjustments'] if a['period']=='prior'])
probe('alternative-performance-measures','APM same keys duplicate current adjustment rationale',lambda c:[a.update(recurring=False,described_nonrecurring=True) for a in c['adjustments'] if a['period']=='prior' and a['definition_key']=='share_compensation'])
probe('held-for-sale-discontinued-operations','HFS source statement clone30 double counted twice offset90',lambda c: c.update(results=[dict(c['results'][0]),dict(c['results'][0],id='duplicate-source-result'),dict(c['results'][1],profit_after_tax='90',source_statement=dict(c['results'][1]['source_statement'],amount='90',lines=[dict(c['results'][1]['source_statement']['lines'][0],gl_amount='-90',amount='90')]))],result_inventory=['component-result','duplicate-source-result','continuing-result'],presentation=dict(c['presentation'],discontinued_profit='60',continuing_profit='90')))
probe('held-for-sale-discontinued-operations','HFS same bank transaction counted twice',lambda c:c.update(cash_flows=c['cash_flows']+[dict(c['cash_flows'][0],id='duplicate-bank-line')],cash_flow_inventory=c['cash_flow_inventory']+['duplicate-bank-line'],presentation=dict(c['presentation'],component_cash_flows={'operating':'40','investing':'-5','financing':'0'})))
probe('held-for-sale-discontinued-operations','HFS uses assets statement as profit source',lambda c:c['current_statement'].update(metric='assets',definition='Balance sheet assets'))

class IndependentSpecialReportingScope(unittest.TestCase):
    def test_scope_privacy_and_certification_checks(self):
        ok=0;bad=[]
        def check(pkg,label,edit,block=True,fw='IFRS'):
         nonlocal ok
         c=case(pkg,fw);edit(c)
         try:r=execute(pkg,ready(pkg,fw,c));rejected=r['status']!='complete'
         except (ReviewRequired,KeyError,ValueError,TypeError) as exc: rejected=True
         if rejected==block:ok+=1
         else:bad.append((pkg,label,'unexpectedly rejected' if rejected else 'unexpectedly complete'))
        for pkg in PACKAGES:
         check(pkg,'positive',lambda c:None,False)
         check(pkg,'no own filing/posting',lambda c:c.update(requested_action='submit_EDGAR'))
         check(pkg,'source population omitted',lambda c:c.update(source_inventory=[]))
        for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
         try:execute('investment-property',dict(framework=fw,reviewer_signoff={'approved':True},resolved=True));bad.append(('investment-property',fw,'complete'))
         except ReviewRequired:ok+=1
        for pkg,method,flags in [
         ('held-for-sale-discontinued-operations','disposal_method',['measurement_requested','allocation_required','reversal_requested','completed_disposal','oci_recycling','retained_interest']),
         ('hyperinflation-accounting','inflation_method',['complete_statements_requested','monetary_gain_calculation_requested','translation_requested','consolidation_requested','journal_requested']),
         ('alternative-performance-measures','apm_method',['invented_adjustments','compliance_certification_requested','per_share_requested','definition_changed']),
         ('sec-filing-accounting','filer',['amended_filing','special_form','compliance_certification','officer_certification','audit_opinion_requested','edgar_submission_requested'])]:
         for flag in flags:check(pkg,flag,lambda c,m=method,f=flag:c[m].update({f:True}))
        for pkg in ['held-for-sale-discontinued-operations','hyperinflation-accounting']:
         for fw in ['US_GAAP','UK_GAAP']:check(pkg,fw,lambda c:None,True,fw)
        check('held-for-sale-discontinued-operations','backdate',lambda c:c['disposal_method'].update(criteria_met_date='2026-10-01'))
        check('held-for-sale-discontinued-operations','depreciation',lambda c:c['assets'][0].update(depreciation_after_classification='1'))
        check('held-for-sale-discontinued-operations','qualify small component',lambda c:c['component'].update(major_geography=False))
        check('held-for-sale-discontinued-operations','disposal gain',lambda c:c['results'][0].update(disposal_gain='1'))
        check('hyperinflation-accounting','threshold only',lambda c:c['inflation_method'].update(threshold_only=True))
        check('hyperinflation-accounting','cash indexed',lambda c:[i.update(expected_restated='50') for i in c['items'] if i['kind']=='monetary'])
        check('hyperinflation-accounting','index date',lambda c:c['indices'][0].update(index_date='2026-01-02'))
        check('hyperinflation-accounting','mixed index',lambda c:c['indices'][0].update(series='other'))
        check('alternative-performance-measures','recurring labelled nonrecurring',lambda c:c['adjustments'][1].update(described_nonrecurring=True))
        check('alternative-performance-measures','wrong jurisdiction rule',lambda c:c['regulatory_method'].update(authority_url='https://www.sec.gov/forms'))
        check('alternative-performance-measures','IFRS18 backdate',lambda c:c['apm_method'].update(mpm_effective=True))
        check('alternative-performance-measures','publication mismatch',lambda c:c['publication']['current'].update(adjusted_amount='181'))
        check('sec-filing-accounting','FPI10K',lambda c:c['filer'].update(form='10-K'))
        check('sec-filing-accounting','stale SEC review',lambda c:c['rule'].update(checked_on='2027-03-30'))
        check('sec-filing-accounting','invent deadline',lambda c:c['calendar'].update(due_date='2027-03-31'))
        check('sec-filing-accounting','wrong scale',lambda c:c['tags'][0].update(scale=3,expected_scale=3))
        check('sec-filing-accounting','wrong sign',lambda c:c['tags'][0].update(sign=-1,expected_sign=-1))
        check('sec-filing-accounting','wrong unit',lambda c:c['tags'][0].update(unit='shares',expected_unit='shares'))
        check('sec-filing-accounting','disclosure failure',lambda c:c['filing_review'].update(disclosure_controls_complete=False))
        for pkg in PACKAGES:
         c=ready(pkg);c['reviewer_signoff']['case_fingerprint']='stale'
         r=execute(pkg,c)
         if r['status']=='partial':ok+=1
         else:bad.append((pkg,'stale reviewer','not partial'))
         c=ready(pkg);c['private_source_notes']='Source: ChatGPT training data; internal-reviewer/hash';c=ready(pkg,c=c);r=execute(pkg,c)
         for route in ['answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export']:
          try:out=to_public(r,route)
          except ReviewRequired:continue
          if 'private_source_notes' in json.dumps(out,default=str) or 'internal-reviewer/hash' in json.dumps(out,default=str):bad.append((pkg,'privacy '+route,'leaked'))
          else:ok+=1
        self.assertFalse(bad)
        self.assertEqual(ok,92)

    def test_stale_knowledge_and_implementation(self):
        original=Path.read_bytes;ok=0
        for pkg in PACKAGES:
         c=ready(pkg);target=next(d['path'] for d in c['knowledge_review']['documents'] if d['path'].endswith('.md'))
         def changed_doc(p,*a,**k):return original(p,*a,**k)+(b'\nchanged' if str(p).endswith(target) else b'')
         with patch.object(Path,'read_bytes',changed_doc):
          try:execute(pkg,c);raise AssertionError('knowledge stale accepted '+pkg)
          except ReviewRequired:ok+=1
         c=ready(pkg)
         def changed_impl(p,*a,**k):return original(p,*a,**k)+(b'\n# changed implementation' if str(p).endswith('skills/special_reporting.py') else b'')
         with patch.object(Path,'read_bytes',changed_impl):
          r=execute(pkg,c);assert r['status']=='partial',(pkg,r['status']);ok+=1
        self.assertEqual(ok,8)

class IndependentOwnerAdapterQA(unittest.TestCase):
    def test_completed_statement_owner_supports_component_partition_and_rejects_contradiction(self):
        from additional_cases import reporting,certify
        from operational_cases import approved
        c=case('held-for-sale-discontinued-operations')
        owner=reporting();owner['jurisdiction']=c['jurisdiction']
        owner=certify('financial-statements',owner)
        actual=execute('financial-statements',owner)
        self.assertEqual(actual['status'],'complete')
        self.assertEqual(actual['calculations']['current']['profit'],__import__('decimal').Decimal('200'))
        c['current_statement']['amount']='200'
        c['current_statement']['lines'][1].update(gl_amount='-170',amount='170')
        c['results'][1]['profit_after_tax']='170'
        c['results'][1]['source_statement']['amount']='170'
        c['results'][1]['source_statement']['lines'][0].update(gl_amount='-170',amount='170')
        c['presentation']['continuing_profit']='170'
        c['imports']=[approved('actual-statements',package='financial-statements',case=owner,result=actual,mode='evidence_only')]
        result=execute('held-for-sale-discontinued-operations',ready('held-for-sale-discontinued-operations',c=c))
        self.assertEqual(result['status'],'complete')
        self.assertEqual(result['calculations']['discontinued_profit'],__import__('decimal').Decimal('30'))
        c['current_statement']['amount']='201'
        c['current_statement']['lines'][1].update(gl_amount='-171',amount='171')
        c['results'][1]['profit_after_tax']='171'
        c['results'][1]['source_statement']['amount']='171'
        c['results'][1]['source_statement']['lines'][0].update(gl_amount='-171',amount='171')
        c['presentation']['continuing_profit']='171'
        with self.assertRaises(ReviewRequired):
            execute('held-for-sale-discontinued-operations',ready('held-for-sale-discontinued-operations',c=c))

if __name__=="__main__":unittest.main()

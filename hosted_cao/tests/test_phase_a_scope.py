"""Phase A scope gate through real authenticated HTTP, no mocked owner."""
from hosted_cao.tests.test_presumed_engineering_qa import IndependentPresumedEngineeringQA, synthetic_case, supplied

class PhaseAScope(IndependentPresumedEngineeringQA):
    # Reuse transport/fixture only, not inherited test population.
    pass
for _name in list(dir(IndependentPresumedEngineeringQA)):
    if _name.startswith('test_'):setattr(PhaseAScope,_name,None)

def scope_matrix(self):
    fields=('entity','jurisdiction','framework','period_start','reporting_period','functional_currency')
    for field in fields:
        for i,value in enumerate(('MISSING','', '   ', None, 42, [], {})):
            with self.subTest(field=field,value=value):
                c=synthetic_case(count=2)
                if value=='MISSING':c.pop(field)
                else:c[field]=value
                c['assets'][0].pop('ready_date')
                cid=self.start(rid=field+str(i))
                status,r=self.call('submit',case_id=cid,evidence=supplied(case=c))
                self.assertEqual(status,422,r); self.assertEqual(r['error']['code'],'identity_conflict')
                paths={x['field_path'] for x in r['error']['requirements']}
                self.assertIn('evidence.facts.machinery.'+field,paths)
                self.assertIn('evidence.facts.machinery.assets[1].ready_date',paths)
                self.assertFalse((self.workspace/'requests'/(field+str(i))/'evidence.json').exists())
                self.assertFalse(r['public_result'].get('journals'))
                self.assertTrue(self.call('status',case_id=cid)[1]['ok'])
PhaseAScope.test_scope_matrix=scope_matrix

def aggregate(self):
    c=synthetic_case(count=1)
    for field in ('entity','jurisdiction','framework','period_start','reporting_period','functional_currency'):c.pop(field)
    cid=self.start();status,r=self.call('submit',case_id=cid,evidence=supplied(case=c))
    self.assertEqual(status,422); self.assertEqual(len(r['error']['requirements']),6)
PhaseAScope.test_aggregate=aggregate
# Prevent unittest discovering the imported base a second time.
del IndependentPresumedEngineeringQA

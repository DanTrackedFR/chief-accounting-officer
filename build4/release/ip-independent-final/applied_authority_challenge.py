"""Independent post-freeze actual-code method-authority challenge; synthetic only."""
from production import assess_case, canonical_knowledge, PACKAGES, case_fingerprint
from investment_property_cases import ready

count = 0
for fw, model, route, mixed in [
    ('IFRS','fair_value','hold','none'),
    ('IFRS','cost','initial','none'),
    ('AASB','cost','hold','none'),
    ('UK_GAAP','group_cost','disposal','none'),
    ('US_GAAP','cost','hold','none'),
    ('IFRS','fair_value','transfer_out_fv','none'),
    ('IFRS','cost','transfer_in_cost','none'),
    ('IFRS','fair_value','hold','separable'),
]:
    claims,_=canonical_knowledge(PACKAGES['investment-property'][1],fw)
    required={'definition','owner_use','subsequent_policy','owner_boundaries','lineage','disclosures'}
    required |= {'fair_value','fv_movement','fv_disclosure'} if model=='fair_value' else {'cost_model','cost_disclosure'}
    if route=='initial':required|={'initial_recognition','initial_cost'}
    if route=='disposal':required.add('disposal')
    if route.startswith('transfer'):required|={'change_use','fv_transfer_out' if route=='transfer_out_fv' else 'cost_transfer'}
    if mixed!='none':required.add('mixed_use')
    for missing in sorted(required):
        c=ready(fw,model,route,mixed)
        c['knowledge_review']['applied_claim_ids']=[x['claim_id'] for x in claims if x['decision']!=missing]
        c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
        r=assess_case('investment-property',c)
        assert r['status']=='blocked',(fw,model,route,missing,r['status'])
        assert 'substantive route authority' in r['conclusion'],r['conclusion']
        assert not r['journal_entry_implications']
        count+=1
print(f'PASS {count} independently recertified method-authority omissions; no released journals')
scope_count=0
for fw in ('AASB','UK_GAAP','US_GAAP'):
    c=ready(fw,'cost' if fw=='US_GAAP' else 'fair_value')
    c['jurisdiction']='NL';c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
    r=assess_case('investment-property',c)
    assert r['status']=='blocked' and not r['journal_entry_implications'],r
    assert 'jurisdiction' in r['conclusion'],r['conclusion']
    scope_count+=1
for compilation in ('2026 effective compilation','AASB140_JAN2027'):
    c=ready('AASB');c['aasb_compilation']=compilation
    c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
    r=assess_case('investment-property',c)
    assert r['status']=='blocked' and not r['journal_entry_implications'],r
    assert 'compilation' in r['conclusion'],r['conclusion']
    scope_count+=1
print(f'PASS {scope_count} independently recertified wrong-jurisdiction/compilation attacks')

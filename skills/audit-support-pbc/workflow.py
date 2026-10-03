"""Management evidence production, not auditor procedures or conclusions."""
from governance_accounting import *
KEYS=('requests','request_source','documents','imports','samples','sample_inventory','auditor_selection','queries','query_inventory','governance_method')
def assess(c,claims):
    rs,docs=start(c,'requests');p=c['governance_method']
    if any(flag(p,k) for k in ('evidence_sufficiency_asserted','auditor_independence_determined','confirmation_control_requested','audit_adjustments_requested','auditor_signoff_requested')):raise ReviewRequired('Auditor judgment/selection/confirmation and adjustment accounting are outside management support')
    texts(p,'assurance_regime','engagement_scope_memo','currency')
    independent_population(c,'request_source',rs,('purpose','account','assertion','due_date','source_doc','ledger_doc'))
    used=set();semantic=set();count=0;gross=ZERO;open_items=[]
    for r in rs:
        texts(r,'purpose','account','assertion','accountable_owner','response_memo','submission_version')
        if r['submission_version']!=r['version']:raise ReviewRequired('Submission version differs from reviewed request')
        identity=(r['purpose'],r['source_doc'],r['account'])
        if identity in semantic:raise ReviewRequired('Duplicate semantic PBC request')
        semantic.add(identity)
        a=doc(docs,r['source_doc']);b=doc(docs,r['ledger_doc'])
        if a['currency']!=b['currency'] or a['currency']!=p['currency']:raise ReviewRequired('PBC source/ledger currency mismatch')
        records=rows(a['content']['records'],False);books=rows(b['content']['records'],False)
        inventory(a['content'],'inventory',records);inventory(b['content'],'inventory',books)
        by={x['id']:x for x in books}
        if set(by)!={x['id'] for x in records}:raise ReviewRequired('PBC full source population does not reconcile to actual books')
        total=ZERO
        for x in records:
            if x!=by[x['id']]:raise ReviewRequired('PBC source file contradicts ledger record')
            if x['account']!=r['account']:raise ReviewRequired('PBC account/assertion scope mismatch')
            key=(r['account'],a['currency'],x['id'])
            if key in used:raise ReviewRequired('PBC evidence counted twice')
            used.add(key);total+=dec(x['amount']);gross+=abs(dec(x['amount']));count+=1
        exact(r['amount'],total,'PBC source subtotal')
        if r.get('owner_import'):owner_assertion(c,r)
        state=enum(r,'state',{'released','open'})
        if state=='open':open_items.append('Unresolved management PBC evidence request')
    selections=c['auditor_selection'];approval(selections,c);texts(selections,'selection_memo','selection_version')
    selected=rows(selections['records']);inventory(selections,'inventory',selected)
    samples=pack(c,'samples','sample_inventory');by={x['id']:x for x in selected}
    if set(by)!={s['id'] for s in samples}:raise ReviewRequired('Management cannot omit/substitute auditor-selected sample IDs')
    requests={r['id']:r for r in rs}
    for s in samples:
        if any(s[k]!=by[s['id']][k] for k in ('request_id','record_id')):raise ReviewRequired('Auditor selection changed')
        if s['request_id'] not in requests:raise ReviewRequired('Sample outside actual PBC request')
        req=requests[s['request_id']];records=doc(docs,req['source_doc'])['content']['records']
        matched=[x for x in records if x['id']==s['record_id']]
        if len(matched)!=1:raise ReviewRequired('Sample not in complete original population')
        if not flag(s,'evidence_available'):
            open_items.append('Auditor-selected evidence unavailable; selection retained and escalated')
        else:
            support_source=doc(docs,s['support_doc'])
            if support_source['currency']!=p['currency']:raise ReviewRequired('Sample support currency mismatch')
            support=support_source['content']
            if support!=matched[0]:raise ReviewRequired('Selected sample support differs from original record')
    queries=pack(c,'queries','query_inventory')
    for q in queries:
        texts(q,'question','accountable_owner','response_memo','impact_memo');enum(q,'kind',{'factual','accounting'})
        if q['kind']=='accounting':
            imp=accounting_owner(c,q['owner_import'])
            if q['accounting_conclusion']!=imp['result']['conclusion']:raise ReviewRequired('Query response alters actual accounting owner conclusion')
        else:doc(docs,q['evidence_doc'])
        if not flag(q,'closed'):open_items.append('Open management audit query')
    review_release(c,KEYS)
    return output(c,'Management PBC and audit-support evidence workpaper reconciled',dict(request_count=len(rs),source_record_count=count,gross_source_amount=gross,sample_count=len(samples),query_count=len(queries),auditor_evidence_sufficiency_certified=False),['Management-side evidence support only; auditor retains procedures, independent selection, confirmation control, sufficiency, independence and opinion. No accounting position or adjustment is created or reposted.'],open_items)

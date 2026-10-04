"""Policy/memo version governance cannot create substantive accounting authority."""
from governance_accounting import *
KEYS=('policies','policy_source','history','history_inventory','documents','imports','governance_method')
SECTIONS=('issue','facts','guidance','analysis','alternatives','judgments','assumptions','conclusion','implementation','uncertainties')
def assess(c,claims):
    rs,docs=start(c,'policies');p=c['governance_method']
    if any(flag(p,k) for k in ('autonomous_policy_selection','transition_calculation_requested','overwrite_history','invented_citations')):raise ReviewRequired('Policy documentation cannot supply missing authority or replace accounting owner')
    independent_population(c,'policy_source',rs,('policy_id','policy_version','effective_from','effective_to','owner_import','memo_doc','policy_change','owner_result_fingerprint','result_path','accounting_conclusion'))
    history=pack(c,'history','history_inventory');groups={};seen=set()
    for h in history:
        texts(h,'policy_id','policy_memo','body_hash')
        n=h['policy_version']
        if type(n) is not int or n<1 or (h['policy_id'],n) in seen:raise ReviewRequired('Policy history version duplicate or invalid')
        seen.add((h['policy_id'],n));groups.setdefault(h['policy_id'],[]).append(h)
        d=doc(docs,h['memo_doc'])
        if h['body_hash']!=d['content_hash']:raise ReviewRequired('Published policy history was overwritten')
    if set(groups)!={r['policy_id'] for r in rs}:raise ReviewRequired('Policy inventory/history coverage mismatch')
    if len({r['policy_id'] for r in rs})!=len(rs):raise ReviewRequired('Multiple current versions for policy')
    for id,hs in groups.items():
        hs.sort(key=lambda h:h['policy_version'])
        for n,h in enumerate(hs,1):
            if h['policy_version']!=n or h['supersedes']!=(None if n==1 else hs[n-2]['id']):raise ReviewRequired('Missing policy supersession/version history')
            if iso(h['effective_from'])>iso(h['effective_to']):raise ReviewRequired('Policy effective date inversion')
            if n>1 and iso(hs[n-2]['effective_to'])>=iso(h['effective_from']):raise ReviewRequired('Policy version overlap/backdating')
    memo_count=0
    for r in rs:
        texts(r,'policy_id','accountable_owner','implementation_memo','exception_memo')
        active=[h for h in groups[r['policy_id']] if iso(h['effective_from'])<=iso(c['period_start']) and iso(c['reporting_period'])<=iso(h['effective_to'])]
        if len(active)!=1 or any(r[k]!=active[0][k] for k in ('policy_version','effective_from','effective_to','memo_doc')):raise ReviewRequired('Wrong/stale policy version for actual reporting span')
        imp=accounting_owner(c,r['owner_import'])
        if imp['package'] in set(BATCH)|{'sec-filing-accounting','alternative-performance-measures'}:raise ReviewRequired('Governance/reporting-control package cannot create underlying accounting policy authority')
        if flag(r,'policy_change') and (imp['package']!='accounting-changes' or imp['case'].get('change',{}).get('kind')!='policy'):raise ReviewRequired('Policy change needs actual completed Accounting Changes owner')
        if r['owner_result_fingerprint']!=imp['result']['case_fingerprint'] or r['accounting_conclusion']!=imp['result']['conclusion']:raise ReviewRequired('Policy conflicts with current actual accounting owner')
        memo=doc(docs,r['memo_doc'])['content']
        if not isinstance(memo,dict):raise ReviewRequired('Structured technical memo required')
        texts(memo,*SECTIONS)
        if memo['conclusion']!=imp['result']['conclusion']:raise ReviewRequired('Polished memo cannot overwrite accounting conclusion')
        if memo['owner_result_fingerprint']!=r['owner_result_fingerprint']:raise ReviewRequired('Memo source owner stale')
        if not flag(r,'implemented') or not flag(r,'exceptions_resolved'):raise ReviewRequired('Policy implementation/exception governance incomplete')
        actual={x['claim_id']:x for x in imp['result']['evidence']}
        citations=rows(memo['citations'])
        if len({x['claim_id'] for x in citations})!=len(citations) or {x['claim_id'] for x in citations}!=set(actual):raise ReviewRequired('Memo must trace all actual applied owner claims exactly once; source limitations stay open')
        for cite in citations:
            if cite['claim_id'] not in actual:raise ReviewRequired('Citation not actual applied accounting owner claim')
            claim=actual[cite['claim_id']]
            if cite['proposition']!=claim['proposition']:raise ReviewRequired('Citation proposition changed')
            locator=cite['locator']
            if locator is not None and (claim['reference_confidence']!='VERIFIED' or locator not in claim['references']):raise ReviewRequired('Unverified/invented paragraph cannot become authority through memo')
        owner_assertion(c,r);memo_count+=1
    review_release(c,KEYS)
    return output(c,'Accounting policy and technical-memo governance workpaper reviewed',dict(current_policy_count=len(rs),retained_history_count=len(history),reviewed_memo_count=memo_count,new_accounting_authority_created=False),['Policy/memo governance only. Underlying accounting selection, estimates, policy-change transition, entries and disclosures remain with completed accounting owners; unresolved authority cannot be certified by document polish. Retain original evidence ratings and period limitations.'])

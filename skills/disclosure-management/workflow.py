"""Current qualified requirement population and source/note controls."""
from governance_accounting import *
KEYS=('requirements','requirement_source','notes','note_inventory','documents','imports','governance_method')
def assess(c,claims):
    rs,docs=start(c,'requirements');p=c['governance_method']
    if any(flag(p,k) for k in ('universal_checklist','compliance_certification','prior_year_rollforward_only','filing_requested','comparative_change_requested')):raise ReviewRequired('Checklist cannot invent requirements, certify compliance or implement comparative accounting')
    source_index=c['requirement_source'];source(c,source_index)
    texts(source_index,'requirement_version','current_scope_memo','topic_coverage_memo','authority_review_memo')
    if source_index['checked_on']!=c['execution_date'] or source_index['effective_period']!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Prior-year requirement applicability cannot silently roll forward')
    independent_population(c,'requirement_source',rs,('topic_id','requirement_key','requirement_text','owner_import','applicability_doc','applicable','owner_requirement','metric','result_path'))
    original=source_index['records']
    topic_ids=source_index['applicable_topic_inventory']
    if not isinstance(topic_ids,list) or len(set(topic_ids))!=len(topic_ids) or set(topic_ids)!={r['topic_id'] for r in original}:raise ReviewRequired('Disclosure applicable-topic population incomplete')
    manifest={t['topic_id']:t for t in json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']}
    if any(id not in manifest or manifest[id]['status']!='APPROVED' for id in topic_ids):raise ReviewRequired('Invented/unapproved disclosure topic')
    notes=pack(c,'notes','note_inventory');by={n['requirement_id']:n for n in notes}
    if len(by)!=len(notes):raise ReviewRequired('Duplicate disclosure requirement output')
    semantic=set();applicable=set();open_items=[]
    for r in rs:
        identity=(r['topic_id'],r['requirement_key'])
        if identity in semantic:raise ReviewRequired('Duplicate semantic disclosure requirement')
        semantic.add(identity);texts(r,'requirement_text','accountable_owner','applicability_memo')
        a=doc(docs,r['applicability_doc'])['content']
        if not isinstance(a,dict) or a['requirement_id']!=r['id'] or a['applicable']!=flag(r,'applicable') or a['current_source_version']!=source_index['requirement_version']:raise ReviewRequired('Requirement applicability contradicts current independent evidence')
        imp=accounting_owner(c,r['owner_import'])
        if r['topic_id'] not in PACKAGES[imp['package']][1]:raise ReviewRequired('Disclosure requirement lacks correct topic owner')
        if r['owner_requirement'] not in imp['result']['disclosures_impacted']:raise ReviewRequired('Checklist label cannot invent accounting-owner disclosure')
        if not flag(r,'applicable'):
            if not flag(a,'not_applicable_independently_reviewed'):raise ReviewRequired('Unsupported disclosure N/A conclusion')
            if dec(r['amount'])!=0 or r['id'] in by:raise ReviewRequired('N/A requirement cannot carry hidden disclosure output')
            continue
        applicable.add(r['id'])
        if r['id'] not in by:raise ReviewRequired('Applicable disclosure missing from output population')
        n=by[r['id']];texts(n,'note_location','cross_reference','narrative')
        if n['narrative']!=imp['result']['conclusion']:raise ReviewRequired('Disclosure narrative contradicts accounting owner')
        if not isinstance(r['result_path'],list) or not r['result_path'] or r['metric']!=r['result_path'][-1]:raise ReviewRequired('Disclosure metric differs from actual completed owner assertion')
        value=owner_assertion(c,r);exact(n['amount'],value,'Note to accounting owner')
        prior_doc=doc(docs,n['issued_prior_doc'])
        if prior_doc['currency']!=n['units']:raise ReviewRequired('Comparative source metadata unit mismatch')
        prior=prior_doc['content']
        comparison(c,prior['period'])
        if prior['requirement_key']!=r['requirement_key'] or prior['units']!=n['units']:raise ReviewRequired('Issued comparative source scope mismatch')
        if not flag(n,'unchanged_comparative'):raise ReviewRequired('Comparative changes need separate actual accounting method/owner bridge')
        exact(n['prior_amount'],prior['amount'],'Issued-to-displayed unchanged comparative')
        statement_doc=doc(docs,n['statement_doc'])
        if statement_doc['currency']!=n['units']:raise ReviewRequired('Statement source metadata unit mismatch')
        statement=statement_doc['content']
        if statement['metric']!=r['metric'] or statement['units']!=n['units']:raise ReviewRequired('Note/statement unit or metric contradiction')
        exact(statement['amount'],value,'Note/statement/owner tie-out')
        if not flag(n,'review_notes_closed'):open_items.append('Unresolved disclosure review note')
    if set(by)!=applicable:raise ReviewRequired('Orphan/invented note outside actual applicable requirements')
    review_release(c,KEYS)
    return output(c,'Current disclosure-management and comparative tie-out workpaper reconciled',dict(requirement_count=len(rs),applicable_count=len(applicable),note_count=len(notes),disclosure_compliance_certified=False),['Supplied qualified current requirement inventory and owner conclusions are inputs, not a universal disclosure rulebook. Unchanged comparatives only; reclassifications/restatements require accounting-owner analysis. No filing or compliance certification.'],open_items)

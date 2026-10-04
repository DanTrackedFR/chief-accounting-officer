"""Supplied accounting interface/data acceptance workpaper; never system writes."""
from final_batch_accounting import *
KEYS=('interfaces','interface_source','books','book_inventory','account_mapping','mapping_inventory','access','access_inventory','documents','document_inventory','imports','owner_links','owner_link_inventory','governance_method')
LIMITS=['Accounting source/target data-integrity workpaper only; no production migration, database/ERP write, access change or technical-completeness certification.','Mappings, accounting conclusions, control thresholds and system metadata must be independently supplied; this is not a reporting/FP&A or generic engineering engine.']
def assess(c,claims):
    rs,d=start(c,'interfaces');original(c,'interface_source',rs)
    books=pack(c,'books','book_inventory',False);maps=pack(c,'account_mapping','mapping_inventory',False);access=pack(c,'access','access_inventory')
    registry=snapshot(c,d,c['governance_method']['registry_doc']);exact_fields(registry,c,('entity','jurisdiction'),'Book registry')
    if digest(registry['books'])!=digest(books) or digest(registry['account_mapping'])!=digest(maps) or digest(registry['access'])!=digest(access):raise ReviewRequired('Actual book/master-data/access registry differs')
    systems={r[k] for r in rs for k in ('source_system','target_system')}
    if {a['system'] for a in access}!=systems:raise ReviewRequired('Full actual accounting system access population required')
    unique([(r['entity'],r['book']) for r in books],'entity/book');unique([(r['source_system'],r['source_account'],r['entity'],r['book']) for r in maps],'account mapping')
    physical=set();interfaces=set();total=ZERO;gross=ZERO;items=0;exceptions=0;open_items=[]
    for r in rs:
        texts(r,'source_system','target_system','interface_key','entity','book','currency','mapping_version','lineage_memo')
        if r['interface_key'] in interfaces:raise ReviewRequired('Aliased duplicate interface')
        interfaces.add(r['interface_key'])
        if (r['entity'],r['book']) not in {(b['entity'],b['book']) for b in books} or r['entity']!=c['entity']:raise ReviewRequired('Entity/book not in actual scoped registry')
        book=next(b for b in books if (b['entity'],b['book'])==(r['entity'],r['book']))
        if book['framework']!=c['framework'] or book['currency']!=r['currency']:raise ReviewRequired('Book reporting basis/currency contradiction')
        src=snapshot(c,d,r['source_doc'],r['currency']);dst=snapshot(c,d,r['target_doc'],r['currency']);qc=snapshot(c,d,r['control_doc'],r['currency'])
        for blob,system in ((src,r['source_system']),(dst,r['target_system'])):
            exact_fields(blob,r,('entity','book','currency','mapping_version'),'Extract scope')
            if blob['system']!=system or blob['period']!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Source/target period/system contradiction')
            inventory(blob,'inventory',rows(blob['records']))
        records={s['id']:s for s in src['records']};targets=dst['records'];unique([t['source_id'] for t in targets],'retry/source lineage')
        if {t['source_id'] for t in targets}!=set(records):raise ReviewRequired('Orphan or missing source-target record')
        for t in targets:
            s=records[t['source_id']];key=(r['source_system'],s['id'],r['entity'],r['book'])
            if key in physical:raise ReviewRequired('Aliased physical source record counted twice')
            physical.add(key)
            match=[m for m in maps if (m['source_system'],m['source_account'],m['entity'],m['book'])==(r['source_system'],s['account'],r['entity'],r['book'])]
            if len(match)!=1:raise ReviewRequired('Unmapped or duplicated account')
            m=match[0];texts(m,'target_account','mapping_memo');exact_fields(t,m,('target_account',),'Approved target account')
            if m['version']!=r['mapping_version']:raise ReviewRequired('Mapping version stale')
            if s['dimension'] not in m['allowed_source_dimensions'] or t['dimension']!=m['dimension_map'][s['dimension']]:raise ReviewRequired('Invalid accounting dimension mapping')
            if t['entity']!=r['entity'] or t['book']!=r['book'] or t['currency']!=r['currency']:raise ReviewRequired('Target accounting dimensions contradiction')
            exact(t['amount'],s['amount'],'Item-level source/target accounting');enum(t,'state',{'posted','held','rejected'})
            if t['state']!='posted':exceptions+=1;open_items.append('Held/rejected accounting records retain unresolved disposition')
            items+=1;total+=dec(s['amount']);gross+=abs(dec(s['amount']))
        exact(r['amount'],sum((abs(dec(s['amount'])) for s in records.values()),ZERO),'Independent gross interface population')
        for blob in (src,dst):
            exact(blob['signed_total'],sum((dec(v['amount']) for v in blob['records']),ZERO),'Extract signed total');exact(blob['gross_total'],sum((abs(dec(v['amount'])) for v in blob['records']),ZERO),'Extract gross total')
        posted=sum((dec(t['amount']) for t in targets if t['state']=='posted'),ZERO)
        exact(dst['gl_amount'],posted,'Subledger target/GL');exact(dst['statement_amount'],posted,'Target/statement')
        exact(qc['approved_threshold'],0,'Only exact zero-tolerance data reconciliation is executable')
        texts(qc,'threshold_basis_memo','access_memo','change_memo','quality_test_memo','fallback_memo')
        if not flag(qc,'accounting_owner_reviewed') or not flag(qc,'negative_tests_passed') or not flag(qc,'exceptions_visible'):raise ReviewRequired('Control acceptance evidence missing')
        if flag(qc,'euc_used') and (not flag(qc,'formula_version_reviewed') or flag(qc,'hidden_override')):raise ReviewRequired('Uncontrolled spreadsheet/manual override')
        if flag(qc,'ai_used') and (not flag(qc,'ai_lineage_validated') or not flag(qc,'human_accounting_decision_retained')):raise ReviewRequired('AI transformation lacks accounting lineage/authority')
        if flag(qc,'migration'):
            if src['balance_date']!=c['period_start'] or dst['balance_date']!=c['period_start']:raise ReviewRequired('Wrong opening migration date')
            exact(qc['original_opening_balance'],src['signed_total'],'Original opening balance');exact(qc['migrated_opening_balance'],dst['signed_total'],'Migrated opening balance')
            if not flag(qc,'parallel_run_reconciled') or not flag(qc,'rollback_tested'):raise ReviewRequired('Cutover accounting acceptance unproven')
        for a in access:
            if a['system'] not in {r['source_system'],r['target_system']}:continue
            if flag(a,'prepare_and_approve') or flag(a,'unapproved_access') or not flag(a,'responsibility_consistent'):raise ReviewRequired('Accounting access responsibility/control contradiction')
    if len({r['currency'] for r in rs})>1:raise ReviewRequired('Unlike currencies cannot be netted/aggregated')
    review_release(c,KEYS)
    return finalize(c,'Accounting source-to-target integrity and control acceptance workpaper',dict(interfaces=len(rs),records=items,signed_amount=total,gross_amount=gross,unresolved_records=exceptions),LIMITS,open_items)

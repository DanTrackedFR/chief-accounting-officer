from reporting_accounting import *

def assess(c,claims):
    common(c,'relationships','declarations','transactions','balances','commitments','disclosure','handoffs','relationship_inventory','counterparty_inventory','reporting_scope','kmp_compensation')
    specialist(c,'legal','Related-party legal assessment');specialist(c,'group','Consolidation');specialist(c,'pricing','Transfer Pricing')
    relations=rows(c['relationships'],False);inventory(c,'relationship_inventory',relations);declarations=rows(c['declarations'],False);inventory(c,'counterparty_inventory',declarations);relmap={r['id']:r for r in relations}
    scope=c['reporting_scope'];policy(c,scope);required(scope,'level','exemptions_review','kmp_scope','small_entity','uk_2026_disclosure_review')
    if scope['level'] not in ['separate','consolidated']:raise ReviewRequired('Reporting-entity related-party scope unresolved')
    if c['framework']=='UK_GAAP' and iso(c['period_start'])>=iso('2026-01-01') and not flag(scope,'uk_2026_disclosure_review'):raise ReviewRequired('FRS102 2026 related-party small-entity disclosure change not reviewed')
    for r in relations:
        reviewed(r,c,'relationship_evidence','identification_memo');required(r,'counterparty','kind','start','end','related','internal_group','arm_length_asserted','pricing_evidence','arm_length_approved')
        if r['kind'] not in ['parent','subsidiary','associate','joint_venture','kmp','close_family','kmp_controlled','other_reviewed']:raise ReviewRequired('Relationship type requires specialist evidence')
        if iso(r['start'])>iso(r['end']):raise ReviewRequired('Relationship dates reversed')
        flag(r,'related');flag(r,'internal_group')
        if flag(r,'arm_length_asserted'):
            texts(r,'pricing_evidence')
            if not flag(r,'arm_length_approved'):raise ReviewRequired('Arm-length assertion unsupported by independent pricing evidence')
    mapped={r['counterparty'] for r in relations}
    for d in declarations:
        reviewed(d,c,'declaration_evidence','search_memo');required(d,'related','relationship_ids')
        if not isinstance(d['relationship_ids'],list):raise ReviewRequired('Declaration relationship identifiers required')
        if flag(d,'related') and (not d['relationship_ids'] or not set(d['relationship_ids'])<=set(relmap)):raise ReviewRequired('Related declaration absent from relationship population')
        for id in d['relationship_ids']:
            if relmap[id]['counterparty']!=d['id'] or relmap[id]['related']!=d['related']:raise ReviewRequired('Relationship/declaration mismatch')
        if {r['id'] for r in relations if r['counterparty']==d['id']}!=set(d['relationship_ids']):raise ReviewRequired('Declaration omits an identified relationship')
    if not mapped<={d['id'] for d in declarations}:raise ReviewRequired('Related master lacks independent declaration coverage')
    transactions=rows(c['transactions']);balances=rows(c['balances']);commitments=rows(c['commitments']);note=rows(c['disclosure']);nmap={n['id']:n for n in note};work=[];sales=ZERO;purchases=ZERO;recs=ZERO;pays=ZERO;maximum=ZERO;eliminations=ZERO
    def relation_for(row,date):
        required(row,'relationship_id','counterparty')
        if row['relationship_id'] not in relmap:raise ReviewRequired('Source row lacks relationship assessment')
        r=relmap[row['relationship_id']]
        if r['counterparty']!=row['counterparty']:raise ReviewRequired('Source/relationship counterparty mismatch')
        related=r['related'] and iso(r['start'])<=date<=iso(r['end'])
        return r,related
    sources=transactions+balances+commitments
    if len({r['id'] for r in sources})!=len(sources) or set(nmap)!={r['id'] for r in sources}:raise ReviewRequired('Complete unique source-to-note disposition required')
    for group,rs in [('transaction',transactions),('balance',balances),('commitment',commitments)]:
        for x in rs:
            reviewed(x,c,'source_evidence','terms_memo','governance_approval');required(x,'amount','gl_amount','type','eliminated','exemption','exemption_memo')
            date=inperiod(c,x['date']) if group=='transaction' else iso(c['reporting_period']);r,related=relation_for(x,date);n=nonnegative(x['amount']);agree(x['gl_amount'],n,'Related source-to-GL')
            eliminated=flag(x,'eliminated')
            if eliminated and (scope['level']!='consolidated' or not r['internal_group']):raise ReviewRequired('Separate/external related-party amount cannot be eliminated')
            if scope['level']=='consolidated' and related and r['internal_group'] and not eliminated:raise ReviewRequired('Intragroup source must reconcile to approved elimination')
            exempt=flag(x,'exemption')
            if exempt:texts(x,'exemption_memo');specialist(c,'exemption','Related-party disclosure specialist')
            included=related and not eliminated and not exempt
            d=nmap[x['id']];reviewed(d,c,'requirement_memo');required(d,'included','amount')
            if flag(d,'included')!=included:raise ReviewRequired('Note relationship timeline/perimeter/exemption conflicts with source')
            agree(d['amount'],n if included else 0,'Related note amount')
            if eliminated:eliminations+=n
            if included:
                if group=='transaction':
                    if x['type'] not in ['sale','purchase','other']:raise ReviewRequired('Related transaction type unresolved')
                    if x['type']=='sale':sales+=n
                    if x['type']=='purchase':purchases+=n
                elif group=='balance':
                    if x['type'] not in ['receivable','payable']:raise ReviewRequired('Related balance classification unresolved')
                    if x['type']=='receivable':recs+=n
                    else:pays+=n
                else:maximum+=n
            work.append({'id':x['id'],'group':group,'related_at_event':related,'included':included,'amount':n,'eliminated':eliminated})
    kmp=rows(c['kmp_compensation']);inventory(c,'kmp_inventory',kmp);kmptotal=ZERO
    for k in kmp:
        reviewed(k,c,'payroll_evidence','period_allocation_memo');required(k,'relationship_id','category','amount','gl_amount','included')
        if k['relationship_id'] not in relmap or relmap[k['relationship_id']]['kind']!='kmp':raise ReviewRequired('KMP compensation lacks evidenced KMP relationship')
        n=nonnegative(k['amount']);included=flag(k,'included')
        agree(k['gl_amount'],n,'KMP payroll/GL source tie')
        if k['category'] not in ['short_term','post_employment','other_long_term','termination','share_based']:raise ReviewRequired('KMP compensation category unsupported')
        if flag(scope,'kmp_scope') and not included:raise ReviewRequired('Applicable KMP compensation requires complete category disclosure')
        if included:kmptotal+=n
    if flag(scope,'kmp_scope') and not kmp:raise ReviewRequired('Applicable KMP compensation disclosure population missing')
    required(c,'kmp_categories_review')
    review=c['kmp_categories_review'];reviewed(review,c,'completeness_memo');required(review,'totals')
    categories=['short_term','post_employment','other_long_term','termination','share_based']
    if set(review['totals'])!=set(categories):raise ReviewRequired('All KMP compensation categories must be reviewed, including nil')
    for category in categories:agree(review['totals'][category],sum((nonnegative(k['amount']) for k in kmp if k['category']==category),ZERO),'KMP category completeness')
    required(c,'statement_totals');s=c['statement_totals']
    for key,n in [('sales',sales),('purchases',purchases),('receivables',recs),('payables',pays),('commitments',maximum),('kmp',kmptotal)]:agree(s[key],n,'Related-party note total '+key)
    population(c,sources,[nonnegative(x['amount']) for x in sources])
    return finish('Evidenced relationships, dated transactions and note populations reconcile.',{'sources':work,'sales':sales,'purchases':purchases,'receivables':recs,'payables':pays,'commitments':maximum,'kmp_compensation':kmptotal,'eliminated_amounts':eliminations},[],
      ['Related-party status and arm-length assertions require actual evidence, not matching names or master flags.','Recognition/measurement stays with underlying accounting; related-party disclosure and group elimination are distinct.'],
      ['Relationships/control/ultimate parent, transactions, balances/terms/security, commitments, applicable KMP categories, exemptions and comparative populations.'])

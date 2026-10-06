"""Typed, evidence-only cross-scope specialist receipts.

The consumer already has an independently reviewed native workpaper. Receipts
verify the exact upstream result and specific accounting meaning; they create no
accounting, conversion, certification or postings. One case per package only.
"""
import copy
from .runtime import at, digest, dimensions, number

# Producer path / consumer path. '*' matches a reviewed native row identity.
CONTRACTS = {
    ('income-taxes','business-combinations','acquisition_dtl'): (('jurisdictions',0,'dtl'),('liabilities','dtl','amount')),
    ('business-combinations','foreign-currency','acquisition_goodwill'): (('initial_goodwill',),('translation','tb','goodwill','balance')),
    ('business-combinations','foreign-currency','acquisition_basis'): ((),('qualified_acquisition',)),
    ('business-combinations','consolidation','acquisition_basis'): ((),('qualified_acquisition',)),
    ('foreign-currency','consolidation','translated_population'): (('translation','translated_tb'),('entities','@producer_entity','balances')),
    ('foreign-currency','consolidation','post_acquisition_profit'): (('translation','profit_translated'),('nci',0,'adjusted_profit')),
    ('foreign-currency','consolidation','nci_oci'): (('translation','cta_movement'),('nci',0,'adjusted_oci')),
    ('intercompany-accounting','consolidation','matched_intercompany'): (('pairs',0,'a_functional'),('intercompany',0,'amount')),
    ('foreign-currency','asset-impairment','goodwill_carrying'): (('translation','translated_tb','goodwill'),('assets','gw','carrying')),
    ('consolidation','management-accounting-analytics','entity_contribution_population'): (('consolidated_balances',),('qualified_contribution_population',)),
    ('foreign-currency','management-accounting-analytics','post_acquisition_contribution'): (('translation','profit_translated'),('documents','group-drivers','content','supported_post_profit')),
    ('financial-statements','management-accounting-analytics','group_profit'): (('current','profit'),('accounts','cash-metric','amount')),
    ('foreign-currency','asset-impairment','unit_carrying'): (('translation','closing_net_translated'),('qualified_unit_carrying',)),
    ('asset-impairment','consolidation','impairment'): (('loss',),('specialist_receipts','impairment')),
    ('consolidation','financial-statements','consolidated_population'): (('consolidated_balances',),('qualified_consolidated_balances',)),
    ('consolidation','financial-statements','nci_profit'): (('nci',0,'profit'),('equity_bridge','nci','profit')),
    ('consolidation','financial-statements','nci_oci'): (('nci',0,'oci'),('equity_bridge','nci','oci')),
    ('consolidation','financial-statements','nci_closing'): (('nci',0,'closing'),('equity_bridge','nci','closing')),
}


def validate_receipts(node, graph, inputs, case):
    source=inputs[node.id]
    receipts=source.get('qualified_owner_results',[])
    required={identity for identity in CONTRACTS if identity[1]==node.selected_skill and any(n.selected_skill==identity[0] for n in graph.nodes.values())}
    required={r for r in required if r[2] not in ('group_profit','post_acquisition_contribution') or (r[2]=='group_profit' and inputs[r[0]].get('qualified_consolidated_balances') is not None) or (r[2]=='post_acquisition_contribution' and inputs[r[0]].get('qualified_acquisition') is not None)}
    supplied={(graph.nodes[r.get('producer')].selected_skill,node.selected_skill,r.get('semantic')) for r in receipts if r.get('producer') in graph.nodes}
    if not required<=supplied:raise ValueError('Mandatory specialist result receipt omitted')
    seen=set()
    for receipt in receipts:
        if set(receipt)!={'producer','semantic','result','source_dimensions','consumer_dimensions','evidence'} or not receipt['evidence']:
            raise ValueError('Qualified specialist receipt schema/evidence required')
        producer=graph.nodes.get(receipt['producer'])
        if not producer or producer.status!='complete' or producer.id not in node.dependencies:
            raise ValueError('Specialist receipt requires completed upstream graph node')
        identity=(producer.selected_skill,node.selected_skill,receipt['semantic'])
        contract=CONTRACTS.get(identity)
        if not contract or identity in seen:raise ValueError('Unknown or duplicate semantic specialist receipt')
        seen.add(identity)
        if digest(receipt['result'])!=digest(producer.result):raise ValueError('Stale or substituted specialist result')
        if tuple(receipt['source_dimensions'])!=dimensions(inputs[producer.id]) or tuple(receipt['consumer_dimensions'])!=dimensions(source):
            raise ValueError('Specialist receipt entity/currency/period dimensions differ')
        upstream=inputs[producer.id]
        if identity[:2] in (('income-taxes','business-combinations'),('business-combinations','foreign-currency')) and upstream['entity']!=source['entity']:
            raise ValueError('Specialist acquisition receipt crosses legal entities')
        if receipt['semantic']=='acquisition_dtl':
            if upstream.get('acquisition_effective_date')!=source['acquisition']['date']:raise ValueError('Acquisition tax determination date differs')
            differences=upstream['jurisdictions'][0]['differences']
            if len(upstream['jurisdictions'])!=1 or len(differences)!=1:raise ValueError('Acquisition tax requires bounded identified asset population')
            difference=differences[0];assets=[a for a in source['assets'] if a.get('asset_identity')==difference.get('asset_identity')]
            if not difference.get('asset_identity') or len(assets)!=1 or number(difference['carrying'])!=number(assets[0]['amount']) or difference['allocation']!='acquisition':raise ValueError('Acquisition tax asset identity/basis differs from qualified fair-value adjustment')
        if receipt['semantic']=='matched_intercompany':
            if len(upstream['pairs'])!=1 or len(source['intercompany'])!=1:raise ValueError('Unbounded intercompany population unsupported')
            if dimensions(upstream)[-1]!=dimensions(source)[-1]:raise ValueError('Intercompany functional result requires qualified group-currency conversion')
            pair=upstream['pairs'][0];elimination=source['intercompany'][0]
            if pair['currency']==dimensions(upstream)[-1] and number(pair['rate_a'])!=1:raise ValueError('Same-currency intercompany rate must be one')
            if {pair['entity_a'],pair['entity_b']}!={elimination['seller'],elimination['buyer']} or pair['transaction_id']!=elimination['source_id']:
                raise ValueError('Intercompany counterparty/transaction differs from elimination')
            local=producer.result['calculations']['pairs'][0]
            a_balance=at(source,['entities',pair['entity_a'],'balances',elimination['credit_account']])
            if number(a_balance)!=number(local['a_functional']):raise ValueError('Parent intercompany source differs from bilateral legal book')
            foreign=inputs.get('foreign-currency')
            if not foreign or foreign['entity']!=pair['entity_b']:raise ValueError('Reciprocal foreign-operation source absent')
            b_balance=at(foreign,['translation','tb',elimination['debit_account'],'balance'])
            if -number(b_balance)!=number(local['b_functional']):raise ValueError('Subsidiary local intercompany book differs from bilateral source')
            if pair['currency']==dimensions(foreign)[-1] and number(pair['rate_b'])!=1:raise ValueError('Same-currency subsidiary rate must be one')
        if receipt['semantic']=='entity_contribution_population':
            selector=source['entity_contribution'];entity=at(upstream,['entities',selector['entity']])
            if selector['entity'] not in producer.result['calculations']['perimeter']:raise ValueError('Contribution entity outside governed perimeter')
            profit=-sum((number(value) for account,value in entity['balances'].items() if upstream['statement_mapping'][account] in ('income','expenses')),number('0'))
            if number(at(source,['documents',selector['document'],'content',selector['field']]))!=profit:
                raise ValueError('Entity analytical contribution differs from qualified standalone source')
        if receipt['semantic']=='unit_carrying':
            if source['unit'].get('source_entity')!=upstream['entity'] or sum((number(r['carrying']) for r in source['assets']),number('0'))!=number(source['qualified_unit_carrying']):
                raise ValueError('Impairment unit carrying amount/entity differs from qualified foreign operation')
        actual=at(producer.result['calculations'],list(contract[0]))
        target=[producer.entity if k=='@producer_entity' else k for k in contract[1]]
        expected=at(source,target)
        if receipt['semantic']=='acquisition_goodwill':
            upstream=inputs[producer.id]
            if source['translation']['operation_id']!=source['entity']:
                raise ValueError('Foreign operation differs from acquired source entity')
            if source.get('activity_selection',{}).get('effective_date')!=upstream['acquisition']['date']:
                raise ValueError('Acquisition date differs from included activity window')
            if number(source['translation']['ownership'])!=number(upstream['nci']['ownership']):
                raise ValueError('Foreign operation ownership differs from acquisition result')
        # The FX output population includes its independently reconciled CTA.
        # A consumer receives the complete translated population plus that reserve,
        # and cannot rerun translation using another set of rates.
        if receipt['semantic']=='translated_population':
            expected=dict(expected)
            cta=expected.pop('translation reserve',None)
            if cta is None or number(cta)!=-number(producer.result['calculations']['translation']['closing_cta']):
                raise ValueError('Translated population omits or duplicates CTA')
            if at(source,['entities',producer.entity,'translation']) is not None:
                raise ValueError('Qualified foreign operation must not be translated twice')
        if digest(actual)!=digest(expected):
            # Native amounts may be Decimal while JSON sources use strings.
            def norm(v):
                if isinstance(v,dict):return {k:norm(x) for k,x in v.items()}
                if isinstance(v,list):return [norm(x) for x in v]
                try:return str(number(v).normalize())
                except (ValueError,ArithmeticError):return v
            if norm(actual)!=norm(expected):raise ValueError('Specialist semantic result binding differs')
        case.handoff_ledger.append(dict(producer=producer.id,consumer=node.id,semantic=receipt['semantic'],purpose='evidence_only',
            fingerprint=producer.result['case_fingerprint'],source_dimensions=receipt['source_dimensions'],consumer_dimensions=receipt['consumer_dimensions']))
    if node.selected_skill=='financial-statements' and receipts:
        actual={r['id']:r['balance'] for r in source['current_tb']}
        if {k:str(number(v).normalize()) for k,v in actual.items()}!={k:str(number(v).normalize()) for k,v in source['qualified_consolidated_balances'].items()}:
            raise ValueError('Financial Statements omitted or duplicated consolidated population')
    if node.selected_skill=='consolidation' and source.get('qualified_acquisition'):
        acquisition=source['qualified_acquisition'];rates=inputs['foreign-currency']['translation']
        if len(source['investments'])!=1 or len(source['nci'])!=1:raise ValueError('Multiple acquisition layers require generalized orchestration')
        inv=source['investments'][0];nci=source['nci'][0];bc=inputs['business-combinations']
        if inv['subsidiary']!=bc['entity'] or inv['parent_entity']!=bc['acquisition']['acquirer'] or nci['subsidiary']!=bc['entity']:
            raise ValueError('Acquisition and consolidation entity perimeter differ')
        rate=number(rates['opening_rate'])
        if number(inv['investment'])!=number(acquisition['consideration'])*rate or number(inv['nci_at_acquisition'])!=number(acquisition['nci'])*rate or number(nci['opening'])!=number(inv['nci_at_acquisition']):
            raise ValueError('Investment or initial NCI differs from acquisition-rate owner handoff')
        if number(inv['goodwill']) or inv['fair_value_adjustments']:
            raise ValueError('Acquisition adjustments already included in qualified foreign-operation source')
        if number(nci['ownership'])!=number(bc['nci']['ownership']):raise ValueError('NCI rights differ from acquisition')
        if number(source['specialist_receipts']['impairment']):
            raise ValueError('Integrated impairment posting/allocation requires separately governed loss route')
    if node.selected_skill=='foreign-currency' and source.get('qualified_acquisition'):
        acquisition=source['qualified_acquisition'];bc=inputs['business-combinations']
        if number(source['translation']['opening_net_assets'])!=number(acquisition['net_assets'])+number(acquisition['initial_goodwill']):
            raise ValueError('Foreign-operation opening net assets omit acquisition adjustments')
        for row in source['translation']['tb']:
            expected_rate=source['translation'][{'asset':'closing_rate','liability':'closing_rate','profit':'profit_rate','equity':'opening_rate'}[row['category']]]
            if number(row['rate'])!=number(expected_rate):raise ValueError('Foreign-operation row rate differs from qualified acquisition/post-acquisition rate schedule')
        if bc['nci']['method']!='fair_value':raise ValueError('Partial-goodwill CGU gross-up/CTA attribution requires separate integrated route')

"""Stage 3 adapters attached to the existing Stage 2 execution lifecycle."""
from decimal import Decimal
from .versions import fingerprint
from .intercompany_network import IntercompanyNetwork, TransactionSide, MatchingDecision


def validate_native_bindings(session, node, source, receipts):
    """Verify reviewed native inputs, never generate inputs or certification."""
    from .runtime import at
    bindings = source.get('stage3_input_bindings')
    if bindings is None:
        if node.economic_id is not None and receipts:
            raise ValueError('Transaction-qualified native consumers require exact input mappings')
        return
    if source.get('versioned_dependency_receipts') != receipts:
        raise ValueError('Reviewed exact dependency receipts required')
    seen = set();mapped=set()
    for binding in bindings:
        if set(binding) != {'dependency_id', 'target_path', 'sign', 'evidence'} or not binding['evidence']:
            raise ValueError('Explicit native source mapping required')
        edge = binding['dependency_id']
        rows = [r for r in receipts if r['dependency_id'] == edge]
        if len(rows) != 1 or binding['sign'] not in (1, -1) or type(binding['sign']) is not int:
            raise ValueError('Wrong source binding')
        target = tuple(binding['target_path'])
        if not target or target in seen:
            raise ValueError('Duplicate/empty native target mapping')
        seen.add(target);mapped.add(edge)
        metric=tuple(rows[0]['metric_path'])
        if node.selected_skill=='foreign-currency' and (len(target)!=4 or target[:2]!=('translation','tb') or target[3]!='balance'):
            raise ValueError('Translation mapping must bind actual native TB row')
        if node.selected_skill=='intercompany-accounting' and node.scope_type=='GROUP' and (len(target)!=3 or target[0]!='pairs' or target[2] not in ('gl_a','gl_b')):
            raise ValueError('Conversion mapping must bind native reciprocal carrying value')
        if node.selected_skill=='consolidation':
            if metric[:2]==('calculations','pairs') and session.cases.scopes.get(rows[0]['producer_scope']).scope_type=='LEGAL_ENTITY':
                if len(target)!=4 or target[0]!='entities' or target[2]!='balances' or source['entities'][target[1]]['id']!=rows[0]['producer_scope']:
                    raise ValueError('Legal-side mapping must bind actual producing legal entity')
            elif metric[:2]==('calculations','translation') and metric[-1] in ('closing_cta','cta_movement'):
                if metric[-1]=='closing_cta':
                    entity_path=len(target)==4 and target[0]=='entities' and target[2]=='balances' and source['entities'][target[1]]['id']==rows[0]['producer_scope'] and target[3] in source['cta_bridge']['cta_accounts']
                    valid=entity_path or target==('cta_bridge','closing')
                else:
                    valid=target in (('cta_bridge','translation'),('equity_bridge','oci'))
                if not valid:raise ValueError('CTA mapping must bind actual reserve and OCI owner bridge')
            elif metric[:2]==('calculations','pairs') and (len(target)!=3 or target[0]!='intercompany' or target[2]!='amount'):

                raise ValueError('Conversion mapping must bind native elimination amount')
        value = rows[0]['value']
        actual = at(source, target)
        if isinstance(value, (dict, list)):
            if binding['sign'] != 1 or value != actual:
                raise ValueError('Native population does not equal qualified producer population')
        else:
            # Sign mapping is bookkeeping identity, not FX/conversion arithmetic.
            a, b = Decimal(str(actual)), Decimal(str(value))
            if not a.is_finite() or not b.is_finite() or a != b * binding['sign']:
                raise ValueError('Native input differs from exact producer metric')
    if not bindings:
        raise ValueError('Stage 3 native source mappings cannot be empty')
    if node.selected_skill == 'consolidation':
        matches = [r for r in receipts if tuple(r['metric_path']) == ('matching','classification')]
        if len(matches) != 1 or matches[0]['value'] != 'MATCHED':
            raise ValueError('Group elimination requires a qualified clean bilateral match')
        match=session.versions.require_current(matches[0]['result_version']).payload()['matching']
        pairs=source['intercompany']
        side_roles={s['role']:s['scope_id'] for s in match['sides']}
        if len(pairs)!=1 or pairs[0]['transaction_id']!=node.economic_id or (pairs[0]['seller'],pairs[0]['buyer'])!=(side_roles.get('payable'),side_roles.get('receivable')):
            raise ValueError('Elimination counterparties/economic identity differ from qualified matching')
        translations = [r for r in receipts if tuple(r['metric_path']) == ('calculations','translation','translated_tb')]
        if len(translations) != 1:
            raise ValueError('Exact translated source population required')
        qualified = translations[0]['value']
        covered = []
        for entity in source['entities']:
            if entity['id']==translations[0]['producer_scope'] and all(entity['balances'].get(k) == v for k,v in qualified.items()):
                covered.append(entity)
        mapped.add(translations[0]['dependency_id'])
        if len(covered) != 1:
            raise ValueError('Consolidation source population differs from qualified translation')
        accounts=source['cta_bridge']['cta_accounts']
        if len(accounts)!=1 or set(covered[0]['balances'])!=set(qualified)|set(accounts):
            raise ValueError('Foreign-operation source population adds unsupported offsets')
        for semantic in ('closing_cta','cta_movement'):
            actual=[r for r in receipts if tuple(r['metric_path'])==('calculations','translation',semantic)]
            if len(actual)!=1 or actual[0]['producer_node']!=translations[0]['producer_node']:
                raise ValueError('Exact owner CTA dependency required')

    if node.selected_skill == 'financial-statements':
        qualified = source.get('stage3_balances')
        if not isinstance(qualified,dict) or {row['id']:row['balance'] for row in source['current_tb']} != qualified:
            raise ValueError('Reporting TB differs from exact qualified consolidated population')
        if len({row['id'] for row in source['current_tb']}) != len(source['current_tb']):
            raise ValueError('Duplicate reporting account')
    if node.selected_skill == 'intercompany-accounting' and node.scope_type == 'GROUP':
        if source.get('stage3_contract') != 'ORDINARY_IC_REASSESSMENT':
            raise ValueError('Explicit bounded framework conversion contract required')
        translations = [r for r in receipts if tuple(r['metric_path'])[:3] == ('calculations','translation','translated_tb')]
        if len(translations) != 1 or len(source['pairs']) != 1:
            raise ValueError('Unsupported general intercompany conversion')
        if source['conversion_economic_id'] != node.economic_id or source['pairs'][0]['transaction_id'] != node.economic_id:
            raise ValueError('Conversion economic identity differs')
        matching_receipts=[r for r in receipts if tuple(r['metric_path'])==('matching','classification')]
        if len(matching_receipts)!=1:
            raise ValueError('Conversion requires exact bilateral matching population')
        match=session.versions.require_current(matching_receipts[0]['result_version']).payload()['matching']
        sides=match['sides'];pair=source['pairs'][0]
        receivable=[s for s in sides if s['role']=='receivable'];payable=[s for s in sides if s['role']=='payable']
        if len(receivable)!=1 or len(payable)!=1 or (pair['entity_a'],pair['entity_b'])!=(receivable[0]['scope_id'],payable[0]['scope_id']) or translations[0]['producer_scope']!=pair['entity_a']:
            raise ValueError('Native conversion counterparties differ from exact qualified legal sides')
        if pair['currency']!=receivable[0]['transaction_currency'] or Decimal(pair['opening_a'])+Decimal(pair['recharge'])-Decimal(pair['settled_a'])!=Decimal(receivable[0]['transaction_amount']):
            raise ValueError('Native conversion principal differs from original commercial transaction')
        legal=[r for r in receipts if r['producer_scope']==pair['entity_b'] and tuple(r['metric_path'])[:2]==('calculations','pairs')]
        if len(legal)!=1 or legal[0]['value_currency']!=(node.functional_currency or node.presentation_currency) or Decimal(pair['gl_b'])!=Decimal(str(legal[0]['value'])):
            raise ValueError('Other legal carrying value lacks exact current reporting-currency qualification')
        for binding in bindings:
            receipt=next(r for r in receipts if r['dependency_id']==binding['dependency_id'])
            if receipt['dependency_id']==translations[0]['dependency_id'] and tuple(binding['target_path'])!=('pairs',0,'gl_a'):
                raise ValueError('Translated carrying amount must bind native originating side')
            if receipt['dependency_id']==legal[0]['dependency_id'] and tuple(binding['target_path'])!=('pairs',0,'gl_b'):
                raise ValueError('Counterparty carrying amount must bind actual native counterparty side')
        pairs = source['pairs']
        scopes = session.cases.scopes
        for pair in pairs:
            if pair['entity_a'] == pair['entity_b'] or any(scopes.get(pair[k]).scope_type != 'LEGAL_ENTITY' for k in ('entity_a','entity_b')):
                raise ValueError('Conversion counterparties must be legal entities')


    for receipt in receipts:
        if tuple(receipt['metric_path'])==('matching','classification'):
            if receipt['value']!='MATCHED':
                raise ValueError('Clean native chain requires qualified matched relationship')
            mapped.add(receipt['dependency_id'])
    if mapped!={r['dependency_id'] for r in receipts}:
        raise ValueError('Native mappings omit declared economically material dependencies')


def bounded_executor(session, node, source, receipts):
    from .governed_plan import observation
    if source.get('method') == 'STAGE3_MATCH':
        if not source.get('evidence') or source.get('versioned_dependency_receipts') != receipts:
            raise ValueError('Exact reviewed matching inputs required')
        network = IntercompanyNetwork(session, source['network_id'])
        for row in source['sides']:
            side = TransactionSide(**row)
            expected = {(r['producer_node'], r['result_version']) for r in receipts}
            if (side.owner_node, side.result_version) not in expected:
                raise ValueError('Matching side lacks declared exact result dependency')
            network.register(side)
        result = network.match(MatchingDecision(**source['decision']))
        if {s.owner_node for s in network.sides.values()} != {r['producer_node'] for r in receipts}:
            raise ValueError('Matching producer population differs from declared dependencies')
        return dict(status='complete', case_fingerprint=fingerprint([source, receipts]),
            matching=result, unresolved_dependencies=[] if result['classification'] in ('MATCHED','TIMING_DIFFERENCE','FX_DIFFERENCE') else [result['relationship_id']], accounting_authority=False, journal_entry_implications=[],
            framework=node.framework, currency=node.functional_currency or node.presentation_currency,
            limitations=['Matching is relationship lineage; unresolved residuals remain visible.'])
    if source.get('method') == 'STAGE3_GROUP_OBSERVATION':
        if not receipts or not source.get('evidence'):
            raise ValueError('Current reporting result required')
        return dict(status='complete', case_fingerprint=fingerprint([source, receipts]),
            observed_results=[dict(dependency=r['dependency_id'], result_version=r['result_version'], value=r['value']) for r in receipts],
            accounting_authority=False, journal_entry_implications=[], framework=node.framework,
            currency=node.presentation_currency, limitations=['Bounded Stage 3 receipt observation, not Stage 4 flagship.'])
    return observation(node, source, receipts)


def public_result(case, route):
    """Curated native reporting and residual projection through public_record."""
    from interfaces.public_output import public_record
    session=case.governance
    reports=[];residuals=[]
    for node_id in sorted(session.versions.active):
        node=session.graph.nodes[node_id]
        version=session.versions.require_current(session.versions.current(node_id).version_id)
        payload=version.payload()
        if node.selected_skill=='financial-statements' and node.scope_type=='GROUP':
            reports.append(payload['calculations']['current'])
        if payload.get('matching',{}).get('classification')=='UNRESOLVED_MISMATCH':
            residuals.append('An intercompany relationship remains unresolved; obtain owner-reviewed evidence. No correction or elimination is inferred.')
    if len(reports)!=1:
        return public_record(dict(status='partial',guidance='Qualified Group reporting requires further owner-reviewed work.',open_items=residuals),route=route)
    report=reports[0]
    calculations=[dict(label=label.replace('_',' '),amount=report[label]) for label in ('profit','oci','closing_equity') if label in report]
    return public_record(dict(status=case.outcome,guidance='The bounded Group reporting chain is current. Other intercompany residuals remain visible.',
        framework='IFRS',currency='EUR',calculations=calculations,open_items=residuals,
        limitations=['Bounded Stage 3 proof; unresolved relationships are excluded from clean eliminations. General framework conversion and the Stage 4 integration flagship are not established.']),route=route)

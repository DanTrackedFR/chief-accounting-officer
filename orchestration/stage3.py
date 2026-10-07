"""Stage 3 adapters attached to the existing Stage 2 execution lifecycle."""
from decimal import Decimal
from .versions import fingerprint
from .intercompany_network import IntercompanyNetwork, TransactionSide, MatchingDecision


def validate_native_bindings(session, node, source, receipts):
    """Verify reviewed native inputs, never generate inputs or certification."""
    from .runtime import at
    bindings = source.get('stage3_input_bindings')
    if node.selected_skill=='foreign-currency' and bindings and source.get('translation',{}).get('enabled'):
        if source['translation']['functional_currency']!=node.functional_currency or source['currency']['functional']!=node.functional_currency:
            raise ValueError('Native translation functional currency differs from governed legal book')
        if source['translation']['presentation_currency']!=source['currency']['presentation']:
            raise ValueError('Native translation presentation currencies differ')
    if node.selected_skill=='consolidation' and source.get('group_population_coverage') is not None:
        validate_group_loan_population(session,node,source,receipts)
        if not bindings:raise ValueError('Full Group accounting requires exact native population bindings')
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
        if not matches or any(r['value'] != 'MATCHED' for r in matches):
            raise ValueError('Group elimination requires qualified clean bilateral matches')
        relationships={}
        for receipt in matches:
            match=session.versions.require_current(receipt['result_version']).payload()['matching']
            side_roles={side['role']:side['scope_id'] for side in match['sides']}
            economic={side['economic_id'] for side in match['sides']}
            if len(economic)!=1:raise ValueError('Matching economic population differs')
            key=next(iter(economic))
            if key in relationships:raise ValueError('Duplicate qualified matching relationship')
            relationships[key]=(side_roles.get('payable'),side_roles.get('receivable'))
        pairs=source['intercompany']
        if len(pairs)!=len(relationships) or len({pair.get('transaction_id') for pair in pairs})!=len(pairs):
            raise ValueError('Elimination matching population omitted/duplicated')
        for pair in pairs:
            if (pair['seller'],pair['buyer'])!=relationships.get(pair['transaction_id']):
                raise ValueError('Elimination counterparties/economic identity differ from qualified matching')
            if node.economic_id is not None and pair['transaction_id']!=node.economic_id:
                raise ValueError('Elimination execution economic identity differs')
        translations = [r for r in receipts if tuple(r['metric_path']) == ('calculations','translation','translated_tb')]
        if not translations or len({r['producer_scope'] for r in translations})!=len(translations):
            raise ValueError('Exact distinct translated source populations required')
        accounts=source['cta_bridge']['cta_accounts']
        if len(accounts)!=1:raise ValueError('Explicit native CTA account required')
        closing=[];movement=[]
        for translated in translations:
            qualified=translated['value']
            covered=[entity for entity in source['entities'] if entity['id']==translated['producer_scope']]
            if len(covered)!=1 or set(covered[0]['balances'])!=set(qualified)|set(accounts) or any(covered[0]['balances'].get(k)!=v for k,v in qualified.items()):
                raise ValueError('Foreign-operation source population adds unsupported offsets or differs from qualified translation')
            mapped.add(translated['dependency_id'])
            for semantic,collector in (('closing_cta',closing),('cta_movement',movement)):
                actual=[r for r in receipts if tuple(r['metric_path'])==('calculations','translation',semantic) and r['producer_node']==translated['producer_node']]
                if len(actual)!=1:raise ValueError('Exact owner CTA dependency required')
                collector.append(actual[0])
                if semantic=='closing_cta' and Decimal(str(covered[0]['balances'][accounts[0]]))!=-Decimal(str(actual[0]['value'])):
                    raise ValueError('Entity CTA reserve differs from exact native owner')
                mapped.add(actual[0]['dependency_id'])
        # Validate separately reviewed aggregate native bridges. This verifies
        # additive owner outputs; it generates no exchange-rate/accounting values.
        close=sum((Decimal(str(r['value'])) for r in closing),Decimal(0))
        move=sum((Decimal(str(r['value'])) for r in movement),Decimal(0))
        if Decimal(str(source['cta_bridge']['closing']))!=-close or Decimal(str(source['cta_bridge']['translation']))!=-move or Decimal(str(source['equity_bridge']['oci']))!=move:
            raise ValueError('Group CTA/OCI bridge differs from complete qualified owner population')

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
        if len(translations) not in (1, 2) or len(source['pairs']) != 1:
            raise ValueError('Unsupported general intercompany conversion')
        if source['conversion_economic_id'] != node.economic_id or source['pairs'][0]['transaction_id'] != node.economic_id:
            raise ValueError('Conversion economic identity differs')
        matching_receipts=[r for r in receipts if tuple(r['metric_path'])==('matching','classification')]
        if len(matching_receipts)!=1:
            raise ValueError('Conversion requires exact bilateral matching population')
        match=session.versions.require_current(matching_receipts[0]['result_version']).payload()['matching']
        sides=match['sides'];pair=source['pairs'][0]
        receivable=[s for s in sides if s['role']=='receivable'];payable=[s for s in sides if s['role']=='payable']
        if len(receivable)!=1 or len(payable)!=1 or (pair['entity_a'],pair['entity_b'])!=(receivable[0]['scope_id'],payable[0]['scope_id']):
            raise ValueError('Native conversion counterparties differ from exact qualified legal sides')
        if pair['currency']!=receivable[0]['transaction_currency'] or Decimal(pair['opening_a'])+Decimal(pair['recharge'])-Decimal(pair['settled_a'])!=Decimal(receivable[0]['transaction_amount']):
            raise ValueError('Native conversion principal differs from original commercial transaction')
        validate_reassessment_sides(session, node, source, receipts, bindings, sides, translations)
        if source.get('recharges') or any(Decimal(str(pair['recharge']))!=0 for pair in source['pairs']):
            raise ValueError('Framework qualification supports ordinary loans only; services/recharges unavailable')
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


def validate_reassessment_sides(session, node, source, receipts, bindings, sides, translations):
    """Bound each carrying input to its exact matched legal side and signed row.

    This qualifies supplied native loan accounting; it supplies no rate,
    balancing adjustment, residual disposition or general conversion authority.
    """
    from .runtime import at
    pair=source['pairs'][0]
    translated={r['producer_scope']:r for r in translations}
    if len(translated)!=len(translations) or set(translated) not in ({pair['entity_a']}, {pair['entity_b']}, {pair['entity_a'],pair['entity_b']}):
        raise ValueError('Native conversion requires distinct exact translated legal sides')
    for role,entity,field in [('receivable',pair['entity_a'],'gl_a'),('payable',pair['entity_b'],'gl_b')]:
        side=next(s for s in sides if s['role']==role)
        if entity in translated:
            receipt=translated[entity]
            version=session.versions.require_current(receipt['result_version'])
            native=session.sources[version.node_id]
            if fingerprint(native)!=version.source_fingerprint:
                raise ValueError('Translation native source version differs')
            if receipt['value_currency']!=(node.functional_currency or node.presentation_currency) or native['translation']['operation_id']!=node.economic_id:
                raise ValueError('Translated side currency/economic identity differs')
            legal_node=session.graph.nodes[side['owner_node']]
            if native['translation']['functional_currency']!=legal_node.functional_currency or native['currency']['functional']!=legal_node.functional_currency:
                raise ValueError('Translated side functional currency differs from exact legal book')
            # The translation must consume this exact current matched legal
            # result, not an equal-value different loan or earlier result.
            rows=[]
            for binding in native.get('stage3_input_bindings',[]):
                edge=session.edges[binding['dependency_id']]
                if edge.producer_node!=side['owner_node']:continue
                if dict(version.dependency_bindings).get(edge.id)!=side['result_version'] or tuple(edge.metric_path)!=tuple(side['metric_path']):continue
                path=tuple(binding['target_path'])
                if len(path)!=4 or path[:2]!=('translation','tb') or path[3]!='balance':continue
                row=native['translation']['tb'][path[2]]
                if tuple(receipt['metric_path'])!=('calculations','translation','translated_tb',row['id']):continue
                sign=1 if role=='receivable' else -1
                if binding['sign']!=sign or row['category']!=('asset' if role=='receivable' else 'liability'):
                    raise ValueError('Translated row must preserve signed legal side')
                legal=session.versions.require_current(side['result_version'])
                if Decimal(str(at(native,path)))!=Decimal(str(at(legal.payload(),tuple(side['metric_path']))))*sign:
                    raise ValueError('Translated row differs from exact matched legal carrying value')
                rows.append(binding)
            if len(rows)!=1:raise ValueError('Translated side lacks exact matched legal row lineage')
            sign=1 if role=='receivable' else -1
        else:
            candidates=[r for r in receipts if r['producer_scope']==entity and tuple(r['metric_path'])==tuple(side['metric_path']) and r['result_version']==side['result_version']]
            if len(candidates)!=1:raise ValueError('Other legal carrying value lacks exact current reporting-currency qualification')
            receipt=candidates[0];sign=1
            if receipt['value_currency']!=(node.functional_currency or node.presentation_currency):
                raise ValueError('Other legal carrying value lacks exact current reporting-currency qualification')
        exact=[b for b in bindings if b['dependency_id']==receipt['dependency_id']]
        if len(exact)!=1 or tuple(exact[0]['target_path'])!=('pairs',0,field) or exact[0]['sign']!=sign:
            raise ValueError('Carrying amount must bind exact signed native counterparty side')


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
    """One curated Group conclusion over current qualified owners and residuals."""
    from interfaces.public_output import public_record
    session=case.governance
    reports=[];residuals=[];observations=[];analytics=[];report_units=[]
    for node_id in sorted(session.versions.active):
        node=session.graph.nodes[node_id]
        version=session.versions.require_current(session.versions.current(node_id).version_id)
        payload=version.payload()
        if node.status=='complete' and not payload.get('unresolved_dependencies') and node.selected_skill=='financial-statements' and node.scope_type=='GROUP':
            reports.append(payload['calculations']['current'])
            scale=session.sources[node_id].get('unit_scale','units')
            if scale not in ('units','million'):raise ValueError('Explicit supported presentation scale required')
            report_units.append(scope_currency(node,scale))
        match=payload.get('matching',{})
        if match.get('classification')=='UNRESOLVED_MISMATCH':
            sides=match['sides']
            amounts=' versus '.join(str(side['transaction_amount'])+' '+side['transaction_currency']+(' million' if session.sources[side['owner_node']].get('unit_scale')=='million' else '') for side in sides)
            names=' and '.join(session.cases.scopes.get(side['scope_id']).display_name for side in sides)
            residuals.append('The intercompany balances between '+names+' remain unresolved ('+amounts+'). Obtain separately reviewed reciprocal confirmation and legal-book reconciliation; no correction or balancing plug is inferred.')
        elif match.get('classification') in ('TIMING_DIFFERENCE','FX_DIFFERENCE'):
            observations.append('An intercompany '+match['classification'].lower().replace('_',' ')+' remains separately classified; it has not been forced to zero or treated as a new Group adjustment.')
        if node.status=='complete' and node.selected_skill=='management-accounting-analytics':
            bridge=payload.get('calculations',{}).get('diagnostic',{}).get('bridge',{})
            if bridge:
                for driver in bridge['drivers']:
                    analytics.append(driver['label']+': '+driver['contribution']+' '+bridge['unit']+'.')
                analytics.append('The analytical bridge retains an unexplained residual of '+bridge['residual']+' '+bridge['unit']+'. Accounting treatment remains the qualified accounting owners’ conclusion.')
    scope=session.cases.scopes.get(case.scope_id)
    record=dict(status=case.outcome,framework=scope.framework,effective_period=' to '.join(case.periods),
        guidance='The Group close and intercompany evidence were reviewed. Final Group reporting is not yet supportable because a required material dependency remains unresolved.' if residuals or len(reports)!=1 or case.outcome!='complete' else 'The material intercompany conflict is resolved and the required accounting and reporting results are current after selective revalidation.' if session.rework_history else 'The qualified Group accounting and reporting results are current.',
        open_items=residuals,reporting=analytics+observations,
        limitations=['Framework qualification is limited to independently reviewed ordinary intercompany loans. General framework conversion remains unavailable. Review approvals are controlled synthetic evidence; this is not an audit opinion.'])
    if len(reports)==1 and not residuals and case.outcome=='complete':
        record['reporting'].append('Statement amounts are presented in '+report_units[0]+'.')
        record['calculations']=[dict(label=label.replace('_',' '),amount=reports[0][label]) for label in ('profit','oci','closing_equity','cash') if label in reports[0]]
    # Dynamic identities must also be excluded inside allowed narrative fields.
    private=[]
    def visit(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if key in ('reviewer','approved_by','reviewer_identity') and isinstance(item,str) and item:private.append(item)
                else:visit(item)
        elif isinstance(value,list):
            for item in value:visit(item)
    visit(session.sources)
    import json
    text=json.dumps(record,ensure_ascii=False)
    if any(token in text for token in private):raise ValueError('Internal reviewer identity in public result')
    return public_record(record,route=route)


def scope_currency(node,scale):
    return node.presentation_currency+(' millions' if scale=='million' else ' currency units')


def current_legal_loan_versions(session, group_node, legal_scopes):
    """Current loan inventories inside an explicitly reviewed Group perimeter.

    Scope membership supplies no dependencies. This validates accounting source
    completeness; each included result still needs an explicit consuming edge.
    """
    versions=[]
    for key in sorted(session.versions.active):
        n=session.graph.nodes[key]
        if n.scope_id not in legal_scopes or n.scope_type!='LEGAL_ENTITY' or n.selected_skill!='intercompany-accounting' or n.period!=group_node.period:continue
        v=session.versions.current(key)
        if session.sources[key].get('intercompany_transactions'):
            session.versions.require_current(v.version_id);versions.append(v.version_id)
    return sorted(versions)


def validate_group_loan_population(session,node,source,receipts):
    """Fail closed on missing legal economics in a full reviewed Group close."""
    coverage=source.get('group_population_coverage')
    if coverage is None:return  # Legacy explicitly bounded transaction chains.
    if not isinstance(coverage,dict) or set(coverage)!={'mode','required_legal_result_versions'} or coverage['mode']!='ALL_CURRENT_LOAN_SIDES':
        raise ValueError('Explicit complete Group loan population contract required')
    entities=source['entities']
    scopes={entity['id'] for entity in entities}
    if not scopes or len(scopes)!=len(entities) or any(session.cases.scopes.get(key).scope_type!='LEGAL_ENTITY' for key in scopes):
        raise ValueError('Full Group accounting requires a distinct registered legal perimeter')
    # ALL_CURRENT is a coverage promise over the governed Group's legal
    # descendants, not a promise over an arbitrarily shortened input list.
    # Hierarchy supplies only this completeness boundary; it supplies neither
    # consolidation authority nor any execution/dependency edge.
    governed=set()
    for row in session.cases.scopes.record():
        if row['scope_type']!='LEGAL_ENTITY' or row['status']!='CURRENT':continue
        if row['effective_from'] and row['effective_from']>node.period[1]:continue
        if row['effective_to'] and row['effective_to']<node.period[0]:continue
        parent=row['parent_scope_id']
        while parent is not None:
            if parent==node.scope_id:
                governed.add(row['scope_id']);break
            parent=session.cases.scopes.get(parent).parent_scope_id
    if scopes!=governed:
        raise ValueError('Full Group source perimeter differs from governed legal scope population')
    expected=current_legal_loan_versions(session,node,scopes)
    if coverage['required_legal_result_versions']!=expected:raise ValueError('Reviewed full Group source inventory differs from actual current legal results')
    matched=[]
    for receipt in receipts:
        if tuple(receipt['metric_path'])!=('matching','classification'):continue
        payload=session.versions.require_current(receipt['result_version']).payload()['matching']
        matched.extend(side['result_version'] for side in payload['sides'])
    if len(matched)!=len(set(matched)) or set(matched)!=set(expected):
        raise ValueError('Full Group accounting omits or duplicates current legal loan economics; qualify every relationship before a clean close')

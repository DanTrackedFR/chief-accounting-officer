"""Exact temporal consumption for complete governed reporting populations.

The native reporting owner retains accounting authority. This boundary qualifies
its supplied opening and comparative populations; it infers no intervening books.
"""
from .versions import fingerprint


def validate_reporting_temporal(session, node, source, receipts):
    target = session.periods.get(node.period_id)
    if target.period_type == 'OPENING':
        key = source.get('opening_stock_dependency')
        if len(receipts) != 1 or receipts[0]['dependency_id'] != key:
            raise ValueError('Opening stock requires one exact adjacent closing receipt')
        receipt = receipts[0]; session.validate_receipt(receipt, node.id)
        edge = session.edges[key]; edge.validate(session.graph, session.cases, session.periods)
        producer = session.graph.nodes[edge.producer_node]
        version = session.versions.require_current(receipt['result_version'])
        native = session.sources[producer.id]
        if (edge.dependency_type != 'OPENING' or not edge.required
                or producer.selected_skill != 'financial-statements'
                or producer.scope_id != node.scope_id or producer.framework != node.framework
                or receipt['value_currency'] != (node.functional_currency or node.presentation_currency)
                or tuple(edge.metric_path) != ('calculations', 'current')
                or fingerprint(native) != version.source_fingerprint
                or source.get('current_tb') != native.get('current_tb')
                or source.get('opening_tb') != native.get('current_tb')
                or source.get('opening', {}).get('period_end') != session.periods.get(edge.producer_period).end):
            raise ValueError('Opening stock differs from exact adjacent native closing')
        return
    complete = any(session.sources.get(r['producer_node'], {}).get('group_population_coverage')
                   for r in receipts)
    complete = complete or any(edge.consumer_node == node.id and edge.required
                               and (edge.dependency_type in ('OPENING', 'COMPARATIVE')
                                    or session.periods.get(edge.producer_period).period_type == 'OPENING')
                               for edge in session.edges.values())
    if not complete and 'temporal_reporting' not in source:
        return  # Retained bounded legacy proofs, not a full governed close.
    declarations = source.get('temporal_reporting')
    if not isinstance(declarations, dict) or set(declarations) != {'OPENING', 'COMPARATIVE'}:
        raise ValueError('Reporting requires separate exact opening and comparative dependencies')
    for kind, field in [('OPENING', 'opening_tb'), ('COMPARATIVE', 'comparative_tb')]:
        key = declarations[kind]
        matches = [r for r in receipts if r['dependency_id'] == key]
        if len(matches) != 1:
            raise ValueError('Missing exact temporal reporting receipt')
        receipt = matches[0]
        session.validate_receipt(receipt, node.id)
        edge = session.edges[key]
        edge.validate(session.graph, session.cases, session.periods)
        producer = session.graph.nodes[edge.producer_node]
        prior = session.periods.get(edge.producer_period)
        current = session.periods.get(node.period_id)
        opening_stock = kind == 'OPENING' and prior.period_type == 'OPENING'
        if (edge.dependency_type != ('QUALIFIED_ALIGNMENT' if opening_stock else kind) or not edge.required
                or producer.selected_skill != 'financial-statements'
                or producer.scope_id != node.scope_id
                or producer.framework != node.framework
                or receipt['value_currency'] != (node.functional_currency or node.presentation_currency)
                or prior.calendar_id != current.calendar_id
                or tuple(edge.metric_path) != ('calculations', 'current')):
            raise ValueError('Temporal reporting producer relationship or dimensions differ')
        version = session.versions.require_current(receipt['result_version'])
        native = session.sources[producer.id]
        if fingerprint(native) != version.source_fingerprint:
            raise ValueError('Temporal reporting source does not match immutable version')
        if source.get(field) != native.get('current_tb'):
            raise ValueError('Temporal reporting TB differs from exact native producer population')
        metadata = source.get('opening' if kind == 'OPENING' else 'comparative', {})
        expected_end = native.get('opening', {}).get('period_end') if opening_stock else prior.end
        if metadata.get('period_end') != expected_end:
            raise ValueError('Temporal reporting source date differs from governed Period')
        if opening_stock:
            if prior.start != current.start or prior.end != current.start:
                raise ValueError('Opening stock must be current reporting boundary')
            # Requalify the opening producer's own exact adjacent closing chain.
            validate_reporting_temporal(session, producer, native,
                [session.receipt(k) for k,e in sorted(session.edges.items()) if e.consumer_node==producer.id])
        if kind == 'COMPARATIVE':
            # Corresponding prior-year reporting interval, explicitly governed.
            if (prior.start[5:], prior.end[5:], int(prior.start[:4])+1, int(prior.end[:4])+1) != (
                    current.start[5:], current.end[5:], int(current.start[:4]), int(current.end[:4])):
                raise ValueError('Reporting comparative must be corresponding prior-year Period')
    if declarations['OPENING'] == declarations['COMPARATIVE']:
        raise ValueError('Opening and comparative receipts must be distinct')

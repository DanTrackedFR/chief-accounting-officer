"""Exact-version, owner-qualified reporting-basis receipts.

No conversion or exchange-rate arithmetic is performed here. Values must be
native accounting-owner outputs, with exact reviewed native input mappings.
"""
import copy
from dataclasses import dataclass, asdict
from .versions import fingerprint
from .periods import identity

LAYERS = frozenset({'LEGAL_ENTITY', 'MATCHING', 'FRAMEWORK_ADJUSTMENT',
                   'TRANSLATION', 'GROUP_ELIMINATION', 'GROUP_REPORTING'})


@dataclass(frozen=True)
class CrossLayerReceipt:
    dependency_id: str
    result_version: str
    producer_node: str
    producer_scope: str
    producer_period: str
    producer_case: str
    producer_layer: str
    framework: str
    currency: str
    semantic_metric: str
    economic_id: str
    metric_path: tuple
    value: object
    result_fingerprint: str
    source_fingerprint: str
    consumer_node: str
    consumer_scope: str
    consumer_period: str
    consumer_case: str
    consumer_layer: str
    required_framework: str
    required_currency: str
    evidence: tuple
    currentness: str = 'CURRENT'
    transformation_version: str | None = None

    @property
    def id(self):
        return identity('cross-layer-receipt', asdict(self))


class ReportingBasis:
    """Contracts composed onto one existing VersionedExecution session."""
    def __init__(self, session):
        self.session = session
        self.contracts = {}
        self.history = []

    def declare(self, edge_id, *, producer_layer, consumer_layer, framework,
                currency, semantic_metric, economic_id, required_framework,
                required_currency, evidence, transformation_version=None):
        edge = self.session.edges[edge_id]
        if edge_id in self.contracts or self.session.versions.current(edge.consumer_node, allow_stale=True):
            raise ValueError('Cannot redefine reporting-basis contract after consumption')
        if producer_layer not in LAYERS or consumer_layer not in LAYERS:
            raise ValueError('Explicit supported accounting layer required')
        if not all(isinstance(v, str) and v.strip() for v in
                   (framework, currency, semantic_metric, economic_id, required_framework, required_currency)) or not evidence:
            raise ValueError('Explicit reporting-basis semantic/evidence contract required')
        if (framework, currency) != (required_framework, required_currency):
            raise ValueError('Qualified conversion/translation required before consumption')
        semantics={'ordinary_reciprocal_balance':('calculations','pairs'),
            'translated_intercompany_balance':('calculations','translation','translated_tb'),
            'qualified_translation_population':('calculations','translation','translated_tb'),
            'matching_classification':('matching','classification'),
            'consolidated_population':('calculations','consolidated_balances'),
            'group_statements':('calculations',),
            'litigation_provision':('calculations','provision')}
        layers={'ordinary_reciprocal_balance':{'LEGAL_ENTITY','FRAMEWORK_ADJUSTMENT'},
            'translated_intercompany_balance':{'TRANSLATION'},'qualified_translation_population':{'TRANSLATION'},
            'matching_classification':{'MATCHING'},'consolidated_population':{'GROUP_ELIMINATION'},
            'group_statements':{'GROUP_REPORTING'},'litigation_provision':{'LEGAL_ENTITY'}}
        if producer_layer not in layers.get(semantic_metric,set()):
            raise ValueError('Semantic metric cannot masquerade as another accounting layer')
        prefix=semantics.get(semantic_metric)
        if prefix is None or tuple(edge.metric_path)[:len(prefix)]!=prefix:
            raise ValueError('Semantic metric differs from native result path')
        producer=self.session.graph.nodes[edge.producer_node]
        consumer=self.session.graph.nodes[edge.consumer_node]
        owners={'MATCHING':{'orchestration-stage3-match'},'TRANSLATION':{'foreign-currency'},
            'FRAMEWORK_ADJUSTMENT':{'intercompany-accounting'},
            'GROUP_ELIMINATION':{'consolidation'},'GROUP_REPORTING':{'financial-statements'}}
        if producer_layer in owners and producer.selected_skill not in owners[producer_layer]:
            raise ValueError('Wrong-layer producer owner')
        if consumer_layer in owners and consumer.selected_skill not in (owners[consumer_layer] | ({'orchestration-stage3-group'} if consumer_layer=='GROUP_REPORTING' else set())):
            raise ValueError('Wrong-layer consumer owner')
        if producer_layer=='LEGAL_ENTITY' and producer.scope_type!='LEGAL_ENTITY':
            raise ValueError('Wrong legal posting layer')
        if producer.economic_id is not None and producer.economic_id!=economic_id:
            raise ValueError('Economic identity differs from producing transaction node')
        if consumer.economic_id is not None and consumer.economic_id!=economic_id:
            raise ValueError('Economic identity differs from consuming transaction node')
        if consumer_layer in ('GROUP_ELIMINATION','GROUP_REPORTING') and (required_framework,required_currency)!=(consumer.framework,consumer.presentation_currency):
            raise ValueError('Group consumer requires its actual reporting basis')
        self.contracts[edge_id] = dict(producer_layer=producer_layer, consumer_layer=consumer_layer,
            framework=framework, currency=currency, semantic_metric=semantic_metric,
            economic_id=economic_id, required_framework=required_framework,
            required_currency=required_currency, evidence=tuple(evidence),
            transformation_version=transformation_version)
        return edge_id

    def receipt(self, edge_id):
        from .runtime import at
        edge = self.session.edges[edge_id]
        basis = self.contracts[edge_id]
        version = self.session.versions.current(edge.producer_node)
        self.session.versions.require_current(version.version_id)
        node = self.session.graph.nodes[edge.producer_node]
        if node.status != 'complete':
            raise ValueError('Current complete producer required')
        if node.framework != basis['framework']:
            raise ValueError('Framework relabelling forbidden')
        if basis['producer_layer'] == 'TRANSLATION':
            native = self._native(version, 'foreign-currency')
            if native['currency']['presentation'] != basis['currency'] or not native['translation']['enabled']:
                raise ValueError('Wrong presentation currency/disabled translation')
            if tuple(edge.metric_path)[:2] != ('calculations', 'translation'):
                raise ValueError('Transaction FX cannot substitute for translation')
        elif basis['currency'] != (node.functional_currency or node.presentation_currency):
            raise ValueError('Value currency relabelling forbidden')
        expected_owners = {'FRAMEWORK_ADJUSTMENT': 'provisions-contingencies',
                           'GROUP_ELIMINATION': 'consolidation',
                           'GROUP_REPORTING': 'financial-statements'}
        if basis['producer_layer'] in expected_owners:
            owner = expected_owners[basis['producer_layer']]
            if basis['producer_layer'] == 'FRAMEWORK_ADJUSTMENT' and node.selected_skill == 'intercompany-accounting':
                owner = 'intercompany-accounting'
            self._native(version, owner)
            if basis['producer_layer']=='FRAMEWORK_ADJUSTMENT' and owner=='intercompany-accounting':
                sources=[v for _,v in version.dependency_bindings if self.session.graph.nodes[self.session.versions.versions[v].node_id].selected_skill=='foreign-currency']
                if len(sources)!=1:raise ValueError('Qualified conversion source version required')
                start=len(self.history)
                try:self.intercompany_conversion(sources[0],version.version_id,basis['economic_id'],('calculations','translation','translated_tb','ic loan'),basis['evidence'])
                finally:del self.history[start:]
        if basis['producer_layer'] == 'LEGAL_ENTITY' and node.scope_type != 'LEGAL_ENTITY':
            raise ValueError('Group result cannot replace legal-side result')
        if basis['producer_layer'] in ('GROUP_ELIMINATION', 'GROUP_REPORTING') and node.scope_type != 'GROUP':
            raise ValueError('Legal result cannot replace Group result')
        receipt = CrossLayerReceipt(edge_id, version.version_id, node.id, node.scope_id,
            node.period_id, node.case_id, basis['producer_layer'], basis['framework'],
            basis['currency'], basis['semantic_metric'], basis['economic_id'], tuple(edge.metric_path),
            copy.deepcopy(at(version.payload(), edge.metric_path)), version.result_fingerprint,
            version.source_fingerprint, edge.consumer_node, edge.consumer_scope,
            edge.consumer_period, edge.consumer_case, basis['consumer_layer'],
            basis['required_framework'], basis['required_currency'], basis['evidence'],
            transformation_version=basis['transformation_version'])
        if receipt.transformation_version is not None:
            self.session.versions.require_current(receipt.transformation_version)
        return receipt

    def validate(self, receipt, consumer_node):
        if not isinstance(receipt, CrossLayerReceipt) or receipt.dependency_id not in self.contracts:
            raise ValueError('Undeclared cross-layer receipt')
        if receipt.consumer_node != consumer_node or receipt != self.receipt(receipt.dependency_id):
            raise ValueError('Stale/wrong-layer/version/dimensional receipt')
        return self.session.versions.require_current(receipt.result_version)

    def _native(self, version, owner):
        from .runtime import production
        node = self.session.graph.nodes[version.node_id]
        if node.selected_skill != owner:
            raise ValueError('Unsupported accounting transformation owner')
        source = self.session.sources[node.id]
        if fingerprint(source) != version.source_fingerprint:
            raise ValueError('Native source/result version mismatch')
        result = production.assess_case(owner, copy.deepcopy(source))
        if result.get('status') != 'complete' or fingerprint(result) != version.result_fingerprint:
            raise ValueError('Native qualification is stale or substituted')
        return source

    def translation(self, source_version, translation_version, economic_id,
                    source_metric, input_path, output_metric, evidence, input_sign=1):
        """Native FX TB row must consume the exact upstream functional amount."""
        from .runtime import at
        source = self.session.versions.require_current(source_version)
        target = self.session.versions.require_current(translation_version)
        native = self._native(target, 'foreign-currency')
        if not evidence or not economic_id or source.node_id == target.node_id:
            raise ValueError('Explicit independent translation lineage required')
        if source_version not in [v for _, v in target.dependency_bindings]:
            raise ValueError('Translation missing exact source dependency')
        source_node = self.session.graph.nodes[source.node_id]
        target_node = self.session.graph.nodes[target.node_id]
        if economic_id!=source_node.economic_id or economic_id!=target_node.economic_id or native['translation']['operation_id']!=economic_id:
            raise ValueError('Translation economic identity differs from qualified source/operation')
        if len(input_path)!=4 or tuple(input_path[:2])!=('translation','tb') or input_path[3]!='balance' or len(output_metric)!=4 or output_metric[3]!=native['translation']['tb'][input_path[2]]['id']:
            raise ValueError('Translation input/output rows differ')
        t = native['translation']
        if t['functional_currency'] != source_node.functional_currency or t['presentation_currency'] == t['functional_currency']:
            raise ValueError('Translation source currency differs')
        from decimal import Decimal
        if type(input_sign) is not int or input_sign not in (1, -1) or Decimal(str(at(source.payload(), source_metric))) * input_sign != Decimal(str(at(native, input_path))):
            raise ValueError('Translation native input differs from source result')
        if tuple(output_metric)[:2] != ('calculations', 'translation'):
            raise ValueError('Qualified translation output required')
        value = at(target.payload(), output_metric)
        record = dict(kind='CURRENCY_TRANSLATION', source_version=source_version,
            source_scope=source.scope_id, source_period=source.period_id,
            result_version=translation_version, owner='foreign-currency', economic_id=economic_id,
            source_currency=t['functional_currency'], target_currency=t['presentation_currency'],
            framework=source_node.framework, source_metric=list(source_metric),
            input_path=list(input_path), input_sign=input_sign, output_metric=list(output_metric), value=copy.deepcopy(value),
            rate_source=copy.deepcopy(native['currency']['rate_source']),
            rate_population=copy.deepcopy(t), evidence=list(evidence), currentness='CURRENT')
        if self.session.graph.nodes[target.node_id].framework != source_node.framework:
            raise ValueError('FX translation cannot change accounting framework')
        self.history.append(record)
        return copy.deepcopy(record)

    def unsupported_conversion(self, source_version, target_framework, economic_id):
        source = self.session.versions.require_current(source_version)
        return dict(status='unresolved', source_version=source_version,
            source_scope=source.scope_id, source_period=source.period_id,
            target_framework=target_framework, economic_id=economic_id,
            accounting_authority=False, owner=None,
            reason='No qualified production contract for general framework conversion')

    def intercompany_conversion(self, source_version, conversion_version, economic_id, source_metric, evidence):
        """Qualified ordinary reciprocal-balance IFRS reassessment; zero adjustment.

        The existing IC owner independently certifies original principal and
        both Group-currency legal carrying amounts. No general recognition or
        measurement conversion is implied by this bounded route.
        """
        from .runtime import at
        from decimal import Decimal
        source = self.session.versions.require_current(source_version)
        target = self.session.versions.require_current(conversion_version)
        original = self._native(source, 'foreign-currency')
        native = self._native(target, 'intercompany-accounting')
        sn = self.session.graph.nodes[source.node_id]
        tn = self.session.graph.nodes[target.node_id]
        if source_version not in [v for _, v in target.dependency_bindings] or not economic_id or not evidence:
            raise ValueError('Exact conversion source dependency/evidence required')
        if sn.framework == tn.framework or tn.scope_type != 'GROUP' or tn.framework != 'IFRS':
            raise ValueError('Unsupported ordinary intercompany conversion route')
        if original['translation']['operation_id'] != economic_id or native.get('conversion_economic_id') != economic_id:
            raise ValueError('Conversion economic identity differs')
        if original['currency']['presentation'] != tn.presentation_currency or tuple(source_metric)[:3] != ('calculations', 'translation', 'translated_tb'):
            raise ValueError('Qualified common presentation-currency input required')
        if len(native['pairs']) != 1 or native['recharges'] or native['pairs'][0]['transaction_id'] != economic_id:
            raise ValueError('General framework conversion remains unresolved')
        pair = native['pairs'][0]
        if Decimal(str(at(source.payload(), source_metric))) != Decimal(pair['gl_a']):
            raise ValueError('IFRS owner legal carrying input differs from qualified translation')
        from .stage3 import validate_native_bindings
        receipts=[self.session.receipt(k) for k,e in sorted(self.session.edges.items()) if e.consumer_node==target.node_id]
        validate_native_bindings(self.session,tn,native,receipts)
        record = dict(kind='FRAMEWORK_CONVERSION', source_version=source_version,
            source_scope=source.scope_id, source_period=source.period_id,
            source_framework=sn.framework, target_framework=tn.framework,
            currency=tn.presentation_currency, owner='intercompany-accounting',
            result_version=conversion_version, economic_id=economic_id,
            semantic_metric='ordinary_reciprocal_balance', adjustment='0',
            consumer_scope=target.scope_id, consumer_period=target.period_id,
            evidence=list(evidence), currentness='CURRENT',
            limitation='Native ordinary IC reassessment only; not a general GAAP converter')
        self.history.append(record)
        return copy.deepcopy(record)

    def validate_transformation(self, record):
        if not isinstance(record, dict) or record.get('currentness') != 'CURRENT':
            raise ValueError('Typed current transformation receipt required')
        start = len(self.history)
        try:
            if record.get('kind') == 'CURRENCY_TRANSLATION':
                expected = self.translation(record['source_version'], record['result_version'],
                    record['economic_id'], tuple(record['source_metric']), tuple(record['input_path']),
                    tuple(record['output_metric']), record['evidence'], record.get('input_sign',1))
            elif record.get('kind') == 'FRAMEWORK_CONVERSION' and record.get('owner') == 'intercompany-accounting':
                expected = self.intercompany_conversion(record['source_version'],record['result_version'],
                    record['economic_id'],('calculations','translation','translated_tb','ic loan'),record['evidence'])
            else:
                raise ValueError('Unsupported transformation receipt')
            if expected != record:
                raise ValueError('Substituted transformation receipt')
        finally:
            del self.history[start:]
        return self.session.versions.require_current(record['result_version'])

    def current_journals(self, context, events, translation_dispositions):
        """Use inherited scoped gross-line allocation with witnessed translation.

        Native translation journals already embodied in the owner-qualified
        Group source TB are evidence, not additional legal or Group postings.
        """
        from .scoped_journals import allocate_scoped
        from .runtime import at
        session = self.session
        native = []
        witnessed = set()
        for disposition in translation_dispositions:
            if set(disposition) != {'translation_version','group_version','source_path','evidence'} or not disposition['evidence']:
                raise ValueError('Explicit embedded translation disposition required')
            translated = session.versions.require_current(disposition['translation_version'])
            group = session.versions.require_current(disposition['group_version'])
            self._native(translated,'foreign-currency');group_source=self._native(group,'consolidation')
            if translated.version_id not in [v for _,v in group.dependency_bindings]:
                raise ValueError('Group lacks exact translation dependency')
            population = translated.payload()['calculations']['translation']['translated_tb']
            path=tuple(disposition['source_path'])
            if len(path)!=3 or path[0]!='entities' or type(path[1]) is not int or path[2]!='balances' or group_source['entities'][path[1]]['id']!=translated.scope_id:
                raise ValueError('Embedded translation disposition must bind actual source legal entity')
            actual = at(group_source,path)
            from decimal import Decimal
            accounts=group_source['cta_bridge']['cta_accounts']
            if len(accounts)!=1 or accounts[0] not in actual or Decimal(str(actual[accounts[0]]))!=-Decimal(str(translated.payload()['calculations']['translation']['closing_cta'])):
                raise ValueError('Embedded CTA must equal qualified owner closing reserve')
            if set(actual)!=set(population)|set(accounts) or any(actual.get(k) != v for k,v in population.items()):
                raise ValueError('Embedded translation population differs')
            if translated.node_id in witnessed:
                raise ValueError('Duplicate translation disposition')
            witnessed.add(translated.node_id)
        for key in sorted(session.versions.active):
            version=session.versions.require_current(session.versions.current(key).version_id)
            node=session.graph.nodes[key];payload=version.payload();journals=payload.get('journal_entry_implications',[])
            if not journals:continue
            if node.selected_skill=='foreign-currency':
                if key not in witnessed:
                    raise ValueError('Translation cannot post as underlying legal economics')
                continue
            if node.selected_skill=='intercompany-accounting' and any(entity!=node.scope_id for entity in payload['calculations']['journal_entities']):
                raise ValueError('Local IC journal entity differs from producing legal book')
            native.append(dict(owner=node.selected_skill,node=key,economic_id=node.economic_id,
                source_scope=node.scope_id,posting_scope=node.scope_id,accounting_layer=node.scope_type,
                currency=node.functional_currency or node.presentation_currency,period=node.period,
                period_id=node.period_id,result_version=version.version_id,journals=journals))
        for event in events:
            version=session.versions.require_current(event['result_version'])
            if (version.scope_id,version.period_id)!=(event['posting_scope'],event['period_id']):
                raise ValueError('Posting dimensions differ from exact result version')
            if any(ref['owner']!=version.node_id for ref in event['primary']+[r for w in event['witnesses'] for r in w]):
                raise ValueError('Wrong result-version journal reference')
        return allocate_scoped(native,context,events)

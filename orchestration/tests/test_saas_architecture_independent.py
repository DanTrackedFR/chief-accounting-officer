"""Independent architecture boundary and remediation regressions.

Original unqualified FX and additive journal-mapping counterexamples remain.
Semantic family gaps are now positive routing contract regressions.
"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from orchestration.registry import ROOT
from orchestration.planning import FACT_ADAPTERS
from orchestration.runtime import CAO, Case, Graph, Node, digest
from core_accounting import ReviewRequired


def workflow(package):
    spec = importlib.util.spec_from_file_location('independent_'+package.replace('-', '_'), ROOT/'skills'/package/'workflow.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def example(package, filename):
    return json.loads((ROOT/'skills'/package/'examples'/filename).read_text())


class SaaSArchitectureIndependent(unittest.TestCase):
    def test_ar_foreign_invoice_is_explicitly_unsupported_not_silently_converted(self):
        case = example('accounts-receivable', 'IFRS.case.json')
        case['invoices'][0]['currency'] = 'USD'
        with self.assertRaisesRegex(ReviewRequired, 'currency unsupported|Missing required facts'):
            workflow('accounts-receivable').assess(case, [])

    def test_ar_gl_remeasurement_has_no_supported_movement_slot(self):
        case = example('accounts-receivable', 'IFRS.case.json')
        case['gl_ar'] = str(int(case['gl_ar']) + 5)
        # Extra unconsumed input cannot qualify a currency remeasurement.
        case['fx_movement'] = '5'
        with self.assertRaisesRegex(ReviewRequired, 'AR subledger to GL'):
            workflow('accounts-receivable').assess(case, [])

    def test_ar_and_ecl_have_semantic_fact_families(self):
        owners = {owner for owner, _ in FACT_ADAPTERS.values()}
        self.assertIn('accounts-receivable', owners)
        self.assertIn('financial-instruments-ecl', owners)

    def test_revenue_and_ar_both_emit_billing_and_cash_journals(self):
        rev = workflow('revenue-recognition').assess(example('revenue-recognition', 'ifrs-case.json'), [])
        ar = workflow('accounts-receivable').assess(example('accounts-receivable', 'IFRS.case.json'), [])
        def roles(result):
            return [(j[0]['side'], j[0]['account']) for j in result['journal_entry_implications']]
        self.assertIn(('Dr', 'receivable'), roles(rev))
        self.assertIn(('Dr', 'cash'), roles(rev))
        self.assertIn(('Dr', 'accounts receivable'), roles(ar))
        self.assertIn(('Dr', 'cash'), roles(ar))

    def test_reporting_mapping_cannot_suppress_duplicate_economic_event(self):
        # Minimal immutable reviewed owner envelopes for one shared billing event.
        graph = Graph()
        journal_rev = [[{'side':'Dr','account':'receivable','amount':'100'}, {'side':'Cr','account':'contract clearing','amount':'100'}]]
        journal_ar = [[{'side':'Dr','account':'accounts receivable','amount':'100'}, {'side':'Cr','account':'contract balance','amount':'100'}]]
        for package, journals in [('revenue-recognition', journal_rev), ('accounts-receivable', journal_ar)]:
            node = Node(package, 'actual supported billing', package, 'billing', 'E', 'IFRS', ['2026-01-01','2026-01-31'])
            node.status='complete'; node.result={'case_fingerprint':package,'journal_entry_implications':journals}
            graph.add(node)
        reporting=Node('fs','reporting','financial-statements','actual statements','E','IFRS',['2026-01-01','2026-01-31'])
        graph.add(reporting)
        mapping={'receivable':'AR','accounts receivable':'AR','contract clearing':'CL','contract balance':'CL'}
        native=[dict(owner=n.selected_skill,case_fingerprint=n.result['case_fingerprint'],journals=n.result['journal_entry_implications']) for n in graph.nodes.values() if n.status=='complete']
        request={'journal_account_mapping':mapping,'journal_pack_review':{'payload_fingerprint':digest(dict(mapping=mapping,native_owner_journals=native)),'approved':True,'preparer':'P','reviewer':'R'}}
        source={'current_tb':[{'id':'AR','balance':'100'},{'id':'CL','balance':'-100'}], 'comparative_tb':[{'id':'AR','balance':'0'},{'id':'CL','balance':'0'}]}
        with self.assertRaisesRegex(ValueError, 'disagree with reviewed statement GL movement'):
            CAO()._journal_mapping(None,graph,{reporting.id:source},request,reporting)

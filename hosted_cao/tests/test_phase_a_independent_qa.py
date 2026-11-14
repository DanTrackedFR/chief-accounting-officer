"""Independent Phase A API challenge. Authenticated HTTP and durable native store.

Synthetic scenarios authored by engineering QA. Expected monetary values are
literal independent calculations, not calls into the implementation formula.
"""
import copy
import hashlib
from decimal import Decimal
import json
import unittest
from hosted_cao.tests.test_presumed_engineering_qa import (
    IndependentPresumedEngineeringQA as Harness, synthetic_case, supplied,
)


# Exact synthetic accepted-main HTTP guidance, independently captured at97d0621.
LEGACY_GUIDANCE = 'Nally calculated these results using the information you provided.\nOrdinary machinery uses the governed cost method; depreciation starts when available for use (IAS 16, ASC 360, FRS 102 Section 17 or AASB 116, as applicable).\nCalculated valid rows are bounded by the supplied file; excluded rows are not included in a complete population total.\nNo policy elections were assumed.\nSupplied class defaults: {"machinery": {"method": "straight_line", "remaining_life": "10", "residual": "0", "scope": "ordinary_ppe"}}\nApplied row assumptions: [{"assumptions": {"method": "straight_line", "remaining_life": "10", "residual": "0", "scope": "ordinary_ppe"}, "row_reference": "assets:1"}]\nExplicit user assumptions: []\nProposed journal implications: [[{"account": "depreciation expense", "amount": "1100.00", "side": "Dr"}, {"account": "accumulated depreciation", "amount": "1100.00", "side": "Cr"}]]'


class PhaseAIndependentQA(unittest.TestCase):
    # Reuse transport/lifecycle, never inherit the prior review's test methods.
    setUp = Harness.setUp
    new_service = Harness.new_service
    close = Harness.close
    envelope = Harness.envelope
    http = Harness.http
    call = Harness.call
    start = Harness.start
    stage = Harness.stage
    job = Harness.job
    complete = Harness.complete
    native = Harness.native
    assert_amount = Harness.assert_amount

    def test_all_scope_fields_reject_actionably_without_staging(self):
        for field in ('entity', 'jurisdiction', 'framework', 'period_start',
                      'reporting_period', 'functional_currency'):
            for variant, value in (('missing', None), ('null', None), ('empty', ''),
                                   ('blank', ' \t '), ('type', 42)):
                with self.subTest(field=field, variant=variant):
                    case = synthetic_case(count=1)
                    if variant == 'missing':
                        case.pop(field)
                    else:
                        case[field] = value
                    cid = self.start(rid='independent-scope-'+field+'-'+variant)
                    status, response = self.call('submit', case_id=cid, evidence=supplied(case=case))
                    self.assertEqual(status, 422, response)
                    self.assertFalse(response['ok'])
                    needs = response['error']['requirements']
                    self.assertTrue(any(n['field_path'].endswith('.'+field) for n in needs), needs)
                    for need in needs:
                        self.assertTrue(all(need.get(k) for k in
                            ('identifier', 'field_path', 'explanation', 'category')), need)
                    folder=self.workspace/'submissions'/hashlib.sha256(cid.encode()).hexdigest()
                    self.assertFalse((folder/'evidence.json').exists(), 'Rejected identity must not persist staged evidence')
                    # Invalid submission is not made into an accounting result.
                    state = self.call('resume', case_id=cid)[1]
                    self.assertFalse(state.get('public_result', {}).get('proposed_journals'))
                    with self.service.db() as db:
                        self.assertEqual(db.execute('SELECT count(*) FROM jobs').fetchone()[0], 0)

    def test_independent_scope_and_row_defects_aggregate(self):
        case = synthetic_case(count=2)
        case.pop('entity');case['framework']=' ';case['functional_currency']=None
        case['assets'][0].pop('ready_date');case['assets'][1].pop('opening_accumulated')
        cid=self.start(rid='independent-scope-mixed')
        status,response=self.call('submit',case_id=cid,evidence=supplied(case=case))
        self.assertEqual(status,422,response)
        paths=[n['field_path'] for n in response['error']['requirements']]
        for field in ('entity','framework','functional_currency','ready_date','opening_accumulated'):
            self.assertTrue(any(path.endswith('.'+field) for path in paths),(field,paths))

    def test_real_identity_mismatch_stays_rejected(self):
        case=synthetic_case(count=1);case['entity']='OTHER-COMPANY'
        cid=self.start(rid='independent-wrong-entity')
        status,response=self.call('submit',case_id=cid,evidence=supplied(case=case))
        self.assertEqual(status,422,response)
        self.assertEqual(response['error']['code'],'identity_conflict')
        self.assertTrue(any(n['field_path'].endswith('.entity') for n in response['error']['requirements']))


    def test_year_month_equivalence_12_24_36_60_and_reopen(self):
        for months, expected in ((12,'18000'),(24,'9000'),(36,'6000'),(60,'3600')):
            for unit in ('years','months','both'):
                with self.subTest(months=months,unit=unit):
                    case=synthetic_case(count=1)
                    case['class_assumptions']['machinery'].pop('remaining_life')
                    asset=case['assets'][0];asset['opening_cost']='18000'
                    if unit in ('years','both'):asset['remaining_life']=str(Decimal(months)/12)
                    if unit in ('months','both'):asset['remaining_life_months']=str(months)
                    cid,done=self.complete(rid='independent-life-'+str(months)+'-'+unit,case=case)
                    public=done['accounting']['public_result'];self.assert_amount(public,'depreciation',expected)
                    self.assertEqual(self.call('resume',case_id=cid)[1]['public_result'],public)
                    # Repeated execution must reuse the same durable result.
                    status,again=self.job(cid,'independent-life-'+str(months)+'-'+unit)
                    self.assertEqual(status,202,again)
                    self.assertEqual(again['accounting']['public_result'],public)

    def test_life_diagnostics_distinct_and_rows_isolated(self):
        case=synthetic_case(count=7)
        case['class_assumptions']['machinery'].pop('remaining_life')
        for asset in case['assets']:asset['opening_cost']='18000'
        case['assets'][0]['remaining_life_months']='36'
        case['assets'][1]['remaining_life_months']='0'
        case['assets'][2]['remaining_life_months']='-1'
        case['assets'][3]['remaining_life_months']=None
        case['assets'][4]['remaining_life_months']='banana'
        case['assets'][5].update(remaining_life='2',remaining_life_months='36')
        # Row seven intentionally has neither field.
        cid,done=self.complete(rid='independent-life-diagnostics',case=case)
        public=done['accounting']['public_result'];self.assert_amount(public,'depreciation','6000')
        self.assertEqual(public['accounting_determination'],'UNRESOLVED')
        needs=public['validation_requirements']
        for row,word in ((2,'exhausted'),(3,'negative'),(4,'null'),(5,'nonnumeric'),(6,'conflicting'),(7,'missing')):
            self.assertTrue(any(n['field_path'].startswith('assets['+str(row)+'].') and word in n['explanation'].lower() for n in needs),(row,word,needs))
        native=self.native(cid)[1]
        self.assertEqual(len(native['proposed_journal_workpaper']),1)
        self.assertEqual(Decimal(native['proposed_journal_workpaper'][0][0]['amount']),Decimal('6000'))
        self.assertEqual(self.call('resume',case_id=cid)[1]['public_result'],public)

    def test_invalid_units_do_not_choose_a_life(self):
        case=synthetic_case(count=1)
        case['assets'][0].update(remaining_life='2',remaining_life_unit='months')
        cid,done=self.complete(rid='independent-life-unsupported-unit',case=case)
        public=done['accounting']['public_result']
        self.assertEqual(public['accounting_determination'],'UNRESOLVED')
        self.assertTrue(any(n['field_path']=='assets[1].remaining_life_unit' for n in public['validation_requirements']))
        self.assertFalse(self.native(cid)[1]['proposed_journal_workpaper'])

    def test_fully_depreciated_in_use_never_disposed_automatically(self):
        case=synthetic_case(count=1)
        case['assets'][0].update(opening_cost='18000',opening_accumulated='18000',remaining_life='0')
        cid,done=self.complete(rid='independent-fully-depreciated',case=case)
        native=self.native(cid)[1]
        self.assertFalse(native['proposed_journal_workpaper'])
        self.assertFalse(done['accounting']['public_result'].get('proposed_journals'))
        self.assertIn('not automatically disposed',json.dumps(done['accounting']['public_result']).lower())


    def monthly_scope(self,start='2026-05-01',end='2026-05-31'):
        path=self.workspace/'company-context.md'
        text=path.read_text()
        import re
        text=re.sub(r'period_start: [0-9-]+','period_start: '+start,text)
        text=re.sub(r'period_end: [0-9-]+','period_end: '+end,text)
        path.write_text(text)
        case=synthetic_case(count=1)
        case.update(period_start=start,reporting_period=end)
        case['assets'][0].update(opening_cost='18000',remaining_life_months='36')
        return case

    def test_monthly_actual_and_legacy_may_and_february(self):
        for start,end,actual in (('2026-05-01','2026-05-31','509.59'),('2026-02-01','2026-02-28','460.27')):
            for convention,expected in (('monthly','500'),('actual_days',actual),(None,actual)):
                case=self.monthly_scope(start,end)
                if convention:case['policy_elections']={'depreciation_convention':convention}
                case['assets'][0]['expected_depreciation']=expected
                cid,done=self.complete(rid='independent-period-'+start+'-'+str(convention),case=case)
                public=done['accounting']['public_result'];self.assert_amount(public,'depreciation',expected)
                checks=[f for f in public['anomaly_report']['findings'] if f['check_id']=='depreciation_comparison']
                self.assertEqual([f['severity'] for f in checks],['PASS'])
                self.assertIn('Monthly depreciation is recommended',public['guidance'])
                self.assertEqual(self.call('resume',case_id=cid)[1]['public_result'],public)

    def test_monthly_partial_requires_election_and_midmonth_use(self):
        case=self.monthly_scope();case['assets'][0]['ready_date']='2026-05-17'
        case['policy_elections']={'depreciation_convention':'monthly'}
        cid,done=self.complete(rid='independent-midmonth-unconfirmed',case=case)
        public=done['accounting']['public_result']
        self.assertEqual(public['accounting_determination'],'UNRESOLVED')
        self.assertFalse(self.native(cid)[1]['proposed_journal_workpaper'])
        self.assertTrue(any(n['field_path']=='policy_elections.partial_month_treatment' for n in public['validation_requirements']))
        case['policy_elections']['partial_month_treatment']='actual_days_in_month'
        cid,done=self.complete(rid='independent-midmonth-explicit',case=case)
        self.assert_amount(done['accounting']['public_result'],'depreciation','241.94')
        self.assertEqual(len(self.native(cid)[1]['proposed_journal_workpaper']),1)

    def test_confirmed_policy_reuse_and_conflict(self):
        case=self.monthly_scope()
        case['asset_policy']={'depreciation_convention':'monthly','confirmation':'confirmed',
            'entity':case['entity'],'framework':case['framework'],'effective_from':'2026-01-01',
            'effective_to':'2026-12-31','policy_version':'independent-company-policy-7'}
        for i in (1,2):
            cid,done=self.complete(rid='independent-company-policy-'+str(i),case=case)
            self.assert_amount(done['accounting']['public_result'],'depreciation','500')
        case['policy_elections']={'depreciation_convention':'actual_days'}
        cid,done=self.complete(rid='independent-policy-conflict',case=case)
        public=done['accounting']['public_result']
        self.assertEqual(public['accounting_determination'],'UNRESOLVED')
        self.assertTrue(any('conflict' in n['explanation'].lower() for n in public['validation_requirements']))
        self.assertFalse(self.native(cid)[1]['proposed_journal_workpaper'])

    def test_monthly_disposal_and_final_period_cap(self):
        case=self.monthly_scope()
        case['policy_elections']={'depreciation_convention':'monthly','partial_month_treatment':'actual_days_in_month'}
        case['assets'][0]['disposal']={'enabled':True,'date':'2026-05-17','proceeds':'16000','ordinary_sale':True,'cash_received':True}
        cid,done=self.complete(rid='independent-monthly-disposal',case=case)
        self.assert_amount(done['accounting']['public_result'],'depreciation','274.19')
        self.assert_amount(done['accounting']['public_result'],'closing cost','0')
        self.assert_amount(done['accounting']['public_result'],'closing accumulated','0')
        case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
        case['assets'][0].update(opening_cost='1000',residual='100',remaining_life_months='0.25')
        cid,done=self.complete(rid='independent-final-period-cap',case=case)
        self.assert_amount(done['accounting']['public_result'],'depreciation','900')
        self.assert_amount(done['accounting']['public_result'],'closing accumulated','900')


    def test_balance_comparisons_opening_closing_and_journals_unchanged(self):
        original=self.monthly_scope();original['policy_elections']={'depreciation_convention':'monthly'}
        original['assets'][0]['opening_accumulated']='3000'
        cid,done=self.complete(rid='independent-comparison-baseline',case=original)
        baseline=self.native(cid)[1]['proposed_journal_workpaper']
        for basis,nbv,acc in (('opening','15000','3000'),('closing','14583.33','3416.67')):
            case=copy.deepcopy(original);case['assets'][0].update(comparison_balance_basis=basis,
                supplied_net_book_value=nbv,supplied_accumulated_depreciation=acc)
            cid,done=self.complete(rid='independent-balances-'+basis,case=case)
            public=done['accounting']['public_result'];comparisons=public['balance_comparisons']
            self.assertEqual(len(comparisons),3)
            self.assertTrue(all(c['status']=='MATCH' for c in comparisons),comparisons)
            self.assertTrue(all(c['balance_basis']==basis and Decimal(c['variance'])==0 for c in comparisons))
            self.assertEqual(self.native(cid)[1]['proposed_journal_workpaper'],baseline)
            self.assertEqual(self.call('resume',case_id=cid)[1]['public_result'],public)
        case=copy.deepcopy(original);case['assets'][0].update(comparison_balance_basis='closing',
            supplied_net_book_value='274583.33',supplied_accumulated_depreciation='3416.67')
        cid,done=self.complete(rid='independent-large-balance-error',case=case)
        comparisons=done['accounting']['public_result']['balance_comparisons']
        self.assertTrue(any(c['status']=='MISMATCH' and Decimal(c['variance'])==Decimal('260000') for c in comparisons))
        self.assertEqual(self.native(cid)[1]['proposed_journal_workpaper'],baseline)

    def test_ambiguous_or_malformed_comparisons_do_not_override_calculation(self):
        for index,value in enumerate(('14500','not-an-amount',None)):
            case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
            case['assets'][0]['supplied_net_book_value']=value
            cid,done=self.complete(rid='independent-invalid-comparison-'+str(index),case=case)
            public=done['accounting']['public_result'];self.assert_amount(public,'depreciation','500')
            self.assertEqual(public['accounting_determination'],'UNRESOLVED')
            self.assertEqual(len(self.native(cid)[1]['proposed_journal_workpaper']),1)
            self.assertTrue(public['validation_requirements'])
            self.assertIn(public['balance_comparisons'][0]['status'],('UNRESOLVED_BASIS','INVALID'))

    def test_public_journals_match_native_and_assumptions_have_real_provenance(self):
        case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
        case['assets'][0].update(residual='1800',remaining_life_months='36')
        cid,done=self.complete(rid='independent-structured-workpaper',case=case)
        public=done['accounting']['public_result'];native=self.native(cid)[1]
        journals=public['proposed_journals'];self.assertEqual(len(journals),1)
        self.assertEqual(journals[0]['lines'],[{**line,'amount':str(line['amount'])} for line in native['proposed_journal_workpaper'][0]])
        self.assertEqual(Decimal(journals[0]['lines'][0]['amount']),Decimal('450'))
        for journal in journals:
            for field in ('journal_reference','case_reference','row_reference','currency',
                          'period_start','reporting_period','accounting_determination',
                          'qualification_status','source_reference'):
                self.assertTrue(journal.get(field),(field,journal))
            self.assertEqual(journal['qualification_status'],'PROPOSED')
            self.assertEqual(journal['row_reference'],'assets:1')
            self.assertEqual(journal['currency'],'EUR')
            self.assertEqual(sum((Decimal(l['amount']) if l['side']=='Dr' else -Decimal(l['amount']) for l in journal['lines']),Decimal(0)),Decimal(0))
        assumptions=public['applied_assumptions']
        for field,value in (('depreciation_convention','monthly'),('remaining_life_months','36'),('residual','1800')):
            self.assertTrue(any(a['field']==field and a['value']==value for a in assumptions),(field,assumptions))
        convention=[a for a in assumptions if a['field']=='depreciation_convention']
        self.assertTrue(all(a['provenance']=='case_election' for a in convention),convention)
        # A changed explanatory sentence must not change journal projection.
        from source_execution import to_public
        changed=copy.deepcopy(native);changed['conclusion']='Independent wording.'
        self.assertEqual(to_public(changed,'tool_output')['proposed_journals'],journals)
        self.assertEqual(self.call('resume',case_id=cid)[1]['public_result'],public)
        repeated=self.job(cid,'independent-structured-workpaper')[1]
        self.assertEqual(repeated['accounting']['public_result'],public)
        self.assertEqual(repeated['attempts'],1)
        encoded=json.dumps(public)
        self.assertNotIn(case['source']['hash'],encoded)
        self.assertNotIn(case['source_attestation']['authenticated_user_reference'],encoded)
        self.assertIn('no posting is authorized',encoded.lower())
        self.assertFalse(native['journal_entry_implications'])

    def test_public_journals_exclude_invalid_rows_and_no_cross_case_amounts(self):
        case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
        invalid=copy.deepcopy(case['assets'][0]);invalid.update(id='INVALID-ASSET',remaining_life_months='-3')
        case['assets'].append(invalid)
        cid,done=self.complete(rid='independent-isolation-first',case=case)
        public=done['accounting']['public_result']
        self.assertEqual(len(public['proposed_journals']),1)
        self.assertEqual(public['proposed_journals'][0]['row_reference'],'assets:1')
        self.assertEqual(Decimal(public['proposed_journals'][0]['lines'][0]['amount']),Decimal('500'))
        other=self.monthly_scope();other['policy_elections']={'depreciation_convention':'monthly'}
        other['assets'][0]['opening_cost']='36000'
        cid2,done2=self.complete(rid='independent-isolation-second',case=other)
        self.assertEqual(Decimal(done2['accounting']['public_result']['proposed_journals'][0]['lines'][0]['amount']),Decimal('1000'))
        self.assertEqual(self.call('resume',case_id=cid)[1]['public_result'],public)
        self.assertNotEqual(cid,cid2)


    def test_public_contract_curation_rejects_invalid_authority_and_provenance(self):
        from interfaces.public_output import public_record,ROUTES
        from pathlib import Path
        case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
        cid,done=self.complete(rid='independent-public-boundary',case=case)
        public=done['accounting']['public_result']
        schema=json.loads((Path(__file__).resolve().parents[2]/'interfaces/public-answer.schema.json').read_text())
        self.assertFalse(set(public)-set(schema['properties']))
        for field in ('proposed_journals','applied_assumptions','balance_comparisons'):
            self.assertEqual(schema['properties'][field]['type'],'array')
        for route in ROUTES:
            self.assertEqual(public_record(public,route=route),public)
        attacks=[]
        p=copy.deepcopy(public);p['proposed_journals'][0]['lines'][0]['amount']='NaN';attacks.append(p)
        p=copy.deepcopy(public);p['proposed_journals'][0]['lines'][0]['amount']='999';attacks.append(p)
        p=copy.deepcopy(public);p['proposed_journals'][0]['qualification_status']='AUTHORIZED';attacks.append(p)
        p=copy.deepcopy(public);p['proposed_journals'][0]['accounting_determination']='UNRESOLVED';attacks.append(p)
        p=copy.deepcopy(public);p['applied_assumptions'][0]['provenance']='confirmed_user_policy';attacks.append(p)
        p=copy.deepcopy(public);p['proposed_journals'][0]['source_reference']=case['source']['hash'];attacks.append(p)
        p=copy.deepcopy(public);p.pop('source_provenance');attacks.append(p)
        for i,attack in enumerate(attacks):
            with self.subTest(attack=i):
                with self.assertRaises(ValueError):public_record(attack,route='tool_output')

    def test_defaults_disclosed_and_company_policy_not_fabricated(self):
        case=self.monthly_scope()
        cid,done=self.complete(rid='independent-default-provenance',case=case)
        assumptions=done['accounting']['public_result']['applied_assumptions']
        actual=[a for a in assumptions if a['field']=='depreciation_convention']
        self.assertEqual(len(actual),1)
        self.assertEqual(actual[0]['value'],'actual_days')
        self.assertEqual(actual[0]['provenance'],'engine_default_unconfirmed')
        self.assertFalse(any(a['provenance']=='confirmed_company_policy_client_asserted' for a in assumptions))


    def test_fingerprint_bridge_rejects_helper_and_witness_tampering(self):
        from pathlib import Path
        from unittest.mock import patch
        import production
        from local_cao.tests.test_authored import evidence
        from hosted_cao.tests.test_prepared_engineering_qa import prepared_evidence
        root=Path(__file__).resolve().parents[2]
        read_bytes=Path.read_bytes
        for name,case in (('formal',evidence('fixed-assets')['facts']['machinery']),
                          ('profile11',prepared_evidence('fixed-assets')['facts']['machinery'])):
            if name=='profile11':case.update(review_mode='prepared_unreviewed')
            baseline=production.case_fingerprint(case)
            for filename in ('skills/phase_a_fingerprint.py',
                'skills/phase-a-compatibility/accepted-main-production.py.txt',
                'skills/phase-a-compatibility/accepted-main-public_output.py.txt',
                'interfaces/public_output.py'):
                target=root/filename
                def mutated(path,*args,**kwargs):
                    value=read_bytes(path,*args,**kwargs)
                    return value+b'\n# independent tamper challenge\n' if path==target else value
                with self.subTest(profile=name,file=filename),patch.object(Path,'read_bytes',mutated):
                    self.assertNotEqual(production.case_fingerprint(case),baseline)
        case=synthetic_case(count=1);case.update(package='fixed-assets',review_mode='prepared_unreviewed',source_assurance='presumed_user_provided')
        baseline=production.case_fingerprint(case)
        for filename in ('skills/phase_a_fingerprint.py','interfaces/source-case.schema.json','skills/source_execution.py','interfaces/public_output.py'):
            target=root/filename
            def mutated(path,*args,**kwargs):
                value=read_bytes(path,*args,**kwargs)
                return value+b'\n# independent new-source tamper challenge\n' if path==target else value
            with self.subTest(profile='profile12',file=filename),patch.object(Path,'read_bytes',mutated):
                self.assertNotEqual(production.case_fingerprint(case),baseline)


    def test_identical_capital_journals_keep_only_valid_row_lineage(self):
        case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
        case['assets'][0]['ready_date']='2026-05-01'
        invalid=copy.deepcopy(case['assets'][0]);invalid.update(id='SECOND-INVALID',remaining_life_months='-1')
        case['assets'].append(invalid)
        case['costs']=[dict(id='COST-VALID',amount='100',kind='purchase',date='2026-05-01',offset='accounts payable',destination=case['assets'][0]['id']),
                       dict(id='COST-INVALID',amount='100',kind='purchase',date='2026-05-01',offset='accounts payable',destination='SECOND-INVALID')]
        cid,done=self.complete(rid='independent-identical-capital-entries',case=case)
        public=done['accounting']['public_result']
        self.assert_amount(public,'depreciation','502.78')
        self.assertEqual([j['row_reference'] for j in public['proposed_journals']],['costs:1','assets:1'])
        self.assertEqual([j['asset_or_transaction_reference'] for j in public['proposed_journals']],['COST-VALID',case['assets'][0]['id']])
        self.assertEqual(len(self.native(cid)[1]['proposed_journal_workpaper']),2)
        self.assertIn('costs:2',public['anomaly_report']['excluded_rows'])

    def test_accounts_payable_structured_journals_keep_valid_invoice_only(self):
        case=synthetic_case('accounts-payable',count=2)
        case['invoices'][0]['amount']='271.19'
        case['invoices'][1]['amount']='-9'
        cid,done=self.complete('accounts-payable',rid='independent-AP-public',case=case)
        public=done['accounting']['public_result']
        self.assert_amount(public,'invoices','271.19')
        self.assertEqual(len(public['proposed_journals']),1)
        self.assertEqual(public['proposed_journals'][0]['row_reference'],'invoices:1')
        native=self.native(cid)[1]['proposed_journal_workpaper'][0]
        self.assertEqual(public['proposed_journals'][0]['lines'],[{**line,'amount':str(line['amount'])} for line in native])
        self.assertEqual(Decimal(native[0]['amount']),Decimal('271.19'))
        self.assertTrue(any(a['field']=='recognition_basis' for a in public['applied_assumptions']))


    def test_structured_results_survive_new_host_instance_over_http(self):
        import threading
        from hosted_cao.service import Server
        case=self.monthly_scope();case['policy_elections']={'depreciation_convention':'monthly'}
        cid,done=self.complete(rid='independent-restarted-host',case=case)
        public=done['accounting']['public_result']
        restarted=self.new_service();server=Server(('127.0.0.1',0),restarted)
        thread=threading.Thread(target=server.serve_forever);thread.start()
        original=self.server
        try:
            self.server=server
            status,reopened=self.http('/v1/jobs/'+done['id'])
            self.assertEqual(status,200,reopened)
            self.assertEqual(reopened['accounting']['public_result'],public)
            status,resumed=self.call('resume',case_id=cid)
            self.assertEqual(status,200,resumed)
            self.assertEqual(resumed['public_result'],public)
            self.assertEqual(reopened['attempts'],1)
            self.assertFalse(restarted.run_one())
        finally:
            self.server=original
            server.shutdown();server.server_close();thread.join();restarted.close()


    def test_historical_native_contract_keeps_workpaper_and_guidance(self):
        from source_execution import to_public
        case=synthetic_case(count=1)
        cid,_=self.complete(rid='independent-historical-contract-shape',case=case)
        historical=copy.deepcopy(self.native(cid)[1])
        historical.pop('execution_case_reference',None)
        historical['calculations'].pop('journal_rows',None)
        historical['calculations'].pop('balance_comparisons',None)
        for asset in historical['calculations']['assets']:
            asset.pop('applied_depreciation_policy',None)
        before=json.dumps(historical,sort_keys=True,default=str)
        projected=to_public(historical,'tool_output')
        self.assertEqual(projected['guidance'],LEGACY_GUIDANCE)
        self.assertEqual(projected['proposed_journals'],[])
        self.assertTrue(any(n['identifier']=='integration.historical_journal_lineage' for n in projected['validation_requirements']))
        self.assertTrue(any('historical' in limitation.lower() for limitation in projected['limitations']))
        self.assertEqual(json.dumps(historical,sort_keys=True,default=str),before)
        self.assertTrue(historical['proposed_journal_workpaper'])

    def test_units_of_production_does_not_claim_calendar_policy_used(self):
        case=synthetic_case(count=1)
        case['assets'][0].update(method='units_of_production',remaining_units='1000',period_units='100')
        cid,done=self.complete(rid='independent-units-provenance',case=case)
        public=done['accounting']['public_result'];self.assert_amount(public,'depreciation','1100')
        self.assertFalse(any(a['field']=='depreciation_convention' for a in public['applied_assumptions']))
        self.assertNotIn('Applied depreciation convention:',public['guidance'])
        self.assertTrue(any(a['field']=='period_units' and a['value']=='100' for a in public['applied_assumptions']))


# unittest module discovery must not collect the imported historical harness.
del Harness

if __name__ == '__main__':
    unittest.main()

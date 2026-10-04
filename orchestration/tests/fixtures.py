"""Controlled synthetic factory sources; fixture-only approval generation.

All input preparation lives in tests, never in the runtime. Synthetic reviewed
cases contain actual native completed owner outputs and independently labelled
source records. They are not authorization records for a real company.
"""
import copy
import sys
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/tests'))
from inventory_cases import case as inventory_case, ready as inventory_ready, sources, content, replace_doc, row, document, disclosure_support
from operational_cases import operational
from additional_cases import certify, fx, reporting
from financing_cases import case as benefits_case, ready as benefits_ready
from cases import revenue
from governance_cases import case as governance_case, ready as governance_ready, source_index, refresh_release
from final_batch_cases import case as practice_case, ready as practice_ready
from production import assess_case, case_fingerprint


def completed(pkg,c):
    r=assess_case(pkg,c)
    if r['status']!='complete': raise AssertionError((pkg,r['conclusion'],r['open_items']))
    return r


def manufacturing(with_fx=True):
    inv=inventory_case(); owners={}
    for pkg in ('fixed-assets','accounts-payable'):
        c=operational(pkg);c['functional_currency']='USD'
        for k in ('invoices','payments'):
            for r in c.get(k,[]):r['currency']='USD'
        if pkg=='accounts-payable':
            c['accruals']=[];c['gl_accrual']='0';c['controls'].update(population_count=1,population_amount='120')
        owners[pkg]=certify(pkg,c)
    c=benefits_case('employee-benefits-payroll');c['functional_currency']='USD'
    owners['employee-benefits-payroll']=benefits_ready('employee-benefits-payroll',c=c)
    costs={'employee-benefits-payroll':(0,'10800',['expense'],'labour'),
           'accounts-payable':(1,'120',['invoices'],'ap'),
           'fixed-assets':(2,'90000',['depreciation'],'depreciation')}
    for pkg,(idx,amount,path,kind) in costs.items():
        target=inv['costs'][idx];target.update(amount=amount,owner_import='actual-'+pkg,owner_kind=kind)
        b=content(inv,target['source_doc']);b.update(amount=amount,currency='USD',eligible_manufacturing=True,
            production_mapping_memo='Synthetic actual factory cost-centre allocation',cost_qualification_memo='Synthetic eligible conversion cost reviewed')
        if idx==0:target['rate']='540';b['rate']='540'
        inv['imports'].append(row(inv,'actual-'+pkg,package=pkg,case=owners[pkg],result=completed(pkg,owners[pkg]),mode='evidence_only'))
        inv['owner_links'].append(row(inv,'link-'+pkg,owner_import='actual-'+pkg,result_path=path,economic_id=target['economic_id'],target_id=target['id'],amount=amount,source_doc=target['source_doc'],source_field='amount'))
    total=Decimal('600')+Decimal('10800')+Decimal('120')+Decimal('45000')
    wip=total/5;fg=total*Decimal('.8');cogs=total/5
    inv['orders'][0].update(closing_wip_cost=str(wip),completed_cost=str(fg))
    inv['movements'][1]['amount']=str(fg);inv['movements'][2]['amount']=str(cogs)
    inv['items'][1]['closing_cost']=str(wip);inv['items'][2]['closing_cost']=str(fg-cogs)
    changes={'Work in progress':wip,'Finished goods':fg-cogs,'Labour clearing':Decimal('-10800'),
        'Overhead clearing':Decimal('-90120'),'Unallocated overhead expense':Decimal('45000'),'Cost of goods sold':cogs}
    for g in inv['gl']:
        if g['id'] in changes:g.update(closing=str(changes[g['id']]),statement=str(changes[g['id']]))
    rm=Decimal('400')
    if with_fx:
        c=fx();c['currency'].update(functional='USD',presentation='USD',ledger='USD');c['translation']['enabled']=False
        c['items'][0].update(id='inventory-purchase',type='historical_nonmonetary',settled_foreign='0',settlement_date=None,account='Inventory acquisition',memo='Synthetic controlled imported component title purchase')
        owners['foreign-currency']=certify('foreign-currency',c)
        amount='110';m=row(inv,'foreign-purchase',economic_id='economic-foreign-purchase',item='component',kind='purchase',quantity='10',amount=amount,date='2026-03-31',currency='USD',unit='units',source_doc='foreign-purchase-source',sequence=1,owner_import='actual-foreign-currency',owner_kind='fx')
        inv['movements'].insert(0,m)
        for i,mov in enumerate(inv['movements']):mov['sequence']=i+1
        document(inv,'foreign-purchase-source',dict(economic_id=m['economic_id'],item=m['item'],quantity='10',date=m['date'],ownership_supported=True,in_period=True,cost_components=[dict(id='price',economic_id='price-foreign-purchase',kind='price',amount=amount)],amount=amount,currency='USD',eligible_manufacturing=True,production_mapping_memo='Synthetic component lot matches FX historical acquisition',cost_qualification_memo='Supported historical translated purchase cost'))
        inv['imports'].append(row(inv,'actual-foreign-currency',package='foreign-currency',case=owners['foreign-currency'],result=completed('foreign-currency',owners['foreign-currency']),mode='evidence_only'))
        inv['owner_links'].append(row(inv,'link-foreign-currency',owner_import='actual-foreign-currency',result_path=['transactions','inventory-purchase','initial'],economic_id=m['economic_id'],target_id=m['id'],amount=amount,source_doc=m['source_doc'],source_field='amount'))
        rm+=Decimal(amount);inv['items'][0].update(closing_quantity='50',closing_cost=str(rm));inv['gl'][0].update(closing=str(rm),statement=str(rm))
        inv['gl'].append(row(inv,'Acquisition clearing',currency='USD',opening='0',closing='-110',statement='-110'))
        inv['count']['records'][0]['quantity']='50';replace_doc(inv,'count-source',inv['count']['records'])
        inv['cutoff']['records']=[dict(id=x['id'],economic_id=x['economic_id'],ownership_supported=True,date_reviewed=True) for x in inv['movements']];replace_doc(inv,'cutoff-source',inv['cutoff']['records'])
    inv['owner_links_inventory']=[x['id'] for x in inv['owner_links']];inv['gl_inventory']=[x['id'] for x in inv['gl']]
    inv['disclosures'].update(closing_inventory=str(rm+wip+fg-cogs),cogs=str(cogs));disclosure_support(inv)
    inv=inventory_ready(c=sources(inv));owners['inventory-cost']=inv;ir=completed('inventory-cost',inv)
    rev=revenue();rev['functional_currency']='USD';rev['price_components']['fixed']='40000'
    rev['obligations']=[rev['obligations'][0]];rev['obligations'][0]['ssp']='40000'
    rev['balance_bridge'].update(opening_revenue='0',opening_contract_net='0',opening_receivable='0',billings='40000',cash_received='0',opening_cost_asset='0');rev['contract_costs']=[];rev['delivered_quantity']='20'
    owners['revenue-recognition']=certify('revenue-recognition',rev);rr=completed('revenue-recognition',owners['revenue-recognition'])
    # Aggregate actual owner journals once, with documented clearing mapping.
    account_map={'depreciation expense':'Overhead clearing','Employee benefit expense':'Labour clearing','expense':'Overhead clearing',
        'cash':'Cash','receivable':'Receivable','revenue':'Revenue','contract clearing':'Contract clearing'}
    balances={'PPE gross':Decimal('600000'),'Accumulated depreciation':Decimal('-180000'),'Raw materials':Decimal('1000'),'Opening equity':Decimal('-421000')}
    for pkg in owners:
        if pkg=='foreign-currency': continue # historical basis owner does not repeat acquisition recognition
        for j in completed(pkg,owners[pkg])['journal_entry_implications']:
            for l in j:
                a=account_map.get(l['account'],l['account']);balances[a]=balances.get(a,Decimal(0))+Decimal(str(l['amount']))*(1 if l['side']=='Dr' else -1)
    # Existing Fixed Assets uses accumulated depreciation account spelling below;
    # opening account must match actual journal label, not a balancing plug.
    depreciation_accounts=[a for a in balances if 'accumulated' in a.lower()]
    if len(depreciation_accounts)>1:
        other=next(a for a in depreciation_accounts if a!='Accumulated depreciation')
        balances[other]+=balances.pop('Accumulated depreciation')
    # Map the actual statements from controlled ledger, no sum of owner balances.
    fs=reporting();fs['functional_currency']='USD'
    assets={'PPE gross','Raw materials','Work in progress','Finished goods','Receivable','Cash'}
    contra={a for a in balances if 'accumulated' in a.lower()}
    liabilities={'Employee benefit payable','Employee withholding payable','accounts payable','Acquisition clearing'}
    def category(a):
        if a in assets or a in contra:return 'asset'
        if a=='Opening equity':return 'equity'
        if a=='Revenue':return 'revenue'
        if a in liabilities:return 'liability'
        return 'expense'
    fs['current_tb']=[dict(id=a,balance=str(v),category=category(a),performance_category='operating',line=a,source_version='Synthetic-factory-GL-v1',classification_memo='Synthetic approved owner-journal clearing map and account classification',cash_account=a=='Cash') for a,v in balances.items() if v]
    fs['comparative_tb']=[dict(id=a,balance=v,category=cat,performance_category='operating',line=a,source_version='Synthetic-opening-GL-v1',classification_memo='Synthetic controlled prior ledger',cash_account=False) for a,v,cat in [('PPE gross','600000','asset'),('accumulated depreciation','-180000','asset'),('Raw materials','1000','asset'),('Opening equity','-421000','equity')]]
    profit=-sum(v for a,v in balances.items() if category(a) in ('expense','revenue'))
    fs['equity_bridge']=[dict(id='owners',opening='421000',profit=str(profit),oci='0',owner_transactions='0',retrospective_adjustments='0',other='0',closing=str(Decimal('421000')+profit),memo='Synthetic opening equity plus actual owned P&L')]
    cash=balances.get('Cash',Decimal(0));adjust=cash-profit
    fs['cash_flow'].update(start_amount=str(profit),adjustments=[dict(id='actual-noncash-working-capital',amount=str(adjust),source='Synthetic full owner ledger movement bridge',noncash_acquisition_fx_excluded=True,memo='Source-to-ledger actual noncash and working-capital classification')],investing='0',financing='0',fx='0',opening='0',closing=str(cash),classifications=[dict(id='actual-net',date='2026-12-31',kind='net_customer_supplier',**{'class':'operating'},amount=str(cash),memo='Synthetic actual cash population')]);fs['notes']=[dict(id='profit-note',target='profit',amount=str(profit),population_evidence='Synthetic full owner ledger',memo='Synthetic current income tie')]
    owners['financial-statements']=certify('financial-statements',fs);fr=completed('financial-statements',owners['financial-statements'])
    # Real complete reconciliation with RM/WIP/FG source identities, no adjustment.
    rec=operational('balance-sheet-reconciliations');rec['functional_currency']='USD'
    stock=dict(sorted(ir['calculations']['inventory_by_class'].items()));stock_total=sum(stock.values())
    rec['trial_balance']=[dict(id=a,balance=str(v),category='balance_sheet') for a,v in stock.items()]+[dict(id='stock-offset',balance=str(-stock_total),category='balance_sheet')]
    rec['inventory']=[dict(id=r['id']) for r in rec['trial_balance']];rec['reconciliations']=[]
    for r in rec['trial_balance']:
        v=r['balance'];rec['reconciliations'].append(row(rec,r['id'],opening=v,additions='0',reductions='0',source_closing=v,gl_closing=v,source_ids=[r['id']],gl_ids=[r['id']],items=[],adjustments=[],threshold='0',relative_threshold='0',max_age_days=30,risk_tier='high',movement_memo='Synthetic independent inventory to GL current balance tie'))
    rec['controls'].update(population_count=len(rec['reconciliations']),population_amount=str(stock_total*2));owners['balance-sheet-reconciliations']=certify('balance-sheet-reconciliations',rec);completed('balance-sheet-reconciliations',owners['balance-sheet-reconciliations'])
    close=operational('month-end-close');close['functional_currency']='USD'
    close['journals']=[];close['accruals']=[];close['controls'].update(population_count=0,population_amount='0')
    owners['month-end-close']=certify('month-end-close',close)
    for pkg in ('accounting-systems-data-integrity','accounting-controls-icfr'):
        c=practice_case(pkg);c['functional_currency']='USD'
        if pkg=='accounting-systems-data-integrity':
            c['interfaces'][0].update(source_system='Synthetic manufacturing subledger',target_system='Synthetic factory GL',interface_key='manufacturing-cost-interface',amount=str(stock_total))
            c['interface_source']['records']=copy.deepcopy(c['interfaces']);c['controls']['population_amount']=str(stock_total)
            for a in c['account_mapping']:a.update(source_system='Synthetic manufacturing subledger',source_account='inventory',target_account='inventory')
            for i,a in enumerate(c['access']):a['system']=('Synthetic manufacturing subledger','Synthetic factory GL')[i]
            src=next(d for d in c['documents'] if d['id']=='source')['content'];dst=next(d for d in c['documents'] if d['id']=='target')['content']
            src.update(system='Synthetic manufacturing subledger',records=[dict(id=a,account='inventory',dimension='HQ',amount=str(v)) for a,v in stock.items()],inventory=list(stock),signed_total=str(stock_total),gross_total=str(stock_total))
            dst.update(system='Synthetic factory GL',records=[dict(id='target-'+a,source_id=a,target_account='inventory',dimension='HQ',entity=c['entity'],book='main-book',currency='USD',amount=str(v),state='posted') for a,v in stock.items()],signed_total=str(stock_total),gross_total=str(stock_total),gl_amount=str(stock_total),statement_amount=str(stock_total))
            dst['inventory']=[r['id'] for r in dst['records']]
            registry=next(d for d in c['documents'] if d['id']=='registry')['content'];registry.update(account_mapping=copy.deepcopy(c['account_mapping']),access=copy.deepcopy(c['access']))
        else:
            c['control_rows'][0]['process']='inventory-reconciliation';c['control_rows'][0]['control_key']='Synthetic inventory cost population completeness';c['control_source']['records']=copy.deepcopy(c['control_rows'])
            for d in c['documents']:
                if d['id']=='design':d['content']['control_key']=c['control_rows'][0]['control_key']
                if d['id']=='risk-scope':d['content']['records'][0]['process']='inventory-reconciliation';d['content']['records'][0]['misstatement']='Omitted factory inventory cost population'
            c['risk_source']['records']=copy.deepcopy(next(d for d in c['documents'] if d['id']=='risk-scope')['content']['records'])
        from governance_accounting import digest
        for d in c['documents']:d['content_hash']=digest(d['content'])
        owners[pkg]=practice_ready(pkg,c=c,release=True)
        completed(pkg,owners[pkg])
    # Disclosure consumes the actual Inventory owner through canonical approved
    # Inventory supplement support; its requirement source remains independently reviewed.
    disc=governance_case('disclosure-management');disc['functional_currency']='USD'
    imp=disc['imports'][0];imp.update(package='financial-statements',case=owners['financial-statements'],result=fr)
    amount=str(fr['calculations']['current']['profit']);disc['requirements'][0]['amount']=amount
    disc['requirements'][0]['owner_requirement']=fr['disclosures_impacted'][0]
    disc['notes'][0].update(amount=amount,narrative=fr['conclusion'])
    disc['requirement_source']['records']=copy.deepcopy(disc['requirements'])
    next(d for d in disc['documents'] if d['id']=='statement')['content']['amount']=amount
    from governance_accounting import digest
    for d in disc['documents']:d['content_hash']=digest(d['content'])
    disc['controls']['population_amount']=str(abs(Decimal(amount)))
    owners['disclosure-management']=governance_ready('disclosure-management',c=refresh_release(disc));completed('disclosure-management',owners['disclosure-management'])
    analytics=governance_case('management-accounting-analytics');analytics['functional_currency']='USD'
    analytics['imports']=[row(analytics,'inventory-owner',package='inventory-cost',case=inv,result=ir,mode='evidence_only')]
    analytics['accounts'][0].update(account='Cost of goods sold',amount=str(cogs),management_amount='0')
    analytics['account_source']['records']=copy.deepcopy(analytics['accounts']);analytics['controls']['population_amount']=str(cogs)
    for d in analytics['documents']:
        if d['id'] in ('current-books','prior-books'):
            value=str(cogs) if d['id']=='current-books' else '0';data=d['content'];data.update(account='Cost of goods sold',statutory_amount=value,management_amount='0',gross_amount=value);data['records'][0].update(account='Cost of goods sold',amount=value)
        if d['id']=='actual-drivers':d['content'].update(account='Cost of goods sold',drivers=[dict(id='actual-factory-inventory-relief',amount=str(cogs))],driver_inventory=['actual-factory-inventory-relief'])
    analytics['explanations'][0].update(account='Cost of goods sold',amount=str(cogs),interpretation_memo='Synthetic actual sales inventory relief owner amount, interpretation remains reviewed')
    analytics['bridge_items']=[row(analytics,'cogs-owner-bridge',account='Cost of goods sold',classification='owner_accounting_adjustment',sign=1,owner_import='inventory-owner',result_path=['cogs'],amount=str(cogs),rationale='Synthetic actual COGS from completed Inventory owner',mapping_memo='Synthetic management pre-relief to statutory COGS')];analytics['bridge_inventory']=['cogs-owner-bridge']
    for d in analytics['documents']:d['content_hash']=digest(d['content'])
    owners['management-accounting-analytics']=governance_ready('management-accounting-analytics',c=refresh_release(analytics));completed('management-accounting-analytics',owners['management-accounting-analytics'])
    family={v[0]:k for k,v in __import__('orchestration.planning',fromlist=['FACT_ADAPTERS']).FACT_ADAPTERS.items()}
    facts={family[p]:copy.deepcopy(c) for p,c in owners.items()}
    facts['task_attributes']=dict(recurring_process=True,material_balance=True)
    handoffs=[]
    for pkg,(idx,amount,path,kind) in costs.items():
        handoffs.append(dict(producer=pkg,consumer='inventory-cost',metric_path=path,target_path=['costs',inv['costs'][idx]['id'],'amount'],semantic={'labour':'factory_labour','ap':'factory_supplier','depreciation':'factory_depreciation'}[kind],amount=amount,purpose='absorb',economic_id=inv['costs'][idx]['economic_id'],qualification_evidence=inv['costs'][idx]['source_doc']))
    if with_fx:handoffs.append(dict(producer='foreign-currency',consumer='inventory-cost',metric_path=['transactions','inventory-purchase','initial'],target_path=['movements','foreign-purchase','amount'],semantic='historical_purchase',amount='110',purpose='absorb',economic_id='economic-foreign-purchase',qualification_evidence='foreign-purchase-source'))
    for metric,account,semantic,sign in [('closing_inventory','Raw materials','inventory_balance',1),('cogs','Cost of goods sold','cogs',1)]:
        # Inventory total is tested against independent reconciliation population;
        # COGS is consumed directly by financial statement row.
        if metric=='closing_inventory':
            continue
        handoffs.append(dict(producer='inventory-cost',consumer='financial-statements',metric_path=[metric],target_path=['current_tb',account,'balance'],semantic=semantic,amount=str(ir['calculations'][metric]),sign=sign,purpose='report',economic_id='inventory-cogs',qualification_evidence='Synthetic owned COGS to GL/statement mapping'))
    handoffs.append(dict(producer='revenue-recognition',consumer='financial-statements',metric_path=['period_revenue'],target_path=['current_tb','Revenue','balance'],semantic='revenue',amount='40000',sign=-1,purpose='report',economic_id='sales-revenue',qualification_evidence='Synthetic goods delivery to revenue GL mapping'))
    handoffs.append(dict(producer='inventory-cost',consumer='balance-sheet-reconciliations',metric_path=['closing_inventory'],target_path=['controls','population_amount'],semantic='inventory_balance',amount=str(stock_total),sign='.5',purpose='report',economic_id='closing-stock',qualification_evidence='Synthetic gross reconciliation total equals twice signed stock asset'))
    assertions=[dict(node='inventory-cost',metric_path=['closing_inventory'],evidence_value=str(stock_total),operator='equal',evidence_ref='Synthetic independent inventory GL total',code='INVENTORY_GL'),dict(node='inventory-cost',metric_path=['quantity_population','product','closing_quantity'],evidence_value='60',operator='equal',evidence_ref='Synthetic manufacturing system physical count',code='SYSTEM_QUANTITY')]
    request=dict(case_id='synthetic-factory-year-end',objective='Prepare our year-end manufacturing accounting review and tell me whether inventory and gross margin are right.',
        scope=dict(entity='Synthetic Group',framework='IFRS',jurisdiction='NL',period_start='2026-01-01',reporting_period='2026-12-31',currency='USD',industry='manufacturing',materiality='1000'),facts=facts,handoffs=handoffs,challenge_assertions=assertions,company_context=[dict(id='factory-margin-policy',attribute='gross_margin_basis',value='inventory_relief_and_manufacturing_expense',status='APPROVED',scope={'entities':['Synthetic Group']},source_refs=['Synthetic approved income statement presentation policy'])],assumptions=['Controlled synthetic company and source data, for deterministic regression only.'],journal_account_mapping=account_map)
    from orchestration.runtime import digest
    from orchestration import CAO
    # Fixture-only synthetic approval of the exact combined journal pack. The
    # runtime cannot generate this record, and still tests actual GL movements.
    native=[]
    for package,source in owners.items():
        result=completed(package,source)
        native.append(dict(owner=package,case_fingerprint=result['case_fingerprint'],journals=result.get('journal_entry_implications',[])))
    request['journal_pack_review']=dict(preparer='Synthetic factory workpaper preparer',reviewer='Synthetic independent factory journal reviewer',approved=True,payload_fingerprint=digest(dict(mapping=account_map,native_owner_journals=native)))
    return request

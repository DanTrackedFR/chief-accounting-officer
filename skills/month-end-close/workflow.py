from operations_accounting import *

def assess(c,claims):
    proof(c,'tasks','journals','close','accruals','calendar')
    calendar=c['calendar'];required(calendar,'working_dates','timezone','holiday_review')
    texts(calendar,'timezone','holiday_review')
    if not isinstance(calendar['working_dates'],list) or not calendar['working_dates']:raise ReviewRequired('Approved local working-date calendar required')
    working=[iso(d) for d in calendar['working_dates']]
    if working!=sorted(set(working)):raise ReviewRequired('Working-date calendar must be unique and chronological')
    def actual_date(t,key):
        v=nonnegative(t[key])
        if v!=v.to_integral_value() or v>=len(working):raise ReviewRequired('Actual close day must map to approved working calendar')
        return working[int(v)]
    tasks=rows(c['tasks'],False); entries=[]; calcs={}; ends={}; visiting=set()
    byid={r['id']:r for r in tasks}
    def end(id):
        if id in visiting:raise ReviewRequired('Close dependency cycle')
        if id in ends:return ends[id]
        if id not in byid:raise ReviewRequired('Missing close predecessor')
        t=byid[id];approval(t,c);required(t,'predecessors','duration','due_day','actual_start_day','actual_finish_day','complete','timezone','unresolved_count')
        texts(t,'timezone')
        if not isinstance(t['predecessors'],list):raise ReviewRequired('Dependency list required')
        if not flag(t,'complete') or t['unresolved_count']!=0:raise ReviewRequired('Unresolved close task or feed rejects')
        visiting.add(id); start=max([end(p) for p in t['predecessors']]+[ZERO]);finish=start+nonnegative(t['duration']);visiting.remove(id)
        actualstart=nonnegative(t['actual_start_day']);actualfinish=nonnegative(t['actual_finish_day'])
        if t['timezone']!=calendar['timezone'] or actual_date(t,'actual_finish_day')>iso(t['approval_date']) or actual_date(t,'actual_finish_day')>iso(c['execution_date']):raise ReviewRequired('Task actual completion follows approval/execution or calendar timezone differs')
        actual_date(t,'actual_start_day')
        if actualfinish<actualstart or actualstart<max([nonnegative(byid[p]['actual_finish_day']) for p in t['predecessors']]+[ZERO]):raise ReviewRequired('Actual task chronology or predecessor completion failed')
        if finish>nonnegative(t['due_day']) or actualfinish>nonnegative(t['due_day']):raise ReviewRequired('Close calendar deadline missed')
        ends[id]=finish;return finish
    for id in byid:end(id)
    js=rows(c['journals']);seen=set();postings=set()
    for j in js:
        approval(j,c);required(j,'class','source_ids','posting_date','posted_at','posting_id','lines','rule_version','cutoff_supported','posted','reversal_plan')
        if j['posting_id'] in postings:raise ReviewRequired('Duplicate destination posting')
        postings.add(j['posting_id'])
        if j['class'] not in ['recurring','nonrecurring','estimate','correction','reclass','consolidation']:raise ReviewRequired('Unsupported journal classification')
        if not isinstance(j['source_ids'],list) or not j['source_ids'] or len(set(j['source_ids']))!=len(j['source_ids']) or seen.intersection(j['source_ids']):raise ReviewRequired('Duplicate or missing journal source lineage')
        seen.update(j['source_ids']);inperiod(c,j['posting_date'])
        if iso(j['approval_date'])>iso(j['posted_at']) or iso(j['posted_at'])>iso(c['execution_date']) or not flag(j,'cutoff_supported') or not flag(j,'posted'):raise ReviewRequired('Journal posted without timely approval/cutoff')
        if not isinstance(j['lines'],list) or not j['lines']:raise ReviewRequired('Journal lines required')
        balance(j['lines']);entries.append(j['lines'])
    population(c,js,[sum((dec(x['amount']) for x in j['lines'] if x['side']=='Dr'),ZERO) for j in js])
    accruals=rows(c['accruals']);accrual_amount=ZERO
    for a in accruals:
        approval(a,c);required(a,'received','posted','opening_accrual','recognition_supported','account','reversal_plan','gl_adjustment')
        if not flag(a,'recognition_supported'):raise ReviewRequired('Accrual receipt/obligation unsupported')
        delta=cash(nonnegative(a['received'])-nonnegative(a['posted'])-nonnegative(a['opening_accrual']))
        if delta<0:raise ReviewRequired('Accrual overlap requires supported release analysis')
        agree(a['gl_adjustment'],delta,'Accrual posted journal');accrual_amount+=delta
        # Accrual is already included in the provided posted journal population.
        linked=[j for j in js if a['id'] in j['source_ids']]
        if len(linked)!=1:raise ReviewRequired('Accrual must link to exactly one posted journal')
        agree(sum((dec(x['amount']) for x in linked[0]['lines'] if x['side']=='Dr' and x['account']==a['account']),ZERO),delta,'Accrual debit')
        agree(sum((dec(x['amount']) for x in linked[0]['lines'] if x['side']=='Cr' and x['account']=='accrued liabilities'),ZERO),delta,'Accrual liability')
    lock=c['close'];approval(lock,c);required(lock,'state','account_certifications_complete','exceptions','reopened','journal_population_reconciled','recognition_error_review','recognition_errors_resolved')
    if not flag(lock,'recognition_errors_resolved') or any(iso(j['posted_at'])>iso(lock['approval_date']) for j in js):raise ReviewRequired('Unresolved error review or lock predates posting')
    if any(iso(t['approval_date'])>iso(lock['approval_date']) or actual_date(t,'actual_finish_day')>iso(lock['approval_date']) for t in tasks):raise ReviewRequired('Close lock predates task completion/certification')
    if lock['state']!='locked' or lock['exceptions'] or not flag(lock,'account_certifications_complete') or not flag(lock,'journal_population_reconciled'):raise ReviewRequired('Close lock certification incomplete')
    if flag(lock,'reopened'):
        required(lock,'reopen_authorization','reclose_evidence')
    calcs={'task_finish_days':ends,'close_day':max(ends.values()),'posted_journal_count':len(js),'incremental_accrual':accrual_amount}
    return finish('Close calendar, journal population and lock certification reconciled.',calcs,entries,
      ['Invoice dates do not establish economic cutoff; prior errors and new estimates require separate framework analysis.','Reopening invalidates the prior lock certification and requires fresh independent approval.'],
      ['Material accrual estimates, corrections, subsequent events and presentation changes require financial reporting review.'])

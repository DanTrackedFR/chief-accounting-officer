"""Company institutional context, never native accounting or authenticated approval.

One append-only ledger in SQLiteStore. All qualification and publication use the
same local transaction/read snapshot. Exact native histories remain authoritative.
"""
import copy
from datetime import date
from .codec import dumps, loads, IntegrityError
from .store import sha, RevisionConflict
from .state import restore

CATEGORIES = {'corporate_profile','reporting_profile','accounting_function','systems_data','policies_positions','controls_evidence'}
ASSERTIONS = {'SOURCE_FACT','USER_STATED','EXTRACTED','INFERRED','ACCOUNTING_CONCLUSION','ASSUMPTION','DISPUTED','APPROVED_POLICY','HISTORICAL_JUDGMENT'}
STATES = {'PROPOSED','OBSERVED','CONFIRMED','DOCUMENTED','APPROVED','SUPERSEDED','RETRACTED'}
DIMENSIONS = {'scope_id','legal_entity_id','scope_type','calendar_id','period_ids','framework','jurisdiction','currency','relationship_id'}
TRANSITIONS = {'PROPOSED':{'OBSERVED','CONFIRMED','DOCUMENTED','APPROVED','RETRACTED'},'OBSERVED':{'CONFIRMED','DOCUMENTED','APPROVED','RETRACTED'},'CONFIRMED':{'DOCUMENTED','APPROVED','SUPERSEDED','RETRACTED'},'DOCUMENTED':{'APPROVED','SUPERSEDED','RETRACTED'},'APPROVED':{'SUPERSEDED','RETRACTED'},'SUPERSEDED':set(),'RETRACTED':set()}


def ident(kind, value): return kind+':'+sha(dumps(value))
def text(value):
    if type(value) is not str or not value.strip(): raise IntegrityError('Explicit nonempty text required')
    return value

def day(value):
    if type(value) is not str or date.fromisoformat(value).isoformat()!=value: raise IntegrityError('Exact canonical date required')
    return value

def temporal(value):
    if type(value) is not dict or set(value)!={'value','precision'}: raise IntegrityError('Explicit time precision required')
    p,v=value['precision'],value['value']
    if p=='unknown':
        if v is not None: raise IntegrityError('Unknown historical date fabricated')
    elif p=='exact': day(v)
    elif p=='month':
        if type(v) is not str or len(v)!=7 or day(v+'-01')[:7]!=v: raise IntegrityError('Invalid month')
    elif p not in {'quarter','year','approximate'} or type(v) is not str or not v.strip(): raise IntegrityError('Invalid uncertain date')
    return value


def applicability(case, scope_id, period_ids, relationship_id=None):
    e=case.governance;s=e.cases.scopes.get(scope_id)
    ps=[e.periods.get(p) for p in period_ids]
    if not ps or len({p.calendar_id for p in ps})!=1: raise IntegrityError('Exact single-calendar applicability required')
    if relationship_id is not None and relationship_id not in {r['id'] for r in e.periods.record()['relationships']}: raise IntegrityError('Unknown temporal relationship')
    return dict(scope_id=s.scope_id,legal_entity_id=s.legal_entity_id,scope_type=s.scope_type,calendar_id=ps[0].calendar_id,
                period_ids=sorted(set(period_ids)),framework=s.framework,jurisdiction=s.jurisdiction,
                currency=s.functional_currency or s.presentation_currency,relationship_id=relationship_id)


class CompanyMemory:
    """Trusted caller supplies explicit decisions; names/tokens authenticate nobody."""
    def __init__(self, store): self.store=store;self.db=store.connection

    def _native(self, company, root, revision=None):
        head=self.store._head(company,root)
        if not head: raise IntegrityError('Unknown Company/Case namespace')
        doc,checksum=self.store._read(company,root,head if revision is None else revision)
        case=restore(doc,company,root)
        from .recovery import read_operation
        for (key,) in self.db.execute('SELECT operation_id FROM operations WHERE company_id=? AND case_id=?',(company,root)):
            read_operation(self.store,company,root,key)
        return case,doc,checksum,head

    def _ledger(self, company, pending=False):
        rows=self.db.execute('SELECT sequence,event_id,payload,sha256,previous_sha256 FROM memory_events WHERE company_id=? ORDER BY sequence',(company,)).fetchall()
        previous=None;records={};events=[];uses=[];versions={}
        for i,(seq,key,wire,checksum,prev) in enumerate(rows,1):
            if seq!=i or sha(wire)!=checksum or prev!=previous: raise IntegrityError('Missing/corrupt memory history')
            event=loads(wire)
            if set(event)!={'contract','company_id','kind','record_id','previous_version','value','reason','recorded_at','qualification'} or event['contract']!=1 or event['company_id']!=company or ident('memory-event',event)!=key:
                raise IntegrityError('Unknown memory event contract/identity')
            kind=event['kind'];rid=event['record_id'];old=records.get(rid)
            receipt=event['qualification']
            if type(receipt) is not dict or set(receipt)!={'root_case','revision','sha256'}:raise IntegrityError('Missing exact memory qualification snapshot')
            source_case,_,source_checksum,_=self._native(company,receipt['root_case'],receipt['revision'])
            if source_checksum!=receipt['sha256']:raise IntegrityError('Changed memory qualification snapshot')
            if kind=='CAPTURE':
                if old is not None or event['previous_version'] is not None: raise IntegrityError('Duplicate memory record')
                record=event['value'];self._record(record);self._qualification(record)
                if record['decision'] is not None and record['decision']['status']!='proposed':raise IntegrityError('Candidate decision is not governed')
                if rid!=ident('memory',record['identity']) or record['company_id']!=company or record['status']!='PROPOSED': raise IntegrityError('Unsafe initial memory authority')
            elif kind=='TRANSITION':
                if old is None or event['previous_version']!=old['version_id']: raise IntegrityError('Missing historical promotion')
                record=event['value'];self._record(record)
                if record['status'] not in TRANSITIONS[old['status']]: raise IntegrityError('Invalid historical transition')
                immutable=set(old)-{'status','governance','version_id','superseded_by'}
                if any(old[k]!=record[k] for k in immutable): raise IntegrityError('Rewritten memory provenance')
                if record['status']=='SUPERSEDED':
                    successor=records.get(record['superseded_by'])
                    if record['superseded_by']==rid or successor is None or successor['status'] not in {'DOCUMENTED','APPROVED'} or rid not in successor['supersedes'] or successor['applicability']!=record['applicability'] or (successor['subject'],successor['attribute'])!=(record['subject'],record['attribute']):raise IntegrityError('Inconsistent supersession history')
                elif record['superseded_by'] is not None:raise IntegrityError('Unexpected historical supersession')
                if record['governance'] is None: raise IntegrityError('Missing governance provenance')
                self._governance(record,record['governance'],old['status'],historical=True)
            elif kind=='DECISION':
                if old is None or event['previous_version']!=old['version_id']:raise IntegrityError('Unknown material decision predecessor')
                record=event['value'];self._record(record)
                if old['decision'] is None or record['decision'] is None:raise IntegrityError('Missing material decision')
                allowed={'proposed':{'documented','approved'},'documented':{'approved','implemented','reversed','superseded'},'approved':{'implemented','reversed','superseded'},'implemented':{'reversed','superseded'},'reversed':set(),'superseded':set()}
                if record['decision']['status']=='approved' and old['status']!='APPROVED':raise IntegrityError('Historical decision approval not governed')
                if record['decision']['status'] not in allowed[old['decision']['status']]:raise IntegrityError('Invalid decision lifecycle')
                if any(old[k]!=record[k] for k in set(old)-{'decision','governance','version_id'}):raise IntegrityError('Decision rewrote company position')
                self._governance(record,record['governance'],old['status'],historical=True)
            elif kind=='USE':
                if old is None or event['previous_version']!=event['value']['memory_version'] or event['previous_version'] not in versions.get(rid,set()): raise IntegrityError('Unbound consumption')
                u=event['value']
                if receipt['root_case']!=old['source']['root_case'] or receipt['revision']!=u.get('source_revision') or receipt['sha256']!=u.get('source_sha256'):raise IntegrityError('Consumed source receipt differs')
                if set(u)!={'root_case','case_id','case_revision','case_sha256','memory_version','use','source_revision','source_sha256'} or u['use']!='CONTEXT_ONLY' or old['version_id']!=u['memory_version'] or old['status'] not in {'CONFIRMED','DOCUMENTED','APPROVED'}:raise IntegrityError('Invalid historical context consumption')
                consumer,_,consumer_checksum,_=self._native(company,u['root_case'],u['case_revision']);c=consumer.governance.cases.get(u['case_id'])
                query=applicability(consumer,c.scope_id,[c.period_id],old['applicability']['relationship_id'])
                if consumer_checksum!=u['case_sha256'] or any(query[k]!=old['applicability'][k] for k in DIMENSIONS-{'period_ids'}) or c.period_id not in old['applicability']['period_ids']:raise IntegrityError('Historical consuming Case binding differs')
                source,_,source_sha,_=self._native(company,old['source']['root_case'],u['source_revision'])
                period=consumer.governance.periods.get(c.period_id)
                if old['effective_from']['precision']!='exact' or old['effective_from']['value']>period.start or old['effective_to']['precision'] not in {'exact','unknown'} or (old['effective_to']['precision']=='exact' and old['effective_to']['value']<period.end):raise IntegrityError('Historical memory use outside effective Period')
                if source_sha!=u['source_sha256'] or any(source.governance.versions.states.get(v)!='CURRENT' for v in old['source']['result_versions']):raise IntegrityError('Historical source qualification differs')
                if any(other['record_id']!=rid and other['status'] not in {'SUPERSEDED','RETRACTED'} and self._overlap(old,other) and dumps(old['value'])!=dumps(other['value']) for other in records.values()):raise IntegrityError('Historical use had unresolved conflict')
                uses.append(event);events.append(dict(event_id=key,**event));previous=checksum;continue
            else: raise IntegrityError('Unknown memory event')
            if receipt['root_case']!=record['source']['root_case']:raise IntegrityError('Qualification source Case differs')
            if kind in {'TRANSITION','DECISION'} and record['status'] in {'CONFIRMED','DOCUMENTED','APPROVED'}:
                if self._assertion_reasons(record) or any(source_case.governance.versions.states.get(v)!='CURRENT' for v in record['source']['result_versions']):raise IntegrityError('Historical promotion qualification invalid')
            if record['record_id']!=rid or record['version_id']!=ident('memory-version',{k:v for k,v in record.items() if k!='version_id'}): raise IntegrityError('Wrong memory version')
            versions.setdefault(rid,set()).add(record['version_id']);records[rid]=record;events.append(dict(event_id=key,**event));previous=checksum
        head=self.db.execute('SELECT sequence,sha256 FROM memory_heads WHERE company_id=?',(company,)).fetchone()
        if (head or (0,None))!=(len(rows),previous): raise IntegrityError('Memory head contradicts retained events')
        if not pending:
            approved=[r for r in records.values() if r['status']=='APPROVED']
            for i,r in enumerate(approved):
                if any(self._overlap(r,other) for other in approved[i+1:]):raise IntegrityError('Duplicate current approved memory history')
            for r in records.values():
                if r['status'] in {'DOCUMENTED','APPROVED'}:
                    for predecessor in r['supersedes']:
                        old=records.get(predecessor)
                        if old is None or old['status']!='SUPERSEDED' or old['superseded_by']!=r['record_id']:raise IntegrityError('Missing reciprocal supersession history')
        return records,events,uses,len(rows),previous

    def _record(self, r):
        fields={'contract','identity','record_id','version_id','company_id','original_candidate','category','subject','attribute','value','assertion','source','applicability','effective_from','effective_to','learned_at','confidence','uncertainty','questions','decision','status','governance','supersedes','superseded_by'}
        if type(r) is not dict or set(r)!=fields or r['contract']!=1: raise IntegrityError('Unknown memory record contract')
        if r['category'] not in CATEGORIES or r['assertion'] not in ASSERTIONS or r['status'] not in STATES: raise IntegrityError('Unknown memory record type')
        for k in ('subject','attribute','company_id'):text(r[k])
        if type(r['source']) is not dict or set(r['source'])!={'root_case','case_id','revision','checkpoint_sha256','bundle_ids','result_versions'}:raise IntegrityError('Unknown memory provenance contract')
        if type(r['source']['revision']) is not int or r['source']['revision']<1:raise IntegrityError('Invalid original source revision')
        for key in ('bundle_ids','result_versions'):
            if type(r['source'][key]) is not list or r['source'][key]!=sorted(set(r['source'][key])):raise IntegrityError('Noncanonical source reference population')
        if type(r['applicability']) is not dict or set(r['applicability'])!=DIMENSIONS: raise IntegrityError('Incomplete applicability')
        temporal(r['learned_at']);temporal(r['effective_from']);temporal(r['effective_to'])
        if r['effective_from']['precision']=='exact' and r['effective_to']['precision']=='exact' and r['effective_from']['value']>r['effective_to']['value']: raise IntegrityError('Invalid effective interval')
        if r['identity']!=dict(company=r['company_id'],case=r['source']['case_id'],candidate=r['original_candidate'],category=r['category'],subject=r['subject'],source=r['source'],dimensions=r['applicability'],effective_from=r['effective_from'],effective_to=r['effective_to']):raise IntegrityError('Memory stable identity differs')
        if r['confidence'] not in {'high','medium','low','unknown'}: raise IntegrityError('Unknown confidence')
        if r['decision'] is not None:
            d=r['decision']
            if set(d)!={'previous_position','new_position','reason','decision_date','status','implications'} or d['status'] not in {'proposed','documented','approved','implemented','reversed','superseded'}: raise IntegrityError('Invalid Decision Register')
            text(d['reason']);temporal(d['decision_date'])
        dumps(r)

    def _qualification(self, r):
        src=r['source'];company=r['company_id']
        original,doc,checksum,_=self._native(company,src['root_case'],src['revision'])
        if checksum!=src['checkpoint_sha256']: raise IntegrityError('Changed original Case checkpoint')
        case,latest,_,_=self._native(company,src['root_case'])
        native=original.governance.cases.get(src['case_id'])
        if not any(dumps(c)==dumps(r['original_candidate']) for c in native.memory_candidates): raise IntegrityError('Candidate not originally observed')
        if r['applicability']!=applicability(original,r['applicability']['scope_id'],r['applicability']['period_ids'],r['applicability']['relationship_id']): raise IntegrityError('Substituted applicability')
        bundles=latest['session'].get('evidence_bundles',{})
        if not src['bundle_ids'] or any(k not in bundles or bundles[k]!=doc['session'].get('evidence_bundles',{}).get(k) for k in src['bundle_ids']): raise IntegrityError('Missing/changed sealed evidence')
        # Archive validity is proven by native restore. Bundle membership alone
        # does not prove candidate wording: bind actual observer context or intake.
        candidate=r['original_candidate'];attribute=r['attribute']
        observed=(candidate.get('source_refs')==['supplied-governed-context'] and attribute in doc['session']['context'] and doc['session']['context'][attribute]==r['value'])
        extracted=any(candidate in bundles[k]['fields']['memory_candidates'] for k in src['bundle_ids'])
        if not observed and not extracted: raise IntegrityError('Candidate evidence linkage unsupported')
        semantic=candidate.get('semantic_status','USER_STATED')
        allowed={'EXTRACTED':{'EXTRACTED','SOURCE_FACT'},'USER_STATED':{'USER_STATED'},'INFERRED':{'INFERRED'},'UNRESOLVED':{'DISPUTED'}}
        if r['assertion'] not in allowed.get(semantic,set()): raise IntegrityError('Original semantic assertion relabeled')
        if extracted:
            from orchestration.intake.sources import Inventory,RawSource
            import json
            fields={k:field for key in src['bundle_ids'] for raw in bundles[key]['raw_sources'] for k,field in Inventory([RawSource(**json.loads(raw))]).fields().items()}
            if not candidate.get('source_refs') or any(k not in fields for k in candidate['source_refs']):raise IntegrityError('Missing extracted candidate source')
            if semantic=='EXTRACTED' and not any(dumps(fields[k]['value'])==dumps(r['value']) for k in candidate['source_refs']):raise IntegrityError('Extracted candidate value differs from source')
        versions=src['result_versions']
        for v in versions:
            if v not in original.governance.versions.versions: raise IntegrityError('Unknown supporting result')
            version=original.governance.versions.versions[v]
            if version.case_id!=src['case_id'] or version.scope_id!=r['applicability']['scope_id']:raise IntegrityError('Unrelated supporting result lineage')
        reasons=[]
        for v in versions:
            if case.governance.versions.states.get(v)!='CURRENT': reasons.append('supporting-result-'+str(case.governance.versions.states.get(v)))
        reasons.extend(self._assertion_reasons(r))
        return reasons

    @staticmethod
    def _assertion_reasons(r):
        reasons=[]
        if r['original_candidate'].get('conflict') or r['assertion'] in {'INFERRED','ASSUMPTION','DISPUTED'}:reasons.append('unresolved-assertion')
        if r['questions']:reasons.append('unresolved-questions')
        return reasons

    def _governance(self,r,g,prior,historical=False):
        fields={'intent','prior_status','target_status','record_id','applicability','authority','evidence_kind','bundle_ids','reason','decision_date','approval_date','authenticated'}
        if type(g) is not dict or set(g)!=fields or g['intent']!='EXPLICIT_MEMORY_TRANSITION' or g['prior_status']!=prior or g['target_status']!=r['status'] or g['record_id']!=r['record_id'] or g['applicability']!=r['applicability']: raise IntegrityError('Exact explicit governance intent required')
        if g['authority']!='TRUSTED_CALLER_ASSERTION' or g['authenticated'] is not False or g['evidence_kind'] not in {'DOCUMENTARY','SYNTHETIC'}: raise IntegrityError('Authenticated approval not implemented')
        text(g['reason']);temporal(g['decision_date']);temporal(g['approval_date'])
        if not g['bundle_ids'] or not set(g['bundle_ids'])<=set(r['source']['bundle_ids']): raise IntegrityError('Governance evidence absent')
        if r['status']=='APPROVED' and r['assertion'] in {'INFERRED','ASSUMPTION','DISPUTED','ACCOUNTING_CONCLUSION'}: raise IntegrityError('Model conclusion is not approved policy')
        if g['evidence_kind']=='DOCUMENTARY' and r['status']=='APPROVED':
            # Documentary approval must be present as exact source wording in the
            # sealed original archive; caller explicitly asserts its applicability.
            _,doc,_,_=self._native(r['company_id'],r['source']['root_case'],r['source']['revision'])
            from orchestration.intake.sources import Inventory,RawSource
            import json
            dimensions=r['applicability'];periods=[original for original in doc['periods']['periods'] if original['period_id'] in dimensions['period_ids']]
            expected=dict(subject=r['subject'],attribute=r['attribute'],value=r['value'],status='APPROVED',scope_id=dimensions['scope_id'],framework=dimensions['framework'],period=[min(p['start'] for p in periods),max(p['end'] for p in periods)],currency=dimensions['currency'],jurisdiction=dimensions['jurisdiction'],convention='DOCUMENTARY_ASSERTION')
            approved=False
            for key in g['bundle_ids']:
                for wire in doc['session']['evidence_bundles'][key]['raw_sources']:
                    raw=RawSource(**json.loads(wire))
                    # Narrow supported documentary envelope, not substring/model
                    # text or an asserted reviewer display label.
                    if raw.format=='json' and isinstance(raw.payload,list):
                        approved |= any(isinstance(row,dict) and row.get('memory_governance')==__import__('json').dumps(expected,sort_keys=True,separators=(',',':')) for row in raw.payload)
            if not approved:raise IntegrityError('Documentary approval assertion not evidenced')
        if not historical and r['status'] not in {'RETRACTED','SUPERSEDED'} and self._qualification(r): raise IntegrityError('Evidence not currently qualified')

    def _append(self,company,kind,rid,previous,value,reason,recorded_at,expected):
        records,events,uses,sequence,checksum=self._ledger(company,pending=True)
        record=value if kind!='USE' else records[rid]
        source,_,source_checksum,source_revision=self._native(company,record['source']['root_case'])
        receipt=dict(root_case=record['source']['root_case'],revision=source_revision,sha256=source_checksum)
        event=dict(contract=1,company_id=company,kind=kind,record_id=rid,previous_version=previous,value=value,reason=text(reason),recorded_at=temporal(recorded_at),qualification=receipt)
        key=ident('memory-event',event)
        for old_event in events:
            if all(old_event.get(k)==event[k] for k in event if k!='qualification'):return old_event['event_id']
        existing=self.db.execute('SELECT payload FROM memory_events WHERE event_id=?',(key,)).fetchone()
        if existing:
            if existing[0]!=dumps(event):raise IntegrityError('Duplicate memory event identity')
            return key
        if type(expected) is not int or expected!=sequence: raise RevisionConflict('Company memory revision changed')
        wire=dumps(event);checksum_new=sha(wire)
        self.db.execute('INSERT INTO memory_events VALUES(?,?,?,?,?,?)',(company,sequence+1,key,wire,checksum_new,checksum))
        self.db.execute('INSERT INTO memory_heads VALUES(?,?,?) ON CONFLICT(company_id) DO UPDATE SET sequence=excluded.sequence,sha256=excluded.sha256',(company,sequence+1,checksum_new))
        return key

    def _transaction(self,write,fn):
        try:
            self.db.execute('BEGIN IMMEDIATE' if write else 'BEGIN');self.store._schema()
            result=fn()
            if write:
                for (company,) in self.db.execute('SELECT company_id FROM memory_heads'):self._ledger(company)
            self.db.execute('COMMIT');return result
        except BaseException:
            if self.db.in_transaction:self.db.execute('ROLLBACK')
            raise

    def capture(self,company,root,case_id,candidate_index,*,category,subject,assertion,bundle_ids,result_versions,dimensions,effective_from,effective_to,learned_at,expected_revision,material,reusable,confidence='unknown',uncertainty=None,questions=None,decision=None,supersedes=None):
        def write():
            if material is not True or reusable is not True: raise IntegrityError('Material/reusable gate required')
            case,doc,checksum,revision=self._native(company,root)
            native=case.governance.cases.get(case_id)
            if type(candidate_index) is not int or candidate_index<0 or candidate_index>=len(native.memory_candidates):raise IntegrityError('Unknown original candidate')
            candidate=copy.deepcopy(native.memory_candidates[candidate_index])
            if candidate.get('scope_id')!=dimensions['scope_id']:raise IntegrityError('Candidate Scope substituted')
            source=dict(root_case=root,case_id=case_id,revision=revision,checkpoint_sha256=checksum,bundle_ids=sorted(set(bundle_ids)),result_versions=sorted(set(result_versions)))
            identity=dict(company=company,case=case_id,candidate=candidate,category=category,subject=subject,source=source,dimensions=dimensions,effective_from=effective_from,effective_to=effective_to)
            rid=ident('memory',identity)
            r=dict(contract=1,identity=identity,record_id=rid,company_id=company,original_candidate=candidate,category=category,subject=subject,attribute=candidate['attribute'],value=candidate['value'],assertion=assertion,source=source,applicability=copy.deepcopy(dimensions),effective_from=effective_from,effective_to=effective_to,learned_at=learned_at,confidence=confidence,uncertainty=uncertainty,questions=questions or [],decision=decision,status='PROPOSED',governance=None,supersedes=sorted(set(supersedes or [])),superseded_by=None)
            if decision is not None and decision.get('status')!='proposed':raise IntegrityError('Candidate decision must remain proposed')
            r['version_id']=ident('memory-version',r);self._record(r);self._qualification(r)
            existing=self._ledger(company)[0].get(rid)
            if existing:
                if existing['identity']!=identity:raise IntegrityError('Candidate identity collision')
                return copy.deepcopy(existing)
            self._append(company,'CAPTURE',rid,None,r,'Material reusable candidate retained without promotion',learned_at,expected_revision)
            return copy.deepcopy(r)
        return self._transaction(True,write)

    def transition(self,company,record_id,governance,*,expected_revision,recorded_at,successor=None):
        return self._transaction(True,lambda:self._transition_write(company,record_id,governance,expected_revision,recorded_at,successor,set()))

    def _transition_write(self,company,record_id,governance,expected_revision,recorded_at,successor,resolving):
        records,events,_,seq,_=self._ledger(company,pending=True)
        old=records.get(record_id)
        if old is None:raise IntegrityError('Unknown Company memory')
        # Lost-ack retry must match exact already persisted intent, not merely
        # the target label; it cannot refresh currentness or native authority.
        if old['governance']==governance:return copy.deepcopy(old)
        target=governance.get('target_status')
        if target not in TRANSITIONS[old['status']]:raise IntegrityError('Prior state transition invalid')
        r=copy.deepcopy(old);r.update(status=target,governance=copy.deepcopy(governance),superseded_by=successor)
        if target=='SUPERSEDED':
            new=records.get(successor)
            if successor==record_id or new is None or record_id not in new['supersedes'] or new['status'] not in {'DOCUMENTED','APPROVED'} or new['subject']!=r['subject'] or new['attribute']!=r['attribute'] or new['applicability']!=r['applicability']:raise IntegrityError('Qualified successor required')
            if self._qualification(new):raise IntegrityError('Unqualified successor')
        elif successor is not None:raise IntegrityError('Unexpected supersession')
        r['version_id']=ident('memory-version',{k:v for k,v in r.items() if k!='version_id'})
        self._record(r);self._governance(r,governance,old['status'])
        if target in {'CONFIRMED','DOCUMENTED','APPROVED'}:
            for other in records.values():
                if other['record_id']==record_id or other['record_id'] in resolving or other['status'] in {'SUPERSEDED','RETRACTED'}:continue
                if self._overlap(r,other) and dumps(other['value'])!=dumps(r['value']):raise IntegrityError('Unresolved overlapping contradiction; preserve both alternatives')
                if target=='APPROVED' and other['status']=='APPROVED' and self._overlap(r,other):raise IntegrityError('Duplicate current approved position')
        self._append(company,'TRANSITION',record_id,old['version_id'],r,governance['reason'],recorded_at,expected_revision)
        return copy.deepcopy(r)

    def resolve_conflict(self,company,successor_id,governance,alternatives,*,expected_revision,recorded_at):
        """Explicit complete alternative disposition, atomic local transition set.

        alternatives maps predecessor IDs to exact SUPERSEDED governance intents.
        Every predecessor is retained; none silently disappears on a new proposal.
        """
        def write():
            records,_,_,seq,_=self._ledger(company)
            new=records.get(successor_id)
            if new is not None and new['governance']==governance and new['status'] in {'DOCUMENTED','APPROVED'} and set(new['supersedes'])==set(alternatives) and alternatives:
                if all(records.get(key,{}).get('governance')==g and records[key]['status']=='SUPERSEDED' and records[key]['superseded_by']==successor_id for key,g in alternatives.items()):return copy.deepcopy(new)
            if seq!=expected_revision:raise RevisionConflict('Company memory revision changed')
            if new is None or new['status']!='PROPOSED' or set(new['supersedes'])!=set(alternatives) or not alternatives:raise IntegrityError('Exact supersession alternatives required')
            for key,g in alternatives.items():
                old=records.get(key)
                if key==successor_id or old is None or not self._overlap(new,old) or old['applicability']!=new['applicability'] or g.get('target_status')!='SUPERSEDED':raise IntegrityError('Invalid conflict resolution alternative')
            chosen=self._transition_write(company,successor_id,governance,seq,recorded_at,None,set(alternatives))
            for key,g in sorted(alternatives.items()):
                seq+=1;self._transition_write(company,key,g,seq,recorded_at,successor_id,set())
            return chosen
        return self._transaction(True,write)

    def decide(self,company,record_id,decision,governance,*,expected_revision,recorded_at):
        def write():
            records,_,_,seq,_=self._ledger(company);old=records.get(record_id)
            if old is None or old['decision'] is None:raise IntegrityError('Material proposed decision required')
            if old['decision']==decision and old['governance']==governance:return copy.deepcopy(old)
            allowed={'proposed':{'documented','approved'},'documented':{'approved','implemented','reversed','superseded'},'approved':{'implemented','reversed','superseded'},'implemented':{'reversed','superseded'},'reversed':set(),'superseded':set()}
            if decision.get('status') not in allowed[old['decision']['status']]:raise IntegrityError('Invalid material decision transition')
            if decision['status']=='approved' and old['status']!='APPROVED':raise IntegrityError('Decision approval requires explicit governed approved position')
            r=copy.deepcopy(old);r.update(decision=copy.deepcopy(decision),governance=copy.deepcopy(governance));r['version_id']=ident('memory-version',{k:v for k,v in r.items() if k!='version_id'})
            self._record(r);self._governance(r,governance,old['status'])
            self._append(company,'DECISION',record_id,old['version_id'],r,decision['reason'],recorded_at,expected_revision)
            return copy.deepcopy(r)
        return self._transaction(True,write)

    def history(self,company,record_id):
        return self._transaction(False,lambda:[event for event in self._ledger(company)[1] if event['record_id']==record_id])

    def _overlap(self,a,b):
        if (a['subject'],a['attribute'])!=(b['subject'],b['attribute']):return False
        da,db=a['applicability'],b['applicability']
        if any(da[k]!=db[k] for k in {'calendar_id','framework','jurisdiction','currency','relationship_id'}):return False
        if any(da[k]!=db[k] for k in {'scope_id','legal_entity_id','scope_type'}):return False
        if not set(da['period_ids'])&set(db['period_ids']):return False
        start=lambda r:r['effective_from']['value'] if r['effective_from']['precision']=='exact' else '0001-01-01'
        end=lambda r:r['effective_to']['value'] if r['effective_to']['precision']=='exact' else '9999-12-31'
        return start(a)<=end(b) and start(b)<=end(a)

    def _retrieve(self,company,root,case_id,subject,attribute,relationship_id=None,historical=False):
        consumer,_,_,_=self._native(company,root);c=consumer.governance.cases.get(case_id)
        query=applicability(consumer,c.scope_id,[c.period_id],relationship_id)
        records,events,uses,revision,_=self._ledger(company)
        matches=[];refused=[];conflicts=[]
        for r in records.values():
            if (r['subject'],r['attribute'])!=(subject,attribute):continue
            d=r['applicability']
            if any(d[k]!=query[k] for k in DIMENSIONS-{'period_ids'}) or c.period_id not in d['period_ids']:continue
            period=consumer.governance.periods.get(c.period_id)
            if r['effective_from']['precision']!='exact' or (r['effective_to']['precision'] not in {'exact','unknown'}):reasons=['effective-interval-uncertain']
            elif r['effective_from']['value']>period.start or (r['effective_to']['precision']=='exact' and r['effective_to']['value']<period.end):continue
            else:reasons=[]
            if not historical:
                if r['status'] not in {'CONFIRMED','DOCUMENTED','APPROVED'}:reasons.append('governance-'+r['status'])
                reasons.extend(self._qualification(r))
                alternatives=[other['record_id'] for other in records.values() if other['record_id']!=r['record_id'] and other['status'] not in {'SUPERSEDED','RETRACTED'} and self._overlap(r,other) and dumps(r['value'])!=dumps(other['value'])]
                if alternatives:reasons.append('unresolved-conflict');conflicts.extend(alternatives)
            entry=dict(record=copy.deepcopy(r),qualification='HISTORICAL' if historical else 'CURRENT_CONTEXT',limitations=['Context only; native ReviewedInputPack and owner qualification still required','No authenticated human approval'],reasons=sorted(set(reasons)))
            (refused if reasons else matches).append(entry)
        return dict(company_id=company,revision=revision,query=query,qualified=matches,refused=refused,conflicts=sorted(set(conflicts)),historical=historical)

    def retrieve(self,company,root,case_id,subject,attribute,*,relationship_id=None,historical=False):
        return self._transaction(False,lambda:self._retrieve(company,root,case_id,subject,attribute,relationship_id,historical))

    def consume_context(self,company,root,case_id,record_id,version_id,*,expected_revision,recorded_at):
        def write():
            records,_,_,_,_=self._ledger(company);r=records.get(record_id)
            if r is None or r['version_id']!=version_id:raise IntegrityError('Exact memory version required')
            result=self._retrieve(company,root,case_id,r['subject'],r['attribute'],r['applicability']['relationship_id'])
            if not any(v['record']['version_id']==version_id for v in result['qualified']):raise IntegrityError('Memory not qualified for this Case')
            _,doc,checksum,revision=self._native(company,root)
            source,_,source_sha,source_revision=self._native(company,r['source']['root_case'])
            value=dict(root_case=root,case_id=case_id,case_revision=revision,case_sha256=checksum,memory_version=version_id,use='CONTEXT_ONLY',source_revision=source_revision,source_sha256=source_sha)
            self._append(company,'USE',record_id,version_id,value,'Exact qualified context consumption; no native input authority',recorded_at,expected_revision)
            return value
        return self._transaction(True,write)

    def audit(self,company):
        def read():
            records,events,uses,revision,_=self._ledger(company)
            return dict(revision=revision,company_context=list(records.values()),case_library=[dict(memory_id=r['record_id'],source_case=r['source']['case_id'],root_case=r['source']['root_case'],result_versions=r['source']['result_versions']) for r in records.values()],artifact_library=[dict(memory_id=r['record_id'],bundle_ids=r['source']['bundle_ids'],checkpoint_sha256=r['source']['checkpoint_sha256']) for r in records.values()],provenance=events,decision_register=[dict(decision_id=ident('decision',[r['record_id'],r['decision']]),memory_id=r['record_id'],decision=r['decision']) for r in records.values() if r['decision'] is not None],uses=uses)
        return self._transaction(False,read)

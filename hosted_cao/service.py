"""Single-host transport and operational jobs; accounting lives in local_cao."""
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import re
import sqlite3
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from contextlib import contextmanager
from local_cao.adapter import ExecutionInterface, canonical, decode, checked_path
from local_cao.context import identity
from orchestration.intake.sources import bounded, MAX_BYTES

LOG = logging.getLogger('hosted_cao')
API_VERSION = '1.0'
OPERATIONS = {'initialize','capabilities','start','status','questions','submit','result','resume','list','context','diagnose'}
SAFE = {'invalid_request': 'Check the versioned request contract.', 'unauthorized': 'Service authentication required.',
        'forbidden': 'Company access is not permitted.', 'not_found': 'Resource unavailable.',
        'conflict': 'Idempotency key is bound to another request.', 'unavailable': 'Service temporarily unavailable.',
        'payload_limit': 'Request exceeds the configured limit.'}

class Error(Exception):
    def __init__(self, code, status=400): self.code=code; self.status=status

class Service:
    def __init__(self, root, companies, credentials):
        self.root=checked_path(root); self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        self.companies={identity(k):checked_path(v) for k,v in companies.items()}
        if not self.companies or len(set(self.companies.values()))!=len(self.companies): raise ValueError('Invalid company namespaces')
        self.credentials=[]
        for row in credentials:
            if set(row)!={'caller_id','token','companies'} or not isinstance(row['token'],str) or len(row['token'])<32: raise ValueError('Invalid credential configuration')
            identity(row['caller_id'])
            if not isinstance(row['companies'],list) or not row['companies'] or set(row['companies'])-self.companies.keys(): raise ValueError('Invalid credential scope')
            if any(hmac.compare_digest(row['token'],r['token']) for r in self.credentials): raise ValueError('Duplicate credential')
            self.credentials.append(dict(row))
        if not self.credentials: raise ValueError('Credentials required')
        self.stop=threading.Event(); self.worker=None; self.lockfd=None
        self.company_locks={k:threading.RLock() for k in self.companies}
        self.run_lock=threading.Lock()
        db=checked_path(self.root/'jobs.sqlite3')
        if db.exists() and not db.is_file(): raise ValueError('Invalid job storage')
        fd=os.open(db,os.O_CREAT|os.O_RDWR,0o600);os.close(fd)
        with self.db() as c:
            c.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, company TEXT NOT NULL, key TEXT NOT NULL, fingerprint TEXT NOT NULL, request TEXT NOT NULL, state TEXT NOT NULL, attempts INTEGER NOT NULL, result_case TEXT, outcome TEXT, input_hash TEXT NOT NULL, error TEXT, created REAL NOT NULL, updated REAL NOT NULL, UNIQUE(company,key))')
        self.dbpath=db

    @contextmanager
    def db(self):
        c=sqlite3.connect(checked_path(self.root/'jobs.sqlite3'),timeout=10)
        c.row_factory=sqlite3.Row;c.execute('PRAGMA synchronous=FULL')
        try: yield c; c.commit()
        except BaseException: c.rollback(); raise
        finally: c.close()

    def authenticate(self, authorization, company):
        token=authorization[7:] if isinstance(authorization,str) and authorization.startswith('Bearer ') else ''
        match=None
        for row in self.credentials:
            if hmac.compare_digest(token.encode(),row['token'].encode()): match=row
        if match is None: raise Error('unauthorized',401)
        if company not in match['companies'] or company not in self.companies: raise Error('forbidden',403)
        return match['caller_id']

    def validate(self, request, company, operation=None):
        try:
            bounded(request)
            if not isinstance(request,dict) or len(canonical(request).encode())>MAX_BYTES: raise ValueError()
            if request.get('company_id')!=company or request.get('contract_version')!=API_VERSION: raise ValueError()
            op=request.get('operation')
            if op not in OPERATIONS|{'execute'} or operation and op!=operation: raise ValueError()
            fields={'contract_version','company_id','operation','route'}
            required=set()
            if op=='start': fields|={'request_id','objective','target_family'}; required={'request_id','objective','target_family'}
            if op in {'status','questions','submit','execute','result','resume'}: fields.add('case_id');required.add('case_id')
            if op=='submit':
                fields|={'evidence','staged_file_id'}
                if ('evidence' in request)==('staged_file_id' in request): raise ValueError()
            if set(request)-fields or required-request.keys(): raise ValueError()
            for k in ('case_id','request_id'):
                if k in request: identity(request[k])
            if 'route' in request:
                from interfaces.public_output import ROUTES
                if request['route'] not in ROUTES: raise ValueError()
            if op=='start' and (not isinstance(request['objective'],str) or not request['objective'].strip() or len(request['objective'])>4000 or not isinstance(request['target_family'],str)): raise ValueError()
            if 'staged_file_id' in request and not re.fullmatch('[A-Za-z0-9_-]{1,80}',request['staged_file_id']): raise ValueError()
            if 'evidence' in request and not isinstance(request['evidence'],dict): raise ValueError()
        except (ValueError,TypeError,KeyError,RecursionError): raise Error('invalid_request') from None
        return dict(request)

    def call(self, company, request):
        r=self.validate(request,company)
        if r['operation']=='execute': raise Error('invalid_request')
        if 'staged_file_id' in r:
            # A host-provisioned regular JSON file. No caller-supplied path is accepted.
            r['evidence_file']='staged/'+r.pop('staged_file_id')+'.json'
        with self.company_locks[company]:
            return ExecutionInterface(self.companies[company]).call(r)

    def input_hash(self, company, request):
        api=ExecutionInterface(self.companies[company])
        config=api._configuration(company)
        _,folder=api._request(request["case_id"],config)
        path=folder/"evidence.json"
        evidence=api.read_json(str(path.relative_to(self.companies[company]))) if path.exists() else None
        return hashlib.sha256(canonical([config,evidence]).encode()).hexdigest()

    def submit_job(self, company, request, key):
        with self.company_locks[company]:
            return self._submit_job(company,request,key)

    def _submit_job(self, company, request, key):
        r=self.validate(request,company,'execute')
        if not isinstance(key,str) or not re.fullmatch('[A-Za-z0-9_.:-]{1,120}',key): raise Error('invalid_request')
        # Validate ownership and request existence before acceptance; status is not execution.
        check=ExecutionInterface(self.companies[company]).call({**r,'operation':'status'})
        if not check['ok']: raise Error('not_found',404)
        payload=canonical(r);fp=hashlib.sha256(payload.encode()).hexdigest()
        jid='job-'+hashlib.sha256(canonical([company,key]).encode()).hexdigest()
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            row=c.execute('SELECT * FROM jobs WHERE company=? AND key=?',(company,key)).fetchone()
            if row:
                if row['fingerprint']!=fp: raise Error('conflict',409)
            else:
                now=time.time();c.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,NULL,NULL,?,NULL,?,?)',(jid,company,key,fp,payload,'ACCEPTED',0,self.input_hash(company,r),now,now))
        return self.job(company,jid)

    def job(self, company, jid):
        with self.db() as c: row=c.execute('SELECT * FROM jobs WHERE company=? AND id=?',(company,jid)).fetchone()
        if row is None: raise Error('not_found',404)
        out={k:row[k] for k in ('id','state','attempts','created','updated')}
        out.update(api_version=API_VERSION,company_id=company,case_id=decode(row['request'])['case_id'])
        if row['result_case']:
            # Always load latest authoritative checkpoint/currentness, never a cached accounting answer.
            with self.company_locks[company]:
                out['accounting']=ExecutionInterface(self.companies[company]).call({**decode(row['request']),'operation':'resume'})
        elif row['outcome']:
            out['accounting']=decode(row['outcome'])
        if row['error']: out['error']={'code':row['error'],'message':SAFE['unavailable']}
        return out

    def start_worker(self):
        import fcntl
        if self.worker: raise ValueError('Worker already started')
        path=checked_path(self.root/'worker.lock'); self.lockfd=os.open(path,os.O_CREAT|os.O_RDWR,0o600)
        try: fcntl.flock(self.lockfd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BaseException: os.close(self.lockfd);self.lockfd=None;raise
        self.worker=threading.Thread(target=self._loop,name='cao-jobs',daemon=True);self.worker.start()

    def run_one(self):
        with self.run_lock:
            return self._run_one()

    def _run_one(self):
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            row=c.execute("SELECT * FROM jobs WHERE state IN ('ACCEPTED','EXECUTING') ORDER BY created,id LIMIT 1").fetchone()
            if row is None:return False
            c.execute("UPDATE jobs SET state='EXECUTING',attempts=attempts+1,updated=? WHERE id=?",(time.time(),row['id']))
        started=time.monotonic();company=row['company'];request=decode(row['request']);api=ExecutionInterface(self.companies[company])
        response=None
        try:
            with self.company_locks[company]:
                response=self._execute_job(api,company,request,row)
            if response['ok']:
                state='SUCCEEDED';error=None;reference=request['case_id'] if response.get('durable') else None
            else:
                state='FAILED';error='unavailable';reference=None
        except Exception:
            state='FAILED';error='unavailable';reference=None
        with self.db() as c:
            c.execute('UPDATE jobs SET state=?,result_case=?,outcome=?,error=?,updated=? WHERE id=?',(state,reference,canonical(response) if response and response.get('ok') and not reference else None,error,time.time(),row['id']))
        LOG.info(canonical({'event':'job_finished','job_id':row['id'],'status':state,'duration_ms':round((time.monotonic()-started)*1000)}))
        return True

    def _execute_job(self,api,company,request,row):
            response=api.call({**request,'operation':'resume'})
            if not response['ok']:
                if response['error']['code']!='not_found': raise Error('unavailable',503)
                if self.input_hash(company,request)!=row['input_hash']: raise Error('conflict',409)
                response=api.call(request)
            return response

    def _loop(self):
        while not self.stop.is_set():
            try:
                if not self.run_one():self.stop.wait(.1)
            except Exception:
                LOG.error(canonical({'event':'worker_error','code':'unavailable'}));self.stop.wait(1)

    def close(self):
        self.stop.set()
        if self.worker:self.worker.join() # graceful: finish the current pure execution
        if self.lockfd is not None:os.close(self.lockfd);self.lockfd=None

    def ready(self):
        if self.worker and not self.worker.is_alive():return False
        try:
            with self.db() as c:return c.execute('PRAGMA quick_check').fetchone()[0]=='ok'
        except Exception:return False

class Server(ThreadingHTTPServer):
    daemon_threads=False
    block_on_close=True
    def __init__(self,address,service,max_connections=32):
        self.service=service;self.slots=threading.BoundedSemaphore(max_connections)
        super().__init__(address,Handler)
    def process_request(self,request,address):
        if not self.slots.acquire(blocking=False):request.close();return
        try:super().process_request(request,address)
        except BaseException:self.slots.release();raise
    def process_request_thread(self,request,address):
        try:super().process_request_thread(request,address)
        finally:self.slots.release()

class Handler(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.0'
    def setup(self):super().setup();self.connection.settimeout(10)
    def log_message(self,*args):pass
    def do_GET(self):self.handle_api()
    def do_POST(self):self.handle_api()
    def do_PUT(self):self.handle_api()
    def do_DELETE(self):self.handle_api()
    def handle_api(self):
        correlation=uuid.uuid4().hex;started=time.monotonic();status=500
        try:
            service=self.server.service
            if self.command=='GET' and self.path in ('/v1/health','/v1/readiness','/v1/version'):
                if self.path=='/v1/readiness' and not service.ready():raise Error('unavailable',503)
                value={'api_version':API_VERSION,'service':'cao','status':'ready' if self.path=='/v1/readiness' else 'ok'};status=200
            else:
                if len(self.headers.get_all('Authorization',[]))!=1 or len(self.headers.get_all('X-CAO-Company',[]))!=1:raise Error('unauthorized',401)
                company=self.headers['X-CAO-Company'];service.authenticate(self.headers['Authorization'],company)
                if self.command=='GET' and re.fullmatch('/v1/jobs/job-[0-9a-f]{64}',self.path):
                    value=service.job(company,self.path.rsplit('/',1)[1]);status=200
                elif self.command=='POST' and self.path in ('/v1/operations','/v1/jobs'):
                    if self.headers.get('Transfer-Encoding') or len(self.headers.get_all('Content-Length',[]))!=1:raise Error('invalid_request')
                    raw=self.headers['Content-Length']
                    if not re.fullmatch('[0-9]{1,10}',raw):raise Error('invalid_request')
                    size=int(raw)
                    if size>MAX_BYTES:raise Error('payload_limit',413)
                    if self.headers.get('Content-Type')!='application/json':raise Error('invalid_request')
                    data=self.rfile.read(size)
                    if len(data)!=size:raise Error('invalid_request')
                    try:body=decode(data.decode('utf-8'))
                    except (ValueError,UnicodeError):raise Error('invalid_request') from None
                    if self.path=='/v1/jobs':
                        if len(self.headers.get_all('Idempotency-Key',[]))!=1:raise Error('invalid_request')
                        value=service.submit_job(company,body,self.headers['Idempotency-Key']);status=202
                    else:
                        value=service.call(company,body);status=200 if value['ok'] else 422
                else:raise Error('not_found',404)
        except Error as exc:
            status=exc.status;value={'api_version':API_VERSION,'ok':False,'error':{'code':exc.code,'message':SAFE[exc.code]}}
        except Exception:
            status=503;value={'api_version':API_VERSION,'ok':False,'error':{'code':'unavailable','message':SAFE['unavailable']}}
        try:
            payload=canonical(value).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.send_header('X-Correlation-ID',correlation);self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(payload)
        except (OSError,ValueError):pass
        LOG.info(canonical({'event':'http','correlation_id':correlation,'status':status,'duration_ms':round((time.monotonic()-started)*1000)}))

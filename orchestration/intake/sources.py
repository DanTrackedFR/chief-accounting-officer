"""Bounded, inert extraction. No filesystem reads, scripts, formulas or OCR.

Normalized workbook/document envelopes are external extraction, not native binary
parsing. Source metadata is supplied evidence, never inferred from filenames.
"""
import copy
import csv
import hashlib
import io
import json
from dataclasses import dataclass, field, asdict

MAX_BYTES = 2_000_000
MAX_ROWS = 10_000
MAX_DEPTH = 12


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def bounded(value, depth=0):
    if depth > MAX_DEPTH: raise ValueError('Payload nesting limit')
    if isinstance(value, dict):
        if len(value) > MAX_ROWS: raise ValueError('Object size limit')
        for k, v in value.items():
            if not isinstance(k, str) or len(k) > 200: raise ValueError('Invalid field identity')
            bounded(v, depth+1)
    elif isinstance(value, list):
        if len(value) > MAX_ROWS: raise ValueError('Row limit')
        for v in value: bounded(v, depth+1)
    elif type(value) not in (str, int, float, bool, type(None)):
        raise ValueError('Non JSON payload')
    canonical(value)


@dataclass(frozen=True)
class RawSource:
    id: str
    name: str
    format: str
    payload: object
    metadata: dict = field(default_factory=dict)
    mime: str = ''
    raw_ref: str = ''


@dataclass
class Extraction:
    source: dict
    fields: dict
    tables: list
    blocks: list
    ledger: list
    errors: list = field(default_factory=list)

    def record(self): return asdict(self)


def extract(raw):
    if not isinstance(raw, RawSource): raise ValueError('RawSource required')
    if not isinstance(raw.id, str) or not raw.id or len(raw.id) > 120: raise ValueError('Source identity invalid')
    if not isinstance(raw.name, str) or not raw.name or len(raw.name) > 300: raise ValueError('Source label invalid')
    bounded(raw.payload); bounded(raw.metadata)
    if len(canonical(raw.payload).encode()) > MAX_BYTES: raise ValueError('Source size limit')
    meta = copy.deepcopy(raw.metadata)
    source = dict(id=raw.id, name=raw.name, format=raw.format, mime=raw.mime,
                  raw_ref=raw.raw_ref, fingerprint=fingerprint(raw.payload),
                  metadata=meta, parser='bounded-'+raw.format+'-v1',
                  extraction_confidence='high', accounting_authority=False,
                  unresolved_dimensions=[k for k in ('entity','period','currency') if not meta.get(k)])
    fields = {}; tables = []; blocks = []; ledger = []

    def add(value, location):
        id = raw.id+':'+str(len(fields)+1)
        fields[id] = dict(id=id, value=copy.deepcopy(value), source_id=raw.id,
                          source_fingerprint=source['fingerprint'], location=location,
                          extracted_fingerprint=fingerprint(value))
        ledger.append(dict(field=id, source_id=raw.id, location=location, method='inert extraction'))
        return id

    def table(name, records, start=1):
        if not isinstance(name, str) or not name or len(name)>120: raise ValueError('Table identity invalid')
        if not isinstance(records, list) or len(records)>MAX_ROWS: raise ValueError('Table population invalid')
        columns = []; rows = []
        for index, record in enumerate(records, start):
            if not isinstance(record, dict) or not record: raise ValueError('Table row must be a flat object')
            if 'record_id' in record and (not isinstance(record['record_id'],str) or not record['record_id'] or len(record['record_id'])>120):raise ValueError('Record identity invalid')
            ids = {}
            for column, value in record.items():
                if isinstance(value, (dict,list)): raise ValueError('Nested table cell unsupported')
                if column not in columns: columns.append(column)
                ids[column] = add(value, dict(table=name, row=index, column=column,
                                              record_id=record.get('record_id')))
            rows.append(dict(source_row=index, original=copy.deepcopy(record), fields=ids))
        tables.append(dict(name=name, original_columns=columns, rows=rows))

    fmt = raw.format
    if fmt in ('csv','tsv'):
        if not isinstance(raw.payload, str): raise ValueError('Delimited text required')
        reader = csv.reader(io.StringIO(raw.payload, newline=''), delimiter=',' if fmt=='csv' else '\t', strict=True)
        try:
            headers = next(reader)
            if not headers or any(not h for h in headers) or len(headers)!=len(set(headers)): raise ValueError('Empty or duplicated columns')
            rows = []
            for values in reader:
                if len(values)!=len(headers): raise ValueError('Malformed delimited row')
                rows.append(dict(zip(headers, values)))
                if len(rows)>MAX_ROWS: raise ValueError('Row limit')
            table('table',rows,start=2)
        except (csv.Error, StopIteration) as exc: raise ValueError('Malformed delimited source') from exc
    elif fmt=='json':
        if isinstance(raw.payload, list): table('table',raw.payload)
        elif isinstance(raw.payload, dict):
            def walk(value,path):
                if isinstance(value,dict):
                    for k,v in value.items():walk(v,path+[k])
                elif isinstance(value,list):
                    for i,v in enumerate(value):walk(v,path+[i])
                else:add(value,dict(path=path))
            walk(raw.payload,[])
        else:raise ValueError('Structured object or rows required')
    elif fmt in ('text','markdown'):
        if not isinstance(raw.payload,str):raise ValueError('Text required')
        for i,paragraph in enumerate(raw.payload.split('\n\n'),1):
            if paragraph.strip():blocks.append(dict(block=i,field=add(paragraph,dict(block=i))))
    elif fmt=='normalized_workbook':
        if not isinstance(raw.payload,dict) or set(raw.payload)!={'sheets'} or not isinstance(raw.payload['sheets'],list):raise ValueError('Normalized workbook envelope required')
        names=[]
        for sheet in raw.payload['sheets']:
            if not isinstance(sheet,dict) or set(sheet)!={'name','rows'}:raise ValueError('Normalized sheet invalid')
            if sheet['name'] in names:raise ValueError('Duplicate sheet')
            names.append(sheet['name']);table(sheet['name'],sheet['rows'])
    elif fmt=='normalized_document':
        if not isinstance(raw.payload,dict) or set(raw.payload)!={'blocks'} or not isinstance(raw.payload['blocks'],list):raise ValueError('Normalized document envelope required')
        seen=set()
        for block in raw.payload['blocks']:
            if not isinstance(block,dict) or not {'id','text'}<=set(block) or set(block)-{'id','text','page','section'}:raise ValueError('Normalized block invalid')
            if not isinstance(block['id'],str) or len(block['id'])>120 or block['id'] in seen:raise ValueError('Duplicate/invalid block identity')
            if not isinstance(block['text'],str):raise ValueError('Block text invalid')
            if 'page' in block and (type(block['page']) is not int or not 1<=block['page']<=100_000):raise ValueError('Page invalid')
            seen.add(block['id']);loc={k:v for k,v in block.items() if k!='text'}
            blocks.append(dict(**loc,field=add(block['text'],loc)))
    else:raise ValueError('Unsupported binary/format; supply normalized text or tables through an external extractor')
    source.update(rows=sum(len(t['rows']) for t in tables), blocks=len(blocks))
    return Extraction(source,fields,tables,blocks,ledger)


class Inventory:
    def __init__(self, sources):
        self.raw = {}; self.extractions = {}; seen=set()
        for raw in sources:
            ex=extract(raw)
            if raw.id in self.raw:raise ValueError('Duplicate file ID')
            identity=(ex.source['fingerprint'],canonical(raw.metadata))
            if identity in seen:raise ValueError('Duplicate source content and scope')
            seen.add(identity);self.raw[raw.id]=copy.deepcopy(raw);self.extractions[raw.id]=ex
    def fields(self):return {k:copy.deepcopy(v) for e in self.extractions.values() for k,v in e.fields.items()}
    def verify(self):
        for id,raw in self.raw.items():
            if extract(raw).record()!=self.extractions[id].record():raise ValueError('Source or extracted row changed after extraction')
    def normalized(self):
        self.verify();return [copy.deepcopy(e.record()) for e in self.extractions.values()]

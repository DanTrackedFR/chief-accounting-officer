"""Strict shared request shapes for the additive Build 3 operations."""
COMMON={'contract_version','company_id','operation','route'}
SHAPES={
'investigate':({'request_id','objective','target_family','context','interpretation'},{'request_id','objective'}),
'document':({'case_id','event_id','document','interpretation'},{'case_id','event_id','document'}),
'continue_investigation':({'case_id','event_id','interpretation'},{'case_id','event_id'}),
'investigation':({'case_id'},{'case_id'}),
'correct_investigation':({'case_id','event_id','node_id','reason','evidence'},{'case_id','event_id','node_id','reason','evidence'}),
'rework_investigation':({'case_id','event_id','evidence'},{'case_id','event_id','evidence'})}


def validate(request):
    op=request.get('operation')
    if op not in SHAPES:return
    allowed,required=SHAPES[op]
    if set(request)-COMMON-allowed or required-set(request):raise ValueError('Investigation request fields')
    from interfaces.public_output import public_record
    public_record({'status':'blocked'},route=request.get('route','tool_output'))

"""Deterministic wire-shape validation; never accounting approval or raw diagnostics."""
CASE_OPERATIONS = {'submit','execute','status','questions','result','resume','document',
                   'continue_investigation','investigation','correct_investigation','rework_investigation'}


def item(field, explanation, category='missing_fact'):
    return dict(identifier='request.'+field,field_path=field,explanation=explanation,category=category)


def requirements(request):
    if not isinstance(request,dict):return [item('$','Request must be an object.','invalid_type')]
    needs=[]
    required=['contract_version','company_id','operation']
    op=request.get('operation')
    if op in CASE_OPERATIONS:required.append('case_id')
    if op in ('start','investigate'):required.extend(['request_id','objective'])
    if op=='start':required.append('target_family')
    for field in required:
        if not isinstance(request.get(field),str) or not request[field].strip():
            needs.append(item(field,'Supply a nonblank '+field.replace('_',' ')+'.'))
    if op=='submit':
        supplied=[k for k in ('evidence','evidence_file','staged_file_id') if k in request]
        if len(supplied)!=1:needs.append(item('evidence','Supply exactly one supported evidence submission.','invalid_shape'))
        if 'evidence' in request and not isinstance(request['evidence'],dict):needs.append(item('evidence','Evidence must be an object.','invalid_type'))
        evidence=request.get('evidence',{})
        if isinstance(evidence,dict) and isinstance(evidence.get('facts'),dict):
            for family,value in evidence['facts'].items():
                for row in value if isinstance(value,list) else [value]:
                    if isinstance(row,dict) and row.get('source_assurance')=='presumed_user_provided' and not row.get('case_id'):
                        needs.append(item('evidence.facts.'+family+'.case_id','Supply the source accounting Case binding.'))
    return needs

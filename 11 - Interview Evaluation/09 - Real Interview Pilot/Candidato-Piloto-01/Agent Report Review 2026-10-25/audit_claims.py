"""Audit explicit claim dependencies; does not infer semantics from prose."""


def audit_claims(record):
    states=record['source_states']
    violations=[]
    scopes={'candidate_knowledge','candidate_experience','candidate_performance','source_record','assessment_status'}
    used_ids=set()
    for claim in record['claims']:
        cid=claim['id'];scope=claim['scope'];refs=claim['source_ids']
        if cid in used_ids or scope not in scopes or not refs or any(ref not in states for ref in refs):
            violations.append(dict(claim_id=cid,code='INVALID_CLAIM_DEPENDENCY'));continue
        used_ids.add(cid)
        blocked=[ref for ref in refs if states[ref]=='unrecoverable']
        if blocked and scope in {'candidate_knowledge','candidate_experience','candidate_performance'}:
            violations.append(dict(claim_id=cid,code='UNRECOVERABLE_SOURCE_USED_FOR_CANDIDATE_JUDGMENT',sources=blocked))
        elif any(states[ref] not in {'usable','confirmed_wording','unrecoverable'} for ref in refs):
            violations.append(dict(claim_id=cid,code='UNSUPPORTED_SOURCE_STATE'))
    for evaluation in record.get('evaluations',[]):
        refs=evaluation['source_ids']
        if not refs or any(ref not in states for ref in refs):
            violations.append(dict(evaluation_id=evaluation['id'],code='INVALID_EVALUATION_DEPENDENCY'))
        elif evaluation['score'] is not None and any(states[ref]=='unrecoverable' for ref in refs):
            violations.append(dict(evaluation_id=evaluation['id'],code='UNRECOVERABLE_SOURCE_SCORED'))
    return dict(passed=not violations,violations=violations,
        scope='EXPLICIT_DEPENDENCIES_ONLY_NOT_FREEFORM_SEMANTIC_VALIDATION')

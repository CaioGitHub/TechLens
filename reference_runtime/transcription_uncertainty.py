"""Source-bound unresolved transcription issues and conservative assessment deferral."""
from copy import deepcopy
from hashlib import sha256

from .transcription_correction import CorrectionPolicyError


def apply_transcription_uncertainty(fixture, segments, questions, responses):
    issues = fixture.get('transcription_uncertainties', [])
    if not isinstance(issues, list):
        raise CorrectionPolicyError('Transcription uncertainties must be a list.')
    if not issues:
        return [], []
    by_id = {s['id']: s for s in segments}
    if len(by_id) != len(segments):
        raise CorrectionPolicyError('Uncertainty requires unique source segment IDs.')
    seen = set()
    records = []
    for issue in issues:
        if not isinstance(issue, dict):
            raise CorrectionPolicyError('Each transcription uncertainty must be a record.')
        for key in ('id', 'segment_id', 'original_sha256', 'reason', 'reviewer'):
            if not isinstance(issue.get(key), str) or not issue[key].strip():
                raise CorrectionPolicyError('Missing uncertainty field: ' + key)
        if issue['id'] in seen or issue.get('status') != 'unresolved':
            raise CorrectionPolicyError('Uncertainty IDs must be unique and status unresolved.')
        seen.add(issue['id'])
        segment = by_id.get(issue['segment_id'])
        if segment is None or sha256(segment['text'].encode()).hexdigest() != issue['original_sha256']:
            raise CorrectionPolicyError('Uncertainty does not match the actual source segment.')
        record = deepcopy(issue)
        record['original_text'] = segment['text']
        record['timestamp'] = segment.get('timestamp')
        record['assessment_use'] = 'NOT_CANDIDATE_EVIDENCE'
        records.append(record)
        segment.setdefault('transcription_uncertainties', []).append(deepcopy(record))

    affected = {}
    known_questions = {q['question_id'] for q in questions}

    def response_scope(response):
        qid = response['question_id']
        return ('question', qid) if qid in known_questions else ('response', response['response_id'])

    for record in records:
        segment = by_id[record['segment_id']]
        scopes = {('question', q['question_id']) for q in questions
                  if segment.get('kind') == 'question' and q['question_id'] == segment.get('question_id')}
        scopes.update(response_scope(r) for r in responses
                      if record['segment_id'] in r.get('original_segments', []))
        for scope in sorted(scopes):
            affected.setdefault(scope, []).append(record)

    for response in responses:
        related = affected.get(response_scope(response), [])
        if not related:
            continue
        # An unresolved issue cannot be hidden by historical or reviewed substitution.
        if response.get('reconstructed_text') != response.get('original_text'):
            raise CorrectionPolicyError('Unresolved transcription must retain its original response text.')
        response['transcription_uncertainties'] = deepcopy(related)
        response['evaluation_eligible'] = False
        response['needs_review'] = True
        response['reconstruction_confidence'] = 'low'

    for question in questions:
        scope = ('question', question['question_id'])
        if scope in affected:
            question['transcription_uncertainties'] = deepcopy(affected[scope])

    deferrals = []
    for scope, related in affected.items():
        deferrals.append({
            'question_id': scope[1] if scope[0] == 'question' else None,
            'response_ids': [r['response_id'] for r in responses if response_scope(r) == scope],
            'status': 'DEFERRED_TRANSCRIPTION_UNCERTAINTY',
            'score': None,
            'reason': 'Source transcription unresolved; no candidate judgment on this question.',
            'uncertainty_ids': [i['id'] for i in related],
            'source_segment_ids': list(dict.fromkeys(i['segment_id'] for i in related)),
        })
    return records, deferrals

"""Conservative, reviewable transcript correction proposals.

Context and a glossary suggest spelling repairs; they do not establish that a
candidate spoke the correct term. Lexical repairs require explicit source review.
"""
from copy import deepcopy
from difflib import SequenceMatcher
from hashlib import sha256
import json
import re
import unicodedata


class CorrectionPolicyError(ValueError):
    pass


class CorrectionReviewRequired(CorrectionPolicyError):
    pass


def _normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text.casefold()) if not unicodedata.combining(c))


def _digest(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def _protected(text):
    normalized = _normalized(text)
    terms = re.findall(
        r'\b(?:nao|nunca|jamais|sem|talvez|acho|acredito|se|quando|sempre|somente|apenas|'
        r'usaria|tentaria|faria|poderia|usei|usamos|trabalhei|configurei|implementei|tenho|'
        r'sincrono|assincrono|verdadeiro|falso|antes|depois)\b', normalized,
    )
    return terms, re.findall(r'\d+(?:[.,]\d+)?', normalized)


def _eligible(original, proposed, context):
    if _protected(original) != _protected(proposed):
        return False, 'protected_meaning_or_quantity_changed'
    if len(re.findall(r'\w+', proposed)) > len(re.findall(r'\w+', original)):
        return False, 'term_completion_not_supported'
    if SequenceMatcher(None, _normalized(original), _normalized(proposed)).ratio() < 0.8:
        return False, 'not_a_close_spelling_repair'
    if not re.search(r'(?<!\w)' + re.escape(proposed) + r'(?!\w)', context, re.IGNORECASE):
        return False, 'canonical_term_not_supported_by_context'
    return True, 'close_alias_with_context_requires_source_review'


def _fingerprint(plan):
    return _digest({
        'original_text':plan['original_text'], 'context':plan['context'],
        'source_segment_ids':plan['source_segment_ids'],
        'corrections':[{k:c[k] for k in ('id','start','end','original_text','proposed_text')} for c in plan['corrections']],
    })


def _validate(plan):
    if _fingerprint(plan) != plan.get('proposal_fingerprint'):
        raise CorrectionPolicyError('The original source or proposed edits changed after the plan was created.')
    source=plan['original_text']
    approved=sorted((c for c in plan['corrections'] if c['status']=='approved'),key=lambda c:(c['start'],c['end']))
    if any(left['end']>right['start'] for left,right in zip(approved,approved[1:])):
        raise CorrectionPolicyError('Approved edit spans overlap; conflict flags are not authoritative.')
    for c in plan['corrections']:
        if source[c['start']:c['end']] != c['original_text']:
            raise CorrectionPolicyError('Edit span does not match the source.')
        if c['status'] not in ('pending','approved','rejected'):
            raise CorrectionPolicyError('Invalid review status.')
        if c['status']=='approved':
            allowed,reason=_eligible(c['original_text'],c['proposed_text'],plan['context'])
            unfinished = bool(re.match(r'\s*\.\.\.',source[c['end']:]))
            if unfinished or not allowed or c.get('overlap_conflict') or not c.get('reviewer') or c.get('source_checked') is not True:
                raise CorrectionPolicyError('Correction was not validly source-reviewed: '+reason)


def propose_corrections(text, *, context='', glossary=None, segment_ids=()):
    if not isinstance(text,str) or not isinstance(context,str):
        raise CorrectionPolicyError('Text and context must be strings.')
    corrections=[]
    for alias,canonical in sorted((glossary or {}).items()):
        if not isinstance(alias,str) or not alias.strip() or not isinstance(canonical,str) or not canonical.strip():
            raise CorrectionPolicyError('Glossary entries must be nonempty strings.')
        for match in re.finditer(r'(?<!\w)'+re.escape(alias)+r'(?!\w)',text,re.IGNORECASE):
            original=match.group()
            if original==canonical:
                continue
            eligible,reason=_eligible(original,canonical,context)
            if re.match(r'\s*\.\.\.',text[match.end():]):
                eligible,reason=False,'unfinished_utterance_requires_review'
            corrections.append({
                'id':_digest([text,match.start(),match.end(),canonical])[:16],
                'start':match.start(),'end':match.end(),'original_text':original,'proposed_text':canonical,
                'context_supported':bool(re.search(r'(?<!\w)'+re.escape(canonical)+r'(?!\w)',context,re.IGNORECASE)),
                'policy_eligible':eligible,'reason':reason,'status':'pending',
                'confidence':'medium' if eligible else 'low','reviewer':None,'source_checked':False,
            })
    corrections.sort(key=lambda c:(c['start'],c['end'],c['proposed_text']))
    for i,c in enumerate(corrections):
        c['overlap_conflict']=any(i!=j and c['start']<o['end'] and o['start']<c['end'] for j,o in enumerate(corrections))
        if c['overlap_conflict']:
            c['policy_eligible']=False
            c['reason']='overlapping_proposals_require_resolution'
    plan={'policy_version':'faithful-transcript-1','original_text':text,'corrected_text':text,
          'context':context,'source_segment_ids':list(segment_ids),'corrections':corrections}
    plan['proposal_fingerprint']=_fingerprint(plan)
    return plan


def materialize_corrections(plan):
    _validate(plan)
    if any(c['status']=='pending' for c in plan['corrections']):
        raise CorrectionReviewRequired('Correction proposals must be explicitly reviewed before evaluation.')
    output=plan['original_text']
    approved=[c for c in plan['corrections'] if c['status']=='approved']
    for c in reversed(approved):
        output=output[:c['start']]+c['proposed_text']+output[c['end']:]
    if _protected(plan['original_text']) != _protected(output):
        raise CorrectionPolicyError('Protected meaning markers changed.')
    return output


def approve_correction(plan, correction_id, *, reviewer, source_checked=False):
    _validate(plan)
    if not isinstance(reviewer,str) or not reviewer.strip() or source_checked is not True:
        raise CorrectionPolicyError('An identified reviewer must confirm checking the original source.')
    result=deepcopy(plan)
    selected=next((c for c in result['corrections'] if c['id']==correction_id),None)
    if selected is None:
        raise CorrectionPolicyError('Unknown correction.')
    if not selected['policy_eligible'] or selected['overlap_conflict']:
        raise CorrectionPolicyError(selected['reason'])
    selected.update(status='approved',reviewer=reviewer.strip(),source_checked=True)
    _validate(result)
    if all(c['status']!='pending' for c in result['corrections']):
        result['corrected_text']=materialize_corrections(result)
    return result


def reject_correction(plan, correction_id, *, reviewer):
    _validate(plan)
    if not isinstance(reviewer,str) or not reviewer.strip():
        raise CorrectionPolicyError('An identified reviewer is required.')
    result=deepcopy(plan)
    selected=next((c for c in result['corrections'] if c['id']==correction_id),None)
    if selected is None:
        raise CorrectionPolicyError('Unknown correction.')
    selected.update(status='rejected',reviewer=reviewer.strip())
    if all(c['status']!='pending' for c in result['corrections']):
        result['corrected_text']=materialize_corrections(result)
    return result

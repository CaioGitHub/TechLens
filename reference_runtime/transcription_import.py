"""Fail closed on declared incomplete transcription when importing scored files.

Legacy files without declarations remain compatible; absence is not fidelity proof.
"""
from hashlib import sha256
import json
from pathlib import Path
import re


FIELDS = {'transcription_uncertainties', 'evaluation_deferrals', 'assessment_complete'}
DECLARATION = re.compile(r'["\']?(?:transcription_uncertainties|evaluation_deferrals|assessment_complete)["\']?\s*:')


class TranscriptionImportBlocked(ValueError):
    def __init__(self, review):
        self.review = review
        super().__init__('Transcription import blocked: ' + '; '.join(review['blockers']))


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('Duplicate JSON field: ' + key)
        obj[key] = value
    return obj


def _load_json(text):
    return json.loads(text, object_pairs_hook=_unique_object)


def _metadata(value, origin, records, blockers):
    if isinstance(value, list):
        for item in value:
            _metadata(item, origin, records, blockers)
    elif isinstance(value, dict):
        fields = FIELDS & value.keys()
        if fields:
            record = {'origin': origin, **{k: value[k] for k in sorted(fields)}}
            records.append(record)
            for field in fields:
                entry = value[field]
                if field == 'assessment_complete':
                    if not isinstance(entry, bool) or entry is False:
                        blockers.append(f'{origin}: assessment incomplete or invalid.')
                elif not isinstance(entry, list) or entry:
                    blockers.append(f'{origin}: unresolved or unsupported {field}.')
        for key, entry in value.items():
            if key not in FIELDS:
                _metadata(entry, origin, records, blockers)


def inspect_transcription_import(evaluations=None, evidence=None, *, structured_interview=None, transcription_review=None):
    paths = {role: path for role, path in [('evaluations', evaluations), ('evidence', evidence)] if path is not None}
    if structured_interview is not None:
        paths['structured_interview'] = structured_interview
    review = {'status': 'CHECKED', 'source_hashes': {}, 'declarations': [], 'blockers': [],
              'fidelity_validated': False}
    fingerprint = {}
    for role, path in paths.items():
        try:
            raw = Path(path).read_bytes()
            review['source_hashes'][role] = sha256(raw).hexdigest()
            text = raw.decode('utf-8-sig')
        except (OSError, UnicodeError) as error:
            review['blockers'].append(f'{role}: source cannot be read ({type(error).__name__}).')
            continue
        matches = list(re.finditer(r'```json\s*\r?\n(.*?)\r?\n```', text, re.S | re.I))
        blocks = [match.group(1) for match in matches]
        remainder = text
        for match in reversed(matches):
            remainder = remainder[:match.start()] + remainder[match.end():]
        if Path(path).suffix.lower() == '.json':
            blocks = [text]
            remainder = ''
        for block in blocks:
            try:
                value = _load_json(block)
            except (ValueError, TypeError):
                if DECLARATION.search(block):
                    review['blockers'].append(f'{role}: malformed declared transcription metadata.')
                continue
            _metadata(value, role, review['declarations'], review['blockers'])
        if DECLARATION.search(remainder):
            review['blockers'].append(f'{role}: transcription metadata is not supported JSON.')

    if transcription_review is not None:
        try:
            raw = Path(transcription_review).read_bytes()
            fingerprint['review_sha256'] = sha256(raw).hexdigest()
            data = _load_json(raw.decode('utf-8-sig'))
            if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
                raise ValueError('Unsupported review schema.')
            if data.get('source_hashes') != review['source_hashes'] or set(review['source_hashes']) != set(paths):
                raise ValueError('Review does not match all configured input files.')
            if not FIELDS.issubset(data):
                raise ValueError('Review is missing completeness declarations.')
            _metadata(data, 'transcription_review', review['declarations'], review['blockers'])
        except (OSError, UnicodeError, ValueError, TypeError) as error:
            review['blockers'].append(f'transcription_review: invalid or unavailable ({type(error).__name__}).')

    fingerprint['source_hashes'] = review['source_hashes']
    review['input_fingerprint'] = sha256(json.dumps(fingerprint, sort_keys=True).encode()).hexdigest()
    review['blockers'] = list(dict.fromkeys(review['blockers']))
    if review['blockers']:
        review['status'] = 'BLOCKED'
        raise TranscriptionImportBlocked(review)
    return review

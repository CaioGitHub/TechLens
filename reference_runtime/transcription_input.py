"""Generic source-preserving input adapter, independent of pilot identities."""
from copy import deepcopy
from hashlib import sha256
import json


def _required_text(record, field):
    value=record.get(field)
    if not isinstance(value,str) or not value.strip():
        raise ValueError('Missing or invalid input field: '+field)
    return value


def build_transcription_fixture(turns, participants, *, interview_id):
    if not isinstance(interview_id,str) or not interview_id.strip():
        raise ValueError('An explicit interview ID is required.')
    if not isinstance(turns,list) or not turns or not isinstance(participants,list) or not participants:
        raise ValueError('Nonempty turn and participant lists are required.')
    names={}; ids=set(); roles=set()
    for participant in participants:
        if not isinstance(participant,dict):
            raise ValueError('Participant must be a record.')
        pid=_required_text(participant,'participant_id')
        name=_required_text(participant,'name')
        role=_required_text(participant,'role')
        if pid in ids or name in names:
            raise ValueError('Participant IDs and speaker labels must be unique.')
        if role not in {'candidate','interviewer','observer'}:
            raise ValueError('Unsupported participant role; roles must be configured explicitly.')
        names[name]=participant;ids.add(pid);roles.add(role)
    if not {'candidate','interviewer'}.issubset(roles):
        raise ValueError('At least one candidate and interviewer must be configured.')
    source_ids=set(); segments=[]; source_records=[]
    for turn in turns:
        if not isinstance(turn,dict):
            raise ValueError('Turn must be a record.')
        sid=_required_text(turn,'id')
        speaker=_required_text(turn,'speaker')
        _required_text(turn,'timestamp')
        text=_required_text(turn,'text')
        if sid in source_ids:
            raise ValueError('Source turn IDs must be unique.')
        source_ids.add(sid)
        segment=deepcopy(turn)
        if speaker in names:
            segment['participant_id']=names[speaker]['participant_id']
        else:
            segment.pop('participant_id',None)
            segment['ambiguous_speaker']=True
        segments.append(segment)
        source_records.append({'segment_id':sid,'text_sha256':sha256(text.encode('utf-8')).hexdigest()})
    fingerprint=sha256(json.dumps({'turns':turns,'participants':participants},sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
    return {'fixture_id':interview_id,'pipeline_version':'generic-transcription-1',
            'participants':deepcopy(participants),'raw_transcript':segments,
            'transcription_source':{'input_sha256':fingerprint,'segments':source_records}}

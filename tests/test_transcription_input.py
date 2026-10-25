from copy import deepcopy
import unittest

from reference_runtime import run_pipeline, PipelineBlocked
from reference_runtime.transcription_input import build_transcription_fixture


class GenericTranscriptionInputTests(unittest.TestCase):
    def participants(self):
        return [dict(participant_id='C',name='Pessoa candidata',role='candidate'),
                dict(participant_id='I1',name='Entrevistador A',role='interviewer'),
                dict(participant_id='I2',name='Entrevistador B',role='interviewer')]

    def turns(self):
        return [dict(id='T1',speaker='Entrevistador A',timestamp='00:01',text='Como você investigaria uma falha?'),
                dict(id='T2',speaker='Pessoa candidata',timestamp='00:03',text='Talvez eu olhasse o log.\nNão sei ainda.'),
                dict(id='T3',speaker='Entrevistador B',timestamp='00:07',text='Como você mediria a latência?'),
                dict(id='T4',speaker='Pessoa candidata',timestamp='00:10',text='Eu mediria p95 e p99.')]

    def build(self,turns=None,participants=None):
        return build_transcription_fixture(self.turns() if turns is None else turns,
            self.participants() if participants is None else participants,interview_id='INTERVIEW-NEW')

    def test_preserves_exact_turns_and_source_identifiers_without_mutating_inputs(self):
        turns=self.turns();participants=self.participants();before=deepcopy((turns,participants))
        fixture=build_transcription_fixture(turns,participants,interview_id='INTERVIEW-NEW')
        self.assertEqual((turns,participants),before)
        self.assertEqual(fixture['fixture_id'],'INTERVIEW-NEW')
        for original,actual in zip(turns,fixture['raw_transcript']):
            for field in ['id','speaker','timestamp','text']:
                self.assertEqual(actual[field],original[field])

    def test_multiple_interviewers_keep_their_own_identity_in_pipeline(self):
        result=run_pipeline(self.build())
        segments=result['artifacts']['speaker_attributed_transcript']
        self.assertEqual([s['participant_id'] for s in segments],['I1','C','I2','C'])
        self.assertEqual(segments[1]['text'],self.turns()[1]['text'])

    def test_unknown_speaker_is_preserved_and_marked_for_review(self):
        turns=self.turns();turns[1]['speaker']='Pessoa não identificada'
        fixture=self.build(turns=turns)
        self.assertEqual(fixture['raw_transcript'][1]['speaker'],'Pessoa não identificada')
        self.assertTrue(fixture['raw_transcript'][1]['ambiguous_speaker'])
        try:
            result=run_pipeline(fixture)
        except PipelineBlocked as error:
            result=error.result
        segment=result['artifacts']['speaker_attributed_transcript'][1]
        self.assertIsNone(segment['participant_id'])
        self.assertTrue(segment['needs_review'])

    def test_duplicate_participant_ids_or_names_are_rejected(self):
        for field in ['participant_id','name']:
            with self.subTest(field=field),self.assertRaises(ValueError):
                participants=self.participants();participants[1][field]=participants[0][field]
                self.build(participants=participants)

    def test_duplicate_source_ids_are_rejected(self):
        turns=self.turns();turns[1]['id']=turns[0]['id']
        with self.assertRaises(ValueError):
            self.build(turns=turns)

    def test_missing_timestamp_and_empty_text_are_not_invented(self):
        for field,value in [('timestamp',None),('text','')]:
            with self.subTest(field=field),self.assertRaises(ValueError):
                turns=self.turns();turns[0][field]=value
                self.build(turns=turns)

    def test_roles_are_configured_and_never_guessed(self):
        participants=self.participants();participants[0]['role']='guessed'
        with self.assertRaises(ValueError):
            self.build(participants=participants)

    def test_build_is_deterministic_and_does_not_require_pilot_names(self):
        self.assertEqual(self.build(),self.build())
        self.assertNotIn('RP05',repr(self.build()))

    def test_conflicting_source_identity_cannot_override_participant_mapping(self):
        fixture=self.build();fixture['raw_transcript'][0]['participant_id']='C'
        with self.assertRaises(ValueError):
            run_pipeline(fixture)

    def test_generic_input_keeps_source_fingerprint_and_uncertainty_gate(self):
        from hashlib import sha256
        fixture=self.build()
        fixture['transcription_uncertainties']=[dict(id='REVIEW-T2',segment_id='T2',
            original_sha256=sha256(self.turns()[1]['text'].encode()).hexdigest(),
            status='unresolved',reason='Recognition error not recoverable.',reviewer='test-reviewer')]
        result=run_pipeline(fixture)
        self.assertEqual(result['artifacts']['transcription_source'],fixture['transcription_source'])
        self.assertEqual(result['artifacts']['evaluation_deferrals'][0]['source_segment_ids'],['T2'])
        self.assertFalse(result['artifacts']['report']['assessment_complete'])


if __name__=='__main__':
    unittest.main()

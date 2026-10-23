from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from reference_runtime import run_pipeline
from reference_runtime.interview_pipeline import run_interview_pipeline
from reference_runtime.real_pilot import build_real_pilot_fixture, render_derived_artifact
from reference_runtime.transcription_correction import CorrectionPolicyError, propose_corrections
from tests.fixtures import nominal_fixture, fixture_for_case


def mark(fixture, segment_id='S02', **changes):
    text = next(s['text'] for s in fixture['transcript'] if s['id'] == segment_id)
    item = dict(id='REVIEW-1', segment_id=segment_id, original_sha256=sha256(text.encode()).hexdigest(),
                status='unresolved', reason='User identified recognition error; exact text unavailable.',
                reviewer='test-reviewer')
    item.update(changes)
    fixture['transcription_uncertainties'] = [item]
    return fixture


class TranscriptionUncertaintyTests(unittest.TestCase):
    def test_affected_question_is_deferred_without_zero_score(self):
        fixture = mark(nominal_fixture())
        before = deepcopy(fixture)
        result = run_pipeline(fixture)
        self.assertEqual(fixture, before)
        affected = result['artifacts']['reconstructed_responses'][0]
        self.assertEqual(affected['original_text'], fixture['transcript'][1]['text'])
        self.assertEqual(affected['reconstructed_text'], affected['original_text'])
        self.assertFalse(affected['evaluation_eligible'])
        self.assertEqual(affected['transcription_uncertainties'][0]['id'], 'REVIEW-1')
        self.assertEqual([e['question_id'] for e in result['artifacts']['evaluations']], ['Q1.1'])
        self.assertTrue(all(e['question_id'] != 'Q1' for e in result['artifacts']['evidence']['evidence_set']))
        deferred = result['artifacts']['evaluation_deferrals'][0]
        self.assertEqual(deferred['question_id'], 'Q1')
        self.assertIsNone(deferred['score'])
        self.assertEqual(deferred['status'], 'DEFERRED_TRANSCRIPTION_UNCERTAINTY')
        self.assertEqual(deferred['uncertainty_ids'], ['REVIEW-1'])

    def test_report_and_evidence_expose_same_uncertainty_and_partial_coverage(self):
        result = run_pipeline(mark(nominal_fixture()))
        artifacts = result['artifacts']
        self.assertEqual(artifacts['report']['evaluation_deferrals'], artifacts['evaluation_deferrals'])
        self.assertEqual(artifacts['evidence']['transcription_uncertainties'], artifacts['transcription_uncertainties'])
        self.assertFalse(artifacts['report']['assessment_complete'])
        self.assertEqual(result['readiness'], 'READY_WITH_WARNINGS')
        self.assertTrue(any('transcription' in w.lower() for w in artifacts['report']['warnings']))

    def test_unaffected_question_retains_existing_evidence_and_score(self):
        baseline = run_pipeline(nominal_fixture())
        result = run_pipeline(mark(nominal_fixture()))
        for name in ['evaluations']:
            expected = [e for e in baseline['artifacts'][name] if e['question_id'] == 'Q1.1']
            actual = [e for e in result['artifacts'][name] if e['question_id'] == 'Q1.1']
            for e in actual:
                # Operational uncertainty warnings may be added; candidate assessment stays identical.
                e['warnings'] = expected[0]['warnings']
            self.assertEqual(actual, expected)
        self.assertEqual([e for e in result['artifacts']['evidence']['evidence_set'] if e['question_id'] == 'Q1.1'],
                         [e for e in baseline['artifacts']['evidence']['evidence_set'] if e['question_id'] == 'Q1.1'])

    def test_coordinator_does_not_present_incomplete_assessment_as_ready_to_advance(self):
        result = run_interview_pipeline(mark(nominal_fixture()))
        self.assertFalse(result['readiness']['ready_for_next_stage'])
        self.assertEqual(result['artifacts']['evaluation_deferrals'][0]['question_id'], 'Q1')

    def test_uncertain_question_text_also_defers_its_answer(self):
        result = run_pipeline(mark(nominal_fixture(), 'S01'))
        self.assertEqual([e['question_id'] for e in result['artifacts']['evaluations']], ['Q1.1'])
        self.assertEqual(result['artifacts']['evaluation_deferrals'][0]['source_segment_ids'], ['S01'])

    def test_grouped_response_with_one_uncertain_segment_is_deferred_as_a_whole(self):
        result = run_pipeline(mark(fixture_for_case('multi_segment_response'), 'S02B'))
        self.assertTrue(all(e['question_id'] != 'Q1' for e in result['artifacts']['evaluations']))
        response = result['artifacts']['reconstructed_responses'][0]
        self.assertIn('Eu mediria p95.', response['original_text'])
        self.assertIn('Depois separaria as dependências.', response['original_text'])

    def test_invalid_unknown_or_stale_marks_are_rejected(self):
        for changes in [dict(segment_id='UNKNOWN'), dict(original_sha256='bad'), dict(reviewer=''),
                        dict(status='resolved'), dict(reason='')]:
            with self.subTest(changes=changes), self.assertRaises(CorrectionPolicyError):
                fixture = mark(nominal_fixture())
                fixture['transcription_uncertainties'][0].update(changes)
                run_pipeline(fixture)

    def test_duplicate_review_identifiers_are_rejected(self):
        fixture = mark(nominal_fixture())
        fixture['transcription_uncertainties'] *= 2
        with self.assertRaises(CorrectionPolicyError):
            run_pipeline(fixture)

    def test_legacy_reconstruction_does_not_silently_replace_unrecoverable_text(self):
        fixture = mark(nominal_fixture())
        fixture['reconstructions'] = {'R1': 'A completed technically correct response.'}
        with self.assertRaises(CorrectionPolicyError):
            run_pipeline(fixture)

    def test_no_change_review_plan_can_preserve_unrecoverable_text(self):
        fixture = mark(nominal_fixture())
        text = fixture['transcript'][1]['text']
        fixture['transcription_correction_plans'] = {'R1': propose_corrections(text, segment_ids=['S02'])}
        result = run_pipeline(fixture)
        self.assertEqual(result['artifacts']['reconstructed_responses'][0]['reconstructed_text'], text)
        self.assertEqual(len(result['artifacts']['evaluation_deferrals']), 1)

    def test_uncertain_experience_is_not_used_for_cross_response_contradiction(self):
        fixture = nominal_fixture()
        fixture.pop('evidence_specs')
        fixture.pop('evaluation_specs')
        fixture['transcript'][1]['text'] = 'Trabalhei em produção com esse serviço.'
        fixture['transcript'][3]['text'] = 'Nunca trabalhei em produção, só consumia.'
        result = run_pipeline(mark(fixture))
        evidence = result['artifacts']['evidence']['evidence_set']
        self.assertTrue(all(e['response_id'] != 'R1' for e in evidence))
        for item in evidence:
            for relation in item.get('relations', []):
                self.assertNotIn('R1', relation.get('response_ids', []))

    def test_existing_run_identifier_cannot_hide_new_uncertainty(self):
        previous = run_interview_pipeline(nominal_fixture(), run_id='SAME-RUN')
        result = run_interview_pipeline(mark(nominal_fixture()), run_id='SAME-RUN', previous_result=previous)
        self.assertFalse(result['reused'])
        self.assertFalse(result['readiness']['ready_for_next_stage'])

    def test_all_questions_deferred_produces_no_numeric_judgments(self):
        fixture = mark(nominal_fixture())
        second = mark(nominal_fixture(), 'S04')['transcription_uncertainties'][0]
        second['id'] = 'REVIEW-2'
        fixture['transcription_uncertainties'].append(second)
        result = run_pipeline(fixture)
        self.assertEqual(result['artifacts']['evaluations'], [])
        self.assertEqual(result['artifacts']['evidence']['evidence_set'], [])
        self.assertEqual(len(result['artifacts']['evaluation_deferrals']), 2)
        self.assertFalse(result['artifacts']['report']['assessment_complete'])

    def test_unlinked_response_does_not_taint_other_unlinked_responses(self):
        fixture = nominal_fixture()
        for number in [5, 6]:
            fixture['transcript'].append(dict(id=f'S0{number}', speaker_role='candidate',
                speaker_id='P-CANDIDATE', kind='response', response_id=f'R{number}',
                question_id='unknown', text=f'Fala sem vínculo {number}.'))
        result = run_pipeline(mark(fixture, 'S05'))
        responses = {r['response_id']: r for r in result['artifacts']['reconstructed_responses']}
        self.assertFalse(responses['R5']['evaluation_eligible'])
        self.assertNotIn('transcription_uncertainties', responses['R6'])
        deferred = result['artifacts']['evaluation_deferrals'][0]
        self.assertIsNone(deferred['question_id'])
        self.assertEqual(deferred['response_ids'], ['R5'])

    def test_real_pilot_preserves_two_errors_and_exports_their_deferrals(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root/'TRANSCRIPTION_REFERENCE_SET_MANIFEST.json').read_text(encoding='utf-8'))
        fixture = build_real_pilot_fixture(root/manifest['sources'][0]['path'])
        review = json.loads((root/'TRANSCRIPTION_PILOT_USER_REVIEW.json').read_text(encoding='utf-8'))
        fixture['transcription_uncertainties'] = []
        for assessment in review['assessments']:
            if assessment['assessment'] != 'INCORRECT':
                continue
            segment = next(s for s in fixture['raw_transcript'] if s['timestamp'] == assessment['timestamp'])
            fixture['transcription_uncertainties'].append(dict(
                id=assessment['case_id'], segment_id=segment['id'],
                original_sha256=sha256(segment['text'].encode()).hexdigest(), status='unresolved',
                reason=assessment['user_statement'], reviewer=assessment['reviewer']))
        before = deepcopy(fixture)
        result = run_interview_pipeline(fixture)
        self.assertEqual(fixture, before)
        artifacts = result['artifacts']
        self.assertEqual(len(artifacts['transcription_uncertainties']), 2)
        deferred = {d['question_id'] for d in artifacts['evaluation_deferrals']}
        self.assertEqual(len(deferred), 2)
        self.assertFalse(deferred & {e['question_id'] for e in artifacts['evaluations']})
        self.assertFalse(deferred & {e['question_id'] for e in artifacts['evidence']['evidence_set']})
        for response in artifacts['reconstructed_responses']:
            if response['question_id'] in deferred:
                self.assertEqual(response['original_text'], response['reconstructed_text'])
        for name in ['structured', 'evidence', 'evaluations', 'global']:
            rendered = render_derived_artifact(name, result)
            body = json.loads(rendered.split('```json\n', 1)[1].split('\n```', 1)[0])
            self.assertEqual(body['evaluation_deferrals'], artifacts['evaluation_deferrals'])
            self.assertFalse(body['assessment_complete'])
            self.assertEqual(len(body['transcription_uncertainties']), 2)


if __name__ == '__main__':
    unittest.main()

"""Real excerpt preservation in the correction path; not a semantic gold set.

Transport uses the nominal fixture: scores here cannot validate the real interview.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from reference_runtime import run_pipeline
from reference_runtime.transcription_correction import (
    CorrectionReviewRequired, materialize_corrections, propose_corrections,
)
from tests.fixtures import nominal_fixture

ROOT = Path(__file__).resolve().parents[1]


class TranscriptionPilotPreservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest_bytes = (ROOT / 'TRANSCRIPTION_REFERENCE_SET_MANIFEST.json').read_bytes()
        cls.manifest = json.loads(cls.manifest_bytes)
        cls.review = json.loads((ROOT / 'TRANSCRIPTION_PILOT_USER_REVIEW.json').read_text(encoding='utf-8'))
        cls.cases = {c['id']: c for c in cls.manifest['cases']}

    def excerpt(self, assessment):
        case = self.cases[assessment['case_id']]
        raw = (ROOT / case['source_path']).read_bytes()
        self.assertEqual(sha256(raw).hexdigest(), case['source_sha256'])
        text = raw.decode('utf-8-sig').splitlines()[case['source_start_line'] - 1]
        self.assertEqual(sha256(text.encode()).hexdigest(), case['excerpt_sha256'])
        return text

    def fixture(self, text):
        fixture = nominal_fixture()
        fixture['transcript'][1]['text'] = text
        return fixture

    def test_review_is_bound_to_exact_sources_and_contains_no_replacement(self):
        self.assertEqual(self.review['manifest_sha256'], sha256(self.manifest_bytes).hexdigest())
        self.assertEqual({a['case_id'] for a in self.review['assessments']}, set(self.cases))
        for assessment in self.review['assessments']:
            with self.subTest(case=assessment['case_id']):
                self.excerpt(assessment)
                self.assertIsNone(assessment['approved_replacement'])
                self.assertFalse(assessment['applied'])

    def test_six_confirmed_excerpts_survive_pipeline_without_evaluation_changes(self):
        cases = [a for a in self.review['assessments'] if a['expected_action'] == 'KEEP']
        self.assertEqual(len(cases), 6)
        for assessment in cases:
            with self.subTest(case=assessment['case_id']):
                text = self.excerpt(assessment)
                fixture = self.fixture(text)
                baseline = run_pipeline(deepcopy(fixture))
                fixture['transcription_correction_plans'] = {
                    'R1': propose_corrections(text, segment_ids=['S02'])
                }
                before = deepcopy(fixture)
                result = run_pipeline(fixture)
                response = result['artifacts']['reconstructed_responses'][0]
                self.assertEqual(response['original_text'], text)
                self.assertEqual(response['reconstructed_text'], text)
                for name in ['evidence', 'evaluations']:
                    self.assertEqual(result['artifacts'][name], baseline['artifacts'][name])
                self.assertEqual(fixture, before)

    def test_two_unrecoverable_excerpts_are_not_completed_or_replaced(self):
        cases = [a for a in self.review['assessments'] if a['assessment'] == 'INCORRECT']
        self.assertEqual(len(cases), 2)
        for assessment in cases:
            with self.subTest(case=assessment['case_id']):
                self.assertEqual(assessment['expected_action'], 'PRESERVE_ORIGINAL_FLAG_UNRESOLVED')
                self.assertEqual(assessment['exact_text_availability'], 'UNAVAILABLE_USER_CONFIRMED')
                text = self.excerpt(assessment)
                plan = propose_corrections(text, segment_ids=['S02'])
                self.assertEqual(materialize_corrections(plan), text)
                fixture = self.fixture(text)
                fixture['transcription_correction_plans'] = {'R1': plan}
                result = run_pipeline(fixture)
                response = result['artifacts']['reconstructed_responses'][0]
                self.assertEqual(response['original_text'], text)
                self.assertEqual(response['reconstructed_text'], text)

    def test_contextual_guesses_on_unrecoverable_excerpts_stay_pending(self):
        # Challenge inputs, not approved corrections or human reference text.
        guesses = {'REF-01': {'Beijava': 'Java'}, 'REF-02': {'ezure': 'Azure'}}
        for assessment in self.review['assessments']:
            if assessment['case_id'] not in guesses:
                continue
            with self.subTest(case=assessment['case_id']):
                text = self.excerpt(assessment)
                glossary = guesses[assessment['case_id']]
                plan = propose_corrections(text, context=' '.join(glossary.values()),
                                           glossary=glossary, segment_ids=['S02'])
                self.assertTrue(plan['corrections'])
                self.assertTrue(all(c['status'] == 'pending' for c in plan['corrections']))
                self.assertEqual(plan['corrected_text'], text)
                fixture = self.fixture(text)
                fixture['transcription_correction_plans'] = {'R1': plan}
                with self.assertRaises(CorrectionReviewRequired):
                    run_pipeline(fixture)


if __name__ == '__main__':
    unittest.main()

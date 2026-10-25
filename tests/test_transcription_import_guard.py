from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from reference_runtime import PilotPaths, run_interview_pipeline, load_pilot_input, load_individual_evaluations, load_evidence_set
from reference_runtime.materialization import materialize_interview_evaluation_v2

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT/'11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01'


class TranscriptionImportGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        folder = Path(self.temporary.name)
        self.evaluations = folder/'evaluations.md'
        self.evidence = folder/'evidence.md'
        self.structured = folder/'structured.md'
        self.output = folder/'output.md'
        shutil.copyfile(PILOT/'Individual Evaluations v2.md', self.evaluations)
        shutil.copyfile(PILOT/'Evidence Set v1.md', self.evidence)
        self.structured.write_text('# Structured input\n', encoding='utf-8')
        self.paths = PilotPaths(self.evaluations, self.evidence, self.output, self.structured)

    def embed(self, path, **metadata):
        with path.open('a', encoding='utf-8') as f:
            f.write('\n```json\n'+json.dumps(metadata)+'\n```\n')

    def issue(self):
        return dict(id='REVIEW-1', status='unresolved', reason='Recognition error; original unavailable.',
                    reviewer='test-reviewer', segment_id='SOURCE-1')

    def sidecar(self, **changes):
        data = dict(schema_version=1, source_hashes={
            name: sha256(getattr(self.paths,name).read_bytes()).hexdigest()
            for name in ['evaluations','evidence','structured_interview']},
            transcription_uncertainties=[self.issue()], evaluation_deferrals=[], assessment_complete=False)
        data.update(changes)
        path = self.output.with_name('review.json')
        path.write_text(json.dumps(data),encoding='utf-8')
        return path

    def assert_blocked_before_scoring(self, paths=None):
        self.output.write_text('Existing report must survive.',encoding='utf-8')
        with patch('reference_runtime.interview_pipeline.run_evaluation_engine') as engine:
            result = run_interview_pipeline(paths or self.paths)
        engine.assert_not_called()
        self.assertEqual(result['pipeline']['status'], 'BLOCKED')
        self.assertEqual(result['pipeline']['failed_stage'], '20.7')
        self.assertFalse(result['readiness']['ready_for_next_stage'])
        self.assertNotIn('evaluation_result',result['artifacts'])
        self.assertNotIn('23.2',[s['stage'] for s in result['stages']])
        self.assertEqual(self.output.read_text(encoding='utf-8'),'Existing report must survive.')
        self.assertFalse(self.output.with_suffix('.md.tmp').exists())
        return result

    def test_evaluation_file_with_unresolved_issue_blocks_before_scoring(self):
        self.embed(self.evaluations, transcription_uncertainties=[self.issue()])
        result = self.assert_blocked_before_scoring()
        self.assertEqual(result['artifacts']['transcription_import_review']['status'],'BLOCKED')

    def test_evidence_file_with_incomplete_assessment_blocks(self):
        self.embed(self.evidence,assessment_complete=False)
        self.assert_blocked_before_scoring()

    def test_structured_file_with_deferrals_blocks_even_without_response_mapping(self):
        self.embed(self.structured,evaluation_deferrals=[dict(question_id=None,score=None)])
        self.assert_blocked_before_scoring()

    def test_sidecar_is_bound_to_all_configured_source_files(self):
        paths = replace(self.paths,transcription_review=self.sidecar())
        self.assert_blocked_before_scoring(paths)

    def test_stale_sidecar_is_rejected(self):
        review = self.sidecar(transcription_uncertainties=[],assessment_complete=True)
        with self.evaluations.open('a') as f:
            f.write('\nChanged after review.\n')
        self.assert_blocked_before_scoring(replace(self.paths,transcription_review=review))

    def test_missing_review_file_is_not_silently_ignored(self):
        self.assert_blocked_before_scoring(replace(self.paths,transcription_review=self.output.with_name('absent.json')))

    def test_complete_empty_review_keeps_legacy_result(self):
        path = self.sidecar(transcription_uncertainties=[],assessment_complete=True)
        result = run_interview_pipeline(replace(self.paths,transcription_review=path))
        self.assertTrue(result['readiness']['ready_for_next_stage'])
        self.assertEqual(result['artifacts']['evaluation_result']['summary']['average_score'],4.7)

    def test_resolved_label_does_not_clear_error_without_review_workflow(self):
        issue = self.issue(); issue['status']='resolved'
        self.embed(self.evaluations,transcription_uncertainties=[issue])
        self.assert_blocked_before_scoring()

    def test_malformed_declared_metadata_blocks(self):
        with self.evaluations.open('a') as f:
            f.write('\n```json\n{"transcription_uncertainties": [broken]}\n```\n')
        self.assert_blocked_before_scoring()

    def test_yaml_declared_incompleteness_is_not_ignored(self):
        with self.evidence.open('a') as f:
            f.write('\n```yaml\nassessment_complete: false\n```\n')
        self.assert_blocked_before_scoring()

    def test_valid_json_cannot_hide_conflicting_yaml_declaration(self):
        self.embed(self.evidence,assessment_complete=True,transcription_uncertainties=[])
        with self.evidence.open('a') as f:
            f.write('\n```yaml\nassessment_complete: false\n```\n')
        self.assert_blocked_before_scoring()

    def test_duplicate_json_keys_cannot_hide_incompleteness(self):
        with self.evaluations.open('a') as f:
            f.write('\n```json\n{"assessment_complete":false,"assessment_complete":true}\n```\n')
        self.assert_blocked_before_scoring()

    def test_malformed_field_types_are_not_treated_as_complete(self):
        self.embed(self.evaluations,assessment_complete='true',transcription_uncertainties={})
        self.assert_blocked_before_scoring()

    def test_direct_materializer_accepts_source_bound_review_file_and_blocks_it(self):
        review = self.sidecar()
        with self.assertRaises(ValueError):
            materialize_interview_evaluation_v2(self.evaluations,self.evidence,self.output,
                structured_interview_path=self.structured,transcription_review=review)
        self.assertFalse(self.output.exists())

    def test_valid_review_does_not_override_inline_pending_issue(self):
        self.embed(self.evidence,transcription_uncertainties=[self.issue()])
        review = self.sidecar(transcription_uncertainties=[],assessment_complete=True)
        self.assert_blocked_before_scoring(replace(self.paths,transcription_review=review))

    def test_structured_metadata_is_also_checked_by_direct_loader(self):
        self.embed(self.structured,assessment_complete=False)
        with self.assertRaises(ValueError):
            load_pilot_input(self.evaluations,self.evidence,structured_interview=self.structured)

    def test_direct_input_loader_does_not_discard_metadata(self):
        self.embed(self.evidence,transcription_uncertainties=[self.issue()])
        with self.assertRaises(ValueError):
            load_pilot_input(self.evaluations,self.evidence)

    def test_individual_evaluation_loader_cannot_drop_uncertainty(self):
        self.embed(self.evaluations,assessment_complete=False)
        with self.assertRaises(ValueError):
            load_individual_evaluations(self.evaluations)

    def test_individual_evidence_loader_cannot_drop_uncertainty(self):
        self.embed(self.evidence,transcription_uncertainties=[self.issue()])
        with self.assertRaises(ValueError):
            load_evidence_set(self.evidence)

    def test_direct_materializer_cannot_overwrite_after_metadata_is_discovered(self):
        self.embed(self.evaluations,assessment_complete=False)
        self.output.write_text('Original output',encoding='utf-8')
        with self.assertRaises(ValueError):
            materialize_interview_evaluation_v2(self.evaluations,self.evidence,self.output)
        self.assertEqual(self.output.read_text(encoding='utf-8'),'Original output')

    def test_cached_run_does_not_hide_new_import_metadata(self):
        first=run_interview_pipeline(self.paths,run_id='same-import')
        self.embed(self.evidence,transcription_uncertainties=[self.issue()])
        result=run_interview_pipeline(self.paths,run_id='same-import',previous_result=first)
        self.assertFalse(result['reused'])
        self.assertEqual(result['pipeline']['status'],'BLOCKED')

    def test_stage_override_cannot_approve_incomplete_transcription(self):
        self.embed(self.evidence,assessment_complete=False)
        result=run_interview_pipeline(self.paths,stage_overrides={'20.7':dict(status='READY',gate='APPROVED')})
        self.assertEqual(result['pipeline']['status'],'BLOCKED')


if __name__=='__main__':
    unittest.main()

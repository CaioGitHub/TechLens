from copy import deepcopy
import unittest
from reference_runtime import run_pipeline
from reference_runtime.transcription_correction import (
    propose_corrections, approve_correction, materialize_corrections,
    CorrectionReviewRequired, CorrectionPolicyError, reject_correction,
)
from tests.fixtures import nominal_fixture


class TranscriptionCorrectionFidelityTests(unittest.TestCase):
    def plan(self, text='Eu usaria Spring Boto neste projeto.', context='A pergunta aborda Spring Boot.'):
        return propose_corrections(text, context=context, glossary={'Spring Boto': 'Spring Boot'}, segment_ids=['S02'])

    def test_proposal_preserves_original_and_waits_for_review(self):
        p = self.plan()
        self.assertEqual(p['original_text'], 'Eu usaria Spring Boto neste projeto.')
        self.assertEqual(p['corrected_text'], p['original_text'])
        self.assertEqual(p['corrections'][0]['proposed_text'], 'Spring Boot')
        with self.assertRaises(CorrectionReviewRequired):
            materialize_corrections(p)

    def test_reviewed_alias_is_applied_with_audit(self):
        p = self.plan()
        reviewed = approve_correction(p, p['corrections'][0]['id'], reviewer='source-reviewer', source_checked=True)
        self.assertEqual(materialize_corrections(reviewed), 'Eu usaria Spring Boot neste projeto.')
        self.assertEqual(p['corrected_text'], p['original_text'])
        self.assertEqual(reviewed['corrections'][0]['reviewer'], 'source-reviewer')

    def test_context_alone_does_not_approve_a_correction(self):
        p = self.plan()
        with self.assertRaises(CorrectionPolicyError):
            approve_correction(p, p['corrections'][0]['id'], reviewer='reviewer', source_checked=False)

    def test_missing_context_blocks_automatic_inference(self):
        p = self.plan(context='Qual foi sua experiencia?')
        self.assertFalse(p['corrections'][0]['context_supported'])
        with self.assertRaises(CorrectionPolicyError):
            approve_correction(p, p['corrections'][0]['id'], reviewer='reviewer', source_checked=True)

    def test_negation_uncertainty_and_modal_are_retained(self):
        text = 'Talvez eu nao usaria Spring Boto, mas eu tentaria verificar.'
        p = self.plan(text)
        p = approve_correction(p, p['corrections'][0]['id'], reviewer='reviewer', source_checked=True)
        self.assertEqual(materialize_corrections(p), text.replace('Spring Boto', 'Spring Boot'))

    def test_numeric_and_polarity_changes_are_not_orthographic_aliases(self):
        for original, proposed in [('Java 17', 'Java 21'), ('sincrono', 'assincrono'), ('nao usei', 'usei')]:
            with self.subTest(original=original):
                p = propose_corrections(original, context=proposed, glossary={original:proposed})
                with self.assertRaises(CorrectionPolicyError):
                    approve_correction(p, p['corrections'][0]['id'], reviewer='reviewer', source_checked=True)

    def test_incomplete_term_is_not_completed(self):
        p = propose_corrections('Eu usaria o Application...', context='Application Insights', glossary={'Application':'Application Insights'})
        with self.assertRaises(CorrectionPolicyError):
            approve_correction(p, p['corrections'][0]['id'], reviewer='reviewer', source_checked=True)

    def test_plan_is_deterministic_and_preserves_linebreaks(self):
        text = 'Primeira linha.\nEu usaria Spring Boto.'
        a,b = self.plan(text),self.plan(text)
        self.assertEqual(a,b)
        reviewed=approve_correction(a,a['corrections'][0]['id'],reviewer='reviewer',source_checked=True)
        self.assertEqual(materialize_corrections(reviewed),text.replace('Spring Boto','Spring Boot'))

    def test_tampered_source_or_span_is_rejected(self):
        p = self.plan()
        p['original_text'] += ' Conteudo inventado.'
        with self.assertRaises(CorrectionPolicyError):
            materialize_corrections(p)

    def test_pipeline_consumes_reviewed_text_and_preserves_original(self):
        fixture=nominal_fixture()
        original='Eu usaria Spring Boto neste projeto.'
        fixture['transcript'][1]['text']=original
        p=self.plan(original)
        p=approve_correction(p,p['corrections'][0]['id'],reviewer='reviewer',source_checked=True)
        fixture['transcription_correction_plans']={'R1':p}
        before=deepcopy(fixture)
        result=run_pipeline(fixture)
        response=result['artifacts']['reconstructed_responses'][0]
        self.assertEqual(response['original_text'],original)
        self.assertEqual(response['reconstructed_text'],'Eu usaria Spring Boot neste projeto.')
        self.assertIn('correction_audit',response)
        self.assertEqual(fixture,before)

    def test_pending_corrections_do_not_reach_evaluation(self):
        fixture=nominal_fixture()
        original='Eu usaria Spring Boto neste projeto.'
        fixture['transcript'][1]['text']=original
        fixture['transcription_correction_plans']={'R1':self.plan(original)}
        with self.assertRaises(CorrectionReviewRequired):
            run_pipeline(fixture)

    def test_no_change_plan_is_identity(self):
        p=propose_corrections('Nao sei explicar esse conceito.',context='conceito',glossary={})
        self.assertEqual(materialize_corrections(p),p['original_text'])

    def test_rejection_preserves_candidate_words(self):
        p=self.plan()
        rejected=reject_correction(p,p['corrections'][0]['id'],reviewer='reviewer')
        self.assertEqual(materialize_corrections(rejected),p['original_text'])
        self.assertEqual(rejected['corrections'][0]['status'],'rejected')

    def test_overlapping_suggestions_cannot_be_silently_applied(self):
        p=propose_corrections('Spring Boto',context='Spring Boot',glossary={'Spring Boto':'Spring Boot','Boto':'Boot'})
        self.assertTrue(all(c['overlap_conflict'] for c in p['corrections']))
        with self.assertRaises(CorrectionPolicyError):
            approve_correction(p,p['corrections'][0]['id'],reviewer='reviewer',source_checked=True)

    def test_multiple_edits_preserve_original_offsets(self):
        original='Application insight envia dados. Spring Boto atende chamadas.'
        p=propose_corrections(original,context='Application Insights e Spring Boot',
                              glossary={'Application insight':'Application Insights','Spring Boto':'Spring Boot'})
        ids=[c['id'] for c in p['corrections']]
        for cid in reversed(ids):
            p=approve_correction(p,cid,reviewer='reviewer',source_checked=True)
        self.assertEqual(materialize_corrections(p),'Application Insights envia dados. Spring Boot atende chamadas.')

    def test_wrong_source_segment_reference_blocks_the_pipeline(self):
        fixture=nominal_fixture()
        original='Eu usaria Spring Boto neste projeto.'
        fixture['transcript'][1]['text']=original
        p=propose_corrections(original,context='Spring Boot',glossary={'Spring Boto':'Spring Boot'},segment_ids=['OUTRO'])
        p=approve_correction(p,p['corrections'][0]['id'],reviewer='reviewer',source_checked=True)
        fixture['transcription_correction_plans']={'R1':p}
        with self.assertRaises(CorrectionPolicyError):
            run_pipeline(fixture)

    def test_legacy_overrides_cannot_bypass_review_in_the_new_path(self):
        fixture=nominal_fixture()
        original='Eu usaria Spring Boto neste projeto.'
        fixture['transcript'][1]['text']=original
        fixture['transcription_correction_plans']={'R1':self.plan(original)}
        fixture['reconstructions']={'R1':'Eu implementei a solucao completa.'}
        with self.assertRaises(CorrectionPolicyError):
            run_pipeline(fixture)

    def test_experience_claim_cannot_be_rewritten_as_implementation(self):
        p=propose_corrections('trabalhei',context='implementei',glossary={'trabalhei':'implementei'})
        with self.assertRaises(CorrectionPolicyError):
            approve_correction(p,p['corrections'][0]['id'],reviewer='reviewer',source_checked=True)

    def test_actual_spans_are_rechecked_even_if_conflict_flags_are_changed(self):
        p=propose_corrections('Application insight',context='Application Insights',
                              glossary={'Application insight':'Application Insights','insight':'Insights'})
        for c in p['corrections']:
            c.update(policy_eligible=True,overlap_conflict=False,status='approved',reviewer='reviewer',source_checked=True)
        with self.assertRaises(CorrectionPolicyError):
            materialize_corrections(p)


if __name__=='__main__':
    unittest.main()

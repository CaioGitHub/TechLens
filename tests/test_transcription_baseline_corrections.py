import unittest
from reference_runtime import run_blind_calibration
from tests.calibration_cases import _case


def run(question, response):
    return run_blind_calibration({'REG': _case('REG', question, response)})['REG']['artifacts']


class BaselineEvidenceCorrectionsTests(unittest.TestCase):
    def test_justified_choice_is_reasoning_without_a_technology_dictionary(self):
        for response in (
            'Eu escolheria processamento em lote pelo menor custo de agendamento.',
            'Eu optaria por entrega incremental pela necessidade de feedback antecipado.',
        ):
            with self.subTest(response=response):
                a = run('Como escolheria a abordagem?', response)
                self.assertIn('reasoning', {e['type'] for e in a['evidence']['evidence_set']})

    def test_unexplained_preference_is_not_reasoning(self):
        a = run('Como escolheria a abordagem?', 'Eu escolheria processamento em lote.')
        self.assertNotIn('reasoning', {e['type'] for e in a['evidence']['evidence_set']})

    def test_sentence_initial_modifier_is_not_a_technical_subject(self):
        for modifier in ('Depois', 'Hoje', 'Inicialmente'):
            with self.subTest(modifier=modifier):
                a = run('Como investigaria latencia?', f'Eu olharia a latencia. {modifier} eu observaria o tempo de resposta.')
                self.assertNotIn('off_topic', {e['type'] for e in a['evidence']['evidence_set']})

    def test_named_subject_mismatch_remains_detected(self):
        a = run('Como funciona Docker?', 'Kubernetes orquestra containers em clusters.')
        self.assertIn('off_topic', {e['type'] for e in a['evidence']['evidence_set']})


if __name__ == '__main__':
    unittest.main()

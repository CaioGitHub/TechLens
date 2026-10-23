"""Regression properties for the audited INC-1 extraction fixes."""
import unittest
from reference_runtime.runtime import SemanticQuestionProfiler, DiscoursePropositionEngine


class Inc1AuditFixTests(unittest.TestCase):
    def profile(self, question):
        return SemanticQuestionProfiler().profile_question(question)[0]

    def discourse(self, response):
        return DiscoursePropositionEngine().extract_discourse_profile(response)

    def test_three_requests_are_distinct(self):
        p = self.profile('Como implementar cache e como invalidar entradas e como medir acertos?')
        self.assertEqual(len(p.secondary_demands), 2)
        self.assertIn('medir', p.secondary_demands[1].description)
        demands = [p.primary_demand] + p.secondary_demands
        self.assertEqual(len({d.demand_id for d in demands}), 3)
        self.assertTrue(all(d.is_mandatory for d in demands))

    def test_mixed_request_boundaries(self):
        p = self.profile('Como configurar filas; como limitar consumo? Como medir atraso?')
        self.assertEqual(len(p.secondary_demands), 2)

    def test_entity_comparison_is_one_demand(self):
        p = self.profile('Qual a diferença entre cache local e cache remoto?')
        self.assertEqual(p.intent_mode, 'COMPARISON')
        self.assertEqual(p.secondary_demands, [])

    def test_single_and_empty_questions(self):
        for question in ('', 'Explique filas.'):
            with self.subTest(question=question):
                self.assertEqual(self.profile(question).secondary_demands, [])

    def test_middle_greeting_preserves_previous_technical_evidence(self):
        p = self.discourse('O cache reduz acessos ao disco. Boa pergunta. Usamos TTL.')
        self.assertEqual([x.text for x in p.propositions], ['O cache reduz acessos ao disco', 'Usamos TTL'])
        self.assertEqual(p.isolated_preambles, ['Boa pergunta.'])

    def test_prefix_greeting_preserves_same_sentence_evidence(self):
        p = self.discourse('Boa pergunta, usamos índices para reduzir leituras.')
        self.assertEqual(len(p.propositions), 1)
        self.assertIn('índices', p.propositions[0].text)

    def test_multiple_greetings_preserve_order(self):
        p = self.discourse('Boa pergunta. Mantemos réplica. Ótima pergunta. Usamos quorum.')
        self.assertEqual(len(p.isolated_preambles), 2)
        self.assertEqual([x.text for x in p.propositions], ['Mantemos réplica', 'Usamos quorum'])

    def test_greeting_only_has_no_technical_propositions(self):
        p = self.discourse('Boa pergunta.')
        self.assertEqual(p.propositions, [])
        self.assertEqual(len(p.isolated_preambles), 1)

    def test_personal_narrative_preserves_mechanism(self):
        p = self.discourse('Quando eu comecei minha carreira la em Recife, usamos filas para desacoplar serviços.')
        self.assertTrue(any('filas' in x.text for x in p.propositions))

    def test_refinement_is_not_retraction(self):
        p = self.discourse('Usamos cache. Ou melhor, usamos cache com TTL.')
        self.assertNotEqual(p.propositions[0].discourse_role, 'RETRACTED_ASSERTION')

    def test_explicit_polarity_reversal_retracts(self):
        for response in ('Usamos cache. Corrigindo, não usamos cache.',
                         'Não usamos cache. Quis dizer, usamos cache.'):
            with self.subTest(response=response):
                p = self.discourse(response)
                self.assertEqual(p.propositions[0].discourse_role, 'RETRACTED_ASSERTION')

    def test_different_conditions_are_not_retracted(self):
        p = self.discourse('Se há falhas, não usamos cache. Ou melhor, se há tráfego estável, usamos cache.')
        self.assertNotEqual(p.propositions[0].discourse_role, 'RETRACTED_ASSERTION')
        self.assertTrue(all(x.is_conditional for x in p.propositions))

    def test_extraction_is_deterministic(self):
        question = 'Como medir atraso e como configurar filas e como tratar falhas?'
        self.assertEqual(self.profile(question).to_dict(), self.profile(question).to_dict())
        response = 'Boa pergunta. Não removemos locks se há concorrência.'
        self.assertEqual(self.discourse(response).to_dict(), self.discourse(response).to_dict())

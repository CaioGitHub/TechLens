"""Behavioral contract coverage for the representational scope of Stage 31.7.35."""
import unittest
from reference_runtime.runtime import (
    SemanticQuestionProfiler, DiscoursePropositionEngine, VALID_INTENT_MODES,
)


class QuestionContracts(unittest.TestCase):
    def profile(self, text):
        return SemanticQuestionProfiler().profile_question(text)

    def test_sc01_all_eleven_intents(self):
        cases = {
            'DEFINITION': 'O que significa isolamento transacional?',
            'CONCEPTUAL_EXPLANATION': 'Explique o papel dos adaptadores na arquitetura.',
            'MECHANISM': 'Como funciona uma fila de prioridade?',
            'COMPARISON': 'Qual a diferença entre processo e thread?',
            'HISTORICAL': 'Quando surgiu o protocolo de consenso?',
            'CAUSALITY': 'Por que ocorre contenção no armazenamento?',
            'DIAGNOSIS': 'Como investigar atraso no consumidor?',
            'IMPLEMENTATION': 'Como configurar o limite de conexões?',
            'PROBLEM_SOLUTION': 'Como evitar perda de mensagens?',
            'DECISION_JUSTIFICATION': 'Quando adotar replicação síncrona?',
            'TRADE_OFF_ANALYSIS': 'Quais as vantagens e desvantagens da replicação?',
        }
        self.assertEqual(set(cases), set(VALID_INTENT_MODES))
        for expected, question in cases.items():
            with self.subTest(expected=expected):
                profile, _ = self.profile(question)
                self.assertEqual(profile.intent_mode, expected)
                self.assertEqual(profile.raw_question, question)

    def test_sc01_unrecognized_intent_records_uncertainty(self):
        _, uncertainty = self.profile('Considere as alternativas para o componente lunara nesta situação.')
        self.assertTrue(uncertainty.unresolved_ambiguities_present)
        self.assertNotEqual(uncertainty.confidence_level, 'HIGH')

    def test_sc02_four_requests_preserve_order(self):
        p, _ = self.profile('Como criar filas e como distribuir tarefas e como medir atraso e como limitar consumo?')
        ds = [p.primary_demand] + p.secondary_demands
        self.assertEqual(len(ds), 4)
        for demand, verb in zip(ds, ['criar', 'distribuir', 'medir', 'limitar']):
            self.assertIn(verb, demand.description)
            self.assertTrue(demand.is_mandatory)
        self.assertEqual(len({d.demand_id for d in ds}), 4)

    def test_sc02_optional_secondary_demand(self):
        p, _ = self.profile('Explique como invalidar entradas e, se souber, comente o custo de memoria.')
        self.assertEqual(len(p.secondary_demands), 1)
        self.assertTrue(p.primary_demand.is_mandatory)
        self.assertFalse(p.secondary_demands[0].is_mandatory)
        self.assertIn('custo', p.secondary_demands[0].description)

    def test_sc05_open_lowercase_entities(self):
        for left, right in [('lunara', 'velun'), ('orven', 'silori')]:
            with self.subTest(left=left):
                p, _ = self.profile(f'Compare o protocolo {left} com o protocolo {right}.')
                self.assertEqual(p.intent_mode, 'COMPARISON')
                entities = ' '.join(p.target_entities).lower()
                self.assertIn(left, entities)
                self.assertIn(right, entities)

    def test_sc06_open_numeric_context(self):
        p, _ = self.profile('Como limitar o processamento a 12 tarefas simultaneas?')
        self.assertTrue(any('12 tarefas simultaneas' in q for q in p.context_qualifiers))

    def test_sc06_shared_operational_context(self):
        p, _ = self.profile('Como configurar filas em producao com alta concorrencia e como medir atraso?')
        self.assertIn('producao', p.context_qualifiers)
        self.assertIn('alta concorrencia', p.context_qualifiers)
        self.assertEqual(len(p.secondary_demands), 1)

    def test_adv06_implicit_joint_demands(self):
        p, _ = self.profile('Como distribuir tarefas e preservar a ordem e tratar falhas?')
        ds = [p.primary_demand] + p.secondary_demands
        self.assertEqual(len(ds), 3)
        self.assertTrue(all(d.is_mandatory for d in ds))


class DiscourseContracts(unittest.TestCase):
    def extract(self, response):
        return DiscoursePropositionEngine().extract_discourse_profile(response)

    def test_sc17_long_preamble_keeps_technical_core(self):
        technical = 'Usamos uma fila persistente para preservar mensagens durante falhas'
        p = self.extract('Hoje peguei muito transito e fiquei parado na avenida durante bastante tempo. ' + technical + '.')
        self.assertEqual([x.text for x in p.propositions], [technical])
        self.assertEqual(len(p.isolated_preambles), 1)

    def test_adv05_long_preamble_pair_invariance(self):
        core = 'Nao removemos os locks. Se houver falhas, repetimos a operacao.'
        baseline = self.extract(core)
        prefixed = self.extract('O transito estava terrivel e a viagem levou duas horas. ' + core)
        self.assertEqual([x.to_dict() for x in baseline.propositions], [x.to_dict() for x in prefixed.propositions])

    def test_sc17_technical_narrative_is_retained(self):
        p = self.extract('Quando eu era estagiario la em Recife, implementei retries com limite para evitar sobrecarga.')
        self.assertTrue(any('retries' in x.text for x in p.propositions))

    def test_sc17_mixed_traffic_sentence_preserves_technical_clause(self):
        p = self.extract('O transito estava terrivel e configurei filas persistentes para evitar perdas.')
        self.assertTrue(any('filas persistentes' in x.text for x in p.propositions))

    def test_sc18_complete_long_negation_scope(self):
        scope = 'removemos as verificacoes de integridade das mensagens recebidas pelo consumidor antes da confirmacao'
        p = self.extract('Nao ' + scope + '.')
        self.assertTrue(p.propositions[0].is_negated)
        self.assertEqual(p.propositions[0].negation_scope, scope)

    def test_sc18_negation_does_not_leak(self):
        p = self.extract('Nao removemos os locks. Mantemos as verificacoes.')
        self.assertTrue(p.propositions[0].is_negated)
        self.assertFalse(p.propositions[1].is_negated)
        self.assertEqual(p.propositions[0].negation_scope, 'removemos os locks')

    def test_sc20_trailing_condition(self):
        p = self.extract('Usamos a replica somente se o atraso estiver abaixo do limite.')
        self.assertTrue(p.propositions[0].is_conditional)
        self.assertEqual(p.propositions[0].condition_premise, 'o atraso estiver abaixo do limite')

    def test_sc20_complete_long_condition(self):
        premise = 'a verificacao de integridade de todas as mensagens do lote terminar antes do prazo'
        p = self.extract('Se ' + premise + ', confirmamos o lote.')
        self.assertEqual(p.propositions[0].condition_premise, premise)

    def test_adv11_prevention_and_destructive_action_differ(self):
        preventive = self.extract('Nao removemos os locks para evitar acessos concorrentes.')
        destructive = self.extract('Removemos os locks para permitir acessos concorrentes.')
        self.assertTrue(preventive.propositions[0].is_negated)
        self.assertFalse(destructive.propositions[0].is_negated)
        self.assertIn('removemos os locks', preventive.propositions[0].negation_scope)

    def test_adv12_conditions_remain_local(self):
        p = self.extract('Se houver falhas, usamos a replica. Se houver trafego estavel, usamos o primario.')
        self.assertEqual([x.condition_premise for x in p.propositions], ['houver falhas', 'houver trafego estavel'])
        self.assertTrue(all(x.discourse_role != 'RETRACTED_ASSERTION' for x in p.propositions))

    def test_sc21_same_sentence_explicit_correction(self):
        p = self.extract('Usamos cache, corrigindo, nao usamos cache.')
        self.assertEqual(len(p.propositions), 2)
        self.assertEqual(p.propositions[0].discourse_role, 'RETRACTED_ASSERTION')
        self.assertTrue(p.propositions[1].is_negated)

    def test_sc21_same_sentence_refinement_is_not_retracted(self):
        p = self.extract('Usamos cache, ou melhor, usamos cache com TTL.')
        self.assertTrue(all(x.discourse_role != 'RETRACTED_ASSERTION' for x in p.propositions))

    def test_sc21_unrelated_assertion_not_retracted(self):
        p = self.extract('Usamos cache. Monitoramos filas. Corrigindo, nao usamos cache.')
        self.assertNotEqual(p.propositions[1].discourse_role, 'RETRACTED_ASSERTION')

    def test_sc21_conditional_polarity_is_not_global_retraction(self):
        p = self.extract('Se houver falhas, nao usamos cache. Corrigindo, se houver trafego estavel, usamos cache.')
        self.assertNotEqual(p.propositions[0].discourse_role, 'RETRACTED_ASSERTION')


if __name__ == '__main__':
    unittest.main()

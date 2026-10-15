"""
Stage 31.7.24 — Controlled Implementation Contract Test Suite (Cycle 4)

Verifies the 5 architectural precision remediation components approved in Stage 31.7.23:
- Increment A: Semantic Intent and Multi-Aspect Demand Extraction (CR-01) -> TC-01, TC-02
- Increment B: Demand-Proposition Nexus Bipartite Matching (CR-06) -> TC-02B
- Increment C: Discursive Genre Filtering & Morphological Circularity Analysis (CR-02, CR-03, CR-05) -> TC-03, TC-04, TC-05
- Increment D: Polarity, Evasion, and Uncertainty Ontology (CR-04, CR-07, CR-08) -> TC-06, TC-07
- Increment E: Strict Ontology Relevance Aggregator & All 7 Canonical Classes Reachable
"""

import unittest
from reference_runtime.runtime import (
    SemanticIntentAndDemandExtractor,
    PropositionDiscourseFilter,
    MorphologicalCircularityAnalyzer,
    DemandPropositionNexusBipartiteMatcher,
    StrictOntologyRelevanceAggregator,
    OpenDomainPropositionEngine,
    evaluate_open_domain_semantic_relevance,
)


class Stage31724IncrementATests(unittest.TestCase):
    """Increment A: Semantic Intent and Demand Extraction (CR-01)."""

    def setUp(self):
        self.extractor = SemanticIntentAndDemandExtractor()
        self.engine = OpenDomainPropositionEngine()

    def test_tc_01_circuit_breaker_multi_state_demands(self):
        """TC-01: Multi-state Circuit Breaker demand requires closed, open, and half-open states."""
        q = "Como o Circuit Breaker lida com falhas consecutivas e transita entre os estados fechado, aberto e meio-aberto?"
        intent, demands = self.extractor.extract_demands(q)
        self.assertGreaterEqual(len(demands), 1)
        # Check aspect goals
        all_goals = [goal for d in demands for goal in d.aspect_goals]
        self.assertIn("fechado", all_goals)
        self.assertIn("aberto", all_goals)
        self.assertIn("meio-aberto", all_goals)

        # Full coverage of all 3 states -> DIRECT
        r_full = "Quando ocorrem falhas consecutivas, o circuito sai do estado fechado e vai para o estado aberto bloqueando requisicoes; apos um timeout, passa para meio-aberto permitindo testes graduais."
        res_full = self.engine.evaluate(q, r_full)
        self.assertEqual(res_full["classification"], "DIRECT", f"TC-01 full coverage must be DIRECT: {res_full}")
        self.assertEqual(res_full["aspect_coverage"]["status"], "FULL")

        # Partial coverage omitting half-open -> PARTIAL
        r_partial = "Quando ocorrem falhas consecutivas, o circuito sai do estado fechado e transita para o estado aberto interrompendo as chamadas imediatamente."
        res_part = self.engine.evaluate(q, r_partial)
        self.assertEqual(res_part["classification"], "PARTIAL", f"TC-01 omitting half-open must be PARTIAL: {res_part}")

    def test_tc_02_saga_coordination_and_compensation(self):
        """TC-02: Saga coordination and compensation (CR-01)."""
        q = "Como o pattern Saga coordena transacoes distribuidas e executa compensacoes em caso de falha?"
        intent, demands = self.extractor.extract_demands(q)
        self.assertEqual(len(demands), 2, f"Coordinated verb phrase must yield 2 demands: {demands}")

        # Complete coverage: covers both coordination and compensation
        r_complete = "O orquestrador da saga envia comandos sequenciais para cada servico local e, se algum passo falhar, dispara transacoes compensatorias em ordem inversa para desfazer os efeitos."
        res_full = self.engine.evaluate(q, r_complete)
        self.assertEqual(res_full["classification"], "DIRECT", f"TC-02 full coverage must be DIRECT: {res_full}")

        # Partial coverage: covers coordination only, omits compensation
        r_coord_only = "A saga coordena as operacoes atraves de um orquestrador central que envia mensagens para os servicos locais executarem suas etapas comitadas."
        res_part = self.engine.evaluate(q, r_coord_only)
        self.assertEqual(res_part["classification"], "PARTIAL", f"TC-02 omitting compensation must be PARTIAL: {res_part}")


class Stage31724IncrementBTests(unittest.TestCase):
    """Increment B: Demand-Proposition Nexus Bipartite Matching (CR-06)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_tc_02b_2pc_coordinator_crash_omission(self):
        """TC-02B: 2PC coordinator crash omission (CR-06)."""
        q = "Como o protocolo Two-Phase Commit coordena transacoes distribuidas e lida com falhas caso o coordenador falhe durante a fase de commit?"
        
        # Mentioning coordinator in normal phase without addressing crash handling must NOT satisfy failure demand
        r_normal_only = "O coordenador envia a mensagem de prepare para todos os participantes e, apos receber os votos de sim, envia a mensagem de commit para confirmar a transacao."
        res_part = self.engine.evaluate(q, r_normal_only)
        self.assertEqual(res_part["classification"], "PARTIAL", f"TC-02B omitting crash recovery must be PARTIAL: {res_part}")

        # Substantive recovery handling for crash
        r_crash_handled = "O coordenador envia prepare aos participantes; se o coordenador falhar durante o commit, os participantes consultam o log de transacoes persistido em disco para resolver o bloqueio ou acionam timeout de recuperacao."
        res_full = self.engine.evaluate(q, r_crash_handled)
        self.assertEqual(res_full["classification"], "DIRECT", f"TC-02B with crash recovery must be DIRECT: {res_full}")


class Stage31724IncrementCTests(unittest.TestCase):
    """Increment C: Discursive Genre Filtering and Morphological Circularity Analysis (CR-02, CR-03, CR-05)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()
        self.circularity_analyzer = MorphologicalCircularityAnalyzer()

    def test_tc_03_creator_biography_and_historical_trivia(self):
        """TC-03: Historical trivia and creator biographies must be RELATED (CR-02 & CR-05)."""
        q = "Como o NGINX gerencia conexoes concorrentes de alta performance?"
        r_hist = "O NGINX foi escrito originalmente por Igor Sysoev no comeco dos anos 2000 para atender a um site russo de grande porte."
        res = self.engine.evaluate(q, r_hist)
        self.assertEqual(res["classification"], "RELATED", f"TC-03 historical trivia must be RELATED: {res}")
        self.assertFalse(res["functional_contribution"])

        q_rel = "Como funciona a normalizacao relacional para evitar anomalias de escrita?"
        r_rel = "O modelo relacional foi formalizado por Edgar Codd em 1970 em seu artigo classico sobre algebra relacional."
        res_rel = self.engine.evaluate(q_rel, r_rel)
        self.assertEqual(res_rel["classification"], "RELATED", f"TC-03 Codd biography must be RELATED: {res_rel}")

    def test_tc_04_autobiographical_experience_declaration(self):
        """TC-04: Autobiographical usage statements without mechanics must be RELATED (CR-02)."""
        q = "Como o Kafka garante a ordenacao das mensagens em um topico?"
        r_decl = "Na nossa empresa utilizamos o Kafka diariamente em producao ha mais de 5 anos para toda a mensageria de microservicos."
        res = self.engine.evaluate(q, r_decl)
        self.assertEqual(res["classification"], "RELATED", f"TC-04 personal declaration must be RELATED: {res}")
        self.assertFalse(res["functional_contribution"])

    def test_tc_05_morphological_circularity_analyzer(self):
        """TC-05: Morphological circular tautologies must yield UNKNOWN (CR-03)."""
        q = "Como a compressao reduz a sobrecarga de transferencia de pacotes de rede?"
        r_circ = "A compressao reduz a sobrecarga comprimindo os pacotes de forma que fiquem comprimidos com alta compressao."
        self.assertTrue(self.circularity_analyzer.detect(q, r_circ), "Circularity analyzer must detect compression tautology")

        res = self.engine.evaluate(q, r_circ)
        self.assertEqual(res["classification"], "UNKNOWN", f"TC-05 circular tautology must be UNKNOWN: {res}")
        self.assertEqual(res["relation_type"], "circular_reasoning_tautology")

        q_trav = "Por que ocorrem travamentos em transacoes concorrentes?"
        r_trav = "Ocorrem travamentos porque as transacoes ficam travadas quando ocorre um travamento de recursos."
        res_trav = self.engine.evaluate(q_trav, r_trav)
        self.assertEqual(res_trav["classification"], "UNKNOWN", f"TC-05 lock circularity must be UNKNOWN: {res_trav}")


class Stage31724IncrementDTests(unittest.TestCase):
    """Increment D: Polarity, Evasion, and Uncertainty (CR-04, CR-07, CR-08)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_tc_06_evasion_mapped_to_insufficient(self):
        """TC-06: Evasive answers must be strictly mapped to INSUFFICIENT (CR-04)."""
        q = "Como mitigar deadlocks em bancos de dados relacionais de alta concorrencia?"
        r_evasive = "Isso depende de muitos fatores e variaveis do ambiente, precisaria consultar a diretoria sobre o orcamento."
        res = self.engine.evaluate(q, r_evasive)
        self.assertEqual(res["classification"], "INSUFFICIENT", f"TC-06 evasion must be INSUFFICIENT: {res}")
        self.assertEqual(res["relation_type"], "evasive_insufficient_content")

        r_manual = "O ideal e consultar o manual e a documentacao oficial para ver os parametros exatos de configuracao."
        res_man = self.engine.evaluate(q, r_manual)
        self.assertEqual(res_man["classification"], "INSUFFICIENT", f"TC-06 doc evasion must be INSUFFICIENT: {res_man}")

    def test_tc_07_colloquial_and_passive_antithesis(self):
        """TC-07: Colloquial and passive antithesis must yield OFF_TOPIC (CR-07 & CR-08)."""
        q = "Como evitar problemas de concorrencia ao atualizar saldo bancario?"
        r_colloquial = "Eu tiro todas as travas e removo qualquer lock para nao travar as consultas."
        res_col = self.engine.evaluate(q, r_colloquial)
        self.assertEqual(res_col["classification"], "OFF_TOPIC", f"TC-07 colloquial antithesis must be OFF_TOPIC: {res_col}")

        r_passive = "O problema e resolvido se as travas forem retiradas e as transacoes acid forem desligadas."
        res_pas = self.engine.evaluate(q, r_passive)
        self.assertEqual(res_pas["classification"], "OFF_TOPIC", f"TC-07 passive antithesis must be OFF_TOPIC: {res_pas}")

        # Avoidance guard: explaining why NOT to remove locks must NOT be OFF_TOPIC
        r_guard = "Usamos versionamento otimista na tabela para evitar retirar as travas de isolamento ou desativar transacoes longas."
        res_guard = self.engine.evaluate(q, r_guard)
        self.assertNotEqual(res_guard["classification"], "OFF_TOPIC", f"TC-07 avoidance guard must NOT be OFF_TOPIC: {res_guard}")


class Stage31724IncrementETests(unittest.TestCase):
    """Increment E: Strict Ontology Relevance Aggregator & All 7 Canonical Classes Reachable."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_all_seven_canonical_classes_reachable(self):
        """Ensure all 7 canonical classes are produced deterministically."""
        expected = {"DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"}
        produced = set()
        samples = [
            ("Como particionar dados?", "Utilizo consistent hashing com aneis virtuais."),
            ("Como implementar retries com backoff e jitter?", "Implemento retries com backoff exponencial multiplicando por dois."),
            ("Como resolver contencao de locks?", "Instrumento as rotinas com metricas no Prometheus e alarmes no Grafana."),
            ("Como o Git calcula hashes?", "O Git foi criado por Linus Torvalds em 2005."),
            ("Como calcular quorum?", "Minha receita de bolo leva farinha e acucar."),
            ("Como funciona o Raft?", "Nao sei responder."),
            ("Como a replicacao garante disponibilidade?", "A replicacao garante disponibilidade porque mantem os dados disponiveis para ficarem disponiveis."),
        ]
        for q, r in samples:
            res = self.engine.evaluate(q, r)
            produced.add(res["classification"])
        self.assertEqual(expected, produced, f"All 7 canonical classes must be reachable: {produced}")


if __name__ == "__main__":
    unittest.main()

"""
Stage 31.7.16 — Controlled Implementation Test Suite

Tests increments for Stage 31.7.16 corresponding to approved contracts CTR-SEM-A through CTR-SEM-H:
- Increment 1: Morphological Normalization and Pronominal Verbs (-se) [CTR-SEM-A, CR-01]
- Increment 2: Multi-Aspect Decomposition and Proportional Coverage [CTR-SEM-B, CR-02]
- Increment 3: Causal Sufficiency and Auxiliary Action Discrimination [CTR-SEM-C, CR-03]
- Increment 4: Polarity, Negation and Inflected Antithesis [CTR-SEM-D, CR-04]
- Increment 5: Open-Domain Structural Matching and Decoupling from Closed Catalogs [CTR-SEM-E, CR-05]
- Increment 6: Epistemic Separation and Style/Length Invariance [CTR-SEM-F, CTR-SEM-G, CTR-SEM-H]
"""

import unittest
from reference_runtime.runtime import (
    OpenDomainPropositionEngine,
    evaluate_open_domain_semantic_relevance,
)


class Stage31716Increment1Tests(unittest.TestCase):
    """Increment 1: Morphological Normalization and Pronominal Verbs (-se) [CTR-SEM-A, CR-01]."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_pronominal_passive_verb_equivalence(self):
        """Active 1st-person and passive pronominal (-se) must produce identical DIRECT classification."""
        question = "Como garantir a consistencia eventual entre microservicos?"
        
        # 1st person active
        resp_active = "Publico os eventos no Kafka com outbox pattern e confirmo na tabela de eventos."
        # Passive synthetic with -se
        resp_pronominal = "Publica-se os eventos no Kafka com outbox pattern e confirma-se na tabela de eventos."
        # Passive analytic
        resp_analytic = "Os eventos sao publicados no Kafka com outbox pattern e confirmados na tabela de eventos."

        r_act = self.engine.evaluate(question, resp_active)
        r_pro = self.engine.evaluate(question, resp_pronominal)
        r_ana = self.engine.evaluate(question, resp_analytic)

        self.assertEqual(r_act["classification"], "DIRECT", f"Active should be DIRECT: {r_act}")
        self.assertEqual(r_pro["classification"], "DIRECT", f"Pronominal -se should be DIRECT: {r_pro}")
        self.assertEqual(r_ana["classification"], "DIRECT", f"Analytic passive should be DIRECT: {r_ana}")

    def test_group_o_invariance_pairs(self):
        """Pairs from Group O (formal -se vs informal 1st person) must be invariant."""
        pairs = [
            (
                "Como calcular idempotencia em requisicoes de pagamento?",
                "Gero o hash da transacao e salvo a chave no Redis com TTL.",
                "Gera-se o hash da transacao e salva-se a chave no Redis com TTL.",
            ),
            (
                "Como evitar conflitos ao persistir dados concorrentes?",
                "Uso optimistic lock com controle de versao na tabela.",
                "Usa-se optimistic lock com controle de versao na tabela.",
            ),
            (
                "Como isolar falhas entre servicos?",
                "Configuro circuit breaker para interromper requisicoes quando a taxa de erro subir.",
                "Configura-se circuit breaker para interromper requisicoes quando a taxa de erro subir.",
            ),
        ]
        for q, resp_informal, resp_formal in pairs:
            res_inf = self.engine.evaluate(q, resp_informal)
            res_form = self.engine.evaluate(q, resp_formal)
            self.assertEqual(
                res_inf["classification"],
                res_form["classification"],
                f"Invariance failed for:\nInf: {resp_informal} -> {res_inf['classification']}\nForm: {resp_formal} -> {res_form['classification']}",
            )


class Stage31716Increment2Tests(unittest.TestCase):
    """Increment 2: Multi-Aspect Decomposition and Proportional Coverage [CTR-SEM-B, CR-02]."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_compound_question_partial_coverage(self):
        """When question demands multiple mechanisms and response only provides one, classify PARTIAL."""
        q = "Como implementar retries com backoff exponencial e jitter para chamadas instaveis de rede?"
        # Only retry, no jitter
        r_partial = "Implementa-se um agendador de retentativas que calcula intervalos progressivamente maiores multiplicando a base por potencias de dois."
        # Full: retry + jitter
        r_full = "Implementa-se retries com backoff exponencial dobrando o intervalo e adicionando jitter aleatorio entre as tentativas."

        res_part = self.engine.evaluate(q, r_partial)
        res_full = self.engine.evaluate(q, r_full)

        self.assertEqual(res_part["classification"], "PARTIAL", f"Should be PARTIAL: {res_part}")
        self.assertEqual(res_full["classification"], "DIRECT", f"Should be DIRECT: {res_full}")

    def test_explicit_omission_markers(self):
        """When response explicitly mentions an omission ('mas nao detalha'), classify PARTIAL."""
        q = "Como o mecanismo detecta e desfaz deadlocks distribuidos?"
        r = "Ele constroi grafos de espera dirigidos para encontrar ciclos, porem nao explica como seleciona e aborta as transacoes causadoras."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "PARTIAL", f"Explicit omission should yield PARTIAL: {res}")


class Stage31716Increment3Tests(unittest.TestCase):
    """Increment 3: Causal Sufficiency and Auxiliary Action Discrimination [CTR-SEM-C, CR-03]."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_auxiliary_monitoring_yields_supporting(self):
        """Adding monitoring/telemetry to an operational failure demand must yield SUPPORTING, not DIRECT."""
        q = "Como resolver contencao de locks e lentidao em transacoes financeiras sob alta concorrencia?"
        r_aux = "Instrumentam-se as rotinas com metricas no Prometheus e alarmes no Grafana para identificar latencia."
        r_aux2 = "Configuro alarmes no AWS CloudWatch e envio de logs para o Elasticsearch com dashboards no Kibana."
        
        res1 = self.engine.evaluate(q, r_aux)
        res2 = self.engine.evaluate(q, r_aux2)

        self.assertEqual(res1["classification"], "SUPPORTING", f"Monitoring should be SUPPORTING: {res1}")
        self.assertEqual(res2["classification"], "SUPPORTING", f"Monitoring should be SUPPORTING: {res2}")

    def test_monitoring_when_asked_is_direct(self):
        """When question explicitly asks for metrics or diagnosis, monitoring tools are DIRECT."""
        q = "Como diagnosticar e monitorar a latencia de endpoints em producao?"
        r = "Instrumento as rotinas com metricas no Prometheus e monto dashboards no Grafana."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT", f"Diagnostic demand should be DIRECT: {res}")


class Stage31716Increment4Tests(unittest.TestCase):
    """Increment 4: Polarity, Negation and Inflected Antithesis [CTR-SEM-D, CR-04]."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_inflected_destructive_antithesis(self):
        """Destructive actions with inflected verbs must be classified as OFF_TOPIC."""
        cases = [
            (
                "Como proteger servidores contra ataques de forca bruta?",
                "Removo qualquer controle de limitacao de requisicoes e permito tentativas infinitas de login.",
            ),
            (
                "Como evitar sobrecarga quando um servico entra em colapso?",
                "Configuro os clientes para reenviar chamadas imediatamente sem timeout em loops infinitos.",
            ),
            (
                "Como aplicar o principio do menor privilegio?",
                "Concedo permissoes de superadministrador irrestritas para todas as contas sem necessidade de autenticacao.",
            ),
        ]
        for q, r in cases:
            res = self.engine.evaluate(q, r)
            self.assertEqual(res["classification"], "OFF_TOPIC", f"Destructive antithesis must be OFF_TOPIC: {q} -> {res}")


class Stage31716Increment5Tests(unittest.TestCase):
    """Increment 5: Open-Domain Structural Matching and Decoupling from Closed Catalogs [CTR-SEM-E, CR-05]."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_orthogonal_domain_disjunctions(self):
        """Frontend or AI/ML responses to backend/concurrency demands must be OFF_TOPIC."""
        cases = [
            (
                "Como alcancar consenso tolerante a falhas em nos que executam o algoritmo Raft?",
                "Eu crio um container com display flex e coloco gap de 10 pixels entre os botoes com background azul no CSS.",
            ),
            (
                "Como evitar deadlocks em transacoes financeiras com locks concorrentes?",
                "Treino um modelo de regressao linear supervisionado usando Scikit-Learn para calcular o erro medio quadratico.",
            ),
            (
                "Como rebalancear particoes em um cluster Kafka sem interrupcao de servico?",
                "Utilizo classes utilitarias do Tailwind CSS como p-4 e text-center para estruturar as tags no HTML.",
            ),
        ]
        for q, r in cases:
            res = self.engine.evaluate(q, r)
            self.assertEqual(res["classification"], "OFF_TOPIC", f"Orthogonal domain must be OFF_TOPIC: {q} -> {res}")

    def test_unseen_technology_functional_mechanism(self):
        """Unknown or fictional technologies with valid functional mechanisms must be DIRECT."""
        q = "Como o motor SuperEngine processa registros em alta velocidade?"
        r = "Ele utiliza ponteiros diretos em memoria e grava os dados em um log sequencial append-only com fsync."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT", f"Unseen tech with mechanism should be DIRECT: {res}")


class Stage31716Increment6Tests(unittest.TestCase):
    """Increment 6: Epistemic Separation and Style/Length Invariance [CTR-SEM-F, CTR-SEM-G, CTR-SEM-H]."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_all_seven_classes_reachable(self):
        """Verify that all 7 classes can be produced by the engine."""
        expected_classes = {"DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"}
        produced_classes = set()

        test_inputs = [
            # DIRECT
            ("Como particionar dados?", "Utilizo consistent hashing com aneis virtuais."),
            # PARTIAL
            ("Como implementar retries com backoff exponencial e jitter?", "Implemento retries com backoff exponencial multiplicando por dois."),
            # SUPPORTING
            ("Como resolver contencao de locks?", "Instrumento as rotinas com metricas no Prometheus e alarmes no Grafana."),
            # RELATED
            ("Como o Git calcula hashes?", "O Git foi criado por Linus Torvalds em 2005."),
            # OFF_TOPIC
            ("Como calcular quorum?", "Minha receita de bolo de chocolate leva tres ovos e farinha."),
            # INSUFFICIENT
            ("Como funciona o Raft?", "Nao sei responder."),
            # UNKNOWN
            ("Como funciona o Raft?", "Depende de muitos fatores e varia conforme a situacao."),
        ]
        for q, r in test_inputs:
            res = self.engine.evaluate(q, r)
            produced_classes.add(res["classification"])

        self.assertEqual(expected_classes, produced_classes, f"All 7 classes must be produced. Got: {produced_classes}")

    def test_length_invariance(self):
        """Short direct answer vs verbose direct answer must both be DIRECT."""
        q = "Como garantir durabilidade sem persistir tabelas de imediato?"
        r_short = "Gravando as operacoes em um log sequencial append-only no disco com fsync."
        r_long = "No contexto de bancos de dados relacionais e transacionais avancados, a abordagem padrao consagrada consiste em gravar primeiramente cada transacao confirmada de modo append-only em um log sequencial com fsync para que mesmo havendo queda de energia as paginas possam ser recuperadas da memoria."

        res_s = self.engine.evaluate(q, r_short)
        res_l = self.engine.evaluate(q, r_long)

        self.assertEqual(res_s["classification"], "DIRECT")
        self.assertEqual(res_l["classification"], "DIRECT")


if __name__ == "__main__":
    unittest.main()

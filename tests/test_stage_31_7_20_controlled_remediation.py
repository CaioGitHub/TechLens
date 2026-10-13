"""
Stage 31.7.20 — Controlled Implementation Test Suite

Verifies the 5 architectural remediation increments approved in Stage 31.7.19:
- Increment 1: Functional Sufficiency and Demand-Proposition Nexus (CR-02)
- Increment 2: Conjunctive Multi-Demand Coverage (CR-01)
- Increment 3: Informational Contribution and Structural Circularity Detection (CR-03)
- Increment 4: Polarity, Negation, and Open Antithesis in Portuguese (CR-04)
- Increment 5: Representation Invariance and Tool Bias Decoupling (CR-05)
"""

import unittest
from reference_runtime.runtime import (
    OpenDomainPropositionEngine,
    evaluate_open_domain_semantic_relevance,
)


class Stage31720Increment1Tests(unittest.TestCase):
    """Increment 1: Functional Sufficiency and Demand-Proposition Nexus (CR-02)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_institutional_metadata_without_mechanism_yields_related(self):
        """Describing open source foundation, creator, or popularity without operational mechanism must be RELATED."""
        q = "Como o algoritmo HNSW organiza grafos para busca de vizinhos mais proximos vetorial?"
        r_meta = "O Milvus e um projeto de codigo aberto sob a Linux Foundation bastante utilizado por equipes de ciencia de dados para projetos de embeddings corporativos."
        res = self.engine.evaluate(q, r_meta)
        self.assertEqual(res["classification"], "RELATED", f"Institutional metadata should be RELATED: {res}")
        self.assertFalse(res["functional_contribution"])

    def test_conceptual_definition_satisfies_definition_intent(self):
        """Definition questions must be satisfied directly by conceptual definitions without requiring operational code."""
        q = "O que e um fencing token em sistemas distribuidos?"
        r = "E um numero sequencial monotonicamente crescente entregue pelo servidor de lock para invalidar escritas de clientes pausados no storage."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT", f"Conceptual definition should be DIRECT: {res}")
        self.assertTrue(res["functional_contribution"])

    def test_creator_biography_without_mechanism_yields_related(self):
        """Creator biography and origin trivia must be RELATED, not DIRECT."""
        q = "Como o Redis gerencia estruturas de dados em memoria utilizando um unico loop de eventos?"
        r = "O Redis foi criado pelo programador italiano Salvatore Sanfilippo enquanto tentava melhorar a performance de um site."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "RELATED", f"Biographical trivia should be RELATED: {res}")


class Stage31720Increment2Tests(unittest.TestCase):
    """Increment 2: Conjunctive Multi-Demand Coverage (CR-01)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_secondary_demand_omission_strictly_yields_partial(self):
        """When question demands two aspects and response only solves aspect 1, classification must strictly be PARTIAL."""
        q = "Compare autenticacao stateless via JWT e stateful via sessao quanto a escalabilidade horizontal e facilidade de revogacao de acessos."
        # Covers JWT horizontal scalability, completely omits session revocation
        r_partial = "O JWT permite escalabilidade horizontal imediata porque os nos da aplicacao nao precisam consultar armazenamento compartilhado para checar credenciais."
        res = self.engine.evaluate(q, r_partial)
        self.assertEqual(res["classification"], "PARTIAL", f"Secondary demand omission must yield PARTIAL: {res}")
        self.assertEqual(res["aspect_coverage"]["status"], "PARTIAL")

    def test_secondary_demand_not_validated_by_single_coincident_word(self):
        """Sharing a generic word like 'dados' or 'banco' must not satisfy secondary demand."""
        q = "Como projetar endpoints de pagamento garantindo idempotencia e como armazenar os comprovantes com expiracao?"
        # Mentions idempotency, does not cover expiration or TTL
        r = "Gera-se um hash unico da transacao financeira na chegada e valida-se se a cobranca ja foi confirmada anteriormente no banco de dados."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "PARTIAL", f"Single word must not satisfy expiration demand: {res}")

    def test_full_conjunctive_satisfaction_yields_direct(self):
        """When both demands are substantively satisfied, classification is DIRECT."""
        q = "Como implementar retries com backoff exponencial e jitter para chamadas instaveis de rede?"
        r_full = "Implementa-se retries com backoff exponencial dobrando o intervalo entre tentativas e adicionando jitter aleatorio para evitar thundering herd."
        res = self.engine.evaluate(q, r_full)
        self.assertEqual(res["classification"], "DIRECT", f"Full conjunctive coverage must be DIRECT: {res}")


class Stage31720Increment3Tests(unittest.TestCase):
    """Increment 3: Informational Contribution and Structural Circularity Detection (CR-03)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_tautological_circular_reasoning_yields_unknown(self):
        """Responses that merely repeat question terms in causal clauses without info gain must yield UNKNOWN."""
        tautology_cases = [
            (
                "Por que transacoes que disputam locks exclusivos entram em estado de espera mutua?",
                "Elas entram em espera mutua porque uma transacao fica esperando a outra esperar num processo em que ambas esperam.",
            ),
            (
                "Como o particionamento de tabelas distribui carga entre servidores de banco de dados?",
                "O particionamento distribui carga porque espalha a carga distribuindo entre os servidores distribuidos.",
            ),
            (
                "Como a replicacao de dados garante alta disponibilidade em clusters distribuidos?",
                "A replicacao garante disponibilidade porque mantem os dados disponiveis para ficarem disponiveis.",
            ),
            (
                "Como o isolamento em transacoes ACID impede interferencias entre operacoes concorrentes?",
                "O isolamento impede interferencias isolando as transacoes para que cada uma fique isolada em isolamento proprio.",
            ),
        ]
        for q, r in tautology_cases:
            res = self.engine.evaluate(q, r)
            self.assertEqual(
                res["classification"],
                "UNKNOWN",
                f"Tautology must be UNKNOWN: {q} -> {r} (Got: {res['classification']})",
            )
            self.assertEqual(res["relation_type"], "circular_reasoning_tautology")

    def test_valid_explanation_with_technical_terms_not_circular(self):
        """Valid explanations using conventional technical terminology must NOT be flagged as circular."""
        q = "Como o algoritmo Raft mantem a consistencia de dados entre multiplos servidores?"
        r = "O lider exige votos da maioria do quorum contendo log estritamente atualizado antes de confirmar entradas append-entries comitadas."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT", f"Substantive technical explanation must be DIRECT: {res}")


class Stage31720Increment4Tests(unittest.TestCase):
    """Increment 4: Polarity, Negation, and Open Antithesis in Portuguese (CR-04)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_destructive_antithesis_portuguese_synonyms(self):
        """Actions proposing disabling security, locks or firewalls in Portuguese must yield OFF_TOPIC."""
        cases = [
            (
                "Como evitar conflitos ao persistir dados concorrentes?",
                "Removo qualquer bloqueio ou restricao de concorrencia e autorizo escritas simultaneas diretas na tabela sem travar linhas.",
            ),
            (
                "Como proteger endpoints contra acessos nao autenticados?",
                "Desabilito todo o firewall e libero todas as portas para que qualquer cliente acesse sem autenticacao.",
            ),
            (
                "Como proteger servicos contra ataques de sobrecarga em lote?",
                "Retiro todos os limites de chamadas e permito tentativas infinitas de requisicoes.",
            ),
        ]
        for q, r in cases:
            res = self.engine.evaluate(q, r)
            self.assertEqual(res["classification"], "OFF_TOPIC", f"Destructive antithesis must be OFF_TOPIC: {q} -> {res}")
            self.assertEqual(res["relation_type"], "destructive_antithesis_assertion")

    def test_avoidance_guard_does_not_trigger_antithesis(self):
        """Explaining why an action is avoided ('para evitar desativar locks') must NOT trigger antithesis."""
        q = "Como garantir integridade em gravacoes concorrentes?"
        r = "Uso versionamento otimista na tabela para evitar desativar locks ou travar transacoes longas."
        res = self.engine.evaluate(q, r)
        self.assertNotEqual(res["classification"], "OFF_TOPIC", f"Avoidance guard should not be OFF_TOPIC: {res}")


class Stage31720Increment5Tests(unittest.TestCase):
    """Increment 5: Representation Invariance and Tool Bias Decoupling (CR-05)."""

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_informal_engineering_phrasing_is_direct(self):
        """Valid functional mechanisms expressed in informal engineering idioms must be DIRECT."""
        q = "Como evitar que um cliente pausado por Stop-the-World cause corrupcao de dados ao despertar e gravar no storage?"
        r_informal = "A gente associa um numero sequencial crescente que o lock entrega; se a thread congelar e acordar atrasada, o banco ve que o numero dela e velho e barra o comando na porta."
        res = self.engine.evaluate(q, r_informal)
        self.assertEqual(res["classification"], "DIRECT", f"Informal engineering fencing explanation must be DIRECT: {res}")

    def test_tool_name_mention_does_not_demote_complete_operational_solution(self):
        """Mentioning HikariCP in a complete connection pool sizing and lifecycle solution must remain DIRECT."""
        q = "Como evitar esgotamento de conexoes JDBC em microsservicos de alto trafego sob concorrencia intensa?"
        r_tool = "Configura-se um pool de conexoes otimizado como HikariCP definindo tamanho maximo estrito compativel com os nucleos do banco, ativando timeout de aquisicao de 2 segundos para falhar rapido e garantindo que todas as transacoes fechem os recursos em blocos try-with-resources imediatamente apos a execucao da query."
        res = self.engine.evaluate(q, r_tool)
        self.assertEqual(res["classification"], "DIRECT", f"Detailed HikariCP solution must be DIRECT, not SUPPORTING: {res}")

    def test_pure_telemetry_monitoring_remains_supporting(self):
        """Pure monitoring/telemetry without core mechanism remains SUPPORTING."""
        q = "Como resolver contencao de locks e lentidao em transacoes financeiras sob alta concorrencia?"
        r_mon = "Instrumentam-se as rotinas com metricas no Prometheus e alarmes no Grafana para identificar latencia."
        res = self.engine.evaluate(q, r_mon)
        self.assertEqual(res["classification"], "SUPPORTING", f"Pure monitoring must be SUPPORTING: {res}")

    def test_all_seven_classes_reachable(self):
        """Ensure all 7 classes can be produced under the remediated engine."""
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
        self.assertEqual(expected, produced, f"All 7 classes must be reachable: {produced}")


if __name__ == "__main__":
    unittest.main()

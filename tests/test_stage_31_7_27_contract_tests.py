import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from reference_runtime.runtime import (
    OpenDomainPropositionEngine,
    evaluate_open_domain_semantic_relevance,
    DomainCompatibilityRecord,
    SemanticDomainDisjunctionEngine,
    DemandPropositionNexusBipartiteMatcher,
    StrictOntologyRelevanceAggregator
)


class Stage31727ContractTests(unittest.TestCase):
    """
    Stage 31.7.27 Mandatory Contract Test Suite (Cycle 5).
    Verifies that the remediated semantic runtime adheres to the 20 fundamental contracts
    approved in Stage 31.7.26, preventing false DIRECT promotions and preserving all 7 classes.
    """

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_tc_01_no_lexical_overlap_correct(self):
        """TC-01: Resposta correta sem sobreposição lexical deve ser DIRECT."""
        q = "Como garantir que um cluster mantenha um unico estado consistente durante particoes de rede?"
        r = "Os nos utilizam um quorum de maioria e um lider eleito para validar qualquer transicao de estado antes de persistir."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_02_semantically_disjoint_domain(self):
        """TC-02: Resposta de domínio semanticamente disjunto (botânica) deve ser OFF_TOPIC."""
        q = "Como funciona o roteamento de pacotes no protocolo BGP?"
        r = "Para cuidar de orquideas regamos duas vezes por semana com adubo foliar equilibrado e poda cuidadosa das folhas secas."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "OFF_TOPIC")
        self.assertFalse(res["functional_contribution"])

    def test_tc_03_thematic_no_functional_mechanism(self):
        """TC-03: Resposta temática sem atendimento funcional (metadados institucionais) deve ser RELATED."""
        q = "Como o Kafka particiona as mensagens em um topico?"
        r = "O Apache Kafka pertence a categoria de solucoes modernas de computacao e foi desenvolvido pela fundacao de software livre com ampla popularidade de mercado."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "RELATED")
        self.assertFalse(res["functional_contribution"])

    def test_tc_04_auxiliary_observability_support(self):
        """TC-04: Contribuição auxiliar de observabilidade/telemetria deve ser SUPPORTING."""
        q = "Como evitar vazamento de memoria em processos concorrentes?"
        r = "Adicionamos metricas no Prometheus e criamos alertas no Grafana para acompanhar o uso de memoria no dashboard."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "SUPPORTING")
        self.assertEqual(res["relation_type"], "auxiliary_observability_support")

    def test_tc_05_compound_partial_fulfillment(self):
        """TC-05: Atendimento parcial de pergunta composta deve ser PARTIAL."""
        q = "Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff."
        r = "O Circuit Breaker transita entre os estados fechado, aberto e meio-aberto para interromper chamadas a servicos com falha."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "PARTIAL")

    def test_tc_06_compound_full_fulfillment(self):
        """TC-06: Atendimento completo de pergunta composta deve ser DIRECT."""
        q = "Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff."
        r = "O Circuit Breaker transita entre fechado, aberto e meio-aberto para barrar chamadas com falha, e o retry aplica exponential backoff aumentando progressivamente o intervalo entre tentativas."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_07_insufficient_deflection(self):
        """TC-07: Resposta insuficiente e evasiva com predicado genérico deve ser INSUFFICIENT."""
        q = "Como solucionar problemas de concorrencia em transacoes de banco?"
        r = "Olha, isso vai depender exclusivamente do orcamento e de muitos fatores de negocio antes de qualquer coisa."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "INSUFFICIENT")
        self.assertFalse(res["functional_contribution"])

    def test_tc_08_genuine_unknown(self):
        """TC-08: Indeterminação genuína com expressão semanticamente ambígua deve ser UNKNOWN."""
        q = "Como devemos tratar falhas intermitentes de conexao na replicacao do banco de dados?"
        r = "A abordagem pode variar conforme a situacao de como a equipe resolver fazer na hora diante da replicacao."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "UNKNOWN")

    def test_tc_09_definition_no_causality_required(self):
        """TC-09: Pergunta de definição sem exigência causal operacional satisfeita conceitualmente deve ser DIRECT."""
        q = "O que e o principio da Inversao de Dependencia?"
        r = "E o principio que dita que modulos de alto nivel nao devem depender de modulos de baixo nivel, mas ambos devem depender de abstracoes."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_10_historical_direct_answer(self):
        """TC-10: Pergunta histórica diretamente respondida deve ser DIRECT."""
        q = "Por que o Kubernetes foi doado para a Cloud Native Computing Foundation?"
        r = "Para fomentar um ecossistema neutro de governanca aberta de containers sem controle exclusivo de um unico fornecedor corporativo."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_11_comparison_direct_answer(self):
        """TC-11: Pergunta comparativa diretamente respondida com os critérios fundamentais deve ser DIRECT."""
        q = "Qual a diferenca entre processo e thread no sistema operacional?"
        r = "Processos possuem espacos de enderecamento de memoria isolados entre si, enquanto threads de um mesmo processo compartilham o mesmo espaco de memoria."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_12_diagnosis_causal_answer(self):
        """TC-12: Pergunta de diagnóstico atendida com mecanismo investigativo deve ser DIRECT."""
        q = "Como diagnosticar vazamentos de conexoes no pool de banco de dados HikariCP?"
        r = "Analisamos se conexoes ativas ultrapassam o limite do pool sem serem devolvidas no bloco try-finally e inspecionamos thread dumps para identificar a linha de codigo retendo a conexao."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_13_unseen_tech_valid_response(self):
        """TC-13: Tecnologia inédita/abstrata operando sob mecanismo canônico válido deve ser DIRECT."""
        q = "Como o banco distribuido ZetaKVS lida com conflitos de concorrencia?"
        r = "O ZetaKVS utiliza carimbos de tempo logicos de Lamport e locks otimistas com verificacao de versao no momento do commit."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_14_colloquial_and_passive_voice(self):
        """TC-14: Linguagem coloquial e voz passiva expressando solução técnica correta deve ser DIRECT."""
        q = "Como lidar com pico repentino de requisicoes sem derrubar a API?"
        r = "E colocada uma fila no meio do caminho pro consumidor ir puxando as mensagens no ritmo dele sem engasgar o banco."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_15_long_operative_disjoint(self):
        """TC-15: Resposta operacional de mecânica automotiva para pergunta de computação distribuída deve ser OFF_TOPIC."""
        q = "Como o protocolo Raft garante a consistencia do log entre lideres e seguidores?"
        r = "A troca de oleo do motor do carro deve ser realizada a cada dez mil quilometros rodados usando lubrificante sintetico 5W30 e substituindo o filtro de combustivel e pastilhas de freio para garantir a longevidade do cabecote."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "OFF_TOPIC")
        self.assertFalse(res["functional_contribution"])

    def test_tc_16_short_precise_direct(self):
        """TC-16: Resposta curta e precisa de definição deve ser DIRECT."""
        q = "O que e idempotencia em APIs REST?"
        r = "E a propriedade onde multiplas requisicoes identicas produzem exatamente o mesmo efeito que uma unica requisicao."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_17_single_dense_proposition_multiple_demands(self):
        """TC-17: Uma única proposição densa satisfazendo legitimamente ambas as demandas deve ser DIRECT."""
        q = "Como o Kafka particiona mensagens e garante a ordem de entrega?"
        r = "O Kafka calcula o hash da chave da mensagem para direciona-la a uma particao especifica onde os offsets sequenciais garantem a ordenacao estrita."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])

    def test_tc_18_circular_tautology(self):
        """TC-18: Tautologia circular reflexiva sem ganho informacional deve ser UNKNOWN."""
        q = "Como funciona a ordenacao no banco de dados?"
        r = "A ordenacao no banco funciona ordenando os dados para que eles fiquem devidamente ordenados."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "UNKNOWN")

    def test_tc_19_destructive_antithesis(self):
        """TC-19: Antítese destrutiva desativando proteções operacionais fundamentais deve ser OFF_TOPIC."""
        q = "Como garantir a durabilidade e seguranca dos dados gravados no banco relacional?"
        r = "A gente desativa o write-ahead log (WAL) e desliga a sincronizacao em disco com fsync para ficar mais rapido sem travas."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "OFF_TOPIC")
        self.assertFalse(res["functional_contribution"])

    def test_tc_20_paraphrase_invariance(self):
        """TC-20: Variação sintática em voz passiva mantendo equivalência semântica estrita deve ser DIRECT."""
        q = "Como um load balancer distribui carga entre instancias?"
        r = "As requisicoes sao distribuidas pelo balanceador de carga entre os servidores disponiveis utilizando a tecnica de round-robin sequencial."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertTrue(res["functional_contribution"])


if __name__ == "__main__":
    unittest.main()

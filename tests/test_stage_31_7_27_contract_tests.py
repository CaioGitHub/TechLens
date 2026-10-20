"""
Contract Test Suite for Stage 31.7.27 — Cycle 5 Semantic Domain Disjunction Architecture.
Tests the 20 mandatory normative contract cases approved in Stage 31.7.26 / Stage 31.7.27.
"""

import unittest
from reference_runtime.runtime import OpenDomainPropositionEngine

class TestStage31727ContractTests(unittest.TestCase):

    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    def test_tc_01_no_lexical_overlap_correct(self):
        q = "Como garantir que um cluster mantenha um unico estado consistente durante particoes de rede?"
        r = "Os nos utilizam um quorum de maioria e um lider eleito para validar qualquer transicao de estado antes de persistir."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_02_semantically_disjoint_domain(self):
        q = "Como funciona o roteamento de pacotes no protocolo BGP?"
        r = "Para cuidar de orquideas regamos duas vezes por semana com adubo foliar equilibrado e poda cuidadosa das folhas secas."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "OFF_TOPIC")

    def test_tc_03_thematic_no_functional_mechanism(self):
        q = "Como o Kafka particiona as mensagens em um topico?"
        r = "O Apache Kafka pertence a categoria de solucoes modernas de computacao e foi desenvolvido pela fundacao de software livre com ampla popularidade de mercado."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "RELATED")

    def test_tc_04_auxiliary_observability_support(self):
        q = "Como evitar vazamento de memoria em processos concorrentes?"
        r = "Adicionamos metricas no Prometheus e criamos alertas no Grafana para acompanhar o uso de memoria no dashboard."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "SUPPORTING")

    def test_tc_05_compound_partial_fulfillment(self):
        q = "Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff."
        r = "O Circuit Breaker transita entre os estados fechado, aberto e meio-aberto para interromper chamadas a servicos com falha."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "PARTIAL")

    def test_tc_06_compound_full_fulfillment(self):
        q = "Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff."
        r = "O Circuit Breaker transita entre fechado, aberto e meio-aberto para barrar chamadas com falha, e o retry aplica exponential backoff aumentando progressivamente o intervalo entre tentativas."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_07_insufficient_deflection(self):
        q = "Como solucionar problemas de concorrencia em transacoes de banco?"
        r = "Olha, isso vai depender exclusivamente do orcamento e de muitos fatores de negocio antes de qualquer coisa."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "INSUFFICIENT")

    def test_tc_08_genuine_unknown(self):
        q = "Como devemos tratar falhas intermitentes de conexao na replicacao do banco de dados?"
        r = "A abordagem pode variar conforme a situacao de como a equipe resolver fazer na hora diante da replicacao."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "UNKNOWN")

    def test_tc_09_definition_no_causality_required(self):
        q = "O que e o principio da Inversao de Dependencia?"
        r = "E o principio que dita que modulos de alto nivel nao devem depender de modulos de baixo nivel, mas ambos devem depender de abstracoes."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_10_historical_direct_answer(self):
        q = "Por que o Kubernetes foi doado para a Cloud Native Computing Foundation?"
        r = "Para fomentar um ecossistema neutro de governanca aberta de containers sem controle exclusivo de um unico fornecedor corporativo."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_11_comparison_direct_answer(self):
        q = "Qual a diferenca entre processo e thread no sistema operacional?"
        r = "Processos possuem espacos de enderecamento de memoria isolados entre si, enquanto threads de um mesmo processo compartilham o mesmo espaco de memoria."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_12_diagnosis_causal_answer(self):
        q = "Como diagnosticar vazamentos de conexoes no pool de banco de dados HikariCP?"
        r = "Analisamos se conexoes ativas ultrapassam o limite do pool sem serem devolvidas no bloco try-finally e inspecionamos thread dumps para identificar a linha de codigo retendo a conexao."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_13_unseen_tech_valid_response(self):
        q = "Como o banco distribuido ZetaKVS lida com conflitos de concorrencia?"
        r = "O ZetaKVS utiliza carimbos de tempo logicos de Lamport e locks otimistas com verificacao de versao no momento do commit."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_14_colloquial_and_passive_voice(self):
        q = "Como lidar com pico repentino de requisicoes sem derrubar a API?"
        r = "E colocada uma fila no meio do caminho pro consumidor ir puxando as mensagens no ritmo dele sem engasgar o banco."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_15_long_operative_disjoint(self):
        q = "Como o protocolo Raft garante a consistencia do log entre lideres e seguidores?"
        r = "A troca de oleo do motor do carro deve ser realizada a cada dez mil quilometros rodados usando lubrificante sintetico 5W30 e substituindo o filtro de combustivel e pastilhas de freio para garantir a longevidade do cabecote."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "OFF_TOPIC")

    def test_tc_16_short_precise_direct(self):
        q = "O que e idempotencia em APIs REST?"
        r = "E a propriedade onde multiplas requisicoes identicas produzem exatamente o mesmo efeito que uma unica requisicao."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_17_single_dense_proposition_multiple_demands(self):
        q = "Como o Kafka particiona mensagens e garante a ordem de entrega?"
        r = "O Kafka calcula o hash da chave da mensagem para direciona-la a uma particao especifica onde os offsets sequenciais garantem a ordenacao estrita."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

    def test_tc_18_circular_tautology(self):
        q = "Como funciona a ordenacao no banco de dados?"
        r = "A ordenacao no banco funciona ordenando os dados para que eles fiquem devidamente ordenados."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "UNKNOWN")

    def test_tc_19_destructive_antithesis(self):
        q = "Como garantir a durabilidade e seguranca dos dados gravados no banco relacional?"
        r = "A gente desativa o write-ahead log (WAL) e desliga a sincronizacao em disco com fsync para ficar mais rapido sem travas."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "OFF_TOPIC")

    def test_tc_20_paraphrase_invariance(self):
        q = "Como um load balancer distribui carga entre instancias?"
        r = "As requisicoes sao distribuidas pelo balanceador de carga entre os servidores disponiveis utilizando a tecnica de round-robin sequencial."
        res = self.engine.evaluate_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")

if __name__ == "__main__":
    unittest.main()

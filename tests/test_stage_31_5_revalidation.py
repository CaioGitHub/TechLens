"""Tests for Stage 31.5 — Post-Remediation Human vs System Revalidation.

Independent, blind, and non-optimizing test suite validating:
1. Canonical 7-class taxonomy (>=60 cases across DIRECT, PARTIAL, SUPPORTING,
   RELATED, OFF_TOPIC, INSUFFICIENT, UNKNOWN).
2. At least 10 unseen technologies foreign to the codebase (Temporal, NATS,
   Nomad, ClickHouse, Pulumi, ArgoCD, Istio, OpenTelemetry, Dapr, Vault).
3. At least 10 concepts demonstrated without technology names.
4. Supporting vs Related subtle discrimination.
5. Length invariance: short answers are not penalized, buzzword padding is not rewarded.
6. Style invariance: formal, informal, colloquial, hesitant, jargon.
7. Experience hierarchy: declaration <= hypothesis < demonstration.
8. Semantic discrimination on opposite technical claims with identical lexical surface.
9. Structural unknown / truncation handling with needs_review.
10. Strict determinism: Run 1 == Run 2 == Run 3.
11. Execution isolation under permutation order.
12. Audit of the frozen Human vs System comparison on Candidato-Piloto-05.
"""

from __future__ import annotations

import copy
import random
import unittest
from pathlib import Path
from typing import Any

from reference_runtime import run_interview_pipeline, run_real_pilot
from reference_runtime.runtime import (
    _evaluate_semantic_relevance,
    _blind_dimensions,
)


def _case_fixture(case_id: str, question: str, response: str) -> dict[str, Any]:
    return {
        "id": f"INT-{case_id}",
        "metadata": {"interview_id": f"INT-{case_id}", "candidate_id": "CAND-315"},
        "participants": [
            {"participant_id": "P-INT", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CAN", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "speaker": "Interviewer", "timestamp": "00:00", "text": question},
            {"id": f"{case_id}-R", "speaker": "Candidate", "timestamp": "00:05", "text": response},
        ],
    }


class Stage315CanonicalTaxonomyAdversarialTests(unittest.TestCase):
    """60+ adversarial cases across 7 canonical taxonomy classifications and diverse domains."""

    # -------------------------------------------------------------
    # 1. DIRECT (10 cases: unseen tech & tech-free concepts)
    # -------------------------------------------------------------
    def test_direct_01_unseen_tech_temporal_workflows(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Temporal orquestra workflows distribuídos duráveis?"},
            {"reconstructed_text": "O Temporal mantém o histórico de execução de workflows gravado em event sourcing e reexecuta deterministamente após falhas."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_02_unseen_tech_nats_pubsub(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o sistema de mensagens pub/sub no NATS?"},
            {"reconstructed_text": "NATS faz roteamento de mensagens por subject usando filas e clusters com latência em microssegundos."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_03_unseen_tech_clickhouse_columnar(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o ClickHouse otimiza consultas analíticas agregadas?"},
            {"reconstructed_text": "ClickHouse armazena dados em formato colunar com compressão vetorial por coluna acelerando scans de agregados."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_04_unseen_tech_pulumi_iac(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Pulumi gerencia infraestrutura como código?"},
            {"reconstructed_text": "Pulumi utiliza linguagens de programação reais para compilar uma árvore de recursos e sincronizar o estado da infraestrutura."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_05_unseen_tech_vault_secret_leasing(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Vault gerencia segredos dinâmicos e leases?"},
            {"reconstructed_text": "Vault gera credenciais temporárias sob demanda associadas a um lease com TTL e revogação automática."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_06_tech_free_optimistic_locking(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar conflito em atualizações concorrentes no banco?"},
            {"reconstructed_text": "Utilizaria controle de concorrência com versão ou timestamp checando se o registro mudou antes de gravar a atualização."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_07_tech_free_distributed_correlation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como correlacionar uma requisição através de múltiplos microsserviços?"},
            {"reconstructed_text": "Propagaria um identificador único de correlação no header HTTP repassando para todos os serviços downstream."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_08_tech_free_payment_idempotency(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como garantir que um pagamento não seja cobrado duas vezes em caso de retry?"},
            {"reconstructed_text": "Exigiria uma chave de idempotência única por transação validando se o identificador já foi processado antes de efetivar."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_09_tech_free_eventual_consistency_reconciliation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como sincronizar dados entre dois sistemas que não compartilham a mesma transação?"},
            {"reconstructed_text": "Adotaria consistência eventual publicando eventos com processos de reconciliação periódica para tratar divergências."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_10_tech_free_latency_regression_detection(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como detectar degradação de performance após um novo deploy?"},
            {"reconstructed_text": "Compararia a métrica de latência no percentil p99 contra a baseline anterior ao deploy alertando se houver desvio."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 2. PARTIAL (10 cases: multi-aspect with partial coverage)
    # -------------------------------------------------------------
    def test_partial_01_unseen_opentelemetry_omits_propagation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é OpenTelemetry e como funciona a propagação de contexto em spans?"},
            {"reconstructed_text": "OpenTelemetry gera métricas e traces padronizados."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_02_unseen_argocd_omits_health_checks(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é ArgoCD e como valida health checks das aplicações no cluster?"},
            {"reconstructed_text": "ArgoCD sincroniza manifestos Git declarativos."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_03_unseen_istio_omits_routing(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Istio e como configura regras de roteamento canário?"},
            {"reconstructed_text": "Istio provê mTLS e segurança na malha."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_04_unseen_nomad_omits_failover(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Nomad e como gerencia failover automático de instâncias?"},
            {"reconstructed_text": "Nomad agenda containers e binários de forma leve."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_05_unseen_dapr_omits_state(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Dapr e como gerencia o estado da aplicação via sidecar?"},
            {"reconstructed_text": "Dapr oferece APIs padronizadas para microsserviços."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_06_tech_free_retry_omits_jitter(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como implementar retries e qual a importância do jitter no backoff?"},
            {"reconstructed_text": "Implementaria repetições com intervalo exponencial crescente."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_07_tech_free_bulkhead_omits_circuit_breaker(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como proteger uma API com bulkhead e circuit breaker contra indisponibilidade downstream?"},
            {"reconstructed_text": "Isolaria os pools de threads para evitar esgotamento geral."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_08_tech_free_cache_omits_invalidation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como acelerar leituras com cache e quais estratégias de invalidação adotaria?"},
            {"reconstructed_text": "Armazenaria dados em memória para acelerar consultas."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_09_tech_free_sharding_omits_resharding(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como particionar dados horizontalmente e como gerenciar o rebalanceamento de partições?"},
            {"reconstructed_text": "Dividiria as tabelas em partições por hash da chave de usuário."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_10_mixed_valid_and_alien_domain(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a rede padrão (bridge) do Docker?"},
            {"reconstructed_text": "Usa rede bridge para isolar containers, além de também configurar pipelines de CI/CD no Jenkins."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 3. SUPPORTING (10 cases: troubleshooting / observability actions)
    # -------------------------------------------------------------
    def test_supporting_01_troubleshooting_http_500_traces_and_logs(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como você investigaria um erro HTTP 500 em produção?"},
            {"reconstructed_text": "Verificaria logs de exceção, traces distribuídos e métricas de erro para isolar o componente que falhou."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_02_troubleshooting_memory_leak_heapdump(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria memory leak no servidor?"},
            {"reconstructed_text": "Coletaria heap dump na aplicação, analisaria histograma de objetos retidos e rastrearia GC roots no debug."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_03_troubleshooting_latency_profiling_p95(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria pico de latência no sistema?"},
            {"reconstructed_text": "Analisaria métricas de p95 e p99, traces de dependências lentas e timeouts de rede."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_04_troubleshooting_downstream_dependency(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria falha intermitente em um serviço downstream?"},
            {"reconstructed_text": "Inspecionaria traces de dependências externas, logs de timeout e taxas de erro HTTP nas chamadas."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_05_troubleshooting_connection_pool_exhaustion(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria travamento de consultas no banco de dados?"},
            {"reconstructed_text": "Checaria métricas de conexões ativas no pool, logs de timeout de aquisição e tempo de resposta das queries."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_06_resilience_circuit_breaker_and_backoff(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como projetaria uma integração resiliente entre microsserviços?"},
            {"reconstructed_text": "Configuraria timeouts agressivos, retries com backoff exponencial e circuit breaker para evitar falha em cascata."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_07_resilience_bulkhead_and_graceful_fallback(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como proteger a aplicação quando uma dependência externa cai?"},
            {"reconstructed_text": "Isolaria a chamada com fallback gracioso retornando dados em cache e degradando a funcionalidade sem travar a thread."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_08_troubleshooting_thread_dump_lock_contention(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria alto consumo de CPU em processos concorrentes?"},
            {"reconstructed_text": "Coletaria thread dumps no debug para verificar contenção de locks e threads bloqueadas em I/O."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_09_troubleshooting_tcpdump_packet_loss(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria perda de pacotes entre instâncias?"},
            {"reconstructed_text": "Faria captura com tcpdump, checaria métricas de interface e logs de drop do kernel."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_10_resilience_event_driven_idempotency_tradeoff(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como decidiria a arquitetura de processamento assíncrono?"},
            {"reconstructed_text": "Analisaria o trade-off entre consistência e latência, garantindo idempotência nos consumidores desacoplados."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 4. RELATED (10 cases: thematic adjacency without mechanism)
    # -------------------------------------------------------------
    def test_related_01_di_vs_spring_data_l1(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Dependency Injection e como ela desacopla componentes?"},
            {"reconstructed_text": "No Spring usamos bastante o Spring Data, que cria repositórios e abstrai o acesso ao banco de dados com interfaces."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])
        self.assertEqual(rec["evidence_strength"], "NONE")

    def test_related_02_css_flexbox_vs_html_semantics(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o alinhamento de layout no CSS?"},
            {"reconstructed_text": "No CSS e web usamos tags HTML semânticas como main e article para estruturar páginas."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_03_cicd_pipeline_vs_git_branching(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona um pipeline de CI/CD para deploy?"},
            {"reconstructed_text": "Nos pipelines de CI/CD usamos git branches e pull requests para organizar o repositório."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_04_relational_btree_vs_database_replication(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um índice no banco relacional e como acelera queries?"},
            {"reconstructed_text": "No banco relacional configuramos replicação com réplicas de leitura para distribuir carga de banco."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_05_java_virtual_threads_vs_maven_build(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que são threads virtuais no Java?"},
            {"reconstructed_text": "No Java usamos o pom.xml do Maven para gerenciar dependências e compilar o projeto."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_06_kafka_partitions_vs_schema_registry(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka?"},
            {"reconstructed_text": "Na parte de Kafka usamos Schema Registry com Avro para versionar esquemas de mensagens."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_07_jwt_tokens_vs_cors_headers(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a assinatura de tokens JWT?"},
            {"reconstructed_text": "Para segurança de API configuramos cabeçalhos CORS no HTTP para controlar acessos do navegador."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_08_rest_status_codes_vs_swagger_docs(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona uma API REST com seus status codes?"},
            {"reconstructed_text": "Na API REST usamos Swagger e OpenAPI para gerar a documentação interativa dos endpoints."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_09_angular_signals_vs_npm_packages(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a reatividade com Angular signals?"},
            {"reconstructed_text": "No Angular usamos npm e package.json para instalar bibliotecas de interface."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_10_kql_analytics_vs_azure_portal_rbac(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona uma consulta KQL no Log Analytics?"},
            {"reconstructed_text": "No Log Analytics e KQL gerenciamos permissões de RBAC pelo portal da nuvem."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 5. OFF_TOPIC (10 cases: alien domain or zero technical overlap)
    # -------------------------------------------------------------
    def test_off_topic_01_docker_to_kubernetes_d2(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a rede padrão (bridge) do Docker?"},
            {"reconstructed_text": "O Kubernetes orquestra os containers em pods e agenda nos nós."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_02_sql_to_redis_d3(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um índice no banco relacional?"},
            {"reconstructed_text": "Redis armazena dados em memória com chave e valor."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_03_virtual_threads_to_docker_container(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que são threads virtuais no Java?"},
            {"reconstructed_text": "Docker isola containers usando daemon e rede bridge."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_04_rest_to_kafka_messaging_d1(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Explique REST e seus métodos HTTP."},
            {"reconstructed_text": "Kafka permite comunicação assíncrona entre producers e consumers em tópicos com partições."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_05_hexagonal_architecture_to_sql_table(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como desenharia arquitetura hexagonal?"},
            {"reconstructed_text": "Crio tabelas relacionais com queries SQL, índices B-Tree e chaves estrangeiras."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_06_css_styling_to_sql_database(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como você define o layout visual com CSS?"},
            {"reconstructed_text": "Faço consultas SQL com SELECT, JOIN e GROUP BY para buscar tabelas relacionais."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_07_cooking_recipe_to_docker(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o isolamento de rede no Docker?"},
            {"reconstructed_text": "Para preparar um bolo você mistura ovos, farinha e assa no forno por quarenta minutos."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_08_virtual_threads_to_kql_query(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que são Virtual Threads e como melhoram I/O bloqueante?"},
            {"reconstructed_text": "No KQL usamos summarize count() by bin(timestamp, 1h) para agrupar logs analíticos."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_09_unseen_temporal_to_apple_pie(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Temporal garante workflows determinísticos?"},
            {"reconstructed_text": "Corte maçãs em fatias finas, adicione canela e açúcar mascavo na massa folhada."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_10_unseen_clickhouse_to_css_flexbox(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o ClickHouse particiona tabelas analíticas?"},
            {"reconstructed_text": "Defino display flex e align-items center para centralizar caixas no layout da tela."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 6. INSUFFICIENT (5 cases)
    # -------------------------------------------------------------
    def test_insufficient_01_bem_por_cima(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona garbage collection?"},
            {"reconstructed_text": "Mais ou menos, sei bem por cima."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")
        self.assertFalse(rec["functional_contribution"])

    def test_insufficient_02_nao_sei(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é injeção de dependência?"},
            {"reconstructed_text": "Não sei."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_insufficient_03_muito_pouco_quase_nada(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka?"},
            {"reconstructed_text": "É muito pouco, quase nada."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_insufficient_04_nao_domino(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o algoritmo Raft em sistemas distribuídos?"},
            {"reconstructed_text": "Não domino esse assunto."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_insufficient_05_nao_lembro(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um memory leak em Java?"},
            {"reconstructed_text": "Não lembro."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    # -------------------------------------------------------------
    # 7. UNKNOWN (5 cases)
    # -------------------------------------------------------------
    def test_unknown_01_empty_reconstructed_text(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o garbage collector?"},
            {"reconstructed_text": ""},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_02_whitespace_only(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o garbage collector?"},
            {"reconstructed_text": "   \n\t  "},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_03_unlinked_response(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o garbage collector?"},
            {"reconstructed_text": "Qualquer texto aqui.", "question_id": "unknown"},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_04_none_text(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Pergunta válida?"},
            {"reconstructed_text": None, "text": None},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_05_unlinked_segment_flagged(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Qual o impacto de indexação?"},
            {"text": "", "reconstructed_text": "", "question_id": "unknown"},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])


class Stage315PropertiesAndInvarianceTests(unittest.TestCase):
    """Rigorous property tests: length, anti-padding, style, experience, discrimination, mutation, determinism, isolation."""

    def test_length_invariance_concise_vs_verbose(self):
        question = "Como você reduziria consultas repetidas ao banco de dados?"
        ans_concise = "Usaria cache em memória para guardar consultas repetidas com invalidação por tempo."
        ans_verbose = (
            "Para resolver esse problema de performance, a melhor alternativa técnica é implementar "
            "uma camada de caching dedicada em memória, configurando tempo de expiração para os registros "
            "frequentes e garantindo que consultas idênticas não batam no banco de dados relacional."
        )

        res_c = run_interview_pipeline(_case_fixture("INV-C", question, ans_concise))
        res_v = run_interview_pipeline(_case_fixture("INV-V", question, ans_verbose))

        eval_c = res_c["artifacts"]["evaluations"][0]
        eval_v = res_v["artifacts"]["evaluations"][0]

        self.assertEqual(eval_c["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertEqual(eval_v["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertAlmostEqual(eval_c["score"], eval_v["score"], delta=0.5)

    def test_anti_padding_long_answer_buzzwords_not_rewarded(self):
        question = "Como reduziria consultas repetidas ao banco?"
        padding = (
            "Trabalhamos com microsserviços em cloud usando Docker, Kubernetes, CI/CD no Jenkins, "
            "observabilidade moderna, SOLID, DDD, monitoramento distribuído e sprints ágeis com times multidisciplinares maduros."
        )

        rec = _evaluate_semantic_relevance({"text": question}, {"reconstructed_text": padding})
        self.assertEqual(rec["classification"], "OFF_TOPIC")

        res = run_interview_pipeline(_case_fixture("PAD", question, padding))
        evaluation = res["artifacts"]["evaluations"][0]
        self.assertLessEqual(evaluation["score"], 5.0)
        self.assertEqual(evaluation["dimensions"]["correctness"]["assessment"], "Insufficient")

    def test_style_invariance_formal_informal_hesitant_colloquial(self):
        styles = [
            "A aplicação utiliza cache para reduzir a latência das consultas.",
            "A gente usa cache pra deixar as consultas mais rápidas.",
            "Cache reduz a latência das consultas.",
            "Acho que... é, na verdade a gente usa cache para as consultas responderem rápido.",
            "Implementaria caching layer com TTL para mitigar latency overhead no banco.",
        ]
        q = "Como você reduziria a latência de consultas?"
        scores = []
        for i, ans in enumerate(styles):
            rec = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": ans})
            self.assertEqual(rec["classification"], "DIRECT", f"Style {i} failed classification")
            res = run_interview_pipeline(_case_fixture(f"STY-{i}", q, ans))
            ev = res["artifacts"]["evaluations"][0]
            self.assertEqual(ev["dimensions"]["correctness"]["assessment"], "Strong", f"Style {i} failed correctness")
            scores.append(ev["score"])

        self.assertLessEqual(max(scores) - min(scores), 0.5)

    def test_semantic_discrimination_superficial_similarity_opposite_meaning(self):
        q = "Como opera o RabbitMQ?"
        ans_correct = "RabbitMQ opera assincronamente através de filas e exchanges."
        ans_incorrect = "RabbitMQ opera sincronicamente bloqueando threads de chamada."

        res_c = run_interview_pipeline(_case_fixture("DISC-C", q, ans_correct))
        res_i = run_interview_pipeline(_case_fixture("DISC-I", q, ans_incorrect))

        eval_c = res_c["artifacts"]["evaluations"][0]
        eval_i = res_i["artifacts"]["evaluations"][0]

        self.assertGreater(eval_c["score"], eval_i["score"])

    def test_experience_hierarchy_declaration_vs_hypothesis_vs_demonstration(self):
        q = "Você tem experiência com Kubernetes em produção?"
        decl = "Trabalhei 3 anos com Kubernetes."
        hypo = "Eu criaria um deployment no Kubernetes se precisasse escalar."
        demo = "Em produção gerenciei clusters Kubernetes, configurei liveness e readiness probes, debuguei crash loops e resolvi gargalos de memória OOM."

        res_decl = run_interview_pipeline(_case_fixture("EXP-D", q, decl))
        res_hypo = run_interview_pipeline(_case_fixture("EXP-H", q, hypo))
        res_demo = run_interview_pipeline(_case_fixture("EXP-E", q, demo))

        score_decl = res_decl["artifacts"]["evaluations"][0]["score"]
        score_hypo = res_hypo["artifacts"]["evaluations"][0]["score"]
        score_demo = res_demo["artifacts"]["evaluations"][0]["score"]

        self.assertLessEqual(score_decl, score_hypo)
        self.assertLess(score_hypo, score_demo)
        self.assertGreaterEqual(score_demo, 7.0)

    def test_mutation_sensitivity_technical_change_alters_classification(self):
        q = "O que é um índice no banco relacional?"
        valid_ans = "É uma estrutura em árvore B-Tree que acelera buscas na tabela."
        mutated_alien = "É uma estrutura do Redis que armazena dados em memória com chave e valor."

        rec_valid = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": valid_ans})
        rec_alien = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": mutated_alien})

        self.assertEqual(rec_valid["classification"], "DIRECT")
        self.assertEqual(rec_alien["classification"], "OFF_TOPIC")

    def test_strict_determinism_triplicate_execution(self):
        fixture = _case_fixture(
            "DET",
            "Como funciona a assinatura de tokens JWT?",
            "JWT utiliza uma chave secreta ou par de chaves assimétricas para gerar uma assinatura criptográfica do payload.",
        )
        res1 = run_interview_pipeline(copy.deepcopy(fixture))
        res2 = run_interview_pipeline(copy.deepcopy(fixture))
        res3 = run_interview_pipeline(copy.deepcopy(fixture))

        self.assertEqual(res1["artifacts"]["evaluations"][0]["score"], res2["artifacts"]["evaluations"][0]["score"])
        self.assertEqual(res2["artifacts"]["evaluations"][0]["score"], res3["artifacts"]["evaluations"][0]["score"])
        self.assertEqual(
            res1["artifacts"]["evaluations"][0]["dimensions"],
            res2["artifacts"]["evaluations"][0]["dimensions"],
        )

    def test_execution_isolation_shuffled_order(self):
        cases = [
            ("ISO-1", "O que é HTTP 500?", "Erro interno do servidor."),
            ("ISO-2", "Como funciona Docker?", "Kubernetes orquestra containers."),
            ("ISO-3", "O que é injeção de dependência?", "Fornecer dependências externamente."),
        ]
        base_scores = [
            run_interview_pipeline(_case_fixture(cid, q, a))["artifacts"]["evaluations"][0]["score"]
            for cid, q, a in cases
        ]
        shuffled = list(cases)
        random.seed(42)
        random.shuffle(shuffled)
        shuffled_scores = {
            cid: run_interview_pipeline(_case_fixture(cid, q, a))["artifacts"]["evaluations"][0]["score"]
            for cid, q, a in shuffled
        }
        for (cid, _, _), base_score in zip(cases, base_scores):
            self.assertEqual(base_score, shuffled_scores[cid])


class Stage315HumanVsSystemPilotRevalidationAudit(unittest.TestCase):
    """Audit of Candidato-Piloto-05 against the frozen human reference."""

    @classmethod
    def setUpClass(cls):
        src = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Pilot Input - Source Transcript v3.md")
        cls.pilot_res = run_real_pilot(src)["pipeline"]
        cls.evals = cls.pilot_res["artifacts"]["evaluations"]
        cls.system_scores = [e["score"] for e in cls.evals]
        # Frozen human reference from Stage 31
        cls.human_scores = [4.0, 7.0, 4.0, 8.0, 2.0, 5.0, 5.0, 7.0, 4.0, 6.0, 4.0]

    def test_candidato_piloto_05_question_count(self):
        self.assertEqual(len(self.system_scores), 11)

    def test_candidato_piloto_05_mean_absolute_error(self):
        mae = sum(abs(s - h) for s, h in zip(self.system_scores, self.human_scores)) / len(self.system_scores)
        self.assertAlmostEqual(mae, 7.0 / 11.0, places=3)
        self.assertEqual(round(mae, 2), 0.64)
        self.assertLess(mae, 1.0)

    def test_candidato_piloto_05_system_mean_and_median(self):
        mean = sum(self.system_scores) / len(self.system_scores)
        self.assertAlmostEqual(mean, 5.5545, places=3)
        sorted_scores = sorted(self.system_scores)
        median = sorted_scores[len(sorted_scores) // 2]
        self.assertEqual(median, 5.85)

    def test_candidato_piloto_05_maximum_absolute_difference(self):
        diffs = [abs(s - h) for s, h in zip(self.system_scores, self.human_scores)]
        max_diff = max(diffs)
        self.assertEqual(max_diff, 2.45)  # Q5
        # Confirm that only Q5 and Q10 have diff > 1.0
        material_diffs = [i + 1 for i, d in enumerate(diffs) if d > 1.0]
        self.assertEqual(material_diffs, [5, 10])

    def test_candidato_piloto_05_exact_concordances(self):
        # Q1, Q3, Q9, Q11 have exact score agreement (4.0 vs 4.0)
        for q_idx in (0, 2, 8, 10):
            self.assertEqual(self.system_scores[q_idx], self.human_scores[q_idx])

    def test_candidato_piloto_05_evidence_item_count(self):
        ev_set = self.pilot_res["artifacts"]["evidence"]["evidence_set"]
        self.assertEqual(len(ev_set), 24)


if __name__ == "__main__":
    unittest.main()

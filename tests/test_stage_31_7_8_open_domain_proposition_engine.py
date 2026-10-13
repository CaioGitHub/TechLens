"""
Stage 31.7.8 — Test Suite for Open-Domain Proposition & Semantic Relation Architecture

Verifies that the OpenDomainPropositionEngine:
1. Operates without requiring lexical overlap (zero-lexical).
2. Handles novel/unseen entities and open-domain fictional technologies.
3. Distinguishes entity roles (central target vs incidental vs alien context).
4. Evaluates question intent (definitions, comparisons, causal problems, diagnostics).
5. Tracks multi-aspect demand coverage and epistemics.
6. Is deterministic, catalog-independent, and robust under semantic mutations.
"""

import unittest
from reference_runtime.runtime import (
    OpenDomainPropositionEngine,
    evaluate_open_domain_semantic_relevance,
    compare_semantic_engines,
    QuestionIntent,
    QuestionDemand,
    TechnicalProposition,
    SemanticRelation,
    AspectCoverage,
    EpistemicEvaluation,
)


class Stage3178OpenDomainPropositionEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    # =========================================================================
    # Grupo A — Unseen Entities & Open-Domain Fictional Technologies
    # =========================================================================
    def test_group_a_unseen_technologies_direct(self):
        """
        Property: Recognizes functional relevance for uncatalogued technologies (real or invented).
        """
        cases = [
            (
                "group_a_01",
                "Como funciona o Dragonfly para cache em memória?",
                "O Dragonfly processa requisições com arquitetura shared-nothing para alto throughput e baixa latência.",
                "DIRECT",
                "Uncatalogued modern cache engine explained with architectural mechanism."
            ),
            (
                "group_a_02",
                "Como o ClickHouse otimiza consultas analíticas?",
                "O ClickHouse armazena dados em formato colunar e usa vetorização SIMD para varrer bilhões de linhas.",
                "DIRECT",
                "Uncatalogued columnar DBMS explained via column storage and vectorization."
            ),
            (
                "group_a_03",
                "Como o TiKV garante consistência distribuída em transações?",
                "O TiKV utiliza o protocolo Raft para replicação de log e consenso entre nós.",
                "DIRECT",
                "Uncatalogued distributed KV store explained via Raft consensus."
            ),
            (
                "group_a_04",
                "Como o TechNova-X gerencia estado volátil em alta escala?",
                "O TechNova-X particiona as partições em shards distribuídos com checkpoint assíncrono em disco.",
                "DIRECT",
                "Fictional technology evaluated via functional partitioning and checkpointing proposition."
            ),
            (
                "group_a_05",
                "Como o DataMesh-Z sincroniza réplicas entre data centers?",
                "Ele utiliza replicação em topologia multi-master com detecção de conflitos por vetor de clocks.",
                "DIRECT",
                "Fictional technology replication mechanism functionally satisfies synchronization question."
            ),
        ]
        for cid, q, r, expected, rationale in cases:
            res = evaluate_open_domain_semantic_relevance(q, r)
            self.assertEqual(
                res["classification"],
                expected,
                f"Failed case {cid} ({rationale}): got {res['classification']}, expected {expected}"
            )

    # =========================================================================
    # Grupo B — Zero Lexical Overlap
    # =========================================================================
    def test_group_b_zero_lexical_overlap(self):
        """
        Property: Identifies functional relation without any shared keywords or stems.
        """
        cases = [
            (
                "group_b_01",
                "Como evitar que duas atualizações concorrentes sobrescrevam uma à outra?",
                "Comparo a versão lida com a versão atual no momento de persistir e descarto se houver divergência.",
                "DIRECT",
                "Classic optimistic concurrency control expressed without mentioning 'concorrência' or 'sobrescrever'."
            ),
            (
                "group_b_02",
                "Como lidar com consumo excessivo de memória sob alta carga?",
                "Descarto dados da memória cache usando eviction LRU para liberar espaço para requisições prioritárias.",
                "DIRECT",
                "Memory pressure mitigation expressed via eviction without repeating question words."
            ),
            (
                "group_b_03",
                "Como mitigar picos de latência causados por requisições simultâneas reconstruindo o mesmo valor ausente?",
                "Uso um mutex distribuído para que somente uma thread calcule o dado enquanto as outras aguardam o resultado.",
                "DIRECT",
                "Thundering herd mitigation without using the term 'thundering herd'."
            ),
        ]
        for cid, q, r, expected, rationale in cases:
            res = evaluate_open_domain_semantic_relevance(q, r)
            self.assertEqual(
                res["classification"],
                expected,
                f"Failed case {cid} ({rationale}): got {res['classification']}, expected {expected}"
            )
            # Verify zero / near-zero lexical overlap assertion
            q_words = set(q.lower().split())
            r_words = set(r.lower().split())
            meaningful_common = {w for w in q_words.intersection(r_words) if len(w) > 4}
            self.assertLessEqual(
                len(meaningful_common), 1,
                f"Case {cid} was supposed to test zero-lexical overlap, but shared: {meaningful_common}"
            )

    # =========================================================================
    # Grupo C — Formal vs Colloquial Invariance (Representation Invariance)
    # =========================================================================
    def test_group_c_representation_invariance(self):
        """
        Property: The system yields the same functional classification regardless of whether
        the candidate uses formal English jargon or colloquial plain Portuguese.
        """
        question = "Como garantir consistência em uma sequência de operações distribuídas quando uma etapa intermediária falha?"
        formal_response = "Implementamos o pattern Saga com compensating transactions para reverter as mutações anteriores."
        colloquial_response = "Se der erro no meio do caminho, executo uma rotina que desfaz e cancela tudo que já tinha sido gravado antes."

        res_formal = evaluate_open_domain_semantic_relevance(question, formal_response)
        res_colloquial = evaluate_open_domain_semantic_relevance(question, colloquial_response)

        self.assertEqual(res_formal["classification"], "DIRECT")
        self.assertEqual(res_colloquial["classification"], "DIRECT")
        self.assertEqual(
            res_formal["classification"],
            res_colloquial["classification"],
            "Representation invariance violated between formal and colloquial explanations"
        )

    # =========================================================================
    # Grupo D — Entity Roles: Target vs Context vs Incidental vs Alien
    # =========================================================================
    def test_group_d_entity_roles(self):
        """
        Property: Presence of an entity does not dictate relevance; the entity's functional
        role (target, context, incidental, alien) governs the semantic classification.
        """
        # Case D1: Kubernetes as central target
        q_target = "Como funciona o Kubernetes?"
        r_target = "O Kubernetes é um orquestrador que substitui gradualmente os pods durante o rolling update."
        res_target = evaluate_open_domain_semantic_relevance(q_target, r_target)
        self.assertEqual(res_target["classification"], "DIRECT")

        # Case D2: Kubernetes as incidental context in a concurrency question
        q_conc = "Como resolver concorrência de escritas no banco de dados?"
        r_incidental = "No meu projeto com Kubernetes, usei optimistic locking com versionamento de registro no banco."
        res_incidental = evaluate_open_domain_semantic_relevance(q_conc, r_incidental)
        self.assertEqual(res_incidental["classification"], "DIRECT")

        # Case D3: Entity present only as background experience declaration without answering
        q_arch = "Como funciona a arquitetura interna do Docker?"
        r_decl = "Eu utilizo Docker e Kubernetes diariamente na minha empresa."
        res_decl = evaluate_open_domain_semantic_relevance(q_arch, r_decl)
        self.assertIn(res_decl["classification"], ["RELATED", "SUPPORTING"])
        self.assertNotEqual(res_decl["classification"], "DIRECT")

        # Case D4: Alien domain containing the entity name incidentally
        q_alien = "Como funciona o Kubernetes?"
        r_alien = "Eu gosto de cozinhar lasanha de berinjela enquanto assisto vídeos sobre Kubernetes no YouTube."
        res_alien = evaluate_open_domain_semantic_relevance(q_alien, r_alien)
        self.assertEqual(res_alien["classification"], "OFF_TOPIC")

    # =========================================================================
    # Grupo E — Definitions
    # =========================================================================
    def test_group_e_definitional_questions(self):
        """
        Property: Evaluates definition questions by checking if response explains nature/mechanism.
        """
        q = "O que é Circuit Breaker?"
        r = "É um padrão de resiliência que monitora falhas consecutivas e abre o circuito temporariamente para evitar sobrecarga."
        res = evaluate_open_domain_semantic_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertEqual(res["question_intent"]["type"], "definition")

    # =========================================================================
    # Grupo F — Comparisons
    # =========================================================================
    def test_group_f_comparative_questions(self):
        """
        Property: Compares two subjects and recognizes contrasting propositions.
        """
        q = "Qual a diferença entre SQL e NoSQL em relação à escalabilidade?"
        r = "Bancos SQL escalam predominantemente de forma vertical enquanto bancos NoSQL escalam horizontalmente por particionamento de nós."
        res = evaluate_open_domain_semantic_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertEqual(res["question_intent"]["type"], "comparison")

    # =========================================================================
    # Grupo G — Causal Problems & Mitigations
    # =========================================================================
    def test_group_g_causal_problem_and_mitigation(self):
        """
        Property: Matches a diagnostic/performance problem to a technical mitigation proposition.
        """
        q = "Como resolver contenção de locks em tabelas transacionais com alta taxa de escrita?"
        r = "Reduzo o escopo das transações, utilizo locks otimistas e particiono as tabelas para diminuir o conflito de linhas."
        res = evaluate_open_domain_semantic_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertIn(res["question_intent"]["type"], ["diagnosis", "implementation"])

    # =========================================================================
    # Grupo H — Diagnostics: Symptom to Investigation
    # =========================================================================
    def test_group_h_diagnostics_symptom_to_investigation(self):
        """
        Property: Links high-level symptoms to investigative procedures and diagnostic metrics.
        """
        q = "Como você investigaria picos repentinos de latência na aplicação?"
        r = "Eu analisaria os tempos de pausa no garbage collector nos logs e verificaria traces de chamadas lentas ao banco."
        res = evaluate_open_domain_semantic_relevance(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        self.assertEqual(res["question_intent"]["type"], "diagnosis")

    # =========================================================================
    # Grupo I — Multi-Aspect Demand Coverage
    # =========================================================================
    def test_group_i_multi_aspect_coverage(self):
        """
        Property: Tracks atomic demand coverage and marks PARTIAL when only a subset of demands is met.
        """
        q = "Explique retries com exponential backoff e como a idempotência protege contra duplicidade."
        
        # Complete coverage
        r_complete = "O retry tenta novamente com intervalos crescentes (backoff) e a chave de idempotência assegura que requisições repetidas não causem efeitos colaterais duplicados."
        res_complete = evaluate_open_domain_semantic_relevance(q, r_complete)
        self.assertEqual(res_complete["classification"], "DIRECT")
        self.assertGreaterEqual(res_complete["aspect_coverage"]["ratio"], 0.75)

        # Partial coverage (covers retry and backoff, ignores idempotency)
        r_partial = "Quando dá erro, a gente tenta de novo aumentando o tempo de espera entre cada tentativa."
        res_partial = evaluate_open_domain_semantic_relevance(q, r_partial)
        self.assertEqual(res_partial["classification"], "PARTIAL")
        self.assertLess(res_partial["aspect_coverage"]["ratio"], 0.75)

    # =========================================================================
    # Grupo J — Epistemic Status
    # =========================================================================
    def test_group_j_epistemic_status_distinction(self):
        """
        Property: Separates demonstrated technical explanation from mere declaration or hypothesis.
        """
        q = "Como você implementaria particionamento em banco de dados relacional?"

        # Demonstrated mechanism
        r_demo = "Criei partições por range de data no PostgreSQL e configurei triggers para roteamento automático de inserções."
        res_demo = evaluate_open_domain_semantic_relevance(q, r_demo)
        self.assertEqual(res_demo["epistemic_status"]["status"], "DEMONSTRATED_EXPERIENCE")

        # Mere declaration
        r_decl = "Eu tenho 8 anos de experiência em bancos de dados relacionais e particionamento."
        res_decl = evaluate_open_domain_semantic_relevance(q, r_decl)
        self.assertEqual(res_decl["epistemic_status"]["status"], "DECLARATION")

        # Hypothesis
        r_hypo = "Acho que talvez dê para criar alguma regra de divisão ou quem sabe usar tabelas separadas."
        res_hypo = evaluate_open_domain_semantic_relevance(q, r_hypo)
        self.assertEqual(res_hypo["epistemic_status"]["status"], "HYPOTHESIS")

    # =========================================================================
    # Grupo K — UNKNOWN / Ambiguous Cases
    # =========================================================================
    def test_group_k_unknown_ambiguous_cases(self):
        """
        Property: Expresses genuine uncertainty or insufficient evidence as UNKNOWN or INSUFFICIENT.
        """
        q = "Como configurar tolerância a falhas na camada de mensageria?"
        r_vague = "Depende bastante de como você resolver estruturar as coisas."
        res = evaluate_open_domain_semantic_relevance(q, r_vague)
        self.assertIn(res["classification"], ["UNKNOWN", "INSUFFICIENT", "RELATED"])

    # =========================================================================
    # Grupo L — Semantic Mutations (Sensitivity & Robustness)
    # =========================================================================
    def test_group_l_semantic_mutations(self):
        """
        Property: Subtle semantic changes (e.g. flipping the mechanism or diverting to an alien domain)
        correctly alter the semantic classification.
        """
        q = "Como evitar problemas de concorrência ao atualizar um saldo compartilhado?"
        
        # Valid mitigation
        r_valid = "Utilizo bloqueio pessimista ou controle otimista com versionamento para impedir atualizações concorrentes sujas."
        res_valid = evaluate_open_domain_semantic_relevance(q, r_valid)
        self.assertEqual(res_valid["classification"], "DIRECT")

        # Opposite/harmful mechanism mutation
        r_mutated_opposite = "Para resolver isso, removo todas as travas e deixo todas as threads escreverem livremente sem validação de versão."
        res_opposite = evaluate_open_domain_semantic_relevance(q, r_mutated_opposite)
        # Under Stage 31.7.19 CR-04 contract, destructive antithesis is OFF_TOPIC (or contrasting)
        self.assertIn(res_opposite["classification"], ["OFF_TOPIC", "RELATED", "SUPPORTING"])

        # Alien domain mutation with same surface words
        r_mutated_alien = "Eu verifico o saldo da minha conta bancária pessoal no celular antes de sair para o almoço com meus colegas."
        res_alien = evaluate_open_domain_semantic_relevance(q, r_mutated_alien)
        self.assertEqual(res_alien["classification"], "OFF_TOPIC")

    # =========================================================================
    # Non-Co-Designed Independent Cases
    # =========================================================================
    def test_independent_unseen_cases(self):
        """
        Property: Evaluates diverse independent problems never seen in previous test suites.
        """
        cases = [
            (
                "indep_01",
                "Como prevenir deadlocks em sistemas com múltiplos recursos compartilhados?",
                "Adoto uma ordem global estrita de aquisição de locks em todos os componentes.",
                "DIRECT"
            ),
            (
                "indep_02",
                "O que é gossip protocol em sistemas distribuídos?",
                "É um protocolo de disseminação de informações peer-to-peer onde nós trocam estado periodicamente com vizinhos aleatórios.",
                "DIRECT"
            ),
            (
                "indep_03",
                "Qual a função de um dead letter queue (DLQ)?",
                "Armazenar mensagens que falharam repetidamente no processamento para análise e isolamento posterior.",
                "DIRECT"
            ),
        ]
        for cid, q, r, expected in cases:
            res = evaluate_open_domain_semantic_relevance(q, r)
            self.assertEqual(res["classification"], expected, f"Failed independent case {cid}")

    # =========================================================================
    # Determinism
    # =========================================================================
    def test_engine_determinism(self):
        """
        Property: Evaluates the same question/response 20 times to guarantee strict determinism.
        """
        q = "Como o Redpanda processa streaming em tempo real?"
        r = "O Redpanda executa arquitetura thread-per-core sem JVM, consumindo a API do Kafka diretamente em C++."
        first_res = evaluate_open_domain_semantic_relevance(q, r)
        for i in range(20):
            cur_res = evaluate_open_domain_semantic_relevance(q, r)
            self.assertEqual(
                first_res["classification"],
                cur_res["classification"],
                f"Determinism failure at run {i}"
            )
            self.assertEqual(
                first_res["aspect_coverage"]["ratio"],
                cur_res["aspect_coverage"]["ratio"],
                f"Determinism ratio failure at run {i}"
            )

    # =========================================================================
    # Catalog Independence
    # =========================================================================
    def test_catalog_independence(self):
        """
        Property: Engine operates identically without referencing any technology catalog.
        """
        q = "Como mitigar gargalos de I/O em banco de dados colunar?"
        r = "Uso compressão de blocos e índices esparsos para minimizar a quantidade de dados lidos do disco."
        res = self.engine.evaluate(q, r)
        self.assertEqual(res["classification"], "DIRECT")
        # Ensure no catalog lookup is used in rationales
        self.assertNotIn("catalog", res["rationale"].lower())

    # =========================================================================
    # Diagnostic Comparison Engine (Legacy vs New)
    # =========================================================================
    def test_compare_semantic_engines(self):
        """
        Property: compare_semantic_engines outputs both legacy and new evaluations side by side
        without altering the legacy output.
        """
        q = "Como resolver concorrência de atualizações sem locks?"
        r = "Comparo a versão antes de gravar e rejeito se desatualizado."
        comp = compare_semantic_engines(q, r)
        self.assertIn("legacy", comp)
        self.assertIn("open_domain", comp)
        self.assertIn("is_concordant", comp)
        self.assertEqual(comp["open_domain"]["classification"], "DIRECT")


if __name__ == "__main__":
    unittest.main()

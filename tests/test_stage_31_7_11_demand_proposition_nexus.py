"""
Stage 31.7.11 — Contract and Architectural Test Suite for Demand-Proposition Nexus Architecture

Verifies that the Demand-Proposition Nexus Engine (Stage 31.7.11):
A. Direct Satisfaction (FUNCTIONALLY_SOLVES -> DIRECT) without lexical overlap
B. False Positive Prevention (Rejects long irrelevant text, buzzwords, entity trivia, non-operative text)
C. Supporting vs Related (Auxiliary observability -> SUPPORTING vs Ecosystem mention -> RELATED)
D. Multi-Aspect Questions (Tracks atomic demands, requires essential coverage, flags PARTIAL on omissions)
E. Polarity and Context (Opposed destructive actions -> ANTITHESIS_OPPOSED / OFF_TOPIC)
F. Epistemic Assessment (Decoupled epistemics: DECLARATION, HYPOTHESIS, CONCEPTUAL, UNCERTAINTY)
G. Representation Invariance (Invariance under length, formality, paraphrase, novel/fictional technologies)
H. Inference Limits (Preserves UNKNOWN and INSUFFICIENT without forcing spurious DIRECT or OFF_TOPIC)
"""

import unittest
from reference_runtime.runtime import (
    OpenDomainPropositionEngine,
    evaluate_open_domain_semantic_relevance,
    compare_semantic_engines,
    QuestionDemand,
    QuestionIntent,
    TechnicalProposition,
    DemandPropositionNexus,
    EpistemicEvaluation,
)


class Stage31711DemandPropositionNexusTests(unittest.TestCase):
    def setUp(self):
        self.engine = OpenDomainPropositionEngine()

    # =========================================================================
    # Categoria A — Atendimento Direto (Zero-Lexical & Operative Mechanism)
    # =========================================================================
    def test_category_a_direct_functional_satisfaction(self):
        """
        Property: A technically correct, functionally operative mechanism directly solves
        the question demand even with zero or minimal lexical overlap.
        """
        cases = [
            (
                "cat_a_01",
                "Como funciona o TiKV para garantir consistência distribuída em transações?",
                "O TiKV utiliza o protocolo Raft para replicação de log e consenso entre nós.",
                "DIRECT"
            ),
            (
                "cat_a_02",
                "Como o ClickHouse otimiza consultas analíticas massivas?",
                "O ClickHouse armazena dados em formato colunar e usa vetorização SIMD para varrer bilhões de linhas.",
                "DIRECT"
            ),
            (
                "cat_a_03",
                "Como o Dragonfly entrega throughput superior a outros caches em memória?",
                "O Dragonfly processa requisições com arquitetura shared-nothing para alto throughput e baixa latência.",
                "DIRECT"
            ),
            (
                "cat_a_04_zero_lexical",
                "Como resolver contenção de concorrência em tabelas de saldo com frequentes gravações?",
                "Utilizo bloqueio pessimista ou controle otimista com versionamento para impedir atualizações simultâneas sujas.",
                "DIRECT"
            )
        ]
        for cid, q, r, expected in cases:
            res = evaluate_open_domain_semantic_relevance(q, r)
            self.assertEqual(res["classification"], expected, f"Failed on case {cid}")
            self.assertTrue(res["functional_contribution"])
            self.assertGreaterEqual(res["aspect_coverage"]["ratio"], 0.75)

    # =========================================================================
    # Categoria B — Falsos Positivos (Word Length, Buzzwords, Disjunct Domains)
    # =========================================================================
    def test_category_b_false_positive_rejection(self):
        """
        Property: Long responses, technical buzzword soup, entity trivia, or operative propositions
        addressing an orthogonal domain MUST NOT be promoted to DIRECT.
        """
        cases = [
            (
                "cat_b_01_buzzwords",
                "Como mitigar race conditions em saldo compartilhado?",
                "Utilizamos Kubernetes com Istio e pods escaláveis com alta resiliência e esteira de microsserviços modernos na nuvem.",
                "OFF_TOPIC"
            ),
            (
                "cat_b_02_alien_cooking",
                "Como evitar problemas de concorrência ao atualizar um saldo compartilhado?",
                "Eu verifico o saldo da minha conta bancária pessoal no celular antes de sair para o almoço com meus colegas.",
                "OFF_TOPIC"
            ),
            (
                "cat_b_03_frontend_disjunct",
                "Como evitar problemas de concorrência ao atualizar um saldo compartilhado em banco de dados?",
                "Uso CSS Grid e media queries para centralizar os elementos do layout e garantir design responsivo em telas widescreen.",
                "OFF_TOPIC"
            ),
            (
                "cat_b_04_devops_disjunct",
                "Como otimizar consultas analíticas lentas em banco de dados relacional?",
                "Implementamos pipelines de CI CD no GitLab com testes automatizados no Selenium e sprints ágeis no Jira.",
                "OFF_TOPIC"
            ),
            (
                "cat_b_05_tautological_trivia",
                "Como funciona o Kubernetes para orquestração de containers?",
                "O Kubernetes é um orquestrador de pods muito robusto que gerencia containers em clusters grandes com muita facilidade.",
                "RELATED"
            )
        ]
        for cid, q, r, expected in cases:
            res = evaluate_open_domain_semantic_relevance(q, r)
            self.assertNotEqual(res["classification"], "DIRECT", f"Case {cid} falsely promoted to DIRECT")
            self.assertEqual(res["classification"], expected, f"Case {cid} expected {expected} but got {res['classification']}")

    # =========================================================================
    # Categoria C — Supporting vs Related (Auxiliary Observability vs Ecosystem)
    # =========================================================================
    def test_category_c_supporting_versus_related(self):
        """
        Property: Observability tools providing auxiliary diagnostic evidence receive SUPPORTING.
        Mentioning ecosystem tools without functional mechanism receives RELATED.
        """
        # Auxiliary observability: contributes to diagnosis/investigation but does not fix root cause
        q_aux = "Como você investigaria e conteria picos anômalos de latência na aplicação?"
        r_aux = "Adiciono métricas no Prometheus e crio alertas no Grafana para monitorar quanto tempo cada requisição demora."
        res_aux = evaluate_open_domain_semantic_relevance(q_aux, r_aux)
        self.assertEqual(res_aux["classification"], "SUPPORTING")
        self.assertTrue(res_aux["functional_contribution"])
        self.assertEqual(res_aux["relation_type"], "auxiliary_observability_support")

        # Mere technology mention without mechanism
        q_rel = "Como o Kafka gerencia ordenação de eventos?"
        r_rel = "O Kafka é uma ferramenta open source muito boa desenvolvida por ex engenheiros da Apache."
        res_rel = evaluate_open_domain_semantic_relevance(q_rel, r_rel)
        self.assertEqual(res_rel["classification"], "RELATED")
        self.assertFalse(res_rel["functional_contribution"])

    # =========================================================================
    # Categoria D — Perguntas Multi-Aspecto (Coverage Tracking & Partial)
    # =========================================================================
    def test_category_d_multi_aspect_coverage(self):
        """
        Property: Demands are decomposed atomically. Full satisfaction of all demands -> DIRECT.
        Omission of secondary or essential demands -> PARTIAL with coverage ratio.
        """
        q = "Explique retries com exponential backoff e como a idempotência protege contra duplicidade."

        # Case 1: Fully satisfied (both retries/backoff AND idempotency)
        r_full = "O retry tenta novamente com intervalos crescentes (backoff) e a chave de idempotência assegura que requisições repetidas não causem efeitos colaterais duplicados."
        res_full = evaluate_open_domain_semantic_relevance(q, r_full)
        self.assertEqual(res_full["classification"], "DIRECT")
        self.assertGreaterEqual(res_full["aspect_coverage"]["ratio"], 0.75)
        self.assertEqual(res_full["aspect_coverage"]["status"], "FULL")

        # Case 2: Partial satisfaction (retries/backoff covered, idempotency omitted)
        r_partial = "Quando dá erro, a gente tenta de novo aumentando o tempo de espera entre cada tentativa."
        res_partial = evaluate_open_domain_semantic_relevance(q, r_partial)
        self.assertEqual(res_partial["classification"], "PARTIAL")
        self.assertLess(res_partial["aspect_coverage"]["ratio"], 0.75)
        self.assertEqual(res_partial["aspect_coverage"]["status"], "PARTIAL")

    # =========================================================================
    # Categoria E — Polaridade e Contexto (Antithesis & Destructive Actions)
    # =========================================================================
    def test_category_e_polarity_and_antithesis(self):
        """
        Property: Proposing actions that disable essential operational safety mechanisms
        without diagnostic justification receives ANTITHESIS_OPPOSED / OFF_TOPIC.
        """
        q = "Como resolver concorrência de escritas e deadlocks em transações financeiras?"
        
        # Destructive antithesis: removing locks and ACID transactions entirely
        r_destructive = "Para resolver isso, desativo todos os locks do banco e desabilito transações ACID para escrever direto sem travar."
        res_destr = evaluate_open_domain_semantic_relevance(q, r_destructive)
        self.assertEqual(res_destr["classification"], "OFF_TOPIC")
        self.assertEqual(res_destr["relation_type"], "destructive_antithesis_assertion")
        self.assertFalse(res_destr["functional_contribution"])

    # =========================================================================
    # Categoria F — Incerteza e Evidência Epistemológica (Decoupled Epistemics)
    # =========================================================================
    def test_category_f_epistemic_assessment_decoupled(self):
        """
        Property: Epistemic status does not override technical relevance, but is tracked separately.
        """
        q = "Como você implementaria particionamento em banco de dados relacional?"

        # Demonstrated experience
        r_demo = "Criei partições por range de data no PostgreSQL e configurei triggers para roteamento automático de inserções."
        res_demo = evaluate_open_domain_semantic_relevance(q, r_demo)
        self.assertEqual(res_demo["epistemic_status"]["status"], "DEMONSTRATED_EXPERIENCE")
        self.assertTrue(res_demo["epistemic_status"]["is_demonstrated"])

        # Declaration of experience without demonstration
        r_decl = "Eu tenho 8 anos de experiência em bancos de dados relacionais e particionamento."
        res_decl = evaluate_open_domain_semantic_relevance(q, r_decl)
        self.assertEqual(res_decl["epistemic_status"]["status"], "DECLARATION")
        self.assertFalse(res_decl["epistemic_status"]["is_demonstrated"])
        self.assertEqual(res_decl["classification"], "RELATED")

        # Speculative hypothesis
        r_hypo = "Acho que talvez dê para criar alguma regra de divisão ou quem sabe usar tabelas separadas."
        res_hypo = evaluate_open_domain_semantic_relevance(q, r_hypo)
        self.assertEqual(res_hypo["epistemic_status"]["status"], "HYPOTHESIS")

    # =========================================================================
    # Categoria G — Invariância de Representação (Style, Length, Novel Entities)
    # =========================================================================
    def test_category_g_representation_invariance(self):
        """
        Property: Equivalent semantic propositions yield equivalent classification regardless
        of formality, wordiness, or novel/invented technology names.
        """
        q = "Como o Novastream lida com particionamento em cluster distribuído?"

        # Concise response with novel technology
        r_concise = "O Novastream particiona dados por consistent hashing com nós virtuais para rebalanceamento."
        res_concise = evaluate_open_domain_semantic_relevance(q, r_concise)
        self.assertEqual(res_concise["classification"], "DIRECT")

        # Informal / verbose paraphrase with novel technology
        r_verbose = "No Novastream, a gente distribui as chaves usando consistent hashing e nós virtuais pra rebalancear os nós sem sobrecarga."
        res_verbose = evaluate_open_domain_semantic_relevance(q, r_verbose)
        self.assertEqual(res_verbose["classification"], "DIRECT")

    # =========================================================================
    # Categoria H — Limites de Inferência (UNKNOWN & INSUFFICIENT Preserved)
    # =========================================================================
    def test_category_h_inference_limits_unknown_insufficient(self):
        """
        Property: Ambiguous, evasive, or bare conversational utterances preserve UNKNOWN or INSUFFICIENT
        without being artificially forced into DIRECT or OFF_TOPIC.
        """
        q = "Como configurar tolerância a falhas na camada de mensageria?"

        # Evasive answer
        r_evasive = "Depende de muitos fatores e de como a equipe resolver fazer."
        res_evasive = evaluate_open_domain_semantic_relevance(q, r_evasive)
        self.assertEqual(res_evasive["classification"], "UNKNOWN")

        # Explicit ignorance
        r_ign = "Não sei, nunca usei essa ferramenta."
        res_ign = evaluate_open_domain_semantic_relevance(q, r_ign)
        self.assertEqual(res_ign["classification"], "INSUFFICIENT")

        # Bare acknowledgement
        r_filler = "Sim, com certeza."
        res_filler = evaluate_open_domain_semantic_relevance(q, r_filler)
        self.assertEqual(res_filler["classification"], "INSUFFICIENT")


if __name__ == "__main__":
    unittest.main()

import re
from reference_runtime.runtime import (
    DemandSpecification,
    QuestionProfile,
    DiscourseProposition,
    DiscourseProfile,
    EpistemicUncertaintyRecord,
    _normalize_text,
)

class SemanticQuestionProfiler:
    """Increment 1: Question Profile and Epistemological Intent Engine."""
    def __init__(self):
        self.conjunctions = [
            (" e como ", " e como "), (" e quais ", " e quais "), (" e qual ", " e qual "),
            (" e de que forma ", " e de que forma "), (" e de que maneira ", " e de que maneira "),
            (" e por que ", " e por que "), (" e onde ", " e onde "), (" e quando ", " e quando "),
            (" e o que ", " e o que "), (", e como ", ", e como "), (", e quais ", ", e quais "),
            (", e de que forma ", ", e de que forma "), (", e de que maneira ", ", e de que maneira "),
            (", e garantir ", ", e "), (", e proteger ", ", e "), (", e lidar com ", ", e "),
            (", e mitigar ", ", e "), (" bem como ", " bem como "), (" alem de como ", " alem de como "),
            ("; como ", "; como "), ("? como ", "? como "), (", como ", ", como "),
            (" e armazena ", " e "), (" e armazenar ", " e "), (" e preserva ", " e "), (" e preservar ", " e "),
            (" e garante ", " e "), (" e garantir ", " e "), (" e rebalancear ", " e "), (" e rebalanceia ", " e "),
            (" e gerenciar ", " e "), (" e gerencia ", " e "), (" e manter ", " e "), (" e mantem ", " e "),
            (" e tratar ", " e "), (" e trata ", " e "), (" e sincronizar ", " e "), (" e sincroniza ", " e "),
            (" e mitigar ", " e "), (" e conter ", " e "), (" e isolar ", " e "), (" e jitter ", " e "),
            (" e vice-versa", " e vice-versa"), (" e vice versa", " e vice versa"),
            (" quanto a ", " quanto a "), (", e qual o impacto ", ", e qual o impacto "),
            (" e executa compensacoes", " e "), (" e lida com falhas", " e "),
            (" e lida com ", " e "), (" e executa ", " e "), (" e transita ", " e ")
        ]

    def profile_question(self, question_text: str) -> tuple[QuestionProfile, EpistemicUncertaintyRecord]:
        q_norm = _normalize_text(question_text)
        words = [w for w in question_text.replace("?", "").replace("!", "").replace(",", "").split()]
        
        # 1. Intent Mode Classification (11 canonical modes)
        if any(p in q_norm for p in ("qual a diferenca", "diferenca entre", "comparar", "versus", " vs ")):
            intent_mode = "COMPARISON"
        elif any(q_norm.startswith(p) or f" {p} " in f" {q_norm} " for p in ("o que e", "qual a definicao", "defina", "qual o conceito", "o que significa", "qual a funcao")):
            intent_mode = "DEFINITION"
        elif any(p in q_norm for p in ("como investigar", "como diagnosticar", "quais metricas", "como identificar", "onde analisar", "como analisar", "como voce investigaria")):
            intent_mode = "DIAGNOSIS"
        elif any(p in q_norm for p in ("quais os trade-offs", "quais sao os trade-offs", "vantagens e desvantagens", "pros e contras")):
            intent_mode = "TRADE_OFF_ANALYSIS"
        elif any(p in q_norm for p in ("por que escolher", "quando usar", "quando adotar", "qual a justificativa")):
            intent_mode = "DECISION_JUSTIFICATION"
        elif any(p in q_norm for p in ("por que", "qual a razao", "qual a causa", "o que leva a", "qual o motivo")):
            intent_mode = "CAUSALITY"
        elif any(p in q_norm for p in ("quem criou", "quando surgiu", "qual a origem", "qual o artigo de")):
            intent_mode = "HISTORICAL"
        elif any(p in q_norm for p in ("como evitar", "como resolver", "como mitigar", "como prevenir", "como solucionar", "como proteger", "como conter")):
            intent_mode = "PROBLEM_SOLUTION"
        elif any(p in q_norm for p in ("como implementar", "como configurar", "como construir", "como criar", "como voce implementaria")):
            intent_mode = "IMPLEMENTATION"
        elif any(p in q_norm for p in ("como funciona", "como opera", "como processa", "qual a arquitetura", "qual o protocolo", "de que maneira funciona", "como ele garante")):
            intent_mode = "MECHANISM"
        elif any(p in q_norm for p in ("explique", "discorra", "fale sobre", "como e o conceito")):
            intent_mode = "CONCEPTUAL_EXPLANATION"
        else:
            intent_mode = "CONCEPTUAL_EXPLANATION"

        # 2. Extract Entities and Context Qualifiers
        stopwords = {
            "como", "qual", "quais", "explique", "o", "a", "os", "as", "em", "para",
            "de", "do", "da", "dos", "das", "se", "no", "na", "nos", "nas", "por",
            "que", "um", "uma", "uns", "umas", "voce", "ele", "ela", "com"
        }
        target_entities = []
        for w in words:
            if w.istitle() and w.lower() not in stopwords and w not in target_entities:
                target_entities.append(w)
        
        # Recognized CS entities if not capitalized
        cs_terms = [
            "kafka", "processo", "thread", "deadlock", "postgres", "redis",
            "circuit breaker", "idempotencia", "inversao de dependencia", "b-tree",
            "btree", "paxos", "raft", "outbox", "saga", "sharding", "particionamento",
            "acid", "spring", "docker", "kubernetes", "rest", "graphql", "grpc"
        ]
        for term in cs_terms:
            if term in q_norm and not any(term.lower() in e.lower() for e in target_entities):
                target_entities.append(term)

        # Context qualifiers
        qualifiers = []
        for q_word in ("ordem de entrega", "alta concorrencia", "producao", "falhas", "distribuido", "transacional", "consistencia", "latencia"):
            if q_word in q_norm:
                qualifiers.append(q_word)

        # 3. Demands Decomposition (Primary & Secondary)
        secondary_demands = []
        has_split = False
        primary_clause = q_norm
        for pattern, split_on in self.conjunctions:
            if pattern in q_norm:
                parts = q_norm.split(split_on, 1)
                primary_clause = parts[0].strip()
                secondary_clause = parts[1].strip()
                has_split = True
                secondary_demands.append(DemandSpecification(
                    demand_id="demand_2",
                    description=secondary_clause,
                    is_mandatory=True
                ))
                break

        primary_demand = DemandSpecification(
            demand_id="demand_1",
            description=primary_clause,
            is_mandatory=True
        )

        # 4. Epistemic Uncertainty
        is_short = len(words) <= 2
        is_ambiguous = ("varia conforme" in q_norm or is_short)
        confidence = "LOW" if is_short else ("MEDIUM" if is_ambiguous else "HIGH")
        limitations = []
        if is_short:
            limitations.append("Pergunta com poucas palavras; contexto sintético reduzido")
        if not target_entities:
            limitations.append("Nenhuma entidade técnica explícita identificada")

        uncertainty = EpistemicUncertaintyRecord(
            confidence_level=confidence,
            unresolved_ambiguities_present=is_ambiguous,
            epistemic_limitations=limitations
        )

        profile = QuestionProfile(
            raw_question=question_text,
            primary_demand=primary_demand,
            intent_mode=intent_mode,
            secondary_demands=secondary_demands,
            target_entities=target_entities,
            context_qualifiers=qualifiers
        )

        return profile, uncertainty


class DiscoursePropositionEngine:
    """Increment 1: Discourse Proposition and Preamble Isolation Engine."""
    def __init__(self):
        # Conversational preamble markers (commute, weather, greetings, personal anecdotes)
        self.preamble_markers = [
            "hoje peguei muito transito", "hoje peguei um transito terrivel", "hoje peguei transito",
            "o transito estava terrivel", "o transito estava infernal", "o transito estava um caos",
            "essa e uma otima pergunta", "essa e uma excelente pergunta", "otima pergunta", "boa pergunta",
            "obrigado pela oportunidade", "bom dia a todos", "boa tarde a todos", "ola pessoal",
            "quando eu comecei minha carreira la em", "quando eu era estagiario la em",
            "olha, para comecar", "para ser bem sincero com voce"
        ]
        self.retraction_markers = [
            "na verdade nao", "na verdade,", "ou melhor,", "ou melhor", "corrigindo,",
            "corrigindo", "quis dizer", "me confundi,", "me confundi"
        ]

    def extract_discourse_profile(self, response_text: str, question_profile: QuestionProfile | None = None) -> DiscourseProfile:
        r_norm = _normalize_text(response_text)
        
        # 1. Preamble Isolation
        isolated_preambles = []
        remaining_text = response_text
        for m in self.preamble_markers:
            if m in r_norm:
                # Find matching span in raw text or split
                idx = r_norm.find(m)
                # Find sentence boundary after preamble marker
                boundary = r_norm.find(".", idx)
                if boundary != -1:
                    preamble_sub = response_text[:boundary+1].strip()
                    isolated_preambles.append(preamble_sub)
                    remaining_text = response_text[boundary+1:].strip()
                else:
                    comma_bound = r_norm.find(",", idx + len(m))
                    if comma_bound != -1 and comma_bound - idx < 60:
                        preamble_sub = response_text[:comma_bound+1].strip()
                        isolated_preambles.append(preamble_sub)
                        remaining_text = response_text[comma_bound+1:].strip()
                break

        # 2. Proposition Decomposition
        # Split remaining text by sentence or semicolon
        raw_sentences = [s.strip() for s in re.split(r'[.;\n]+', remaining_text) if s.strip()]
        if not raw_sentences and remaining_text:
            raw_sentences = [remaining_text]
        if not raw_sentences and isolated_preambles:
            raw_sentences = [isolated_preambles[0]] # fallback if response was only preamble

        propositions: list[DiscourseProposition] = []
        for i, s in enumerate(raw_sentences, 1):
            s_norm = _normalize_text(s)
            prop_id = f"prop_{i}"

            # Negation detection
            neg_match = re.search(r'\b(nao|nunca|jamais|sem|nao devemos|nao se deve|evitar)\s+([^,.;]{3,40})', s_norm)
            is_negated = bool(neg_match)
            negation_scope = neg_match.group(2).strip() if neg_match else ""

            # Conditional detection
            cond_match = re.search(r'\b(se|caso|desde que|a nao ser que|contanto que|dependendo de|conforme)\s+([^,.;]{3,40})', s_norm)
            is_conditional = bool(cond_match)
            condition_premise = cond_match.group(2).strip() if cond_match else ""

            # Discourse role
            if any(rm in s_norm for rm in self.retraction_markers):
                discourse_role = "RETRACTED_ASSERTION"
            elif any(t in s_norm for t in ("edgar codd", "linus torvalds", "artigo de 1970", "criado por")):
                discourse_role = "HISTORICAL_METADATA"
            elif any(t in s_norm for t in ("prometheus", "grafana", "datadog", "metricas no prometheus", "sentry")):
                discourse_role = "OBSERVABILITY_SUPPORT"
            elif any(t in s_norm for t in ("nao sei", "desconheco", "nunca trabalhei com", "nao me recordo")):
                discourse_role = "IGNORANCE_DECLARATION"
            elif len(s.split()) <= 3 and any(t in s_norm for t in ("sim", "ok", "conheco", "com certeza")):
                discourse_role = "EMPTY_FILLER"
            else:
                discourse_role = "TECHNICAL_CORE"

            propositions.append(DiscourseProposition(
                prop_id=prop_id,
                text=s,
                discourse_role=discourse_role,
                is_negated=is_negated,
                negation_scope=negation_scope,
                is_conditional=is_conditional,
                condition_premise=condition_premise
            ))

        # Check self-correction / retraction retroactively (SC-21)
        for i in range(1, len(propositions)):
            curr_text = _normalize_text(propositions[i].text)
            if any(rm in curr_text for rm in ("na verdade nao", "ou melhor", "corrigindo", "quis dizer")):
                # The PREVIOUS proposition contained the retracted assertion!
                propositions[i-1].discourse_role = "RETRACTED_ASSERTION"

        return DiscourseProfile(
            raw_response=response_text,
            propositions=propositions,
            isolated_preambles=isolated_preambles
        )

# Quick demonstration
profiler = SemanticQuestionProfiler()
engine = DiscoursePropositionEngine()

# Test 1: Compound Question
q1 = "Como o particionamento no Kafka funciona e como ele garante a ordem de entrega?"
qp1, unc1 = profiler.profile_question(q1)
print("Test 1 - Intent Mode:", qp1.intent_mode)
print("Test 1 - Primary Demand:", qp1.primary_demand)
print("Test 1 - Secondary Demands:", qp1.secondary_demands)
print("Test 1 - Target Entities:", qp1.target_entities)
print("Test 1 - Qualifiers:", qp1.context_qualifiers)

# Test 2: Preamble Isolation & Negation
r2 = "Hoje peguei muito transito na volta do trabalho. Mas no Kafka, nos particionamos as mensagens por chave e nao usamos lock pessimista para evitar deadlock."
dp2 = engine.extract_discourse_profile(r2, qp1)
print("\nTest 2 - Isolated Preambles:", dp2.isolated_preambles)
print("Test 2 - Propositions Count:", len(dp2.propositions))
for p in dp2.propositions:
    print(f"  {p.prop_id}: role={p.discourse_role}, is_negated={p.is_negated}, scope='{p.negation_scope}', text='{p.text}'")

# Test 3: Retraction (SC-21)
r3 = "Usamos lock exclusivo em tudo. Na verdade nao, utilizamos optimistic locking com versao para nao bloquear as transacoes."
dp3 = engine.extract_discourse_profile(r3, qp1)
print("\nTest 3 - Self Correction:")
for p in dp3.propositions:
    print(f"  {p.prop_id}: role={p.discourse_role}, text='{p.text}'")

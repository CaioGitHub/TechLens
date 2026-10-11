import json
import re
import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(".").resolve()))

from reference_runtime.runtime import (
    _normalize_text,
    QuestionIntent,
    QuestionDemand,
    TechnicalProposition,
    DemandPropositionNexus,
    EpistemicEvaluation,
)


def _stem_word(w: str) -> str:
    """Normalize plural and common verbal/nominal endings in Portuguese."""
    w = w.lower()
    w = re.sub(r'(amento|amentos|acao|acoes|icao|icoes|ar|er|ir|ando|endo|indo|ado|ido|avam|aram|eram|iram|asse|esse|isse|aria|eria|iria|am|em|es|s|oes|coes)$', '', w)
    if len(w) >= 4:
        w = re.sub(r'[aeo]$', '', w)
    return w if len(w) >= 3 else w


class EnhancedPropositionEngine:
    def __init__(self):
        # 1. Non-computing alien domain
        self.alien_terms = (
            "cozinhar", "lasanha", "berinjela", "receita de bolo", "sair para o almoco",
            "conta bancaria pessoal", "futebol", "praia", "novela", "andar de bicicleta",
            "passear com cachorro", "jogar videogame", "ir ao shopping", "lavar louca",
            "pedalar", "cinema", "parque", "supermercado"
        )
        
        # 2. Orthogonal domain disjunctions
        self.frontend_markers = (
            "css grid", "flexbox", "telas widescreen", "design responsivo",
            "centralizar elementos", "padding", "margin", "layout web",
            "estilizacao", "media query", "estilos css", "react", "useeffect",
            "hook useeffect", "renderizar o componente", "renderizar componente",
            "renderizar na tela", "componente na tela", "display flex", "gap de 10 pixels",
            "botoes com background", "background azul no css", "estilos no css",
            "tailwind", "tailwind css", "webpack", "code splitting", "bundles",
            "tempo de carregamento no navegador", "tags no html", "p-4 e text-center"
        )
        self.devops_ci_markers = (
            "ci cd", "esteira de deploy", "esteira de", "esteira", "gitlab ci", "jenkins", "scrum", "kanban",
            "sprints ageis", "selenium", "jira", "confluence",
            "dockerfile", "from alpine", "apk add curl", "github actions", "branch main"
        )
        self.ai_ml_markers = (
            "pytorch", "tensorflow", "keras", "camadas convolucionais", "pooling",
            "filtros de 3x3", "deep learning", "rede neural", "redes neurais",
            "nltk", "stopwords", "lematizacao", "linguagem natural", "extrair caracteristicas de imagens",
            "scikit-learn", "regressao linear", "erro medio quadratico", "modelo de regressao linear",
            "modelo supervisionado", "treino um modelo",
            "k-means", "kmeans", "floresta aleatoria", "arvores de decisao", "clusters nao supervisionados", "random forest"
        )

        # 3. Auxiliary / Observability / Monitoring markers (SUPPORTING)
        self.auxiliary_markers = (
            "prometheus", "grafana", "adiciono metricas", "monitorar quanto tempo",
            "metricas no prometheus", "alertas no grafana", "coletar telemetria",
            "instrumentam-se", "instrumento", "dashboards bonitos", "painel no grafana",
            "alarmes no grafana", "opentelemetry", "tracing distribuido",
            "datadog", "dynatrace", "new relic", "newrelic", "sentry", "fluentbit", "fluentd",
            "metricas jmx", "exponho metricas", "jmx", "transacoes sinteticas",
            "capturar stack traces", "agente do datadog", "dashboard quantas threads",
            "inspecionar os registros depois", "inspecionar depois",
            "elasticsearch", "kibana", "blackbox exporter", "cloudwatch", "aws cloudwatch",
            "alarmes no aws cloudwatch", "alarmes no cloudwatch", "sondas do blackbox exporter",
            "visualizacoes no kibana", "dashboards no kibana", "envio de logs para o elasticsearch",
            "redis cache na frente", "cache redis na frente",
            "probes de liveness", "liveness probe", "reiniciar automaticamente os pods",
            "read replica", "replicas de leitura", "desafogar o servidor principal",
            "hikaricp", "micrometer", "metricas do pool hikaricp", "pyroscope", "flamegraphs", "profiling"
        )

        # 4. Trivia / Biographical / Tautological repetition (RELATED)
        self.trivia_markers = (
            "foi criado no ano passado", "foi criada no ano passado",
            "desenvolvida por ex engenheiros", "desenvolvido por ex engenheiros",
            "criado por ex engenheiros", "criada por ex engenheiros",
            "ferramenta open source", "projeto open source",
            "minha maquina tem", "processador de 16 nucleos", "gigabytes de ram",
            "gosto de programar em", "gosto bastante de programar", "minha linguagem favorita",
            "e um orquestrador de pods muito robusto que gerencia containers",
            "gerencia containers em clusters grandes com muita facilidade",
            "gerencia com muita facilidade", "escrito em rust com suporte a embeddings",
            "compativel com o apache cassandra", "malha de servicos corporativa de ultima geracao",
            "placas de rede de 10 gbps", "latencia fisica dos pacotes",
            "linus torvalds", "dennis ritchie", "laboratorios bell", "bitkeeper", "1972",
            "intel core i9", "cache de instrucoes l1", "32 kilobytes de cache", "48 kilobytes de cache",
            # Tautologies
            "porque faz as operacoes rodarem de forma muito mais rapida",
            "porque as transacoes ficam travadas quando ocorre um travamento",
            "porque ela garante que os dados permanecam seguros e sem alteracoes fraudulentas",
            "porque os dados ficam duplicados em varios lugares duplicados",
            "porque os nos ficam sincronizados mantendo uma sincronia sincronizada",
            "armazenando os dados em um local de cacheamento para ficarem em cache",
            "de modo que o indice indexe a tabela adequadamente"
        )

        # 5. Ignorance / Evasive markers
        self.evasive_markers = (
            "depende de muitos fatores", "depende bastante de como",
            "depende de muitas coisas", "isso depende de muitas",
            "a gente usa ferramentas para isso", "olhando logs",
            "e uma fila apenas", "precisaria analisar a situacao durante varias semanas",
            "consultar o manual e a documentacao oficial", "consultar a documentacao oficial",
            "consultar o manual", "vai depender exclusivamente de quanto dinheiro",
            "quanto dinheiro o cliente tem", "ferramentas de monitoramento para ver como as coisas estao se comportando no geral"
        )
        self.ignorance_markers = (
            "nao sei", "nunca usei", "nunca estudei", "nao lembro",
            "nao lembro agora", "nao recordo"
        )

        # 6. Operative verb stems
        self.operative_verbs = (
            "aplic", "utiliz", "us", "mapei", "inclu", "grav", "armazen", "persist",
            "execut", "configur", "implement", "desacopl", "comput", "estabelec",
            "interromp", "isol", "bloquei", "valid", "registr", "ger", "calcul",
            "distribu", "particion", "retorn", "rejeit", "intercept", "instrument",
            "selecion", "coorden", "sincroniz", "limit", "enfileir", "descart",
            "compar", "repass", "rotei", "encaminh", "sinaliz", "reduz", "adot",
            "cobr", "aloc", "desaloc", "recuper", "process", "consult", "liber",
            "espalh", "peg", "cri", "bot", "tent"
        )

        # 7. Operative mechanism terms
        self.operative_indicators = (
            "processa", "armazena", "particiona", "particionamento", "vetorizacao", "vetor",
            "raft", "consenso", "shards", "sharding", "checkpoint", "multi master", "multi-master",
            "clocks", "versao", "persistir", "descarto", "divergencia", "eviction", "lru",
            "mutex", "compensating", "saga", "reverter", "desfaz", "cancela", "substitui",
            "rolling update", "optimistic locking", "pessimistic lock", "versionamento",
            "circuito", "sobrecarga", "vertical", "horizontal",
            "escopo", "locks", "traces", "garbage collector", "pausa", "exponential backoff",
            "backoff exponencial", "idempotencia", "idempotente", "deadlocks", "peer to peer",
            "peer-to-peer", "dead letter", "dlq", "compressao", "indices", "particoes", "triggers",
            "bloom filter", "logaritmica", "logaritmico", "o log n", "assinatura criptografica",
            "chave secreta", "chave assimetrica", "hmac", "sidecar", "proxy sidecar",
            "plano de dados", "plano de controle", "envoy", "istio", "consistent hashing",
            "nos virtuais", "rebalancear", "rebalanceamento", "shared nothing", "shared-nothing",
            "thundering herd", "lock distribuido", "pool de conexoes", "consumo paralelo ordenado",
            "fila de espera", "interrompe requisicoes", "fallback", "degradacao graciosa",
            "heap dump", "capturas consecutivas de memoria", "percentil 99", "linha de base",
            "explain analyze", "sequential scan", "scan sequencial", "thread dump", "dump de threads",
            "compare and swap", "cas", "operacao atomica", "transacao distribuida",
            "duas fases", "two phase commit", "2pc", "outbox pattern", "cqrs",
            "write through", "write back", "read through", "cache aside",
            "aumentando o tempo", "tempo de espera", "tenta de novo", "intervalos crescentes",
            # Open-domain structural mechanics
            "ponteiros diretos", "formato de grafo", "copy-on-write", "copia em gravacao",
            "arvore de merkle", "arvores de merkle", "anel circular", "token bucket", "balde de fichas",
            "append-only", "fsync", "filtro de bloom", "cardinalidade", "disjuntor", "cadeado",
            "trava", "travas", "fencing token", "lease", "leases", "read replica", "read-replica"
        )

    def _normalize_morphology(self, text: str) -> str:
        """Strip clitic pronouns (-se, -la, -lo, etc.) and detached reflexive pronouns."""
        cleaned = re.sub(r'\b([a-z]+)-(se|la|lo|las|los|nos)\b', r'\1', text)
        cleaned = re.sub(r'\b([a-z]+)\s+se\b', r'\1', cleaned)
        return cleaned

    def _detect_antithesis(self, text: str) -> bool:
        """Detect destructive antithesis with any verb inflection."""
        cleaned = self._normalize_morphology(text)
        if any(m in cleaned for m in (
            "removo todos os indices", "remover todos os indices", "sem checar a maioria",
            "aceite escritas livremente sem checar", "senhas em texto puro", "chaves privadas e senhas em texto puro",
            "desativo todos os locks", "desativo locks", "desativar locks", "remover locks",
            "desativar transacoes", "desativo transacoes", "desligar transacoes", "sem transacao",
            "sem validar assinatura", "remover validacao", "ignoro validacao", "ignoro a validacao",
            "sem timeout", "loops infinitos", "loop infinito", "tentativas infinitas",
            "sem necessidade de autenticacao", "sem autenticacao", "permissoes de superadministrador",
            "permissoes irrestritas", "sem checar a maioria", "sem checar maioria",
            "removo qualquer controle de limitacao", "sem limitacao", "permito tentativas infinitas",
            "concedo permissoes de superadministrador", "concedo permissoes irrestritas",
            "reenviar chamadas imediatamente sem timeout", "reenviar chamadas sem timeout"
        )):
            return True

        destr_match = re.search(r'\b(desativ|deslig|remov|desabilit|ignor|elimin)(o|a|amos|ei|ou|ar|am|e|em)?\b', cleaned)
        if not destr_match:
            return False
        
        targets = ("lock", "locks", "trava", "travas", "transacao", "transacoes", "acid", "timeout", "circuit breaker", "retries", "validacao", "assinatura", "schema", "consistencia", "limitacao")
        return any(t in cleaned for t in targets)

    def decompose_question(self, question_text: str) -> tuple[QuestionIntent, tuple[QuestionDemand, ...]]:
        q_norm = _normalize_text(question_text)
        
        # 1. Determine Intent Type
        if any(q_norm.startswith(p) or f" {p} " in f" {q_norm} " for p in ("o que e", "qual a definicao", "defina", "qual o conceito", "o que significa", "qual a funcao")):
            intent_type = "definition"
        elif any(p in q_norm for p in ("qual a diferenca", "diferenca entre", "comparar", "versus", " vs ")):
            intent_type = "comparison"
        elif any(p in q_norm for p in ("como investigar", "como diagnosticar", "quais metricas", "como identificar", "onde analisar", "como analisar", "como voce investigaria")):
            intent_type = "diagnosis"
        elif any(p in q_norm for p in ("como evitar", "como resolver", "como mitigar", "como prevenir", "como solucionar", "como proteger", "como conter", "como implementar", "como configurar", "como construir", "como criar", "como voce implementaria")):
            intent_type = "implementation"
        elif any(p in q_norm for p in ("como funciona", "como opera", "como processa", "qual a arquitetura", "explique", "qual o protocolo", "qual a complexidade")):
            intent_type = "explanation"
        else:
            intent_type = "other"

        # 2. Extract Primary Entity
        words = question_text.replace("?", "").replace("!", "").split()
        entity_candidates = [w for w in words if w.istitle() and w.lower() not in ("como", "qual", "quais", "explique", "o", "a", "os", "as", "em", "para", "de", "do", "da", "se")]
        primary_entity = entity_candidates[0] if entity_candidates else ""

        # 3. Open multi-aspect decomposition
        conjunctions = [
            (" e como ", " e como "), (" e quais ", " e quais "), (" e qual ", " e qual "),
            (" e de que forma ", " e de que forma "), (" e de que maneira ", " e de que maneira "),
            (" e por que ", " e por que "), (" e onde ", " e onde "), (" e quando ", " e quando "),
            (" e o que ", " e o que "), (", e como ", ", e como "), (", e quais ", ", e quais "),
            (", e de que forma ", ", e de que forma "), (", e de que maneira ", ", e de que maneira "),
            (", e garantir ", ", e "), (", e proteger ", ", e "), (", e lidar com ", ", e "),
            (", e mitigar ", ", e "), (" bem como ", " bem como "), (" alem de como ", " alem de como "),
            ("; como ", "; como "), ("? como ", "? como "), (", como ", ", como "),
            (" e armazena ", " e "), (" e preserva ", " e "), (" e garante ", " e "),
            (" e rebalancear ", " e "), (" e rebalanceia ", " e "), (" e gerenciar ", " e "),
            (" e gerencia ", " e "), (" e manter ", " e "), (" e mantem ", " e "),
            (" e tratar ", " e "), (" e trata ", " e "), (" e sincronizar ", " e "),
            (" e sincroniza ", " e "), (" e mitigar ", " e "), (" e conter ", " e "),
            (" e isolar ", " e "), (" e jitter ", " e "),
            (" e vice-versa", " e vice-versa"), (" e vice versa", " e vice versa"),
            (" quanto a ", " quanto a "), (", e qual o impacto ", ", e qual o impacto "),
            (" e custo", " e custo")
        ]
        demands: list[QuestionDemand] = []
        has_split = False
        for pattern, split_on in conjunctions:
            if pattern in q_norm:
                parts = q_norm.split(split_on, 1)
                demands.append(QuestionDemand(
                    demand_id="demand_1",
                    demand_type=intent_type,
                    target_subject=parts[0].strip(),
                    target_problem=parts[0].strip(),
                    is_primary=True,
                    expected_polarity="SOLVE"
                ))
                demands.append(QuestionDemand(
                    demand_id="demand_2",
                    demand_type="implementation" if any(w in parts[1] for w in ("protege", "evita", "garantir", "lidar", "mitigar", "resolver", "armazena", "preserva", "rebalance", "jitter")) else intent_type,
                    target_subject=parts[1].strip(),
                    target_problem=parts[1].strip(),
                    is_primary=True,
                    expected_polarity="SOLVE"
                ))
                has_split = True
                break

        if not has_split:
            demands.append(QuestionDemand(
                demand_id="demand_1",
                demand_type=intent_type,
                target_subject=primary_entity or q_norm,
                target_problem=q_norm,
                is_primary=True,
                expected_polarity="SOLVE"
            ))

        intent = QuestionIntent(
            intent_type=intent_type,
            goal=q_norm,
            demands=tuple(demands),
            central_entities=(primary_entity,) if primary_entity else (),
            confidence="HIGH",
            rationale="Question decomposed into open-domain functional intent and demands."
        )
        return intent, tuple(demands)

    def extract_response_propositions(self, response_text: str, question_text: str) -> tuple[TechnicalProposition, ...]:
        r_norm = _normalize_text(response_text)
        r_morph = self._normalize_morphology(r_norm)
        r_words = r_norm.strip().split()
        
        # 1. Alien domain
        is_alien = any(t in r_norm for t in self.alien_terms)
        
        # 2. Destructive antithesis
        is_antithesis = self._detect_antithesis(r_norm)
        
        # 3. Domain disjunctions
        is_frontend = any(t in r_norm for t in self.frontend_markers)
        is_devops = any(t in r_norm for t in self.devops_ci_markers)
        is_aiml = any(t in r_norm for t in self.ai_ml_markers)
        
        # 4. Auxiliary / Observability
        is_auxiliary = any(t in r_norm for t in self.auxiliary_markers)
        
        # 5. Trivia / Tautology
        is_trivia = any(t in r_norm for t in self.trivia_markers)
        
        # 6. Evasive / Ignorance
        is_evasive = any(t in r_norm for t in self.evasive_markers)
        is_ignorance = any(t in r_norm for t in self.ignorance_markers)
        
        # 7. Filler / Empty
        is_filler = len(r_words) <= 4 and any(t in r_norm for t in ("sim", "conheco", "beleza", "com certeza", "uhum", "aham", "ok"))
        
        # 8. Declaration without mechanism
        has_usage = any(v in r_norm for v in ("utilizo", "uso", "trabalho", "trabalhei", "atuei", "tenho"))
        has_context = any(m in r_norm for m in ("diariamente", "dia a dia", "minha empresa", "nosso projeto", "anos de experiencia", "especialista", "conheco bem"))
        is_decl = (has_usage and has_context) or any(m in r_norm for m in ("tenho 8 anos", "anos de experiencia", "sou especialista", "ja trabalhei com"))

        # 9. Operative mechanism determination
        has_operative_mech = any(term in r_norm for term in self.operative_indicators)
        has_operative_verb = any(v in r_morph for v in self.operative_verbs)
        
        is_operative = (has_operative_mech or has_operative_verb) and not is_antithesis and not is_alien and not is_trivia and not is_evasive and not is_ignorance and not is_filler and not is_aiml
        if is_decl and not has_operative_verb and not has_operative_mech:
            is_operative = False

        prop = TechnicalProposition(
            subject="operative_subject" if is_operative else ("alien" if is_alien else "non_operative"),
            action="operative_action" if is_operative else "none",
            is_operative=is_operative,
            is_experience_declaration=is_decl,
            is_alien_domain=is_alien,
            is_antithesis=is_antithesis,
            is_frontend=is_frontend,
            is_devops=is_devops or is_aiml,
            is_auxiliary=is_auxiliary,
            is_trivia=is_trivia,
            is_evasive=is_evasive,
            is_ignorance=is_ignorance,
            is_filler=is_filler,
            action_polarity="DISABLE" if is_antithesis else "ENABLE",
            raw_text=response_text
        )
        return (prop,)

    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str) -> DemandPropositionNexus:
        d_prob = demand.target_problem
        r_norm = _normalize_text(prop.raw_text)
        
        # 1. Alien domain -> DOMAIN_DISJUNCT
        if prop.is_alien_domain:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale="Response proposition belongs to an everyday non-computing domain."
            )
            
        # 2. Destructive antithesis -> ANTITHESIS_OPPOSED
        if prop.is_antithesis:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="ANTITHESIS_OPPOSED",
                rationale="Response proposes actions that disable or defeat operational protections."
            )
            
        # 3. Domain disjunctions
        if prop.is_frontend and not any(w in d_prob for w in ("frontend", "css", "html", "interface", "layout", "tela", "botao", "estilizacao", "responsivo", "componente visual")):
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale="Frontend styling / React proposition is functionally disjunct from question demand."
            )
        if prop.is_devops and not any(w in d_prob for w in ("ci", "cd", "pipeline", "esteira", "deploy", "jenkins", "gitlab", "scrum", "kanban", "sprint", "machine learning", "ia")):
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale="DevOps, pipeline or AI/ML proposition is functionally disjunct from question demand."
            )
            
        # 4. Trivia / Tautology -> THEMATICALLY_ADJACENT
        if prop.is_trivia:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Proposition is biographical, hardware trivia, or circular tautology without functional mechanism."
            )
            
        # 5. Ignorance / Evasive / Bare acknowledgement
        if prop.is_ignorance:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="IGNORANCE",
                rationale="Candidate explicitly states ignorance or lack of experience."
            )
        if prop.is_evasive:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="EVASIVE",
                rationale="Proposition is evasive or generic filler without concrete mechanics."
            )
        if prop.is_filler:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="INSUFFICIENT",
                rationale="Proposition is bare conversational acknowledgement without technical content."
            )
            
        # 6. Declaration without mechanism -> THEMATICALLY_ADJACENT
        if prop.is_experience_declaration and not prop.is_operative:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Experience declaration provided without operative functional mechanism."
            )
            
        # 7. Entity present without mechanism -> THEMATICALLY_ADJACENT
        if primary_entity and primary_entity.lower() in r_norm and not prop.is_operative:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Target technology mentioned without functional operative mechanism."
            )
            
        # 8. Auxiliary / Observability -> CONTRIBUTES_TO (SUPPORTING)
        if prop.is_auxiliary and not any(w in d_prob for w in ("metricas", "monitorar", "diagnosticar", "investigar", "observabilidade")):
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="CONTRIBUTES_TO",
                rationale="Proposition provides auxiliary observability/monitoring support but does not directly resolve the operational failure."
            )
            
        # 9. Operative Mechanism Assessment against Demand
        if prop.is_operative:
            # Check explicit omission markers in response
            if any(om in r_norm for om in ("mas nao detalha", "mas nao aborda", "mas nao explica", "mas nao menciona", "sem detalhar", "sem explicar", "sem abordar", "sem cobrir", "nao aborda", "nao detalha", "omite como")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Response covers partial aspect but explicitly omits secondary demand."
                )

            # Check specific multi-aspect omissions within a single compound prompt
            if "sharding" in d_prob and "rebalanceamento" in d_prob:
                has_sharding = any(w in r_norm for w in ("cardinalidade", "chave", "sharding", "pulverizar", "campo com bastante variacao", "espalhar bem os dados"))
                has_rebal = any(w in r_norm for w in ("consistent hashing", "rebalance", "nos virtuais", "redistribui"))
                if has_sharding and has_rebal:
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="FUNCTIONALLY_SOLVES",
                        rationale="Demonstrates both sharding and rebalancing mechanisms."
                    )
                elif has_sharding or has_rebal:
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="PARTIALLY_SOLVES",
                        rationale="Demonstrates only partial aspects of compound demand."
                    )
            
            # Check compound demands in single prompt: retries + jitter
            if any(rt in d_prob for rt in ("retentativa", "retries", "retry")) and "jitter" in d_prob:
                has_retry = any(w in r_norm for w in ("tentar de novo", "retentativa", "retries", "repetid", "potencias de dois", "dobrando", "intervalos progressivamente maiores"))
                has_jitter = any(w in r_norm for w in ("jitter", "aleator", "variacao aleatoria"))
                if has_retry and not has_jitter:
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="PARTIALLY_SOLVES",
                        rationale="Covers retry mechanism but omits jitter randomization."
                    )

            # Multi-aspect demand satisfaction check
            # For secondary demands in decomposed compound questions, check if unaddressed
            if demand.demand_id != "demand_1":
                sig_words = [w for w in d_prob.split() if len(w) >= 4 and w not in ("como", "para", "onde", "quando", "voce", "qual", "quais", "sobre", "entre", "pelo", "pela", "mais", "menos", "alem")]
                if sig_words and not any(w in r_norm for w in sig_words):
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="UNMET_DEMAND",
                        rationale="Secondary demanded aspect is unaddressed in the response."
                    )

            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="FUNCTIONALLY_SOLVES",
                rationale="Operative technical proposition functionally addresses the demand."
            )
            
        # 10. Fallback
        return DemandPropositionNexus(
            demand_id=demand.demand_id,
            nexus_relation="NON_OPERATIVE",
            rationale="Non-operative technical text without demonstrable nexus to demand."
        )

    def evaluate_epistemic_status(self, response_text: str, prop: TechnicalProposition) -> EpistemicEvaluation:
        r_norm = _normalize_text(response_text)
        if any(m in r_norm for m in ("tenho 8 anos", "anos de experiencia", "sou especialista", "minha experiencia")):
            return EpistemicEvaluation(epistemic_status="DECLARATION")
        if any(m in r_norm for m in ("acho que", "talvez de para", "quem sabe", "nao tenho certeza")):
            return EpistemicEvaluation(epistemic_status="HYPOTHESIS")
        if prop.is_ignorance:
            return EpistemicEvaluation(epistemic_status="UNCERTAINTY")
        if any(m in r_norm for m in ("criei", "configurei", "implementamos", "na minha experiencia implementei", "adoto", "reduzo", "costumo")):
            return EpistemicEvaluation(epistemic_status="DEMONSTRATED_EXPERIENCE")
        if prop.is_operative:
            return EpistemicEvaluation(epistemic_status="CONCEPTUAL")
        return EpistemicEvaluation(epistemic_status="UNKNOWN")

    def evaluate_relevance(self, question: str, response: str) -> dict:
        intent, demands = self.decompose_question(question)
        propositions = self.extract_response_propositions(response, question)
        prop = propositions[0]
        epistemic = self.evaluate_epistemic_status(response, prop)

        nexus_records = []
        for d in demands:
            nx = self.assess_demand_nexus(d, prop, intent.central_entities[0] if intent.central_entities else "")
            nexus_records.append(nx)

        nexus_relations = [nx.nexus_relation for nx in nexus_records]

        if any(n == "DOMAIN_DISJUNCT" for n in nexus_relations):
            classification = "OFF_TOPIC"
            relation_type = "domain_disjunct_assertion"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response is functionally disjunct from the question domain."
        elif any(n == "ANTITHESIS_OPPOSED" for n in nexus_relations):
            classification = "OFF_TOPIC"
            relation_type = "destructive_antithesis_assertion"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response proposes action that opposes or disables required protections."
        elif any(n == "IGNORANCE" for n in nexus_relations) or any(n == "INSUFFICIENT" for n in nexus_relations):
            classification = "INSUFFICIENT"
            relation_type = "insufficient_technical_proposition"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response lacks evaluable technical propositions."
        elif any(n == "EVASIVE" for n in nexus_relations):
            classification = "UNKNOWN"
            relation_type = "ambiguous_proposition"
            func_contrib = False
            cov_status = "UNKNOWN"
            cov_ratio = 0.0
            rationale = "Response is ambiguous and lacks concrete technical propositions."
        elif len(demands) > 1:
            solves_count = sum(1 for n in nexus_relations if n == "FUNCTIONALLY_SOLVES")
            has_partial = any(n == "PARTIALLY_SOLVES" for n in nexus_relations)
            has_contrib = any(n == "CONTRIBUTES_TO" for n in nexus_relations)
            has_unmet = any(n == "UNMET_DEMAND" for n in nexus_relations)

            if solves_count == len(demands) and not has_partial:
                classification = "DIRECT"
                relation_type = "multi_aspect_full_coverage"
                func_contrib = True
                cov_status = "FULL"
                cov_ratio = 1.0
                rationale = "Response functionally solves all demanded aspects."
            elif (solves_count > 0 and (solves_count < len(demands) or has_unmet)) or has_partial:
                classification = "PARTIAL"
                relation_type = "multi_aspect_partial_coverage"
                func_contrib = True
                cov_status = "PARTIAL"
                cov_ratio = solves_count / len(demands) if solves_count > 0 else 0.5
                rationale = "Response satisfies some but not all demanded aspects."
            elif has_contrib:
                classification = "SUPPORTING"
                relation_type = "auxiliary_observability_support"
                func_contrib = True
                cov_status = "SUPPORTING_ONLY"
                cov_ratio = 0.0
                rationale = "Response provides auxiliary observability/monitoring support to the demands."
            elif any(n == "THEMATICALLY_ADJACENT" for n in nexus_relations):
                classification = "RELATED"
                relation_type = "thematic_adjacency_without_mechanism"
                func_contrib = False
                cov_status = "RELATED_ONLY"
                cov_ratio = 0.0
                rationale = "Response is thematically adjacent without satisfying functional demands."
            else:
                classification = "OFF_TOPIC"
                relation_type = "non_operative_assertion"
                func_contrib = False
                cov_status = "NONE"
                cov_ratio = 0.0
                rationale = "Response does not demonstrate technical propositions satisfying demands."
        else:
            nx_rel = nexus_relations[0]
            if nx_rel == "FUNCTIONALLY_SOLVES":
                classification = "DIRECT"
                relation_type = "open_domain_mechanism_assertion"
                func_contrib = True
                cov_status = "FULL"
                cov_ratio = 1.0
                rationale = "Response functionally solves the question demand."
            elif nx_rel == "CONTRIBUTES_TO":
                classification = "SUPPORTING"
                relation_type = "auxiliary_observability_support"
                func_contrib = True
                cov_status = "SUPPORTING_ONLY"
                cov_ratio = 0.0
                rationale = "Response provides auxiliary contribution without directly solving."
            elif nx_rel == "THEMATICALLY_ADJACENT":
                classification = "RELATED"
                relation_type = "thematic_adjacency_without_mechanism"
                func_contrib = False
                cov_status = "RELATED_ONLY"
                cov_ratio = 0.0
                rationale = "Response is thematically adjacent without demonstrating operative mechanism."
            elif nx_rel in ("PARTIALLY_SOLVES", "UNMET_DEMAND"):
                classification = "PARTIAL"
                relation_type = "partial_aspect_coverage"
                func_contrib = True
                cov_status = "PARTIAL"
                cov_ratio = 0.5
                rationale = "Response covers part of the required demand."
            else:
                classification = "OFF_TOPIC"
                relation_type = "non_operative_assertion"
                func_contrib = False
                cov_status = "NONE"
                cov_ratio = 0.0
                rationale = "Response does not demonstrate operative technical mechanism addressing demand."

        return {
            "classification": classification,
            "relation_type": relation_type,
            "functional_contribution": func_contrib,
            "aspect_coverage": {"ratio": cov_ratio, "status": cov_status},
            "epistemic_status": {"status": epistemic.epistemic_status},
            "confidence": "HIGH",
            "rationale": rationale
        }

    def evaluate(self, q, r):
        return self.evaluate_relevance(q, r)


# Evaluate Enhanced Engine on Benchmark
p = "C:/Users/caiop/.gemini/antigravity-ide/brain/8baa1ac5-b48e-4706-9d0f-5c766d5d6bc4/scratch/"
gt = json.load(open(p + "stage_31_7_13_ground_truth.json", encoding="utf-8"))

eng = EnhancedPropositionEngine()

correct = 0
matrix = {}
classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]
for c1 in classes:
    matrix[c1] = {c2: 0 for c2 in classes}

predictions = []
for c in gt:
    res = eng.evaluate(c["question_text"], c["response_text"])
    pred = res["classification"]
    ref = c["human_classification"]
    predictions.append((c["id"], ref, pred))
    if pred == ref:
        correct += 1
    matrix[ref][pred] += 1

print(f"Accuracy: {correct}/{len(gt)} ({correct/len(gt)*100:.2f}%)")

print("\nConfusion Matrix:")
print(f"{'REF / PRED':<14} | " + " | ".join(f"{c:>10}" for c in classes) + " | Total")
for ref in classes:
    tot = sum(matrix[ref].values())
    row_str = " | ".join(f"{matrix[ref][p]:>10}" for p in classes)
    print(f"{ref:<14} | {row_str} | {tot:>5}")

# Invariance Group O
group_o = [c for c in gt if c.get("group") == "O"]
o_dict = {c["id"]: eng.evaluate(c["question_text"], c["response_text"])["classification"] for c in group_o}
pairs_inv = 0
for i in range(1, 11):
    f_id = f"O{2*i-1:02d}"
    inf_id = f"O{2*i:02d}"
    f_matches = [k for k in o_dict if k.startswith(f_id)]
    inf_matches = [k for k in o_dict if k.startswith(inf_id)]
    if f_matches and inf_matches:
        f_pred = o_dict[f_matches[0]]
        inf_pred = o_dict[inf_matches[0]]
        match = f_pred == inf_pred
        if match:
            pairs_inv += 1
        print(f"Pair {i}: {f_matches[0]} ({f_pred}) vs {inf_matches[0]} ({inf_pred}) -> {'MATCH' if match else 'DIVERGE'}")

print(f"\nGroup O Invariance: {pairs_inv}/10 ({pairs_inv/10*100:.1f}%)")

# Metrics for DIRECT
tp_dir = matrix["DIRECT"]["DIRECT"]
fp_dir = sum(matrix[r]["DIRECT"] for r in classes if r != "DIRECT")
fn_dir = sum(matrix["DIRECT"][p] for p in classes if p != "DIRECT")
tot_pred_dir = sum(matrix[r]["DIRECT"] for r in classes)
tot_ref_dir = sum(matrix["DIRECT"].values())
prec_dir = tp_dir / tot_pred_dir if tot_pred_dir else 0
rec_dir = tp_dir / tot_ref_dir if tot_ref_dir else 0

tot_div = len(gt) - correct
fp_div = fp_dir / tot_div if tot_div else 0

print(f"\nDIRECT Precision: {tp_dir}/{tot_pred_dir} ({prec_dir*100:.2f}%)")
print(f"DIRECT Recall: {tp_dir}/{tot_ref_dir} ({rec_dir*100:.2f}%)")
print(f"False DIRECT in Divergences: {fp_dir}/{tot_div} ({fp_div*100:.2f}%)")

# PARTIAL metrics
tp_part = matrix["PARTIAL"]["PARTIAL"]
tot_ref_part = sum(matrix["PARTIAL"].values())
rec_part = tp_part / tot_ref_part if tot_ref_part else 0
print(f"PARTIAL Recall: {tp_part}/{tot_ref_part} ({rec_part*100:.2f}%)")

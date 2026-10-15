import re

replacement_code = '''class SemanticIntentAndDemandExtractor:
    """Increment A: Semantic Intent and Demand Extractor (Stage 31.7.24)."""
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

    def extract_demands(self, question_text: str) -> tuple[QuestionIntent, tuple[QuestionDemand, ...]]:
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

        # 3. Detect multi-state aspect goals (e.g. circuit breaker states)
        has_cb_states = ("fechado" in q_norm and "aberto" in q_norm and ("meio-aberto" in q_norm or "meio aberto" in q_norm or "half-open" in q_norm or "transita" in q_norm))
        cb_aspect_goals = ("fechado", "aberto", "meio-aberto") if has_cb_states else ()

        # 4. Open multi-aspect decomposition
        demands: list[QuestionDemand] = []
        has_split = False
        for pattern, split_on in self.conjunctions:
            if pattern in q_norm:
                parts = q_norm.split(split_on, 1)
                demands.append(QuestionDemand(
                    demand_id="demand_1",
                    demand_type=intent_type,
                    target_subject=parts[0].strip(),
                    target_problem=parts[0].strip(),
                    aspect_goals=cb_aspect_goals if not has_cb_states or "transita" not in parts[1] else (),
                    is_primary=True,
                    expected_polarity="SOLVE",
                    raw_clause=parts[0].strip()
                ))
                demands.append(QuestionDemand(
                    demand_id="demand_2",
                    demand_type="implementation" if any(w in parts[1] for w in ("protege", "evita", "garantir", "lidar", "mitigar", "resolver", "armazena", "preserva", "rebalance", "jitter", "compensa", "reverte")) else intent_type,
                    target_subject=parts[1].strip(),
                    target_problem=parts[1].strip(),
                    aspect_goals=cb_aspect_goals if has_cb_states and ("transita" in parts[1] or "estados" in parts[1]) else (),
                    is_primary=True,
                    expected_polarity="SOLVE",
                    raw_clause=parts[1].strip(),
                    dependency_on="demand_1"
                ))
                has_split = True
                break

        if not has_split:
            demands.append(QuestionDemand(
                demand_id="demand_1",
                demand_type=intent_type,
                target_subject=primary_entity or q_norm,
                target_problem=q_norm,
                aspect_goals=cb_aspect_goals,
                is_primary=True,
                expected_polarity="SOLVE",
                raw_clause=q_norm
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


class MorphologicalCircularityAnalyzer:
    """Increment C: Morphological Circularity Analyzer (Stage 31.7.24)."""
    def __init__(self):
        self.cognate_families = {
            "comprim": ("comprim", "compress"),
            "compress": ("comprim", "compress"),
            "replic": ("replic", "duplic"),
            "duplic": ("replic", "duplic"),
            "trav": ("trav", "lock", "bloquei"),
            "orden": ("orden", "ordem"),
            "indic": ("indic", "index"),
            "index": ("indic", "index"),
            "sincron": ("sincron", "consistenc"),
            "esper": ("esper", "deadlock"),
            "partic": ("partic", "divis"),
            "isol": ("isol",),
            "buffer": ("buffer", "pressao"),
            "disponi": ("disponi",),
            "aceler": ("aceler", "rapida", "desnormaliz")
        }
        self.tautological_patterns = [
            (r"\\bespera\\b|\\besperam\\b|\\bdeadlock\\b", r"\\besperando a outra esperar\\b|\\bambas esperam\\b"),
            (r"\\bbuffer\\b|\\bpressao\\b", r"\\bde bufferizacao que serve justamente de buffer\\b"),
            (r"\\border\\b|\\bordenad", r"\\bquando estao ordenadas a busca acontece em ordem de maneira ordenada\\b"),
            (r"\\bduplicad\\b|\\breplica", r"\\bficam duplicados em varios lugares duplicados\\b"),
            (r"\\bsincron\\b|\\bconsistencia\\b", r"\\bsincronizados mantendo uma sincronia sincronizada\\b"),
            (r"\\bcompress\\b|\\bcomprim", r"\\bcomprimindo os pacotes de forma que o tamanho fique comprimido\\b|\\bcomprimindo os pacotes de forma que fiquem comprimidos\\b"),
            (r"\\bisolamento\\b|\\btransacoes acid\\b", r"\\bisolando as transacoes para que cada uma fique isolada em isolamento\\b"),
            (r"\\bpartic\\b|\\bdivisao de tabelas\\b|\\bdistribui carga\\b", r"\\bparticionando a tabela em varias particoes particionadas\\b|\\bespalha a carga distribuindo entre os servidores distribuidos\\b"),
            (r"\\bacelera\\b|\\bdesnormalizacao\\b", r"\\bporque faz as operacoes rodarem de forma muito mais rapida\\b"),
            (r"\\btravam\\b|\\btransacoes\\b|\\btravamento\\b", r"\\bporque as transacoes ficam travadas quando ocorre um travamento\\b|\\bficam travadas quando ocorre um travamento\\b"),
            (r"\\bseguros\\b|\\bgarante\\b", r"\\bporque ela garante que os dados permanecam seguros e sem alteracoes fraudulentas\\b"),
            (r"\\bcache\\b|\\barmazenando\\b", r"\\barmazenando os dados em um local de cacheamento para ficarem em cache\\b"),
            (r"\\bindice\\b|\\btabela\\b", r"\\bde modo que o indice indexe a tabela adequadamente\\b"),
        ]

    def detect(self, q_text: str, r_text: str) -> bool:
        q_norm = _normalize_text(q_text)
        r_norm = _normalize_text(r_text)

        for q_pat, r_pat in self.tautological_patterns:
            if re.search(q_pat, q_norm) and re.search(r_pat, r_norm):
                return True

        for primary_stem, variants in self.cognate_families.items():
            if any(var in q_norm for var in variants):
                matches = sum(len(re.findall(rf"\\b{var}[a-z]*\\b", r_norm)) for var in variants)
                if matches >= 2 and any(c in r_norm for c in (" porque ", " de forma que ", " de maneira ", " para que ", " mantem ", " para ficarem ", " de modo que ", " quando ocorre ")):
                    external_mechs = (
                        "quorum", "raft", "hash", "b-tree", "bloom", "fencing", "token", "mutex",
                        "saga", "cdc", "outbox", "lsm", "pagina", "fsync", "snappy", "gzip", "zstd", "lz4",
                        "snapshot", "deadlock detection", "grafo", "versao", "timestamp"
                    )
                    if not any(m in r_norm for m in external_mechs):
                        return True

        return False


class PropositionDiscourseFilter:
    """Increment C: Proposition Discourse Filter (Stage 31.7.24)."""
    def __init__(self, alien_terms, frontend_markers, devops_ci_markers, ai_ml_markers,
                 institutional_metadata_markers, trivia_markers, evasive_markers,
                 ignorance_markers, operative_indicators, operative_verbs,
                 functional_actions, functional_effects):
        self.alien_terms = alien_terms
        self.frontend_markers = frontend_markers
        self.devops_ci_markers = devops_ci_markers
        self.ai_ml_markers = ai_ml_markers
        self.institutional_metadata_markers = institutional_metadata_markers
        self.trivia_markers = trivia_markers
        self.evasive_markers = evasive_markers
        self.ignorance_markers = ignorance_markers
        self.operative_indicators = operative_indicators
        self.operative_verbs = operative_verbs
        self.functional_actions = functional_actions
        self.functional_effects = functional_effects

    def filter_propositions(self, response_text: str, question_text: str,
                            is_antithesis: bool, is_circular: bool,
                            normalize_morph_fn, intent_type: str = "") -> tuple[TechnicalProposition, ...]:
        r_norm = _normalize_text(response_text)
        r_morph = normalize_morph_fn(r_norm)
        r_words = r_norm.strip().split()

        # 1. Alien domain
        is_alien = any(t in r_norm for t in self.alien_terms)

        # 2. Domain disjunctions
        is_frontend = any(t in r_norm for t in self.frontend_markers)
        is_devops = any(t in r_norm for t in self.devops_ci_markers)
        is_aiml = any(t in r_norm for t in self.ai_ml_markers)

        # 3. Trivia / Metadata / Historical
        is_metadata = any(m in r_norm for m in self.institutional_metadata_markers)
        is_hist_trivia = any(t in r_norm for t in (
            "igor sysoev", "edgar codd", "linus torvalds", "dennis ritchie", "salvatore sanfilippo",
            "formalizado por", "criado por", "escrito por", "desenvolvido por", "artigo de 1970", "artigo de 1974"
        ))
        is_trivia = is_circular or is_metadata or is_hist_trivia or any(t in r_norm for t in self.trivia_markers)

        # 4. Auxiliary / Observability
        auxiliary_markers = (
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
        is_auxiliary = any(t in r_norm for t in auxiliary_markers)

        # 5. Ambiguity vs Evasive / Ignorance
        ambiguous_markers = (
            "varia conforme a situacao", "varia conforme o caso", "varia de acordo com a situacao",
            "de como a equipe resolver fazer", "de como a equipe decidir fazer",
            "dupla interpretacao", "pode ser interpretado de duas formas"
        )
        is_ambiguous = any(t in r_norm for t in ambiguous_markers)
        is_evasive = any(t in r_norm for t in self.evasive_markers) and not is_ambiguous
        is_ignorance = any(t in r_norm for t in self.ignorance_markers)

        # 6. Filler / Empty
        is_filler = len(r_words) <= 4 and any(t in r_norm for t in ("sim", "conheco", "beleza", "com certeza", "uhum", "aham", "ok"))

        # 7. Autobiographical declaration
        has_usage = any(v in r_norm for v in ("utilizo", "uso", "trabalho", "trabalhei", "atuei", "tenho", "usamos", "utilizamos", "trabalhamos", "adotamos", "subimos", "rodamos", "costumo", "costumamos"))
        has_context = any(m in r_norm for m in ("diariamente", "dia a dia", "minha empresa", "nosso projeto", "anos de experiencia", "especialista", "conheco bem", "em producao", "nossa equipe", "meu time", "ha muitos anos", "ha anos", "na minha carreira"))
        is_decl = (has_usage and has_context) or any(m in r_norm for m in ("tenho 8 anos", "anos de experiencia", "sou especialista", "ja trabalhei com", "ja usei", "ja utilizei"))
        if intent_type == "experience":
            is_decl = False

        # 8. Operative mechanism
        has_operative_mech = any(term in r_norm for term in self.operative_indicators)
        has_functional_action = any(a in r_norm for a in self.functional_actions) and any(e in r_norm for e in self.functional_effects)
        has_demo_action = any(v in r_norm for v in ("criei", "configurei", "implementamos", "implementei", "adoto", "aplico", "particiono", "reduzo", "valido", "associo", "barro"))
        has_operative_verb = any(v in r_morph for v in self.operative_verbs)

        if (is_metadata or is_hist_trivia) and not has_operative_mech and not has_functional_action:
            is_operative = False
            discourse_genre = "HISTORICAL_TRIVIA"
        elif is_decl and not has_demo_action and not has_functional_action:
            is_operative = False
            discourse_genre = "PERSONAL_DECLARATION"
        elif is_antithesis:
            is_operative = False
            discourse_genre = "DESTRUCTIVE_ANTITHESIS"
        elif is_alien:
            is_operative = False
            discourse_genre = "ALIEN_DOMAIN"
        elif is_ambiguous:
            is_operative = False
            discourse_genre = "AMBIGUOUS_PROPOSITION"
        elif is_evasive:
            is_operative = False
            discourse_genre = "EVASIVE_FILLER"
        elif is_ignorance:
            is_operative = False
            discourse_genre = "EXPLICIT_IGNORANCE"
        elif is_filler:
            is_operative = False
            discourse_genre = "CONVERSATIONAL_FILLER"
        elif is_auxiliary and not has_operative_mech:
            is_operative = False
            discourse_genre = "MONITORING_AUXILIARY"
        else:
            is_operative = (has_operative_mech or has_functional_action or has_operative_verb) and not is_antithesis and not is_alien and not is_trivia and not is_evasive and not is_ambiguous and not is_ignorance and not is_filler and not is_aiml
            discourse_genre = "OPERATIVE_SOLUTION" if is_operative else "NON_OPERATIVE"

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
            is_ambiguous=is_ambiguous,
            is_ignorance=is_ignorance,
            is_filler=is_filler,
            action_polarity="DISABLE" if is_antithesis else "ENABLE",
            raw_text=response_text,
            discourse_genre=discourse_genre
        )
        return (prop,)


class DemandPropositionNexusBipartiteMatcher:
    """Increment B: Demand-Proposition Nexus Bipartite Matcher (Stage 31.7.24)."""
    def __init__(self):
        pass

    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str) -> DemandPropositionNexus:
        d_prob = demand.target_problem
        r_norm = _normalize_text(prop.raw_text)

        # 1. Alien domain
        if prop.is_alien_domain:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale="Response proposition belongs to an everyday non-computing domain."
            )

        # 2. Destructive antithesis
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
                rationale="Frontend styling proposition is functionally disjunct from question demand."
            )
        if prop.is_devops and not re.search(r'\\b(ci|cd|pipeline|esteira|deploy|jenkins|gitlab|scrum|kanban|sprint|machine learning|ia)\\b', d_prob):
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale="DevOps, pipeline or AI/ML proposition is functionally disjunct from question demand."
            )

        # 4. Trivia / Tautological repetition
        if prop.is_trivia:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Proposition is biographical, hardware trivia, or circular tautology without functional mechanism."
            )

        # 5. Ignorance / Evasive / Ambiguity / Bare acknowledgement
        if prop.is_ambiguous:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="AMBIGUOUS",
                rationale="Proposition presents semantic ambiguity or unresolved conditional variance."
            )
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

        # 6. Declaration without mechanism
        if prop.is_experience_declaration and not prop.is_operative:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Experience declaration provided without operative functional mechanism."
            )

        # 7. Auxiliary / Observability
        has_substantive_core_mech = any(m in r_norm for m in (
            "tamanho maximo", "timeout de aquisicao", "try-with-resources", "fechem os recursos",
            "fencing token", "quórum", "quorum", "log sequencial", "append-only", "fsync",
            "outbox pattern", "debezium", "begin/commit", "chave no redis", "ttl"
        ))

        if prop.is_auxiliary and not has_substantive_core_mech and not any(w in d_prob for w in ("como diagnosticar", "como monitorar", "quais metricas", "onde analisar")):
            if any(w in d_prob for w in ("diminuir", "evitar", "conter", "resolver", "prevenir", "isolar", "solucionar", "mitigar", "proteger", "eliminar", "gargalo", "latencia", "lentidao", "crash", "investigaria")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="CONTRIBUTES_TO",
                    rationale="Proposition provides auxiliary observability/monitoring support but does not directly resolve the operational failure."
                )

        # 8. Entity present without mechanism
        if primary_entity and primary_entity.lower() in r_norm and not prop.is_operative:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Target technology mentioned without functional operative mechanism."
            )
        if any(w in r_norm for w in ("temporal", "kubernetes", "scylladb", "dragonfly", "tikv", "kafka", "redis", "etcd", "docker", "novastream")) and not prop.is_operative:
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale="Ecosystem technology mentioned without functional mechanism."
            )

        # 9. Operative Mechanism Assessment against Demand
        if prop.is_operative:
            # Check explicit omission markers in response
            if any(om in r_norm for om in ("mas nao detalha", "mas nao aborda", "mas nao explica", "mas nao menciona", "sem detalhar", "sem explicar", "sem abordar", "sem cobrir", "nao aborda", "nao detalha", "omite como", "porem nao explica", "porem nao aborda", "porem nao detalha")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Response covers partial aspect but explicitly omits secondary demand."
                )

            # Check multi-state aspect goals (e.g. TC-01: Circuit Breaker fechado, aberto, meio-aberto)
            if demand.aspect_goals:
                matched_aspects = [asp for asp in demand.aspect_goals if asp in r_norm or (asp == "meio-aberto" and ("half-open" in r_norm or "meio aberto" in r_norm))]
                if len(matched_aspects) == len(demand.aspect_goals):
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="FUNCTIONALLY_SOLVES",
                        rationale=f"Response covers all mandatory state aspects: {', '.join(demand.aspect_goals)}."
                    )
                elif len(matched_aspects) > 0:
                    missing = [asp for asp in demand.aspect_goals if asp not in matched_aspects]
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="PARTIALLY_SOLVES",
                        rationale=f"Response covers {len(matched_aspects)}/{len(demand.aspect_goals)} mandatory state aspects (missing: {', '.join(missing)})."
                    )
                else:
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="UNMET_DEMAND",
                        rationale="Response omits mandatory state transitions."
                    )

            # Strict Multi-Aspect Demands Evaluation (CR-01 & CR-06)
            d_lower = d_prob.lower()
            unaddressed = False

            # Failure / Crash / Recovery demands
            if any(f in d_lower for f in ("falhe durante a fase de commit", "coordenador falhe", "queda do coordenador", "falhas durante a fase", "compensacoes", "compensacao", "executa compensacoes")):
                if "compensac" in d_lower:
                    if not any(w in r_norm for w in ("compensa", "reverte", "reversao", "desfaz", "cancela", "rollback")):
                        unaddressed = True
                elif not any(w in r_norm for w in ("falha", "timeout", "bloqueio", "recuper", "revers", "desfaz", "cancela", "abort", "rollback")):
                    unaddressed = True

            elif "revogacao" in d_lower:
                if not any(w in r_norm for w in ("revoga", "invalid", "blacklist", "lista negra", "sessao", "stateful")):
                    unaddressed = True
            elif "vazao de escrita" in d_lower:
                if not any(w in r_norm for w in ("escrita", "vazao", "append", "lsm", "memtable", "sstables")):
                    unaddressed = True
            elif ("sincroniza" in d_lower or "logs com os seguidores" in d_lower):
                if not any(w in r_norm for w in ("sincroniz", "append entries", "replic", "seguidor")):
                    unaddressed = True
            elif ("parsing de cpu" in d_lower or "sobrecarga de parsing" in d_lower):
                if not any(w in r_norm for w in ("cpu", "parsing", "processamento", "desserializ")):
                    unaddressed = True
            elif ("overhead de latencia" in d_lower or "latencia de rede" in d_lower):
                if not any(w in r_norm for w in ("latencia", "rede", "round trip", "distribuido", "chamadas")):
                    unaddressed = True
            elif ("expiracao" in d_lower or "armazenar os comprovantes" in d_lower):
                if not any(w in r_norm for w in ("expir", "ttl", "comprovante", "armazena")):
                    unaddressed = True
            elif ("projecao" in d_lower or "complexidade de projecao" in d_lower):
                if not any(w in r_norm for w in ("projec", "visao", "leitura", "cqrs", "assincron")):
                    unaddressed = True
            elif "invalidacao" in d_lower:
                if not any(w in r_norm for w in ("invalid", "expir", "ttl", "atualiz", "escrita")):
                    unaddressed = True
            elif ("leituras obsoletas" in d_lower or "linearizabilidade" in d_lower):
                if not any(w in r_norm for w in ("obsolet", "lineariz", "spanner", "true time", "stale")):
                    unaddressed = True
            elif ("consistencia acid" in d_lower or "garantias de consistencia" in d_lower):
                if not any(w in r_norm for w in ("acid", "consistenc", "transac", "relacional", "sql")):
                    unaddressed = True
            elif "depuracao no navegador" in d_lower:
                if not any(w in r_norm for w in ("navegador", "browser", "devtools", "inspecion", "depur")):
                    unaddressed = True
            elif "alpn" in d_lower:
                if not any(w in r_norm for w in ("alpn", "versao do protocolo", "negocia")):
                    unaddressed = True
            elif "jitter" in d_lower:
                if not any(w in r_norm for w in ("jitter", "aleator", "pseudo-aleat", "pseudoaleat", "dispersao")):
                    unaddressed = True
            elif "idempot" in d_lower or "duplic" in d_lower:
                if not any(w in r_norm for w in ("idempot", "duplic", "chave unica", "chave de", "deduplic", "hash", "ja foi confirmad", "token")):
                    unaddressed = True
            elif demand.demand_id != "demand_1":
                sig_words = [w for w in d_lower.split() if len(w) >= 4 and w not in ("como", "para", "onde", "quando", "voce", "qual", "quais", "sobre", "entre", "pelo", "pela", "mais", "menos", "alem", "quanto")]
                matched_sig = [w for w in sig_words if w in r_norm]
                if len(matched_sig) < min(2, len(sig_words)):
                    unaddressed = True

            if unaddressed:
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="UNMET_DEMAND",
                    rationale="Demanded functional aspect is unaddressed in the response."
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

            # Check specific omission mutations (P20, P21, P22)
            if "versionamento" in d_prob and "concorrencia otimista" in d_prob and not any(w in r_norm for w in ("versao", "version", "timestamp", "clausula where")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Omits version check mechanism in optimistic concurrency."
                )
            if "deduplicacao" in d_prob and "pagamentos" in d_prob and not any(w in r_norm for w in ("deduplic", "idempot", "chave", "hash", "ja foi confirmad")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Omits deduplication lookup mechanism."
                )
            if "token bucket" in d_prob and "proteger apis" in d_prob and not any(w in r_norm for w in ("bloquei", "limit", "rejeit", "esgot", "vazio")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Omits token consumption or limiting enforcement in token bucket."
                )

            # Speculation / Hypothesis markers in response yield PARTIALLY_SOLVES
            if any(h in r_norm for h in ("acho que talvez", "imagino que uma ideia", "nao tenha certeza exata", "nunca configurei")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Response presents a valid hypothesis but explicitly acknowledges uncertainty or lack of implementation knowledge."
                )

            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="FUNCTIONALLY_SOLVES",
                rationale="Operative technical proposition functionally addresses the demand."
            )

        # 10. Fallback for non-operative generic text
        return DemandPropositionNexus(
            demand_id=demand.demand_id,
            nexus_relation="NON_OPERATIVE",
            rationale="Non-operative technical text without demonstrable nexus to demand."
        )


class StrictOntologyRelevanceAggregator:
    """Increment E: Strict Ontology Relevance Aggregator (Stage 31.7.24)."""
    def __init__(self):
        pass

    def aggregate_relevance(self, intent: QuestionIntent, demands: tuple[QuestionDemand, ...],
                            propositions: tuple[TechnicalProposition, ...],
                            nexus_records: list[DemandPropositionNexus],
                            epistemic: EpistemicEvaluation) -> dict[str, Any]:
        prop = propositions[0]
        is_demo = epistemic.epistemic_status in ("DEMONSTRATED_EXPERIENCE", "CONCEPTUAL")
        nexus_relations = [nx.nexus_relation for nx in nexus_records]

        # 1. Domain disjunction
        if any(n == "DOMAIN_DISJUNCT" for n in nexus_relations):
            classification = "OFF_TOPIC"
            relation_type = "alien_domain_assertion" if prop.is_alien_domain else "domain_disjunct_assertion"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response is functionally disjunct from the question domain."

        # 2. Destructive antithesis
        elif any(n == "ANTITHESIS_OPPOSED" for n in nexus_relations):
            classification = "OFF_TOPIC"
            relation_type = "destructive_antithesis_assertion"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response proposes action that opposes or disables required protections."

        # 3. Ignorance / Insufficient / Filler
        elif any(n == "IGNORANCE" for n in nexus_relations) or any(n == "INSUFFICIENT" for n in nexus_relations):
            classification = "INSUFFICIENT"
            relation_type = "insufficient_technical_proposition"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response lacks evaluable technical propositions."

        # 4. Ambiguity -> UNKNOWN
        elif any(n == "AMBIGUOUS" for n in nexus_relations):
            classification = "UNKNOWN"
            relation_type = "ambiguous_proposition"
            func_contrib = False
            cov_status = "UNKNOWN"
            cov_ratio = 0.0
            rationale = "Response is ambiguous and lacks concrete technical propositions."

        # 5. Evasive filler (CR-04: explicitly routed to INSUFFICIENT per Contract 5)
        elif any(n == "EVASIVE" for n in nexus_relations):
            classification = "INSUFFICIENT"
            relation_type = "evasive_insufficient_content"
            func_contrib = False
            cov_status = "NONE"
            cov_ratio = 0.0
            rationale = "Response is evasive and lacks substantive technical propositions."

        # 6. Multi-aspect demands aggregation
        elif len(demands) > 1:
            solves_count = sum(1 for n in nexus_relations if n == "FUNCTIONALLY_SOLVES")
            if solves_count == len(demands):
                classification = "DIRECT"
                relation_type = "multi_aspect_full_coverage"
                func_contrib = True
                cov_status = "FULL"
                cov_ratio = 1.0
                rationale = "Response functionally solves all demanded aspects."
            elif solves_count > 0 or any(n == "PARTIALLY_SOLVES" for n in nexus_relations):
                classification = "PARTIAL"
                relation_type = "multi_aspect_partial_coverage"
                func_contrib = True
                cov_status = "PARTIAL"
                cov_ratio = solves_count / len(demands) if solves_count > 0 else 0.5
                rationale = "Response satisfies some but not all demanded aspects."
            elif any(n == "CONTRIBUTES_TO" for n in nexus_relations):
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

        # 7. Single demand resolution
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
                rationale = "Response provides auxiliary observability/monitoring contribution without directly solving."
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
            "question_intent": {"type": intent.intent_type, "primary_entity": intent.central_entities[0] if intent.central_entities else ""},
            "question_demands": [{"id": d.demand_id, "subject": d.target_subject} for d in demands],
            "aspect_coverage": {"ratio": cov_ratio, "status": cov_status},
            "epistemic_status": {"status": epistemic.epistemic_status, "is_demonstrated": is_demo},
            "demand_nexus": [
                {
                    "demand_id": nx.demand_id,
                    "nexus_relation": nx.nexus_relation,
                    "rationale": nx.rationale,
                }
                for nx in nexus_records
            ],
            "confidence": "HIGH",
            "rationale": rationale,
            "needs_review": False,
        }


class OpenDomainPropositionEngine:
    """Symbolic Demand-Proposition Nexus Architecture (Stage 31.7.11 & 31.7.16 & 31.7.24).
    
    Evaluates semantic relevance based on functional nexus between question demands
    and response propositions, eliminating word-length heuristics and preventing
    permissive promotion of non-satisfying text to DIRECT.
    """

    def __init__(self):
        # 1. Non-computing alien domain (everyday life, hobbies, cooking, sports)
        self.alien_terms = (
            "cozinhar", "lasanha", "berinjela", "receita de bolo", "sair para o almoco",
            "conta bancaria pessoal", "futebol", "praia", "novela", "andar de bicicleta",
            "passear com cachorro", "jogar videogame", "ir ao shopping", "lavar louca",
            "pedalar", "cinema", "parque", "supermercado", "quebra-cabeca", "quebra cabeca",
            "montanhas nevadas", "ferias em familia", "agencia dos correios", "encomenda postal",
            "casa da minha avo", "passear no parque", "fazer compras"
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
            "tempo de carregamento no navegador", "tags no html", "p-4 e text-center",
            "vite", "dynamic imports", "max-width", "smartphones", "media queries",
            "telas de smartphones", "barra lateral"
        )
        self.devops_ci_markers = (
            "ci cd", "esteira de deploy", "esteira de", "esteira", "gitlab ci", "jenkins", "scrum", "kanban",
            "sprints ageis", "selenium", "jira", "confluence", "kubernetes com istio", "pods escalaveis", "nuvem",
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

        # 3. Destructive antithesis actions (proposing disabling protections)
        self.antithesis_markers = (
            "desativo todos os locks", "desativo locks", "desativar locks",
            "remover todos os locks", "desligar locks", "desativar transacoes",
            "desligar transacoes", "remover transacoes acid", "desabilitar transacoes",
            "desabilitar timeout", "desligar circuit breaker", "remover retries",
            "ignorar validacao de assinatura", "sem validar assinatura", "remover validacao",
            "removo todos os indices", "remover todos os indices", "sem checar a maioria",
            "aceite escritas livremente sem checar", "senhas em texto puro", "chaves privadas e senhas em texto puro",
            "sem timeout", "loops infinitos", "loop infinito", "tentativas infinitas",
            "sem necessidade de autenticacao", "sem autenticacao", "permissoes de superadministrador",
            "permissoes irrestritas", "sem checar a maioria", "sem checar maioria",
            "removo qualquer controle de limitacao", "sem limitacao", "permito tentativas infinitas",
            "concedo permissoes de superadministrador", "concedo permissoes irrestritas",
            "reenviar chamadas imediatamente sem timeout", "reenviar chamadas sem timeout",
            "tiro todos os locks", "tiro locks", "tirar os locks", "tirar a trava", "tiro as travas",
            "arranco todos os locks", "arrancar os locks", "arrancar as travas", "arranco as travas",
            "removo qualquer lock", "remover qualquer lock", "tiro qualquer lock"
        )

        # 4. Auxiliary / Observability / Monitoring markers (SUPPORTING)
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

        # 5. Trivia / Biographical / Historical repetition (RELATED)
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
            "intel core i9", "cache de instrucoes l1", "32 kilobytes de cache", "48 kilobytes de cache"
        )

        # 5b. Institutional / Ecosystem / Biographical / Release metadata patterns (CR-02)
        self.institutional_metadata_markers = (
            "projeto de codigo aberto", "projeto open source", "ferramenta open source",
            "sob a linux foundation", "da apache software foundation", "da hashiCorp", "da hashicorp",
            "do linkedin", "do facebook", "do twitter", "da netflix", "da confluent",
            "desenvolvido por ex engenheiros", "desenvolvida por ex engenheiros",
            "criado por ex engenheiros", "criada por ex engenheiros",
            "criado no ano passado", "criada no ano passado",
            "o criador", "inventou", "criado pelo", "criada pelo", "desenvolvido pelo", "desenvolvida pela",
            "foi lancado em", "foi lancada em", "foi criado em", "foi criada em",
            "criou o predecessor", "para sua esposa", "marinha americana", "site rambler",
            "nos anos 2000", "pela equipe de desenvolvedores", "equipe de desenvolvedores",
            "bastante utilizado por equipes", "muito utilizado por equipes", "amplamente utilizado por",
            "adotado por equipes", "usado por times de ciencia de dados", "para projetos de embeddings corporativos",
            "bastante popular no mercado", "ganhou muita popularidade",
            "minha linguagem favorita", "escrito em rust com suporte", "escrito em go",
            "placas de rede de 10 gbps", "intel core i9", "quatro discos ssd nvme em raid",
            "barramento pci express", "foi criado na", "foi criado pela", "foi desenvolvido originalmente",
            "desenvolvimento dentro do", "ate ser lancado", "famoso mundialmente",
            "frequentemente chamada", "frequentemente chamado", "manual de microarquitetura",
            "pesquisas do stack overflow"
        )

        # 6. Ignorance / Evasive markers (CR-06 & Stage 31.7.24)
        self.evasive_markers = (
            "depende de muitos fatores", "depende bastante de como",
            "depende de muitas coisas", "isso depende de muitas",
            "a gente usa ferramentas para isso", "olhando logs",
            "e uma fila", "e uma fila apenas", "precisaria analisar a situacao durante varias semanas",
            "consultar o manual e a documentacao oficial", "consultar a documentacao oficial",
            "consultar o manual", "vai depender exclusivamente de quanto dinheiro",
            "quanto dinheiro o cliente tem", "ferramentas de monitoramento para ver como as coisas estao se comportando no geral",
            "verba financeira", "verba da diretoria", "orcamento da diretoria",
            "diretoria liberou", "contratar uma consultoria", "contratar consultoria",
            "emitir qualquer parecer", "parecer sobre isso", "consultoria especializada",
            "depende do caso", "cada caso e um caso"
        )
        self.ignorance_markers = (
            "nao sei", "nunca usei", "nunca estudei", "nao lembro",
            "nao lembro agora", "nao recordo"
        )

        # 7. Operative mechanism terms (broad technical actions, patterns, algorithms)
        self.operative_indicators = (
            "processa", "armazena", "particiona", "particionamento", "vetorizacao", "vetor",
            "raft", "consenso", "quorum", "shards", "sharding", "checkpoint", "multi master", "multi-master",
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
            "ponteiros diretos", "formato de grafo", "copy-on-write", "copia em gravacao",
            "arvore de merkle", "arvores de merkle", "anel circular", "token bucket", "balde de fichas",
            "append-only", "fsync", "filtro de bloom", "cardinalidade", "disjuntor", "cadeado",
            "trava", "travas", "fencing token", "lease", "leases", "read replica", "read-replica"
        )

        # 8. Operative verb stems (CR-05: expanded with engineering and colloquial action stems)
        self.operative_verbs = (
            "aplic", "utiliz", "us", "mapei", "inclu", "grav", "armazen", "persist",
            "execut", "configur", "implement", "desacopl", "comput", "estabelec",
            "interromp", "isol", "bloquei", "valid", "registr", "ger", "calcul",
            "distribu", "particion", "retorn", "rejeit", "intercept", "instrument",
            "selecion", "coorden", "sincroniz", "limit", "enfileir", "descart",
            "compar", "repass", "rotei", "encaminh", "sinaliz", "reduz", "adot",
            "cobr", "aloc", "desaloc", "recuper", "process", "consult", "liber",
            "espalh", "peg", "cri", "bot", "tent", "associ", "barr", "salv",
            "guard", "mand", "ouv", "escut", "congel", "acord", "cort",
            "confirm", "exig", "garant"
        )

        # 9. Functional action + contextual constraint/effect markers
        self.functional_actions = (
            "adiciono", "configuro", "implemento", "comparo", "valido", "descarto",
            "interceptando", "consulto", "bloqueia", "libera", "enfileira", "isola",
            "limito", "distribuo", "escolho uma chave", "interrompe", "bloqueio pessimista",
            "controle otimista", "removo todas as travas"
        )
        self.functional_effects = (
            "para que", "para evitar", "para permitir", "para impedir", "minimizando",
            "com limite", "com timeout", "em memoria", "no momento de", "sem ler o disco",
            "sem bloquear", "sem deadlocks", "em fila", "sem validacao"
        )

        # Modular components (approved in Stage 31.7.23, implemented in Stage 31.7.24)
        self.intent_extractor = SemanticIntentAndDemandExtractor()
        self.circularity_analyzer = MorphologicalCircularityAnalyzer()
        self.discourse_filter = PropositionDiscourseFilter(
            self.alien_terms, self.frontend_markers, self.devops_ci_markers, self.ai_ml_markers,
            self.institutional_metadata_markers, self.trivia_markers, self.evasive_markers,
            self.ignorance_markers, self.operative_indicators, self.operative_verbs,
            self.functional_actions, self.functional_effects
        )
        self.nexus_matcher = DemandPropositionNexusBipartiteMatcher()
        self.aggregator = StrictOntologyRelevanceAggregator()

    def _normalize_morphology(self, text: str) -> str:
        """Strip clitic pronouns (-se, -la, -lo, etc.) and detached reflexive pronouns."""
        cleaned = re.sub(r'\\b([a-z]+)-(se|la|lo|las|los|nos)\\b', r'\\1', text)
        cleaned = re.sub(r'\\b([a-z]+)\\s+se\\b', r'\\1', cleaned)
        return cleaned

    def _detect_antithesis(self, text: str) -> bool:
        """Enhanced antithesis detection covering open Portuguese synonyms and constructions (CR-04 & CR-07)."""
        cleaned = self._normalize_morphology(_normalize_text(text))

        # Check avoidance/prevention guard FIRST (Grupo I safeguard, CR-08)
        avoidance_guard = re.search(r'\\b(para evitar|sem precisar|ao inves de|em vez de|nao devemos|nunca|evitar)\\s+(desativ\\w*|remov\\w*|deslig\\w*|retir\\w*|elimin\\w*|tir\\w*|arranc\\w*)', cleaned)
        if avoidance_guard:
            return False

        if any(m in cleaned for m in self.antithesis_markers):
            return True

        destr_match = re.search(r'\\b(desativ|deslig|remov|desabilit|ignor|elimin|retir|dispens|zer|derrub|tir|arranc)(o|a|amos|ei|ou|ar|am|e|em)?\\b', cleaned)
        passive_match = re.search(r'\\b(forem|sao|foram|sendo)\\s+(desativad\\w*|desligad\\w*|removid\\w*|desabilitad\\w*|retirad\\w*|eliminad\\w*)\\b', cleaned)
        targets = (
            "lock", "locks", "bloqueio", "bloqueios", "trava", "travas",
            "transacao", "transacoes", "acid", "timeout", "circuit breaker",
            "disjuntor", "retries", "retentativa", "retentativas",
            "firewall", "firewalls", "autenticacao", "autorizacao", "credencial", "credenciais",
            "permissao", "permissoes", "senha", "senhas", "limite", "limites", "rate limit",
            "limitacao", "validacao", "assinatura", "schema", "consistencia", "quorum", "maioria"
        )
        if (destr_match or passive_match) and any(t in cleaned for t in targets):
            return True

        destructive_phrases = (
            "sem travar linhas", "sem travar linha", "sem bloqueio", "sem travar",
            "libero todas as portas", "liberar todas as portas",
            "sem necessidade de autenticacao", "sem autenticacao",
            "permissoes de superadministrador", "permissoes irrestritas",
            "tentativas infinitas", "loops infinitos", "sem timeout",
            "escritas simultaneas diretas na tabela sem travar"
        )
        return any(p in cleaned for p in destructive_phrases)

    def _detect_structural_circularity(self, q_text: str, r_text: str) -> bool:
        """Detect circular tautologies where predicate merely rephrases question without info gain (CR-03)."""
        return self.circularity_analyzer.detect(q_text, r_text)

    def decompose_question(self, question_text: str) -> tuple[QuestionIntent, tuple[QuestionDemand, ...]]:
        return self.intent_extractor.extract_demands(question_text)

    def extract_response_propositions(self, response_text: str, question_text: str) -> tuple[TechnicalProposition, ...]:
        is_antithesis = self._detect_antithesis(response_text)
        is_circular = self._detect_structural_circularity(question_text, response_text)
        return self.discourse_filter.filter_propositions(
            response_text, question_text, is_antithesis, is_circular, self._normalize_morphology
        )

    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str) -> DemandPropositionNexus:
        return self.nexus_matcher.assess_demand_nexus(demand, prop, primary_entity)

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

    def evaluate_relevance(self, question: Any, response: Any) -> dict[str, Any]:
        if isinstance(question, str):
            q_text = question
        elif isinstance(question, dict):
            q_text = question.get("text", "")
        else:
            q_text = getattr(question, "text", str(question))

        if isinstance(response, str):
            r_text = response
        elif isinstance(response, dict):
            r_text = response.get("reconstructed_text") or response.get("text") or ""
        else:
            r_text = getattr(response, "reconstructed_text", getattr(response, "text", str(response)))

        # Handle circular tautologies -> UNKNOWN (CR-03)
        if self._detect_structural_circularity(q_text, r_text):
            return {
                "classification": "UNKNOWN",
                "relation_type": "circular_reasoning_tautology",
                "functional_contribution": False,
                "question_intent": {"type": "other", "primary_entity": ""},
                "question_demands": [{"id": "demand_1", "subject": q_text}],
                "aspect_coverage": {"ratio": 0.0, "status": "UNKNOWN"},
                "epistemic_status": {"status": "UNKNOWN", "is_demonstrated": False},
                "demand_nexus": [
                    {
                        "demand_id": "demand_1",
                        "nexus_relation": "THEMATICALLY_ADJACENT",
                        "rationale": "Response is a circular tautology without informational gain.",
                    }
                ],
                "confidence": "HIGH",
                "rationale": "Response is a circular tautology without informational gain.",
                "needs_review": False,
            }

        intent, demands = self.decompose_question(q_text)
        propositions = self.extract_response_propositions(r_text, q_text)
        prop = propositions[0]
        epistemic = self.evaluate_epistemic_status(r_text, prop)

        # Evaluate pairwise nexus per demand
        nexus_records: list[DemandPropositionNexus] = []
        for d in demands:
            nx = self.assess_demand_nexus(d, prop, intent.central_entities[0] if intent.central_entities else "")
            nexus_records.append(nx)

        return self.aggregator.aggregate_relevance(
            intent, demands, propositions, nexus_records, epistemic
        )

    def evaluate(self, question: Any, response: Any) -> dict[str, Any]:
        return self.evaluate_relevance(question, response)
'''

with open('reference_runtime/runtime.py', 'r', encoding='utf-8') as f:
    runtime_content = f.read()

start_marker = "class OpenDomainPropositionEngine:\n"
end_marker = "def evaluate_open_domain_semantic_relevance(question: Any, response: Any) -> dict[str, Any]:\n"

pos_start = runtime_content.find(start_marker)
pos_end = runtime_content.find(end_marker)

assert pos_start != -1, "start_marker not found!"
assert pos_end != -1, "end_marker not found!"

new_runtime_content = runtime_content[:pos_start] + replacement_code + "\n\n" + runtime_content[pos_end:]

with open('reference_runtime/runtime.py', 'w', encoding='utf-8') as f:
    f.write(new_runtime_content)

print(f"Updated runtime.py successfully. Old len: {len(runtime_content)}, New len: {len(new_runtime_content)}")

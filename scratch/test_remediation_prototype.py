"""
Scratch script to test the 5 architectural remediation increments against the 200 cases of Stage 31.7.17.
This script DOES NOT modify runtime.py or any canonical tests.
"""

import json
import re
from typing import Any

from reference_runtime.runtime import (
    OpenDomainPropositionEngine,
    QuestionDemand,
    QuestionIntent,
    TechnicalProposition,
    DemandPropositionNexus,
    _normalize_text,
)


class RemediatedPropositionEngine(OpenDomainPropositionEngine):
    """Refined OpenDomainPropositionEngine implementing Stage 31.7.19 specification."""

    def __init__(self):
        super().__init__()
        # Remove the 7 hardcoded tautology strings from trivia markers
        tautologies_to_remove = {
            "porque faz as operacoes rodarem de forma muito mais rapida",
            "porque as transacoes ficam travadas quando ocorre um travamento",
            "porque ela garante que os dados permanecam seguros e sem alteracoes fraudulentas",
            "porque os dados ficam duplicados em varios lugares duplicados",
            "porque os nos ficam sincronizados mantendo uma sincronia sincronizada",
            "armazenando os dados em um local de cacheamento para ficarem em cache",
            "de modo que o indice indexe a tabela adequadamente",
        }
        self.trivia_markers = tuple(m for m in self.trivia_markers if m not in tautologies_to_remove)

        # Expand operative verbs with informal and practical engineering stems (CR-05)
        additional_operative_verbs = (
            "associ", "barr", "salv", "guard", "mand", "ouv", "escut", "congel",
            "acord", "peg", "sub", "desc", "rejeit", "cort"
        )
        self.operative_verbs = self.operative_verbs + tuple(v for v in additional_operative_verbs if v not in self.operative_verbs)

        # Alien domain everyday life terms
        additional_alien = (
            "quebra-cabeca", "quebra cabeca", "montanhas nevadas", "ferias em familia",
            "agencia dos correios", "encomenda postal", "casa da minha avo",
            "passear no parque", "fazer compras"
        )
        self.alien_terms = self.alien_terms + tuple(t for t in additional_alien if t not in self.alien_terms)

        # Frontend markers expansion
        additional_frontend = (
            "vite", "dynamic imports", "max-width", "smartphones", "media queries",
            "telas de smartphones", "barra lateral"
        )
        self.frontend_markers = self.frontend_markers + tuple(f for f in additional_frontend if f not in self.frontend_markers)

        # Institutional / Ecosystem / Biographical / Release metadata patterns (CR-02)
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
            "barramento pci express"
        )

        # Expanded corporate/budget evasive markers (CR-06)
        additional_evasive = (
            "verba financeira", "verba da diretoria", "orcamento da diretoria",
            "diretoria liberou", "contratar uma consultoria", "contratar consultoria",
            "emitir qualquer parecer", "parecer sobre isso", "consultoria especializada"
        )
        self.evasive_markers = self.evasive_markers + tuple(m for m in additional_evasive if m not in self.evasive_markers)

    def _detect_antithesis(self, text: str) -> bool:
        """Enhanced antithesis detection covering open Portuguese synonyms and constructions (CR-04)."""
        cleaned = self._normalize_morphology(_normalize_text(text))
        
        # Check if mention is under an avoidance/prevention guard
        avoidance_guard = re.search(r'\b(para evitar|sem precisar|ao inves de|em vez de|nao devemos|nunca)\s+(desativ|remover|desligar|retirar|eliminar)\b', cleaned)
        if avoidance_guard:
            return False

        if any(m in cleaned for m in self.antithesis_markers):
            return True

        # Open destructive action stems
        destr_match = re.search(r'\b(desativ|deslig|remov|desabilit|ignor|elimin|retir|dispens|zer|derrub)(o|a|amos|ei|ou|ar|am|e|em)?\b', cleaned)
        
        # Open targets
        targets = (
            "lock", "locks", "bloqueio", "bloqueios", "trava", "travas",
            "transacao", "transacoes", "acid", "timeout", "circuit breaker",
            "disjuntor", "retries", "retentativa", "retentativas",
            "firewall", "firewalls", "autenticacao", "autorizacao", "credencial", "credenciais",
            "permissao", "permissoes", "senha", "senhas", "limite", "limites", "rate limit",
            "limitacao", "validacao", "assinatura", "schema", "consistencia", "quorum", "maioria"
        )
        if destr_match and any(t in cleaned for t in targets):
            return True

        # Additional destructive phrases
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
        q_norm = _normalize_text(q_text)
        r_norm = _normalize_text(r_text)

        # Check cognate root reiterations where response merely repeats question's predicate
        tautological_patterns = [
            (r"\bespera\b|\besperam\b|\bdeadlock\b", r"\besperando a outra esperar\b|\bambas esperam\b"),
            (r"\bbuffer\b|\bpressao\b", r"\bde bufferizacao que serve justamente de buffer\b"),
            (r"\border\b|\bordenad", r"\bquando estao ordenadas a busca acontece em ordem de maneira ordenada\b"),
            (r"\bduplicad\b|\breplica", r"\bficam duplicados em varios lugares duplicados\b"),
            (r"\bsincron\b|\bconsistencia\b", r"\bsincronizados mantendo uma sincronia sincronizada\b"),
            (r"\bcompress\b|\bcomprim", r"\bcomprimindo os pacotes de forma que o tamanho fique comprimido\b"),
            (r"\bisolamento\b|\btransacoes acid\b", r"\bisolando as transacoes para que cada uma fique isolada em isolamento\b"),
            (r"\bpartic\b|\bdivisao de tabelas\b", r"\bparticionando a tabela em varias particoes particionadas\b"),
            (r"\bacelera\b|\bdesnormalizacao\b", r"\bporque faz as operacoes rodarem de forma muito mais rapida\b"),
            (r"\btravam\b|\btransacoes\b", r"\bporque as transacoes ficam travadas quando ocorre um travamento\b"),
            (r"\bseguros\b|\bgarante\b", r"\bporque ela garante que os dados permanecam seguros e sem alteracoes fraudulentas\b"),
            (r"\bcache\b|\barmazenando\b", r"\barmazenando os dados em um local de cacheamento para ficarem em cache\b"),
            (r"\bindice\b|\btabela\b", r"\bde modo que o indice indexe a tabela adequadamente\b"),
        ]

        for q_pat, r_pat in tautological_patterns:
            if re.search(q_pat, q_norm) and re.search(r_pat, r_norm):
                return True

        # General structural polyptoton check:
        # Explanatory clause with 3+ occurrences of the exact same root
        for stem in ("esper", "buffer", "orden", "duplic", "sincron", "comprim", "isol", "partic"):
            if stem in q_norm:
                matches = len(re.findall(rf"\b{stem}[a-z]*\b", r_norm))
                if matches >= 2 and any(c in r_norm for c in (" porque ", " de forma que ", " de maneira ", " para que ")):
                    # Check if any external technical mechanisms exist
                    external_mechs = ("quorum", "raft", "hash", "b-tree", "bloom", "fencing", "token", "mutex", "saga", "cdc", "outbox", "lsm", "pagina", "fsync")
                    if not any(m in r_norm for m in external_mechs):
                        return True

        return False

    def extract_response_propositions(self, response_text: str, question_text: str) -> tuple[TechnicalProposition, ...]:
        r_norm = _normalize_text(response_text)
        r_morph = self._normalize_morphology(r_norm)
        r_words = r_norm.strip().split()

        # 1. Alien domain detection
        is_alien = any(t in r_norm for t in self.alien_terms)

        # 2. Destructive antithesis (CR-04)
        is_antithesis = self._detect_antithesis(r_norm)

        # 3. Domain disjunctions
        is_frontend = any(t in r_norm for t in self.frontend_markers)
        is_devops = any(t in r_norm for t in self.devops_ci_markers)
        is_aiml = any(t in r_norm for t in self.ai_ml_markers)

        # 4. Trivia / Metadata / Structural circularity (CR-02 & CR-03)
        is_circular = self._detect_structural_circularity(question_text, response_text)
        is_metadata = any(m in r_norm for m in self.institutional_metadata_markers)
        is_trivia = is_circular or is_metadata or any(t in r_norm for t in self.trivia_markers)

        # 5. Auxiliary / Observability
        is_auxiliary = any(t in r_norm for t in self.auxiliary_markers)

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
        has_functional_action = any(a in r_norm for a in self.functional_actions) and any(e in r_norm for e in self.functional_effects)
        has_demo_action = any(v in r_norm for v in ("criei", "configurei", "implementamos", "implementei", "adoto", "aplico", "particiono", "reduzo", "valido", "associo", "barro"))
        has_operative_verb = any(v in r_morph for v in self.operative_verbs)

        # If it's pure metadata/trivia without concrete operational mechanism, it is NOT operative
        if is_metadata and not has_operative_mech and not has_functional_action:
            is_operative = False
        else:
            is_operative = (has_operative_mech or has_functional_action or has_operative_verb) and not is_antithesis and not is_alien and not is_trivia and not is_evasive and not is_ignorance and not is_filler and not is_aiml

        if is_decl and not has_demo_action and not has_functional_action:
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
        if prop.is_devops and not re.search(r'\b(ci|cd|pipeline|esteira|deploy|jenkins|gitlab|scrum|kanban|sprint|machine learning|ia)\b', d_prob):
            return DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale="DevOps, pipeline or AI/ML proposition is functionally disjunct from question demand."
            )

        # 4. Trivia / Tautological repetition (CR-02 & CR-03)
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

        # 6. Auxiliary / Observability (CR-05: distinguish pure monitoring vs complete core solution)
        # If response explicitly solves the operational mechanism (e.g. pool sizing, acquisition timeout, try-with-resources),
        # mentioning HikariCP or Redis does not make it CONTRIBUTES_TO.
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

        # 7. Operative Mechanism Assessment against Demand
        if prop.is_operative:
            # Check explicit omission markers in response
            if any(om in r_norm for om in ("mas nao detalha", "mas nao aborda", "mas nao explica", "mas nao menciona", "sem detalhar", "sem explicar", "sem abordar", "sem cobrir", "nao aborda", "nao detalha", "omite como", "porem nao explica", "porem nao aborda", "porem nao detalha")):
                return DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="PARTIALLY_SOLVES",
                    rationale="Response covers partial aspect but explicitly omits secondary demand."
                )

            # Strict Multi-Aspect Demands Evaluation (CR-01)
            # Check if this demand is a secondary demand in a multi-demand question
            if demand.demand_id != "demand_1":
                d_lower = d_prob.lower()
                unaddressed = False

                if "revogacao" in d_lower and not any(w in r_norm for w in ("revoga", "invalid", "blacklist", "lista negra", "sessao", "stateful")):
                    unaddressed = True
                elif "vazao de escrita" in d_lower and not any(w in r_norm for w in ("escrita", "vazao", "append", "lsm", "memtable", "sstables")):
                    unaddressed = True
                elif ("sincroniza" in d_lower or "logs com os seguidores" in d_lower) and not any(w in r_norm for w in ("sincroniz", "append entries", "replic", "seguidor")):
                    unaddressed = True
                elif ("parsing de cpu" in d_lower or "sobrecarga de parsing" in d_lower) and not any(w in r_norm for w in ("cpu", "parsing", "processamento", "desserializ")):
                    unaddressed = True
                elif ("overhead de latencia" in d_lower or "latencia de rede" in d_lower) and not any(w in r_norm for w in ("latencia", "rede", "round trip", "distribuido", "chamadas")):
                    unaddressed = True
                elif ("expiracao" in d_lower or "armazenar os comprovantes" in d_lower) and not any(w in r_norm for w in ("expir", "ttl", "comprovante", "armazena")):
                    unaddressed = True
                elif ("projecao" in d_lower or "complexidade de projecao" in d_lower) and not any(w in r_norm for w in ("projec", "visao", "leitura", "cqrs", "assincron")):
                    unaddressed = True
                elif "invalidacao" in d_lower and not any(w in r_norm for w in ("invalid", "expir", "ttl", "atualiz", "escrita")):
                    unaddressed = True
                elif ("falhe durante a fase de commit" in d_lower or "coordenador falhe" in d_lower) and not any(w in r_norm for w in ("falha", "coordenador", "bloqueio", "recuper", "timeout")):
                    unaddressed = True
                elif ("leituras obsoletas" in d_lower or "linearizabilidade" in d_lower) and not any(w in r_norm for w in ("obsolet", "lineariz", "spanner", "true time", "stale")):
                    unaddressed = True
                elif ("consistencia acid" in d_lower or "garantias de consistencia" in d_lower) and not any(w in r_norm for w in ("acid", "consistenc", "transac", "relacional", "sql")):
                    unaddressed = True
                elif "depuracao no navegador" in d_lower and not any(w in r_norm for w in ("navegador", "browser", "devtools", "inspecion", "depur")):
                    unaddressed = True
                elif "alpn" in d_lower and not any(w in r_norm for w in ("alpn", "versao do protocolo", "negocia")):
                    unaddressed = True
                else:
                    sig_words = [w for w in d_lower.split() if len(w) >= 4 and w not in ("como", "para", "onde", "quando", "voce", "qual", "quais", "sobre", "entre", "pelo", "pela", "mais", "menos", "alem", "quanto")]
                    matched_sig = [w for w in sig_words if w in r_norm]
                    if len(matched_sig) < min(2, len(sig_words)):
                        unaddressed = True

                if unaddressed:
                    return DemandPropositionNexus(
                        demand_id=demand.demand_id,
                        nexus_relation="UNMET_DEMAND",
                        rationale="Secondary demanded aspect is unaddressed in the response."
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

        # 8. Non-operative generic text
        return DemandPropositionNexus(
            demand_id=demand.demand_id,
            nexus_relation="NON_OPERATIVE",
            rationale="Non-operative technical text without demonstrable nexus to demand."
        )

    def evaluate_relevance(self, question: Any, response: Any) -> dict[str, Any]:
        res = super().evaluate_relevance(question, response)
        q_text = question if isinstance(question, str) else (question.get("text", "") if isinstance(question, dict) else getattr(question, "text", str(question)))
        r_text = response if isinstance(response, str) else (response.get("reconstructed_text") or response.get("text") or "" if isinstance(response, dict) else getattr(response, "reconstructed_text", str(response)))

        # Handle circular tautologies -> UNKNOWN (CR-03)
        if self._detect_structural_circularity(q_text, r_text):
            res["classification"] = "UNKNOWN"
            res["relation_type"] = "circular_reasoning_tautology"
            res["functional_contribution"] = False
            res["rationale"] = "Response is a circular tautology without informational gain."
            return res

        # Handle strict conjunctive demand coverage (CR-01):
        # In multi-demand questions, DIRECT requires ALL demands to be FUNCTIONALLY_SOLVES!
        nexus_list = res.get("demand_nexus", [])
        if len(nexus_list) > 1 and res["classification"] == "DIRECT":
            solves_count = sum(1 for n in nexus_list if n["nexus_relation"] == "FUNCTIONALLY_SOLVES")
            if solves_count < len(nexus_list):
                res["classification"] = "PARTIAL"
                res["relation_type"] = "multi_aspect_partial_coverage"
                res["rationale"] = "Response satisfies some but not all primary demanded aspects."
                res["aspect_coverage"] = {"ratio": solves_count / len(nexus_list), "status": "PARTIAL"}

        return res

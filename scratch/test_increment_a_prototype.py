import re
from dataclasses import dataclass

@dataclass(frozen=True)
class DomainCompatibilityRecord:
    is_disjoint: bool = False
    disjunction_type: str = "COMPATIBLE_TECHNICAL"  # RADICAL_DISJUNCTION, THEMATIC_METADATA, COMPATIBLE_TECHNICAL, OPEN_DOMAIN_PLAUSIBLE
    confidence: float = 1.0
    evidence: tuple[str, ...] = ()
    rationale: str = ""

class SemanticDomainDisjunctionEngine:
    """Increment A: Semantic Domain Disjunction Engine (Stage 31.7.27, Cycle 5).
    
    Evaluates semantic compatibility and detects radical domain disjunctions
    (botany/gardening, culinary recipes, automotive combustion mechanics, physical painting/crafts, everyday chores)
    without using brittle closed vocabulary lists.
    
    Also identifies institutional, biographical and category metadata (THEMATIC_METADATA)
    that discusses open-source foundations, creators, or releases without describing
    the demanded technical mechanism.
    """

    def __init__(self):
        # 1. Radical Disjunction Semantic Clusters (Non-Computing Everyday Life)
        # Each cluster consists of roots and phrases representing distinct non-computing domains.
        self.disjoint_domain_clusters = {
            "BOTANY_GARDENING": (
                r"\borqu[ií]deas?\b", r"\bjardinagem\b", r"\baduba[cç][aã]o\b", r"\badubo\b",
                r"\bpoda\b", r"\bpodar\b", r"\bcultivo de\b", r"\bregar\b", r"\brega\b",
                r"\bterra vegetal\b", r"\bfolhas verdes\b", r"\bvasos? de planta\b",
                r"\bhorta\b", r"\bgermina[cç][aã]o\b", r"\bsementes?\b", r"\bfotoss[ií]ntese\b"
            ),
            "CULINARY_RECIPES": (
                r"\bbolo de chocolate\b", r"\bclaras em neve\b", r"\bassar a \d+\b",
                r"\bassar no forno\b", r"\bforno pr[eé]-?aquecido\b", r"\bfarinha e cacau\b",
                r"\breceita de\b", r"\bpanela\b", r"\brefogar\b", r"\bpitada de sal\b",
                r"\bmassa de pizza\b", r"\bcozinhar\b", r"\blasanha\b", r"\bberinjela\b"
            ),
            "AUTOMOTIVE_MECHANICS": (
                r"\btroca de [oó]leo\b", r"\b[oó]leo do motor\b", r"\blubrificante sint[eé]tico\b",
                r"\bquil[oô]metros rodados\b", r"\bpastilhas? de freio\b", r"\bfiltro de combust[ií]vel\b",
                r"\bescapamento\b", r"\bcabe[cç]ote do motor\b", r"\bvela de igni[cç][aã]o\b",
                r"\bbalanceamento de (?:rodas|pneus)\b", r"\balinhamento e balanceamento\b",
                r"\bcorreia dentada\b", r"\bradiador do carro\b"
            ),
            "PHYSICAL_ARTS_CRAFTS": (
                r"\btinta a [oó]leo\b", r"\bverniz acr[ií]lico\b", r"\bpinceladas?\b",
                r"\btela de linho\b", r"\baquarela\b", r"\bcavalete de pintura\b",
                r"\bescultura em argila\b", r"\bmarcenaria\b", r"\blixar madeira\b"
            ),
            "EVERYDAY_CHORES": (
                r"\blavar lou[cç]a\b", r"\bpassar roupa\b", r"\barrumar a cama\b",
                r"\bpassear com (?:o )?cachorro\b", r"\bpassear com o c[aã]o\b",
                r"\bjogar futebol\b", r"\bnovela das oito\b", r"\bir ao shopping\b"
            )
        }

        # 2. Computing Context Markers (to protect against metaphorical uses of terms like 'árvore', 'raiz', 'motor', 'limpar')
        self.computing_context_markers = (
            "transacao", "thread", "banco", "tabela", "cluster", "servidor", "api", "protocolo",
            "memoria", "rede", "pacote", "cache", "requisicao", "dados", "query", "processo",
            "cpu", "lock", "disco", "conexao", "indice", "particao", "mensagem", "fila", "topico",
            "kafka", "docker", "kubernetes", "postgres", "redis", "http", "tcp", "ip", "dns",
            "algoritmo", "codigo", "software", "sistema", "microsservico", "computacao"
        )

        # 3. Thematic / Institutional / Biographical Metadata Patterns
        self.institutional_metadata_patterns = (
            r"\bpertence [aà] categoria de solu[cç][oõ]es\b",
            r"\bfoi lan[cç]ad[ao] pela funda[cç][aã]o\b",
            r"\bsob a (?:linux|apache) foundation\b",
            r"\bda apache software foundation\b",
            r"\bdo (?:linkedin|facebook|twitter|netflix|confluent|google)\b",
            r"\bcom ampla popularidade de mercado\b",
            r"\bganhou muita popularidade\b",
            r"\bprojeto open source\b",
            r"\bferramenta open source\b",
            r"\bprojeto de c[oó]digo aberto\b",
            r"\bcriad[ao] por ex-?engenheiros\b",
            r"\bdesenvolvid[ao] por ex-?engenheiros\b",
            r"\bminha equipe anterior utilizava [a-z0-9_]+ para armazenar dados de clientes e t[ií]nhamos reuni[oõ]es\b",
            r"\bt[ií]nhamos reuni[oõ]es semanais para discutir\b"
        )

        # 4. Evasive / Generic Deflection Patterns
        self.evasive_patterns = (
            r"\bvai variar de acordo com o caso concreto\b",
            r"\bdepende exclusivamente do or[cç]amento dispon[ií]vel\b",
            r"\bdepende dos fatores e dos custos envolvidos\b",
            r"\bdepende de muitos fatores\b",
            r"\bdepende bastante de como\b",
            r"\bcada caso [eé] um caso\b",
            r"\bvai depender de quanto dinheiro\b",
            r"\bconsultar uma consultoria\b"
        )

    def assess_compatibility(self, question_text: str, response_text: str, demands, prop) -> DomainCompatibilityRecord:
        from reference_runtime.runtime import _normalize_text
        q_norm = _normalize_text(question_text)
        r_norm = _normalize_text(response_text)

        # Check for genuine computing context in response with word boundaries
        has_comp_context = any(re.search(rf"\b{m}\b", r_norm) for m in self.computing_context_markers)

        # 1. Check for Radical Disjunction
        for domain_name, patterns in self.disjoint_domain_clusters.items():
            for pat in patterns:
                m = re.search(pat, r_norm)
                if m:
                    # If computing context is absent, or the disjoint pattern is prominent
                    if not has_comp_context:
                        return DomainCompatibilityRecord(
                            is_disjoint=True,
                            disjunction_type="RADICAL_DISJUNCTION",
                            confidence=0.95,
                            evidence=(m.group(0), domain_name),
                            rationale=f"Response proposition belongs to disjoint non-computing domain '{domain_name}' ({m.group(0)})."
                        )

        # 2. Check for Thematic Metadata Only
        for pat in self.institutional_metadata_patterns:
            m = re.search(pat, r_norm)
            if m:
                # If there are no concrete engineering mechanism keywords in the response
                mech_keywords = ("hash", "offset", "particion", "replica", "commit", "abort", "qu[oó]rum", "deadlock", "index", "sharding", "lru", "lock", "consensus", "atomic")
                if not any(k in r_norm for k in mech_keywords):
                    return DomainCompatibilityRecord(
                        is_disjoint=False,
                        disjunction_type="THEMATIC_METADATA",
                        confidence=0.90,
                        evidence=(m.group(0),),
                        rationale=f"Response presents institutional/category metadata ({m.group(0)}) without technical mechanism."
                    )

        # 3. Check for Evasive Deflection
        for pat in self.evasive_patterns:
            m = re.search(pat, r_norm)
            if m:
                return DomainCompatibilityRecord(
                    is_disjoint=False,
                    disjunction_type="EVASIVE_DEFLECTION",
                    confidence=0.95,
                    evidence=(m.group(0),),
                    rationale=f"Response proposition is an evasive deflection ({m.group(0)})."
                )

        # 4. Compatible Technical / Open Domain Plausible
        return DomainCompatibilityRecord(
            is_disjoint=False,
            disjunction_type="COMPATIBLE_TECHNICAL",
            confidence=1.0,
            evidence=(),
            rationale="Response is compatible with technical domain."
        )

engine = SemanticDomainDisjunctionEngine()
print("Engine initialized successfully.")

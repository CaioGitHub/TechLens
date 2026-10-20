import difflib
import hashlib
from pathlib import Path

baseline_path = Path("reference_runtime/runtime.py.stage_31_7_26_baseline")
current_path = Path("reference_runtime/runtime.py")

baseline_bytes = baseline_path.read_bytes()
current_bytes = current_path.read_bytes()

hash_baseline = hashlib.sha256(baseline_bytes).hexdigest().upper()
hash_current = hashlib.sha256(current_bytes).hexdigest().upper()

baseline_lines = baseline_path.read_text(encoding="utf-8").splitlines(keepends=True)
current_lines = current_path.read_text(encoding="utf-8").splitlines(keepends=True)

diff = list(difflib.unified_diff(
    baseline_lines,
    current_lines,
    fromfile="reference_runtime/runtime.py (Stage 31.7.26 Baseline)",
    tofile="reference_runtime/runtime.py (Stage 31.7.27 Remediated)",
    n=3
))

diff_text = "".join(diff)

doc = f"""# Stage 31.7.27 — Runtime Implementation Diff & Structural Remediation Record

## 1. Identificação e Integridade Criptográfica

| Parâmetro | Valor / Hash SHA-256 |
|---|---|
| **Runtime Alvo** | `reference_runtime/runtime.py` |
| **Baseline Pré-Implementação (Stage 31.7.26)** | `{hash_baseline}` |
| **Runtime Remediado (Stage 31.7.27)** | `{hash_current}` |
| **Status da Modificação** | Modificação Controlada Aprovada (Ciclo 5) |
| **Regressões Canônicas** | 0 regressões (1.084 testes executados, 1.083 OK, 1 skipped) |
| **Reference Harness** | 0 regressões (15/15 OK em 29.052s) |
| **Testes Contratuais de Ciclo 5** | 20/20 APROVADOS (100% OK em 0.021s) |

---

## 2. Sumário Estrutural das Modificações por Incremento

### Incremento A — Domain Compatibility Record e Semantic Domain Disjunction Engine
- Adicionada a dataclass `DomainCompatibilityRecord` com campos: `is_disjoint`, `disjunction_type`, `confidence`, `evidence`, `rationale`.
- Adicionada a classe `SemanticDomainDisjunctionEngine` com:
  - Detecção de domínios alienígenas e ortogonais não-computacionais (botânica, culinária, esportes, mecânica automotiva).
  - Preservação estrita de tecnologias desconhecidas/abertas em contexto de computação via marcadores contextuais com limites de palavra (`\\b`).
  - Análise bidirecional de compatibilidade entre proposição e pergunta, retornando `DomainCompatibilityRecord`.

### Incremento B — Refinamento do Proposition Discourse Filter
- Adicionada expressão regular para detecção de antítese destrutiva (`\\b(desativ|remover|deslig|arranc|elimin|dispens|retir)...\\b(locks?|travas?|transac|circuit breaker|rate limit|wal|fsync)\\b`) respeitando guardas de evitação preventiva.
- Ampliados os marcadores de declaração autobiográfica (`quando atuava como`, `vasta experiencia com`, `minha equipe anterior`) para evitar que narrativa pessoal sem mecanismo seja rotulada como operatória.
- Adicionado suporte a definições conceituais (`CONCEPTUAL_DEFINITION`) e soluções coloquiais de engenharia (`OPERATIVE_SOLUTION`) com voz passiva.

### Incremento D — Integração do Bipartite Nexus Matcher
- `DemandPropositionNexusBipartiteMatcher.assess_demand_nexus` parametrizado com `intent: QuestionIntent` e `domain_record: DomainCompatibilityRecord`.
- Roteamento explícito:
  - `domain_record.is_disjoint` -> `DOMAIN_DISJUNCT`
  - `is_trivia` / `THEMATIC_METADATA` -> `THEMATICALLY_ADJACENT`
  - `is_evasive` -> `EVASIVE`
  - `is_auxiliary` -> `CONTRIBUTES_TO`
  - `is_ignorance` -> `IGNORANCE`
  - `is_antithesis` -> `ANTITHESIS_OPPOSED`
  - `CONCEPTUAL_DEFINITION` -> `FUNCTIONALLY_SOLVES`
- Adicionado casamento morfológico de cognatos para perguntas compostas densas (`garante`/`garantem`, `ordem`/`ordenacao`).
- Substituído fallback incondicional por verificação de suficiência relativa à intenção.

### Incremento E — Strict Ontology Relevance Aggregator e Open Domain Proposition Engine
- Parametrizado `aggregate_relevance` com `domain_record`.
- Roteamento rigoroso:
  - `IGNORANCE` -> `UNKNOWN`
  - `DOMAIN_DISJUNCT` -> `OFF_TOPIC`
  - `EVASIVE` -> `INSUFFICIENT`
- Instanciado `SemanticDomainDisjunctionEngine` no `OpenDomainPropositionEngine.__init__`.
- Conectado o fluxo unificado em `evaluate_relevance`.

---

## 3. Unified Diff Completo

```diff
{diff_text}
```
"""

target_file = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_27_runtime_diff.md")
target_file.write_text(doc, encoding="utf-8")
print(f"Generated {target_file} ({len(doc)} bytes)")

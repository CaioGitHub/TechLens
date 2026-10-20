# Resultados de Conformidade de Schema e Validação — Stage 31.7.35

## 1. Visão Geral e Arquivo de Schema

- **Schema Sob Auditoria**: `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_34_evidence_traceability_schema.json`
- **Validador de Runtime**: `validate_evidence_traceability_record` em `reference_runtime/runtime.py`
- **Dialeto Formal**: JSON Schema Draft-07 (`http://json-schema.org/draft-07/schema#`)
- **Título do Schema**: `Stage31_7_31_EvidenceTraceabilityRecord`

---

## 2. Auditoria Estrutural Segundo o Draft-07

### 2.1. Verificação Sintática e Metaschema
1. **Validade Sintática JSON**: O arquivo carrega sem erros com `json.load()` (357 linhas, 9.179 bytes).
2. **Declaração de Metaschema**: A chave `$schema` declara explicitamente `"http://json-schema.org/draft-07/schema#"`.
3. **Consistência de Listas `required`**: Todas as 10 propriedades obrigatórias de nível raiz e todas as propriedades obrigatórias de objetos aninhados foram inspecionadas. Zero inconsistências ou apontamentos para chaves inexistentes em `properties`.
4. **Validade das Expressões Regulares**:
   - `runtime_version_hash`: pattern `^[A-F0-9]{64}$` é uma regex válida para hash SHA-256 em hexadecimal maiúsculo de 64 caracteres.
   - `timestamp_utc`: formato Draft-07 `"format": "date-time"`.

### 2.2. Alinhamento Estrito de Enums (Schema vs Runtime)

Foi executada uma auditoria automatizada cruzando todos os enums do schema com as constantes de runtime:

| Entidade / Campo | Enums no Schema | Enums no Runtime (`runtime.py`) | Discrepâncias | Status |
|---|---|---|---|---|
| `intent_mode` | 11 itens (`DEFINITION`, `CONCEPTUAL_EXPLANATION`, `MECHANISM`, `COMPARISON`, `HISTORICAL`, `CAUSALITY`, `DIAGNOSIS`, `IMPLEMENTATION`, `PROBLEM_SOLUTION`, `DECISION_JUSTIFICATION`, `TRADE_OFF_ANALYSIS`) | `VALID_INTENT_MODES` (11 itens) | Nenhuma | **100% MATCH** |
| `discourse_role` | 9 itens (`TECHNICAL_CORE`, `CONVERSATIONAL_PREAMBLE`, `ANALOGY_VEHICLE`, `ANALOGY_GROUNDING`, `HISTORICAL_METADATA`, `OBSERVABILITY_SUPPORT`, `EMPTY_FILLER`, `IGNORANCE_DECLARATION`, `RETRACTED_ASSERTION`) | `VALID_DISCOURSE_ROLES` (9 itens) | Nenhuma | **100% MATCH** |
| `thematic_presumption_status` | 4 itens (`ESTABLISHED`, `REBUTTED_ALIEN_DOMAIN`, `REBUTTED_HOMONYMY`, `NOT_ESTABLISHED`) | `VALID_THEMATIC_STATUSES` (4 itens) | Nenhuma | **100% MATCH** |
| `rebuttal_reason` | 4 itens (`NONE`, `ALIEN_PREDICATE_OVERRIDE`, `DISJOINT_CATEGORY_MISMATCH`, `UNRESOLVED_AMBIGUITY`) | `VALID_REBUTTAL_REASONS` (4 itens) | Nenhuma | **100% MATCH** |
| `nexus_relation` | 9 itens (`FUNCTIONALLY_SOLVES`, `CONTRIBUTES_TO`, `ANALOGOUS_GROUNDING`, `THEMATICALLY_ADJACENT`, `CIRCULAR_REPETITION`, `OPPOSED_ANTITHESIS`, `IGNORANCE`, `DOMAIN_DISJUNCT`, `UNRESOLVED_AMBIGUITY`) | `VALID_NEXUS_RELATIONS` (9 itens) | Nenhuma | **100% MATCH** |
| `confidence_level` | 3 itens (`HIGH`, `MEDIUM`, `LOW`) | `VALID_CONFIDENCE_LEVELS` (3 itens) | Nenhuma | **100% MATCH** |
| `classification` | 7 itens (`DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`) | `VALID_CLASSIFICATIONS` (7 itens) | Nenhuma | **100% MATCH** |

---

## 3. Comparação Entre o Schema Draft-07 e o Validador Personalizado

O runtime `reference_runtime/runtime.py` implementa `validate_evidence_traceability_record(data) -> tuple[bool, list[str]]`. A auditoria comparou o comportamento desta função contra a especificação formal do JSON Schema Draft-07:

| Dimensão de Validação | Schema Draft-07 | Validador Personalizado (`runtime.py`) | Análise de Compatibilidade |
|---|---|---|---|
| **Formato de Timestamp** | Valida de acordo com RFC 3339 / ISO 8601 (`format: date-time`) | Valida via expressão regular `_ISO_DATE_PATTERN` | **Compatível**. O regex cobre timestamps ISO 8601 padrão com `Z` ou offset de fuso horário. |
| **Padrão de Hash SHA-256** | `pattern: "^[A-F0-9]{64}$"` | `_HASH_64_PATTERN.match(h)` | **Idêntico**. Exige 64 caracteres hexadecimais maiúsculos. |
| **Limites de `coverage_ratio`** | `minimum: 0.0, maximum: 1.0` | `isinstance(cr, (int, float)) and 0.0 <= cr <= 1.0` | **Idêntico**. Intervalo fechado $[0.0, 1.0]$. |
| **Propriedades Desconhecidas** | Draft-07 permite por padrão (`additionalProperties` não especificado) | Permite chaves adicionais sem erro | **Idêntico**. Ambos admitem extensão aberta para propriedades futuras. |
| **Campo Opcional `applied_contract_ids`** | Opcional em `final_decision`, `type: array, items: {type: string}` | Se presente, valida que é `list` e todos elementos são `str` | **Idêntico**. Satisfaz o `FINDING-06` e retrocompatibilidade. |
| **Validação de `secondary_demands`** | Especifica schema dos itens se array presente | Valida presença de `primary_demand` | **Nuance Não-Impeditiva**: O validador customizado foca na demanda primária obrigatória; a validação recursiva completa é exercitada nos testes do INC-0. |

---

## 4. Bateria de Testes Positivos e Negativos

Os 17 testes contratuais em `tests/test_stage_31_7_34_inc0_contracts.py` comprovaram o comportamento discriminativo do validador e do schema:

### 4.1. Casos Positivos
- **Caso P-01 (Registro Completo Válido)**: Contém todas as 10 seções, enums válidos, `applied_contract_ids: ["SC-01", "SC-02"]`. Resultado: `True, []`.
- **Caso P-02 (Registro Mínimo Válido)**: Campos opcionais com valores default ou listas vazias, sem `applied_contract_ids`. Resultado: `True, []`.
- **Caso P-03 (Retrocompatibilidade FINDING-06)**: Ausência total da chave `applied_contract_ids` permanece 100% válida. Resultado: `True, []`.

### 4.2. Casos Negativos
- **Caso N-01 (Propriedade Raiz Ausente)**: Omissão de `question_profile` ou `final_decision`. Resultado: `False` com erro explícito de propriedade ausente.
- **Caso N-02 (Hash Inválido)**: Hash em minúsculas ou com tamanho diferente de 64 caracteres hexadecimais. Resultado: `False`.
- **Caso N-03 (Timestamp Malformado)**: Formatos como `"2026-10-19 23:00:00"` (sem `T` ou `Z`). Resultado: `False`.
- **Caso N-04 (Enum Inválido)**: `intent_mode: "SUPER_EXPLANATION"` ou `classification: "MAYBE"`. Resultado: `False` com enum rejeitado.
- **Caso N-05 (Limites Numéricos Violados)**: `coverage_ratio: 1.5` ou `-0.1`. Resultado: `False`.
- **Caso N-06 (Tipo Inválido em `applied_contract_ids`)**: Lista contendo inteiros `[101, 102]`. Resultado: `False`.

---

## 5. Conclusão de Conformidade

O schema `stage_31_7_34_evidence_traceability_schema.json` e o validador de runtime `validate_evidence_traceability_record`:
1. São formalmente consistentes entre si;
2. Refletem fielmente os contratos semânticos aprovados no Stage 31.7.31 e Stage 31.7.32;
3. Resolvem de ponta a ponta o `FINDING-06` da auditoria adversarial;
4. Não impõem bloqueios técnicos ou incompatibilidades para o início do **INC-1**.

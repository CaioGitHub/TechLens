# Stage 31.7.29 — Análise Estrutural de Causa-Raiz (RCA): Operatividade Gramatical versus Pertinência Semântica

## 1. Visão Geral e Problema Identificado

O Stage 31.7.28 submeteu o runtime remediado no Ciclo 5 (`6C44B7A8...`) a um conjunto 100% inédito de 250 casos de validação cega, revelando um bloqueio metodológico com **67,20% de acurácia global**, **34 falsos `DIRECT`** (taxa de 41,46% entre as 82 divergências) e **22 rebaixamentos indevidos de `RELATED` para `OFF_TOPIC`**.

Esta investigação de causa-raiz disseca os mecanismos computacionais internos do runtime que permitiram:
1. A promoção indevida de processos de culinária, cerâmica, construção civil e botânica para `DIRECT` (26 casos);
2. O rebaixamento indevido de metadados institucionais, históricos e contextuais legítimos de software para `OFF_TOPIC` (22 casos).

---

## 2. RCA 1: Falsos DIRECTs por Confusão entre Operatividade e Pertinência (26 Casos)

### 2.1. O Fenômeno Observado
Respostas com descrições processuais perfeitas de domínios não computacionais receberam classificação `DIRECT`:
- *Exemplo 1 (`VAL-31-7-28-183`):*
  - **Pergunta:** *"Como configurar o balanceamento dinamico de carga no subsistema 1?"*
  - **Resposta:** *"O processo de confeccao de vasos de argila do artesanato tradicional 1 requer amassamento da pasta mineral na roda de oleiro com posterior queima em forno a lenha."*
  - **Predição do Sistema:** `DIRECT` (relação: `open_domain_mechanism_assertion`).
- *Exemplo 2 (`VAL-31-7-28-175`):*
  - **Pergunta:** *"Como a tecnica de sharding distribui grandes volumes de dados em servidores distintos?"*
  - **Resposta:** *"A mistura de concreto estrutural exige o traco correto de cimento Portland, areia media lavada, brita graduada e agua, batidos na betoneira por tres minutos."*
  - **Predição do Sistema:** `DIRECT` (relação: `open_domain_mechanism_assertion`).

### 2.2. Onde a Evidência de Incompatibilidade foi Perdida: O Rastreamento da Falha

```text
[Pergunta Técnica] ──► [Extração de Demanda] (demand_1: sharding / balanceamento)
         │
         ▼
[Resposta Alienígena] ──► [SemanticDomainDisjunctionEngine]
                                 │
                                 ├─► Regex Clusters: Busca "\bescultura em argila\b", etc.
                                 │   FALHA: Texto contém "vasos de argila", "cimento Portland".
                                 │   Resultado: is_disjoint = False (NÃO DETECTADO!)
                                 ▼
                          [PropositionDiscourseFilter]
                                 │
                                 ├─► Analisa verbos: "requer", "exige", "mistura", "bate".
                                 │   São verbos transitivos ativos de processo.
                                 │   Resultado: is_operative = True (OPERATIVO!)
                                 ▼
                 [DemandPropositionNexusBipartiteMatcher]
                                 │
                                 ├─► Checa: is_disjoint? False. is_operative? True.
                                 │   Cai no Fallback de Domínio Aberto (Linha 3670):
                                 │   Resultado: FUNCTIONALLY_SOLVES
                                 ▼
                 [StrictOntologyRelevanceAggregator]
                                 │
                                 └─► Recebe FUNCTIONALLY_SOLVES com cobertura 1.0:
                                     Resultado Final: DIRECT (FALSO DIRECT EXPLOSIVO!)
```

### 2.3. A Causa-Raiz Estrutural Confirmada
1. **Dependência de Vocabulário Fechado no Motor de Disjunção:**
   O `SemanticDomainDisjunctionEngine` tentou capturar domínios disjuntos por meio de uma lista estática de 5 clusters de regex (`BOTANY_GARDENING`, `CULINARY_RECIPES`, `AUTOMOTIVE_MECHANICS`, `PHYSICAL_ARTS_CRAFTS`, `EVERYDAY_CHORES`). Qualquer domínio alienígena não explicitamente catalogado (construção civil, cerâmica utilitária, medicina veterinária, astronomia, corte e costura, marcenaria pesada) passa invisível pela checagem.
2. **Equiparação Falaciosa de Operatividade Gramatical com Pertinência Semântica:**
   O `PropositionDiscourseFilter` avalia se uma proposição é *operacional* com base na morfologia dos verbos (verbos transitivos diretos, voz ativa, presença de complementos de ação). Contudo, **um texto pode ser gramaticalmente operacional em seu próprio domínio e ser 100% irrelevante para a pergunta**.
3. **Ausência de Validação de Afinidade Ontológica entre Entidades:**
   O `DemandPropositionNexusBipartiteMatcher` não verifica se os substantivos e entidades da proposição (*cimento, argila, oleiro, betoneira*) possuem qualquer relação temática ou estrutural com o alvo da pergunta (*sharding, balanceador, réplicas, banco de dados*). Na ausência de uma flag de veto explícito, ele presume que qualquer frase operacional resolve funcionalmente a demanda.

---

## 3. RCA 2: Rebaixamento Indevido de Metadados Legítimos para OFF_TOPIC (22 Casos)

### 3.1. O Fenômeno Observado
Respostas com descrições históricas, institucionais e contextuais de tecnologias de software legítimas receberam classificação `OFF_TOPIC`:
- *Exemplo (`VAL-31-7-28-133`):*
  - **Pergunta:** *"Como o PostgreSQL implementa o controle de concorrencia multiversao (MVCC)?"*
  - **Resposta:** *"O PostgreSQL teve origem no projeto POSTGRES liderado por Michael Stonebraker na Universidade de Berkeley e e amplamente elogiado pela sua conformidade com padroes SQL."*
  - **Referência Humana:** `RELATED` (relação contextual sem atendimento operacional).
  - **Predição do Sistema:** `OFF_TOPIC` (relação: `non_operative_assertion`).

### 3.2. Rastreamento do Fluxo de Execução da Falha
1. **Falha de Reconhecimento de Metadados no `SemanticDomainDisjunctionEngine`:**
   O padrão `institutional_metadata_patterns` continha expressões engessadas, como `\bsob a (?:linux|apache) foundation\b` e `\bpertence [aà] categoria de solu[cç][oõ]es\b`. A resposta continha *"Universidade de Berkeley"*, *"projeto POSTGRES"* e *"pertence à categoria de ferramentas"*. Por não casar com as strings literais, a resposta não recebeu a marcação `THEMATIC_METADATA`.
2. **Classificação como Não-Operacional no `PropositionDiscourseFilter`:**
   Como a resposta descreve fatos históricos (*"teve origem"*, *"liderado por"*), ela não contém verbos de implementação computacional. O filtro marcou corretamente `is_operative = False`.
3. **Queda no Fallback `NON_OPERATIVE` no Matcher:**
   No `DemandPropositionNexusBipartiteMatcher`, sem a marcação de metadados e com `is_operative = False`, o fluxo caiu na última linha do método:
   ```python
   # Line 3674
   return DemandPropositionNexus(
       demand_id=demand.demand_id,
       nexus_relation="NON_OPERATIVE",
       rationale="Non-operative technical text without demonstrable nexus to demand."
   )
   ```
4. **O "Sumidouro" Incondicional do Agregador:**
   No `StrictOntologyRelevanceAggregator`, o bloco condicional verifica `FUNCTIONALLY_SOLVES`, `CONTRIBUTES_TO`, `THEMATICALLY_ADJACENT` e `PARTIALLY_SOLVES`. Qualquer outra relação (incluindo `NON_OPERATIVE`) cai no `else:`:
   ```python
   # Line 3815
   else:
       classification = "OFF_TOPIC"
       relation_type = "non_operative_assertion"
   ```
   **O agregador tratou a ausência de um mecanismo operacional como prova positiva de que o candidato estava falando fora do assunto (`OFF_TOPIC`)!**

### 3.3. A Causa-Raiz Estrutural Confirmada
- **Violação do Contrato Conceitual de `RELATED`:**
  O sistema assumiu uma falsa dicotomia: *ou a resposta é um mecanismo operacional funcional (`DIRECT`/`PARTIAL`), ou ela é fora do assunto (`OFF_TOPIC`)*. Isso destruiu a classe `RELATED`, que existe exatamente para acolher respostas que compartilham o contexto da tecnologia (PostgreSQL, Docker, Kubernetes), mas não respondem à mecânica da pergunta.

---

## 4. Distinção Rígida entre Causas Confirmadas e Hipóteses

| Tópico Investigado | Status | Evidência Comprobatória |
|---|:---:|---|
| O motor de disjunção depende de regexes literais que falham em novos domínios | **CONFIRMADO** | 26 casos de cerâmica, construção e agronomia não ativaram `is_disjoint` devido a vocabulário inédito. |
| O filtro discursivo confunde verbos transitivos com pertinência técnica | **CONFIRMADO** | Sentenças de artesanato com o verbo *"requer"* foram marcadas com `is_operative = True`. |
| O agregador converte indevidamente `NON_OPERATIVE` em `OFF_TOPIC` | **CONFIRMADO** | Código explícito nas linhas 3814–3820 de `runtime.py`; 22 casos de metadados caíram no `else: OFF_TOPIC`. |
| A divergência de hash entre 3FD3... e 6C44... causou os falsos DIRECTs | **REFUTADO** | A execução comparativa provou que ambos os runtimes geram exatamente os mesmos 26 falsos DIRECTs e 22 falsos OFF_TOPICs. |
| Redes neurais ou embeddings são estritamente necessários para resolver o problema | **HIPÓTESE NÃO COMPROVADA** | Uma arquitetura ontológica aberta baseada em substantivos nucleares da demanda e extração de papéis de entidade resolve a disjunção sem depender de modelos pesados. |

---

## 5. Diretrizes Inegociáveis para a Arquitetura do Ciclo 6

1. **PROIBIDO expandir regexes de domínios alienígenas:** Não criar listas para cerâmica, construção civil, marcenaria ou esportes.
2. **PROIBIDO tratar operatividade gramatical como pertinência semântica:** Uma ação só é funcionalmente relevante se atuar sobre as entidades do domínio da demanda.
3. **OBRIGATÓRIO desacoplar `NON_OPERATIVE` de `OFF_TOPIC`:** Sentenças que compartilham as entidades da pergunta (PostgreSQL, Linux, Docker), mas não apresentam ações resolutivas, devem ser roteadas para `RELATED`, e NUNCA para `OFF_TOPIC`.
4. **OBRIGATÓRIO exigir evidência positiva de disjunção para `OFF_TOPIC`:** `OFF_TOPIC` só pode ser emitido quando houver evidência estruturada de que as entidades da resposta são incompatíveis com as entidades da demanda.

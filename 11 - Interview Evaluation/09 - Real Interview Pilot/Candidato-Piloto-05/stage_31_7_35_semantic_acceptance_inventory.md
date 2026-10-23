# Stage 31.7.35 — Inventário dos critérios semânticos ainda abertos

Data: 2026-10-23. Adendo do plano atual; os planos e contratos históricos permanecem preservados.

## Resultado do inventário

16 critérios semânticos atribuídos a INC-1/INC-2 na matriz histórica, mais oito casos adversariais atribuídos no roadmap. Cada referência mantém fonte e significado originais. Os cenários representacionais já aprovados não são promovidos automaticamente a evidência de aceitação final.

## Critérios semânticos

Fonte das expectativas: `stage_31_7_31_contract_counterexample_matrix.json`. Atribuição histórica: `stage_31_7_33_contract_to_component_traceability.json`. O inventário JSON contém evidência exigida, nó de rastreabilidade, módulo planejado e ação seguinte por critério.

| Referência local na fonte semântica | Atribuição histórica | Cenário original | Classe esperada |
| --- | --- | --- | --- |
| SC-01 | INC-1 | Direct without lexical overlap | DIRECT |
| SC-02 | INC-1 | Genuinely disjoint alien domain not previously enumerated | OFF_TOPIC |
| SC-05 | INC-1 | Auxiliary observability contribution | SUPPORTING |
| SC-06 | INC-1 | Partially correct answer on multi-aspect question | PARTIAL |
| SC-07 | INC-1 | Compound question with complete fulfillment | DIRECT |
| SC-08 | INC-1 | Compound question with partial explicit omission | PARTIAL |
| SC-11 | INC-1 | Comparative question with structured axes | DIRECT |
| SC-12 | INC-1 | Diagnostic investigation scenario | DIRECT |
| SC-17 | INC-2 | Short concise technical definition | DIRECT |
| SC-18 | INC-2 | Long answer with irrelevant rambling padding | INSUFFICIENT |
| SC-20 | INC-2 | Avoidance guard on destructive keywords | DIRECT |
| SC-21 | INC-2 | Unseen fictional technology with sound distributed mechanism | DIRECT |
| SC-22 | INC-2 | Paired invariance parity across syntactic variations | DIRECT |
| SC-32 | INC-2 | Explicit Self-Correction Overriding Initial Incorrect Hypothesis | DIRECT |
| SC-33 | INC-2 | Direct Internal Contradiction Destroying Conceptual Truth Value | INSUFFICIENT |
| SC-34 | INC-2 | Distributed Multi-Sentence Composition (Definition + Mechanism + Trade-off) | DIRECT |

Todos permanecem **não demonstrados por esta suíte representacional**, o que não significa inexistência de testes ou capacidade equivalente em outras partes do projeto.

## Casos adversariais

Fonte: `stage_31_7_32_adversarial_counterexamples.json`. Diferentemente da matriz semântica genérica, estes casos possuem perguntas e respostas concretas para execução posterior.

| Referência local na fonte adversarial | Atribuição histórica | Categoria | Classe esperada |
| --- | --- | --- | --- |
| ADV-06 | INC-1 | Compound Demand With Missing Secondary Element | PARTIAL |
| ADV-05 | INC-2 | Mixed Response With Conversational Preamble | DIRECT |
| ADV-09 | INC-2 | Negation Scope Inversion | DIRECT |
| ADV-10 | INC-2 | Conditional Scope Invariance | DIRECT |
| ADV-11 | INC-2 | Discourse Self-Correction Resolution | DIRECT |
| ADV-12 | INC-2 | Real Internal Contradiction Destroying Truth Value | INSUFFICIENT |
| ADV-13 | INC-2 | Apparent Contradiction Reconciled by Operational Context | DIRECT |
| ADV-14 | INC-2 | Distributed Evidence Across Multiple Sentences | DIRECT |

## Lacunas concretas de evidência

1. O módulo `tests/test_stage_31_7_34_increments.py`, referenciado pelos 16 testes planejados, não está presente. Não é correto registrar esses alvos como executados.
2. Não foram encontradas classes com os nomes planejados `QuestionProfileExtractor`, `SufficiencyAssessmentEngine` e `DiscourseSegmentationEngine`. Existem `SemanticQuestionProfiler`, `DiscoursePropositionEngine` e mecanismos classificatórios anteriores. É necessária avaliação funcional antes de afirmar ausência de capacidade ou criar componentes novos.
3. As 16 entradas da matriz semântica têm descrições de evidência, mas não pares concretos `question`/`response`. Seus campos descritivos não devem ser executados como se fossem respostas de entrevista. Elaborar casos e fixar oracles antes de consultar previsões.
4. O nó planejado `discourse_profile.scopes` não é campo da dataclass atual. Negação e condição estão nas proposições. É preciso documentar e validar a correspondência dos caminhos de evidência; serialização válida sozinha não prova vínculo causal.
5. A atribuição histórica coloca cenários de domínio e tecnologia inédita em etapas de perfil/segmentação. Conservar essa atribuição como fato histórico, mas registrar dependências de afinidade, equivalência e agregação antes de exigir uma decisão completa de um extrator.
6. O contrato de composição apresenta uma contradição com duas classificações alternativas no texto, enquanto a matriz fixa SC-33 como INSUFFICIENT. Definir o oracle pela fonte aplicável e registrar a divergência, sem escolher o rótulo após observar a previsão.

## Suficiência por intenção

As dez famílias originais continuam exigindo critérios próprios: definição/conceito, mecanismo, comparação, história, causalidade, diagnóstico, implementação, solução de problema, justificativa e trade-offs. Para cada família, preparar resposta suficiente, parcial, auxiliar, temática e insuficiente; incluir contradição conforme o contrato original e um caso de fronteira. As subclasses representacionais de definição/conceito não criam uma exigência universal de código. Contar intenções identificadas não comprova suficiência de respostas.

Para demandas compostas, verificar atendimento total, parcial, omissão explícita e pedidos opcionais. A ausência de aspecto obrigatório não deve automaticamente produzir OFF_TOPIC; a omissão de aspecto opcional não deve diminuir a cobertura obrigatória.

## Ordem de trabalho e condições de progressão

1. **Oracles e rastreabilidade:** fixar os casos executáveis e a origem dos critérios; validar caminhos de evidência sem mudar os rótulos históricos. Registrar ambiguidades antes da execução.
2. **Diagnóstico funcional:** executar primeiro os oito casos adversariais originais e os casos preparados; persistir previsões e evidências reais. Usar a API canônica existente e distinguir classificação correta de trace causal completo. Essa execução será diagnóstica sobre casos conhecidos, não validação cega independente.
3. **Primeira falha:** investigar a origem na sequência pergunta → resposta → proposições → nexo → cobertura → decisão. Reutilizar capacidade existente antes de criar outra camada.
4. **Correções incrementais:** uma propriedade por grupo; teste de reprodução e regressão antes da próxima mudança. Diante de falha inesperada, corrigir ou documentar o bloqueio antes de avançar. Sem rollback destrutivo de trabalho alheio.
5. **Aceitação:** confirmar todos os critérios aplicáveis e suas dependências, regressão e harness no mesmo hash; preservar limitações e criar checkpoint separado. Não avançar de incremento só pela aprovação de testes representacionais.

## Estado desta execução

`SEMANTIC_ACCEPTANCE_INVENTORIED_NOT_VALIDATED`.

Runtime inalterado: `E537ED4DD81892B1378877536976E668A14ECCF975B8EE87BFF1245746E8E6B0`. Nenhuma previsão semântica nova foi executada nesta preparação. Não há nova contagem de testes globais ou novos resultados de qualidade semântica. As evidências anteriores permanecem válidas para o hash registrado, sem serem reinterpretadas como homologação integral.

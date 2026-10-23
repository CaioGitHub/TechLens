# Stage 31.7.35 — Adendo de reconciliação de escopo e critérios de aceite

Data: 2026-10-23. Este adendo registra a interpretação operacional das evidências existentes. Não altera a ontologia, o classificador, as expectativas semânticas históricas ou os relatórios anteriores.

## 1. Evidência atual

Branch `codex/inc1-contract-coverage`, checkpoint de entrada `15d08c0`, código inalterado desde a última regressão aprovada. Foram conferidos os métodos referenciados na suíte complementar e reexecutados os 52 testes direcionados: todos aprovados. A regressão global de 1.119 testes (1.118 aprovados, um ignorado) e o harness 15/15 são evidências da execução anterior no mesmo hash; não foram reexecutados para esta mudança documental.

## 2. Identificadores precisam da fonte

A matriz semântica do 31.7.31 e a rastreabilidade local do 31.7.35 reutilizam identificadores com sentidos diferentes. Por exemplo:

| ID local | Matriz semântica 31.7.31 | Rastreabilidade representacional 31.7.35 |
| --- | --- | --- |
| SC-01 | Resposta direta sem sobreposição lexical | Identificação do modo de intenção |
| SC-02 | Domínio alienígena disjunto | Decomposição de demandas |
| SC-05 | Contribuição auxiliar de observabilidade | Comparação e entidades |
| SC-06 | Resposta parcial a pergunta composta | Qualificadores de contexto |

Referências novas devem usar `arquivo#identificador`. Não é permitido somar testes de representação como cumprimento dos contratos semânticos homônimos. A disposição individual está em `stage_31_7_35_scope_reconciliation.json`. Os quatro casos ADV pertencem à fonte adversarial própria e também exigem referência qualificada; não são procurados como se fossem entradas da matriz SC.

## 3. Dez famílias e onze modos

O contrato de suficiência do 31.7.31 tem dez famílias e agrupa “Definição / Conceito” numa linha. O plano atual e o enum do runtime distinguem `DEFINITION` e `CONCEPTUAL_EXPLANATION`, resultando em onze modos representacionais. Essa correspondência explica a diferença de contagem como agrupamento; não prova que a suficiência das duas modalidades foi implementada. As outras nove famílias mantêm correspondência nominal com os modos atuais. Nenhum enum ou contrato histórico foi removido.

## 4. Escopo que fica estabelecido

- Plano atual 31.7.35: extração representacional de pergunta e discurso; há cenários de teste aprovados, com limitações explícitas.
- Roadmap 31.7.33 INC-1: perfil e suficiência por intenção; a aceitação da suficiência continua aberta.
- Roadmap 31.7.33 INC-2: segmentação, escopos e contradições; trabalho representacional já realizado é evidência parcial reutilizável, não conclusão automática desse incremento.
- INC-3 a INC-5: não são antecipados ou aprovados por este adendo.

Os contratos semânticos SC-07, SC-08, SC-11 e SC-12 continuam com as expectativas originais de atendimento composto, omissão explícita, comparação e diagnóstico. Esta reconciliação não os dispensa nem os realoca silenciosamente.

## 5. Critérios de aceite verificáveis

| Critério | Estado nesta execução | Evidência ou pendência |
| --- | --- | --- |
| Integridade do runtime | Verificado | Hash igual antes/depois; nenhuma edição de código |
| Métodos representacionais referenciados existem | Verificado | Inspeção AST da suíte complementar |
| Cenários direcionados | Verificado | 52 testes aprovados nesta execução |
| Regressão e harness no mesmo hash | Evidência anterior preservada | 1.119 testes globais e 15 de harness; saídas reais versionadas |
| Referências sem colisão de significado | Reconciliado por adendo | Fonte + identificador; equivalência não presumida |
| Famílias de intenção versus modos | Correspondência documental explicitada | Dez famílias, onze modos; não prova suficiência |
| Suficiência por intenção do INC-1 histórico | Aberto | Necessita critérios originais, oracles e evidência funcional próprios |
| Aceitação integral do INC-2 histórico | Aberto | Necessita cobertura completa dos contratos e limites de segmentação |
| Proveniência histórica dos snapshots | Ressalva mantida | Nome e igualdade de bytes não demonstram cronologia |
| Independência da validação semântica | Não demonstrada | Não houve nova validação independente |

## 6. Decisão e continuidade

Gate documental limitado: `REPRESENTATION_REFERENCES_RECONCILED_SEMANTIC_ACCEPTANCE_OPEN`.

O Stage 31.7.35 permanece aberto. O próximo trabalho é inventariar, a partir das fontes originais, os critérios funcionais ainda não evidenciados de suficiência e segmentação; para cada um, registrar teste/oracle e dependência antes de modificar runtime. A reconciliação documental não substitui aprovação semântica nem autoriza pular incrementos.

Os limites conhecidos permanecem: extração heurística, escopos locais e retratação por reversão conservadora, sem solução geral para paráfrases e alvos remotos. Relatórios históricos e resultados de testes não foram reescritos.

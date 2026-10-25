# Resultado da validação diagnóstica do roteiro

Data: 2026-10-25. Estado: `DIAGNOSTIC_COMPLETED_LIMITED_EVIDENCE`.

Foram analisados três casos fictícios, com 20 turnos, usando o projeto como fonte do método e dos critérios. As entradas e 15 expectativas foram fixadas antes dos relatórios, sem notas-alvo. O mesmo agente criou os casos, conheceu as expectativas, produziu as análises e as revisou: não há cegamento nem independência.

| Caso | Resultado observado |
| --- | --- |
| Transcrição clara | Três perguntas estruturadas, original preservado e evidência conceitual/hipotética separada de experiência em produção. |
| Transcrição incompleta | Fala perdida preservada; Q1 adiada sem zero; declaração de estudo registrada; voz desconhecida não atribuída à candidata. |
| Erros técnicos | Falas incorretas preservadas; erros examinados pela rubrica; autocorreção limitada à primeira resposta. |

## Achado e revisão

F01: na primeira versão do terceiro relatório, a justificativa da nota de Q1 podia misturar a tensão observada em outra pergunta à avaliação daquela resposta. A revisão restringiu a nota às evidências de Q1, preservando a inconsistência como limite de confiança. O julgamento passou de 6,0 a 7,0; não existe score esperado no oracle. As versões iniciais estão em `revisions/`. Essa revisão não prova calibração da nota e não altera o runtime.

## Verificações

O auditor `audit_outputs.py` realizou 30 verificações estruturais, todas aprovadas: integridade das entradas/expectativas, original, cobertura, citações e autoria, referências, dimensões, ausência de zero para perda da transcrição, fontes, limites visíveis e ausência de correção aplicada. Dois controles negativos foram detectados: citação adulterada e score zero em pergunta adiada. Esses resultados não validam a qualidade semântica das notas.

As 15 expectativas receberam autoavaliação manual com evidência indicada em `results.json`; isso não equivale a aprovação humana ou independente. Nenhum teste do runtime foi usado para substituir a análise da entrevista. Não foram rodados novamente os testes do runtime nesta entrega de cenários e documentação.

## Limites e próximo passo

O segundo caso não testa preservação de uma nota técnica não afetada, pois sua segunda pergunta é apenas informativa. Essa lacuna deve ser coberta por um caso adicional, sem alterar retroativamente as entradas desta rodada. Ainda faltam entrevista distinta e avaliação independente por outro contexto/agente ou revisor. Não há acurácia geral, percentual de automação ou medição de esforço humano a declarar.

Para repetir: fornecer o guia e as fontes do método e enviar um arquivo de `cases/` ao agente, sem expor `reference/` ou `analyses/`. Guardar a saída antes da comparação. O ambiente de execução precisa controlar esse acesso; a separação de pastas não garante cegamento.

Os artefatos desta pasta são exercícios diagnósticos, não relatórios finais de pessoas reais. Os gates históricos de validação semântica do projeto permanecem inalterados.

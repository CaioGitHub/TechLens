# Stage 31.2 — Human vs System Post-Correction

## Scope

Comparação nova entre a avaliação humana independente congelada no Stage 31 e a avaliação do sistema após a correção controlada do Stage 31.2. O relatório humano original não foi alterado e seus scores não foram usados como alvo de ajuste.

## Human Evaluation

Fonte congelada: `Stage 31 — Human Evaluation Independent.md`.

Scores: `4.0, 7.0, 4.0, 8.0, 2.0, 5.0, 5.0, 7.0, 4.0, 6.0, 4.0`.

## System After Correction

Scores: `4.0, 7.05, 4.0, 7.05, 4.45, 5.85, 6.0, 7.05, 4.0, 7.65, 4.0`.

Average: `5.55`.

Median: `5.85`.

## Comparison

| Questão | Humano | Sistema pós-correção | Diferença absoluta | Observação |
|---|---:|---:|---:|---|
| Q1 | 4.0 | 4.0 | 0.00 | declaração/insuficiência preservada |
| Q2 | 7.0 | 7.05 | 0.05 | diferença calibracional |
| Q3 | 4.0 | 4.0 | 0.00 | resposta fragmentada não promovida |
| Q4 | 8.0 | 7.05 | 0.95 | divergência residual não crítica |
| Q5 | 2.0 | 4.45 | 2.45 | resposta Kafka/Rabbit classificada como off-topic |
| Q6 | 5.0 | 5.85 | 0.85 | resposta parcial sobre JDBC |
| Q7 | 5.0 | 6.0 | 1.00 | divergência residual |
| Q8 | 7.0 | 7.05 | 0.05 | diferença calibracional |
| Q9 | 4.0 | 4.0 | 0.00 | declaração de ferramenta não promovida |
| Q10 | 6.0 | 7.65 | 1.65 | divergência residual |
| Q11 | 4.0 | 4.0 | 0.00 | uso de Copilot tratado como declaração |

Mean absolute difference: `0.64`.

Maximum absolute difference: `2.45` em Q5.

Material divergences above `1.0`: Q5 e Q10.

## Interpretation

A correção reduziu a diferença média absoluta de `2.01` para `0.64` sem otimização pelos scores humanos. A maior divergência restante, Q5, está semanticamente explicada: o sistema identifica conteúdo válido sobre mensageria, mas não o transfere como evidência de REST.

O score de Q5 não é tratado como erro de cálculo isolado. A resposta não é uma explicação de REST; o valor residual representa conteúdo técnico fora do tópico e insuficiência para a pergunta avaliada.

## Status

Este documento é um novo resultado de validação pós-correção. Não altera o gate histórico `HUMAN_VS_SYSTEM_BLOCKED`.

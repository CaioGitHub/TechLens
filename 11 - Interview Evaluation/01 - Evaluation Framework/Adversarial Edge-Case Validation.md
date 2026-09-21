---
type: reference
status: understood
confidence: 100
created: 2026-09-20
updated: 2026-09-20
tags:
  - interview-evaluation
  - validation
  - adversarial
  - meta
---
# Etapa 29 — Adversarial / Edge-Case Validation

## 1. Objetivo

Validar se o pipeline completo preserva estrutura, evidência, rastreabilidade e separação de responsabilidades quando submetido a transcrições sintéticas adversariais. A etapa tenta quebrar o runtime; não transforma casos adversariais em entradas anotadas nem usa o resultado esperado durante a execução.

```text
RAW TRANSCRIPT
→ 20.1–20.7
→ STRUCTURED INTERVIEW
→ EVIDENCE SET
→ EVALUATION
→ ORACLE COMPARISON
```

Nenhuma entrevista real ou relatório de candidato foi processado.

## 2. Relação com as etapas anteriores

| Etapa | Papel |
|---|---|
| 26 | contratos internos e harness determinístico |
| 27 | execução end-to-end sobre transcript bruto |
| 28 | calibração semântica blind |
| 29 | tentativa adversarial de encontrar atribuições, links, reconstruções, evidências e avaliações incorretas |

A Etapa 29 adiciona cobertura de robustez e não substitui as etapas 26–28.

## 3. Blindness e oracle

Os fixtures possuem `raw_transcript`, participantes e metadata operacional. O runtime recebe uma cópia sanitizada sem:

```text
oracle
expected_score
expected_dimensions
evidence_specs
evaluation_specs
adversarial_label
```

O oracle independente está em `tests/adversarial_cases.py` e é consultado somente após `run_pipeline`. Não existem branches por ID de caso para produzir scores ou evidências.

## 4. Casos executados

Foram executados 30 casos adversariais principais, com duas variantes no caso de senioridade, além de casos operacionais de bloqueio, warning e baixa confiança de reconstrução:

```text
ADV-01 contradição na mesma resposta
ADV-02 autocorreção parcial
ADV-03 autocorreção incorreta
ADV-04 confirmação induzida
ADV-05 entrevistador fornece a resposta
ADV-06 resposta interrompida em múltiplos turnos
ADV-07 pergunta reformulada / follow-up
ADV-08 follow-up que muda o escopo
ADV-09 resposta correta para pergunta errada
ADV-10 jargão sem evidência
ADV-11 eloquência superficial
ADV-12 resposta curta densa
ADV-13 experiência exagerada declarada
ADV-14 experiência demonstrada curta
ADV-15 incerteza
ADV-16 incerteza com hipótese
ADV-17 conflito entre respostas
ADV-18 intervenção contraditória do entrevistador
ADV-19 speaker ambiguity
ADV-20 termo técnico corrompido
ADV-21 resposta interrompida sem conclusão
ADV-22 pergunta sem resposta
ADV-23 resposta sem pergunta identificável
ADV-24 resposta parcialmente correta
ADV-25 evidências múltiplas conflitantes
ADV-26 comentário do entrevistador separado
ADV-27 pergunta do candidato
ADV-28 conclusão correta com argumento incorreto
ADV-29 mutação de complexidade
ADV-30-A/B invariância de senioridade
ADV-BLOCKED, ADV-WARNING e ADV-LOW-RECON
```

## 5. Mutation e invariance

Foram verificadas:

- verbosidade e texto periférico;
- eloquência;
- declaração de senioridade;
- declaração de experiência/CV;
- inflação de jargão;
- complexidade arquitetural irrelevante;
- idempotência;
- alteração controlada de transcript;
- follow-up e ordem de detalhes;
- influência do entrevistador.

As mutações não alteraram indevidamente a avaliação técnica. A declaração de senioridade permaneceu fora da evidência.

## 6. Responsibility boundaries

As fronteiras foram verificadas novamente:

- Transcription Processing preserva falas, atribuições, links, reconstrução e confidence, sem score;
- Evidence Model preserva evidências positivas, parciais, negativas, contraditórias, insuficientes e de confirmação;
- Evaluation Engine avalia o Evidence Set sem receber CV, senioridade ou conteúdo do entrevistador como evidência do candidato;
- Orchestration bloqueia downstream em erro crítico e continua com warnings recuperáveis, sem inventar conteúdo.

## 7. Confidence, ausência e traceability

Foram validadas:

```text
participant → speaker → segment → question → response → evidence → evaluation
```

`missing`, `unknown`, `unanswered` e confirmação induzida não foram convertidos silenciosamente em conhecimento negativo ou demonstração positiva. Uma `reconstruction_confidence` baixa foi preservada sem copiar mecanicamente esse valor para a confidence da avaliação.

## 8. Falhas iniciais e correções

### Falha 1 — autocorreções e erros não reconhecidos

**Causa:** vocabulário blind insuficiente para formas como `thread do sistema operacional`, `não, acho`, `Ah, verdade` e `retry agressivo`.

**Correção:** ampliar sinais semânticos controlados, preservando a separação entre `self_correction` e `technical_error`.

**Regression:** PASS.

### Falha 2 — off-topic e hipótese/incerteza incompletos

**Causa:** a heurística cobria somente alguns pares de domínios e não reconhecia `não sei`/`investigaria` como sinais distintos.

**Correção:** adicionar relações de domínio e sinais explícitos de uncertainty/hypothesis.

**Regression:** PASS.

### Falha 3 — mutations periféricas inflavam score

**Causa:** CV, senioridade e jargão aumentavam o comprimento bruto usado por completude/profundidade.

**Correção:** normalizar metadata e jargão periférico antes das dimensões, sem removê-los do transcript original.

**Regression:** PASS.

### Falha 4 — expectativa excessiva no caso de warning

**Causa:** uma fala desconhecida corretamente produzia warning, mas não uma avaliação utilizável.

**Correção:** o teste passou a verificar continuidade dos artefatos e warning, sem exigir evidência inventada.

**Regression:** PASS.

Nenhum peso, threshold, dimensão, regra de N/A ou conceito canônico da Rubric/Evaluation Engine foi alterado.

## 9. Resultado final

Execução:

```text
py -3 .\run_adversarial_edge_cases.py
py -3 -m unittest tests.test_adversarial_edge_cases -q
```

Resultado:

```text
37 Stage 29 tests: PASS
33 non-blocked executions: PASS/PASS_WITH_WARNING
1 blocked execution: BLOCKED as expected
FAIL: 0
NOT_EXECUTED: 0
```

O caso `ADV-BLOCKED` é uma condição operacional esperada e não uma falha da etapa; `ADV-WARNING` continua sem fabricar avaliação quando não existe resposta atribuível.

Após as correções estruturais da Etapa 30.1, a mesma execução passou a reportar:

```text
34 executions
29 PASS
4 PASS_WITH_WARNING
1 BLOCKED as expected
0 FAIL
```

Os warnings adicionais são intencionais: perguntas do candidato e respostas sem
vínculo confiante agora são explicitamente sinalizadas em vez de serem tratadas
silenciosamente como fluxo avaliável comum.

## 10. Limitações

1. O runtime permanece determinístico e baseado em heurísticas controladas.
2. Os transcripts são sintéticos; não representam entrevistas reais.
3. Não há LLM/NLP de produção nem interpretação humana aberta.
4. Os artefatos históricos das Etapas 19/19.1 continuam indisponíveis.
5. A validação adversarial cobre os contratos representados pelo runtime de referência, não todos os erros possíveis de um parser de produção.

## 11. Gate

```text
ADVERSARIAL_EDGE_CASE_VALIDATION_COMPLETE
```

Status:

```text
READY_WITH_WARNINGS
```

As limitações são de escopo e não impedem o uso desta etapa como referência adversarial do runtime local.

## 12. Próxima etapa

Recomenda-se uma etapa futura de comparação com um avaliador semântico independente ou corpus anotado por humanos, sem alterar a Rubric ou o Evaluation Engine para acomodar resultados.

## Ver também

- [[Reference Runtime]]
- [[Semantic Blind Calibration]]
- [[Synthetic Interview Full Run]]
- [[Interview Evaluation Pipeline]]
- [[Evidence Model]]
- [[Evaluation Engine]]
- [[Scoring Rubric]]
- [[Interview Evaluation MOC]]

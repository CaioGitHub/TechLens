# Stage 30.2 — Human Review & Structured Interview Approval

## 1. Objetivo

Verificar se a representação derivada do piloto real corresponde ao transcript original com fidelidade, rastreabilidade e segurança semântica suficientes para servir de base à avaliação técnica. Esta aprovação é estrutural e não representa aprovação, reprovação, contratação ou senioridade do candidato.

## 2. Escopo

A revisão comparou `Transcript Original.md` com os artefatos pós-correção:

- `After Correction - Entrevista Estruturada.md`;
- `After Correction - Evidence Set.md`;
- `After Correction - Individual Evaluations.md`;
- `After Correction - Interview Evaluation v2.md`;
- `Stage 30 — After Correction.md`;
- `Stage 30.1 — Pilot Failure Analysis.md`.

O transcript original permaneceu a fonte de verdade e não foi alterado.

## 3. Participant Review

### Resultado

`VALID`

Foram identificados quatro participantes:

| Participant ID | Role | Confidence | Review |
|---|---|---|---|
| `P-05-CANDIDATE` | candidate | high | Falas de Ingrid Mazoni atribuídas ao candidato |
| `P-05-INTERVIEWER-1` | interviewer | high | Falas de Morais, Michelly Pereira de Vasconcelos |
| `P-05-INTERVIEWER-2` | interviewer | high | Falas de Paes, Caio Victor Pessoa de Vasconcelos |
| `P-05-OBSERVER` | observer | high | Falas de Nascimento, Rodrigo Borges do |

Não foi encontrada fala crítica do candidato atribuída a outro participante.

## 4. Speaker Attribution Review

### Resultado

`VALID`

As respostas relevantes preservaram `speaker_role: candidate`, IDs de segmentos `RP05-*` e confiança alta. Falas curtas, interrupções e comentários intermediários não foram convertidos em respostas do candidato sem origem no transcript.

## 5. Question Review

### Resultado

`VALID_WITH_LIMITATIONS`

Foram revisadas 11 perguntas avaliáveis. Todas possuem `question_id`, texto, speaker de entrevista e `source.segment_ids` válidos. O prompt contextual `RP05-113`, `E tem uma Daily também, só nossa, né?`, foi excluído após a correção do Stage 30.1.

Perguntas técnicas reais, como observabilidade e JDBC, continuam avaliáveis. Não havia no transcript pós-correção um caso técnico equivalente à frase de Daily para uma nova classificação ambígua; a preservação de perguntas técnicas com tag question foi coberta pelos testes do Stage 30.1.

As cinco perguntas do candidato foram preservadas como `CQ1`–`CQ5`, com `evaluation_eligible: false`, e não contaminaram as avaliações.

## 6. Response Review

### Resultado

`VALID_WITH_WARNINGS`

Foram preservadas 47 respostas. A sequência de respostas múltiplas, interrupções e retomadas permanece representada por segmentos de origem. Respostas sem pergunta identificável continuam `unknown`/`needs_review`, sem vínculo forçado.

Os casos mais relevantes revisados foram:

- `R26`: continuação contextual após explicação dos entrevistadores sobre Azure;
- `R43`: pergunta do candidato sobre acesso a logs;
- `R24`: resposta curta `Não, nenhum.` após contexto conversacional;
- `R31`: continuação da resposta de investigação.

Nenhum desses casos apresentou perda comprovada de evidência avaliável ou necessidade de criar vínculo por proximidade.

## 7. Reconstruction Review

### Resultado

`SAFE`

As 47 reconstruções do runtime possuem `original_text == reconstructed_text`. Não foram detectadas mudanças semânticas, completamento de respostas, correções técnicas indevidas ou remoção de expressões de incerteza.

O ruído do transcript, incluindo termos como `dyna trace`, `ezure` e `Lego Analytics`, não foi silenciosamente convertido em uma afirmação técnica mais precisa.

## 8. Linking Review

### Resultado

`CORRECT_WITH_ACCEPTED_UNKNOWN`

Os vínculos avaliáveis seguem a estrutura:

`Q1 → R1`, `Q2 → R3/R4/R6/R7/R8/R9/R10`, `Q3 → R12/R14`, `Q4 → R16`, `Q5 → R17`, `Q6 → R19`, `Q7 → R21`, `Q8 → R22/R23`, `Q9 → R25`, `Q10 → R27/R29/R31`, `Q11 → R32/R34`.

As respostas sem evidência suficiente para vínculo permanecem `unknown/needs_review`. Essa decisão é considerada correta e mais segura do que vincular por proximidade.

## 9. Evidence Review

### Resultado

`SUPPORTED`

Foram revisadas 22 evidências. Cada uma:

- referencia uma resposta existente;
- referencia a mesma pergunta da resposta;
- contém texto presente na resposta;
- aponta para segmentos `RP05-*` existentes;
- é alcançada por pelo menos uma avaliação quando utilizada.

Não foram encontradas evidências inventadas, órfãs ou com `source = unknown`.

As evidências do piloto foram classificadas pelo runtime como `conceptual` ou `reasoning`. Não houve evidência explícita dos tipos `experience_declaration`, `demonstrated_experience`, `hypothesis` ou `uncertainty` no conjunto final. Isso limita a granularidade da revisão, mas não introduziu uma afirmação falsa.

## 10. Individual Evaluation Review

### Resultado

`SUPPORTABLE_WITH_WARNINGS`

As 11 avaliações referenciam perguntas, respostas e evidências existentes. Os scores estão dentro do contrato, e cada avaliação utiliza evidência vinculada à mesma pergunta e resposta. A diferença entre as avaliações é sustentada pelas dimensões calculadas a partir do Evidence Set.

Os scores não foram alterados durante esta revisão. A confiança `high` deve ser interpretada como confiança no vínculo e na evidência disponível, não como certeza absoluta sobre a qualidade técnica global.

Limitação: o Evidence Set possui categorias semânticas coarse-grained; portanto, a distinção entre experiência declarada e experiência demonstrada não foi explicitada em campos próprios neste piloto. A revisão não promoveu declarações de experiência a experiência demonstrada.

## 11. Global Evaluation Review

### Resultado

`VALID_WITH_LIMITATIONS`

O conjunto global contém 11 avaliações, 22 evidências e referências completas de IDs. A distribuição pós-correção é:

- média: `6,93`;
- mediana: `7,05`;
- avaliações: 11;
- perguntas avaliáveis: 11.

As limitações e warnings permanecem proporcionais ao escopo: linking conservador, prompts conversacionais e cobertura limitada ao conteúdo efetivamente identificado.

O artefato global pós-correção não materializa uma análise qualitativa detalhada por domínio, complexidade, strengths e gaps; ele preserva readiness, estágios, IDs e warnings. Essa é uma limitação do adapter/materializador atual, não uma conclusão inventada. A aprovação é, portanto, com warnings.

## 12. External Context Contamination Review

### Resultado

`PASS`

Não foram encontrados CV, senioridade, cargo, empresa, salário, decisão de contratação ou contexto da vaga usados como evidência nas avaliações. A revisão também confirmou que a aprovação estrutural não altera scores nem o Evaluation Engine.

## 13. Traceability Audit

### Resultado

`PASS`

A cadeia foi validada:

`global traceability → evaluation → evidence → response → question → source.segment_ids → transcript`

Todos os segmentos referenciados pertencem ao transcript original e seguem o padrão `RP05-*`. Não foram encontrados IDs órfãos ou fontes desconhecidas em evidências utilizadas por avaliações.

## 14. Findings

```yaml
human_review:
  findings:
    - id: HR-30.2-001
      severity: P2
      stage: 23.2
      affected_ids: [global-artifact]
      description: "O artefato global pós-correção não materializa análise qualitativa detalhada por domínio, complexidade, strengths e gaps."
      source: "After Correction - Interview Evaluation v2.md"
      expected: "Resumo global proporcional e detalhado, quando produzido pelo contrato da etapa."
      actual: "Readiness, estágios, traceability e warnings são preservados; a análise qualitativa detalhada não é materializada."
      impact: "Limita a revisão global, mas não quebra a rastreabilidade nem inventa conclusões."
      status: ACCEPTED
    - id: HR-30.2-002
      severity: INFO
      stage: 21
      affected_ids: [evidence-set]
      description: "A taxonomia materializada de evidências é coarse-grained e não explicita experiência declarada versus demonstrada."
      source: "After Correction - Evidence Set.md"
      expected: "Distinção explícita quando houver evidência correspondente."
      actual: "As evidências finais são conceptual/reasoning."
      impact: "Reduz a granularidade da auditoria sem promover afirmações não demonstradas."
      status: ACCEPTED
    - id: HR-30.2-003
      severity: INFO
      stage: 20.6
      affected_ids: [R26, R43]
      description: "Respostas contextuais permanecem unknown/needs_review."
      source: "After Correction - Entrevista Estruturada.md"
      expected: "Vínculo somente quando houver evidência conversacional suficiente."
      actual: "R26 e R43 permanecem sem vínculo."
      impact: "Nenhuma evidência avaliável perdida foi demonstrada; vincular por proximidade seria mais arriscado."
      status: ACCEPTED
```

## 15. Accepted Limitations

- A análise global detalhada por domínio não está presente no materializador pós-correção.
- O Evidence Set não explicita todas as categorias semânticas possíveis.
- Respostas contextuais sem vínculo seguro permanecem `unknown/needs_review`.
- Não houve segundo avaliador humano independente.
- A revisão aprova a representação estrutural, não a correção absoluta de cada score.

## 16. Approval Decision

`APPROVED_WITH_WARNINGS`

A representação estruturada é suficientemente fiel, rastreável e semanticamente segura para servir de base à avaliação técnica do piloto. Não há P0, speaker crítico incorreto, evidência inventada, linking crítico incorreto, score sem suporte demonstrável ou contaminação externa.

Esta decisão não significa aprovação ou reprovação do candidato, contratação, senioridade ou aderência à vaga.

## 17. Confidence

`HIGH` para identificação de participantes, atribuição de speakers, origem das perguntas, respostas, evidências e rastreabilidade.

`MEDIUM` para a suficiência da avaliação global, devido à materialização global resumida, à taxonomia coarse-grained e à ausência de segundo avaliador humano.

## 18. Gate

`STRUCTURED_INTERVIEW_APPROVED_WITH_WARNINGS`

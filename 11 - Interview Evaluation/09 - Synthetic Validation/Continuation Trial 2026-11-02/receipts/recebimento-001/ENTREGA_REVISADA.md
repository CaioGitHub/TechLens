# Entrega revisada — revisão assistida

## 1. Escopo, preservação e limites

Esta é uma **revisão assistida posterior à primeira execução**. A primeira entrega e seu registro permanecem preservados e não foram sobrescritos. Esta versão altera somente as decisões e os indicadores afetados pelos achados da `CONFERENCIA.md`.

Foram usados como evidência textual os pedidos, respostas, vínculos e notas reproduzidos em `ENTREGA_DA_ANALISE.md`, confrontados com os achados de `CONFERENCIA.md` e com a tarefa desta revisão. O pacote atual não contém `TRANSCRICAO_SIMULADA.md`, `CONDICOES_DA_FONTE.md`, a Taxonomia, a Rubrica nem `TRANSCRIPTION_EVALUATION_CHECK.md`; por isso não alego leitura direta desses arquivos nesta revisão. Não houve áudio, fonte externa, runtime, harness, teste, validação humana independente ou autenticação de experiência real.

Mantêm-se os limites já declarados: a fala de 06:43 é irrecuperável, “grafano” permanece incerto, e não se infere senioridade, contratação, competência geral ou desfecho não dito.

## 2. Classificação revisada por unidade

| Unidade | Pedido e evidência relevante | Decisão revisada |
|---|---|---|
| Q1 — 00:27–00:36 | Inventário de linguagens e ferramentas; “grafano” incerto e Java 21 apenas estudado | Contextual, sem nota |
| Q2 — 01:02–01:12 | Explicação conceitual de transação, sem configuração | Técnica avaliável |
| Q3 — 01:40–01:51 | Efeito de rollback sobre e-mail externo já enviado | Técnica avaliável |
| Q4 — 02:14–02:23 | Diferença entre autenticação e autorização; inversão seguida de autocorreção explícita | Técnica avaliável; autocorreção preservada |
| Q5 — 02:58–03:06 | Confirmação de participação em observabilidade; não pede demonstração | **Contextual, sem nota**. O relato espontâneo sobre identificador nos logs e o limite de que a plataforma configurou o coletor são preservados, sem criar unidade pontuada. |
| Q6 — 03:28–03:40 | Exemplo, ações realizadas e o que conseguiu concluir | Técnica avaliável |
| Q7 — 04:13–04:29 | Conduta diante de possível gravação antes da queda e motivo para não repetir às cegas | Técnica avaliável, hipotética |
| Q8 — 05:05–05:17 | Dificuldades de implementar tratamento de repetição e cuidados necessários | Técnica avaliável |
| Q9 — 05:42–05:55 | Como começar investigação de API lenta sem acesso ao ambiente de teste | Técnica avaliável |
| Q10 — 06:31–06:43 | Ajuste de alerta e verificação do efeito | Técnica adiada por fonte comprometida; sem zero |
| Q11 — 07:04–07:16 | Se expiração de cache garante valor sempre mais recente | Técnica avaliável |
| Q12 — 07:45–07:54 | Ferramenta usada para organizar tarefas | Contextual, sem nota |
| Q13 — 08:15–08:34 | Pergunta da candidata e resposta do entrevistador sobre acesso e coletor | Contextual, sem nota da candidata |

Resultado de cobertura: 8 técnicas avaliáveis, 1 técnica adiada e 4 contextuais. Q5 não é técnica adiada; é contextual.

## 3. Fundamento e dimensões aplicáveis

As dimensões abaixo são aplicadas somente quando o pedido as convoca. N/A significa que a unidade não solicitou aquela dimensão, não que houve falha.

| Unidade | Nota | Dimensões aplicáveis e fundamento | Dimensões N/A |
|---|---:|---|---|
| Q2 | **8,0** | Correção, clareza e completude do conceito pedido | Profundidade de configuração, aplicação prática e trade-offs: o pedido excluiu configuração e não pediu cenário ou trade-off |
| Q3 | **2,0** | Correção do comportamento perguntado e explicação da relação entre rollback local e efeito externo | Experiência prática, implementação e trade-offs: não foram pedidos |
| Q4 | **8,0** | Distinção conceitual, relevância e resposta final; a inversão inicial e a autocorreção são ambas preservadas | Implementação, experiência prática e trade-offs: não foram pedidos |
| Q6 | **5,5** | Exemplo concreto, ações realizadas e conclusão efetivamente relatada. A candidata buscou registros pelo identificador e localizou a integração de pagamento; também declarou que não determinou a causa nem acompanhou o desfecho. Isso registra o limite do que conseguiu concluir, sem transformar causa raiz ou acompanhamento posterior em requisito autônomo | Implementação, validação de causa raiz e acompanhamento posterior: não foram pedidos como condições separadas; somente podem ser considerados na medida em que se relacionam ao pedido de conclusão |
| Q7 | **8,0** | Aplicação ao cenário, motivo para evitar repetição às cegas e condicionamento ao contrato; a fala é hipotética, como o pedido | Experiência comprovada, implementação e resultado observado: não foram pedidos e não são inferidos |
| Q8 | **3,0** | Atendimento ao pedido específico de dificuldades e cuidados de implementação | Benefícios gerais não substituem as dificuldades/cuidados solicitados; implementação realizada, resultado e trade-offs adicionais não foram demonstrados/pedidos |
| Q9 | **7,5** | Estratégia inicial, uso dos dados acessíveis, consideração da restrição de não acesso a teste e cautela operacional | Causa raiz, correção em produção e validação final: o pedido era como começar a investigação |
| Q11 | **9,0** | Resposta direta, correção e explicação da janela de cópia/staleness | Estratégia completa de invalidação, implementação e teste: não foram pedidos |

Q10 permanece adiada: todas as dimensões avaliativas são N/A enquanto o trecho necessário estiver comprometido. Não há nota nem inclusão em denominador.

## 4. Avaliação revisada

### Q2 — 8,0

A explicação atende ao pedido conceitual de unidade, confirmação ou desfazimento. Não exige configuração que a pergunta expressamente excluiu.

### Q3 — 2,0

A resposta afirma que rollback cancelaria automaticamente e-mail já enviado por API externa. Esse é o erro central na dimensão solicitada; não foram acrescentados requisitos de implementação ou experiência.

### Q4 — 8,0

A resposta começa invertida, corrige-se espontaneamente e termina com a distinção correta entre identidade e permissão. A autocorreção é mantida como evidência relevante; não se aplica desconto automático nem nota-alvo.

### Q5 — contextual, sem nota

A pergunta solicita confirmação de participação, não uma demonstração. Preservam-se o identificador nos logs e a autoria limitada à plataforma quanto ao coletor, mas não se atribui nota nem se usa a unidade nos indicadores técnicos.

### Q6 — 5,5

O exemplo é concreto: busca por registros usando o identificador e localização da falha na integração de pagamento. A resposta também informa o limite do que conseguiu concluir: não determinou a causa e não acompanhou o desfecho. A nota se fundamenta no atendimento parcial aos três elementos pedidos — exemplo, ações e conclusão —, sem afirmar que a pergunta necessariamente exigia causa raiz ou acompanhamento posterior. Não há aumento automático nem redução por requisito inventado.

### Q7 — 8,0

A candidata não repetiria às cegas, consultaria o resultado e condicionaria a reutilização de chave ao contrato. Isso atende ao cenário hipotético; não é tratado como experiência de implementação.

### Q8 — 3,0

Confiança, prevenção de duplicação e experiência em rede ruim são benefícios ou objetivos pertinentes, mas não explicam as dificuldades e cuidados de implementação solicitados. A âncora decorre dessa lacuna específica, não do tamanho da resposta.

### Q9 — 7,5

O início proposto usa horários, operações, duração, erros e registros/painéis disponíveis, preservando a restrição de acesso e a cautela de não alterar sem coordenação. Não se exige investigação completa porque o pedido era o primeiro passo.

### Q10 — adiada, sem nota

O trecho de 06:43 não permite avaliar o ajuste de alerta ou seu efeito. Não se recupera conteúdo nem se confirma “grafano” por suposição.

### Q11 — 9,0

A resposta nega corretamente que expiração de um minuto garanta o valor mais recente e explica que a origem pode mudar durante a janela. Não se exige estratégia adicional não solicitada.

## 5. Indicadores revisados

- **Técnicas avaliáveis:** 8 (Q2, Q3, Q4, Q6, Q7, Q8, Q9, Q11).
- **Técnica adiada:** 1 (Q10), fora do denominador e sem zero.
- **Contextuais sem nota:** 4 (Q1, Q5, Q12, Q13).
- **Lista única de notas:** 8,0; 2,0; 8,0; 5,5; 8,0; 3,0; 7,5; 9,0.
- **Soma:** 51,0.
- **Média parcial das técnicas avaliáveis:** 51,0 / 8 = **6,38**.
- **Mediana:** **7,75**.
- **Faixas:** 0–2: 1; 3–4: 1; 5–6: 1; 7–8: 4; 9–10: 1.
- **Menor nota:** 2,0. **Maior nota:** 9,0.

Essa média é parcial e não é média global da entrevista. Não é comparada com uma média desejada nem usada para igualar outro ensaio.

## 6. Síntese revisada

O material utilizável mostra explicação adequada de transação, distinção final correta entre autenticação e autorização com autocorreção, uso prático limitado de correlação em logs, raciocínio hipotético para evitar duplicação, início ordenado de investigação de lentidão e compreensão da janela de expiração de cache. Também mostra erro sobre o alcance do rollback e resposta insuficiente ao pedido específico de dificuldades/cuidados de implementação.

Q5 registra participação e autoria limitada, mas permanece contextual. Q6 demonstra exemplo e ações concretas e declara limites de conclusão; não permite afirmar causa raiz ou desfecho. Q10 segue sem julgamento. Nenhum desses dados sustenta inferência sobre senioridade, experiência geral, contratação ou validação real.

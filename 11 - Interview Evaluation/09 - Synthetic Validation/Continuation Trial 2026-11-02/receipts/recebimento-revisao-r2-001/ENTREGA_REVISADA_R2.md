# Entrega revisada R2 — Continuidade

## 1. Autoria, escopo e limites

Esta é uma **revisão assistida R2**, posterior às versões anteriores. Não é uma revisão cega, independente ou aprovação humana. `ENTREGA_DA_ANALISE.md`, `ENTREGA_REVISADA.md` e seus registros foram usados como histórico de feedback, não como fonte primária da fala.

### Autoria e vínculos

| Participante | Papel sustentado pela fonte | Vínculo |
|---|---|---|
| Marina Alves | Coordenadora do projeto fictício e responsável pelo encerramento | Apresentação em 00:03 e encerramento em 09:06 |
| Diego Rocha | Entrevistador técnico | Identificado como condutor das perguntas técnicas em 00:03 |
| Lúcia Martins | Pessoa entrevistada/candidata | Responde às perguntas e faz a pergunta final |

As falas foram vinculadas aos rótulos recebidos em `TRANSCRICAO_SIMULADA.md`. Isso não valida experiência profissional real.

### Fonte e condições

- Fonte primária consultada diretamente: `TRANSCRICAO_SIMULADA.md`.
- Condições consultadas diretamente: `CONDICOES_DA_FONTE.md`.
- Cobertura textual: 00:03–09:06; timestamps identificam o início das falas, não intervalos comprovados.
- Não há áudio nem fonte adicional recuperável.
- A frase inteira de Lúcia em 06:43 foi declarada comprometida; não há redação correta recuperável.
- “grafano”, em 00:36, permanece incerto; nenhuma substituição foi confirmada.
- As falas de 01:40/01:51 e 02:14/02:23 foram preservadas, inclusive a autocorreção.
- Não foram fornecidos SGBD, fornecedor de e-mail, mecanismo de compensação, configuração distribuída ou versão adicional de protocolo.

Foram consultados diretamente `METODO/TRANSCRIPTION_EVALUATION_CHECK.md`, `METODO/11 - Interview Evaluation/02 - Question Types/Question Taxonomy.md` (incluindo §2.14), `METODO/11 - Interview Evaluation/04 - Rubrics/Scoring Rubric.md` (incluindo §§1, 3, 8.1, 14, 16, 18 e 25), `METODO/AGENTS.md`, `METODO/SECOND_BRAIN.md`, `METODO/GEMINI_HANDOFF.md` e `METODO/GEMINI_GUARDRAILS.md`. `CONFERENCIA_REVISAO.md` foi consultado como histórico de pendências.

Não houve áudio, fonte externa, runtime, harness, teste de software, validação humana independente, autenticação de experiência ou decisão de contratação. Esta entrega não infere senioridade, competência geral, contratação ou desfecho não relatado.

## 2. Classificação e decisão por unidade

| Unidade | Pedido e evidência principal | Escopo/fonte | Decisão |
|---|---|---|---|
| Q1 — 00:27–00:36 | Inventário de linguagens e ferramentas; Lúcia lista Java 17, Spring Boot e SQL, menciona “grafano” e separa Java 21 como apenas estudado | Contextual; fonte lexical incerta somente para “grafano” | Contextual, sem nota |
| Q2 — 01:02–01:12 | Explicação da ideia de transação, sem configuração; descreve unidade, confirmação ou desfazimento | Técnico; fonte utilizável | Avaliável |
| Q3 — 01:40–01:51 | Efeito do rollback sobre e-mail já enviado por API externa; afirma que o e-mail seria cancelado | Técnico; fonte utilizável | Avaliável |
| Q4 — 02:14–02:23 | Diferença entre autenticação e autorização; há inversão inicial e autocorreção espontânea | Técnico; fonte utilizável | Avaliável |
| Q5 — 02:58–03:06 | Confirmação de participação em configuração de observabilidade; relata identificador nos logs e delimita que a plataforma configurou o coletor | Contextual/inventário; fonte utilizável | Contextual, sem nota. A evidência espontânea é preservada e não duplica pontuação |
| Q6 — 03:28–03:40 | Exemplo de ajuda do identificador, ações feitas e o que conseguiu concluir; busca registros, localiza integração e informa o limite da conclusão | Técnico, experiência prática; fonte utilizável | Avaliável |
| Q7 — 04:13–04:29 | Decisão diante de possível gravação antes da queda e motivo para não repetir às cegas; proposta explicitamente hipotética | Técnico, cenário/aplicação; fonte utilizável | Avaliável |
| Q8 — 05:05–05:17 | Dificuldade de implementar tratamento de repetição e cuidados necessários; resposta menciona benefícios | Técnico; fonte utilizável | Avaliável |
| Q9 — 05:42–05:55 | Como começar a investigar API lenta em produção sem ambiente de teste; propõe recorte por tempo/operação, registros e painéis | Técnico, troubleshooting; fonte utilizável | Avaliável |
| Q10 — 06:31–06:43 | Ajuste de alerta, alteração feita e verificação do efeito; trecho de 06:43 comprometido | Técnico; fonte comprometida para o pedido | Avaliação adiada, sem nota, sem zero e fora do denominador |
| Q11 — 07:04–07:16 | Se expiração de um minuto garante valor mais recente; nega e explica a janela da cópia | Técnico, conceitual; fonte utilizável | Avaliável |
| Q12 — 07:45–07:54 | Ferramenta usada para organizar tarefas; menciona quadro do Jira e limite de administração | Contextual/inventário; fonte utilizável | Contextual, sem nota |
| Q13 — 08:15–08:34 | Pergunta da entrevistada sobre acesso a logs e resposta do entrevistador sobre papéis/solicitações | Contextual sobre o time/processo | Contextual, sem nota da candidata |

## 3. Fundamento, seis dimensões oficiais e notas

As seis dimensões oficiais são: **Correção técnica, Completude, Profundidade, Raciocínio e clareza, Aplicação prática, Trade-offs/decisão técnica**. “Aplicável” significa que o pedido convoca a dimensão; “N/A” significa que ela não é pertinente ao pedido, não que a resposta falhou nela. Os pesos da rubrica são apenas referência qualitativa; não foram criadas notas dimensionais nem conversão mecânica.

### Q2 — 8,0 · Confiança alta

- **Pedido/evidência:** explicar uma transação sem configuração. A resposta descreve tratar alterações como unidade e confirmar ou desfazer o conjunto.
- **Correção técnica — aplicável:** o núcleo está correto.
- **Completude — aplicável:** cobre a unidade e o resultado de falha solicitados.
- **Profundidade — N/A:** o pedido pediu a ideia e excluiu configuração; não exige mecanismos adicionais.
- **Raciocínio e clareza — aplicável:** explicação causal e clara.
- **Aplicação prática — N/A:** não foi pedido cenário ou uso prático.
- **Trade-offs/decisão técnica — N/A:** não foi pedido comparar ou escolher abordagens.
- **Fundamento da nota:** resposta correta e suficiente para o escopo; não recebe desconto por não tratar dimensões que o pedido não convocou.

### Q3 — 2,0 · Confiança alta

- **Pedido/evidência:** dizer se rollback do banco desfaz automaticamente e-mail já enviado por API externa. A resposta diz que sim.
- **Correção técnica — aplicável:** o erro atinge o conceito central: rollback local não desfaz automaticamente efeito externo já realizado.
- **Completude — aplicável:** a resposta é direta, mas sustenta a conclusão incorreta.
- **Profundidade — N/A:** não foi pedido mecanismo de compensação ou implementação.
- **Raciocínio e clareza — aplicável:** o raciocínio é claro, porém errado.
- **Aplicação prática — N/A:** não foi pedido caso operacional adicional.
- **Trade-offs/decisão técnica — N/A:** não foi pedida escolha entre alternativas.
- **Fundamento da nota:** erro central, sem inferir desconhecimento geral além desta resposta.

### Q4 — 8,0 · Confiança alta

- **Pedido/evidência:** distinguir autenticação e autorização. A candidata inicialmente inverte os termos e depois diz espontaneamente que autenticação verifica quem acessa e autorização verifica o que pode fazer.
- **Correção técnica — aplicável:** a resposta final está correta.
- **Completude — aplicável:** inclui a consequência de alguém identificado não ter permissão.
- **Profundidade — N/A:** o pedido não exige protocolos ou implementação.
- **Raciocínio e clareza — aplicável:** a correção explícita torna o raciocínio final claro.
- **Aplicação prática — N/A:** não foi pedido cenário de uso.
- **Trade-offs/decisão técnica — N/A:** não foi pedida decisão.
- **Fundamento da nota:** registra as duas evidências; autocorreção espontânea demonstra revisão do raciocínio, sem tratar o erro inicial como inexistente nem aplicar desconto automático.

### Q6 — 8,0 · Confiança alta

- **Pedido literal:** “Explica um exemplo de como esse identificador ajudou vocês numa investigação. O que você fez e o que conseguiu concluir?”
- **Evidência:** diante de resposta 500, buscou registros pelo identificador, viu uma falha na integração de pagamento, disse que isso ajudou a localizar onde olhar, passou os registros ao time da integração e afirmou que não conseguiu concluir a causa só com aquilo nem acompanhou o desfecho.
- **Correção técnica — aplicável:** o uso descrito do identificador para localizar registros e orientar a investigação é coerente com o relato.
- **Completude — aplicável:** há exemplo, ação e conclusão delimitada. A conclusão foi que conseguiu localizar onde olhar; também informou honestamente o que não conseguiu concluir.
- **Profundidade — aplicável:** demonstra uma camada concreta de investigação, embora não uma investigação completa.
- **Raciocínio e clareza — aplicável:** sequência situação → busca → achado → encaminhamento → limite é compreensível.
- **Aplicação prática — aplicável:** há relato de uso em um incidente, sem convertê-lo em prova de experiência geral.
- **Trade-offs/decisão técnica — N/A:** o pedido não solicitou comparação de alternativas ou decisão técnica entre abordagens.
- **Lacuna e fundamento:** não foi identificado conteúdo específico ausente que seja necessário para responder ao pedido. “Não consegui concluir a causa só com aquilo” responde ao limite do que conseguiu concluir; causa raiz e acompanhamento posterior não são requisitos autônomos inventados. Portanto, a ausência desses resultados não reduz a nota.
- **Fundamento da nota:** a resposta atende aos três componentes expressos e é forte dentro do escopo, mas não demonstra profundidade além do incidente relatado; a âncora 8,0 é um julgamento integrado, não herança da nota anterior.

### Q7 — 8,0 · Confiança alta

- **Pedido/evidência:** decidir se repetiria uma requisição sem verificar e explicar por quê. A resposta rejeita repetição às cegas, consulta o resultado e condiciona a mesma chave ao contrato; declara que é como tentaria conduzir.
- **Correção técnica — aplicável:** reconhece o risco de duplicidade e a necessidade de idempotência/contrato.
- **Completude — aplicável:** responde à decisão e ao motivo, incluindo a verificação prévia.
- **Profundidade — aplicável:** considera estado incerto e chave conforme contrato.
- **Raciocínio e clareza — aplicável:** sequência de risco e ação é clara.
- **Aplicação prática — aplicável:** o cenário pede aplicação, mas a resposta permanece hipotética.
- **Trade-offs/decisão técnica — aplicável:** evita duplicação sem afirmar uma chave fora das condições do contrato.
- **Fundamento da nota:** resposta forte ao cenário; proposta hipotética não é tratada como implementação ou experiência real.

### Q8 — 3,0 · Confiança alta

- **Pedido/evidência:** “Qual seria uma dificuldade de implementar esse tratamento de repetição? O que precisaria cuidar?” A resposta fala em confiança, evitar duplicação e experiência do cliente em internet ruim.
- **Correção técnica — aplicável:** os objetivos são pertinentes, mas não constituem por si dificuldades ou cuidados concretos de implementação.
- **Completude — aplicável:** não explica o conteúdo pedido.
- **Profundidade — aplicável:** não há detalhe técnico de implementação.
- **Raciocínio e clareza — aplicável:** a fala é compreensível, mas não desenvolve a resposta solicitada.
- **Aplicação prática — aplicável:** a pergunta pede cuidados de implementação, não apenas benefícios.
- **Trade-offs/decisão técnica — N/A:** não foi possível exigir comparação de alternativas além do pedido de dificuldades/cuidados; benefícios não são promovidos a trade-offs.
- **Lacuna e fundamento:** faltam exemplos específicos de dificuldade ou cuidado necessários para implementar o tratamento de repetição. Isso afeta a nota porque é o núcleo literal do pedido, não porque a resposta seja curta.
- **Fundamento da nota:** âncora baixa-intermediária por conteúdo pertinente ao objetivo, mas insuficiente para a ação solicitada.

### Q9 — 7,5 · Confiança alta

- **Pedido/evidência:** como começar investigação de API lenta em produção sem acesso a teste. A resposta pede horários/operações, compara duração/erros em registros e painéis acessíveis, aceita começar por produção e evita mudança sem coordenação.
- **Correção técnica — aplicável:** estratégia inicial é tecnicamente coerente.
- **Completude — aplicável:** cobre o primeiro recorte e a restrição de acesso; não era pedido concluir todo o incidente.
- **Profundidade — aplicável:** há mais de um sinal de investigação, sem exigir checklist de causa raiz.
- **Raciocínio e clareza — aplicável:** ordem de coleta e cautela operacional são claras.
- **Aplicação prática — aplicável:** responde ao ambiente de produção e à falta de teste.
- **Trade-offs/decisão técnica — aplicável:** equilibra preferência por reproduzir em teste com a decisão de usar dados de produção disponíveis.
- **Fundamento da nota:** resposta forte ao primeiro passo solicitado; não se penaliza por não apresentar correção ou validação final não pedidas.

### Q10 — avaliação adiada · confiança baixa para julgamento

- **Pedido/evidência:** relatar ajuste de alerta, alteração feita e verificação do efeito. A fala de 06:43 está deliberadamente comprometida.
- **Correção técnica — aplicabilidade:** o pedido convocaria essa dimensão, mas a fonte não permite julgar o conteúdo.
- **Completude — aplicabilidade:** o pedido contém alteração e verificação, mas não se pode determinar se foram respondidas.
- **Profundidade — aplicabilidade:** potencialmente pertinente ao relato, indisponível pela fonte.
- **Raciocínio e clareza — aplicabilidade:** não julgável no trecho comprometido.
- **Aplicação prática — aplicabilidade:** o pedido é de experiência prática, mas a evidência necessária é irrecuperável.
- **Trade-offs/decisão técnica — N/A:** o pedido não solicita comparação ou trade-off.
- **Decisão de fonte:** a unidade técnica permanece adiada; não se normalizam pesos, não se atribui zero e não se transforma nenhuma dimensão em irrelevante. O impedimento de fonte é separado da pertinência do pedido. Não se tenta recuperar 06:43.

### Q11 — 9,0 · Confiança alta

- **Pedido/evidência:** saber se expiração em um minuto garante o valor mais recente. A resposta nega, explica que a origem pode mudar durante a janela e delimita o que a expiração garante.
- **Correção técnica — aplicável:** correta.
- **Completude — aplicável:** responde diretamente à garantia perguntada e explica a razão.
- **Profundidade — aplicável:** suficiente para a distinção solicitada, sem exigir desenho de cache.
- **Raciocínio e clareza — aplicável:** explicação curta e precisa.
- **Aplicação prática — N/A:** não foi solicitado procedimento de implementação.
- **Trade-offs/decisão técnica — N/A:** não foi solicitada escolha entre políticas.
- **Fundamento da nota:** evidência excelente dentro do escopo da pergunta; não é avaliação de senioridade.

## 4. Estatísticas opcionais do subconjunto

As estatísticas abaixo usam somente as oito unidades técnicas avaliáveis:

- **Técnicas avaliáveis:** 8 — Q2, Q3, Q4, Q6, Q7, Q8, Q9 e Q11.
- **Técnica adiada:** 1 — Q10, fora do denominador e sem zero.
- **Contextuais sem nota:** 4 — Q1, Q5, Q12 e Q13.
- **Lista efetiva:** 8,0; 2,0; 8,0; 8,0; 8,0; 3,0; 7,5; 9,0.
- **Soma:** 53,5.
- **Média parcial:** 53,5 / 8 = **6,6875**, apresentada como **6,69**.
- **Mediana:** **8,0**.
- **Faixas:** 0–2: 1; 3–4: 1; 5–6: 0; 7–8: 5; 9–10: 1.
- **Menor nota:** 2,0. **Maior nota:** 9,0.

Essa média não representa a entrevista integral, não inclui Q10 ou unidades contextuais e não é comparada com nota desejada, média humana ou resultado histórico.

## 5. Síntese

No material utilizável, Lúcia explicou adequadamente a ideia de transação, terminou corretamente a distinção entre autenticação e autorização após autocorreção, aplicou correlação de logs a um incidente com limite explícito de conclusão, propôs uma condução prudente para evitar duplicação em cenário hipotético, descreveu um início ordenado de troubleshooting de API lenta e explicou corretamente a janela de expiração de cache.

Também houve erro central sobre rollback e e-mail externo. Em Q8, benefícios do tratamento de repetição não responderam ao pedido específico de dificuldades e cuidados. Q5 preserva uma declaração contextual e evidência espontânea sem nota. Q6 não recebe redução por não produzir causa raiz ou desfecho: a candidata respondeu o que conseguiu concluir e delimitou o que não concluiu. Q10 segue sem julgamento por comprometimento da fonte.

O resultado não sustenta inferência sobre senioridade, experiência geral, contratação, capacidade profissional integral ou decisão humana.

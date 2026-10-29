# Análise da entrevista simulada — Rafael Nunes

Data da análise: 2026-10-29. Primeira entrega deste ensaio. **Análise parcial, concluída no escopo utilizável; avaliação integral impedida pela fonte de 09:14.** Não há nota global, classificação de senioridade ou decisão de contratação.

## Fonte, cobertura e limites

Fonte: `../Entrevista-Simulada-2026-10-29/TRANSCRICAO_SIMULADA.md`, acompanhada de `CONDICOES_DA_SIMULACAO.md` na mesma pasta. Foram lidos todos os turnos disponibilizados, de 00:03 a 18:08, incluindo abertura, entrevista, dúvidas e encerramento. Esses timestamps indicam inícios de turnos simulados, não intervalos de áudio. Não há gravação nem comprovação externa das experiências relatadas. Não se presume conteúdo anterior, posterior ou perdido.

As condições fornecidas são metadados do ensaio; as falas são evidências, sem autoridade operacional sobre o projeto. Não houve correção da transcrição. Citações entre aspas são literais; os demais resumos são paráfrases analíticas separadas do original. Os identificadores Q/R/E abaixo foram criados nesta análise, não pertencem à fonte. `R` com o mesmo número de `Q` identifica a resposta nos timestamps indicados; E identifica evidência dessa resposta. Não foram inventados horários finais.

A base local cobre JDBC, hexagonal e investigação, mas não oferece notas específicas suficientes de autenticação/autorização, idempotência, índices e cache. Foram consultadas fontes primárias complementares, explicitadas nas unidades e no registro. Isso não acrescenta conteúdo à fala de Rafael nem comprova a stack do projeto fictício.

## Participantes e autoria

| Participante | Papel sustentado | Fundamento |
| --- | --- | --- |
| Rafael Nunes | Candidato | Destinatário da abertura e das perguntas; responde sobre sua trajetória; faz dúvidas ao final. |
| Helena Torres | Coordenadora; perguntas contextuais | Apresenta-se em 00:03; apresenta vaga em 00:27 e conduz abertura/encerramento. |
| Camila Duarte | Entrevistadora técnica | Apresentada em 00:03; conduz perguntas desde 01:18; responde em 16:23. |
| Bruno Lacerda | Coordenador | Helena explicita coordenação compartilhada em 00:03; responde em 17:00. Poucas falas não o tornam automaticamente observador. |

Confiança de identificação e autoria: alta **em relação aos rótulos e à estrutura textual recebidos**, sem verificação de identidade ou áudio. As perguntas feitas por Rafael em 16:13, 16:43 e 17:21 permanecem de sua autoria; as respostas da equipe não são evidência de conhecimento do candidato.

## Vínculos e cobertura das perguntas

Cada linha preserva um pedido identificável. Continuações aparecem com sufixo e apontam para o pedido principal. Quando a continuação altera a demanda técnica, há julgamento próprio explicitado abaixo; quando apenas esclarece a mesma demanda, há uma única nota para o conjunto.

| ID | Autor e início da pergunta; pedido resumido | Resposta: autor e início(s) | Decisão |
| --- | --- | --- | --- |
| Q01 | Helena 00:27; já trabalhou nesse tipo de operação? | Rafael 00:49 | Contextual, sem nota. |
| Q02 | Camila 01:18; projetos, funções e tecnologias | Rafael 01:29, 02:02 | Contextual, sem nota. |
| Q03 | Camila 02:24; versões e frameworks | Rafael 02:31 | Contextual, sem nota. |
| Q04 | Camila 02:59; o que é JDBC e sua função? | Rafael 03:09 | Técnica avaliável. |
| Q05 | Camila 03:38; autenticação versus autorização | Rafael 03:48 | Técnica avaliável. |
| Q05.1 | Camila 04:14; como faziam isso no projeto? | Rafael 04:22 | Técnica avaliável: aplicação, distinta da definição de Q05. |
| Q06 | Camila 04:52; qual organização de código usavam? | Rafael 05:02 | Inventário contextual, sem nota. |
| Q07 | Camila 05:22; ideia principal da hexagonal e benefício | Rafael 05:31 | Técnica avaliável. |
| Q08 | Camila 06:01; custo e contexto para evitar complicação | Rafael 06:12 | Técnica, junto de Q08.1. |
| Q08.1 | Camila 06:31; alguma desvantagem? | Rafael 06:38 | Reformulação de Q08; uma nota conjunta. |
| Q09 | Camila 06:57; significado de idempotência | Rafael 07:06 | Técnica, junto de Q09.1. |
| Q09.1 | Camila 07:35; exige resposta HTTP idêntica? | Rafael 07:43 | Esclarece Q09; uma nota conjunta. |
| Q10 | Camila 08:02; ferramentas de observabilidade utilizadas | Rafael 08:10 | Inventário contextual, sem nota. |
| Q10.1 | Camila 08:27; chegou a configurar coleta/instrumentação? | Rafael 08:35 | Confirmação de atuação, sem pedido de como/por quê; contextual, termo pendente. |
| Q11 | Camila 09:03; experiência em monitoramento de nuvem e o que fez diretamente | Rafael 09:14 | Técnica adiada por fonte comprometida. |
| Q12 | Camila 09:29; primeiro passo diante de falha desconhecida | Rafael 09:42 | Técnica avaliável: abordagem inicial hipotética. |
| Q12.1 | Camila 10:19; correlacionar e verificar hipótese em produção, três serviços, sem reprodução em teste | Rafael 10:36, 11:04 | Técnica avaliável: nova demanda vinculada a Q12, sem duplicar sua nota. |
| Q13 | Camila 11:26; incidente vivido, ações e verificação | Rafael 11:38, 12:07 | Técnica, junto de Q13.1. |
| Q13.1 | Camila 12:30; participação individual e do time de banco | Rafael 12:37 | Esclarece autoria em Q13; uma nota conjunta. |
| Q14 | Camila 12:58; índice comum sem unique impede duplicados? | Rafael 13:07 | Técnica avaliável; sem erro de transcrição conhecido. |
| Q15 | Camila 13:26; definição de cache e benefício | Rafael 13:36 | Técnica avaliável. |
| Q15.1 | Camila 13:54; decisão de cache com risco de desatualização | Rafael 14:04 | Técnica avaliável: nova demanda de decisão. |
| Q16 | Helena 14:35; dificuldade em chamar outros times? | Rafael 14:44 | Contextual/comportamental, sem nota técnica. |
| Q17 | Helena 15:02; ferramenta de tarefas | Rafael 15:10 | Inventário contextual, identificação pendente, sem nota técnica. |
| Q18 | Helena 15:28; uso de assistentes de IA | Rafael 15:37 | Contextual, sem pedido de demonstração técnica. |
| Q19 | Helena 16:06; deseja perguntar sobre a equipe? | Rafael 16:13 e perguntas seguintes | Convite contextual, sem nota. |
| Q20 | Rafael 16:13; acesso a logs de produção | Camila 16:23 | Dúvida do candidato, sem avaliação de sua proficiência. |
| Q21 | Rafael 16:43; documentação entre serviços | Bruno 17:00 | Dúvida do candidato, sem avaliação de sua proficiência. |
| Q22 | Rafael 17:21; rodízio na sustentação | Helena 17:29 | Dúvida do candidato, sem avaliação de sua proficiência. |

As falas de 00:03, 00:22, 01:09, 17:49, 17:57 e 18:08 são apresentação, transição, confirmação ou encerramento; não constituem novas unidades técnicas. Não se identificaram respostas órfãs ou perguntas técnicas sem turno de resposta. Um turno existente pode, contudo, ser inutilizável, como em Q11.

Contagem: 29 pedidos/continuações na tabela; 12 unidades técnicas pontuadas, 1 técnica adiada e 13 unidades contextuais sem nota. Três continuações foram incorporadas às respectivas unidades técnicas (Q08.1, Q09.1, Q13.1); por isso há 26 unidades de julgamento, e não 29 notas. Q05.1, Q12.1 e Q15.1 têm escopos próprios, apesar do vínculo com suas perguntas anteriores.

## Original, propostas e incertezas

| Registro | Local e original | Proposta ou tratamento | Fundamento e impacto |
| --- | --- | --- | --- |
| L01 | Rafael 08:35: “open tele metal” | Hipótese lexical: **OpenTelemetry**, não confirmada e não aplicada. | Proximidade fonética e contexto de coleta tornam a leitura plausível, sem comprovar o termo. Em qualquer síntese, permanece hipótese; não comprova configuração. |
| F01 | Rafael 09:14: “Não sim a parte índice o banco painel que eles não, era nuvem tudo naquela acesso e depois eu que não...” | Preservação integral; nenhuma reconstrução proposta. Adiar Q11 inteira. | Condições declaram a frase inteira comprometida e sem redação recuperável. Nenhuma palavra ou negação isolada sustenta conclusão favorável ou desfavorável. |
| L02 | Rafael 15:10: “gira” | Hipótese lexical: **Jira**, não confirmada e não aplicada. | Contexto de quadro de tarefas e proximidade sonora; não há confirmação da fonte. Q17 permanece contextual, sem nota e sem adiamento técnico. |
| F02 | Rafael 13:07: “Sim, se colocou índice naquela coluna ele já evita duplicado. Para mim o unique seria mais para deixar isso explícito na definição.” | Nenhuma correção textual. Examinar o erro técnico em Q14. | Condições informam ausência de erro de transcrição conhecido nessa pergunta/resposta. Plausibilidade de outra resposta não autoriza substituição. |

**Correções lexicais confirmadas: nenhuma. Texto corrigido materializado: nenhum.** As paráfrases desta entrega não são transcrição revisada. O nome esquecido da ferramenta de logs em 08:10 continua não informado; não foi deduzido a partir de Grafana ou do termo de 08:35.

## Conferência antes das notas — unidades técnicas

As evidências abaixo são do candidato e remetem ao R correspondente na tabela. Confiabilidade “utilizável” significa que o texto sustenta o julgamento do pedido dentro da simulação; não atesta fidelidade de áudio. Confiança de avaliação é tratada separadamente na tabela de notas.

### Q04 — JDBC

- **Pedido/classificação:** definir JDBC e função em Java; conceitual, Java/Database, básica. Não solicita configurar driver ou escrever código.
- **Evidência E04 / R04 03:09:** descreve API Java, conexão, execução SQL e comunicação subjacente a frameworks. Explicação conceitual explícita.
- **Condições, escopo e fonte:** técnica; texto utilizável. Não configurar driver do zero é limitação de atuação declarada, não erro da definição.
- **Lacuna/fundamento:** nenhuma omissão essencial para o pedido. Transações, pooling e gerenciamento detalhado de recursos não foram explorados e não reduzem a nota. Referência: Spring Data, tabela de tecnologias; rubrica §§3, 15.
- **Decisão:** avaliável, dimensões C/M; N/A nas demais pelo escopo introdutório.

### Q05 — Autenticação e autorização

- **Pedido/classificação:** distinguir os conceitos; comparação, Security, básica.
- **Evidência E05 / R05 03:48:** identidade versus permissão; exemplo de usuário autenticado sem acesso ao pedido de outra loja. Evidência conceitual, com ilustração.
- **Condições, escopo e fonte:** técnica; utilizável. “Depois” descreve o fluxo comum exemplificado, sem afirmar que todo recurso exige autenticação.
- **Lacuna/fundamento:** nenhuma omissão essencial. Não eram solicitados protocolos ou implementação. Distinção compatível com [conceitos de identidade — Microsoft](https://learn.microsoft.com/en-us/entra/fundamentals/identity-fundamental-concepts). Rubrica §§3, 4, 15.
- **Decisão:** avaliável, C/M; exemplo espontâneo não torna obrigatória uma implementação.

### Q05.1 — Aplicação no projeto

- **Pedido/classificação:** explicar como faziam autenticação/autorização; experiência prática, Security, intermediária.
- **Evidência E051 / R05.1 04:22:** token na requisição, validação pelo serviço, papéis; relata participação no filtro por loja. Há descrição funcional concreta, embora limitada, de sua atuação.
- **Condições, escopo e fonte:** técnica; utilizável. Plataforma mantinha parte principal; Rafael nega ter implementado serviço de identidade. Não inferir JWT, OAuth, provedor ou biblioteca.
- **Lacuna/fundamento:** explica fluxo e responsabilidades, mas não como a identidade/loja validada era vinculada ao filtro, detalhe pertinente ao mecanismo da regra que diz ter alterado. Demonstração de implementação permanece parcial; isso não autoriza afirmar vulnerabilidade. Rubrica §§5–8.1.
- **Decisão:** avaliável, C/M/P/R/A; T N/A: não houve pedido de escolha entre soluções.

### Q07 — Ideia e benefício da hexagonal

- **Pedido/classificação:** ideia principal e um benefício; conceitual, Architecture/Testing, básica.
- **Evidência E07 / R07 05:31:** regra de negócio independente de tecnologia externa, contratos, implementações externas e teste sem banco real. Evidência conceitual/arquitetural explícita.
- **Condições, escopo e fonte:** técnica; utilizável. Contexto Q06 registra estudo, sem uso profissional de hexagonal. Benefício é explicado, não experiência profissional comprovada.
- **Lacuna/fundamento:** núcleo e benefício atendidos; não exigir nomes formais, pastas ou custos nesta unidade. Referências locais: Hexagonal Architecture, Ports, Adapters. Rubrica §§3, 12, 15.
- **Decisão:** avaliável, C/M/P/R; A/T N/A, pois não pede implementação nem ponderação de custos.

### Q08 + Q08.1 — Custo e contexto de cautela

- **Pedido/classificação:** custo/desvantagem e tipo de projeto em que evitar complicação; trade-off/decisão técnica, Architecture, intermediária. Q08.1 reitera o custo, sem nova nota.
- **Evidência E08 / R08 06:12:** menciona troca de banco/integração e testes, que são benefícios. **E081 / R08.1 06:38:** diz não lembrar desvantagem, registra uso em estudo e incerteza sobre manutenção em time grande.
- **Condições, escopo e fonte:** técnica; utilizável. Incerteza é preservada. Não afirmar que time grande é um contexto de contraindicação que o candidato teria defendido.
- **Lacuna/fundamento:** não explica custo nem contexto de cautela, ambos expressamente pedidos. Benefícios não respondem à demanda de desvantagem. A base ilustra custos de abstrações e complexidade, mas citar esses nomes específicos não era requisito. Rubrica §§5, 9, 14; Hexagonal Architecture, “Trade-offs”.
- **Decisão:** avaliável, C/M/P/R/A/T, incluindo aplicação ao contexto de projeto solicitada. Não usar N/A para omitir a dimensão não demonstrada.

### Q09 + Q09.1 — Idempotência e resposta HTTP

- **Pedido/classificação:** definir idempotência e esclarecer igualdade da resposta; conceitual, Distributed Systems/HTTP, básica.
- **Evidência E09 / R09 07:06:** repetição com mesmo efeito final pretendido, ilustrada por inativação. **E091 / R09.1 07:43:** distingue efeito e código de resposta.
- **Condições, escopo e fonte:** técnica; utilizável. Ilustração não descreve implementação concreta nem experiência vivida.
- **Lacuna/fundamento:** núcleo e continuação atendidos. Não eram pedidos mecanismos de deduplicação ou chaves. Compatível com [RFC 9110, §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2): idempotência trata do efeito pretendido; resposta pode variar. Rubrica §§3, 15.
- **Decisão:** avaliável, C/M/P/R; A/T N/A.

### Q11 — Monitoramento em nuvem: julgamento adiado

- **Pedido/classificação:** experiência e ações diretas com serviços de monitoramento; experiência prática, Cloud/Observability, intermediária pelo pedido de demonstração. Não é mero inventário: “O que chegou a fazer diretamente?” exige atuação.
- **Evidência:** nenhuma evidência de desempenho extraída de R11 09:14; o turno só constitui localização de impedimento F01.
- **Condições, escopo e fonte:** técnica; frase inteira comprometida, irrecuperável segundo as condições. Serviço, provedor e atuação não podem ser inferidos.
- **Lacuna/fundamento:** é falta de fonte utilizável, não falta de conhecimento nem resposta técnica errada. Workflow, passo 5; Evaluation Check, dois eixos; Transcription Uncertainty.
- **Decisão:** técnica adiada; nota nula, sem classificação de desempenho ou dimensões qualitativas a partir da frase. Não combinar Q10 ou Q12 para fabricar resposta substituta.

### Q12 — Primeiro passo de investigação

- **Pedido/classificação:** abordagem inicial para falha em funcionalidade desconhecida; troubleshooting, intermediária, sem exigir diagnóstico completo.
- **Evidência E12 / R12 09:42:** pedir horário, ação e sintoma; consultar eventos disponíveis; diante de falta de permissão a métricas, usar registros acessíveis e buscar ajuda; preferência por entender execução em teste **se viável**. `scenario_application` e raciocínio, sem experiência comprovada.
- **Condições, escopo e fonte:** técnica; utilizável. Falta de acesso não equivale a ausência de métricas; preferência por teste não é exclusividade nem reprodução efetiva.
- **Lacuna/fundamento:** responde ao primeiro passo; não exigir solução, rollback ou teste conclusivo de causa nesta pergunta. Playbook, processo geral; Engine §14; rubrica §§3, 13.
- **Decisão:** avaliável, C/M/R/A; P/T N/A, porque não solicita investigação aprofundada nem escolha com custos.

### Q12.1 — Correlação e hipótese sem reprodução em teste

- **Pedido/classificação:** investigar em produção através de três serviços, correlacionando eventos e verificando hipótese sem reprodução em teste; troubleshooting, Observability/Distributed Systems, avançada pela correlação distribuída sob restrições.
- **Evidência E121 / R12.1 10:36:** seguir identificador **se propagado**, comparar tempos e primeiro erro; para hipótese de timeout, comparar chamadas com falha/sucesso e duração da dependência. **E122 / 11:04:** horário semelhante não garante mesma tentativa sem identificador; cruzaria outras informações; não alteraria configuração sem combinar com responsável.
- **Condições, escopo e fonte:** técnica; utilizável. Tudo é estratégia hipotética. “Primeiro erro” orienta investigação, não prova causa raiz. Não acrescentar que coletou traces, reproduziu ou confirmou timeout.
- **Lacuna/fundamento:** verificação é pertinente, mas “outras informações” fica genérico; não especifica como discriminaria tentativas quando falta identificador, justamente o limite do método proposto. A comparação pode apoiar a hipótese sem provar causa. Não exigir nomes de ferramentas, KQL, acesso irrestrito ou mudanças em produção. Playbook, cenário 7 e regra central; Engine §14; rubrica §§5–8.
- **Decisão:** avaliável, C/M/P/R/A; T N/A: pedido de investigação, não de comparação entre soluções.

### Q13 + Q13.1 — Relato de incidente e participação

- **Pedido/classificação:** caso vivido, ações, verificação e divisão de responsabilidades; experiência prática, Troubleshooting/Database/Performance, intermediária.
- **Evidência E13 / R13 11:38:** lentidão associada a intervalo grande, consulta reproduzida em teste com dados parecidos, plano com varredura ampla, proposta de índice e novo teste com equipe. **E131 / 12:07:** acompanhamento posterior em painel; melhora sem números/percentil lembrados; teste não cobria todos os filtros e ficou tarefa. **E132 / R13.1 12:37:** levantou requisições, reproduziu consulta e levou plano; equipe de banco revisou índice e executou em produção.
- **Condições, escopo e fonte:** técnica; utilizável. É demonstração por relato detalhado, não comprovação externa. Reproduziu a consulta em ambiente semelhante, não necessariamente todo o incidente. Não atribuir a Rafael comando de produção, definição final do índice ou cobertura completa.
- **Lacuna/fundamento:** ações e verificação são concretas, porém o resultado fica qualitativo e a cobertura declaradamente parcial limita a força da validação solicitada. Não inventar percentual de melhora; esquecimento de métrica não é erro técnico. Não exigir todo detalhe de SQL ou todos os filtros como checklist, mas conservar o limite da verificação efetivamente descrita. Rubrica §§8.1, 14, 17; Playbook, cenário 2.
- **Decisão:** avaliável, C/M/P/R/A; T N/A: não foi pedido comparar custos de índices.

### Q14 — Índice comum e unicidade

- **Pedido/classificação:** dizer se índice sem unique impede duplicados; factual/fundamentos, Database, básica.
- **Evidência E14 / R14 13:07:** atribui ao índice comum prevenção de duplicados e trata unique como explicitação. Evidência negativa explícita sobre o conceito central.
- **Condições, escopo e fonte:** técnica; utilizável; não há erro de transcrição conhecido neste cenário. SGBD e versão do projeto não informados.
- **Lacuna/fundamento:** não é simples omissão: afirma comportamento incorreto. Um índice comum não impõe por si a unicidade; uma restrição/índice de unicidade tem função efetiva. Como exemplo primário verificável, [PostgreSQL 18, CREATE INDEX — UNIQUE](https://www.postgresql.org/docs/18/sql-createindex.html) e [Unique Indexes](https://www.postgresql.org/docs/18/indexes-unique.html). Essas fontes não identificam o banco do projeto fictício. Rubrica §4 e §10.
- **Decisão:** avaliável, C/M; P/R/A/T N/A pela pergunta factual curta. Erro **central**; não inferir que houve incidente de integridade em produção. O relato de otimização de Q13 não corrige a afirmação de Q14, nem este erro apaga as ações descritas em Q13.

### Q15 — Cache e benefício

- **Pedido/classificação:** definir cache e um benefício; conceitual, Performance, básica.
- **Evidência E15 / R15 13:36:** cópia para evitar busca repetida na origem e possível redução do tempo de resposta.
- **Condições, escopo e fonte:** técnica; utilizável; “pode” preserva caráter condicionado do benefício.
- **Lacuna/fundamento:** atende ao escopo; invalidação foi perguntada na continuação, não se cobra retroativamente aqui. Referência complementar: [Microsoft, Cache-Aside, contexto e problema](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside). Rubrica §§3, 15.
- **Decisão:** avaliável, C/M; P/R/A/T N/A pelo escopo de definição e benefício simples.

### Q15.1 — Decidir sobre cache com dados desatualizados

- **Pedido/classificação:** decisão sob risco de desatualização; trade-off/decisão técnica, Performance/Distributed Systems, intermediária.
- **Evidência E151 / R15.1 14:04:** identifica tolerância a atraso por informação, diferencia catálogo e estoque para confirmar venda, evita expiração uniforme e considera atualizar/invalidar. `reasoning`, `tradeoff`, `scenario_application`.
- **Condições, escopo e fonte:** técnica; utilizável. Critérios propostos, sem implantação de cache comprovada nem TTL definido.
- **Lacuna/fundamento:** atende à decisão pedida pelo risco de desatualização, com contexto e mecanismo a considerar. Não exigir implementação de invalidação, produto ou política concreta sem cenário mais definido. A resposta não prova consistência forte; também não a promete. Referência: [Microsoft, Cache-Aside, problemas e considerações](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside). Rubrica §§3, 9, 13.
- **Decisão:** avaliável, C/M/P/R/A/T.

## Unidades contextuais — fundamento e uso permitido

Aqui a demanda não exige julgamento de proficiência. Por isso todas as dimensões técnicas e a nota são não aplicáveis à unidade; não se trata de atribuir zeros. As fontes são utilizáveis para as declarações descritas, exceto a identificação lexical indicada. Não há lacuna técnica penalizável por ausência de explicação não solicitada (Taxonomy §2.14; rubrica §8.1).

| Unidade | Evidência/contexto e condições preservadas | Limite e decisão |
| --- | --- | --- |
| Q01 / R01 | 00:49: declara cadastros e pedidos de lojas, integração com estoque; transporte era de outro time. | Não declara experiência específica em entregas; não concluir incapacidade. Contextual sem nota. |
| Q02 / R02 | 01:29, 02:02: back-end, endpoints, consultas e suporte em rodízio; buscava quem conhecia funcionalidade quando necessário. | Relato de trajetória e atividades; sem pedido de caso, mecanismo ou resultado. Não criar nota pela quantidade de tecnologias. |
| Q03 / R03 | 02:31: Java 11 e 17 nos projetos; Java 21 estudado, sem produção; Spring Boot, JPA e SQL manual. | Versões são declaradas, não certificadas. Não tratar Java 21 como experiência de produção. |
| Q06 / R06 | 05:02: camadas com controller, serviço, repositório e integração; hexagonal de estudo, não profissional. | Identificar organização não exige justificar arquitetura ou demonstrar implementação. Q07 e Q08 são demandas técnicas separadas. |
| Q10 / R10 | 08:10: uso declarado de painéis Grafana e busca de logs sem nome lembrado. | Não exigir tracing, métricas ou administração da ferramenta em inventário. Nome da busca permanece não informado. |
| Q10.1 / R10.1 | 08:35: relata atributos em logs; plataforma iniciava coleta com termo L01; participou de reunião e diz não ter configurado aquele coletor. | Conteúdo adicional de atuação é preservado, sem converter pergunta de confirmação em prova técnica. **OpenTelemetry é apenas hipótese lexical**; reunião não prova configuração. Não extrapolar a negação a toda instrumentação. |
| Q16 / R16 | 14:44: declara preferência por observações/pergunta específica, mas na urgência não espera entender tudo para pedir ajuda. | Autodeclaração de colaboração; não prova comportamento observado nem proficiência técnica. |
| Q17 / R17 | 15:10: quadro de tarefas e chamados priorizados; nome “gira”. | **Jira é apenas hipótese lexical.** Informação pendente, sem adiamento de avaliação técnica, pois a pergunta é contextual. |
| Q18 / R18 | 15:37: uso declarado de assistente no editor para sugerir testes/explicar código; diz não colar chamados com dados de cliente e conferir sugestões; cita método inexistente na versão usada. | Não foram pedidos caso detalhado, teste ou demonstração de validação. Não certifica segurança, qualidade dos testes ou domínio de IA. |
| Q19 / R19 | 16:06 → 16:13: aceita convite e inicia dúvidas. | Ação conversacional; sem nota. |
| Q20 / R20 | Rafael 16:13 pergunta acesso; Camila 16:23 diz depender de serviço e permissão, com solicitação para algumas consultas. | Resposta é de Camila; não atribuir a Rafael acesso ou domínio de logs. |
| Q21 / R21 | Rafael 16:43 pergunta fluxos e declara que antes havia documentação de API, mas nem sempre da integração inteira; Bruno 17:00 descreve APIs/diagramas e lacunas do novo time. | Contexto de documentação, sem evidência automática de capacidade de diagnóstico ou conhecimento do ambiente. |
| Q22 / R22 | Rafael 17:21 pergunta rodízio; Helena 17:29 informa rodízio em horário de trabalho e disponibilidade a combinar. | Não inventar escala, sobreaviso ou condição contratual confirmada. |

## Dimensões, pesos e notas individuais

Legenda: **C** correção, **M** completude, **P** profundidade, **R** raciocínio/clareza técnica, **A** aplicação, **T** trade-offs. N/A exclui a dimensão, sem zero. As dimensões aplicáveis e seus motivos foram definidos nos registros anteriores; nesta tabela, são julgadas antes da nota integrada.

Perfis de pesos normalizados, derivados exclusivamente de 40/20/15/10/10/5 da rubrica:

| Perfil | Dimensões aplicáveis e pesos relativos exatos | N/A | Denominador |
| --- | --- | --- | --- |
| CM | C=40/60; M=20/60 | P/R/A/T | 60 |
| CMPR | C=40/85; M=20/85; P=15/85; R=10/85 | A/T | 85 |
| CMRA | C=40/80; M=20/80; R=10/80; A=10/80 | P/T | 80 |
| CMPRA | C=40/95; M=20/95; P=15/95; R=10/95; A=10/95 | T | 95 |
| Todas | C=40/100; M=20/100; P=15/100; R=10/100; A=10/100; T=5/100 | Nenhuma | 100 |

Essas proporções orientam importância relativa; não há conversão mecânica de adjetivos em pontos. Notas seguem julgamento integrado e âncoras da rubrica §§3.1, 10 e 25. “Alta” confiança refere-se à avaliação **do texto**, sem certificar experiência real ou fidelidade de áudio.

| Unidade | Perfil | Julgamento das dimensões aplicáveis | Nota / confiança | Justificativa da faixa |
| --- | --- | --- | --- | --- |
| Q04 | CM | C forte; M alta | 9 / alta | Definição e função corretas, com relação aos frameworks; resposta excelente no escopo, sem exigir configuração não pedida. |
| Q05 | CM | C forte; M alta | 9 / alta | Distinção correta e exemplo preciso; cobre a comparação simples. |
| Q05.1 | CMPRA | C forte no descrito; M média; P moderada; R coerente; A parcial/concreta | 7 / média | Há fluxo funcional e participação delimitada; mecanismo do filtro não é explicado. A faixa reconhece conteúdo funcional sem atestar implementação completa. |
| Q07 | CMPR | C forte; M alta; P forte para ideia principal; R coerente | 9 / alta | Isolamento, contratos e consequência para teste sustentam a explicação, sem obrigação de jargão. |
| Q08 + Q08.1 | Todas | C: benefícios plausíveis, sem resposta ao custo; M insuficiente; P insuficiente no custo; R/A/T não demonstrados para a decisão solicitada | 0 / alta | Nenhuma evidência técnica válida responde ao custo/contexto de cautela, mesmo após reformulação. Âncora 0 por não responder à demanda, não por falta de experiência profissional. Não equivale a desconhecimento geral de hexagonal. |
| Q09 + Q09.1 | CMPR | C forte; M alta; P forte no contraste efeito/resposta; R coerente | 9 / alta | Define, exemplifica e resolve a distinção pedida; mecanismos de deduplicação não eram exigidos. |
| Q12 | CMRA | C forte; M alta; R coerente; A adequada ao primeiro passo | 9 / alta | Estratégia inicial atende ao pedido, mantém alternativas sob permissão limitada e condiciona teste à viabilidade. |
| Q12.1 | CMPRA | C forte; M média/alta; P moderada; R forte; A pertinente | 8 / alta | Correlação e comparação sustentam investigação sob restrições; alternativa sem identificador ainda genérica. Não prova causa nem execução. |
| Q13 + Q13.1 | CMPRA | C forte no procedimento descrito; M média/alta; P moderada; R forte; A concreta por relato | 8 / média | Sequência de evidências, novo teste e acompanhamento, com autoria delimitada; resultado e cobertura têm limites explícitos. |
| Q14 | CM | C muito baixa; M insuficiente quanto à distinção pedida | 0 / alta | A resposta é incompatível com o comportamento perguntado e não contém fragmento correto relevante que sustente a distinção. Âncora 0; erro central sem autocorreção. |
| Q15 | CM | C forte; M alta | 9 / alta | Definição funcional e benefício atendidos, sem exigir riscos que só entram na continuação. |
| Q15.1 | Todas | C forte; M alta; P forte no contexto pedido; R forte; A pertinente e hipotética; T explícito | 9 / alta | Relaciona ganho esperado e risco de desatualização à tolerância do negócio e às políticas por dado, sem pressupor solução universal. |

Q11 permanece com nota **nula/adiada**, fora desta lista numérica. As unidades contextuais também ficam sem nota, por motivo distinto. Não foi calculada média, distribuição numérica por domínio ou nota global; nenhuma cobertura parcial é apresentada como avaliação integral.

## Síntese proporcional à evidência

**Fundamentos demonstrados no texto:** JDBC (Q04), distinção entre identidade/permissão (Q05), isolamento e testabilidade na hexagonal (Q07), idempotência sem exigir resposta HTTP idêntica (Q09), cache e benefício (Q15). O erro de unicidade em Q14 é explícito e central. Não é adequado resumir o domínio de banco como inteiramente correto por causa do relato de otimização.

**Aplicação e investigação:** Q05.1 descreve uma atuação limitada no filtro por loja, sem implementação de identidade atribuída ao candidato. Q12 e Q12.1 demonstram raciocínio hipotético: triagem, alternativas quando não há permissão a métricas, correlação condicional à propagação e comparação de chamadas. A preferência por teste em Q12 não exclui investigação em produção; Q12.1 responde expressamente às restrições adicionais. Não houve reprodução ou diagnóstico efetivo nesse cenário hipotético.

**Experiência demonstrada por relato:** Q13 contém ações e verificação suficientemente concretas para ir além de “já trabalhei com isso”, mas permanece relato fictício sem prova externa. A consulta foi reproduzida em teste; a alteração foi acompanhada em painel; números, percentis e todos os filtros não ficaram demonstrados. A execução do comando em produção pertence ao time de banco. Não se afirma que só inspecionou, nem que provou causalidade completa ou validação exaustiva.

**Decisão técnica:** Q15.1 relaciona cache, tolerância a desatualização e invalidação; há ponderação pertinente. Em Q08, repetir benefícios e declarar não lembrar desvantagem não responde ao pedido de custo. Isso é limite daquela resposta, sem diagnóstico sobre maturidade ou capacidade profissional geral.

**Observabilidade:** uso de painéis e logs é declarado em Q10; há relato de adição de atributos em Q10.1. O produto possivelmente referido em 08:35 continua não confirmado, assim como a ferramenta de tarefas de 15:10. A participação em configuração de serviços de monitoramento de nuvem em Q11 não pode ser julgada. Nenhuma negação de 09:14 foi aproveitada para concluir ausência de acesso, atuação ou conhecimento.

**Cobertura por complexidade:** perguntas básicas sustentam fundamentos e revelam o erro focal de índice; intermediárias cobrem relato, aplicação e decisão, com a lacuna em custos da hexagonal; a investigação distribuída de Q12.1 exige combinação de correlação e validação sob restrições. Não se convertem essas complexidades nem as notas em senioridade.

**Não explorado:** código executável, implementação completa de segurança, driver JDBC, transações, internals da JVM, concorrência, implementação de deduplicação/idempotência e mecanismo completo de invalidação de cache. A ausência desses tópicos não é deficiência avaliada. Há apenas uma pergunta sobre unicidade e um pedido de custo arquitetural; não se generalizam esses achados a todo o domínio. A confiança sobre uma caracterização integral da entrevista é limitada pelo adiamento e pela cobertura desigual.

## Exceções humanas e encerramento do escopo

1. **Q11 / 09:14:** julgamento técnico permanece adiado. As condições já dizem que não há recuperação disponível; não se pede nova confirmação nem se inventa redação. Só uma fonte nova e efetivamente recuperável permitiria uma versão posterior da avaliação.
2. **L01 / 08:35 e L02 / 15:10:** confirmar nomes seria necessário apenas para materializar substituições lexicais. As hipóteses podem permanecer pendentes sem impedir esta entrega; não há decisão humana indispensável para analisar as demais unidades.

Não há outra intervenção indispensável identificada. O escopo utilizável está analisado e conferido; **a entrevista não está integralmente avaliada**. Por isso esta entrega de trabalho não foi publicada como `Relatório-Rafael Nunes.md` em `06 - Reports/`. Uma revisão futura deve preservar esta primeira saída, a fonte e o motivo da revisão.

# Conferência de fundamento antes da nota e da entrega

Criado em 2026-10-26; controle de entrega atualizado em 2026-11-03. Controle do método seguido pelo agente do usuário. Não modifica o runtime, os pesos de referência ou as âncoras da rubrica. Não demonstra validação independente do agente.

## Registro obrigatório antes da pontuação

Para cada unidade de pergunta/resposta, preencher estes campos antes de decidir a nota. Usar referências aos turnos, sem duplicar desnecessariamente a transcrição.

| Campo | Conteúdo exigido |
| --- | --- |
| Pedido | Ação realmente solicitada e localização da pergunta, incluindo complementações vinculadas. |
| Evidência | O que foi dito na resposta utilizável, com localização e distinção entre declaração, demonstração e proposta hipotética. |
| Condições | Condições explícitas, negação, modalidade, fonte de confirmação e o que não foi informado. Preservar a condição literal ao parafrasear. |
| Escopo e fonte | Classificar separadamente o escopo da demanda e a confiabilidade dos trechos necessários, conforme a tabela abaixo. |
| Lacuna e fundamento | Conteúdo não explicado, sua relação com o pedido e o critério/seção aplicável. Distinguir falta de menção, erro expresso e incerteza da transcrição. |
| Decisão | Contextual sem nota, técnico avaliável ou julgamento técnico adiado por fonte, com justificativa. Dimensões aplicáveis e N/A dependem do pedido, não da resposta ser longa ou da pessoa declarar experiência. |

Uma limitação só pode reduzir a avaliação se houver ligação verificável entre pedido, evidência e critério. Se não conseguir fundamentar essa ligação, retirar a penalização e registrar o assunto como não explorado, sem aumentar a nota automaticamente. Uma omissão pode ser relevante mesmo sem o entrevistador ter enunciado cada componente: explicar por que é necessária para responder ao núcleo do pedido, sem converter exemplos da base em lista obrigatória de nomes, ferramentas ou etapas.

Benefício não comprova trade-off; preferência não comprova exclusividade; proposta não comprova execução ou reprodução efetiva; falta de acesso não significa conteúdo insuficiente. Não completar o ambiente ou a arquitetura para justificar uma avaliação favorável ou desfavorável. Conhecimento sobre um tema diferente não satisfaz automaticamente a demanda. Não exigir resposta longa, palavra formal, código ou vivência profissional quando o pedido não os exige.

Os percentuais de referência e as âncoras continuam em Scoring Rubric. Quando apresentar pesos normalizados, mostrar dimensões, N/A e denominador proporcional. Não criar pesos nem converter adjetivos em média numérica automática. Uma nota deve permanecer justificável independentemente de resultados históricos.

## Dois eixos: escopo da pergunta e confiabilidade da fonte

Classificar primeiro a demanda pelo que pede. Incerteza lexical não transforma uma pergunta contextual em técnica. Em seguida, registrar o estado da fonte e o impacto na informação disponível.

| Escopo | Fonte utilizável para o pedido | Fonte incerta ou comprometida |
| --- | --- | --- |
| Contextual / inventário | Registrar declaração e limites, sem nota de proficiência. | Continua contextual e sem nota técnica. Preservar original e registrar identificação/informação pendente, sem inventar nome ou conclusão. Não criar uma avaliação técnica adiada para algo que nunca seria pontuado. |
| Técnico | Avaliar o conteúdo utilizável conforme a rubrica e o pedido. | Se o problema impede julgamento confiável da unidade técnica, adiar essa avaliação, sem zero ou inferência de desempenho baseada no trecho comprometido. |

Não confundir identificação pendente com fonte irrecuperável: ambas exigem preservar o texto, mas a confirmação possível e o impacto são distintos. Confirmação explícita pode autorizar uma versão derivada separada, sem atestar proficiência nem valer para outros casos. Uma frase inteira declarada comprometida não sustenta conclusões qualitativas favoráveis ou desfavoráveis, inclusive em inventários.

Pedir intervenção humana apenas para decisão nova indispensável. Um nome incerto em inventário pode permanecer pendente sem bloquear a análise de outras unidades. Uma entrevista incompleta não pode ser declarada integralmente avaliada apenas por haver notas nas partes restantes.

Este quadro orienta relatórios produzidos por agentes. Não altera o comportamento já implementado do runtime diante de marcações estruturadas de incerteza nem autoriza contornar seus bloqueios. A identificação de julgamentos técnicos adiados permanece separada das perguntas contextuais sem nota.

## Conferência obrigatória das sínteses

Antes de entregar, comparar tabelas, títulos, justificativas e síntese com os registros das unidades:

- Cada afirmação deve manter a origem e o alcance da evidência. Marcar hipótese não confirmada em cada ocorrência pertinente, ou usar descrição genérica sustentada.
- Preservar condições e negações também nos resumos; não trocar ausência de acesso por ausência de dados, nem preferência por exclusividade. Não promover possibilidade a execução comprovada.
- Descrever conteúdo não explicado, sem converter uma resposta em diagnóstico da experiência real, caráter, maturidade ou capacidade profissional geral.
- Se uma classificação mudar, propagar o ajuste a todas as tabelas e indicadores, mantendo contextuais e adiadas fora das médias técnicas por seus respectivos motivos.
- Conferir citações, autoria, timestamps e referências pelos títulos/seções reais. Número de linha não é número de seção. Distinguir citação literal de paráfrase.
- Conferir fontes efetivamente consultadas e verificações realmente realizadas. Não declarar ausência de alucinação, conformidade integral ou cegamento apenas pela própria afirmação ou por ignorar um histórico acessível.

Se houver inconsistência, corrigir antes da entrega. Registrar limites remanescentes em vez de afirmar garantia total. O usuário recebe a análise concluída no escopo possível e apenas as exceções necessárias; não precisa executar esta conferência no lugar do agente.


## Controle final rastreável

Antes de apresentar a primeira entrega, o agente executa as verificações abaixo sobre a própria análise e registra um quadro compacto ao final de REGISTRO_DE_EXECUCAO.md. Em uma revisão, registrar no novo REGISTRO_DA_REVISAO.md. Usar ATENDE, FALHA ou NAO_VERIFICAVEL, com unidades/localizações conferidas, evidência do resultado e eventual correção ou limite. Não preencher ATENDE apenas por ter lido esta instrução ou marcado uma lista. Este é um controle do próprio agente, não prova de auditoria independente, decisão humana ou execução de software.

| Controle | Verificação que deve ter evidência na entrega |
| --- | --- |
| Elegibilidade de cada nota | Identificar a ação pedida e sua localização antes de usar a riqueza da resposta como justificativa para pontuar. Confirmar uso/conhecimento ou listar ferramentas continua contextual sem nota, mesmo com explicação espontânea. Se houver complemento técnico real, citar seu pedido e separar o escopo, sem criar pergunta retrospectiva ou nota duplicada. |
| Fundamento das penalizações | Para cada limitação que afete julgamento, ligar pedido → conteúdo ausente/incorreto → necessidade desse conteúdo → regra aplicável. Dizer que um item é relevante ou que não é checklist não demonstra sua necessidade. Não presumir produção, restrições, causa raiz, resultado positivo ou implementação completa. Limites factuais podem ser registrados sem serem penalizações. Se não houver fundamento, retirar a penalização sem aumentar nota automaticamente. |
| Origem das condições e confirmações | Identificar quem confirmou, qual trecho e o alcance: usuário, fala do entrevistador, declaração do candidato ou hipótese do agente. Uma confirmação do usuário não é fala audível do entrevistador. Conservar o original e a proveniência separadamente; não transformar hipótese em confirmação nem pedir novamente condição já fornecida. |
| Vínculos e sínteses | Conferir autor, timestamp/posição, pergunta e resposta, incluindo perguntas do candidato à equipe. A opinião do entrevistador e o contexto da vaga não completam respostas. Repercutir toda mudança de elegibilidade/fundamento em títulos, tabelas, resumo e indicadores, preservando modalidades e fonte comprometida. |
| Lista de notas e indicadores | Se houver estatísticas, partir de uma lista única das unidades elegíveis. Conferir soma, denominador, arredondamento e frequências. Usar frequências por valor exato ou intervalos explícitos que contemplem notas fracionárias sem lacunas ou sobreposição. Contextuais e adiadas ficam fora por motivos distintos. A média do subconjunto não vira avaliação integral. Não é obrigatório gerar estatísticas. |
| Fidelidade e verificabilidade | Não extrair desempenho de frase integralmente comprometida. Distinguir dimensão N/A ao pedido de julgamento indisponível pela fonte. Declarar arquivos realmente consultados, contexto exposto, consultas não verificáveis e correções feitas antes da entrega. Não afirmar teste, escuta, isolamento ou assinatura humana que não ocorreu. |

Uma FALHA encontrada deve ser corrigida e novamente conferida antes da entrega. No quadro, registrar a correção realizada e o resultado da nova conferência, sem apagar sua ocorrência. Se faltar evidência ou acesso para resolver uma pendência, registrar NAO_VERIFICAVEL, seu alcance e o que permanece indisponível; não liberar nota ou conclusão dependente como se estivesse verificada. As partes não afetadas podem ser entregues com limites explícitos. Não tornar o usuário responsável por refazer esse controle em cada unidade.

Uma versão já entregue permanece preservada. Alteração após feedback é revisão assistida com novo arquivo e registro; nunca reescrever a primeira tentativa para aparentar sucesso. Este reforço organiza a aplicação das regras existentes e não altera pesos, âncoras, rubrica ou gates históricos. Sua inclusão no pacote não comprova que qualquer agente já passou a executá-lo corretamente.

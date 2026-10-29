# Protocolo híbrido de validação de análises

Versão 1 — 2026-10-29. Este protocolo organiza a verificação de relatórios produzidos com o TechLens. Não muda a rubrica, os pesos, as âncoras ou os bloqueios do runtime. Uma avaliação independente não é estabelecida só por trocar de conversa, agente ou fornecedor.

## Papéis e limites

| Papel | Responsabilidade | Limite |
| --- | --- | --- |
| Responsável pelo ensaio | Fixar fonte, condições, versão do método e critérios; guardar entregas e liberar a comparação depois da leitura prévia. | Não fornecer resultado esperado ou antecipar conclusões ao revisor. |
| Agente executor | Fazer a análise, autoconferir e produzir a primeira entrega e seu registro. | Sua revisão não é independente. Não reescrever a primeira entrega depois de comentários. |
| Revisor de leitura separada | Ler fonte e método antes de ver a análise; registrar sua leitura e limites; depois comparar evidências e justificativas. | Outro modelo pode compartilhar vieses. Declarar histórico, acesso e conhecimento prévio. |
| Responsável humano pelas divergências | Resolver casos materiais com apoio na fonte e conhecimento técnico adequado; solicitar segunda opinião quando necessário. | Não usar preferência pessoal ou uma nota humana como gabarito. Sem evidência suficiente, manter incerteza e não simular resolução. |

As funções devem ser separadas quando possível. Se houver acúmulo de papéis, registrar isso e reduzir a alegação de independência, sem impedir o uso diagnóstico. Sem responsável humano disponível, divergências materiais ficam pendentes e as unidades afetadas não são liberadas para uso conclusivo.

## Etapa 0 — fixar o ensaio

Antes da primeira análise: registrar identificação da entrevista/trecho, cobertura, fonte original, condições confirmadas, versão do método, critérios abaixo, responsáveis e acessos. Preservar bytes do original e registrar hashes quando houver ferramentas para isso; se não houver, declarar integridade não verificada. Hash diferente, por si só, não demonstra outra entrevista.

Não distribuir relatórios anteriores, avaliações humanas ou notas alvo ao executor. As condições de erro da transcrição são entradas legítimas, não gabarito de desempenho. Não pedir ao agente para recuperar fala declarada irrecuperável. Não confundir registro de integridade com comprovação de áudio ou autenticidade do conteúdo.

## Etapa 1 — primeira entrega do executor

Executar o roteiro e a conferência antes da nota. Guardar ENTREGA_DA_ANALISE.md e REGISTRO_DE_EXECUCAO.md sem edição antes de comentários ou comparação. Registrar versão e hashes. Uma correção posterior é uma nova versão com motivo; não torna a primeira tentativa um acerto retroativo.

## Etapa 2 — leitura prévia do revisor

Disponibilizar somente fonte, condições, método e o formulário [FICHA_REVISAO_PREVIA.md](99%20-%20Templates/Interview%20Validation/FICHA_REVISAO_PREVIA.md). Não fornecer a análise do executor, registro de suas notas, auditorias anteriores ou decisões esperadas.

O revisor registra sua leitura por localização da fonte: pedido, evidência utilizável, condições, escopo e confiabilidade, conteúdo não explicado que seria necessário ao pedido, assunto não explorado e eventuais limites. Não é obrigatório produzir notas: a prioridade é registrar o que a fonte sustenta antes de sofrer influência da análise. Se registrar uma faixa ou nota, ela não vira alvo de ajuste para o executor.

O revisor informa conhecimento prévio e acessos reais. Se já conhece a análise ou as conclusões, a rodada fica identificada como revisão assistida/contexto exposto; não inventar leitura cega retroativa. Pode continuar como auditoria, mas uma nova leitura sem essa exposição permanece necessária para sustentar maior independência.

Guardar a ficha recebida sem edição e registrar hash/data de recebimento antes de liberar a etapa 3. A separação de pastas é operacional, não bloqueio técnico. Não usar o registro do executor como prova da leitura efetiva de todas as suas fontes.

## Etapa 3 — comparação por unidade

Depois de preservar a ficha, liberar somente a primeira análise e seu registro. O revisor preenche [MATRIZ_DIVERGENCIAS.md](99%20-%20Templates/Interview%20Validation/MATRIZ_DIVERGENCIAS.md), relacionando unidades por autoria, timestamp/posição e pedido, não apenas pelos IDs criados por cada agente.

Para cada ponto: registrar as duas posições, fonte, regra aplicável, classificação, impacto e possibilidade de resolução. Alterações da leitura inicial após exposição ficam rastreadas; a ficha original não é substituída. Concordância entre agentes não prova correção e divergência numérica, sozinha, não prova erro. Não usar votação ou média de notas dos revisores como verdade técnica.

## Critérios comuns, definidos antes da revisão

1. Fonte, autoria, condições e modalidades preservadas, incluindo citações e referências corretas.
2. Hipóteses lexicais não promovidas a fatos; confirmação restrita ao trecho confirmado.
3. Fonte comprometida não gera nota zero ou conclusão favorável/desfavorável retirada de fragmentos. Escopo contextual e confiabilidade separados.
4. Pedido, evidência e fundamento explícito para cada limitação que afeta julgamento; requisito não solicitado exige justificativa de necessidade ao núcleo da pergunta.
5. Declaração de uso, relato concreto, hipótese e comportamento observado separados, sem inferência de caráter, carreira ou senioridade.
6. Dimensões aplicáveis/N/A definidas pelo pedido, normalização correta quando apresentada, âncoras existentes e ausência de nota alvo.
7. Cobertura, vínculos, contagens e cálculos coerentes; partes adiadas e contextuais fora das médias técnicas por motivos distintos.
8. Sínteses e títulos preservam os limites dos detalhes. Não produzir conclusão integral quando há impedimento relevante.
9. Fontes e verificações efetivamente usadas distinguem-se de conhecimento prévio, alegações e consultas não verificáveis.

Esses critérios não constituem gabarito exaustivo de conteúdo técnico ou notas. A revisão do especialista pode identificar erro não antecipado, que deve ser registrado com evidência e sem reescrever o protocolo inicial para ocultar a descoberta.

## Classificação e consequência

| Classe | Exemplo | Consequência |
| --- | --- | --- |
| Erro material | Fala inventada, autoria trocada, hipótese aplicada sem confirmação, negação invertida, requisito extra afetando avaliação, cálculo ou síntese que muda a conclusão. | Impedir uso conclusivo da unidade afetada até corrigir em nova versão ou adiar por fonte; rever sínteses dependentes. |
| Diferença justificável de julgamento | Faixas de nota distintas com evidências e critérios defensáveis. | Registrar para calibração; não forçar igualdade nem mudar pesos para concordar. |
| Questão de fonte | Texto irrecuperável, autoria ou nome não confirmado. | Manter limitação; não confundir indisponibilidade da fonte com erro do candidato ou do executor. |
| Problema editorial | Formatação ou referência imprecisa sem alteração da conclusão. | Corrigir com registro; se a referência sustenta conclusão inexistente, reclassificar como material. |
| Ambiguidade do método | Duas leituras plausíveis de uma regra com efeitos relevantes. | Registrar separadamente, suspender decisão afetada e propor esclarecimento testável; não alterar regra no meio do ensaio sem nova versão. |

Usar ATENDE, FALHA ou NAO_VERIFICAVEL para cada critério examinado, com evidência. Não chamar desconhecido de aprovado. Severidade depende do impacto, não de uma lista automática de palavras. Um problema pequeno pode ser material se inverter o julgamento.

## Etapa 4 — resolução humana e decisão

O responsável humano verifica a fonte e o fundamento dos pontos materiais. Se não possuir conhecimento suficiente para o tema, registrar pendência ou pedir opinião técnica apropriada. Mantém-se a posição inicial de cada revisor; a decisão registra quem decidiu, por quê e com qual evidência. Fonte irrecuperável não é resolvida por consenso.

Usar [DECISAO_VALIDACAO.md](99%20-%20Templates/Interview%20Validation/DECISAO_VALIDACAO.md):

- **PENDENTE:** revisão/comparação ainda não concluída ou há ponto material sem resolução. Não liberar as unidades afetadas.
- **BLOQUEADO_NO_ESCOPO_AFETADO:** impedimento material confirmado sem correção/fonte suficiente; demais unidades podem continuar, com relatório parcial explícito.
- **USO_SUPERVISIONADO_NO_ESCOPO_REVISADO:** nenhum erro material identificado permanece aberto nas unidades liberadas; incertezas/adiamentos continuam visíveis. Não significa avaliação integral ou método homologado.

Registrar separadamente o resultado da primeira entrega e o da versão corrigida. Uma versão pode ser utilizável com partes adiadas e sem nota global. Nenhum desses estados aprova contratação, senioridade ou um gate histórico do projeto. Sem comparação completa, não preencher decisão final como aprovada.

## Evidência acumulada e próximos ensaios

Relatar unidades revisadas, falhas por tipo, itens não verificáveis e diferenças justificadas, com denominadores definidos. Não calcular acurácia estatística com um ensaio conveniente ou pequena simulação. Se repetir execução, manter cada resultado, sem escolher só o melhor. Critérios/entradas de uma nova rodada devem ser fixados antes da saída.

O primeiro ensaio deste protocolo usa a simulação longa existente: outra leitura pode testar o processo, mas não transforma essa fonte em entrevista real distinta. Outra entrevista e revisão com independência adequadamente documentada continuam pendentes.

## Referências de desenho

O protocolo combina verificações determinísticas, avaliação por agentes e resolução/calibração humana. Referências consultadas para a recomendação: [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) e [NIST AI RMF Core, Measure 1.3](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/). Este documento é uma escolha operacional do projeto, não certificação de conformidade com essas fontes.

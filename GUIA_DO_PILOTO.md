# Piloto supervisionado do TechLens

Comece por LEIA_PRIMEIRO.md e ANALISAR_ENTREVISTA.md. Este pacote destina-se a envio controlado a empresas convidadas. A versão e o commit de origem estão em package_manifest.json. Não há transcrição, resultado de candidato ou nota esperada no ZIP.

## Quem faz o quê

- A empresa fornece a transcrição e usa o próprio agente com acesso aos arquivos extraídos. Não é necessário instalar Python, cadastrar modelo ou conectar uma API ao TechLens.
- O agente consulta o método, organiza perguntas e respostas, preserva a fonte, identifica incertezas, avalia o conteúdo utilizável e confere a própria entrega.
- O responsável da empresa resolve somente exceções indispensáveis de fonte e decisões materiais que dependam de revisão humana. Não precisa preencher previamente a análise nem confirmar cada nota.
- Correção de transcrição não pode melhorar o conhecimento demonstrado, remover negação ou transformar hipótese em experiência. Uma frase irrecuperável fica sem avaliação, nunca com zero por falha da transcrição.

## Fluxo de trabalho

1. Extraia o ZIP numa pasta nova e preserve o arquivo recebido. Disponibilize a pasta completa ao seu agente e forneça a transcrição colada na conversa ou em TXT/Markdown. Informe apenas condições conhecidas, como erros confirmados ou áudio acessível. O restante permanece não informado.
2. Use o pedido copiável de ANALISAR_ENTREVISTA.md. Sem fonte, o agente deve aguardar. Se não conseguir ler um arquivo essencial, deve informar a limitação, sem alegar análise integral.
3. Receba ENTREGA_DA_ANALISE.md e REGISTRO_DE_EXECUCAO.md. Guarde a primeira entrega sem edição antes de fornecer comentários. Se houver arquivos com esses nomes, use outra pasta; não sobrescreva.
4. Examine as exceções. Nome incerto em inventário pode permanecer pendente sem bloquear outras perguntas. Uma resposta técnica comprometida fica adiada; condições já declaradas irrecuperáveis não precisam ser reconfirmadas.
5. Se houver correção, forneça ao revisor fonte, condições, método, versão recebida e feedback, quando existir. Peça ENTREGA_REVISADA.md e REGISTRO_DA_REVISAO.md em uma pasta nova. Mantenha cada versão e o motivo das alterações. A nova versão não torna correta a primeira tentativa.
6. Use a entrega no escopo sustentado. Trechos adiados continuam visíveis; médias parciais não são notas globais. O relatório não decide contratação nem senioridade.

## Três tipos de revisão

| Tipo | Acesso e limite |
| --- | --- |
| Assistida | Revisor recebe a análise e comentários posteriores. Registrar o feedback e as mudanças. |
| Exposta à análise | Revisor recebe a análise, mesmo sem feedback. Isso não é leitura prévia cega. |
| Leitura prévia separada | Primeiro recebe somente fonte, condições e método; sua ficha é preservada antes de liberar a análise. Seguir PROTOCOLO_VALIDACAO.md e os três formulários de revisão. Outra conversa ou fornecedor não prova independência. |

Nenhum formulário autoriza o agente a assinar uma decisão humana. Divergências materiais sem resolução impedem uso conclusivo da unidade e das sínteses dependentes.

## Registrar o uso e devolver problemas

Copie 99 - Templates/Interview Validation/REGISTRO_DO_PILOTO.md para uma área local da empresa. Informe a versão do pacote, agente/modelo se conhecido, condições da entrada, localização das entregas e revisões. Não invente identidade do modelo ou verificações que não ocorreram.

Para cada problema, registre localização, comportamento observado, pedido relevante, regra/fundamento, impacto, versão afetada, tratamento e estado: aberto, em análise, resolvido ou não verificável. Use uma das classes do protocolo: erro material, diferença justificável de julgamento, questão de fonte, problema editorial ou ambiguidade do método. Questão de fonte irrecuperável pode permanecer limitada; consenso não recupera a fala.

Envie o registro ao contato que forneceu o pacote. Comece por uma descrição sem dados de candidatos ou por um exemplo mínimo fictício que reproduza o problema, identificado como fictício. Não envie a entrevista inteira ou o histórico do candidato por padrão. Quando a fonte original for indispensável, combine previamente o compartilhamento autorizado e limite-o ao trecho necessário. Uma adaptação fictícia demonstra uma reprodução, não a integridade da fonte original.

Durante o piloto, erro material impede uso conclusivo do trecho afetado até correção ou adiamento adequado. Diferenças defensáveis não são resolvidas por votação, média de notas ou ajuste dos pesos para concordar. O registro do piloto é acompanhamento, não aprovação automática.

## Caminho opcional com preparação automática

Quem já tem o repositório de desenvolvimento e Python pode usar o guia PREPARAR_ANALISE.md daquele checkout para preparar pastas completas de análise e revisão. O ZIP de método não instala nem inclui esses programas; o fluxo acima funciona sem eles. Não é necessário solicitar acesso ao código para usar o método no agente.

## Limites desta entrega

Este é um piloto operacional. Generalização para entrevistas reais distintas e calibração independente continuam pendentes; a validação real foi adiada pelo responsável pelo projeto. Ensaios e correções anteriores não são garantias para qualquer agente. Hashes verificam consistência dos arquivos, não correção semântica, autoria autenticada ou independência. O pacote não promove gates históricos nem autoriza lançamento público ou publicação de entrevistas.

# Preparar análise e revisão com todos os arquivos

Data: 2026-11-03. Incremento operacional para o agente que a empresa já utiliza. Não conecta modelos, não analisa a entrevista automaticamente e não muda a rubrica. O agente continua fazendo a maior parte da análise e apresenta exceções de fonte ao responsável.

O preparador reúne a transcrição, condições e o método em uma pasta nova. Na revisão, inclui também a entrega e seu registro. Isso evita entregar somente o feedback sem acesso à fonte. O fluxo manual de ANALISAR_ENTREVISTA.md continua disponível; esta ferramenta é opcional para quem organiza os arquivos.

## Análise

Use um ZIP do método criado e conferido conforme PACOTE_DO_METODO.md. Com Python disponível, execute no repositório:

```text
python -m scripts.interview_workspace analysis --method-package "TechLens-Metodo.zip" --transcript "entrevista.md" --conditions "condicoes.md" --output "trabalhos/entrevista-001"
```

`--conditions` é opcional. Sem ele, condições permanecem não informadas; não são inventadas confirmação de áudio, correção ou ausência de erro. Entradas precisam ser texto UTF-8 não vazio, até 10 MiB por arquivo; formatos Word/PDF/áudio não são convertidos por esta ferramenta. Nomes, timestamps e demais bytes da transcrição e das condições são copiados sem normalização.

Disponibilize ao seu agente a pasta completa `entrevista-001`, preferencialmente em uma conversa sem relatórios anteriores, e peça para seguir LEIA_PRIMEIRO.md e TAREFA.md. METODO/ contém as referências; o agente deve declarar seu contexto e o que realmente consultou. A ferramenta não executa o agente.

Saídas solicitadas: ENTREGA_DA_ANALISE.md e REGISTRO_DE_EXECUCAO.md. Guarde a primeira entrega antes de qualquer feedback. Nenhuma nota esperada é gerada.

## Revisão com a fonte disponível

```text
python -m scripts.interview_workspace review --workspace "trabalhos/entrevista-001" --analysis "trabalhos/entrevista-001/ENTREGA_DA_ANALISE.md" --execution-record "trabalhos/entrevista-001/REGISTRO_DE_EXECUCAO.md" --feedback "comentarios.md" --output "trabalhos/revisao-001"
```

`--feedback` é opcional. Com ele, a tarefa é uma revisão assistida; sem ele, continua sendo uma revisão exposta à análise recebida. Não é a leitura prévia separada do PROTOCOLO_VALIDACAO.md: aquela etapa deve ocorrer antes de liberar a análise do executor.

Envie a pasta completa `revisao-001` ao revisor. Ela traz método, fonte, condições, ENTREGA_RECEBIDA.md, REGISTRO_RECEBIDO.md e, se fornecido, FEEDBACK_RECEBIDO.md. Os arquivos de saída pedidos são ENTREGA_REVISADA.md e REGISTRO_DA_REVISAO.md. Os nomes genéricos de recebimento identificam as duas entradas selecionadas no comando, não garantem que sejam a primeira versão. Para outra rodada, selecione explicitamente a versão desejada e use outro destino; mantenha todas as pastas anteriores para rastrear a sequência.

## Preservação e limites

- Pastas de destino existentes são recusadas. A revisão deve ficar fora da pasta original. Fonte e entradas não são sobrescritas.
- Antes da revisão, o preparador confere os hashes das entradas da pasta de análise e o método nela incluído. Se uma entrada mudou, interrompe antes de criar o destino. Edições autorizadas na fonte exigem nova pasta de análise e registro próprio da mudança.
- Somente entradas fixas e os arquivos explicitamente selecionados são copiados; relatórios adicionais e arquivos privados próximos não são coletados automaticamente. O manifesto registra hashes e revisão do método; não autentica autoria nem qualidade semântica.
- A ferramenta só lê e grava localmente. A pasta resultante contém a transcrição e, na revisão, resultados da entrevista. Disponibilize-a somente a destinatários autorizados; o comando não publica nem inclui essas pastas em commits.
- Preservação de arquivos não comprova leitura real pelo agente. O responsável recebe a análise, confere as exceções indispensáveis e mantém adiamentos visíveis, sem transformar erro de transcrição em falha do candidato.

Por decisão do usuário em 2026-11-03, o desenvolvimento prossegue sem exigir agora outra entrevista real. Essa validação permanece não realizada, com generalização e calibração pendentes; não foi substituída por homologação. O ciclo fictício anterior teve falhas na primeira tentativa e correções assistidas até R2. Os gates históricos, método, pesos e runtime permanecem inalterados.


## Compatibilidade da entrega piloto

O preparador aceita pacotes techlens.method.v1 e techlens.method.v2. O v2 inclui protocolo, formulários e guia do piloto; a revisão recebe todos os documentos daquela versão. Use o ZIP original como entrada do comando analysis, não um ZIP de pasta já enriquecida com entrevistas ou resultados. A construção opcional do ZIP a partir do checkout pode usar --release-version 0.1.0-piloto.1, conforme PACOTE_DO_METODO.md. Nenhuma instalação é necessária para quem usa diretamente o pacote com seu agente.


## Controle de entrega — atualização 0.1.0-piloto.2

As tarefas de análise e revisão pedem o controle final rastreável do Check no próprio registro da execução/revisão. Isso exige referências e limites, não aprovação automática. Pacotes .1 e v1 anteriores continuam aceitos; não substituir a versão usada por uma entrevista em andamento sem registrar a mudança.

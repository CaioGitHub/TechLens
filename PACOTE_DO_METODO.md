# Distribuição reproduzível do método

Data: 2026-10-28. Construtor e verificador: `scripts/agent_method_package.py`. O usuário final continua usando o próprio agente; não há integração de modelo ou alteração da análise/score.

## Para quem recebe o pacote

Extraia o ZIP em uma pasta nova, abra ANALISAR_ENTREVISTA.md e disponibilize a transcrição ao seu agente conforme esse guia. O pacote base não traz transcrição, candidato avaliado ou relatório anterior; sem fonte, o agente deve aguardar. Não é necessário Python para ler o método ou executar a análise textual.

Preserve o ZIP original. A empresa pode adicionar a transcrição e guardar as saídas na área extraída sem modificar o arquivo ZIP. A verificação abaixo se aplica ao pacote original, não à pasta enriquecida com dados da entrevista. Não enviar histórico de candidatos como gabarito. Uso supervisionado; integridade de arquivos não comprova qualidade semântica do agente.

## Para quem prepara uma distribuição

No repositório com Python e Git disponíveis, executar:

```text
python -m scripts.agent_method_package build --repo . --ref HEAD --output caminho/TechLens-Metodo.zip
python -m scripts.agent_method_package verify caminho/TechLens-Metodo.zip
```

Também é possível indicar uma revisão conhecida em --ref e o executável Git em --git. A revisão precisa conter todos os documentos obrigatórios. O construtor resolve a revisão para um commit antes de ler os arquivos; alterações locais e arquivos não rastreados não são exportados. Não substitui ZIP existente. A mesma revisão e versão do construtor, no mesmo ambiente de compactação, geram os mesmos bytes; o SHA-256 do arquivo aparece na saída.

## Seleção e rastreabilidade

A lista explícita METHOD_SOURCES seleciona documentos de método e referências técnicas, não diretórios inteiros. Ela não inclui transcrições de entrada, diretórios de relatórios/pilotos, critérios reservados, testes, código do runtime ou .git. Exemplos metodológicos da rubrica continuam presentes e não são respostas esperadas de uma entrevista enviada.

O roteiro distribuído conserva o método e omite o apêndice de execuções. Um nome ilustrativo do modelo de processamento é generalizado. README, START_HERE, GEMINI_HANDOFF e resumos de continuidade são gerados para orientar o snapshot sem importar resultados de candidatos. As transformações, arquivos gerados, hashes dos bytes de origem e hashes dos arquivos distribuídos ficam declarados em package_manifest.json.

A seleção protege contra inclusão acidental de outras pastas. Ela não é um classificador de conteúdo sensível: alterações futuras nos próprios documentos selecionados precisam de revisão antes de distribuição. O manifesto identifica source_commit do método, não comprova aprovação desse commit nem assinatura de autor.

## Verificação e limites

O verificador lê o ZIP sem extrair arquivos: confere a lista exata de membros permitidos, duplicatas, formato do manifesto, limites de tamanho e hashes. Arquivos extras, ausentes ou alterados são rejeitados. A verificação prova consistência com o manifesto do próprio ZIP, não autenticidade criptográfica: quem reescrever conteúdo e manifesto pode criar outro pacote internamente consistente. Para reconhecer o arquivo recebido, comparar também o SHA-256 com o informado por uma origem confiável.

Referências conceituais que não constam na seleção continuam indisponíveis; o agente deve declarar a falta de fonte essencial, não alegar leitura de arquivos ausentes. Nenhuma validação de pacote substitui correção da transcrição, supervisão de exceções, calibração de notas ou entrevista real distinta para generalização. Os gates históricos permanecem inalterados.

## Verificação de desenvolvimento

Dez contratos cobrem seleção de fontes, exclusão de artefatos privados, determinismo, revisão histórica, exclusão de mudanças locais, recusa de sobrescrita, fonte obrigatória ausente e rejeição de conteúdo alterado, membro extra, duplicado ou caminho fora da seleção. Os testes usam repositórios temporários fictícios, sem publicar ou consumir dados reais. Resultados da rodada ficam em PACKAGE_DISTRIBUTION_RESULTS_2026-10-28.json.


Verificação desta rodada: dez contratos de empacotamento aprovados; regressão completa com 610 testes e Reference Harness com 15, sem falhas ou erros. ZIP de ensaio construído e verificado. Resultados em PACKAGE_DISTRIBUTION_RESULTS_2026-10-28.json. A validação do próximo piloto com entrevista distinta permanece pendente; o novo pacote não inclui fonte ou avaliação de candidato.


## Protocolo híbrido de validação — 2026-10-29

Protocolo em PROTOCOLO_VALIDACAO.md e formulários em 99 - Templates/Interview Validation/. A leitura prévia do revisor deve ser preservada antes de liberar a análise do executor. Comparação por unidade, classificação de divergências e decisão humana do escopo material; sem nota alvo ou alegação automática de independência. Primeiro ensaio preparado com a simulação existente, mas a execução e a comparação do novo revisor continuam pendentes. Nenhuma validação real, revisão independente ou calibração foi concluída nesta preparação; método de pontuação e gates preservados.


## Pastas completas de trabalho — 2026-11-03

Ver PREPARAR_ANALISE.md e scripts/interview_workspace.py. O preparador consome este ZIP de método, preserva fonte e condições e reúne os arquivos selecionados em outra pasta para revisão. A distribuição do método continua sem entrevistas; as pastas de trabalho incluem somente a entrevista e as entregas selecionadas pelo usuário e não são publicadas automaticamente.


## Entrega 0.1.0-piloto.1 — formato v2

O construtor passa a gerar techlens.method.v2 por padrão, acrescentando PROTOCOLO_VALIDACAO.md, os três formulários de revisão em branco, GUIA_DO_PILOTO.md e REGISTRO_DO_PILOTO.md. O primeiro arquivo da jornada é LEIA_PRIMEIRO.md; ANALISAR_ENTREVISTA.md contém o pedido principal. A entrega é para envio controlado, sem lançamento público ou entrevistas de exemplo no ZIP.

```
python -m scripts.agent_method_package build --repo . --ref HEAD --release-version 0.1.0-piloto.1 --output TechLens-0.1.0-piloto.1.zip
python -m scripts.agent_method_package verify TechLens-0.1.0-piloto.1.zip
```

O manifesto v2 registra release_version, package_format, source_commit e hashes. O verificador continua aceitando ZIPs v1 existentes sem exigir metadados que não existiam. Para reconstruir uma revisão histórica com a seleção antiga, usar --package-format techlens.method.v1. A mesma revisão, seleção e versão do construtor geram os mesmos bytes no mesmo ambiente de compactação.

scripts/interview_workspace.py aceita ambos os formatos e preserva a seleção correspondente na preparação de análise e revisão, incluindo pastas v1 anteriores sem metadados novos. O registro de acompanhamento da empresa deve ficar fora do ZIP original. Templates em branco não são execução ou aprovação.

A mensagem de entrega e o registro técnico da preparação ficam separados do ZIP de método. O conteúdo fornecido a uma empresa continua sem relatos de candidatos, critérios reservados ou resultados históricos. Os sete arquivos privados de preparação do reteste antigo foram arquivados fora do repositório, com conferência de hashes e recibo exclusivamente local; não foram publicados.


## Atualização 0.1.0-piloto.2

A versão padrão passa a 0.1.0-piloto.2, conservando o formato v2 e a compatibilidade v1. A mesma seleção incorpora o controle final rastreável atualizado e suas referências no roteiro/guia. Construir com --release-version 0.1.0-piloto.2 e um destino novo; não sobrescrever o ZIP .1. O pacote continua sem resultados de candidatos, critérios reservados ou conteúdo privado de piloto. Ver PILOT_FEEDBACK_2026-11-03.md no checkout para o resumo geral do retorno; esse resumo de desenvolvimento não é distribuído ao executor.

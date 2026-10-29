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

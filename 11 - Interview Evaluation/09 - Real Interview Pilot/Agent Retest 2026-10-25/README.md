# Reteste controlado do agente — 2026-10-25

Estado: `PACKAGE_READY_AWAITING_USER_AGENT_EXECUTION`.

Estratégia escolhida: fornecer a uma conversa nova do agente do usuário um snapshot isolado do método, transcrição e condições conhecidas da fonte, sem avaliações anteriores. O objetivo imediato é testar o respeito às incertezas e a produção de uma análise rastreável, não medir detecção cega de falhas nem comparar notas com um gabarito.

O ZIP executor foi gerado localmente e conferido; caminho e hash em `package_verification.json`. Ele contém LEIA_PRIMEIRO.md, TAREFA_PARA_O_AGENTE.md, TRANSCRICAO_ORIGINAL.md, CONDICOES_DA_FONTE.md e as referências de método. Não contém COMPARACAO_RESERVADA.md, relatórios de candidatos, resultados do reteste ou diretório Git. Não enviar a pasta de preparação inteira ao executor.

Para usar: extrair o ZIP numa pasta separada, abrir uma conversa nova com acesso somente às entradas do pacote e enviar o pedido de análise de TAREFA_PARA_O_AGENTE.md. Guardar a resposta em uma nova entrega, sem ajustar notas depois de ver critérios. A separação de arquivos não é uma sandbox e não comprova cegamento; registrar o acesso efetivamente disponível ao agente.

O guia distribuído conserva o método e omite o apêndice de execuções anteriores. Exemplos de nomes de participantes em um documento metodológico foram generalizados; critérios e fonte da entrevista não foram alterados. Transformações e hashes estão no manifesto interno do pacote. A versão de origem do método está fixa em build_spec.json.

COMPARACAO_RESERVADA.md define os critérios para a comparação posterior. Nenhuma nova análise foi executada nem aprovada nesta etapa. Para reconstruir outro pacote, usar build_package.py com --repo, --output e, se necessário, --git; ele lê a revisão Git fixada e se recusa a sobrescrever saída existente.

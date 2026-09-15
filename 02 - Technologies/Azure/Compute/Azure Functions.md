---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Functions

## O que é?

Azure Functions é a oferta serverless do Azure para execução de código orientada a eventos (event-driven): você fornece uma função que reage a um "trigger" (gatilho), e a plataforma cuida inteiramente do provisionamento e escala da infraestrutura de execução.

## Conceitos principais

- **Serverless**: você não gerencia (nem vê) servidores diretamente; paga tipicamente pelo consumo/execução, não por capacidade reservada continuamente.
- **Triggers**: o evento que dispara a execução da função (ex.: requisição HTTP, mensagem em uma fila, timer agendado, evento de um Storage).
- **Event-driven**: o modelo de execução responde a eventos, em vez de manter um processo sempre ativo esperando requisições.
- **Scaling**: escala automaticamente (inclusive a zero) conforme o volume de eventos.
- **Stateless execution**: cada execução é tipicamente independente — estado que precisa persistir entre execuções deve ser armazenado externamente (ex.: [[Azure Databases|banco de dados]], [[Azure Storage]]).

## Long-running Web Application vs. Event-driven Function

| | Aplicação Web (ex.: Spring Boot em App Service) | Azure Function |
|---|---|---|
| Execução | Processo de longa duração, sempre ativo | Executa sob demanda, por evento |
| Modelo de custo | Capacidade reservada (mesmo ocioso) | Tipicamente por execução/consumo |
| Adequado para | APIs com tráfego constante, estado de aplicação em memória | Processamento assíncrono, integrações pontuais, tarefas agendadas |

## Conexão com Java (apenas conceitual)

Azure Functions suporta funções escritas em Java, mas o modelo de execução (curta duração, stateless, por evento) é fundamentalmente diferente do modelo de uma aplicação Spring Boot tradicional (processo de longa duração). Uma aplicação Spring Boot inteira normalmente não é reescrita como uma Function apenas por estar no Azure — a escolha depende do formato do problema (workload orientado a evento vs. serviço de longa duração).

## Relações

- [[Azure Compute]]
- [[Choosing Azure Compute]]

## Referências

- Microsoft Learn — "Azure Functions overview": https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview

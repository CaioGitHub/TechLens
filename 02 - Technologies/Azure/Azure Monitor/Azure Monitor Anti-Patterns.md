---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Monitor Anti-Patterns

## Monitorar apenas CPU

Ignora latência, throughput, erros e saturação de outros recursos (ver [[Golden Signals]]) — CPU normal não significa aplicação saudável.

## Ignorar erros da aplicação

Focar apenas em métricas de infraestrutura sem observar [[Application Logs]] deixa passar problemas de lógica de negócio que não afetam CPU/memória.

## Criar centenas de alertas

Gera fadiga de alerta ("alert fatigue") — a equipe passa a ignorar notificações, inclusive as importantes (ver [[Azure Monitoring Alerting Strategy]]).

## Alertas sem ação definida

Um alerta que dispara sem que ninguém saiba o que fazer não ajuda — apenas produz ruído.

## Thresholds arbitrários

Definir limites copiados de outro sistema ou "no chute", sem considerar o comportamento real do recurso monitorado, gera falsos positivos ou negativos.

## Não monitorar dependências

Ignorar o tempo/saúde de bancos de dados e APIs externas esconde a causa mais comum de lentidão e erro em aplicações distribuídas.

## Não monitorar disponibilidade

Focar apenas em métricas internas sem verificar acessibilidade real do ponto de vista do usuário (ver [[Availability Monitoring]]).

## Confundir logs com métricas

Tentar usar logs para tudo (incluindo o que uma métrica resolveria de forma mais barata e rápida) ou vice-versa — ver [[Logs vs Metrics]].

## Guardar logs sem estratégia de retenção

Acumular logs indefinidamente sem política de retenção aumenta custo sem benefício proporcional (ver [[Azure Monitor Cost Awareness]]).

## Não considerar custo de ingestão

Habilitar todas as categorias de log em todos os recursos sem considerar volume e custo de ingestão/armazenamento.

## Não correlacionar sinais

Investigar métricas, logs e traces isoladamente, sem tentar montar a narrativa completa de um incidente (ver [[Correlation]]).

## Não definir severidade

Tratar todos os alertas como igualmente importantes dificulta a priorização real da equipe.

## Monitorar sem definir o que é sucesso

Coletar sinais sem antes definir o que "normal"/"saudável" significa para o sistema (ver [[SLI SLO SLA]]) — sem uma referência, é difícil saber quando agir.

## Depender apenas de dashboards

Dashboards exigem alguém olhando ativamente — não substituem uma estratégia de alertas para detecção proativa (ver [[Monitoring vs Alerting]]).

## Considerar "processo rodando" sinônimo de aplicação saudável

Ver a ressalva explícita em [[Health Check]] e [[Availability Monitoring]] — disponibilidade real depende da experiência do usuário, não apenas do estado do processo.

## Relações

- [[Azure Monitoring Alerting Strategy]]
- [[Golden Signals]]
- [[Azure Anti-Patterns]]

## Referências

- Microsoft Learn — "Best practices for alerting": https://learn.microsoft.com/en-us/azure/azure-monitor/best-practices-alerts

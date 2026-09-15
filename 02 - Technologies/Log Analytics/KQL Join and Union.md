---
type: concept
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - log-analytics
  - kql
---

# KQL Join and Union

## `join` — relacionar conjuntos de dados diferentes

```
Requests
   +
Dependencies
   ↓
Correlation
   ↓
Investigation
```

Diferentes tipos de telemetria vivem em tabelas diferentes (ver [[Application Insights Tables]]). Responder "quais dependências pertencem a esta requisição?" exige relacionar `AppRequests` com `AppDependencies` — tipicamente pelo `OperationId` compartilhado (ver [[Correlation]]).

```kql
AppRequests
| where Success == false
| join kind=inner (
    AppDependencies
) on OperationId
```

### Tipos de join relevantes

- **inner** — retorna apenas combinações onde há correspondência em ambos os lados.
- **leftouter** — retorna todas as linhas do lado esquerdo, com colunas do lado direito nulas quando não há correspondência.

### Riscos

- **Chaves incorretas ou ausentes** — um join sobre uma coluna que não identifica a operação corretamente produz combinações sem sentido.
- **Cardinalidade** — se o lado direito tiver múltiplas linhas por chave, o resultado se multiplica (uma requisição com 5 dependências gera 5 linhas combinadas) — é preciso ter isso em mente ao agregar depois.
- **Custo/performance** — joins são mais custosos que filtros simples; devem ser aplicados **depois** de filtrar cada lado pelo período de tempo relevante, não sobre tabelas inteiras.

Joins não devem ser usados indiscriminadamente — apenas quando a pergunta realmente exige relacionar dados de tabelas diferentes.

## `union` — consultar múltiplas tabelas juntas

```kql
AppRequests
| union AppExceptions
| where TimeGenerated > ago(1h)
```

`union` combina linhas de tabelas diferentes em um único resultado — útil, por exemplo, para visualizar requests e exceptions em uma única linha do tempo. Deve ser usado com intenção clara: tabelas com schemas muito diferentes produzem um resultado com muitas colunas vazias, dificultando a leitura.

## Relações

- [[Kusto Query Language]]
- [[Correlation]]
- [[Application Insights Tables]]
- [[Log Analytics Troubleshooting with KQL]]

## Referências

- Microsoft Learn — "join operator": https://learn.microsoft.com/en-us/kusto/query/join-operator?view=microsoft-fabric
- Microsoft Learn — "union operator": https://learn.microsoft.com/en-us/kusto/query/union-operator?view=microsoft-fabric

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

# KQL Data Types and Dynamic

## Tipos relevantes

- **string** — texto.
- **int** / **long** — números inteiros (32/64 bits).
- **real** — números de ponto flutuante.
- **bool** — verdadeiro/falso.
- **datetime** — timestamp (usado extensivamente em `TimeGenerated`, filtros de tempo).
- **dynamic** — estrutura que pode representar JSON, arrays ou objetos.

## `dynamic`

Telemetria frequentemente carrega propriedades customizadas em uma coluna do tipo `dynamic` — comum no campo `Properties` (chamado `customDimensions` no modelo clássico), que armazena pares chave-valor definidos pela aplicação (ver [[Application Telemetry#Custom Telemetry|Custom Telemetry]]).

```kql
AppRequests
| extend UserId = tostring(Properties.userId)
```

Acessa-se uma propriedade dentro de um valor `dynamic` com notação de ponto (`Properties.userId`), e converte-se para o tipo esperado com funções como `tostring()`, `toint()`, `todouble()` — o valor bruto dentro de um `dynamic` não tem tipo fixo até ser explicitamente convertido.

## `parse` — extrair informação de strings estruturadas

```kql
AppTraces
| parse Message with "User " userId " performed " action
```

`parse` extrai partes de uma string usando um padrão declarado. Alternativas conceituais:

- **`extract()`** — extrai uma parte de uma string usando uma expressão regular, quando apenas um valor é necessário.
- **`split()`** — divide uma string em partes usando um delimitador.

Esta base trata essas funções apenas como visão geral — extração avançada de texto não estruturado foge do escopo desta etapa.

## Relações

- [[Kusto Query Language]]
- [[Application Insights Tables]]
- [[KQL Projection]]

## Referências

- Microsoft Learn — "Scalar data types": https://learn.microsoft.com/en-us/kusto/query/scalar-data-types/?view=microsoft-fabric
- Microsoft Learn — "parse operator": https://learn.microsoft.com/en-us/kusto/query/parse-operator?view=microsoft-fabric

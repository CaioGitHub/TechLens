---
type: concept
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - log-analytics
  - kql
  - anti-patterns
---

# KQL Anti-Patterns

## 1. Query sem limite temporal

```kql
AppRequests
| where Success == false
```

Sem um filtro de `TimeGenerated`, a query varre todo o histórico retido — lento, caro, e frequentemente irrelevante (um erro de três meses atrás raramente interessa para investigar um incidente de agora). Sempre comece com uma janela de tempo (ver [[KQL Filtering]]).

## 2. Query gigante desde o início

Escrever uma query com dezenas de operadores encadeados (`where` + `join` + `summarize` + `extend` múltiplos) sem validar etapas intermediárias dificulta encontrar onde algo deu errado. Prefira o workflow incremental descrito em [[KQL Query Performance]].

## 3. Join sem necessidade ou sem entender a chave

Relacionar tabelas sem uma chave de correlação clara (como `OperationId`) produz combinações sem sentido, ou explosão de linhas por cardinalidade inesperada. Ver [[KQL Join and Union]].

## 4. Filtrar tarde

Aplicar `where` apenas no fim do pipeline, depois de `summarize` ou `join` sobre um volume grande de dados, desperdiça processamento que poderia ter sido evitado filtrando cedo.

## 5. Selecionar tudo

Omitir `project`/`project-away` e carregar todas as colunas (incluindo `dynamic` grandes) quando apenas algumas são relevantes, tornando o resultado difícil de ler e mais pesado de processar.

## 6. Concluir com poucos dados

Usar `take 20` (uma amostra de exploração) como se fosse uma amostra estatisticamente representativa, ou tirar conclusões de um endpoint com poucas requisições no período analisado.

## 7. Confundir média com realidade

```
Average latency
```

não mostra necessariamente `p95`, `p99` ou outliers — uma média pode parecer saudável enquanto uma parcela relevante dos usuários tem experiência ruim. Ver [[KQL Aggregation]].

## 8. Usar KQL como SQL

Aplicar mentalidade relacional (pensar em transações, normalização, chaves estrangeiras rígidas) sem compreender que KQL foi desenhado para exploração analítica sobre grandes volumes de dados semi-estruturados. Ver [[Kusto Query Language]].

## 9. Investigar sinais isoladamente

Olhar apenas requests, ou apenas exceptions, sem correlacionar via `OperationId`, perde o contexto de que múltiplos sinais podem descrever a mesma operação (ver [[Correlation]]).

## 10. Ignorar custo e volume

Tratar "mais telemetria e queries sempre maiores" como estratégia padrão, sem considerar volume de dados e custo de processamento (ver [[Azure Monitor Cost Awareness]]).

## Relações

- [[Kusto Query Language]]
- [[KQL Query Performance]]
- [[Azure Monitor Anti-Patterns]]

## Referências

- Microsoft Learn — "Query best practices": https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/best-practices

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

# KQL Query Performance

## Fatores que afetam custo e desempenho

```
Data Volume
    ↓
Query Scope
    ↓
Processing
    ↓
Cost / Performance
```

Quanto mais dados uma query precisa varrer, mais cara e lenta ela é — tanto em tempo de resposta quanto em custo potencial de processamento (relacionado ao volume geral discutido em [[Azure Monitor Cost Awareness]]).

## Boas práticas

- **Limitar tempo cedo** — um filtro de `TimeGenerated` restritivo no início da query reduz drasticamente o volume processado (ver [[KQL Filtering]]).
- **Filtrar cedo, no geral** — aplicar `where` antes de operações mais pesadas (`join`, `summarize` sobre muitas colunas).
- **Selecionar apenas colunas necessárias** — `project` reduz volume de dados transferido nas etapas seguintes.
- **Evitar joins desnecessários** — um `join` só deve existir quando a pergunta realmente exige relacionar tabelas (ver [[KQL Join and Union]]).
- **Entender o volume antes de generalizar** — uma amostra pequena (`take`) não garante representatividade estatística.
- **Começar simples e validar** — ver o workflow abaixo.

## Workflow recomendado

```
Query simples
    ↓
Validar resultado
    ↓
Adicionar complexidade
    ↓
Validar novamente
```

Construir uma query completa de uma vez (com múltiplos `where`, `join`, `summarize`, `extend` simultaneamente) dificulta identificar onde algo deu errado. O caminho mais confiável é começar com uma tabela e um filtro de tempo, verificar o resultado, e adicionar operadores incrementalmente.

## Segurança e dados sensíveis

Assim como a telemetria pode conter dados sensíveis (ver [[Application Telemetry#Dados sensíveis|Application Telemetry]]), os **resultados de queries** também podem expor esses dados — mensagens de exceção, propriedades customizadas, parâmetros de requisição. Exemplos de query nesta base evitam projetar colunas que tipicamente carregam segredos (tokens, senhas, credenciais); ao escrever queries reais, revisar quais colunas são exibidas e para quem os resultados são compartilhados continua sendo responsabilidade de quem investiga.

## Relações

- [[Kusto Query Language]]
- [[KQL Query Pipeline]]
- [[Azure Monitor Cost Awareness]]
- [[KQL Anti-Patterns]]

## Referências

- Microsoft Learn — "Query best practices": https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/best-practices

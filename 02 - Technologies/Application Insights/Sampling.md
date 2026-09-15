---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - observability
---

# Sampling

## Por que sampling existe

```
Aplicação
   ↓
Muita telemetria
   ↓
Sampling
   ↓
Telemetria armazenada
```

Uma aplicação com tráfego significativo pode gerar um volume de telemetria (requests, dependencies, traces) alto o suficiente para se tornar caro e, em parte, redundante — muitas requisições idênticas e bem-sucedidas acrescentam pouco valor de investigação adicional. Sampling é a técnica de reter apenas uma parte estatisticamente representativa da telemetria, reduzindo volume, ingestão e custo (ver [[Azure Monitor Cost Awareness]]) sem descartar a capacidade de investigação.

## O trade-off

```
Sampling excessivo
        ↓
Pouca informação
        ↓
Troubleshooting prejudicado
```

Sampling é um equilíbrio: pouco sampling mantém alta representatividade mas custa mais; sampling agressivo reduz custo mas pode descartar exatamente os eventos raros (uma exceção pouco frequente, um erro intermitente) que mais importam para uma investigação. Um bom sampling preserva operações correlacionadas inteiras — ver seção abaixo.

## Tipos de sampling

- **Adaptive sampling** (padrão no agente Java atual) — ajusta automaticamente a taxa de amostragem para manter um volume de telemetria aproximadamente constante, mesmo sob picos de tráfego.
- **Fixed-rate sampling** — uma taxa de amostragem fixa e explícita (ex.: sempre reter 10% das operações), útil quando é necessário um comportamento determinístico e previsível.

Ambos preservam **operações inteiras**: se uma requisição for selecionada pela amostragem, todos os itens de telemetria correlacionados a ela (dependencies, exceptions, traces daquela mesma operação) são preservados juntos — sampling não descarta itens isolados de uma operação amostrada.

## Sampling e investigação de erros raros

Um cenário comum: 99% das requisições funcionam, 1% falha intermitentemente. Se o sampling for agressivo, o pequeno percentual de falhas pode não estar entre os dados retidos, dificultando a investigação. Isso é uma razão para considerar taxas de sampling mais conservadoras em aplicações onde falhas raras são criticamente importantes, ou revisar a taxa quando uma investigação específica exigir mais dados.

## Escopo desta nota

Esta nota trata do conceito e do trade-off. Detalhes de configuração específicos (arquivos de configuração do agente, variáveis de ambiente) mudam com frequência entre versões — consulte a documentação oficial atual antes de configurar em um projeto real.

## Relações

- [[Azure Monitor Cost Awareness]]
- [[Instrumentation]]
- [[Application Insights Troubleshooting]]

## Referências

- Microsoft Learn — "Sampling in Application Insights": https://learn.microsoft.com/en-us/azure/azure-monitor/app/sampling

---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Availability Monitoring

## O que é?

Availability, do ponto de vista de monitoramento, é a verificação de que a aplicação está realmente acessível e respondendo corretamente **do ponto de vista do usuário/cliente externo** — não apenas que o processo está tecnicamente em execução.

## Modelo

```
Client
   ↓
Endpoint
   ↓
Application
```

A pergunta central é: um cliente externo, tentando acessar o endpoint, consegue de fato completar a operação esperada?

## Availability ≠ "processo está rodando"

Um processo pode estar tecnicamente ativo (o sistema operacional o reporta como "rodando") mas ainda assim inacessível para o usuário real — por um problema de rede, DNS, certificado TLS expirado, ou a aplicação travada respondendo apenas a health checks internos, mas não a requisições reais. Availability verifica a experiência de ponta a ponta, não apenas o estado do processo.

## Relação com Health Check

Um [[Health Check]] é um mecanismo comum usado para alimentar essa verificação, mas não é garantia automática de disponibilidade real percebida pelo usuário — ver a ressalva em [[Health Check]].

## No Application Insights

O [[Application Insights]] materializa esse conceito através de testes de disponibilidade (availability tests) — verificações periódicas, feitas de fora da aplicação (a partir de pontos de presença externos), que simulam a perspectiva de um cliente real acessando um endpoint. O modelo atualmente suportado é baseado em recursos **workspace-based** (integrados a um [[Log Analytics Workspace]]); a modalidade clássica está em processo de retirada — confira a documentação oficial para o estado atual antes de configurar um teste em um projeto real.

## Relações

- [[Health Check]]
- [[Performance Monitoring]]
- [[Golden Signals]]
- [[Application Insights]]

## Referências

- Microsoft Learn — "Application Insights availability tests": https://learn.microsoft.com/en-us/azure/azure-monitor/app/availability-overview

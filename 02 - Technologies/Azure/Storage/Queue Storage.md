---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Queue Storage

## O que é?

Queue Storage é um serviço de mensageria simples do Azure, usado para desacoplar componentes de uma aplicação através de processamento assíncrono.

## Modelo

```
Producer
    ↓
Queue
    ↓
Consumer
```

O produtor coloca uma mensagem na fila e segue seu fluxo sem esperar o processamento terminar; um ou mais consumidores retiram e processam as mensagens em seu próprio ritmo.

## Por que desacoplar

Sem uma fila, o produtor precisaria chamar o consumidor diretamente e esperar (acoplamento síncrono) — se o consumidor estiver lento ou indisponível, o produtor também é afetado. Uma fila absorve picos de carga e permite que produtor e consumidor escalem e falhem de forma independente.

## Nota de escopo

Esta é uma introdução conceitual mínima. Mensageria mais avançada (Service Bus, Event Grid, Event Hubs, garantias de entrega, ordenação, dead-lettering) pertence a uma etapa futura de arquitetura distribuída — não aprofundada aqui.

## Relações

- [[Azure Storage]]

## Referências

- Microsoft Learn — "Introduction to Azure Queue Storage": https://learn.microsoft.com/en-us/azure/storage/queues/storage-queues-introduction

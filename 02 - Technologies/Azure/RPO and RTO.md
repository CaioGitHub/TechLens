---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# RPO and RTO

## O que são?

Duas métricas centrais de qualquer estratégia de disaster recovery:

```
RPO (Recovery Point Objective)
↓
Quanto dado eu posso perder? (medido em tempo desde o último backup/replicação válida)

RTO (Recovery Time Objective)
↓
Quanto tempo posso ficar indisponível até restaurar o serviço?
```

## Exemplo

Se o RPO é de 1 hora, a organização aceita perder até 1 hora de dados em caso de desastre (o backup/replicação mais recente disponível tem no máximo 1 hora). Se o RTO é de 4 horas, a organização precisa ter o serviço restaurado em até 4 horas após o incidente.

## Como se relacionam com mecanismos do Azure

- Backups mais frequentes reduzem o RPO possível, mas aumentam custo/complexidade operacional.
- [[Azure Regions|Region Pairs]] e replicação geo-redundante ajudam a atingir RPO/RTO mais agressivos, mas não os garantem automaticamente — a estratégia de failover ainda precisa ser desenhada e testada.
- [[Azure Availability Zones]] endereçam principalmente disponibilidade dentro de uma região; recuperação de uma falha regional completa depende de estratégia multi-região.

## Por que definir RPO/RTO antes de escolher a solução técnica

RPO e RTO são requisitos de negócio (quanto risco a organização aceita) — a solução técnica (frequência de backup, replicação síncrona/assíncrona, multi-região) deve ser escolhida **depois** de definir esses requisitos, não o contrário.

## Relações

- [[Azure Availability]]
- [[Azure Regions]]
- [[Azure Well-Architected Framework]]

## Referências

- Microsoft Learn — "Recovery point objective (RPO) and recovery time objective (RTO)": https://learn.microsoft.com/en-us/azure/reliability/disaster-recovery-overview

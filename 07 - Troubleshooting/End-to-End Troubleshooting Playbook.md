---
type: troubleshooting
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - troubleshooting
  - integration
  - azure-monitor
  - kql
---

# End-to-End Troubleshooting Playbook

Processo sistemático de investigação atravessando **todas** as camadas: aplicação (Java/Spring/Hexagonal), Azure, Application Insights, Azure Monitor, Log Analytics e KQL. Esta nota **não duplica** as queries e cenários já documentados em [[Application Insights Troubleshooting]], [[Azure Monitor Troubleshooting]] e [[Log Analytics Troubleshooting with KQL]] — ela conecta esses processos em uma visão end-to-end e adiciona os cenários que cruzam camadas de infraestrutura/rede/disponibilidade ainda não cobertos.

## Processo geral

```
Sintoma
   ↓
Impacto
   ↓
Hipótese
   ↓
Métrica
   ↓
Logs
   ↓
Trace
   ↓
Dependency
   ↓
Correlação
   ↓
KQL
   ↓
Evidência
   ↓
Root Cause
   ↓
Correção
   ↓
Validação
```

Regra central: **o primeiro sinal encontrado não é a causa raiz.** Cada etapa produz evidência que confirma ou descarta a hipótese anterior; root cause só é declarado quando a evidência é suficiente e consistente com o sintoma original.

## Cenário 1 — HTTP 500

Ver o processo detalhado e as queries KQL em [[Application Insights Troubleshooting#Cenário 1 — HTTP 500]] e [[Log Analytics Troubleshooting with KQL#Cenário 1 — HTTP 500]].

Resumo do fluxo: `Error Rate → Requests → Exceptions → Trace → Dependency → Database/External API`.

| Pergunta | Resposta |
|---|---|
| Sintoma | Aumento de respostas HTTP 500 |
| Impacto | Usuários não conseguem completar a operação |
| Métrica | Error rate ([[Request Telemetry]]) |
| Logs | [[Exception Telemetry]] correlacionadas por `OperationId` |
| Correlação | `AppRequests` ⋈ `AppExceptions` por `OperationId` |
| Dependência | [[Dependency Telemetry]] da mesma operação |
| Confirmação | Exceção + dependência com falha consistente no mesmo intervalo de tempo |
| Validação | Error rate volta ao baseline após a correção |

## Cenário 2 — Latência

Ver [[Log Analytics Troubleshooting with KQL#Cenário 3 — A API ficou lenta?]].

Fluxo: `Latency → Request → Percentiles → Trace → Dependencies → Database/External API`.

**Nunca usar apenas a média.** Explorar p50/p95/p99 (ver [[KQL Aggregation]]): a média pode parecer normal enquanto uma fração relevante dos usuários enfrenta degradação severa — percentis altos revelam experiências de cauda que afetam usuários reais mesmo quando o "sistema em média" parece saudável.

## Cenário 3 — Dependência lenta

Ver [[Application Insights Troubleshooting#Cenário 2 — API lenta, CPU normal]] e [[Log Analytics Troubleshooting with KQL#Cenário 5 — Qual dependência está causando lentidão?]].

Fluxo: `Request → Trace → Dependency → Database/External API`.

Relacionar com: timeout, latency, retries, failures, connection issues, dependências externas. **Não assumir que a aplicação é a causa** — CPU/memória normais + `AppDependencies` com `DurationMs` alto ou `Success == false` aponta para o lado externo da chamada.

## Cenário 4 — Banco de dados

Fluxo arquitetural: `Application → Repository Port → Database Adapter → Database`.
Fluxo de observabilidade: `Request → Trace → Dependency → Database`.

Como distinguir a origem do problema:

| Hipótese | Evidência a buscar |
|---|---|
| Problema de aplicação | Alto uso de CPU/memória no processo, sem dependência lenta correspondente |
| Problema de adapter | Muitas conexões abertas, pool esgotado, sem lentidão no lado do banco |
| Problema de consulta | `AppDependencies` com `DurationMs` alto em `Target` específico, consistente por operação |
| Problema de conexão | Falhas de conexão (`Success == false`, `ResultCode` de timeout) intermitentes |
| Problema de banco/infraestrutura | Métricas de recurso do próprio banco (DTU/CPU do Azure SQL) degradadas mesmo sem mudança na aplicação |

Ver [[Azure Databases]] e [[Resource Monitoring]] para métricas do lado do recurso Azure.

## Cenário 5 — Disponibilidade

Fluxo: `Availability → Endpoint → Networking → Application → Health Check → Metrics → Logs`.

**Processo rodando ≠ aplicação disponível.** Considerar, em ordem:

1. **Endpoint** — o DNS resolve? O endpoint responde a qualquer coisa?
2. **Rede** — [[Network Security Group|NSG]], firewall, [[Virtual Network]] mal configurada bloqueando tráfego.
3. **Autenticação** — falha de identidade/token bloqueando todas as requisições antes de chegar à lógica de negócio.
4. **Aplicação** — o processo está de fato aceitando conexões (não apenas "rodando")?
5. **Health Check** — [[Health Check]] reporta saudável mesmo com dependências fora do ar?
6. **Dependências** — uma dependência crítica indisponível pode derrubar a disponibilidade percebida mesmo com a aplicação "up".

Ver [[Availability Monitoring]] e [[Azure Availability]].

## Cenário 6 — Problema de infraestrutura

Fluxo: `Application → Application Insights → Azure Monitor → Resource Metrics → Resource Logs → Activity Log`.

Como separar **Application Problem** vs **Platform/Infrastructure Problem**:

- Se [[Application Telemetry]] (requests/dependencies/exceptions) está normal, mas o usuário ainda percebe degradação → suspeitar de infraestrutura.
- [[Resource Monitoring|Resource Metrics]] (CPU, memória, I/O do host/plataforma) e [[Resource Logs]] (eventos do próprio recurso Azure) mostram degradação sem correspondência no código da aplicação.
- [[Azure Activity Log]] mostra se houve uma mudança administrativa (deploy, scale, configuração) correlacionada no tempo com o início do problema.

Se as três fontes (aplicação, recurso, activity log) não mostram nada anormal simultaneamente, a causa provavelmente não é de infraestrutura — volte para os cenários de aplicação/dependência.

## Cenário 7 — Incidente distribuído

Cenário: `Client → API A → API B → Database/External API`.

Processo de reconstrução:

1. Identificar o `OperationId`/`Operation_Id` de uma requisição afetada em **API A** (ver [[Correlation]]).
2. Usar o mesmo identificador para localizar a chamada correspondente em **API B** — a propagação de contexto (distributed tracing) é o que torna isso possível (ver [[Distributed Tracing]]).
3. Ordenar por `TimeGenerated` para reconstruir a sequência real de eventos entre os dois serviços.
4. Verificar `AppDependencies` em API A (chamada para API B) e `AppRequests` em API B (recebimento da chamada) — os tempos devem ser consistentes.
5. Repetir para a dependência final (banco/API externa) a partir de API B.
6. Usar [[Application Map]] para visualizar a topologia da chamada distribuída.

Ver a técnica de `union` sobre múltiplas tabelas filtrando por `OperationId` em [[Log Analytics Troubleshooting with KQL#Cenário 7 — Correlação: o que aconteceu nesta operação específica?]].

## Matriz de investigação

| Sintoma | Primeiro olhar | Evidência | Próximo passo |
|---|---|---|---|
| HTTP 500 | Error Rate | Exceptions | Trace |
| Latência | p95/p99 | Requests | Dependencies |
| API indisponível | Availability | Endpoint | Networking |
| DB lenta | Dependency | Database | Query/infra |
| Exceções | Exceptions | Trace | Root Cause |
| Serviço externo lento | Dependency | Duration | External service |
| Recurso Azure degradado | Metrics | Resource Logs | Infrastructure |

## Fluxo de decisão

```
Qual é o problema?

├── Erro?
│   ├── HTTP 4xx → validação/entrada do cliente
│   └── HTTP 5xx → Cenário 1
│
├── Lentidão?
│   ├── Application → Cenário 2
│   ├── Dependency → Cenário 3 / Cenário 4
│   └── Infrastructure → Cenário 6
│
├── Indisponibilidade?
│   ├── Endpoint
│   ├── Networking
│   ├── Application
│   └── Dependency → Cenário 5
│
└── Recurso degradado?
    ├── Metrics
    ├── Resource Logs
    └── Activity Log → Cenário 6
```

O objetivo é uma metodologia de investigação, não memorizar queries.

## KQL como ferramenta de investigação

Cada consulta deve responder a uma pergunta operacional real — ver exemplos completos (pergunta → tabela → filtro → agregação → correlação → conclusão) em [[Log Analytics Troubleshooting with KQL]] e a referência de schema em [[Application Insights Tables]] (`TimeGenerated`, `DurationMs`, `DependencyType`, `ExceptionType`).

## Relações

- [[Integration]]
- [[Reference Architecture - Java Spring Azure]]
- [[Application Insights Troubleshooting]]
- [[Azure Monitor Troubleshooting]]
- [[Log Analytics Troubleshooting with KQL]]
- [[Correlation]]
- [[Distributed Tracing]]

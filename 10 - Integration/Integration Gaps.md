---
type: reference
status: learning
confidence: 40
created: 2026-09-09
updated: 2026-09-09
tags:
  - integration
  - gaps
---

# Integration Gaps

Registro honesto de lacunas identificadas após a integração da Etapa 10. Gaps são **registrados**, não preenchidos automaticamente — conteúdo só deve ser criado quando houver uma etapa dedicada a isso.

## CRITICAL

- Nenhuma lacuna crítica identificada. A base cobre, de forma conectada, todo o fluxo conceitual solicitado (Java 21 → Spring Boot → Hexagonal → Azure → Azure Monitor → Application Insights → Log Analytics → KQL → Troubleshooting).

## HIGH

- **Ausência de prática real**: todos os cenários de troubleshooting, exercícios de KQL e a arquitetura de referência são conceituais. Nenhum foi validado contra uma aplicação real rodando no Azure. Ver [[Reference Project Specification]] e [[Competency Matrix]].
- **Virtual Threads + Application Insights**: o comportamento de propagação de contexto do agente OpenTelemetry Java com Virtual Threads não tem confirmação oficial conclusiva da Microsoft — apenas relatos da comunidade (ver [[Java Spring Boot Application Insights#Virtual Threads]]). Deve ser revalidado quando houver documentação oficial mais madura.

## MEDIUM

- **Segurança aprofundada**: a visão integrada de segurança (Managed Identity, RBAC, Key Vault, dados sensíveis em telemetria) é conceitual e superficial por design desta etapa. Um estudo aprofundado de [[Azure Security Fundamentals]] aplicado à observabilidade não foi feito.
- **Distributed Tracing multi-serviço real**: o Cenário 7 (incidente distribuído) do [[End-to-End Troubleshooting Playbook]] é descrito conceitualmente; nunca foi exercitado com duas APIs reais se comunicando.
- **Dashboards reais**: [[Dashboards and Workbooks]] é conhecido conceitualmente, mas nenhum dashboard foi de fato construído/validado.

## LOW

- **Custo real**: a visão de custo (telemetry volume → retention → queries → cost) é qualitativa; não há números reais de precificação aplicados a um cenário concreto.
- **Alertas configurados de ponta a ponta**: [[Alert Rules]] e [[Azure Monitor Action Groups]] são conhecidos, mas não há um exemplo de configuração completa ligada a um cenário de troubleshooting real.

## Ferramentas/tópicos explicitamente fora de escopo agora (Future Topics)

Conforme instrução explícita da Etapa 10, os seguintes temas **não devem ser iniciados** agora e só aparecem aqui como registro de escopo futuro:

- Kubernetes / AKS aprofundado
- Terraform / Infrastructure as Code aprofundado
- CI/CD avançado
- Docker aprofundado
- Service Bus, Event Grid
- Redis, Cosmos DB
- DDD avançado
- SRE avançado
- OpenTelemetry avançado (além do que já existe em [[Azure Monitor OpenTelemetry]])
- Security avançado (além dos fundamentos já cobertos)
- FinOps
- Microservices avançados (além do cenário distribuído conceitual já documentado)

## Relações

- [[Integration]]
- [[Competency Matrix]]
- [[Reference Project Specification]]

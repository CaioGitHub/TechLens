---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - hexagonal-architecture
---

# Azure Anti-Patterns

## Objetivo

Registrar problemas comuns ao integrar uma aplicação com Azure — cada um explicado pelo porquê é um problema, considerando trade-offs, não como regra absoluta.

## Colocar secrets no código

Connection strings, chaves de API ou senhas hardcoded no código-fonte ou em arquivos de configuração versionados. Problema: vazamento praticamente garantido mais cedo ou mais tarde (histórico do Git, logs, código compartilhado). Ver [[Azure Key Vault]] e [[Managed Identity]].

## Usar credenciais estáticas sem necessidade

Usar uma connection string com usuário/senha quando [[Managed Identity]] resolveria o mesmo problema sem segredo armazenado. Problema: mais superfície de ataque e mais trabalho de rotação de credenciais sem necessidade real.

## Expor serviços desnecessariamente à Internet

Configurar um banco de dados ou Storage Account com endpoint público quando um [[Public vs Private Networking|Private Endpoint]] seria suficiente. Problema: aumenta a superfície de ataque sem ganho funcional.

## Usar VM quando PaaS seria suficiente

Escolher [[Virtual Machines]] por hábito, quando [[Azure App Service]] atenderia com muito menos responsabilidade operacional (patching, scaling). Problema: custo operacional desnecessário — mas pode ser uma escolha válida se houver requisito real de controle do SO.

## Usar AKS sem necessidade

Adotar [[Azure Kubernetes Service]] para uma aplicação simples, sem necessidade real de orquestração complexa. Problema: complexidade operacional desproporcional ao problema (ver [[Choosing Azure Compute]]).

## Criar infraestrutura excessivamente complexa

Multiplicar VNets, regras de rede, camadas de abstração sem necessidade concreta. Problema: dificulta operação e depuração sem benefício real — overengineering de infraestrutura, análogo ao overengineering arquitetural já discutido em [[Hexagonal Architecture]].

## Ignorar custos

Escolher tiers/SKUs sem considerar o pilar Cost Optimization do [[Azure Well-Architected Framework]]. Problema: custo operacional inesperado, especialmente com reserved capacity mal dimensionada ou recursos esquecidos rodando.

## Ignorar disponibilidade / não considerar regiões

Não considerar [[Azure Availability Zones]] ou [[Azure Regions|Region Pairs]] para workloads críticos, ou escolher uma região sem considerar latência/residência de dados dos usuários reais. Problema: risco de indisponibilidade maior que o aceitável, ou não conformidade regulatória.

## Misturar configuração de ambiente

Não separar claramente configuração/segredos entre development, staging e production (ver [[Spring Profiles]], [[Azure Naming and Organization]]). Problema: risco de um ambiente afetar outro acidentalmente (ex.: apontar para o banco de produção em um teste).

## Acoplar domínio diretamente ao Azure

O [[Domain]] importando diretamente um SDK do Azure (ex.: `BlobServiceClient` usado dentro de uma classe de domínio). Problema: viola a [[Dependency Rule]] — o Domain passa a depender de infraestrutura externa específica, dificultando testes e futura substituição de provedor.

## Utilizar Azure SDK diretamente no Core sem necessidade arquitetural

Semelhante ao anterior: usar tipos do SDK do Azure em uma [[Use Case]] ou interface de [[Ports|Port]], em vez de mantê-los isolados nos Adapters (ver [[Hexagonal Architecture + Azure]]). Não é automaticamente proibido — mas deve ser uma escolha consciente de trade-off, não um acidente de design.

## Relações

- [[Hexagonal Architecture + Azure]]
- [[Azure Security Fundamentals]]
- [[Azure Well-Architected Framework]]
- [[Spring Boot Anti-Patterns]]

## Referências

- Microsoft Learn — "Azure Architecture Center — Antipatterns": https://learn.microsoft.com/en-us/azure/architecture/antipatterns/

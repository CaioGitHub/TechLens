---
type: technology
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - hexagonal-architecture
---

# Azure SQL

## O que é?

Azure SQL Database é o serviço de banco de dados relacional gerenciado do Azure baseado no motor SQL Server, usado tipicamente como banco de dados de uma aplicação, incluindo aplicações Spring Boot.

## Onde ele entra na arquitetura

```
Spring Boot
    ↓
Database Adapter
    ↓
SQL Database
```

Do ponto de vista da [[Hexagonal Architecture]], Azure SQL é **infraestrutura externa** acessada por um [[Adapters|Driven Adapter]] — nunca diretamente pelo [[Application Core]].

## Conexão com Spring Data / JPA / Hibernate

```
Application Core (Domain, Use Case, Repository Port)
        ↓
Persistence Adapter
        ↓
Spring Data (JPA) → Hibernate → JDBC
        ↓
Azure SQL Database
```

O Core continua dependendo apenas do [[Ports|Repository Port]] que ele mesmo define; a implementação concreta ([[Spring Data Repository vs Repository Port|Persistence Adapter]]) é quem efetivamente usa Spring Data/JPA/Hibernate/JDBC para conversar com o Azure SQL. Ver [[Spring Data]] para a diferenciação entre essas quatro tecnologias.

## Responsabilidades mantidas separadas

| Camada | Responsabilidade |
|---|---|
| Application (Core) | Regra de negócio, orquestração — não sabe que existe um "Azure SQL" |
| Persistence Adapter | Traduzir entre modelo de domínio e modelo de persistência, usar Spring Data/JPA |
| Database (Azure SQL) | Armazenar e consultar dados de forma durável |

## Relações

- [[Azure Databases]]
- [[Managed Database]]
- [[Spring Data]]
- [[Spring Data Repository vs Repository Port]]
- [[Hexagonal Architecture + Azure]]

## Referências

- Microsoft Learn — "What is Azure SQL Database?": https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview

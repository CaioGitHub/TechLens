---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - moc
  - azure
---

# Azure Databases

MOC para bancos de dados gerenciados no Azure, com foco no que importa para uma aplicação Java/Spring Boot.

## Serviços relacionais

- **Azure SQL Database** — ver [[Azure SQL]].
- **Azure Database for PostgreSQL** / **Azure Database for MySQL** — mesma proposta de valor de "banco relacional gerenciado" que Azure SQL, apenas com motores diferentes; os mesmos conceitos de [[Managed Database]] se aplicam.

## NoSQL

- **Cosmos DB** — banco de dados multi-modelo, distribuído globalmente, com garantias de consistência configuráveis. Mencionado aqui apenas como referência — não aprofundado nesta etapa (uso típico: cenários que exigem baixa latência global ou modelos de dados não relacionais).

## Foco conceitual desta etapa

- Relational vs. NoSQL — a escolha depende do formato dos dados e do padrão de consulta, não é abordada em profundidade nesta base (pertence a uma discussão de modelagem de dados).
- Managed database — ver [[Managed Database]].
- Scalability, availability, backup, connectivity — tratados de forma geral, não específicos de um motor de banco.

## Relações

- [[Azure SQL]]
- [[Managed Database]]
- [[Spring Data]]

## Referências

- Microsoft Learn — "Databases on Azure": https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/data-store-overview

---
type: study
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - learning-path
  - integration
---

# Integration Learning Path

Como estudar a stack inteira, do fundamento à investigação, usando o conhecimento já construído no Second Brain.

## Trilha sequencial

```
1. Java 21
      ↓
2. Spring Boot
      ↓
3. Hexagonal Architecture
      ↓
4. Azure Fundamentals
      ↓
5. Azure Monitor
      ↓
6. Application Insights
      ↓
7. Log Analytics
      ↓
8. KQL
      ↓
9. Observability
      ↓
10. Troubleshooting
      ↓
11. End-to-End Architecture
```

| Etapa | Nota de entrada |
|---|---|
| 1 | [[Java 21]] |
| 2 | [[Spring Boot]] |
| 3 | [[Hexagonal Architecture]] |
| 4 | [[Azure]] |
| 5 | [[Azure Monitor]] |
| 6 | [[Application Insights]] |
| 7 | [[Log Analytics]] |
| 8 | [[Kusto Query Language]] |
| 9 | [[Observability]] |
| 10 | [[End-to-End Troubleshooting Playbook]] |
| 11 | [[Reference Architecture - Java Spring Azure]] |

## Trilha baseada em cenários (aprofundamento)

```
Aprender conceito
      ↓
Implementar
      ↓
Executar
      ↓
Gerar telemetria
      ↓
Investigar
      ↓
Encontrar problema
      ↓
Corrigir
      ↓
Validar
```

Aplicar essa trilha usando a especificação em [[Reference Project Specification]]: implementar cada cenário simulado, gerar telemetria real, investigar usando [[End-to-End Troubleshooting Playbook]], e validar a correção observando as métricas voltarem ao normal.

## Como usar esta trilha

- Cada etapa numerada tem seu próprio Learning Path interno (ex.: [[Hexagonal Architecture Learning Path]], [[Application Insights Learning Path]], [[Log Analytics Learning Path]], [[Azure Monitor Learning Path]]) — esta trilha é o mapa de nível superior, não substitui os aprofundamentos.
- Não pule para o KQL sem entender o que gera a telemetria (Application Insights) e onde ela é armazenada (Log Analytics).
- Use a [[Competency Matrix]] para avaliar honestamente o nível atual antes de avançar.

## Relações

- [[Integration]]
- [[End-to-End Mental Model]]
- [[Competency Matrix]]

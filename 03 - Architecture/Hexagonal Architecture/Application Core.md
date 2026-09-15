---
type: architecture
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Application Core

## Objetivo

Descrever o que fica "dentro do hexágono" em Hexagonal Architecture: o núcleo da aplicação, isolado de detalhes de infraestrutura.

## Problema que resolve

Sem um núcleo isolado, regras de negócio se espalham por controllers, repositórios e outras camadas de infraestrutura, tornando-se dependentes de frameworks e difíceis de testar isoladamente.

## Princípios

O Application Core não deve depender de: banco de dados, frameworks web, protocolos de rede, providers de nuvem, bibliotecas de mensageria. Ele só deve depender de si mesmo e de abstrações que ele mesmo define ([[Ports]]).

## Componentes

O Core é tipicamente composto por (a divisão exata varia por sistema, não é uma exigência rígida):

- **[[Domain]]**: entidades, value objects, regras de negócio invariantes.
- **Application** (casos de uso): orquestra o domínio para realizar uma operação completa — ver [[Use Case]].
- **[[Ports]]**: contratos que o Core define para se comunicar com o mundo externo, em ambas as direções.

**Infrastructure** (adapters, frameworks, drivers) fica fora do Core por definição.

## Fluxo

```
Adapter (externo) → Port (contrato do Core) → Use Case → Domain
```

## Vantagens

- Testável isoladamente, sem precisar de banco de dados, rede ou UI real.
- Pode evoluir independentemente de mudanças de infraestrutura (trocar banco, trocar framework web).

## Desvantagens

- Exige disciplina: é fácil "vazar" uma dependência de infraestrutura para dentro do Core por conveniência.
- Não há imposição estrutural automática — nada impede fisicamente que alguém importe uma biblioteca de infraestrutura dentro do Core, a não ser convenção de equipe e revisão de código (ou ferramentas de análise arquitetural).

## Trade-offs

A divisão física (pastas) entre Domain/Application/Infrastructure não é exigida pela arquitetura — o que importa é a direção das dependências (ver [[Dependency Rule]]), não a estrutura de diretórios. Times pequenos podem optar por uma estrutura mais simples desde que a regra de dependência seja respeitada.

## Exemplo

Ver exemplo completo ("Create Order") em [[Hexagonal Architecture]].

## Relações

- [[Domain]]
- [[Use Case]]
- [[Ports]]
- [[Hexagonal Architecture]]
- [[Dependency Rule]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/

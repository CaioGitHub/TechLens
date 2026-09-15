---
type: reference
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Hexagonal vs Clean vs Onion

Comparação de referência entre as três abordagens arquiteturais mais citadas para isolar regras de negócio de infraestrutura. Todas compartilham a mesma ideia central (dependências apontando para dentro, em direção ao núcleo) com vocabulário e ênfases diferentes — **nenhuma é declarada aqui como "melhor"**.

| Aspecto | Hexagonal (Ports & Adapters) | Clean Architecture | Onion Architecture |
|---|---|---|---|
| Origem | Alistair Cockburn, 2005 | Robert C. Martin, 2012 | Jeffrey Palermo, 2008 |
| Metáfora visual | Hexágono (Core cercado por Ports/Adapters) | Círculos concêntricos | Camadas de uma cebola |
| Foco principal | Simetria entre entrada e saída via Ports/Adapters | Regras de negócio centrais e independência de frameworks | Isolamento do modelo de domínio no centro |
| Camadas nomeadas | Core, Ports, Adapters (sem camadas rígidas obrigatórias) | Entities → Use Cases → Interface Adapters → Frameworks & Drivers | Domain Model → Domain Services → Application Services → Infrastructure |
| Regra de dependência | Ver [[Dependency Rule]] | "The Dependency Rule": círculos externos dependem dos internos | Camadas externas dependem das internas |
| Ênfase | Plugabilidade de interfaces (múltiplos "lados" podem acionar/ser acionados) | Fronteiras explícitas e nomeadas entre camadas | Pureza e proteção do modelo de domínio |

## Semelhanças

- Todas colocam regras de negócio no centro, isoladas de frameworks, UI, banco de dados.
- Todas seguem uma variante da mesma regra de dependência: de fora para dentro.
- Todas visam testabilidade e possibilidade de trocar infraestrutura sem alterar o núcleo.

## Diferenças

- Hexagonal não prescreve quantas camadas devem existir dentro do Core — fala genericamente em "dentro" vs. "fora". Clean Architecture é mais prescritiva quanto a camadas nomeadas (Entities, Use Cases, Interface Adapters, Frameworks). Onion enfatiza fortemente a pureza do modelo de domínio no centro absoluto.
- Hexagonal usa a linguagem de Ports/Adapters; Clean fala em Use Cases/Interface Adapters; Onion fala em Domain Model/Domain Services.

## Sobreposição conceitual

Na prática, uma aplicação bem estruturada segundo qualquer uma das três costuma satisfazer as outras duas — a diferença é majoritariamente de vocabulário e ênfase didática, não de resultado final.

## Relações

- [[Hexagonal Architecture]]
- [[Dependency Rule]]
- [[Application Core]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/
- Martin, Robert C. "The Clean Architecture", blog.cleancoder.com, 2012.
- Palermo, Jeffrey. "The Onion Architecture", jeffreypalermo.com, 2008.

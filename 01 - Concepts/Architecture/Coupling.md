---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - architecture
---

# Coupling

## O que é?

Coupling (acoplamento) é o grau de dependência entre dois módulos, classes ou componentes de um sistema. Quanto mais um módulo conhece ou depende dos detalhes internos de outro, maior o acoplamento entre eles.

## Por que existe?

Todo sistema precisa que suas partes colaborem entre si — colaboração implica algum grau de dependência. O conceito existe para que essa dependência seja avaliada e controlada conscientemente, em vez de crescer de forma acidental.

## Qual problema resolve (ou ajuda a identificar)?

Alto acoplamento torna o sistema frágil: uma mudança em um módulo força mudanças em cascata em outros módulos que dependem dele. Isso dificulta manutenção, testes isolados e substituição de partes do sistema.

## Como funciona?

Acoplamento pode ser medido informalmente pela pergunta: "quantos outros módulos eu preciso entender/mudar se eu alterar este aqui?". Formas comuns de acoplamento, do mais forte ao mais fraco:

- Dependência direta de uma implementação concreta (forte).
- Dependência de uma abstração/interface (mais fraco — ver [[Dependency Inversion]]).
- Comunicação por mensagens/eventos, sem conhecimento direto do receptor (mais fraco ainda).

## Exemplo

```java
// Alto acoplamento: o caso de uso conhece diretamente o driver JDBC
class CreateOrder {
    void execute(Order order) {
        var conn = DriverManager.getConnection("jdbc:...");
        // ...
    }
}

// Baixo acoplamento: o caso de uso depende apenas de uma abstração
interface OrderRepository {
    void save(Order order);
}

class CreateOrder {
    private final OrderRepository repository;
    CreateOrder(OrderRepository repository) { this.repository = repository; }
    void execute(Order order) { repository.save(order); }
}
```

## Quando é aceitável mais acoplamento?

Em módulos que naturalmente pertencem à mesma responsabilidade e mudam juntos (ex.: uma entidade e seus value objects internos). Nem toda dependência é um problema — o alvo é evitar acoplamento **desnecessário** com detalhes de infraestrutura ou tecnologia.

## Relações

- [[Cohesion]] — geralmente buscados juntos: baixo acoplamento + alta coesão.
- [[Dependency Inversion]] — principal técnica para reduzir acoplamento com infraestrutura.
- [[Hexagonal Architecture]] — motivação central da arquitetura é reduzir o acoplamento do Core com o mundo externo.

## Referências

- Larman, Craig. *Applying UML and Patterns* — princípios GRASP (Low Coupling / High Cohesion).

---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Component Scanning

## O que é?

Component Scanning é o mecanismo pelo qual o Spring **descobre automaticamente** classes anotadas no classpath e as registra como [[Spring Bean|Beans]] na [[ApplicationContext]], sem exigir declaração explícita de cada uma.

## Annotations envolvidas

`@Component` é a anotação genérica; as demais são especializações semânticas dela, usadas pelo Spring apenas para fins de **registro e, em alguns casos, comportamento adicional do framework** (ex.: `@Repository` habilita tradução de exceções de persistência; `@RestController` combina `@Controller` + `@ResponseBody`):

- `@Component` — genérica.
- `@Service` — especialização usada convencionalmente para lógica de aplicação.
- `@Repository` — especialização usada convencionalmente para acesso a dados; adiciona tradução automática de exceções de persistência.
- `@Controller` / `@RestController` — especialização para camada web (Spring MVC).

## IMPORTANTE: mecanismo de framework ≠ conceito arquitetural

Estas anotações são **mecanismos do Spring para registrar e categorizar componentes no container**. Elas não definem, por si só, responsabilidades arquiteturais como Domain, Use Case, Driving Adapter ou Driven Adapter (conceitos de [[Hexagonal Architecture]]). Uma classe anotada com `@Service` pode ou não corresponder a um Use Case da arquitetura — isso depende do desenho da aplicação, não da anotação em si. Ver discussão detalhada em [[Spring Boot + Hexagonal Architecture]].

| Conceito arquitetural (Hexagonal) | Mecanismo do Spring (registro no container) |
|---|---|
| Independe de framework | Depende do Spring especificamente |
| Define responsabilidade e fronteira | Define apenas como o objeto é descoberto/registrado |
| Ex.: Use Case, Driving Adapter | Ex.: `@Service`, `@RestController` |

## Como funciona

`@SpringBootApplication` (ver [[Spring Boot Application]]) inclui `@ComponentScan`, que instrui o Spring a varrer o pacote da classe principal (e subpacotes) em busca de classes anotadas, registrando-as automaticamente como Beans — sem precisar de um método `@Bean` para cada uma.

## Quando preferir configuração explícita em vez de Component Scanning?

Quando o Bean vem de uma biblioteca externa (que você não pode anotar) ou quando a construção do objeto exige lógica condicional — nesses casos, um método `@Bean` dentro de uma classe `@Configuration` é mais apropriado (ver [[Spring Configuration]]).

## Relações

- [[Spring Bean]]
- [[ApplicationContext]]
- [[Spring Configuration]]
- [[Spring Boot Application]]
- [[Hexagonal Architecture]]

## Referências

- Spring Framework Reference — "Classpath Scanning and Managed Components": https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html

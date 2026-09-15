---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Exception Handling

## O que é?

Mecanismo do Spring MVC para capturar exceções lançadas durante o processamento de uma requisição e traduzi-las para uma resposta HTTP apropriada, tipicamente de forma centralizada via `@ControllerAdvice` + `@ExceptionHandler`, em vez de tratamento espalhado em cada controller.

## Exemplo

```java
@ControllerAdvice
class ApiExceptionHandler {

    @ExceptionHandler(OrderNotConfirmableException.class) // exceção de Domain
    ResponseEntity<ErrorResponse> handle(OrderNotConfirmableException ex) {
        return ResponseEntity.badRequest().body(new ErrorResponse(ex.getMessage()));
    }
}
```

## Fluxo conceitual

```
Domain Exception (regra de negócio violada)
      ↓
Application Boundary (propaga através do Use Case)
      ↓
HTTP Error (traduzida pelo Driving Adapter/exception handler para status code + corpo)
```

## Tipos de erro a distinguir

- **Erros de domínio**: violação de uma regra de negócio (ex.: `OrderNotConfirmableException`) — devem ser exceções próprias do [[Domain]], sem qualquer referência a HTTP.
- **Erros de aplicação**: falha na orquestração do Use Case (ex.: item não encontrado para compor o pedido).
- **Erros técnicos**: falha de infraestrutura (timeout de banco, falha de rede) — normalmente vêm de um [[Adapters|Driven Adapter]].

## Por que não acoplar o Domain a classes de HTTP

Se uma exceção de domínio já carregasse um `HttpStatus`, o Domain passaria a depender de um conceito de infraestrutura (protocolo HTTP), quebrando o isolamento descrito em [[Dependency Rule]]. A tradução de "exceção de domínio" para "código HTTP" é responsabilidade do Adapter (`@ControllerAdvice`), não do Domain — a menos que haja uma justificativa concreta para uma exceção específica não seguir essa regra.

## Relações

- [[Domain]]
- [[Spring REST]]
- [[Dependency Rule]]
- [[Adapters]]

## Referências

- Spring Framework Reference — "Exceptions" (Web MVC): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html

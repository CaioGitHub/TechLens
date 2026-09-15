---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - spring-boot
---

# Spring REST

## O que é?

Suporte do Spring MVC (módulo do Spring Framework, habilitado via `spring-boot-starter-web`) para expor operações de uma aplicação como recursos HTTP, seguindo o estilo REST (recursos identificados por URI, manipulados via métodos HTTP).

## Conceitos REST aplicados (visão de implementação, não um curso de REST)

- **Resource**: uma entidade endereçável por URI (ex.: `/orders/{id}`).
- **HTTP methods**: `GET` (leitura), `POST` (criação), `PUT`/`PATCH` (atualização), `DELETE` (remoção).
- **Status codes**: comunicam o resultado (`200 OK`, `201 Created`, `404 Not Found`, `400 Bad Request`, etc.).
- **Serialization/Deserialization**: conversão automática entre JSON e objetos Java, feita pelo Jackson (trazido pelo starter web) via os conversores de mensagem do Spring MVC.

## @RestController e mapeamentos

```java
@RestController
@RequestMapping("/orders")
class OrderController {

    private final CreateOrderPort createOrder; // Input Port

    OrderController(CreateOrderPort createOrder) {
        this.createOrder = createOrder;
    }

    @PostMapping
    ResponseEntity<Void> create(@RequestBody @Valid CreateOrderRequest request) {
        createOrder.execute(request.toCommand());
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}
```

`@RestController` combina `@Controller` (registra a classe como componente web) e `@ResponseBody` (serializa o retorno diretamente no corpo da resposta, em vez de resolver uma view). `@RequestMapping`/`@GetMapping`/`@PostMapping`/`@PutMapping`/`@DeleteMapping` mapeiam métodos HTTP e caminhos a métodos Java.

## Conexão obrigatória com Arquitetura Hexagonal

```
@RestController
      ↓
Driving Adapter
      ↓
Input Port
      ↓
Use Case
```

Um `@RestController` **desempenha o papel** de [[Adapters|Driving Adapter]]: ele traduz uma requisição HTTP para uma chamada a um [[Ports|Input Port]] do [[Application Core]]. A anotação em si é um mecanismo do Spring para registrar o componente web (ver [[Component Scanning]]) — quem determina que essa classe funciona como Driving Adapter é o **desenho da aplicação**, não a anotação.

## Relações

- [[Adapters]]
- [[Ports]]
- [[DTO]]
- [[Spring Validation]]
- [[Spring Exception Handling]]
- [[Component Scanning]]

## Referências

- Spring Framework Reference — "Web on Servlet Stack": https://docs.spring.io/spring-framework/reference/web/webmvc.html

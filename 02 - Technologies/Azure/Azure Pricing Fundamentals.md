---
type: reference
status: learning
confidence: 35
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Pricing Fundamentals

## Nota temporal

> Preços, tiers e limites específicos mudam com o tempo. Esta nota registra apenas **modelos conceituais de cobrança**, não valores — qualquer valor específico deve ser consultado na calculadora oficial da Microsoft na data da decisão.

## Modelos de cobrança

- **Pay-as-you-go**: paga-se pelo que é consumido, sem compromisso prévio — flexível, mas geralmente o preço unitário mais alto.
- **Consumption**: modelo comum em serviços serverless ([[Azure Functions]], [[Azure Container Apps]] escalando a zero) — cobrança proporcional ao uso real (execuções, tempo de CPU).
- **Reserved capacity**: comprometer-se com um volume/tempo de uso previamente (ex.: 1 ou 3 anos) em troca de desconto significativo sobre o preço pay-as-you-go — adequado para cargas previsíveis e estáveis.
- **Tiers/SKUs**: a maioria dos serviços gerenciados oferece níveis (ex.: Basic, Standard, Premium) com diferentes limites de capacidade, recursos e preço.

## Outros custos frequentemente esquecidos

- **Egress**: tráfego de saída da rede do Azure para a internet costuma ter custo; tráfego de entrada e tráfego dentro da mesma região frequentemente não tem (ou tem custo menor) — variável por serviço e região.
- **Storage costs**: custo de armazenamento pode variar por tier de acesso (ver [[Blob Storage]]) e por redundância escolhida (local vs. geo-redundante).

## Relação com Well-Architected

Custo é um dos cinco pilares do [[Azure Well-Architected Framework]] — a escolha de serviço/tier deve ser avaliada em conjunto com os demais pilares (não apenas "o mais barato").

## Relações

- [[Azure Well-Architected Framework]]
- [[Choosing Azure Compute]]

## Referências

- Microsoft Azure Pricing Calculator (consultar na data da decisão): https://azure.microsoft.com/en-us/pricing/calculator/

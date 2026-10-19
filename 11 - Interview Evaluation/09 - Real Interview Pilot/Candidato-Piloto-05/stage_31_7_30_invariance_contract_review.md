# Stage 31.7.30 — Revisão Adversarial de Invariância de Representação

## 1. Princípio da Invariância de Representação Semântica

A invariância de representação estabelece que o sistema deve produzir a mesma classe de relevância para quaisquer duas formulações discursivas que compartilhem o mesmo valor de verdade técnico e a mesma capacidade resolutiva perante a pergunta:

$$\text{Classificação}(R_1) = \text{Classificação}(R_2) \quad \text{se} \quad \text{Significado}(R_1) \equiv \text{Significado}(R_2)$$

O motor deve ser resistente a variações estilísticas, retóricas, sintáticas e sociolinguísticas que não alterem o conteúdo informacional.

---

## 2. As Oito Famílias de Transformações Discursivas

| Família de Transformação | Exemplo Canônico ($R_1$ vs $R_2$) | Efeito Semântico Real | Comportamento Exigido |
|---|---|---|---|
| **1. Paráfrase Formal** | $R_1$: "Utiliza hash da chave para determinar a partição."<br>$R_2$: "A partição de destino é calculada aplicando-se um algoritmo de dispersão sobre a chave." | Preservação estrita do mecanismo. | **Invariância Obrigatória:** Mesma classe (`DIRECT`). |
| **2. Mudança de Ordem das Orações** | $R_1$: "Abre o circuito se a taxa de erro subir, respondendo com fallback."<br>$R_2$: "Responde com fallback assim que o circuito abrir devido ao aumento na taxa de falhas." | Preservação causal idêntica. | **Invariância Obrigatória:** Mesma classe (`DIRECT`). |
| **3. Variação de Tamanho (Conciso vs Prolixo)** | $R_1$: "Deadlock ocorre quando dois processos retêm recursos mutuamente necessários."<br>$R_2$: "No dia a dia quando temos concorrência pesada em bancos pode acontecer de duas transações travarem porque uma quer a linha que a outra já bloqueou e nenhuma solta." | O conteúdo conceitual é preservado; a versão longa adiciona contexto informal. | **Invariância Obrigatória:** Mesma classe (`DIRECT`). Tamanho não pode ser proxy de nota. |
| **4. Voz Ativa vs Voz Passiva** | $R_1$: "O coordenador envia mensagens de prepare aos participantes."<br>$R_2$: "Mensagens de prepare são transmitidas aos nós participantes pelo coordenador." | Equivalência lógica de papéis semânticos (agente e paciente idênticos). | **Invariância Obrigatória:** Mesma classe (`DIRECT`). |
| **5. Linguagem Coloquial de Engenharia** | $R_1$: "Enfileiramos mensagens no broker assíncrono."<br>$R_2$: "A gente joga tudo numa fila pra não engasgar o backend." | Coloquialismo mantendo a mecânica de nivelamento de carga (load leveling). | **Invariância Obrigatória:** Mesma classe (`DIRECT`). Não penalizar informalidade. |
| **6. Omissão de Repetições Desnecessárias** | $R_1$: "Em um banco de dados relacional, o índice B-tree acelera a busca porque o índice B-tree organiza chaves..."<br>$R_2$: "Ele acelera a busca porque organiza as chaves em árvore balanceada." | Eliminação de redundâncias estilísticas mantendo o conteúdo. | **Invariância Obrigatória:** Mesma classe (`DIRECT`). Anáfora pronominal válida. |
| **7. Substituição por Explicação Conceitual Equivalente** | $R_1$: "Implementamos idempotência com token único de transação."<br>$R_2$: "Cada requisição leva um identificador único conferido em tabela antes de processar." | Implementação concreta da mesma garantia conceitual. | **Invariância Obrigatória:** Mesma classe (`DIRECT`). |
| **8. Inclusão de Preâmbulo Irrelevante sem Contradição** | $R_1$: "O Paxos atinge consenso em duas fases: prepare e accept."<br>$R_2$: "O trânsito estava pesado hoje de manhã. Sobre o Paxos, ele atinge consenso em duas fases: prepare e accept." | O preâmbulo é ruído conversacional inócuo; o cerne técnico é idêntico. | **Invariância Obrigatória:** Mesma classe (`DIRECT`). O ruído não pode contaminar a resposta. |

---

## 3. Demarcação entre Variações Invariantes e Rupturas Semânticas Reais

O sistema deve distinguir com precisão entre uma variação que *preserva* o significado e uma alteração que *destrói* a suficiência ou a polaridade:

```text
                               ┌─────────────────────────────────┐
                               │ Variação Textual sob Avaliação  │
                               └────────────────┬────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
     [Preservação de Conteúdo]                                     [Ruptura Semântica Real]
     - Paráfrase direta                                            - Omissão de demanda obrigatória
     - Voz passiva / ativa                                         - Mudança de polaridade (NÃO / SIM)
     - Coloquialismo de engenharia                                 - Introdução de antítese destrutiva
     - Ruído conversacional isolável                               - Mudança para domínio disjunto
                 │                                                             │
                 ▼                                                             ▼
       (MESMA CLASSE EXIGIDA)                                      (ALTERAÇÃO DE CLASSE OBRIGATÓRIA)
```

### Critério de Auditoria:
Nenhuma alegação de invariância é válida se a transformação omitir uma demanda essencial em pergunta composta (e.g. explicar apenas particionamento e omitir ordenação). Nesse caso, a transição de `DIRECT` para `PARTIAL` é legítima e necessária.

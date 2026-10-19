# Stage 31.7.30 — Revisão de Suficiência e Adequação Relativa à Intenção da Pergunta

## 1. Princípio da Suficiência Dependente da Intenção

Um dos vícios metodológicos superados no Ciclo 6 é a exigência universal de cadeias causais e código de implementação para qualquer tipo de pergunta. A suficiência de uma resposta é uma grandeza **estritamente relativa à intenção epistemológica da pergunta**:

$$\text{Suficiência}(\text{Resposta}) = f(\text{Conteúdo da Resposta}, \text{Intenção da Demanda})$$

Uma resposta não precisa conter linhas de código, comandos SQL ou métricas operacionais para ser classificada como `DIRECT` se a pergunta demandava uma definição formal ou um contraste arquitetural de alto nível.

---

## 2. Matriz dos Dez Modos de Intenção e Critérios de Suficiência

| Modo de Intenção | Pergunta Típica | Critério de Suficiência Plena (`DIRECT`) | O que NÃO Pode ser Exigido | Risco Crítico |
|---|---|---|---|---|
| **1. Definição Conceitual** | *"O que é idempotência em APIs REST?"* | Definição formal rigorosa das propriedades e garantias do conceito. | Código executável, headers HTTP, nomes de frameworks. | Rebaixar para `INSUFFICIENT` por falta de comandos de implementação. |
| **2. Explicação de Mecanismo** | *"Como o MVCC do PostgreSQL funciona?"* | Elucidação dos mecanismos internos (snapshots, tuplas visíveis, xmin/xmax). | Histórico da universidade de criação ou comandos de instalação. | Confundir metadados históricos (`RELATED`) com o mecanismo (`DIRECT`). |
| **3. Comparação Arquitetural** | *"Diferença entre processos e threads?"* | Contraste simétrico dos eixos essenciais (espaço de endereçamento, custo de troca de contexto). | Código em C com fork() ou clone(). | Exigir detalhamento de syscalls em pergunta comparativa teórica. |
| **4. Histórico e Origem** | *"Por que o Linux adotou kernel monolítico?"* | Contextualização histórica legítima e trade-offs da época (overhead de IPC). | Configuração do kernel atual ou patches Git. | Tratar história como irrelevante quando a pergunta era expressamente histórica. |
| **5. Causalidade e Propagação** | *"O que causa cascata de falhas em microsserviços?"* | Identificação do efeito dominó (esgotamento de threads por bloqueio síncrono). | Arquivos yaml de configuração de circuit breaker. | Exigir a solução quando a pergunta pedia a causa do fenômeno. |
| **6. Diagnóstico e Investigação** | *"Como investigar alto consumo de CPU na JVM?"* | Procedimento sistemático de diagnóstico (thread dumps, profiling, correlação de threads com PID). | Solução definitiva do bug antes de analisar os dumps. | Exigir código corrigido em pergunta estritamente investigativa. |
| **7. Implementação / Solução** | *"Como implementar rate limiting no Redis?"* | Algoritmo ou comandos concretos (Sorted Set com timestamps, ZADD, ZREMRANGEBYSCORE). | Demonstração formal de provas matemáticas. | Aceitar apenas ideias vagas sem comandos executáveis. |
| **8. Solução de Problema** | *"Como resolver contenção de locks no Postgres?"* | Ações corretivas aplicáveis (reduzir tempo de transação, índices, ordenar updates). | Análise da árvore sintática do parser do Postgres. | Confundir observabilidade passiva (`SUPPORTING`) com correção (`DIRECT`). |
| **9. Justificativa de Decisão** | *"Por que escolher mensageria assíncrona?"* | Justificativa técnica baseada em desacoplamento temporal e nivelamento de picos (load leveling). | Código de producer/consumer Kafka. | Desqualificar raciocínio arquitetural de negócio. |
| **10. Análise de Trade-offs** | *"Trade-offs entre consistência forte e eventual?"* | Ponderação explícita de latência, disponibilidade (CAP) e complexidade de concorrência. | Escolha dogmática de uma única tecnologia. | Considerar a resposta ambígua (`UNKNOWN`) quando ela pondera trade-offs reais. |

---

## 3. Decomposição de Demandas Compostas e Regras de Cobertura

Para perguntas com múltiplas demandas, a arquitetura deve isolar e hierarquizar os elementos do enunciado:

### 3.1. Tipologia dos Elementos do Enunciado:
1. **Demanda Principal Obrigatória ($D_P$):** Aspecto central sem o qual a resposta não tem mérito (e.g. "Como o Kafka particiona mensagens").
2. **Demanda Secundária Obrigatória ($D_S$):** Segundo aspecto cumulativo requerido (e.g. "E como garante a ordenação na entrega").
3. **Contexto / Cenário ($C$):** Pano de fundo da pergunta (e.g. "Em um ambiente com alto volume de dados"). Não exige resposta isolada.
4. **Exemplo Ilustrativo ($E$):** Casos hipotéticos citados para clareza.
5. **Proposição Contraditória ($P_{contra}$):** Conteúdo que se choca com boas práticas ou afirmações anteriores da própria resposta.

### 3.2. Regra de Agregação de Demandas Compostas ($D_P + D_S$):
- **Se $D_P$ e $D_S$ forem plenamente atendidas:** $\implies \textbf{DIRECT}$
- **Se apenas $D_P$ ou apenas $D_S$ for atendida:** $\implies \textbf{PARTIAL}$
- **Se ambas forem atendidas apenas com observabilidade/telemetria:** $\implies \textbf{SUPPORTING}$
- **Se ambas receberem apenas contexto histórico:** $\implies \textbf{RELATED}$
- **Se houver contradição destrutiva em qualquer demanda:** $\implies \textbf{OFF\_TOPIC}$ (veto de segurança)
- **Se o candidato declarar ignorância em uma e responder a outra:** $\implies \textbf{PARTIAL}$ (o mérito técnico demonstrado prevalece sobre o desconhecimento parcial).

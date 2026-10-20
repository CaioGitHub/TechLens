# Stage 31.7.31 — Contrato Formal de Suficiência da Resposta por Intenção

## 1. Princípio da Demanda Epistemológica

A suficiência técnica de uma resposta mede se as evidências apresentadas pelo candidato atendem aos requisitos necessários e suficientes fixados pela intenção da pergunta.

Não existe um padrão único de resposta ideal:
- Perguntas conceituais exigem rigor definicional, dispensando implementação;
- Perguntas de diagnóstico exigem método investigativo, dispensando correção prévia;
- Perguntas de trade-off exigem ponderação dialética de forças opostas, dispensando dogmatismo.

---

## 2. Matriz Exaustiva dos Modos de Intenção e Critérios de Suficiência

| Modo de Intenção | 1. Suficiente (`DIRECT`) | 2. Parcial (`PARTIAL`) | 3. Auxiliar (`SUPPORTING`) | 4. Temática (`RELATED`) | 5. Insuficiente (`INSUFFICIENT`) | 6. Contradição Invalidante |
|---|---|---|---|---|---|---|
| **Definição / Conceito** | Define formalmente as propriedades e invariantes essenciais. | Cita uma propriedade mas omite a garantia nuclear. | Cita onde o conceito é monitorado. | Cita quem cunhou o termo ou onde é usado. | "É algo importante em TI." | Atribui propriedades opostas (e.g. idempotente altera estado a cada chamada). |
| **Mecanismo Operacional** | Descreve os componentes internos e o fluxo causal de funcionamento. | Explica a entrada e saída sem detalhar o mecanismo interno. | Explica como observar o mecanismo em logs. | Discute o contexto histórico da ferramenta. | Cita nomes de componentes sem explicar o fluxo. | Afirma que o mecanismo faz o inverso da sua função. |
| **Comparação Arquitetural** | Contrasta simetricamente os eixos estruturais de ambos os polos. | Detalha um polo com perfeição e ignora o segundo polo. | Descreve ferramentas comuns aos dois polos. | Cita que ambos pertencem à mesma categoria. | "Um é melhor que o outro." | Inverte os papéis dos polos comparados. |
| **Histórico e Origem** | Elucida a gênese, motivações originais e contexto de criação. | Cita o ano sem explicar as motivações técnicas originais. | Cita repositórios de arquivamento histórico. | Cita a versão atual sem tratar da origem. | "Foi criado há muito tempo." | Afirma autoria manifestamente falsa ou anacrônica. |
| **Causalidade / Propagação** | Identifica a causa-raiz e a cadeia de propagação do efeito. | Identifica o sintoma sem chegar à causa geradora. | Fornece métricas para acompanhar o sintoma. | Cita incidentes famosos relacionados. | "O sistema caiu por sobrecarga." | Afirma que a causa é impossível de acontecer no software. |
| **Diagnóstico / Investigação** | Apresenta método sistemático de isolamento e análise de evidências. | Cita comandos isolados sem linha lógica investigativa. | Configura alertas de estouro de limiar. | Relata experiência genérica com problemas similares. | "Reinicia o pod para ver se volta." | Apaga logs e descarta evidências antes da análise. |
| **Implementação / Código** | Apresenta comandos, assinaturas, algoritmos ou passos executáveis. | Descreve a arquitetura sem os comandos operacionais. | Fornece scripts de teste de carga. | Discute documentação da biblioteca. | "Configura no arquivo de properties." | Comandos com sintaxe destrutiva ou parâmetros invertidos. |
| **Solução de Problema** | Ação corretiva direta que anula a causa-raiz da falha. | Ação paliativa que atenua o impacto sem resolver a causa. | Alertas que avisam quando o problema reincide. | Relata que já viu esse erro em outros projetos. | "Isso depende de reuniões com o time." | Proposta que agrava o problema (e.g. desligar travas). |
| **Justificativa de Decisão** | Fundamenta a escolha técnica em requisitos não-funcionais concretos. | Justifica apenas por gosto pessoal ou simplicidade aparente. | Relata métricas de custo da solução. | Cita que grandes empresas usam essa solução. | "Foi escolhido porque é o padrão da moda." | Justificativa com premissa tecnicamente falsa. |
| **Análise de Trade-offs** | Pondera prós, contras, custos de recurso e complexidade operacional. | Cita apenas as vantagens, omitindo os custos e limitações. | Painéis que comparam custos em nuvem. | Afirma que toda tecnologia tem trade-offs. | "Tudo depende de tudo." | Nega a existência de trade-offs (afirma ser bala de prata). |

---

## 3. Gestão de Demandas Compostas e Aspectos Múltiplos

Perguntas que demandam múltiplos aspectos são decompostas formalmente:

$$\text{Demanda Total } \mathcal{D} = \big\{ D_{P} \big\} \cup \big\{ D_{S_1}, D_{S_2}, \dots \big\} \cup \big\{ \text{Contexto } C \big\} \cup \big\{ \text{Opcionais } O \big\}$$

### Regras de Cobertura e Salvaguardas:
1. **Atendimento Total ($D_P \land D_S$):** Gera $\textbf{DIRECT}$.
2. **Atendimento Parcial ($D_P \land \neg D_S$ ou $\neg D_P \land D_S$):** Gera $\textbf{PARTIAL}$.
   - *Salvaguarda Mandatória:* A ausência de um elemento obrigatório secundário **JAMAIS** rebaixa a resposta para `OFF_TOPIC`. O mérito do aspecto respondido é protegido.
3. **Atendimento de Aspecto Principal com Omissão Declarada:** Se o candidato responde $D_P$ com precisão e diz expressamente *"sobre $D_S$ eu não tenho certeza"*, a classificação é **obrigatoriamente $\textbf{PARTIAL}$**, valorizando a honestidade intelectual e o mérito demonstrado.
4. **Demandas Opcionais / Contexto ($C, O$):** A resposta não é penalizada se não abordar exemplos solicitados como ilustrações periféricas, desde que a demanda conceitual/mecânica principal esteja resolvida.

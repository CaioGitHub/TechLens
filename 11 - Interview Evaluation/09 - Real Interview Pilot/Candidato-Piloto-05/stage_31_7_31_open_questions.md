# Stage 31.7.31 — Questões em Aberto e Limites Tecnológicos Não Demonstrados

## 1. Princípio da Honestidade Epistemológica

A especificação de uma arquitetura refinada não equivale à demonstração empírica de sua viabilidade em código. Este documento delimita com precisão as capacidades exigidas pela especificação, os mecanismos atualmente demonstrados no projeto, as hipóteses cuja viabilidade técnica permanece em aberto e as dependências tecnológicas que exigirão decisão formal de governança antes de qualquer implementação.

---

## 2. Separação Estrita de Capacidades Tecnológicas

| Capacidade Exigida pela Arquitetura | Status Atual no TechLens | Mecanismo Proposto no Ciclo 6 | Limite Conhecido / Questão em Aberto |
|---|:---:|---|---|
| **1. Classificação de Intenção da Pergunta (10 Modos)** | **Implementado e Validado** | `SemanticIntentAndDemandExtractor` baseado em padrões sintáticos determinísticos. | Alta acurácia em perguntas canônicas de entrevista; vulnerável a enunciados prolixos com múltiplas orações interrogativas embutidas. |
| **2. Decomposição de Demandas Compostas ($D_P + D_S$)** | **Implementado e Validado** | Extração estruturada de cláusulas conjuntivas ("e como", "além de"). | Funciona bem para perguntas com marcadores explícitos; pode falhar quando a segunda demanda está em oração subordinada implícita. |
| **3. Isolamento de Preâmbulo Conversacional** | **Parcialmente Demonstrado** | Filtro de sentenças iniciais com marcadores fáticos e de rotina. | Risco de descartar respostas onde o candidato inicia a explicação técnica imediatamente na primeira oração sem preâmbulo. |
| **4. Detecção de Analogias Pedagógicas ($D_V \to D_T$)** | **Apenas Especificado** | Análise de conectivos comparativos e verificação de aterrissagem no domínio de software. | **QUESTÃO NÃO DEMONSTRADA:** Regras determinísticas conseguem separar analogias complexas de divagações puras sem um modelo de linguagem ou parsing sintático profundo? |
| **5. Reconhecimento de Equivalência Aberta e Hiperônimos** | **Apenas Especificado** | Casamento por invariantes conceituais sem exigir repetição de tokens literais. | **LIMITE TECNOLÓGICO CRÍTICO:** Como verificar que "árvore balanceada" é "B-tree" em vocabulário aberto sem manter um dicionário oculto ou usar embeddings vetoriais contextuais? |
| **6. Detecção de Contradições Internas no Discurso** | **Apenas Especificado** | Pareamento de orações com polaridades opostas operando sobre o mesmo objeto. | Risco de falsos positivos em respostas dialéticas maduras que discutem trade-offs e limitações reais de engenharia. |
| **7. Resolução de Homonímia / Polissemia por Predicado** | **Parcialmente Demonstrado** | Detecção de verbos e argumentos alienígenas atuando sobre o termo compartilhado. | Exige discernir se palavras como "mercado", "custo" ou "tráfego" estão sendo usadas em sentido computacional ou do mundo físico. |
| **8. Veto a Antíteses Destrutivas com Salvaguarda** | **Implementado e Validado** | Regexes de verbos destrutivos associadas a guardas de evitação preventiva ("para evitar"). | Altamente robusto e com 100% de passagem nos testes de regressão canônicos. |
| **9. Roteamento Explícito para `RELATED`** | **Pronto para Implementar** | Substituição do sumidouro incondicional `else: OFF_TOPIC` por roteamento para `RELATED`. | Mecânica de agregador puramente lógica, simples, determinística e de baixíssimo risco de regressão. |

---

## 3. As Quatro Grandes Questões em Aberto para Governança

### Questão Aberta 1: Motor Simbólico Puro vs. Hibridismo Vetorial
- *O Dilema:* A generalização semântica aberta (reconhecer paráfrases de tecnologias inéditas e analogias do mundo real) pode ser mantida 100% determinística através de grafos sintáticos e regras formais, ou o sistema exigirá um encoder vetorial contextual (embedding local pequeno ou modelo de linguagem) atuando como oráculo semântico subordinado?
- *Recomendação:* Tentar exaurir a modelagem estruturada de predicados no Ciclo 6 antes de introduzir dependências neurais pesadas, preservando o determinismo e a auditabilidade estrita.

### Questão Aberta 2: Critério de Parada e Granularidade de Conceitos
- *O Dilema:* Até que ponto uma resposta concisa deve ser cobrada por detalhes de implementação? Em perguntas sobre algoritmos de consenso, citar "duas fases com quorum de maiorias" é suficiente para `DIRECT`, ou exige-se detalhar as mensagens específicas de rede (`PrepareRequest`, `PromiseResponse`)?
- *Recomendação:* Adotar o princípio de suficiência essencial: a elucidação do invariante causal do algoritmo confere `DIRECT`; a omissão de detalhes de rede não pode rebaixar a resposta para `INSUFFICIENT` ou `RELATED`.

### Questão Aberta 3: Calibração de Limiares em Respostas Coloquiais
- *O Dilema:* Engenheiros sêniores frequentemente utilizam gírias profissionais ("engasgar o banco", "subir na unha", "matar a thread", "bater no limite"). Como garantir que o filtro de disjunção não confunda gírias operacionais de engenharia com verbos de violência física ou ofícios alienígenas?
- *Recomendação:* O filtro de disjunção deve operar sobre substantivos concretos físicos (argila, cimento, safena, soneto), e não sobre verbos de ação coloquiais que são historicamente polissêmicos na engenharia.

### Questão Aberta 4: Independência Epistemológica do Benchmark (`REFERENCE_INDEPENDENCE_UNRESOLVED`)
- *O Dilema:* O benchmark histórico de 250 casos foi gerado em ciclos anteriores e auditado internamente. Uma acurácia elevada sobre esse conjunto demonstra que o motor é generalizável, ou apenas que ele convergiu com as referências internas?
- *Recomendação de Governança:* **Manter a ressalva `REFERENCE_INDEPENDENCE_UNRESOLVED` inalterada.** A independência metodológica plena só poderá ser atestada quando o sistema for submetido a um comitê duplo-cego externo ou a transcrições reais de candidatos não vistas em desenvolvimento.

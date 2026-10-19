# Stage 31.7.30 — Decisão Arquitetural e Governança do Ciclo 6

## 1. Síntese dos Gates Emitidos

Com base na auditoria forense de integridade e na revisão adversarial independente, emitem-se os seguintes gates formais:

$$\textbf{Gate de Proveniência: RUNTIME\_PROVENANCE\_RECONCILED}$$
$$\textbf{Decisão Arquitetural: ARCHITECTURE\_REQUIRES\_REVISION}$$
$$\textbf{Ressalva Epistemológica Mantida: REFERENCE\_INDEPENDENCE\_UNRESOLVED}$$

---

## 2. Fundamentação da Decisão de Proveniência (`RUNTIME_PROVENANCE_RECONCILED`)

Todas as 9 afirmações e evidências relativas à substituição do alvo de validação foram formalmente verificadas (`VERIFIED`):
1. O runtime avaliado no Stage 31.7.28 foi comprovadamente `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`.
2. Houve autorização explícita e interativa do usuário registrada no início do Stage 31.7.28.
3. A discrepância com `3FD3F80D...` decorreu de um erro administrativo de transcrição após a correção das 5 falhas da suíte canônica no Stage 31.7.27.
4. O diff exato de 84 linhas e 3 blocos funcionais foi auditado linha a linha.
5. A execução comparativa comprovou que os 26 falsos DIRECTs e os 22 falsos OFF_TOPICs são idênticos em ambos os runtimes, demonstrando que as correções de salvaguarda não tiveram qualquer influência sobre o bloqueio semântico do Ciclo 5.

---

## 3. Fundamentação da Decisão Arquitetural (`ARCHITECTURE_REQUIRES_REVISION`)

A proposta de arquitetura do Stage 31.7.29 representa um avanço substantivo ao diagnosticar corretamente a falha das regexes nominais fechadas e o sumidouro indevido de `OFF_TOPIC` no agregador. Contudo, o teste de estresse adversarial identificou regras excessivamente fortes e lacunas contratuais que impedem a aprovação imediata para implementação:

### 3.1. Fragilidades Inaceitáveis Identificadas:
1. **Regra de Veto Absoluto de OFF_TOPIC Refutada por Homonímia e Divagação:**
   A regra *"Se a resposta compartilhar uma entidade com a pergunta, OFF_TOPIC deve ser proibido"* falha no Cenário E (*"Como funciona injeção de dependências no Spring?" $\to$ "A injeção de dependências é importante assim como a dependência econômica de um país em relação às importações"*). O compartilhamento de um token de entidade não pode blindar divagações alienígenas contra `OFF_TOPIC`.
2. **Risco de Falso OFF_TOPIC em Respostas sem Repetição Literal (Falha de Hiperônimos):**
   A exigência de intersecção literal de entidades ($E_R \cap E_Q \neq \emptyset$) falha no Cenário C (*"Como um índice B-tree acelera uma consulta?" $\to$ "A estrutura mantém as chaves ordenadas em uma árvore balanceada..."*). A resposta é 100% `DIRECT`, mas não repete as strings literais "índice" ou "B-tree".
3. **Ausência de Contratos para Analogias Pedagógicas e Ruído Conversacional:**
   A arquitetura não especificava como tratar analogias do mundo real (disjuntor elétrico para Circuit Breaker, Caso STRESS-06) nem preâmbulos conversacionais seguidos de respostas corretas (trânsito antes do Paxos, Caso STRESS-07).
4. **Vulnerabilidade de Elogios Superficiais Citar a Entidade:**
   Frases triviais como *"O PostgreSQL é muito popular"* (Cenário B) seriam promovidas indevidamente a `RELATED` em vez de `INSUFFICIENT` por causa da presença do nome do banco.

---

## 4. O que Precisa Mudar na Arquitetura (Prescrições Mandatórias para o Stage 31.7.31)

Para que a arquitetura possa receber autorização de planejamento de implementação, a especificação deve ser retificada com as seguintes correções estruturais:

1. **Substituir o Veto Absoluto por Presunção Refutável de Conexão Temática:**
   O compartilhamento de entidades gera apenas uma presunção de pertinência temática, que deve ser **refutada** caso os predicados e complementos centrais da oração atuem sobre universos alienígenas (geopolítica, culinária, artesanato).
2. **Incorporar Reconhecimento de Equivalência Funcional e Hiperônimos:**
   O casador de entidades deve reconhecer sinônimos técnicos e hiperônimos canônicos (e.g. "árvore balanceada" $\equiv$ "B-tree", "algoritmo de dispersão" $\equiv$ "hash"), não exigindo identidade estrita de strings.
3. **Instituir Regra de Isenção para Analogias Pedagógicas:**
   Orações subordinadas comparativas (*"funciona como..."*, *"é análogo a..."*) devem ser isoladas, e o teste de pertinência deve avaliar a proposição principal transposta para o software.
4. **Adotar Segmentação Oracional para Isolar Preâmbulos Ruidosos:**
   Períodos conversacionais preliminares (*"O trânsito estava parado..."*) devem ser filtrados, permitindo que a proposição técnica substantiva subsequente seja avaliada em seu mérito real.
5. **Calibrar o Filtro de Substância de Metadados:**
   Exigir dados históricos, institucionais ou organizacionais reais para classificar como `RELATED`, rebaixando elogios vazios ou repetições de chavões para `INSUFFICIENT`.

---

## 5. Próxima Ação Autorizada

- **Stage 31.7.31 — Architectural Remediation & Refined Specification (Cycle 6):**
  Refatorar a especificação arquitetural incorporando as 5 prescrições mandatórias acima, formalizando os novos contratos SC-23 a SC-28, sem implementar código no runtime.

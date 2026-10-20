# Stage 31.7.31 — Contrato de Substância, Metadados e Contribuições Auxiliares

## 1. Princípio da Funcionalidade Relativa do Conteúdo

A distinção entre uma resposta técnica substantiva, uma contribuição auxiliar e um mero metadado **não é uma propriedade intrínseca do texto isolado, mas uma relação funcional entre o conteúdo enunciado e a intenção da pergunta**.

Uma informação factual sobre história, licença, popularidade ou observabilidade pode ser:
- `DIRECT`: quando a pergunta demandava exatamente esse fato;
- `SUPPORTING`: quando a pergunta demandava resolução de problema e o fato atua como instrumentação de apoio;
- `RELATED`: quando a pergunta demandava mecânica de código e o fato apenas contextualiza a ferramenta;
- `INSUFFICIENT`: quando a afirmação é um chavão genérico desprovido de dados avaliáveis.

---

## 2. Tipologia de Conteúdos e Funções Epistêmicas

```text
 ┌────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
 │ Categoria de Conteúdo  │ Papel Funcional perante a Demanda da Pergunta                            │
 ├────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
 │ Resposta Substantiva   │ Atua diretamente sobre o mecanismo causal ou definição central pedida.  │
 │ Atendimento Parcial    │ Resolve substantivamente um dos aspectos, mas deixa outro descoberto.    │
 │ Contribuição Auxiliar  │ Fornece telemetria, logs, alertas ou governança periférica de suporte.  │
 │ Metadado Contextual    │ Cita história, origem, mantenedores, criadores ou licença da ferramenta.│
 │ Filler / Chavão        │ Elogios vazios, chavões de mercado ("é moderno, muito bom") sem fatos. │
 │ Disjunção de Domínio   │ Proposições sobre universos alheios (argila, botânica, culinária).      │
 └────────────────────────┴─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Resolução dos Seis Casos Obrigatórios de Relatividade Funcional

### Caso A: Histórico em Pergunta Operacional
- **Pergunta:** *"Como o PostgreSQL implementa o controle de concorrência multiversão (MVCC)?"*
- **Resposta:** *"O PostgreSQL teve origem no projeto POSTGRES liderado por Michael Stonebraker em Berkeley."*
- **Demanda da Pergunta:** Mecanismo operacional de banco de dados (tuplas, snapshots, visibilidade).
- **Conteúdo da Resposta:** Metadado histórico e institucional.
- **Função Relativa:** O conteúdo compartilha a entidade, mas não atua sobre a demanda de MVCC.
- **Classificação:** $\textbf{RELATED}$ (e NÃO `OFF_TOPIC`, pois a tecnologia é legítima).

### Caso B: Histórico em Pergunta Histórica
- **Pergunta:** *"Qual a origem histórica e acadêmica do PostgreSQL?"*
- **Resposta:** *"O PostgreSQL teve origem no projeto POSTGRES liderado por Michael Stonebraker na Universidade de Berkeley nos anos 80."*
- **Demanda da Pergunta:** Origem histórica e acadêmica.
- **Conteúdo da Resposta:** Exatamente a origem em Berkeley com Stonebraker.
- **Função Relativa:** O metadado histórico é aqui a **demanda substantiva principal**.
- **Classificação:** $\textbf{DIRECT}$ (com confiança máxima).

### Caso C: Popularidade em Pergunta sobre Fatores de Adoção
- **Pergunta:** *"Quais fatores contribuíram para a ampla adoção corporativa do Apache Kafka?"*
- **Resposta:** *"Sua popularidade cresceu devido à capacidade de desacoplar produtores e consumidores em escala massiva, tornando-se o padrão da indústria para arquiteturas orientadas a eventos."*
- **Demanda da Pergunta:** Fatores de adoção e expansão no mercado.
- **Conteúdo da Resposta:** Análise de adoção corporativa e padrão de ecossistema.
- **Função Relativa:** A análise de mercado e popularidade atende diretamente ao enunciado.
- **Classificação:** $\textbf{DIRECT}$

### Caso D: Popularidade / Elogio em Pergunta sobre Mecanismo
- **Pergunta:** *"Como funciona o particionamento de mensagens no Kafka?"*
- **Resposta:** *"O Kafka é uma ferramenta incrível, super popular e muito utilizada por todas as grandes empresas de tecnologia."*
- **Demanda da Pergunta:** Mecânica de particionamento (chaves, hashes, tópicos).
- **Conteúdo da Resposta:** Elogio genérico de mercado / buzzword padding.
- **Função Relativa:** Não apresenta mecanismo técnico nem metadados informativos reais.
- **Classificação:** $\textbf{INSUFFICIENT}$

### Caso E: Observabilidade como Contribuição Auxiliar em Troubleshooting
- **Pergunta:** *"Como diagnosticar e resolver contenção de conexões no pool de banco de dados?"*
- **Resposta:** *"Configuramos alertas de tempo de espera de conexão no Prometheus com dashboards no Grafana."*
- **Demanda da Pergunta:** Diagnóstico e resolução do esgotamento de conexões (dimensionamento, queries lentas, vazamento).
- **Conteúdo da Resposta:** Métricas e alertas passivos.
- **Função Relativa:** Instrumentação de suporte. Ajuda a ver o problema, mas não investiga a causa nem resolve a contenção.
- **Classificação:** $\textbf{SUPPORTING}$

### Caso F: Observabilidade como Demanda Principal
- **Pergunta:** *"Como correlacionar logs, métricas e traces distribuídos para rastrear uma requisição ponta a ponta?"*
- **Resposta:** *"Injetamos um TraceID e SpanID no contexto da requisição com OpenTelemetry, propagando nos headers HTTP e carimbando em cada linha de log estruturado para correlacionar no Jaeger."*
- **Demanda da Pergunta:** Mecanismo de correlação de telemetria (três pilares).
- **Conteúdo da Resposta:** Mecanismo exato de propagação de TraceID e injeção em logs.
- **Função Relativa:** A telemetria aqui é o objeto principal da pergunta.
- **Classificação:** $\textbf{DIRECT}$

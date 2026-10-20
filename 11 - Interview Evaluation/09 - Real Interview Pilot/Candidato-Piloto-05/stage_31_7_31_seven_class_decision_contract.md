# Stage 31.7.31 — Contrato Decisório das Sete Classes Canônicas

## 1. Princípio da Fechadura Ontológica

As sete classes de relevância semântica do TechLens constituem uma partição exaustiva e mutuamente excludente do espaço de avaliação.

**PROIBIÇÃO DE CLASSES GENÉRICAS RESIDUAIS:**
- É terminantemente proibido utilizar `OFF_TOPIC` como consequência automática da ausência de código ou mecanismo operacional;
- É terminantemente proibido utilizar `RELATED` como sumidouro genérico para casos ambíguos ou difíceis;
- É terminantemente proibido utilizar `UNKNOWN` para respostas fracas, lacônicas ou com declarações de ignorância (que pertencem a `INSUFFICIENT`).

---

## 2. As Seis Fronteiras Canônicas de Decisão

```text
       ┌───────────┐         (Omissão de Demanda Obrigatória)         ┌───────────┐
       │  DIRECT   │ ◄──────────────────────────────────────────────► │  PARTIAL  │
       └─────┬─────┘                                                  └─────┬─────┘
             │                                                              │
(Causa-Raiz vs Instrumentação)                               (Resolução Parcial vs Suporte Geral)
             │                                                              │
             ▼                                                              ▼
       ┌───────────┐         (Métricas/Alertas vs Contexto Histórico)  ┌───────────┐
       │SUPPORTING │ ◄──────────────────────────────────────────────► │  RELATED  │
       └─────┬─────┘                                                  └─────┬─────┘
             │                                                              │
(Domínio Técnico vs Universo Alheio)                        (Mesmo Ecossistema vs Domínio Disjunto)
             │                                                              │
             ▼                                                              ▼
       ┌───────────┐         (Divagação Alienígena vs Desconhecimento) ┌───────────┐
       │ OFF_TOPIC │ ◄──────────────────────────────────────────────► │INSUFFICIENT│
       └───────────┘                                                  └─────┬─────┘
                                                                            │
                                                       (Falta de Conteúdo vs Tautologia/Ambiguidade)
                                                                            │
                                                                            ▼
                                                                      ┌───────────┐
                                                                      │  UNKNOWN  │
                                                                      └───────────┘
```

---

### Fronteira 1: `DIRECT` versus `PARTIAL`
- **Pergunta Divisória:** *A resposta satisfaz a totalidade das demandas obrigatórias fixadas pela pergunta, ou deixa lacunas substanciais em elementos mandatórios?*
- **Critério Rígido:** Se a pergunta tiver 1 demanda, satisfação do mecanismo $\to$ `DIRECT`. Se tiver 2 demandas ($D_P + D_S$), o cumprimento de ambas $\to$ `DIRECT`; o cumprimento de apenas uma $\to$ `PARTIAL`.
- **Caso Limítrofe:** O candidato resolve plenamente a demanda principal e aborda a secundária de forma ultra-concisa com 1 termo correto.
  - *Decisão:* Concede `DIRECT` se o termo contiver a propriedade invariante; caso contrário, `PARTIAL`.

### Fronteira 2: `PARTIAL` versus `SUPPORTING`
- **Pergunta Divisória:** *A resposta atua substantivamente sobre o fenômeno central da pergunta (mesmo que em parte dela), ou limita-se a oferecer telemetria, observabilidade e logs passivos?*
- **Critério Rígido:** Se a proposição altera o fluxo do problema ou define o conceito $\to$ `PARTIAL`. Se a proposição apenas monitora ou gera alertas para a falha sem agir sobre a causa $\to$ `SUPPORTING`.
- **Caso Limítrofe:** Em uma pergunta sobre como resolver deadlock, o candidato sugere configurar timeout de lock e monitorar deadlocks no Grafana.
  - *Decisão:* O timeout de lock atua sobre a causa $\to$ `PARTIAL`. O dashboard é secundário. O mérito ativo prevalece.

### Fronteira 3: `SUPPORTING` versus `RELATED`
- **Pergunta Divisória:** *O conteúdo contribui efetivamente como ferramenta auxiliar para a operação do sistema indagado, ou apenas compartilha o ecossistema tecnológico em nível de contexto histórico/institucional?*
- **Critério Rígido:** `SUPPORTING` requer instrumentação utilizável no sistema (Prometheus, OpenTelemetry, Grafana, healthchecks, scripts de load test). `RELATED` descreve fatos contextuais (Berkeley, CNCF, criadores, versão, licença).
- **Caso Limítrofe:** O candidato cita que a documentação oficial da CNCF recomenda boas práticas de pods.
  - *Decisão:* Citar a documentação é metadado institucional $\to$ `RELATED`. Citar a diretiva exata de configuração do pod $\to$ `SUPPORTING` ou `DIRECT`.

### Fronteira 4: `RELATED` versus `OFF_TOPIC`
- **Pergunta Divisória:** *Existe vínculo com o ecossistema e tecnologia de software da pergunta, ou a proposição opera sobre outro ofício humano ou propõe antítese destrutiva?*
- **Critério Rígido:** Se a proposição pertencer ao universo de computação e referenciar a tecnologia legítima da pergunta $\to$ `RELATED` (mesmo sem código). Se pertencer a artesanato, agricultura, medicina ou mandar desativar transações $\to$ `OFF_TOPIC`.
- **Caso Limítrofe:** O candidato fala sobre como o fundador da empresa usava uma metodologia de marcenaria para gerenciar o projeto de software.
  - *Decisão:* Se o núcleo da oração for a marcenaria $\to$ `OFF_TOPIC`. Se for uma analogia de gestão de software $\to$ `RELATED`.

### Fronteira 5: `INSUFFICIENT` versus `UNKNOWN`
- **Pergunta Divisória:** *Houve uma tentativa de resposta onde faltam evidências (desconhecimento, evasão, preenchimento vazio), ou a afirmação é estruturalmente indecidível, ambígua ou tautológica?*
- **Critério Rígido:** Declarações de "não sei", "nunca trabalhei", "depende da reunião da diretoria" ou frases vazias ("é muito bom") $\to$ `INSUFFICIENT`. Tautologias circulares reflexivas ("A replicação replica o que deve ser replicado") e paradoxos não condicionais $\to$ `UNKNOWN`.
- **Caso Limítrofe:** Resposta de 2 palavras: *"Depende, varia."*
  - *Decisão:* Sem critérios condicionais explícitos, trata-se de evasão pura $\to$ `INSUFFICIENT`.

### Fronteira 6: `INSUFFICIENT` versus `OFF_TOPIC`
- **Pergunta Divisória:** *O candidato permaneceu no contexto da entrevista tentando responder sem substância, ou mudou de assunto discorrendo sobre um universo completamente estranho?*
- **Critério Rígido:** Enrolação de entrevista corporativa e declarações de desconhecimento pertencem a `INSUFFICIENT`. Discursos sobre argila, cimento, culinária ou literatura pertencem a `OFF_TOPIC`.
- **Caso Limítrofe:** *"Eu não sei responder sobre Kafka porque na minha vida eu sempre gostei mais de cuidar de plantas."*
  - *Decisão:* A declaração explícita de desconhecimento da demanda técnica prevalece como sinal primário de insuficiência $\to$ `INSUFFICIENT`.

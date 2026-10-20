# Stage 31.7.33 — Registro de Dependências Abertas e Limites Tecnológicos

## 1. Visão Geral da Demarcação de Limites

Em estrita consonância com as regras de governança do TechLens ("Evidência > Impressão" e "Não inventar conhecimento do candidato"), este documento demarca as **capacidades que permanecem formalmente não demonstradas**, as dependências tecnológicas externas e as limitações estruturais que delimitam o escopo da futura implementação no Ciclo 6.

---

## 2. Capacidades Tecnológicas Não Demonstradas

### 2.1. Extração Universal de Papéis Semânticos (SRL) Sem Modelo Neural
- **Estado Atual:** O sistema apoia-se em análise léxico-sintática determinística de estruturas oracionais em português e inglês.
- **Limitação:** Em orações com inversão sintática complexa, elipses severas ou duplo sentido coloquial, um parser simbólico puro pode falhar em determinar com 100% de precisão o sujeito e o objeto direto de um predicado alienígena.
- **Tratamento no Ciclo 6:** Casos ambíguos onde o predicado não puder ser categorizado com alta confiança **NÃO** dispararão refutação de presunção; serão encaminhados para a avaliação de suficiência e, persistindo a dúvida, rotulados com incerteza epistêmica (`UNKNOWN`).

### 2.2. Resolução Aberta Universal de Sinônimos Idiossincráticos
- **Estado Atual:** O motor cobre formalmente os invariantes essenciais de computação (estruturas de dados, algoritmos de consenso, controle de concorrência, particionamento, idempotência).
- **Limitação:** Não é viável codificar deterministicamente todos os termos proprietários ou jargões corporativos de empresas específicas sem um catálogo fechado ou um modelo de embeddings denso.
- **Tratamento no Ciclo 6:** O motor não tentará adivinhar jargões desconhecidos; asserções estruturadas sobre conceitos inéditos que respeitem a lógica interna serão avaliadas pelo mérito mecânico (Caso ADV-04), enquanto termos sem substância serão classificados honestamente como `UNKNOWN`.

---

## 3. Dependências de Governança e Processo

### 3.1. Independência do Benchmark (`REFERENCE_INDEPENDENCE_UNRESOLVED`)
- **Dependência:** Contratação ou formação de um comitê duplo-cego independente com transcrições reais de entrevistas técnicas nunca vistas durante o desenvolvimento.
- **Status:** Esta dependência permanece **ABERTA**. Nenhuma melhoria nas métricas internas do benchmark de 250 casos pode ser utilizada para encerrar essa ressalva.

### 3.2. Desacoplamento do Pipeline Geral de Transcrição
- **Demarcação:** O motor desenvolvido e planejado nos estágios 31.7.x avalia estritamente a relação semântica entre um par `(pergunta, resposta)`.
- **Limitação:** Este motor não resolve erros de diarização, falhas de pontuação de ASR (whisper/transcribe) ou ruídos acústicos de áudio, que pertencem aos estágios anteriores (20.1 a 20.7 do pipeline). A aprovação da arquitetura semântica não convalida o pipeline ponta a ponta de transcrição.

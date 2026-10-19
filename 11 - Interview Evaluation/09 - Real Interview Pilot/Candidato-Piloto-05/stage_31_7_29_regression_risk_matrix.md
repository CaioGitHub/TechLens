# Stage 31.7.29 — Matriz de Riscos de Regressão e Mitigações (Ciclo 6)

## 1. Visão Geral da Análise de Riscos

A transição para a arquitetura do Ciclo 6 (baseada em vinculação de entidades e afinidade tópica aberta) introduz novos pontos de contato entre a extração de demandas e o agregador ontológico. Para evitar que a correção dos 26 falsos `DIRECT` e 22 falsos `OFF_TOPIC` desestabilize comportamentos já homologados, esta matriz mapeia os riscos críticos de regressão e define salvaguardas verificáveis.

---

## 2. Matriz de Riscos Estruturais

| ID | Descrição do Risco | Severidade | Probabilidade | Impacto | Cenário Concreto de Falha | Mitigação Arquitetural Obrigatória |
|:---:|---|:---:|:---:|:---:|---|---|
| **R01** | **Hipersensibilização de Veto (Falso OFF_TOPIC em Domínio Aberto)** | Crítica | Média | Alto | Uma resposta direta a uma pergunta sobre tecnologia inédita (e.g. *QuantumMesh*) ser vetada como `OFF_TOPIC` por não constar no léxico padrão de software. | A disjunção radical só pode ser disparada se houver substantivos concretos de domínios alienígenas identificados ($E_R$ pertence a culinária/botânica/artesanato). A novidade lexical por si só **jamais** gera disjunção. |
| **R02** | **Sub-detecção de Domínios Alienígenas (Persistência de Falso DIRECT)** | Crítica | Média | Alto | Uma resposta sobre outro ofício humano (e.g. alfaiataria, mineração, pilotagem) passar pelo motor por não estar catalogada e ser promovida a `DIRECT`. | Exigir que para receber `FUNCTIONALLY_SOLVES` a proposição deve atuar diretamente sobre as entidades nucleares extraídas da pergunta ($E_Q$). Ação sobre entidades estranhas veta `DIRECT`. |
| **R03** | **Vazamento de Metadados Institucionais para DIRECT** | Média | Baixa | Médio | Uma resposta que apenas cita quem fundou a tecnologia ser promovida a `DIRECT` se contiver verbos ativos como *"criou"* ou *"implementou"*. | Metadados descritivos sobre entidades externas (fundações, pessoas, anos) são ancorados em `THEMATICALLY_ADJACENT` e roteados obrigatoriamente para `RELATED`. |
| **R04** | **Rebaixamento Indevido de Suporte para OFF_TOPIC** | Alta | Baixa | Alto | Respostas de observabilidade (Prometheus/Grafana) serem confundidas com respostas não-operativas e caírem em `OFF_TOPIC`. | O classificador de instrumentalidade de observabilidade opera com precedência hierárquica superior ao fallback de não-operatividade, garantindo fixação em `SUPPORTING`. |
| **R05** | **Quebra de Invariância Sintática (Voz Passiva e Coloquial)** | Média | Baixa | Médio | Paráfrases coloquiais de engenharia (*"A gente joga numa fila..."*) ou voz passiva analítica receberem predições divergentes das versões formais. | Normalização morfológica de lemas verbais e avaliação semântica no nível do nexo de demanda, mantendo paridade nos 20 pares de teste. |
| **R06** | **Disparo Cego de Antítese Destrutiva em Frases de Prevenção** | Crítica | Baixa | Alto | A frase *"Aplicamos locks para evitar desativar travas"* ser marcada como antítese destrutiva por causa do termo *"desativar travas"*. | Manter e expandir a guarda de evitação (`avoidance_guard`) impedindo gatilhos quando precedidos por locuções como *"para evitar"*, *"sem precisar"*, *"nunca"*. |
| **R07** | **Regressão na Suíte Canônica Workspace (1.067 Testes)** | Crítica | Baixa | Extremo | Alterações estruturais quebrarem contratos unitários históricos de stages anteriores (Stages 20 a 31.7.27). | Zero tolerância a regressões. Todo incremento deve validar a suíte canônica integral (`tests/`) e o Reference Harness antes de qualquer aprovação. |

---

## 3. Protocolo de Salvaguardas e Critérios de Parada

Antes de qualquer autorização de implementação no Ciclo 6:
1. **Regra de Isolamento:** Os testes de contrato do Stage 31.7.29 deverão rodar isoladamente sem tocar no código canônico de produção.
2. **Critério de Não-Regressão:** O benchmark histórico de 250 casos e a suíte de 1.067 testes canônicos devem permanecer 100% preservados.
3. **Imutabilidade do Runtime no RCA:** O runtime atual (`6C44B7A8...`) não poderá sofrer nenhuma edição até que a especificação arquitetural seja formalmente revisada e aprovada.

---
type: reference
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-23
  - risk-management
  - rollback-plan
  - cycle-4
---

# Stage 31.7.23 — Plano de Riscos e Procedimentos de Rollback (Cycle 4)

## 1. Visão Geral de Mitigação de Riscos

A refatoração modular do motor `OpenDomainPropositionEngine` em 5 componentes no **Stage 31.7.24** introduz intervenções profundas no fluxo de execução semântica. Para proteger a integridade do projeto e assegurar continuidade sem degradação do Reference Harness, este plano cataloga os riscos técnicos, define gatilhos observáveis de rollback e formaliza o procedimento de restauração imediata.

---

## 2. Catálogo de Riscos Técnicos e Mitigações

| ID | Risco Identificado | Severidade | Probabilidade | Mecanismo de Prevenção / Mitigação |
|---|---|:---:|:---:|---|
| **R-01** | **Regressão na Suíte Canônica ou Harness** | **CRÍTICA** | Média | Execução automatizada da suíte de 1.038 testes e do Reference Harness (15 testes) a cada incremento finalizado. Qualquer falha dispara rollback automático. |
| **R-02** | **Hiper-segmentação de Demandas (Over-segmentation)** | **ALTA** | Média | O parser de demandas não deve fatiar perguntas simples em fragmentos atômicos artificiais; orações explicativas subordinadas não devem virar demandas obrigatórias separadas. |
| **R-03** | **Falsos Positivos de Tautologia Circular** | **ALTA** | Baixa | O analisador de circularidade só dispara `is_circular_tautology = True` se não houver mecanismos técnicos externos substantivos; explicações didáticas preservam `uncertainty = 'BORDERLINE'`. |
| **R-04** | **Hiper-filtragem de Discurso Operativo** | **ALTA** | Média | Relatos de experiência que contenham explicações operacionais detalhadas devem preservar a proposição técnica operativa, isolando apenas a frase autobiográfica introdutória. |
| **R-05** | **Degradação de Latência / Tempo de Execução** | **MÉDIA** | Baixa | O emparelhamento bipartido opera sobre no máximo 3 a 5 demandas e 2 a 4 proposições por caso, mantendo complexidade $O(N \cdot M)$ microscópica ($< 5\text{ ms}$ por caso). |

---

## 3. Gatilhos Observáveis de Rollback por Incremento

O rollback imediato é **mandatório e inegociável** mediante a ocorrência de qualquer um dos seguintes eventos observáveis:

### Gatilhos no Incremento A (Demandas)
- [ ] Qualquer quebra em testes unitários existentes de decomposição de perguntas.
- [ ] Perguntas simples sobre conceitos únicos (ex: "O que é WAL?") gerando mais de uma demanda primária.

### Gatilhos no Incremento B (Nexo Bipartido)
- [ ] Falha em qualquer teste canônico de validação cruzada do Harness.
- [ ] Respostas completas de casos canônicos recebendo `UNMET` por falha de emparelhamento.

### Gatilhos no Incremento C (Discurso e Circularidade)
- [ ] Respostas técnicas legítimas da suíte de teste sendo marcadas como `HISTORICAL_TRIVIA` ou `PERSONAL_DECLARATION`.
- [ ] Tautologias conhecidas falhando nos testes de contrato `TC-03`, `TC-04` ou `TC-05`.

### Gatilhos no Incremento D (Polaridade e Evasão)
- [ ] Respostas preventivas do Grupo I (salvaguarda de evitação) voltando a ser marcadas como `OFF_TOPIC`.
- [ ] Respostas com desconhecimento explícito sendo classificadas erroneamente como `DIRECT`.

### Gatilhos no Incremento E (Agregação Integrada)
- [ ] Menos de 1.037 testes aprovados na suíte de testes unitários.
- [ ] Menos de 15 testes aprovados no Reference Harness.
- [ ] Tempo total de execução do Reference Harness excedendo 45 segundos.

---

## 4. Procedimento Formal de Rollback

Caso um gatilho de rollback seja acionado durante o Stage 31.7.24:

### Passo 1: Interromper a Execução Imediatamente
Não tentar correções sucessivas sobre código quebrado. Interromper imediatamente o script de teste.

### Passo 2: Restaurar o Checkpoint do Incremento Anterior
Executar o comando de restauração a partir do checkpoint recuperável do baseline congelado:
```powershell
# Exemplo de rollback total para o baseline de início do Ciclo 4:
Copy-Item "reference_runtime/runtime.py.stage_31_7_23_baseline" -Destination "reference_runtime/runtime.py" -Force
```

### Passo 3: Auditar o Hash SHA-256 do Runtime Restaurado
Verificar se o hash do arquivo restaurado corresponde perfeitamente ao baseline congelado:
```powershell
py -c "import hashlib; print(hashlib.sha256(open('reference_runtime/runtime.py','rb').read()).hexdigest().upper())"
# Saída esperada: 75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC
```

### Passo 4: Executar a Regressão de Verificação
Confirmar que o ambiente retornou ao estado 100% verde:
```powershell
py -m unittest discover tests
py -m unittest tests.test_stage_26_reference_harness
```

### Passo 5: Registrar a Falha e Diagnosticar em Ambiente Isolado
Registrar a falha no diário de bordo e isolar a implementação do componente em um protótipo em `scratch/` antes de tentar nova aplicação controlada.

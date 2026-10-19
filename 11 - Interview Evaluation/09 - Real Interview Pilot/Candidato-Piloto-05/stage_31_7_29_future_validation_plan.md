# Stage 31.7.29 — Plano Futuro de Implementação e Revalidação Cega (Ciclo 6)

## 1. Sequenciamento Metodológico Rigoroso

Conforme os princípios fundamentais de `AGENTS.md` e a regra de transição deliberada de estágios, a evolução para o Ciclo 6 obedece à seguinte sequência:

```text
Stage 31.7.28 (BLOCKED)
       │
       ▼
Stage 31.7.29 (RCA & Especificação Arquitetural do Ciclo 6)  ◄── ESTÁGIO ATUAL
       │
       ▼
[Revisão Formal e Aprovação de Governança]
       │
       ▼
Stage 31.7.30 (Implementação Controlada dos 5 Incrementos do Ciclo 6)
       │
       ▼
Stage 31.7.31 (Revalidação Semântica Cega Independente — Ciclo 6)
```

---

## 2. Pré-Condições Obrigatórias para o Stage 31.7.30 (Implementação Controlada)

O Stage 31.7.30 **NÃO** pode ser iniciado automaticamente. A autorização formal depende do cumprimento cumulativo de:
1. **Aprovação Formal da Arquitetura do Ciclo 6:** Validação explícita pelo usuário das diretrizes de vinculação de entidades e roteamento do agregador.
2. **Suíte de Testes Contratuais Pré-Codificada:** Criação de `tests/test_stage_31_7_30_contract_tests.py` contendo os 22 cenários contratuais de `stage_31_7_29_semantic_contracts.json`.
3. **Snapshot de Entrada Congelado:** Preservação intacta de `runtime.py.stage_31_7_29_forensic_entry` (SHA-256 `6C44B7A8...`) como linha de base para rollback imediato.

---

## 3. Estrutura do Stage 31.7.31 (Revalidação Semântica Cega — Ciclo 6)

1. **Benchmark 100% Inédito:**
   - Construção de um novo conjunto balanceado de 250 casos (zero sobreposição com as 633 perguntas e 688 respostas dos benchmarks anteriores).
   - Selagem criptográfica prévia de `stage_31_7_31_ground_truth.json` e `stage_31_7_31_blind_input.json`.
2. **Isolamento de Execução:**
   - O runtime executará de forma estritamente cega, consumindo apenas identificadores e textos, sem acesso a referências humanas.
3. **Limiares Formais de Aprovação (Gates do Ciclo 6):**
   - Acurácia Exata Global: $\ge 75,00\%$
   - Recall de `DIRECT`: $\ge 85,00\%$
   - Precisão de `DIRECT`: $\ge 70,00\%$
   - Taxa de Falsos DIRECT entre divergências: $\le 10,00\%$
   - Recall de `PARTIAL`: $\ge 60,00\%$
   - Recall de `RELATED`: $\ge 60,00\%$ (novo limiar específico para proteger contra o rebaixamento para OFF_TOPIC)
   - Paridade de Invariância Pareada: $\ge 80,00\%$
   - Regressões Canônicas no Workspace: **0 (Zero)**
4. **Governança Epistemológica:**
   - Manutenção mandatória da ressalva $\textbf{REFERENCE\_INDEPENDENCE\_UNRESOLVED}$, registrando com total honestidade que o benchmark foi adjudicado internamente até a contratação de comitê externo independente.

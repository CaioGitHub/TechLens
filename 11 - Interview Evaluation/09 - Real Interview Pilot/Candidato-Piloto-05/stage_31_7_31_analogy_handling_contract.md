# Stage 31.7.31 — Contrato de Tratamento de Analogias Pedagógicas entre Domínios

## 1. Princípio da Bipolaridade Analógica

Na comunicação técnica entre engenheiros, o recurso a analogias pedagógicas do mundo físico (e.g. hidráulica para filas, disjuntores residenciais para circuit breakers, tráfego urbano para roteamento de rede) é um padrão legítimo de explicação.

O sistema **não pode tratar a presença de vocabulário de outro domínio como evidência automática de `OFF_TOPIC`**, desde que a oração analógica cumpra o princípio da **Bipolaridade com Aterrissagem Computacional**:

$$\text{Analogia Válida} = \langle \text{Veículo } (D_V), \text{ Alvo } (D_T), \text{ Mapeamento } (D_V \to D_T) \rangle$$

---

## 2. Critérios de Identificação da Função Explicativa

Para que uma menção a outro domínio seja reconhecida como analogia e não como divagação irrelevante, o texto deve apresentar:
1. **Marcadores Discursivos Comparativos de Conexão:**
   - *"funciona como..."*, *"é análogo a..."*, *"se parece com..."*, *"pense como um..."*, *"é a mesma ideia de..."*.
2. **Presença Obrigatória dos Dois Polos:**
   - O polo do domínio-veículo $D_V$ (e.g. "disjuntor da casa");
   - O polo do domínio-alvo computacional $D_T$ (e.g. "chamadas ao serviço", "microsserviço", "requisições").
3. **Isolamento Sintático da Oração Subordinada:**
   - A oração analógica deve ser tratada como um modificador discursivo subordinado, preservando o núcleo resolutivo da oração principal.

---

## 3. Matriz de Avaliação de Padrões Analógicos

| Padrão de Analogia | Descrição Estrutural | Ação Arquitetural | Classificação Resultante |
|---|---|---|:---:|
| **1. Analogia Pertinente com Aterrissagem Completa** | O candidato utiliza a metáfora e em seguida mapeia e explica a mecânica exata no software. | Concede presunção resolutiva plena; avalia o núcleo computacional. | $\textbf{DIRECT}$ |
| **2. Analogia Parcialmente Correta** | A metáfora cobre um aspecto (e.g. abrir o circuito), mas ignora o estado crucial (e.g. transição meio-aberto/half-open). | Registra cobertura parcial de aspectos. | $\textbf{PARTIAL}$ |
| **3. Analogia Desprovida de Aterrissagem (Ungrounded)** | O candidato descreve com perfeição o disjuntor da casa ou o cano de água, mas não explica o que o software faz. | A resposta não resolve a demanda computacional; veta `DIRECT`. | $\textbf{INSUFFICIENT}$ / $\textbf{RELATED}$ |
| **4. Analogia Superficial sem Mecanismo** | Comparação poética ou retórica vazia (*"O Kafka é como o ar que respiramos"*). | Rejeita status de analogia técnica; trata como filler retórico. | $\textbf{INSUFFICIENT}$ |
| **5. Analogia Seguida de Conclusão Errada** | O candidato usa boa analogia, mas a conclusão técnica viola o conceito (*"como disjuntor... então desativamos para não cair"*). | Prevalência da contradição destrutiva; a analogia não salva o erro. | $\textbf{OFF\_TOPIC}$ |
| **6. Divagação Alienígena Disfarçada de Analogia** | O candidato começa comparando com artesanato e passa 3 parágrafos ensinando a queimar argila sem voltar ao software. | Disjunção ontológica confirmada; refuta a analogia. | $\textbf{OFF\_TOPIC}$ |

---

## 4. Salvaguardas Negativas Rígidas

1. **PROIBIDO imunizar erros conceituais com analogias:** Uma resposta que propõe desativar travas transacionais para acelerar o banco continua sendo `OFF_TOPIC` (antítese destrutiva), mesmo que o candidato use a metáfora de "abrir as comportas de uma represa".
2. **PROIBIDO inferir mecanismo por osmose:** Se o candidato explicar como funciona o disjuntor elétrico residencial e parar por aí, o sistema não pode completar a resposta mentalmente. Sem aterrissagem no software, a resposta é insuficiente.
3. **PROIBIDO rebaixar analogias completas para `OFF_TOPIC`:** Se o candidato explicar que o circuit breaker funciona como disjuntor e em seguida descrever a interceptação de chamadas HTTP, o motor **não pode** disparar veto de domínio por causa dos termos "disjuntor", "casa" ou "eletrodoméstico".

---
type: reference
status: unresolved
confidence: 100
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - human-review
  - review-matrix
---

# Stage 30.2 ? Human Review Matrix v4

> This matrix is a presentation artifact only. It does not apply decisions, alter v4, or create v5. Every human decision remains `PENDING`.

## State

```yaml
human_review: BLOCKED
structured_interview_approved: false
source: Pilot Input - Source Transcript v3.md
structured_interview: Structured Interview - Controlled Correction v4.md
downstream: NOT_EXECUTED
```

## Decision rule

Runtime classifications and the text under **Suggested interpretation ? NOT A HUMAN DECISION** are review aids only. The reviewer must choose an option explicitly; silence does not approve, reject, reassign, reconstruct or classify any item.

## Priority legend

- **P0:** speaker attribution, candidate-evidence boundary, question/response linking or evaluation eligibility.
- **P1:** compound questions, follow-ups, candidate-question classification, response segmentation or reconstruction.
- **P2:** peripheral terms, small transcription ambiguity or non-critical warnings.

## Vis?o A ? Detalhada

### P0/P1 ? 24 UNKNOWN/UNLINKED responses

#### U01 ? R2

- **Priority:** P1
- **Response ID:** `R2`
- **Speaker:** Ingrid Mazoni
- **Original text:** Tudo bem.
- **Reconstructed text:** Tudo bem.
- **Source segments:** RAW-009
- **Context before/after:**
- `RAW-008` (01:32) ? **Morais, Michelly Pereira de**: Aí no final a gente vai tirando suas dúvidas e eu explico um pouquinho mais da vaga, tá?
- `RAW-009` (01:36) ? **Ingrid Mazoni**: Tudo bem.
- `RAW-010` (01:38) ? **Morais, Michelly Pereira de**: Bora lá, Caio!
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q1` ? Trabalho aqui no projeto do open finance do Bradesco, tá? Eu divido aqui a coordenação com o Rodrigo, que está aqui. É, você já ouviu falar um pouquinho do projeto open finance?
  - `Q2` ? Beleza. E aí Ingrid, tudo certo? Pra começar, eu queria entender, queria que tu contasse mais ou menos um pouco da tua experiência profissional, qual foram os projetos que tu já atuou, tecnologias, um contexto assim.
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U02 ? R24

- **Priority:** P0
- **Response ID:** `R24`
- **Speaker:** Ingrid Mazoni
- **Original text:** Não, nenhum.
- **Reconstructed text:** Não, nenhum.
- **Source segments:** RAW-048
- **Context before/after:**
- `RAW-047` (06:32) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Um desconforto assim, chamar algumas pessoas para conversar, então tem uma chamar para uma agenda, uma equipe para discutir sobre algum problema que está acontecendo.
- `RAW-048` (06:43) ? **Ingrid Mazoni**: Não, nenhum.
- `RAW-049` (06:46) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q8` ? Camada, mas hexagonal tem conhecimento, já chegou a usar.
  - `Q9` ? Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- **Why runtime marked it unknown:** runtime did not retain a confident question link after a boundary, intervention or conversational exchange.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U03 ? R26

- **Priority:** P0
- **Response ID:** `R26`
- **Speaker:** Ingrid Mazoni
- **Original text:** É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.
- **Reconstructed text:** É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.
- **Source segments:** RAW-052
- **Context before/after:**
- `RAW-051` (07:08) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, é o que a gente usa atualmente, inclusive tem também conhecimento com Azure e as funcionalidades dele, tipo Azure Monitor, o Lego Analytics, ZepSight.
- `RAW-052` (07:22) ? **Ingrid Mazoni**: É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.
- `RAW-053` (07:34) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Mhm.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q9` ? Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
  - `Q10` ? E que tu não tem conhecimento sobre a funcionalidade, como é que tu iria conduzir a investigação?
- **Why runtime marked it unknown:** runtime did not retain a confident question link after a boundary, intervention or conversational exchange.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U04 ? R35

- **Priority:** P1
- **Response ID:** `R35`
- **Speaker:** Ingrid Mazoni
- **Original text:** Tranquilo.
- **Reconstructed text:** Tranquilo.
- **Source segments:** RAW-075
- **Context before/after:**
- `RAW-074` (09:37) ? **Morais, Michelly Pereira de**: É uma área de sustentação, tá? Então, assim, a gente está prevendo mudar esse cenário um pouquinho, tá? Porque hoje a gente faz toda análise e passa para o cliente fazer as corretivas.
- `RAW-075` (10:09) ? **Ingrid Mazoni**: Tranquilo.
- `RAW-076` (10:27) ? **Morais, Michelly Pereira de**: É, mas se tiver a fase da entrevista com eles, pode ficar tranquila, pode vir tranquilo, que é nesse nessa linha mesmo que eles seguem também está e é bem rapidinho também. Não demora, não está.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U05 ? R36

- **Priority:** P1
- **Response ID:** `R36`
- **Speaker:** Ingrid Mazoni
- **Original text:** Tudo bem.
- **Reconstructed text:** Tudo bem.
- **Source segments:** RAW-077
- **Context before/after:**
- `RAW-076` (10:27) ? **Morais, Michelly Pereira de**: É, mas se tiver a fase da entrevista com eles, pode ficar tranquila, pode vir tranquilo, que é nesse nessa linha mesmo que eles seguem também está e é bem rapidinho também. Não demora, não está.
- `RAW-077` (10:41) ? **Ingrid Mazoni**: Tudo bem.
- `RAW-078` (10:43) ? **Morais, Michelly Pereira de**: Você tem alguma dúvida?
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U06 ? R37

- **Priority:** P0
- **Response ID:** `R37`
- **Speaker:** Ingrid Mazoni
- **Original text:** É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?
- **Reconstructed text:** É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?
- **Source segments:** RAW-079
- **Context before/after:**
- `RAW-078` (10:43) ? **Morais, Michelly Pereira de**: Você tem alguma dúvida?
- `RAW-079` (10:45) ? **Ingrid Mazoni**: É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?
- `RAW-080` (10:55) ? **Morais, Michelly Pereira de**: Na vaga, na minha opinião, não. Assim, a gente que nem OA pergunta que o Caio fez de como você é, qual a sua postura mediante as pessoas que você precisa falar? Isso é o mais importante, eu acho.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** runtime did not retain a confident question link after a boundary, intervention or conversational exchange.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U07 ? R38

- **Priority:** P1
- **Response ID:** `R38`
- **Speaker:** Ingrid Mazoni
- **Original text:** Entendi.
- **Reconstructed text:** Entendi.
- **Source segments:** RAW-093
- **Context before/after:**
- `RAW-092` (12:19) ? **Morais, Michelly Pereira de**: Então, nesse estilo, aí eles gostam bastante, sabe? Eles gostam que a gente demonstre isso para eles, tá? Que a gente tem interesse, que a gente consegue fazer.
- `RAW-093` (12:29) ? **Ingrid Mazoni**: Entendi.
- `RAW-094` (12:29) ? **Morais, Michelly Pereira de**: A gente se destaca por esse perfil, tá? E assim, a gente, só para você ter uma ideia, a gente já está com esse cliente, já vai fazer uns 4 anos que a gente vai renovando assim, sem precisar entrar para a concorrência. Então eles estão sempre renovando o contrato com a gente.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U08 ? R39

- **Priority:** P1
- **Response ID:** `R39`
- **Speaker:** Ingrid Mazoni
- **Original text:** Entendi bacana.
- **Reconstructed text:** Entendi bacana.
- **Source segments:** RAW-098
- **Context before/after:**
- `RAW-097` (13:05) ? **Morais, Michelly Pereira de**: Então o pessoal gosta bastante de trabalhar, o pessoal do banco é bem parceiro, é só essa alimentação que a gente tem, que a gente ainda não põe a mão na massa de fato, a gente só faz análise e manda para eles. Mas a gente está tentando mudar isso, sabe? Quebrar essa barreira deles e a gente conseguir colocar a mão também.
- `RAW-098` (13:25) ? **Ingrid Mazoni**: Entendi bacana.
- `RAW-099` (13:30) ? **Morais, Michelly Pereira de**: Mais alguma dúvida?
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U09 ? R40

- **Priority:** P1
- **Response ID:** `R40`
- **Speaker:** Ingrid Mazoni
- **Original text:** É.
- **Reconstructed text:** É.
- **Source segments:** RAW-100
- **Context before/after:**
- `RAW-099` (13:30) ? **Morais, Michelly Pereira de**: Mais alguma dúvida?
- `RAW-100` (13:33) ? **Ingrid Mazoni**: É.
- `RAW-101` (13:34) ? **Morais, Michelly Pereira de**: Pode perguntar, que aqui é o momento.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U10 ? R41

- **Priority:** P1
- **Response ID:** `R41`
- **Speaker:** Ingrid Mazoni
- **Original text:** É o dia a dia.
- **Reconstructed text:** É o dia a dia.
- **Source segments:** RAW-105
- **Context before/after:**
- `RAW-104` (13:41) ? **Morais, Michelly Pereira de**: Você diz o dia a dia?
- `RAW-105` (13:43) ? **Ingrid Mazoni**: É o dia a dia.
- `RAW-106` (13:44) ? **Morais, Michelly Pereira de**: Quer falar, Caio, que você já tá no dia a dia, acho que fica mais fácil, né?
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q11` ? Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** runtime did not retain a confident question link after a boundary, intervention or conversational exchange.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U11 ? R43

- **Priority:** P0
- **Response ID:** `R43`
- **Speaker:** Ingrid Mazoni
- **Original text:** E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?
- **Reconstructed text:** E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?
- **Source segments:** RAW-119
- **Context before/after:**
- `RAW-118` (15:27) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Yes.
- `RAW-119` (15:28) ? **Ingrid Mazoni**: E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?
- `RAW-120` (15:41) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Aqui a gente tem, tem. A gente só não pode fazer consulta em banco de produção, mas log de produção a gente tem acesso.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** runtime did not retain a confident question link after a boundary, intervention or conversational exchange.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U12 ? R44

- **Priority:** P1
- **Response ID:** `R44`
- **Speaker:** Ingrid Mazoni
- **Original text:** Entendi, bacana.
- **Reconstructed text:** Entendi, bacana.
- **Source segments:** RAW-121
- **Context before/after:**
- `RAW-120` (15:41) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Aqui a gente tem, tem. A gente só não pode fazer consulta em banco de produção, mas log de produção a gente tem acesso.
- `RAW-121` (15:53) ? **Ingrid Mazoni**: Entendi, bacana.
- `RAW-122` (15:57) ? **Ingrid Mazoni**: Acho que era isso mesmo de dúvida que eu tinha.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U13 ? R45

- **Priority:** P1
- **Response ID:** `R45`
- **Speaker:** Ingrid Mazoni
- **Original text:** Acho que era isso mesmo de dúvida que eu tinha.
- **Reconstructed text:** Acho que era isso mesmo de dúvida que eu tinha.
- **Source segments:** RAW-122
- **Context before/after:**
- `RAW-121` (15:53) ? **Ingrid Mazoni**: Entendi, bacana.
- `RAW-122` (15:57) ? **Ingrid Mazoni**: Acho que era isso mesmo de dúvida que eu tinha.
- `RAW-123` (16:00) ? **Morais, Michelly Pereira de**: Yeah.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** runtime did not retain a confident question link after a boundary, intervention or conversational exchange.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U14 ? R46

- **Priority:** P1
- **Response ID:** `R46`
- **Speaker:** Ingrid Mazoni
- **Original text:** Tudo bem.
- **Reconstructed text:** Tudo bem.
- **Source segments:** RAW-127
- **Context before/after:**
- `RAW-126` (16:22) ? **Morais, Michelly Pereira de**: É, eu vou com você na entrevista, está eu ou o Rodrigo vai te acompanhar. Você não vai sozinha com o cliente, não está? A gente fica junto.
- `RAW-127` (16:22) ? **Ingrid Mazoni**: Tudo bem.
- `RAW-128` (16:33) ? **Ingrid Mazoni**: Tudo bem?
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U15 ? R47

- **Priority:** P1
- **Response ID:** `R47`
- **Speaker:** Ingrid Mazoni
- **Original text:** Tudo bem?
- **Reconstructed text:** Tudo bem?
- **Source segments:** RAW-128
- **Context before/after:**
- `RAW-127` (16:22) ? **Ingrid Mazoni**: Tudo bem.
- `RAW-128` (16:33) ? **Ingrid Mazoni**: Tudo bem?
- `RAW-129` (16:34) ? **Morais, Michelly Pereira de**: A.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U16 ? R48

- **Priority:** P1
- **Response ID:** `R48`
- **Speaker:** Ingrid Mazoni
- **Original text:** Entendi.
- **Reconstructed text:** Entendi.
- **Source segments:** RAW-135
- **Context before/after:**
- `RAW-134` (17:17) ? **Paes, Caio Victor Pessoa de Vasconcelos**: manualmente nessa parte mas tem alguns projeto que é mais front do que backend só quem foca muito mais na parte de backend
- `RAW-135` (17:29) ? **Ingrid Mazoni**: Entendi.
- `RAW-136` (17:33) ? **Ingrid Mazoni**: Beleza.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U17 ? R49

- **Priority:** P1
- **Response ID:** `R49`
- **Speaker:** Ingrid Mazoni
- **Original text:** Beleza.
- **Reconstructed text:** Beleza.
- **Source segments:** RAW-136
- **Context before/after:**
- `RAW-135` (17:29) ? **Ingrid Mazoni**: Entendi.
- `RAW-136` (17:33) ? **Ingrid Mazoni**: Beleza.
- `RAW-137` (17:34) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Mhm.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U18 ? R50

- **Priority:** P1
- **Response ID:** `R50`
- **Speaker:** Ingrid Mazoni
- **Original text:** Eu estou pensando aqui.
- **Reconstructed text:** Eu estou pensando aqui.
- **Source segments:** RAW-140
- **Context before/after:**
- `RAW-139` (17:40) ? **Morais, Michelly Pereira de**: Mm-hmm.
- `RAW-140` (17:40) ? **Ingrid Mazoni**: Eu estou pensando aqui.
- `RAW-141` (17:45) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Pode ficar a vontade, viu?
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U19 ? R51

- **Priority:** P1
- **Response ID:** `R51`
- **Speaker:** Ingrid Mazoni
- **Original text:** Entendi.
- **Reconstructed text:** Entendi.
- **Source segments:** RAW-146
- **Context before/after:**
- `RAW-145` (18:16) ? **Paes, Caio Victor Pessoa de Vasconcelos**: esses aí no geral mas todos os projetos do swagger
- `RAW-146` (18:22) ? **Ingrid Mazoni**: Entendi.
- `RAW-147` (18:24) ? **Ingrid Mazoni**: E como que chega a demanda para vocês? É, a descrição no card, no Jira, é.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U20 ? R52

- **Priority:** P1
- **Response ID:** `R52`
- **Speaker:** Ingrid Mazoni
- **Original text:** Tem.
- **Reconstructed text:** Tem.
- **Source segments:** RAW-149
- **Context before/after:**
- `RAW-148` (18:33) ? **Paes, Caio Victor Pessoa de Vasconcelos**: É, no caso, aqui no RTB, as demandas é de acordo com o que vem chegando de demanda, de tickets e dentes geral. Tem umas plataformas, Service Desk e o ServiceNow. Cada um vem as coisas diferentes e de acordo com a quantidade que vai chegando, aí vai sendo criado cards no Jira.
- `RAW-149` (18:33) ? **Ingrid Mazoni**: Tem.
- `RAW-150` (18:52) ? **Paes, Caio Victor Pessoa de Vasconcelos**: tem toda a descrição algumas não vem a descrição tão bonitinha mas a
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U21 ? R53

- **Priority:** P1
- **Response ID:** `R53`
- **Speaker:** Ingrid Mazoni
- **Original text:** Entendi.
- **Reconstructed text:** Entendi.
- **Source segments:** RAW-151
- **Context before/after:**
- `RAW-150` (18:52) ? **Paes, Caio Victor Pessoa de Vasconcelos**: tem toda a descrição algumas não vem a descrição tão bonitinha mas a
- `RAW-151` (19:06) ? **Ingrid Mazoni**: Entendi.
- `RAW-152` (19:10) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Mhm.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U22 ? R54

- **Priority:** P1
- **Response ID:** `R54`
- **Speaker:** Ingrid Mazoni
- **Original text:** Acho que eu não tenho mais dúvidas.
- **Reconstructed text:** Acho que eu não tenho mais dúvidas.
- **Source segments:** RAW-153
- **Context before/after:**
- `RAW-152` (19:10) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Mhm.
- `RAW-153` (19:13) ? **Ingrid Mazoni**: Acho que eu não tenho mais dúvidas.
- `RAW-154` (19:17) ? **Morais, Michelly Pereira de**: Tá bom, então.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U23 ? R55

- **Priority:** P1
- **Response ID:** `R55`
- **Speaker:** Ingrid Mazoni
- **Original text:** Eu perguntei bastante coisa, né?
- **Reconstructed text:** Eu perguntei bastante coisa, né?
- **Source segments:** RAW-155
- **Context before/after:**
- `RAW-154` (19:17) ? **Morais, Michelly Pereira de**: Tá bom, então.
- `RAW-155` (19:18) ? **Ingrid Mazoni**: Eu perguntei bastante coisa, né?
- `RAW-156` (19:21) ? **Morais, Michelly Pereira de**: Não, mas tem que perguntar mesmo. É o momento. É importante? É.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

#### U24 ? R56

- **Priority:** P1
- **Response ID:** `R56`
- **Speaker:** Ingrid Mazoni
- **Original text:** Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês.
- **Reconstructed text:** Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês.
- **Source segments:** RAW-163
- **Context before/after:**
- `RAW-162` (19:43) ? **Morais, Michelly Pereira de**: É obrigado aí pela participação. Foi um prazer aí te conhecer, conhecer seu seus conhecimentos e espero que dê certo aí. Torcendo aí para dar certo, viu? Boa sorte.
- `RAW-163` (19:54) ? **Ingrid Mazoni**: Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês.
- `RAW-164` (20:01) ? **Morais, Michelly Pereira de**: Regina.
- **Current question_id:** `unknown`
- **Possible question(s):**
  - `Q12` ? E tem uma Daily também, só nossa, né?
- **Why runtime marked it unknown:** short acknowledgement, closing remark or conversational response was not safely eligible for an evaluation link.
- **Suggested interpretation ? NOT A HUMAN DECISION:** review whether this is a non-evaluable acknowledgement/closing, a candidate question, or a response to the nearest prompt; do not force a link.
- **Human decision:** `PENDING`
- **Options:** A ? Reassign to a question; B ? Reassign to another question; C ? Keep UNKNOWN; D ? Mark as non-evaluable; E ? Other

### P0/P1 ? 12 evaluation questions

#### Q01 ? `Q1`

- **Priority:** P1
- **Question ID:** `Q1`
- **Speaker:** Morais, Michelly Pereira de
- **Question:** Trabalho aqui no projeto do open finance do Bradesco, tá? Eu divido aqui a coordenação com o Rodrigo, que está aqui. É, você já ouviu falar um pouquinho do projeto open finance?
- **Original source:** RAW-002 (00:19)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R1
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Potential contextual, follow-up or compound/conversational content may require classification.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-001` (00:03) ? **Morais, Michelly Pereira de**: É me apresentando aqui, está rapidamente. Aí depois a gente já começa A Entrevista técnica, está? É bom. Eu sou a Michele, trabalho aqui na CAP já há um pouco mais de 16 anos. É.
- `RAW-002` (00:19) ? **Morais, Michelly Pereira de**: Trabalho aqui no projeto do open finance do Bradesco, tá? Eu divido aqui a coordenação com o Rodrigo, que está aqui. É, você já ouviu falar um pouquinho do projeto open finance?
- `RAW-003` (00:35) ? **Ingrid Mazoni**: É muito pouco, bem por cima.

#### Q02 ? `Q2`

- **Priority:** P1
- **Question ID:** `Q2`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Beleza. E aí Ingrid, tudo certo? Pra começar, eu queria entender, queria que tu contasse mais ou menos um pouco da tua experiência profissional, qual foram os projetos que tu já atuou, tecnologias, um contexto assim.
- **Original source:** RAW-011 (01:40)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R3, R4, R6, R7, R8, R9, R10
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-010` (01:38) ? **Morais, Michelly Pereira de**: Bora lá, Caio!
- `RAW-011` (01:40) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Beleza. E aí Ingrid, tudo certo? Pra começar, eu queria entender, queria que tu contasse mais ou menos um pouco da tua experiência profissional, qual foram os projetos que tu já atuou, tecnologias, um contexto assim.
- `RAW-012` (01:43) ? **Ingrid Mazoni**: Tudo bem.

#### Q03 ? `Q3`

- **Priority:** P1
- **Question ID:** `Q3`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?
- **Original source:** RAW-022 (03:42)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R12, R14
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-021` (03:35) ? **Ingrid Mazoni**: É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs.
- `RAW-022` (03:42) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?
- `RAW-023` (03:46) ? **Ingrid Mazoni**: Yes.

#### Q04 ? `Q4`

- **Priority:** P1
- **Question ID:** `Q4`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Perfeito, certo? A versão do Java, ela era qual é 17? Era mais avançada. Tu lembra qual é?
- **Original source:** RAW-029 (03:56)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R16
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-028` (03:55) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Okay.
- `RAW-029` (03:56) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, certo? A versão do Java, ela era qual é 17? Era mais avançada. Tu lembra qual é?
- `RAW-030` (04:05) ? **Ingrid Mazoni**: Era começou com a 8, depois mudou para 17 e agora é 21. O pessoal está migrando tudo, não é?

#### Q05 ? `Q5`

- **Priority:** P1
- **Question ID:** `Q5`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Saberia explicar para mim qual é a diferença entre o produtos e consumes em um API rest?
- **Original source:** RAW-032 (04:27)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R17
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-031` (04:13) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, certo? Eu vou fazer uma perguntinha assim sobre Java, que é a tecnologia que a gente mais usa aqui. Na verdade, no RTB a gente usa praticamente Java a parte backend, então.
- `RAW-032` (04:27) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Saberia explicar para mim qual é a diferença entre o produtos e consumes em um API rest?
- `RAW-033` (04:34) ? **Ingrid Mazoni**: Consumers.

#### Q06 ? `Q6`

- **Priority:** P1
- **Question ID:** `Q6`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Certo, e tu saberia também explicar o que é o JDBC e a função dele na aplicação Java?
- **Original source:** RAW-035 (04:56)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R19
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-034` (04:37) ? **Ingrid Mazoni**: Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila.
- `RAW-035` (04:56) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Certo, e tu saberia também explicar o que é o JDBC e a função dele na aplicação Java?
- `RAW-036` (05:04) ? **Ingrid Mazoni**: O JDBC me vem muito ali a é.

#### Q07 ? `Q7`

- **Priority:** P1
- **Question ID:** `Q7`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Certo, nos projetos que tu já atuou e atua atualmente, vocês usam arquitetura hexagonal ou outro tipo de arquitetura?
- **Original source:** RAW-039 (05:16)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R21
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-038` (05:15) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Mhm.
- `RAW-039` (05:16) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Certo, nos projetos que tu já atuou e atua atualmente, vocês usam arquitetura hexagonal ou outro tipo de arquitetura?
- `RAW-040` (05:28) ? **Ingrid Mazoni**: Ele é mais arquitetura em camadas.

#### Q08 ? `Q8`

- **Priority:** P1
- **Question ID:** `Q8`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Camada, mas hexagonal tem conhecimento, já chegou a usar.
- **Original source:** RAW-041 (05:31)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R22, R23
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Potential contextual, follow-up or compound/conversational content may require classification.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-040` (05:28) ? **Ingrid Mazoni**: Ele é mais arquitetura em camadas.
- `RAW-041` (05:31) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Camada, mas hexagonal tem conhecimento, já chegou a usar.
- `RAW-042` (05:36) ? **Ingrid Mazoni**: Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,

#### Q09 ? `Q9`

- **Priority:** P1
- **Question ID:** `Q9`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- **Original source:** RAW-049 (06:46)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R25
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-048` (06:43) ? **Ingrid Mazoni**: Não, nenhum.
- `RAW-049` (06:46) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- `RAW-050` (06:58) ? **Ingrid Mazoni**: Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos.

#### Q10 ? `Q10`

- **Priority:** P1
- **Question ID:** `Q10`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Question:** E que tu não tem conhecimento sobre a funcionalidade, como é que tu iria conduzir a investigação?
- **Original source:** RAW-055 (07:54)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R27, R29, R31
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Runtime marked this as an evaluation-eligible question; semantic boundary, follow-up status and response eligibility still require human confirmation.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-054` (07:38) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Certo, para fechar aqui, eu tenho uma pergunta que eu gosto de fazer para todas as entrevistas que eu faço. Uma pergunta bem interessante. Assim é, vamos imaginar que tu vai receber um incidente que ninguém está conseguindo resolver ele. Não existe documentação.
- `RAW-055` (07:54) ? **Paes, Caio Victor Pessoa de Vasconcelos**: E que tu não tem conhecimento sobre a funcionalidade, como é que tu iria conduzir a investigação?
- `RAW-056` (08:01) ? **Ingrid Mazoni**: Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando

#### Q11 ? `Q11`

- **Priority:** P1
- **Question ID:** `Q11`
- **Speaker:** Morais, Michelly Pereira de
- **Question:** Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
- **Original source:** RAW-066 (08:46)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R32, R34
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Potential contextual, follow-up or compound/conversational content may require classification.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-065` (08:44) ? **Ingrid Mazoni**: Scroll.
- `RAW-066` (08:46) ? **Morais, Michelly Pereira de**: Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.
- `RAW-067` (09:00) ? **Ingrid Mazoni**: Sim, eu utilizo bastante.

#### Q12 ? `Q12`

- **Priority:** P1
- **Question ID:** `Q12`
- **Speaker:** Morais, Michelly Pereira de
- **Question:** E tem uma Daily também, só nossa, né?
- **Original source:** RAW-113 (15:04)
- **Question type:** technical; kind=interviewer_question
- **Linked response(s):** R42
- **Follow-up/reformulation:** not explicitly represented by the runtime
- **Current status:** identified; evaluation_eligible=True
- **Potential issue:** Potential contextual, follow-up or compound/conversational content may require classification.
- **Human decision:** `PENDING`
- **Options:** A ? MARK_EVALUABLE; B ? MARK_NON_EVALUABLE; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? KEEP_AS_IS; G ? OTHER
- **Context:**
- `RAW-112` (14:57) ? **Paes, Caio Victor Pessoa de Vasconcelos**: A gente vai fazer análise de incidente, PRB, ticket, enfim, e tem muitas partes de comunicação também com eles.
- `RAW-113` (15:04) ? **Morais, Michelly Pereira de**: E tem uma Daily também, só nossa, né?
- `RAW-114` (15:05) ? **Ingrid Mazoni**: You think she?

### P0/P1 ? 5 candidate questions

#### CQ01 ? `CQ1`

- **Priority:** P1
- **Candidate Question ID:** `CQ1`
- **Speaker:** Ingrid Mazoni
- **Original text:** Como que é que?
- **Reconstructed text:** Como que é que?
- **Context:**
- `RAW-101` (13:34) ? **Morais, Michelly Pereira de**: Pode perguntar, que aqui é o momento.
- `RAW-102` (13:35) ? **Ingrid Mazoni**: Como que é que?
- `RAW-103` (13:37) ? **Ingrid Mazoni**: Como que é a equipe de trabalho aí? Como que funciona?
- **Current classification:** candidate_question; candidate_question=True; evaluation_eligible=False
- **Human decision:** `PENDING`
- **Options:** A ? CONFIRM_CANDIDATE_QUESTION; B ? RECLASSIFY; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? OTHER

#### CQ02 ? `CQ2`

- **Priority:** P1
- **Candidate Question ID:** `CQ2`
- **Speaker:** Ingrid Mazoni
- **Original text:** Como que é a equipe de trabalho aí? Como que funciona?
- **Reconstructed text:** Como que é a equipe de trabalho aí? Como que funciona?
- **Context:**
- `RAW-102` (13:35) ? **Ingrid Mazoni**: Como que é que?
- `RAW-103` (13:37) ? **Ingrid Mazoni**: Como que é a equipe de trabalho aí? Como que funciona?
- `RAW-104` (13:41) ? **Morais, Michelly Pereira de**: Você diz o dia a dia?
- **Current classification:** candidate_question; candidate_question=True; evaluation_eligible=False
- **Human decision:** `PENDING`
- **Options:** A ? CONFIRM_CANDIDATE_QUESTION; B ? RECLASSIFY; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? OTHER

#### CQ03 ? `CQ3`

- **Priority:** P1
- **Candidate Question ID:** `CQ3`
- **Speaker:** Ingrid Mazoni
- **Original text:** Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais?
- **Reconstructed text:** Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais?
- **Context:**
- `RAW-130` (16:36) ? **Morais, Michelly Pereira de**: Beleza, mais alguma dúvida?
- `RAW-131` (16:40) ? **Ingrid Mazoni**: Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais?
- `RAW-132` (16:47) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Aqui a gente usa o Java, tem projetos, a minoria é o Java 18, a maioria já tá 21, o Springwood também a gente usa bastante na RTB aqui a parte da Azure, que é a parte de monitoramento.
- **Current classification:** candidate_question; candidate_question=True; evaluation_eligible=False
- **Human decision:** `PENDING`
- **Options:** A ? CONFIRM_CANDIDATE_QUESTION; B ? RECLASSIFY; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? OTHER

#### CQ04 ? `CQ4`

- **Priority:** P1
- **Candidate Question ID:** `CQ4`
- **Speaker:** Ingrid Mazoni
- **Original text:** Como que a como que a como que é a parte de documentação de API de vocês, vocês usam swagger, essas coisas?
- **Reconstructed text:** Como que a como que a como que é a parte de documentação de API de vocês, vocês usam swagger, essas coisas?
- **Context:**
- `RAW-142` (17:46) ? **Morais, Michelly Pereira de**: Pode ficar à vontade, porque aqui é o momento das dúvidas. O cliente não.
- `RAW-143` (17:50) ? **Ingrid Mazoni**: Como que a como que a como que é a parte de documentação de API de vocês, vocês usam swagger, essas coisas?
- `RAW-144` (18:01) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Sim, os projetos usam swagger, todos eles. Agora, quem faz mais a documentação, no caso manual, assim, tipo documentação de código, é mais o as equipes, as VS, pagamento, consentimento.
- **Current classification:** candidate_question; candidate_question=True; evaluation_eligible=False
- **Human decision:** `PENDING`
- **Options:** A ? CONFIRM_CANDIDATE_QUESTION; B ? RECLASSIFY; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? OTHER

#### CQ05 ? `CQ5`

- **Priority:** P1
- **Candidate Question ID:** `CQ5`
- **Speaker:** Ingrid Mazoni
- **Original text:** E como que chega a demanda para vocês? É, a descrição no card, no Jira, é.
- **Reconstructed text:** E como que chega a demanda para vocês? É, a descrição no card, no Jira, é.
- **Context:**
- `RAW-146` (18:22) ? **Ingrid Mazoni**: Entendi.
- `RAW-147` (18:24) ? **Ingrid Mazoni**: E como que chega a demanda para vocês? É, a descrição no card, no Jira, é.
- `RAW-148` (18:33) ? **Paes, Caio Victor Pessoa de Vasconcelos**: É, no caso, aqui no RTB, as demandas é de acordo com o que vem chegando de demanda, de tickets e dentes geral. Tem umas plataformas, Service Desk e o ServiceNow. Cada um vem as coisas diferentes e de acordo com a quantidade que vai chegando, aí vai sendo criado cards no Jira.
- **Current classification:** candidate_question; candidate_question=True; evaluation_eligible=False
- **Human decision:** `PENDING`
- **Options:** A ? CONFIRM_CANDIDATE_QUESTION; B ? RECLASSIFY; C ? SPLIT; D ? MERGE; E ? RECONSTRUCT; F ? OTHER

### P1 ? 13 NEEDS_REVIEW segments

#### NR01 ? `RAW-008`

- **Priority:** P1
- **Review ID:** `NR01`
- **Segment ID:** `RAW-008`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Aí no final a gente vai tirando suas dúvidas e eu explico um pouquinho mais da vaga, tá?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR02 ? `RAW-046`

- **Priority:** P1
- **Review ID:** `NR02`
- **Segment ID:** `RAW-046`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Original:** e com isso a gente acaba que tendo que se comunicar com muitas pessoas assim alguns até que a gente nem conhecia antes então acaba que a gente tem que ter uma comunicação bem ativa entre os projetos tu teria algum é
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR03 ? `RAW-063`

- **Priority:** P1
- **Review ID:** `NR03`
- **Segment ID:** `RAW-063`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Original:** Quer falar mais alguma coisa?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR04 ? `RAW-064`

- **Priority:** P1
- **Review ID:** `NR04`
- **Segment ID:** `RAW-064`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Top Ingrid, com metodologia ágil, você trabalha com o que aí?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR05 ? `RAW-078`

- **Priority:** P1
- **Review ID:** `NR05`
- **Segment ID:** `RAW-078`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Você tem alguma dúvida?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR06 ? `RAW-081`

- **Priority:** P1
- **Review ID:** `NR06`
- **Segment ID:** `RAW-081`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Do que o próprio técnico, porque assim é a gente como sustentação, a gente precisa falar muito com as pessoas, então a gente tem que ser comunicativo. Então eu acho que esse é um ponto que eu acho que pega bastante, sabe?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR07 ? `RAW-089`

- **Priority:** P1
- **Review ID:** `NR07`
- **Segment ID:** `RAW-089`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** É assim, o banco, o cliente, ele gosta muito de da pessoa e a pessoa ser proativa, sabe? Tomar a frente, tipo assim, isso não é minha responsabilidade, mas você levanta a mão, fala, eu consigo, quer que eu faça, posso fazer, sabe?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR08 ? `RAW-099`

- **Priority:** P1
- **Review ID:** `NR08`
- **Segment ID:** `RAW-099`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Mais alguma dúvida?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR09 ? `RAW-104`

- **Priority:** P1
- **Review ID:** `NR09`
- **Segment ID:** `RAW-104`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Você diz o dia a dia?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR10 ? `RAW-106`

- **Priority:** P1
- **Review ID:** `NR10`
- **Segment ID:** `RAW-106`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Quer falar, Caio, que você já tá no dia a dia, acho que fica mais fácil, né?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR11 ? `RAW-130`

- **Priority:** P1
- **Review ID:** `NR11`
- **Segment ID:** `RAW-130`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Beleza, mais alguma dúvida?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR12 ? `RAW-138`

- **Priority:** P1
- **Review ID:** `NR12`
- **Segment ID:** `RAW-138`
- **Speaker:** Morais, Michelly Pereira de
- **Original:** Tem dúvidas?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

#### NR13 ? `RAW-141`

- **Priority:** P1
- **Review ID:** `NR13`
- **Segment ID:** `RAW-141`
- **Speaker:** Paes, Caio Victor Pessoa de Vasconcelos
- **Original:** Pode ficar a vontade, viu?
- **Current reconstruction:** unchanged; no automatic normalization in v4
- **Current confidence:** high
- **Reason for review:** runtime structural classification requires human confirmation (question/intervention/conversational boundary or speaker/evaluation eligibility).
- **Possible interpretations:**
  1. Preserve current runtime classification and warning.
  2. Reclassify the segment as conversational/intervention/non-evaluable or reconstruct only from transcript-supported form.
- **Human decision:** `PENDING`
- **Options:** A ? RESOLVED; B ? KEEP_WARNING; C ? KEEP_UNKNOWN; D ? RECONSTRUCT; E ? KEEP_ORIGINAL; F ? OTHER

### P2 ? Termos t?cnicos amb?guos

#### T01 ? `Beijava`

- **Priority:** P2
- **Original:** Beijava
- **Possible reconstruction:** Java?
- **Context:** - `RAW-022` (03:42) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?
- `RAW-023` (03:46) ? **Ingrid Mazoni**: Yes.
- `RAW-024` (03:49) ? **Ingrid Mazoni**: Beijava.
- `RAW-025` (03:50) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Java, vamos só mexer com o back.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T02 ? `C Sharpe`

- **Priority:** P2
- **Original:** C Sharpe
- **Possible reconstruction:** C#?
- **Context:** - `RAW-021` (03:35) ? **Ingrid Mazoni**: É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs.
- `RAW-022` (03:42) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?
- `RAW-023` (03:46) ? **Ingrid Mazoni**: Yes.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T03 ? `Angula`

- **Priority:** P2
- **Original:** Angula
- **Possible reconstruction:** Angular?
- **Context:** - `RAW-021` (03:35) ? **Ingrid Mazoni**: É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs.
- `RAW-022` (03:42) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?
- `RAW-023` (03:46) ? **Ingrid Mazoni**: Yes.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T04 ? `produtos e consumes`

- **Priority:** P2
- **Original:** produtos e consumes
- **Possible reconstruction:** producers/consumers?
- **Context:** - `RAW-031` (04:13) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, certo? Eu vou fazer uma perguntinha assim sobre Java, que é a tecnologia que a gente mais usa aqui. Na verdade, no RTB a gente usa praticamente Java a parte backend, então.
- `RAW-032` (04:27) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Saberia explicar para mim qual é a diferença entre o produtos e consumes em um API rest?
- `RAW-033` (04:34) ? **Ingrid Mazoni**: Consumers.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T05 ? `dyna trace`

- **Priority:** P2
- **Original:** dyna trace
- **Possible reconstruction:** Dynatrace?
- **Context:** - `RAW-049` (06:46) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- `RAW-050` (06:58) ? **Ingrid Mazoni**: Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos.
- `RAW-051` (07:08) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, é o que a gente usa atualmente, inclusive tem também conhecimento com Azure e as funcionalidades dele, tipo Azure Monitor, o Lego Analytics, ZepSight.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T06 ? `ezure`

- **Priority:** P2
- **Original:** ezure
- **Possible reconstruction:** Azure?
- **Context:** - `RAW-051` (07:08) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, é o que a gente usa atualmente, inclusive tem também conhecimento com Azure e as funcionalidades dele, tipo Azure Monitor, o Lego Analytics, ZepSight.
- `RAW-052` (07:22) ? **Ingrid Mazoni**: É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.
- `RAW-053` (07:34) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Mhm.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T07 ? `Lego Analytics`

- **Priority:** P2
- **Original:** Lego Analytics
- **Possible reconstruction:** Log Analytics?
- **Context:** - `RAW-049` (06:46) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- `RAW-050` (06:58) ? **Ingrid Mazoni**: Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos.
- `RAW-051` (07:08) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, é o que a gente usa atualmente, inclusive tem também conhecimento com Azure e as funcionalidades dele, tipo Azure Monitor, o Lego Analytics, ZepSight.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T08 ? `ZepSight`

- **Priority:** P2
- **Original:** ZepSight
- **Possible reconstruction:** App/observability product name unclear
- **Context:** - `RAW-049` (06:46) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?
- `RAW-050` (06:58) ? **Ingrid Mazoni**: Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos.
- `RAW-051` (07:08) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Perfeito, é o que a gente usa atualmente, inclusive tem também conhecimento com Azure e as funcionalidades dele, tipo Azure Monitor, o Lego Analytics, ZepSight.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

#### T09 ? `Springwood`

- **Priority:** P2
- **Original:** Springwood
- **Possible reconstruction:** Spring Boot?
- **Context:** - `RAW-130` (16:36) ? **Morais, Michelly Pereira de**: Beleza, mais alguma dúvida?
- `RAW-131` (16:40) ? **Ingrid Mazoni**: Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais?
- `RAW-132` (16:47) ? **Paes, Caio Victor Pessoa de Vasconcelos**: Aqui a gente usa o Java, tem projetos, a minoria é o Java 18, a maioria já tá 21, o Springwood também a gente usa bastante na RTB aqui a parte da Azure, que é a parte de monitoramento.
- **Alternative interpretation:** another spoken term, product name or transcription artifact remains possible.
- **Why reconstruction may be safe or unsafe:** safe only if the transcript context makes the referent unambiguous; unsafe if it adds a technology name not actually supported by the audio/text.
- **Current runtime state:** original text preserved; no automatic normalization applied.
- **Human decision:** `PENDING`

### P1 ? Investiga??o da diferen?a 44 ? 47

The preserved v3 artifact records the aggregate count (44) but does not preserve a complete machine-readable response inventory. Therefore the three individual additions cannot be identified deterministically without modifying/replaying the historical v3 implementation. The v4 inventory below is the source for explicit human comparison; no merge or approval is applied.

#### D01 ? candidate additional unit `R2`

- **New response ID:** not provable from preserved v3 inventory; v4 candidate shown for comparison only
- **Source segments:** RAW-009
- **Original text:** Tudo bem.
- **Corresponding old response, if any:** not determinable from the preserved v3 aggregate artifact
- **Reason for new segmentation:** possible intervention separation, acknowledgement isolation or parser boundary; requires v3/v4 unit-level diff
- **Could this be a duplicate?:** UNCERTAIN
- **Human decision:** `PENDING`

#### D02 ? candidate additional unit `R24`

- **New response ID:** not provable from preserved v3 inventory; v4 candidate shown for comparison only
- **Source segments:** RAW-048
- **Original text:** Não, nenhum.
- **Corresponding old response, if any:** not determinable from the preserved v3 aggregate artifact
- **Reason for new segmentation:** possible intervention separation, acknowledgement isolation or parser boundary; requires v3/v4 unit-level diff
- **Could this be a duplicate?:** UNCERTAIN
- **Human decision:** `PENDING`

#### D03 ? candidate additional unit `R26`

- **New response ID:** not provable from preserved v3 inventory; v4 candidate shown for comparison only
- **Source segments:** RAW-052
- **Original text:** É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.
- **Corresponding old response, if any:** not determinable from the preserved v3 aggregate artifact
- **Reason for new segmentation:** possible intervention separation, acknowledgement isolation or parser boundary; requires v3/v4 unit-level diff
- **Could this be a duplicate?:** UNCERTAIN
- **Human decision:** `PENDING`

## Vis?o B ? Matriz compacta

| ID | Tipo | Trecho | Poss?vel v?nculo/interpreta??o ? NOT A HUMAN DECISION | Decis?o |
|---|---|---|---|---|
| U01 / R2 | UNKNOWN | Tudo bem. | Q1, Q2 | PENDING |
| U02 / R24 | UNKNOWN | Não, nenhum. | Q8, Q9 | PENDING |
| U03 / R26 | UNKNOWN | É na parte de ferramentas de observability, não, mas todo o sistema deles está n | Q9, Q10 | PENDING |
| U04 / R35 | UNKNOWN | Tranquilo. | Q11, Q12 | PENDING |
| U05 / R36 | UNKNOWN | Tudo bem. | Q11, Q12 | PENDING |
| U06 / R37 | UNKNOWN | É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem algu | Q11, Q12 | PENDING |
| U07 / R38 | UNKNOWN | Entendi. | Q11, Q12 | PENDING |
| U08 / R39 | UNKNOWN | Entendi bacana. | Q11, Q12 | PENDING |
| U09 / R40 | UNKNOWN | É. | Q11, Q12 | PENDING |
| U10 / R41 | UNKNOWN | É o dia a dia. | Q11, Q12 | PENDING |
| U11 / R43 | UNKNOWN | E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia | Q12 | PENDING |
| U12 / R44 | UNKNOWN | Entendi, bacana. | Q12 | PENDING |
| U13 / R45 | UNKNOWN | Acho que era isso mesmo de dúvida que eu tinha. | Q12 | PENDING |
| U14 / R46 | UNKNOWN | Tudo bem. | Q12 | PENDING |
| U15 / R47 | UNKNOWN | Tudo bem? | Q12 | PENDING |
| U16 / R48 | UNKNOWN | Entendi. | Q12 | PENDING |
| U17 / R49 | UNKNOWN | Beleza. | Q12 | PENDING |
| U18 / R50 | UNKNOWN | Eu estou pensando aqui. | Q12 | PENDING |
| U19 / R51 | UNKNOWN | Entendi. | Q12 | PENDING |
| U20 / R52 | UNKNOWN | Tem. | Q12 | PENDING |
| U21 / R53 | UNKNOWN | Entendi. | Q12 | PENDING |
| U22 / R54 | UNKNOWN | Acho que eu não tenho mais dúvidas. | Q12 | PENDING |
| U23 / R55 | UNKNOWN | Eu perguntei bastante coisa, né? | Q12 | PENDING |
| U24 / R56 | UNKNOWN | Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do pr | Q12 | PENDING |
| Q01 / Q1 | QUESTION | Trabalho aqui no projeto do open finance do Bradesco, tá? Eu divido aqui a coord | responses: R1 | PENDING |
| Q02 / Q2 | QUESTION | Beleza. E aí Ingrid, tudo certo? Pra começar, eu queria entender, queria que tu  | responses: R3, R4, R6, R7, R8, R9, R10 | PENDING |
| Q03 / Q3 | QUESTION | Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharp | responses: R12, R14 | PENDING |
| Q04 / Q4 | QUESTION | Perfeito, certo? A versão do Java, ela era qual é 17? Era mais avançada. Tu lemb | responses: R16 | PENDING |
| Q05 / Q5 | QUESTION | Saberia explicar para mim qual é a diferença entre o produtos e consumes em um A | responses: R17 | PENDING |
| Q06 / Q6 | QUESTION | Certo, e tu saberia também explicar o que é o JDBC e a função dele na aplicação  | responses: R19 | PENDING |
| Q07 / Q7 | QUESTION | Certo, nos projetos que tu já atuou e atua atualmente, vocês usam arquitetura he | responses: R21 | PENDING |
| Q08 / Q8 | QUESTION | Camada, mas hexagonal tem conhecimento, já chegou a usar. | responses: R22, R23 | PENDING |
| Q09 / Q9 | QUESTION | Perfeito é sobre investigação assim de análise, problemas, incidentes no geral,  | responses: R25 | PENDING |
| Q10 / Q10 | QUESTION | E que tu não tem conhecimento sobre a funcionalidade, como é que tu iria conduzi | responses: R27, R29, R31 | PENDING |
| Q11 / Q11 | QUESTION | Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu | responses: R32, R34 | PENDING |
| Q12 / Q12 | QUESTION | E tem uma Daily também, só nossa, né? | responses: R42 | PENDING |
| CQ01 / CQ1 | CANDIDATE QUESTION | Como que é que? | excluded from evaluation by runtime; confirmation pending | PENDING |
| CQ02 / CQ2 | CANDIDATE QUESTION | Como que é a equipe de trabalho aí? Como que funciona? | excluded from evaluation by runtime; confirmation pending | PENDING |
| CQ03 / CQ3 | CANDIDATE QUESTION | Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais? | excluded from evaluation by runtime; confirmation pending | PENDING |
| CQ04 / CQ4 | CANDIDATE QUESTION | Como que a como que a como que é a parte de documentação de API de vocês, vocês  | excluded from evaluation by runtime; confirmation pending | PENDING |
| CQ05 / CQ5 | CANDIDATE QUESTION | E como que chega a demanda para vocês? É, a descrição no card, no Jira, é. | excluded from evaluation by runtime; confirmation pending | PENDING |
| NR01 / RAW-008 | NEEDS_REVIEW | Aí no final a gente vai tirando suas dúvidas e eu explico um pouquinho mais da v | classification/reconstruction pending | PENDING |
| NR02 / RAW-046 | NEEDS_REVIEW | e com isso a gente acaba que tendo que se comunicar com muitas pessoas assim alg | classification/reconstruction pending | PENDING |
| NR03 / RAW-063 | NEEDS_REVIEW | Quer falar mais alguma coisa? | classification/reconstruction pending | PENDING |
| NR04 / RAW-064 | NEEDS_REVIEW | Top Ingrid, com metodologia ágil, você trabalha com o que aí? | classification/reconstruction pending | PENDING |
| NR05 / RAW-078 | NEEDS_REVIEW | Você tem alguma dúvida? | classification/reconstruction pending | PENDING |
| NR06 / RAW-081 | NEEDS_REVIEW | Do que o próprio técnico, porque assim é a gente como sustentação, a gente preci | classification/reconstruction pending | PENDING |
| NR07 / RAW-089 | NEEDS_REVIEW | É assim, o banco, o cliente, ele gosta muito de da pessoa e a pessoa ser proativ | classification/reconstruction pending | PENDING |
| NR08 / RAW-099 | NEEDS_REVIEW | Mais alguma dúvida? | classification/reconstruction pending | PENDING |
| NR09 / RAW-104 | NEEDS_REVIEW | Você diz o dia a dia? | classification/reconstruction pending | PENDING |
| NR10 / RAW-106 | NEEDS_REVIEW | Quer falar, Caio, que você já tá no dia a dia, acho que fica mais fácil, né? | classification/reconstruction pending | PENDING |
| NR11 / RAW-130 | NEEDS_REVIEW | Beleza, mais alguma dúvida? | classification/reconstruction pending | PENDING |
| NR12 / RAW-138 | NEEDS_REVIEW | Tem dúvidas? | classification/reconstruction pending | PENDING |
| NR13 / RAW-141 | NEEDS_REVIEW | Pode ficar a vontade, viu? | classification/reconstruction pending | PENDING |
| T01 | RECONSTRUCTION | Beijava | Java? | PENDING |
| T02 | RECONSTRUCTION | C Sharpe | C#? | PENDING |
| T03 | RECONSTRUCTION | Angula | Angular? | PENDING |
| T04 | RECONSTRUCTION | produtos e consumes | producers/consumers? | PENDING |
| T05 | RECONSTRUCTION | dyna trace | Dynatrace? | PENDING |
| T06 | RECONSTRUCTION | ezure | Azure? | PENDING |
| T07 | RECONSTRUCTION | Lego Analytics | Log Analytics? | PENDING |
| T08 | RECONSTRUCTION | ZepSight | App/observability product name unclear | PENDING |
| T09 | RECONSTRUCTION | Springwood | Spring Boot? | PENDING |
| D01 | RESPONSE COUNT | R2 / Tudo bem. | v3 correspondence unknown; duplication uncertain | PENDING |
| D02 | RESPONSE COUNT | R24 / Não, nenhum. | v3 correspondence unknown; duplication uncertain | PENDING |
| D03 | RESPONSE COUNT | R26 / É na parte de ferramentas de observability, não, mas todo o sistema de | v3 correspondence unknown; duplication uncertain | PENDING |

## Final state

```text
Human Review Matrix prepared.
Pending:
- Unknown/unlinked: 24
- Evaluation questions: 12
- Candidate questions: 5
- Needs Review: 13
- Technical reconstructions: 9
- Response count discrepancies: 3
Structured Interview v5: NOT CREATED
Human Review: BLOCKED
Awaiting explicit human decisions.
```

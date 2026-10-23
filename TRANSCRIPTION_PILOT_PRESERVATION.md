# Verificação de preservação dos trechos reais

Data: 2026-10-23.

Quatro métodos novos em `tests/test_transcription_pilot_preservation.py` verificam as fontes fixadas por hash, os seis trechos confirmados pelo usuário, os dois trechos incorretos sem redação recuperável e o bloqueio de propostas contextuais pendentes. As substituições usadas para desafiar o bloqueio são entradas de teste, não referências de correção aprovadas.

Resultado: 23 testes direcionados (quatro novos e 19 de fidelidade) aprovados; regressão completa 553/553, harness 15/15, sem falhas, erros ou skips. Resultados reais em `TRANSCRIPTION_PILOT_PRESERVATION_RESULTS.json`; runtime e módulo de correção permaneceram inalterados durante a execução.

Os trechos reais são transportados pelo fixture nominal para exercitar reconstrução e encaminhamento. Não se trata de reavaliação da entrevista completa com seu contexto original. Para os seis controles, evidências e avaliações permanecem iguais entre o fixture sem plano e o mesmo fixture com plano sem mudanças; isso verifica invariância no transporte, não a validade dos scores nem fidelidade semântica geral.

Os dois erros permanecem intactos, com estado de incerteza no registro externo `TRANSCRIPTION_PILOT_USER_REVIEW.json`. O fluxo ainda não foi ampliado para carregar essa marcação às evidências e à apresentação da avaliação. Portanto, não foi demonstrada proteção do candidato contra penalização decorrente desses erros.

Próximo incremento recomendado: propagar incerteza de transcrição da fonte às respostas, evidências e apresentação da avaliação, com testes de vínculo, preservação e ausência de inferências. Definir explicitamente como a incerteza afeta a possibilidade de avaliar a passagem, antes de usar o piloto em decisões sobre o candidato; não modificar scores para fazer testes passarem. Esse incremento continua pendente.
